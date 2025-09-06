"""
Tests for AuthApi class.
"""

import pytest
import responses
from unittest.mock import patch, Mock
from clickedu import AuthApi, AppInitResponse, AuthorizationResponse, AppPermissionsResponse
from clickedu.exceptions import APIError, AuthenticationError


class TestAuthApi:
    """Test AuthApi class."""
    
    def test_auth_api_initialization(self, test_config):
        """Test AuthApi initialization."""
        auth_api = AuthApi(test_config)
        
        assert auth_api.config == test_config
        assert auth_api.cookie is None
        assert auth_api.session is not None
        assert "User-Agent" in auth_api.session.headers
    
    @responses.activate
    def test_app_clickedu_init_success(self, test_config):
        """Test successful app initialization."""
        # Mock the response
        responses.add(
            responses.POST,
            f"https://{test_config.domain}/ws/app_clickedu_init.php",
            json={"token": "test_token", "secret": "test_secret"},
            status=200,
            headers={"set-cookie": "PHPSESSID=test_session_id; path=/"}
        )
        
        auth_api = AuthApi(test_config)
        result = auth_api.app_clickedu_init()
        
        assert result is not None
        assert isinstance(result, AppInitResponse)
        assert result.token == "test_token"
        assert result.secret == "test_secret"
        assert auth_api.cookie == "PHPSESSID=test_session_id"
    
    @responses.activate
    def test_app_clickedu_init_failure(self, test_domain):
        """Test app initialization failure."""
        # Mock the response with error
        responses.add(
            responses.POST,
            f"https://{test_domain}/ws/app_clickedu_init.php",
            json={"error": "Invalid credentials"},
            status=400
        )
        
        auth_api = AuthApi(test_domain)
        with pytest.raises(APIError, match="Failed to initialize app"):
            auth_api.app_clickedu_init()
    
    @responses.activate
    def test_authorization_success(self, test_domain):
        """Test successful user authorization."""
        responses.add(
            responses.GET,
            f"https://{test_domain}/authorization.php",
            json={"id_usuari": "test_user_id"},
            status=200
        )
        
        auth_api = AuthApi(test_domain)
        result = auth_api.authorization("test_token", "test_user", "test_pass")
        
        assert result is not None
        assert isinstance(result, AuthorizationResponse)
        assert result.id_usuari == "test_user_id"
    
    @responses.activate
    def test_authorization_failure(self, test_domain):
        """Test user authorization failure."""
        responses.add(
            responses.GET,
            f"https://{test_domain}/authorization.php",
            json={"error": "Invalid credentials"},
            status=401
        )
        
        auth_api = AuthApi(test_domain)
        with pytest.raises(AuthenticationError, match="Failed to authorize user"):
            auth_api.authorization("test_token", "test_user", "test_pass")
    
    @responses.activate
    def test_app_clickedu_permissions_success(self, test_domain):
        """Test successful permissions setting."""
        responses.add(
            responses.POST,
            f"https://{test_domain}/ws/app_clickedu_permissions.php",
            json={"user_id": "test_user_id", "type": 1},
            status=200
        )
        
        auth_api = AuthApi(test_domain)
        auth_api.cookie = "PHPSESSID=test_session_id"
        result = auth_api.app_clickedu_permissions("test_token", "test_user_id")
        
        assert result is not None
        assert isinstance(result, AppPermissionsResponse)
        assert result.user_id == "test_user_id"
        assert result.type == 1
        assert result.error is None
    
    @responses.activate
    def test_app_clickedu_permissions_error(self, test_domain):
        """Test permissions setting with error."""
        responses.add(
            responses.POST,
            f"https://{test_domain}/ws/app_clickedu_permissions.php",
            json={"error": "Permission denied", "msg": "Access denied"},
            status=403
        )
        
        auth_api = AuthApi(test_domain)
        auth_api.cookie = "PHPSESSID=test_session_id"
        with pytest.raises(APIError, match="Failed to set permissions"):
            auth_api.app_clickedu_permissions("test_token", "test_user_id")
    
    @responses.activate
    def test_check_token_success(self, test_domain):
        """Test successful token check."""
        responses.add(
            responses.GET,
            f"https://{test_domain}/ws/app_clickedu_check_token.php",
            json={"status": "valid"},
            status=200
        )
        
        auth_api = AuthApi(test_domain)
        auth_api.cookie = "PHPSESSID=test_session_id"
        result = auth_api.check_token("test_token")
        
        assert result is not None
        assert result["status"] == "valid"
    
    @responses.activate
    def test_check_token_failure(self, test_domain):
        """Test token check failure."""
        responses.add(
            responses.GET,
            f"https://{test_domain}/ws/app_clickedu_check_token.php",
            json={"error": "Invalid token"},
            status=401
        )
        
        auth_api = AuthApi(test_domain)
        auth_api.cookie = "PHPSESSID=test_session_id"
        with pytest.raises(APIError, match="Failed to check token"):
            auth_api.check_token("test_token")
    
    def test_set_cookie(self, test_domain):
        """Test cookie setting."""
        auth_api = AuthApi(test_domain)
        auth_api.set_cookie("PHPSESSID=test_session_id")
        
        assert auth_api.cookie == "PHPSESSID=test_session_id"
        assert auth_api.session.cookies.get("PHPSESSID") == "test_session_id"
    
    def test_get_cookie_header_success(self, test_domain):
        """Test getting cookie header when cookie is set."""
        auth_api = AuthApi(test_domain)
        auth_api.cookie = "PHPSESSID=test_session_id"
        
        header = auth_api.get_cookie_header()
        assert header == {"Cookie": "PHPSESSID=test_session_id"}
    
    def test_get_cookie_header_no_cookie(self, test_domain):
        """Test getting cookie header when no cookie is set."""
        auth_api = AuthApi(test_domain)
        
        with pytest.raises(AuthenticationError, match="Cookie not set"):
            auth_api.get_cookie_header()
    
    def test_app_clickedu_permissions_no_cookie(self, test_domain):
        """Test permissions setting without cookie."""
        auth_api = AuthApi(test_domain)
        
        with pytest.raises(AuthenticationError, match="Cookie not set"):
            auth_api.app_clickedu_permissions("test_token", "test_user_id")
    
    def test_check_token_no_cookie(self, test_domain):
        """Test token check without cookie."""
        auth_api = AuthApi(test_domain)
        
        with pytest.raises(AuthenticationError, match="Cookie not set"):
            auth_api.check_token("test_token")
