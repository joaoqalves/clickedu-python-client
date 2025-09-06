"""
ClickEdu API Client
A Python client for interacting with the ClickEdu API to search for domains.
"""

# Main client interface
from .client import ClickEduClient

# Data models
from .models import (
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

# Authentication
from .auth import AuthApi, ClickeduApi, get_user

# Query API
from .query import QueryApi

# Exceptions
from .exceptions import (
    ClickEduError,
    AuthenticationError,
    AuthorizationError,
    APIError,
    ConfigurationError,
    FileDownloadError,
    ValidationError,
)

__version__ = "0.1.0"
__all__ = [
    # Main client
    "ClickEduClient",
    
    # Data models
    "User",
    "AppInitResponse",
    "AuthorizationResponse", 
    "AppPermissionsResponse",
    "TokenResponse",
    "ValidateResponse",
    "InitQueryResponse",
    "NewsItem",
    "NewsResponse",
    "PhotoAlbum",
    "PhotoAlbumsResponse",
    "Photo",
    "GetAlbumByIdResponse",
    
    # Authentication
    "AuthApi",
    "ClickeduApi",
    "get_user",
    
    # Query API
    "QueryApi",
    
    # Exceptions
    "ClickEduError",
    "AuthenticationError",
    "AuthorizationError",
    "APIError",
    "ConfigurationError",
    "FileDownloadError",
    "ValidationError",
]
