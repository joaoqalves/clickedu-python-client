"""
Data models for ClickEdu API responses.
"""

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class User:
    """User class to represent the final user data from getUser flow."""
    id: str
    user_id: int
    child_id: str
    base_url: str
    auth_token: str
    secret_token: str
    access_token: str


@dataclass
class AppInitResponse:
    """Response from app_clickedu_init.php."""
    token: str
    secret: str


@dataclass
class AuthorizationResponse:
    """Response from authorization.php."""
    id_usuari: str


@dataclass
class AppPermissionsResponse:
    """Response from app_clickedu_permissions.php."""
    error: Optional[str] = None
    msg: Optional[str] = None
    user_id: Optional[str] = None
    type: Optional[int] = None


@dataclass
class TokenResponse:
    """Response from token endpoint."""
    access_token: str


@dataclass
class ValidateResponse:
    """Response from validate endpoint."""
    id: str
    user_id: int


@dataclass
class InitQueryResponse:
    """Response from /init query."""
    # Add fields as needed based on actual response
    pass


@dataclass
class NewsItem:
    """Individual news item."""
    title: str
    subtitle: Optional[str] = None
    body: Optional[str] = None
    imagePath: Optional[str] = None
    imageText: Optional[str] = None
    filePath: Optional[str] = None


@dataclass
class NewsResponse:
    """Response from /news query."""
    total: int
    news: List[NewsItem]


@dataclass
class PhotoAlbum:
    """Photo album data."""
    id: str
    name: str
    coverImageLarge: Optional[str] = None
    coverImageSmall: Optional[str] = None


@dataclass
class PhotoAlbumsResponse:
    """Response from /photo_albums query."""
    albums: List[PhotoAlbum]


@dataclass
class Photo:
    """Photo data."""
    id: str
    pathLarge: Optional[str] = None
    pathSmall: Optional[str] = None


@dataclass
class GetAlbumByIdResponse:
    """Response from /pictures query."""
    photos: List[Photo]
