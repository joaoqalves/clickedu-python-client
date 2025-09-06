"""
Tests for ClickEdu response models.
"""

import pytest
from clickedu import (
    User,
    AppInitResponse,
    AuthorizationResponse,
    AppPermissionsResponse,
    TokenResponse,
    ValidateResponse,
    InitQueryResponse,
    NewsItem,
    NewsResponse,
    PhotoAlbum,
    PhotoAlbumsResponse,
    Photo,
    GetAlbumByIdResponse,
)


class TestUser:
    """Test User dataclass."""
    
    def test_user_creation(self):
        """Test User object creation."""
        user = User(
            id="test_id",
            user_id=12345,
            child_id="child_123",
            base_url="test.clickedu.eu",
            auth_token="test_auth_token",
            secret_token="test_secret_token",
            access_token="test_access_token"
        )
        
        assert user.id == "test_id"
        assert user.user_id == 12345
        assert user.child_id == "child_123"
        assert user.base_url == "test.clickedu.eu"
        assert user.auth_token == "test_auth_token"
        assert user.secret_token == "test_secret_token"
        assert user.access_token == "test_access_token"
    
    def test_user_required_fields(self):
        """Test that User requires all fields."""
        with pytest.raises(TypeError):
            User(
                id="test_id",
                user_id=12345,
                # Missing required fields
            )


class TestAppInitResponse:
    """Test AppInitResponse dataclass."""
    
    def test_app_init_response_creation(self):
        """Test AppInitResponse object creation."""
        response = AppInitResponse(
            token="test_token",
            secret="test_secret"
        )
        
        assert response.token == "test_token"
        assert response.secret == "test_secret"


class TestAuthorizationResponse:
    """Test AuthorizationResponse dataclass."""
    
    def test_authorization_response_creation(self):
        """Test AuthorizationResponse object creation."""
        response = AuthorizationResponse(
            id_usuari="test_user_id"
        )
        
        assert response.id_usuari == "test_user_id"


class TestAppPermissionsResponse:
    """Test AppPermissionsResponse dataclass."""
    
    def test_app_permissions_response_creation(self):
        """Test AppPermissionsResponse object creation with all fields."""
        response = AppPermissionsResponse(
            error="test_error",
            msg="test_message",
            user_id="test_user_id",
            type=1
        )
        
        assert response.error == "test_error"
        assert response.msg == "test_message"
        assert response.user_id == "test_user_id"
        assert response.type == 1
    
    def test_app_permissions_response_defaults(self):
        """Test AppPermissionsResponse with default values."""
        response = AppPermissionsResponse()
        
        assert response.error is None
        assert response.msg is None
        assert response.user_id is None
        assert response.type is None


class TestTokenResponse:
    """Test TokenResponse dataclass."""
    
    def test_token_response_creation(self):
        """Test TokenResponse object creation."""
        response = TokenResponse(
            access_token="test_access_token"
        )
        
        assert response.access_token == "test_access_token"


class TestValidateResponse:
    """Test ValidateResponse dataclass."""
    
    def test_validate_response_creation(self):
        """Test ValidateResponse object creation."""
        response = ValidateResponse(
            id="test_id",
            user_id=12345
        )
        
        assert response.id == "test_id"
        assert response.user_id == 12345


class TestInitQueryResponse:
    """Test InitQueryResponse dataclass."""
    
    def test_init_query_response_creation(self):
        """Test InitQueryResponse object creation."""
        response = InitQueryResponse()
        # InitQueryResponse is empty, just test it can be created
        assert response is not None


class TestNewsItem:
    """Test NewsItem dataclass."""
    
    def test_news_item_creation(self):
        """Test NewsItem object creation with all fields."""
        news_item = NewsItem(
            title="Test Title",
            subtitle="Test Subtitle",
            body="Test body content",
            imagePath="test_image.jpg",
            imageText="Test image text",
            filePath="../private/test_file.pdf"
        )
        
        assert news_item.title == "Test Title"
        assert news_item.subtitle == "Test Subtitle"
        assert news_item.body == "Test body content"
        assert news_item.imagePath == "test_image.jpg"
        assert news_item.imageText == "Test image text"
        assert news_item.filePath == "../private/test_file.pdf"
    
    def test_news_item_defaults(self):
        """Test NewsItem with default values."""
        news_item = NewsItem(title="Test Title")
        
        assert news_item.title == "Test Title"
        assert news_item.subtitle is None
        assert news_item.body is None
        assert news_item.imagePath is None
        assert news_item.imageText is None
        assert news_item.filePath is None


class TestNewsResponse:
    """Test NewsResponse dataclass."""
    
    def test_news_response_creation(self):
        """Test NewsResponse object creation."""
        news_items = [
            NewsItem(title="News 1"),
            NewsItem(title="News 2")
        ]
        response = NewsResponse(
            total=2,
            news=news_items
        )
        
        assert response.total == 2
        assert len(response.news) == 2
        assert response.news[0].title == "News 1"
        assert response.news[1].title == "News 2"


class TestPhotoAlbum:
    """Test PhotoAlbum dataclass."""
    
    def test_photo_album_creation(self):
        """Test PhotoAlbum object creation with all fields."""
        album = PhotoAlbum(
            id="album_1",
            name="Test Album",
            coverImageLarge="test_large.jpg",
            coverImageSmall="test_small.jpg"
        )
        
        assert album.id == "album_1"
        assert album.name == "Test Album"
        assert album.coverImageLarge == "test_large.jpg"
        assert album.coverImageSmall == "test_small.jpg"
    
    def test_photo_album_defaults(self):
        """Test PhotoAlbum with default values."""
        album = PhotoAlbum(
            id="album_1",
            name="Test Album"
        )
        
        assert album.id == "album_1"
        assert album.name == "Test Album"
        assert album.coverImageLarge is None
        assert album.coverImageSmall is None


class TestPhotoAlbumsResponse:
    """Test PhotoAlbumsResponse dataclass."""
    
    def test_photo_albums_response_creation(self):
        """Test PhotoAlbumsResponse object creation."""
        albums = [
            PhotoAlbum(id="album_1", name="Album 1"),
            PhotoAlbum(id="album_2", name="Album 2")
        ]
        response = PhotoAlbumsResponse(albums=albums)
        
        assert len(response.albums) == 2
        assert response.albums[0].id == "album_1"
        assert response.albums[1].id == "album_2"


class TestPhoto:
    """Test Photo dataclass."""
    
    def test_photo_creation(self):
        """Test Photo object creation with all fields."""
        photo = Photo(
            id="photo_1",
            pathLarge="test_large.jpg",
            pathSmall="test_small.jpg"
        )
        
        assert photo.id == "photo_1"
        assert photo.pathLarge == "test_large.jpg"
        assert photo.pathSmall == "test_small.jpg"
    
    def test_photo_defaults(self):
        """Test Photo with default values."""
        photo = Photo(id="photo_1")
        
        assert photo.id == "photo_1"
        assert photo.pathLarge is None
        assert photo.pathSmall is None


class TestGetAlbumByIdResponse:
    """Test GetAlbumByIdResponse dataclass."""
    
    def test_get_album_by_id_response_creation(self):
        """Test GetAlbumByIdResponse object creation."""
        photos = [
            Photo(id="photo_1"),
            Photo(id="photo_2")
        ]
        response = GetAlbumByIdResponse(photos=photos)
        
        assert len(response.photos) == 2
        assert response.photos[0].id == "photo_1"
        assert response.photos[1].id == "photo_2"
