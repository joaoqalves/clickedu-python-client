"""
Integration tests for the complete ClickEdu flow.
"""

import pytest
import responses
from clickedu import get_user, QueryApi


class TestFullFlow:
    """Test the complete ClickEdu authentication and query flow."""
    
    @responses.activate
    def test_complete_flow_success(self, test_domain, test_credentials, test_config):
        """Test complete flow from authentication to querying."""
        # Mock authentication flow
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
        
        # Mock query responses
        responses.add(
            responses.GET,
            f"https://{test_domain}/ws/app_clickedu_query.php",
            json={"status": "success"},
            status=200
        )
        
        responses.add(
            responses.GET,
            f"https://{test_domain}/ws/app_clickedu_query.php",
            json={
                "total": 1,
                "news": [
                    {
                        "title": "Test News",
                        "subtitle": "Test Subtitle",
                        "body": "Test body",
                        "imagePath": "test_image.jpg",
                        "imageText": "Test image text",
                        "filePath": "../private/test_file.pdf"
                    }
                ]
            },
            status=200
        )
        
        # Execute the flow
        user = get_user(test_domain, test_credentials["username"], test_credentials["password"])
        
        assert user is not None
        
        # Test querying
        query_api = QueryApi(user, test_config)
        
        # Test init query
        init_result = query_api.init()
        assert init_result is not None
        
        # Test news query
        news_result = query_api.get_news()
        assert news_result is not None
        assert news_result.total == 1
        assert len(news_result.news) == 1
        assert news_result.news[0].title == "Test News"
    
    @responses.activate
    def test_photo_albums_flow(self, test_domain, test_credentials, test_config):
        """Test photo albums query flow."""
        # Create a mock user for this test (skip authentication)
        from clickedu import User
        user = User(
            id="test_id",
            user_id=12345,
            child_id="test_user_id",
            base_url=test_domain,
            auth_token="test_token",
            secret_token="test_secret",
            access_token="test_access_token"
        )
        
        # Mock photo albums response
        responses.add(
            responses.GET,
            f"https://{test_domain}/ws/app_clickedu_query.php",
            json={
                "albums": [
                    {
                        "id": "album_1",
                        "name": "Test Album 1",
                        "coverImageLarge": "../private/test_large_1.jpg",
                        "coverImageSmall": "../private/test_small_1.jpg"
                    }
                ]
            },
            status=200
        )
        
        # Mock photos response
        responses.add(
            responses.GET,
            f"https://{test_domain}/ws/app_clickedu_query.php",
            json={
                "photos": [
                    {
                        "id": "photo_1",
                        "pathLarge": "../private/test_large_1.jpg",
                        "pathSmall": "../private/test_small_1.jpg"
                    }
                ]
            },
            status=200
        )
        
        query_api = QueryApi(user, test_config)
        
        # Test photo albums query
        albums_result = query_api.get_photo_albums()
        assert albums_result is not None
        assert len(albums_result.albums) == 1
        assert albums_result.albums[0].id == "album_1"
        
        # Test getting photos from album
        photos_result = query_api.get_album_by_id("album_1")
        assert photos_result is not None
        assert len(photos_result.photos) == 1
        assert photos_result.photos[0].id == "photo_1"
    
    @responses.activate
    def test_file_download_flow(self, test_domain, test_credentials, tmp_path, test_config):
        """Test file download flow."""
        # Create a mock user
        from clickedu import User
        user = User(
            id="test_id",
            user_id=12345,
            child_id="test_user_id",
            base_url=test_domain,
            auth_token="test_token",
            secret_token="test_secret",
            access_token="test_access_token"
        )
        
        # Mock file download
        file_content = b"Test PDF content"
        responses.add(
            responses.GET,
            f"https://{test_domain}/private/test_file.pdf",
            body=file_content,
            status=200
        )
        
        query_api = QueryApi(user, test_config)
        download_dir = str(tmp_path / "files")
        result = query_api.download_file("../private/test_file.pdf", download_dir)
        
        assert result is not None
        assert result.endswith("test_file.pdf")
        
        # Verify file content
        with open(result, "rb") as f:
            assert f.read() == file_content
