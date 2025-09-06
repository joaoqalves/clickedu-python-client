"""
Tests for QueryApi class.
"""

import pytest
import responses
from unittest.mock import patch, Mock
from clickedu import QueryApi, InitQueryResponse, NewsResponse, PhotoAlbumsResponse, GetAlbumByIdResponse
from clickedu.exceptions import APIError


class TestQueryApi:
    """Test QueryApi class."""
    
    def test_query_api_initialization(self, mock_user, test_config):
        """Test QueryApi initialization."""
        query_api = QueryApi(mock_user, test_config)
        
        assert query_api.user == mock_user
        assert query_api.cons_key == test_config.cons_key
        assert query_api.cons_secret == test_config.cons_secret
        assert query_api.session is not None
    
    def test_get_url_and_default_params(self, mock_user, test_config):
        """Test URL and default parameters generation."""
        query_api = QueryApi(mock_user, test_config)
        url, params = query_api._get_url_and_default_params()
        
        expected_url = f"https://{mock_user.base_url}/ws/app_clickedu_query.php"
        assert url == expected_url
        
        expected_params = {
            "auth_token": mock_user.auth_token,
            "auth_secret": mock_user.secret_token,
            "cons_key": query_api.cons_key,
            "cons_secret": query_api.cons_secret,
            "id_fill": mock_user.child_id,
        }
        assert params == expected_params
    
    @responses.activate
    def test_default_query_success(self, mock_user, test_config):
        """Test successful default query execution."""
        responses.add(
            responses.GET,
            f"https://{mock_user.base_url}/ws/app_clickedu_query.php",
            json={"status": "success", "data": "test_data"},
            status=200
        )
        
        query_api = QueryApi(mock_user, test_config)
        result = query_api._default_query("/test", {"param": "value"})
        
        assert result is not None
        assert result["status"] == "success"
        assert result["data"] == "test_data"
    
    @responses.activate
    def test_default_query_failure(self, mock_user, test_config):
        """Test default query execution failure."""
        responses.add(
            responses.GET,
            f"https://{mock_user.base_url}/ws/app_clickedu_query.php",
            json={"error": "Query failed"},
            status=500
        )
        
        query_api = QueryApi(mock_user, test_config)
        with pytest.raises(APIError, match="Failed to execute query"):
            query_api._default_query("/test")
    
    @responses.activate
    def test_init_query_success(self, mock_user, test_config):
        """Test successful init query."""
        responses.add(
            responses.GET,
            f"https://{mock_user.base_url}/ws/app_clickedu_query.php",
            json={"status": "success"},
            status=200
        )
        
        query_api = QueryApi(mock_user, test_config)
        result = query_api.init()
        
        assert result is not None
        assert isinstance(result, InitQueryResponse)
    
    @responses.activate
    def test_init_query_failure(self, mock_user, test_config):
        """Test init query failure."""
        responses.add(
            responses.GET,
            f"https://{mock_user.base_url}/ws/app_clickedu_query.php",
            json={"error": "Init failed"},
            status=500
        )
        
        query_api = QueryApi(mock_user, test_config)
        with pytest.raises(APIError, match="Failed to execute query"):
            query_api.init()
    
    @responses.activate
    def test_get_news_success(self, mock_user, mock_news_response, test_config):
        """Test successful news retrieval."""
        responses.add(
            responses.GET,
            f"https://{mock_user.base_url}/ws/app_clickedu_query.php",
            json={
                "total": 2,
                "news": [
                    {
                        "title": "Test News 1",
                        "subtitle": "Test Subtitle 1",
                        "body": "Test body 1",
                        "imagePath": "test_image_1.jpg",
                        "imageText": "Test image text 1",
                        "filePath": "../private/test_file_1.pdf"
                    },
                    {
                        "title": "Test News 2",
                        "subtitle": "Test Subtitle 2",
                        "body": "Test body 2",
                        "imagePath": "test_image_2.jpg",
                        "imageText": "Test image text 2",
                        "filePath": "../private/test_file_2.pdf"
                    }
                ]
            },
            status=200
        )
        
        query_api = QueryApi(mock_user, test_config)
        result = query_api.get_news(start_limit=0, end_limit=10)
        
        assert result is not None
        assert isinstance(result, NewsResponse)
        assert result.total == 2
        assert len(result.news) == 2
        assert result.news[0].title == "Test News 1"
        assert result.news[1].title == "Test News 2"
    
    @responses.activate
    def test_get_news_failure(self, mock_user, test_config):
        """Test news retrieval failure."""
        responses.add(
            responses.GET,
            f"https://{mock_user.base_url}/ws/app_clickedu_query.php",
            json={"error": "News retrieval failed"},
            status=500
        )
        
        query_api = QueryApi(mock_user, test_config)
        with pytest.raises(APIError, match="Failed to execute query"):
            query_api.get_news()
    
    @responses.activate
    def test_get_photo_albums_success(self, mock_user, test_config):
        """Test successful photo albums retrieval."""
        responses.add(
            responses.GET,
            f"https://{mock_user.base_url}/ws/app_clickedu_query.php",
            json={
                "albums": [
                    {
                        "id": "album_1",
                        "name": "Test Album 1",
                        "coverImageLarge": "../private/test_large_1.jpg",
                        "coverImageSmall": "../private/test_small_1.jpg"
                    },
                    {
                        "id": "album_2",
                        "name": "Test Album 2",
                        "coverImageLarge": "../private/test_large_2.jpg",
                        "coverImageSmall": "../private/test_small_2.jpg"
                    }
                ]
            },
            status=200
        )
        
        query_api = QueryApi(mock_user, test_config)
        result = query_api.get_photo_albums(start_limit=0, end_limit=10)
        
        assert result is not None
        assert isinstance(result, PhotoAlbumsResponse)
        assert len(result.albums) == 2
        assert result.albums[0].id == "album_1"
        assert result.albums[1].id == "album_2"
    
    @responses.activate
    def test_get_album_by_id_success(self, mock_user, test_config):
        """Test successful album photos retrieval."""
        responses.add(
            responses.GET,
            f"https://{mock_user.base_url}/ws/app_clickedu_query.php",
            json={
                "photos": [
                    {
                        "id": "photo_1",
                        "pathLarge": "../private/test_large_1.jpg",
                        "pathSmall": "../private/test_small_1.jpg"
                    },
                    {
                        "id": "photo_2",
                        "pathLarge": "../private/test_large_2.jpg",
                        "pathSmall": "../private/test_small_2.jpg"
                    }
                ]
            },
            status=200
        )
        
        query_api = QueryApi(mock_user, test_config)
        result = query_api.get_album_by_id("album_1")
        
        assert result is not None
        assert isinstance(result, GetAlbumByIdResponse)
        assert len(result.photos) == 2
        assert result.photos[0].id == "photo_1"
        assert result.photos[1].id == "photo_2"
    
    def test_fix_images_urls(self, mock_user, test_config):
        """Test image URL fixing."""
        from clickedu import PhotoAlbum
        
        query_api = QueryApi(mock_user, test_config)
        
        albums = [
            PhotoAlbum(
                id="album_1",
                name="Test Album",
                coverImageLarge="../private/test_large.jpg",
                coverImageSmall="../private/test_small.jpg"
            )
        ]
        
        fixed_albums = query_api._fix_images_urls(albums, ["coverImageLarge", "coverImageSmall"])
        
        assert len(fixed_albums) == 1
        assert fixed_albums[0].coverImageLarge.startswith("https://")
        assert fixed_albums[0].coverImageSmall.startswith("https://")
        assert "test_large.jpg" in fixed_albums[0].coverImageLarge
        assert "test_small.jpg" in fixed_albums[0].coverImageSmall
    
    def test_get_photo_base_url(self, mock_user, test_config):
        """Test photo base URL generation."""
        query_api = QueryApi(mock_user, test_config)
        base_url = query_api._get_photo_base_url()
        
        expected_url = f"https://{mock_user.base_url}/private/app-{query_api.cons_key}-{query_api.cons_secret}-{mock_user.auth_token}-{mock_user.secret_token}/"
        assert base_url == expected_url
    
    @responses.activate
    def test_download_file_success(self, mock_user, tmp_path, test_config):
        """Test successful file download."""
        # Create a temporary file content
        file_content = b"Test file content"
        
        responses.add(
            responses.GET,
            f"https://{mock_user.base_url}/private/test_file.pdf",
            body=file_content,
            status=200
        )
        
        query_api = QueryApi(mock_user, test_config)
        download_dir = str(tmp_path / "files")
        result = query_api.download_file("../private/test_file.pdf", download_dir)
        
        assert result is not None
        assert result.endswith("test_file.pdf")
        
        # Check file was downloaded
        with open(result, "rb") as f:
            assert f.read() == file_content
    
    @responses.activate
    def test_download_file_failure(self, mock_user, test_config):
        """Test file download failure."""
        responses.add(
            responses.GET,
            f"https://{mock_user.base_url}/private/test_file.pdf",
            json={"error": "File not found"},
            status=404
        )
        
        query_api = QueryApi(mock_user, test_config)
        result = query_api.download_file("../private/test_file.pdf")
        
        assert result is None
    
    def test_download_file_invalid_path(self, mock_user, test_config):
        """Test file download with invalid path."""
        query_api = QueryApi(mock_user, test_config)
        result = query_api.download_file("invalid_path")
        
        assert result is None
