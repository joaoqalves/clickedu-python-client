"""
Authentication API for ClickEdu.
"""

import requests
from typing import Optional, Dict, Any
from ..models import AppInitResponse, AuthorizationResponse, AppPermissionsResponse
from ..exceptions import AuthenticationError, APIError
from ..utils.logger import setup_logger


class AuthApi:
    """AuthApi class for handling authentication operations."""
    
    def __init__(self, config_or_domain):
        """
        Initialize AuthApi.
        
        Args:
            config_or_domain: Configuration object or domain string (for backward compatibility)
        """
        # Backward compatibility: accept domain string
        if isinstance(config_or_domain, str):
            from ..config import Config
            self.config = Config(domain=config_or_domain)
        else:
            self.config = config_or_domain
            
        self.session = requests.Session()
        self.cookie: Optional[str] = None
        self.logger = setup_logger("clickedu.auth")
        
        # Set default headers
        self.session.headers.update(self.config.get_default_headers())
    
    def app_clickedu_init(self) -> Optional[AppInitResponse]:
        """Initialize app tokens."""
        url = f"{self.config.base_url}/ws/app_clickedu_init.php"
        
        data = {
            "cons_key": self.config.cons_key,
            "cons_secret": self.config.cons_secret
        }
        
        try:
            self.logger.info("Initializing app tokens...")
            response = self.session.post(url, data=data)
            response.raise_for_status()
            
            # Extract cookie from response
            cookies_header = response.headers.get('set-cookie')
            if cookies_header:
                # Get the first cookie
                php_cookie = cookies_header.split(';')[0] if isinstance(cookies_header, str) else cookies_header[0].split(';')[0]
                self.set_cookie(php_cookie)
                self.logger.debug(f"Cookie set: {php_cookie[:20]}...")
            
            result = response.json()
            init_response = AppInitResponse(
                token=result.get("token", ""),
                secret=result.get("secret", "")
            )
            
            self.logger.info("App init successful!")
            return init_response
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error in app_clickedu_init: {e}")
            if hasattr(e, 'response') and e.response is not None:
                self.logger.error(f"Response status: {e.response.status_code}")
                self.logger.error(f"Response content: {e.response.text}")
            raise APIError(f"Failed to initialize app: {e}", e.response.status_code if hasattr(e, 'response') and e.response else None) from e
    
    def set_cookie(self, cookie: str) -> None:
        """Set the cookie for subsequent requests."""
        self.cookie = cookie
        self.session.cookies.set('PHPSESSID', cookie.split('=')[1] if '=' in cookie else cookie)
    
    def authorization(self, access_token: str, user: str, password: str) -> Optional[AuthorizationResponse]:
        """Authorize user with access token."""
        url = f"{self.config.base_url}/authorization.php"
        
        params = {
            "access_token": access_token,
            "user": user,
            "pass": password
        }
        
        try:
            self.logger.info(f"Authorizing user: {user}")
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            result = response.json()
            auth_response = AuthorizationResponse(
                id_usuari=result.get("id_usuari", "")
            )
            
            self.logger.info("Authorization successful!")
            return auth_response
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error in authorization: {e}")
            if hasattr(e, 'response') and e.response is not None:
                self.logger.error(f"Response status: {e.response.status_code}")
                self.logger.error(f"Response content: {e.response.text}")
            raise AuthenticationError(f"Failed to authorize user: {e}") from e
    
    def app_clickedu_permissions(self, token: str, user_id: str) -> Optional[AppPermissionsResponse]:
        """Set app permissions."""
        url = f"{self.config.base_url}/ws/app_clickedu_permissions.php"
        
        data = {
            "resource": "[0,1]",
            "oauth_token": token,
            "acceptar": "1",
            "id_usr": user_id,
            "es_webapp": "false"
        }
        
        try:
            self.logger.info(f"Setting permissions for user ID: {user_id}")
            response = self.session.post(url, data=data, headers=self.get_cookie_header())
            response.raise_for_status()
            
            result = response.json()
            permissions_response = AppPermissionsResponse(
                error=result.get("error"),
                msg=result.get("msg"),
                user_id=result.get("user_id"),
                type=result.get("type")
            )
            
            if permissions_response.error is None:
                self.logger.info("Permissions set successfully!")
            else:
                self.logger.warning(f"Error setting permissions: {permissions_response.msg}")
            
            return permissions_response
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error in app_clickedu_permissions: {e}")
            if hasattr(e, 'response') and e.response is not None:
                self.logger.error(f"Response status: {e.response.status_code}")
                self.logger.error(f"Response content: {e.response.text}")
            raise APIError(f"Failed to set permissions: {e}", e.response.status_code if hasattr(e, 'response') and e.response else None) from e
    
    def check_token(self, auth_token: str) -> Optional[Dict[str, Any]]:
        """Check token validity."""
        url = f"{self.config.base_url}/ws/app_clickedu_check_token.php"
        
        params = {
            "version": "2",
            "nom": "ClickEdu Python",
            "platform": "Android",
            "token": auth_token
        }
        
        try:
            self.logger.info("Checking token...")
            response = self.session.get(url, params=params, headers=self.get_cookie_header())
            response.raise_for_status()
            
            result = response.json()
            self.logger.info("Token check successful!")
            return result
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error in check_token: {e}")
            if hasattr(e, 'response') and e.response is not None:
                self.logger.error(f"Response status: {e.response.status_code}")
                self.logger.error(f"Response content: {e.response.text}")
            raise APIError(f"Failed to check token: {e}", e.response.status_code if hasattr(e, 'response') and e.response else None) from e
    
    def get_cookie_header(self) -> Dict[str, str]:
        """Get cookie header for requests."""
        if self.cookie is None:
            raise AuthenticationError("Cookie not set! Call app_clickedu_init first!")
        
        return {"Cookie": self.cookie}
