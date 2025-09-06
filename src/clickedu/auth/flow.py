"""
Authentication flow for ClickEdu API client.
"""

from typing import Optional
from ..models import User
from ..exceptions import AuthenticationError, APIError
from ..utils.logger import setup_logger
from .auth_api import AuthApi
from .clickedu_api import ClickeduApi


def get_user(web_url: str, username: str, password: str, config=None) -> Optional[User]:
    """
    Get user following the TypeScript flow.
    
    Args:
        web_url: The web URL (domain) for the ClickEdu instance
        username: Username for authentication
        password: Password for authentication
        config: Configuration object (optional, will create one if not provided)
        
    Returns:
        User object with all authentication data or None if failed
        
    Raises:
        AuthenticationError: If authentication fails
        APIError: If API requests fail
    """
    logger = setup_logger("clickedu.flow")
    
    try:
        logger.info(f"Starting getUser flow for {web_url}")
        
        # Use provided config or create new one
        if config is None:
            from ..config import Config
            config = Config(domain=web_url)
        
        # Step 1: Initialize AuthApi and get tokens
        auth_api = AuthApi(config)
        init_result = auth_api.app_clickedu_init()
        if not init_result:
            raise AuthenticationError("Failed to initialize app tokens")
        
        # Step 2: Authorize user
        auth_result = auth_api.authorization(init_result.token, username, password)
        if not auth_result:
            raise AuthenticationError("Failed to authorize user")
        
        # Step 3: Set permissions
        permissions_result = auth_api.app_clickedu_permissions(init_result.token, auth_result.id_usuari)
        if not permissions_result:
            raise AuthenticationError("Failed to set permissions")
        
        # Step 4: Get access token from ClickeduApi
        clickedu_api = ClickeduApi(config)
        token_result = clickedu_api.token(username, password)
        if not token_result:
            raise AuthenticationError("Failed to get access token")
        
        # Step 5: Validate token
        validate_result = clickedu_api.validate(token_result.access_token, auth_result.id_usuari)
        if not validate_result:
            raise AuthenticationError("Failed to validate token")
        
        # Step 6: Check token (optional, continue even if fails)
        try:
            check_result = auth_api.check_token(init_result.token)
            if not check_result:
                logger.warning("Token check failed, but continuing...")
        except Exception as e:
            logger.warning(f"Token check failed: {e}, but continuing...")
        
        # Create and return User object
        user = User(
            id=validate_result.id,
            user_id=validate_result.user_id,
            child_id=auth_result.id_usuari,
            base_url=web_url,
            auth_token=init_result.token,
            secret_token=init_result.secret,
            access_token=token_result.access_token
        )
        
        logger.info("getUser flow completed successfully!")
        return user
        
    except (AuthenticationError, APIError):
        # Re-raise known exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error in getUser flow: {e}")
        raise AuthenticationError(f"Unexpected error in authentication flow: {e}") from e
