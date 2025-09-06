"""
Test configuration and fixtures for ClickEdu tests.
"""

import pytest
import os
from unittest.mock import Mock, patch
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@pytest.fixture
def mock_user():
    """Create a mock User object for testing."""
    from clickedu import User
    return User(
        id="test_id",
        user_id=12345,
        child_id="child_123",
        base_url="test.clickedu.eu",
        auth_token="test_auth_token",
        secret_token="test_secret_token",
        access_token="test_access_token"
    )

@pytest.fixture
def mock_app_init_response():
    """Create a mock AppInitResponse for testing."""
    from clickedu import AppInitResponse
    return AppInitResponse(
        token="test_token",
        secret="test_secret"
    )

@pytest.fixture
def mock_authorization_response():
    """Create a mock AuthorizationResponse for testing."""
    from clickedu import AuthorizationResponse
    return AuthorizationResponse(
        id_usuari="test_user_id"
    )

@pytest.fixture
def mock_token_response():
    """Create a mock TokenResponse for testing."""
    from clickedu import TokenResponse
    return TokenResponse(
        access_token="test_access_token"
    )

@pytest.fixture
def mock_validate_response():
    """Create a mock ValidateResponse for testing."""
    from clickedu import ValidateResponse
    return ValidateResponse(
        id="test_id",
        user_id=12345
    )

@pytest.fixture
def mock_news_response():
    """Create a mock NewsResponse for testing."""
    from clickedu import NewsResponse, NewsItem
    return NewsResponse(
        total=2,
        news=[
            NewsItem(
                title="Test News 1",
                subtitle="Test Subtitle 1",
                body="Test body 1",
                imagePath="test_image_1.jpg",
                imageText="Test image text 1",
                filePath="../private/test_file_1.pdf"
            ),
            NewsItem(
                title="Test News 2",
                subtitle="Test Subtitle 2",
                body="Test body 2",
                imagePath="test_image_2.jpg",
                imageText="Test image text 2",
                filePath="../private/test_file_2.pdf"
            )
        ]
    )

@pytest.fixture
def mock_photo_albums_response():
    """Create a mock PhotoAlbumsResponse for testing."""
    from clickedu import PhotoAlbumsResponse, PhotoAlbum
    return PhotoAlbumsResponse(
        albums=[
            PhotoAlbum(
                id="album_1",
                name="Test Album 1",
                coverImageLarge="test_cover_large_1.jpg",
                coverImageSmall="test_cover_small_1.jpg"
            ),
            PhotoAlbum(
                id="album_2",
                name="Test Album 2",
                coverImageLarge="test_cover_large_2.jpg",
                coverImageSmall="test_cover_small_2.jpg"
            )
        ]
    )

@pytest.fixture
def mock_photos_response():
    """Create a mock GetAlbumByIdResponse for testing."""
    from clickedu import GetAlbumByIdResponse, Photo
    return GetAlbumByIdResponse(
        photos=[
            Photo(
                id="photo_1",
                pathLarge="test_photo_large_1.jpg",
                pathSmall="test_photo_small_1.jpg"
            ),
            Photo(
                id="photo_2",
                pathLarge="test_photo_large_2.jpg",
                pathSmall="test_photo_small_2.jpg"
            )
        ]
    )

@pytest.fixture
def mock_requests_session():
    """Create a mock requests session."""
    with patch('requests.Session') as mock_session:
        yield mock_session.return_value

@pytest.fixture
def test_domain():
    """Test domain for ClickEdu."""
    return "test.clickedu.eu"

@pytest.fixture
def test_config():
    """Test configuration object."""
    from clickedu.config import Config
    return Config(domain="test.clickedu.eu", log_level="WARNING")

@pytest.fixture
def test_credentials():
    """Test credentials."""
    return {
        "username": "test_user",
        "password": "test_password"
    }

@pytest.fixture(autouse=True)
def setup_test_env():
    """Set up test environment variables."""
    os.environ.update({
        "CLICKEDU_DOMAIN": "test.clickedu.eu",
        "CLICKEDU_CONS_KEY": "test_cons_key",
        "CLICKEDU_CONS_SECRET": "test_cons_secret",
        "CLICKEDU_API_KEY": "test_api_key",
        "LOG_LEVEL": "WARNING",
        "DEFAULT_LANGUAGE": "ca"
    })
