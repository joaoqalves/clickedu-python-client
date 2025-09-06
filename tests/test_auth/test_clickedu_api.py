"""
Tests for ClickeduApi class.
"""

import pytest
import responses
from clickedu import ClickeduApi, TokenResponse, ValidateResponse
from clickedu.exceptions import AuthenticationError


class TestClickeduApi:
    """Test ClickeduApi class."""
    
    def test_clickedu_api_initialization(self, test_domain):
        """Test ClickeduApi initialization."""
        api = ClickeduApi(test_domain)
        
        assert api.config.domain == test_domain
        assert api.session is not None
        assert "User-Agent" in api.session.headers
    
    @responses.activate
    def test_token_success(self, test_domain, test_credentials):
        """Test successful token retrieval."""
        responses.add(
            responses.POST,
            "https://api.clickedu.eu/login/v1/auth/token",
            json={"access_token": "test_access_token"},
            status=200
        )
        
        api = ClickeduApi(test_domain)
        result = api.token(test_credentials["username"], test_credentials["password"])
        
        assert result is not None
        assert isinstance(result, TokenResponse)
        assert result.access_token == "test_access_token"
    
    @responses.activate
    def test_token_failure(self, test_domain, test_credentials):
        """Test token retrieval failure."""
        responses.add(
            responses.POST,
            "https://api.clickedu.eu/login/v1/auth/token",
            json={"error": "Invalid credentials"},
            status=401
        )
        
        api = ClickeduApi(test_domain)
        with pytest.raises(AuthenticationError, match="Failed to get access token"):
            api.token(test_credentials["username"], test_credentials["password"])
    
    @responses.activate
    def test_validate_success(self, test_domain):
        """Test successful token validation."""
        responses.add(
            responses.GET,
            "https://api.clickedu.eu/login/v1/auth/token/validate",
            json={"id": "test_id", "user_id": 12345},
            status=200
        )
        
        api = ClickeduApi(test_domain)
        result = api.validate("test_access_token", "test_child_id")
        
        assert result is not None
        assert isinstance(result, ValidateResponse)
        assert result.id == "test_id"
        assert result.user_id == 12345
    
    @responses.activate
    def test_validate_failure(self, test_domain):
        """Test token validation failure."""
        responses.add(
            responses.GET,
            "https://api.clickedu.eu/login/v1/auth/token/validate",
            json={"error": "Invalid token"},
            status=401
        )
        
        api = ClickeduApi(test_domain)
        with pytest.raises(AuthenticationError, match="Failed to validate token"):
            api.validate("test_access_token", "test_child_id")
    
    def test_token_request_headers(self, test_domain, test_credentials):
        """Test that token request includes correct headers."""
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.POST,
                "https://api.clickedu.eu/login/v1/auth/token",
                json={"access_token": "test_access_token"},
                status=200
            )
            
            api = ClickeduApi(test_domain)
            api.token(test_credentials["username"], test_credentials["password"])
            
            # Check the request was made with correct headers
            request = rsps.calls[0].request
            assert "x-api-key" in request.headers
            assert "domain" in request.headers
            # The domain comes from the config
            assert request.headers["domain"] == test_domain
    
    def test_validate_request_headers(self, test_domain):
        """Test that validate request includes correct headers."""
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                "https://api.clickedu.eu/login/v1/auth/token/validate",
                json={"id": "test_id", "user_id": 12345},
                status=200
            )
            
            api = ClickeduApi(test_domain)
            api.validate("test_access_token", "test_child_id")
            
            # Check the request was made with correct headers
            request = rsps.calls[0].request
            assert "x-api-key" in request.headers
            assert "domain" in request.headers
            assert "Authorization" in request.headers
            assert request.headers["Authorization"] == "Bearer test_access_token"
