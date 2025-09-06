"""
ClickEdu API for authentication.
"""

import requests
from typing import Optional
from ..models import TokenResponse, ValidateResponse
from ..exceptions import AuthenticationError, APIError
from ..utils.logger import setup_logger


class ClickeduApi:
    """ClickeduApi class for handling ClickEdu API operations."""
    
    def __init__(self, config_or_domain):
        """
        Initialize ClickeduApi.
        
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
        self.logger = setup_logger("clickedu.api")
        
        # Set default headers
        self.session.headers.update({
            'User-Agent': self.config.get_user_agent()
        })
    
    def token(self, username: str, password: str) -> Optional[TokenResponse]:
        """Get access token."""
        url = f"{self.config.api_base_url}/login/v1/auth/token"
        
        data = {
            "grant_type": "password",
            "client_id": "32",
            "client_secret": self.config.client_secret,
            "username": username,
            "password": password
        }
        
        headers = self.config.get_api_headers()
        
        try:
            self.logger.info(f"Getting access token for user: {username}")
            response = self.session.post(url, data=data, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            token_response = TokenResponse(
                access_token=result.get("access_token", "")
            )
            
            self.logger.info("Access token obtained!")
            return token_response
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error getting token: {e}")
            if hasattr(e, 'response') and e.response is not None:
                self.logger.error(f"Response status: {e.response.status_code}")
                self.logger.error(f"Response content: {e.response.text}")
            raise AuthenticationError(f"Failed to get access token: {e}") from e
    
    def validate(self, access_token: str, child_id: str) -> Optional[ValidateResponse]:
        """Validate access token."""
        url = f"{self.config.api_base_url}/login/v1/auth/token/validate"
        
        params = {
            "oauth_token": access_token,
            "child_id": child_id
        }
        
        headers = self.config.get_api_headers()
        headers["Authorization"] = f"Bearer {access_token}"
        
        try:
            self.logger.info("Validating access token...")
            response = self.session.get(url, params=params, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            validate_response = ValidateResponse(
                id=result.get("id", ""),
                user_id=result.get("user_id", 0)
            )
            
            self.logger.info("Token validation successful!")
            return validate_response
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error validating token: {e}")
            if hasattr(e, 'response') and e.response is not None:
                self.logger.error(f"Response status: {e.response.status_code}")
                self.logger.error(f"Response content: {e.response.text}")
            raise AuthenticationError(f"Failed to validate token: {e}") from e
