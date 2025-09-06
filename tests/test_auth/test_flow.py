"""
Tests for the main authentication flow (get_user function).
"""

import pytest
import responses
from unittest.mock import patch, Mock
from clickedu import get_user, User
from clickedu.exceptions import APIError, AuthenticationError


class TestGetUserFlow:
    """Test the main get_user authentication flow."""
    
    @responses.activate
    def test_get_user_success(self, test_domain, test_credentials):
        """Test successful user authentication flow."""
        # Mock all the required API calls
        responses.add(
            responses.POST,
            f"https://{test_domain}/ws/app_clickedu_init.php",
            json={"token": "test_token", "secret": "test_secret"},
            status=200,
            headers={"set-cookie": "PHPSESSID=test_session_id; path=/"}
        )
        
        responses.add(
            responses.GET,
            f"https://{test_domain}/authorization.php",
            json={"id_usuari": "test_user_id"},
            status=200
        )
        
        responses.add(
            responses.POST,
            f"https://{test_domain}/ws/app_clickedu_permissions.php",
            json={"user_id": "test_user_id", "type": 1},
            status=200
        )
        
        responses.add(
            responses.POST,
            "https://api.clickedu.eu/login/v1/auth/token",
            json={"access_token": "test_access_token"},
            status=200
        )
        
        responses.add(
            responses.GET,
            "https://api.clickedu.eu/login/v1/auth/token/validate",
            json={"id": "test_id", "user_id": 12345},
            status=200
        )
        
        responses.add(
            responses.GET,
            f"https://{test_domain}/ws/app_clickedu_check_token.php",
            json={"status": "valid"},
            status=200
        )
        
        result = get_user(test_domain, test_credentials["username"], test_credentials["password"])
        
        assert result is not None
        assert isinstance(result, User)
        assert result.id == "test_id"
        assert result.user_id == 12345
        assert result.child_id == "test_user_id"
        assert result.base_url == test_domain
        assert result.auth_token == "test_token"
        assert result.secret_token == "test_secret"
        assert result.access_token == "test_access_token"
    
    @responses.activate
    def test_get_user_init_failure(self, test_domain, test_credentials):
        """Test get_user flow when app initialization fails."""
        responses.add(
            responses.POST,
            f"https://{test_domain}/ws/app_clickedu_init.php",
            json={"error": "Init failed"},
            status=400
        )
        
        with pytest.raises(APIError, match="Failed to initialize app"):
            get_user(test_domain, test_credentials["username"], test_credentials["password"])
    
    @responses.activate
    def test_get_user_authorization_failure(self, test_domain, test_credentials):
        """Test get_user flow when authorization fails."""
        responses.add(
            responses.POST,
            f"https://{test_domain}/ws/app_clickedu_init.php",
            json={"token": "test_token", "secret": "test_secret"},
            status=200,
            headers={"set-cookie": "PHPSESSID=test_session_id; path=/"}
        )
        
        responses.add(
            responses.GET,
            f"https://{test_domain}/authorization.php",
            json={"error": "Invalid credentials"},
            status=401
        )
        
        with pytest.raises(AuthenticationError, match="Failed to authorize user"):
            get_user(test_domain, test_credentials["username"], test_credentials["password"])
    
    @responses.activate
    def test_get_user_permissions_failure(self, test_domain, test_credentials):
        """Test get_user flow when permissions setting fails."""
        responses.add(
            responses.POST,
            f"https://{test_domain}/ws/app_clickedu_init.php",
            json={"token": "test_token", "secret": "test_secret"},
            status=200,
            headers={"set-cookie": "PHPSESSID=test_session_id; path=/"}
        )
        
        responses.add(
            responses.GET,
            f"https://{test_domain}/authorization.php",
            json={"id_usuari": "test_user_id"},
            status=200
        )
        
        responses.add(
            responses.POST,
            f"https://{test_domain}/ws/app_clickedu_permissions.php",
            json={"error": "Permission denied"},
            status=403
        )
        
        with pytest.raises(APIError, match="Failed to set permissions"):
            get_user(test_domain, test_credentials["username"], test_credentials["password"])
    
    @responses.activate
    def test_get_user_token_failure(self, test_domain, test_credentials):
        """Test get_user flow when token retrieval fails."""
        responses.add(
            responses.POST,
            f"https://{test_domain}/ws/app_clickedu_init.php",
            json={"token": "test_token", "secret": "test_secret"},
            status=200,
            headers={"set-cookie": "PHPSESSID=test_session_id; path=/"}
        )
        
        responses.add(
            responses.GET,
            f"https://{test_domain}/authorization.php",
            json={"id_usuari": "test_user_id"},
            status=200
        )
        
        responses.add(
            responses.POST,
            f"https://{test_domain}/ws/app_clickedu_permissions.php",
            json={"user_id": "test_user_id", "type": 1},
            status=200
        )
        
        responses.add(
            responses.POST,
            "https://api.clickedu.eu/login/v1/auth/token",
            json={"error": "Invalid credentials"},
            status=401
        )
        
        with pytest.raises(AuthenticationError, match="Failed to get access token"):
            get_user(test_domain, test_credentials["username"], test_credentials["password"])
    
    @responses.activate
    def test_get_user_validation_failure(self, test_domain, test_credentials):
        """Test get_user flow when token validation fails."""
        responses.add(
            responses.POST,
            f"https://{test_domain}/ws/app_clickedu_init.php",
            json={"token": "test_token", "secret": "test_secret"},
            status=200,
            headers={"set-cookie": "PHPSESSID=test_session_id; path=/"}
        )
        
        responses.add(
            responses.GET,
            f"https://{test_domain}/authorization.php",
            json={"id_usuari": "test_user_id"},
            status=200
        )
        
        responses.add(
            responses.POST,
            f"https://{test_domain}/ws/app_clickedu_permissions.php",
            json={"user_id": "test_user_id", "type": 1},
            status=200
        )
        
        responses.add(
            responses.POST,
            "https://api.clickedu.eu/login/v1/auth/token",
            json={"access_token": "test_access_token"},
            status=200
        )
        
        responses.add(
            responses.GET,
            "https://api.clickedu.eu/login/v1/auth/token/validate",
            json={"error": "Invalid token"},
            status=401
        )
        
        with pytest.raises(AuthenticationError, match="Failed to validate token"):
            get_user(test_domain, test_credentials["username"], test_credentials["password"])
    
    @responses.activate
    def test_get_user_check_token_failure_continues(self, test_domain, test_credentials):
        """Test get_user flow when token check fails but continues."""
        responses.add(
            responses.POST,
            f"https://{test_domain}/ws/app_clickedu_init.php",
            json={"token": "test_token", "secret": "test_secret"},
            status=200,
            headers={"set-cookie": "PHPSESSID=test_session_id; path=/"}
        )
        
        responses.add(
            responses.GET,
            f"https://{test_domain}/authorization.php",
            json={"id_usuari": "test_user_id"},
            status=200
        )
        
        responses.add(
            responses.POST,
            f"https://{test_domain}/ws/app_clickedu_permissions.php",
            json={"user_id": "test_user_id", "type": 1},
            status=200
        )
        
        responses.add(
            responses.POST,
            "https://api.clickedu.eu/login/v1/auth/token",
            json={"access_token": "test_access_token"},
            status=200
        )
        
        responses.add(
            responses.GET,
            "https://api.clickedu.eu/login/v1/auth/token/validate",
            json={"id": "test_id", "user_id": 12345},
            status=200
        )
        
        responses.add(
            responses.GET,
            f"https://{test_domain}/ws/app_clickedu_check_token.php",
            json={"error": "Token check failed"},
            status=500
        )
        
        result = get_user(test_domain, test_credentials["username"], test_credentials["password"])
        
        # Should still succeed even if token check fails
        assert result is not None
        assert isinstance(result, User)
        assert result.id == "test_id"
    
    def test_get_user_exception_handling(self, test_domain, test_credentials):
        """Test get_user flow with exception handling."""
        with patch('clickedu.auth.flow.AuthApi') as mock_auth_api:
            mock_instance = Mock()
            mock_instance.app_clickedu_init.side_effect = Exception("Test exception")
            mock_auth_api.return_value = mock_instance
            
            with pytest.raises(AuthenticationError, match="Unexpected error in authentication flow"):
                get_user(test_domain, test_credentials["username"], test_credentials["password"])
