#!/usr/bin/env python3
"""
ClickEdu Clean API Demo
Demonstrates the new clean ClickEdu API client usage.
"""

import sys
import getpass
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from clickedu import ClickEduClient, ClickEduError, AuthenticationError


def main():
    """Main demo function."""
    print("ClickEdu Clean API Demo")
    print("=" * 30)
    
    username = input("Enter username: ").strip()
    if not username:
        print("Username required. Exiting.")
        return
    
    password = getpass.getpass("Enter password: ")
    if not password:
        print("Password required. Exiting.")
        return
    
    try:
        # Create client and authenticate
        client = ClickEduClient(log_level="INFO")
        user = client.authenticate(username, password)
        
        print(f"\n✅ Authentication successful!")
        print(f"User ID: {user.user_id}")
        print(f"Child ID: {user.child_id}")
        print(f"Base URL: {user.base_url}")
        
        # Test initialization
        print("\n🔍 Testing initialization...")
        init_result = client.init()
        if init_result:
            print("✅ Initialization successful!")
        else:
            print("❌ Initialization failed!")
        
        # Test news retrieval
        print("\n📰 Testing news retrieval...")
        news_result = client.get_news(start_limit=0, end_limit=5)
        if news_result:
            print(f"✅ News retrieval successful! Found {news_result.total} total news items")
            for i, news_item in enumerate(news_result.news[:3], 1):
                print(f"  {i}. {news_item.title}")
                if news_item.subtitle:
                    print(f"     Subtitle: {news_item.subtitle}")
                if news_item.filePath:
                    print(f"     File: {news_item.filePath}")
                    # Download the file
                    downloaded_path = client.download_file(news_item.filePath)
                    if downloaded_path:
                        print(f"     📁 Downloaded to: {downloaded_path}")
        else:
            print("❌ News retrieval failed!")
        
        # Test photo albums
        print("\n📸 Testing photo albums...")
        albums_result = client.get_photo_albums(start_limit=0, end_limit=5)
        if albums_result:
            print(f"✅ Photo albums retrieval successful! Found {len(albums_result.albums)} albums")
            for i, album in enumerate(albums_result.albums[:3], 1):
                print(f"  {i}. {album.name} (ID: {album.id})")
                if album.coverImageLarge:
                    print(f"     Cover: {album.coverImageLarge}")
        else:
            print("❌ Photo albums retrieval failed!")
        
        # Test album photos (if we have albums)
        if albums_result and albums_result.albums:
            album_id = albums_result.albums[0].id
            print(f"\n🖼️  Testing photos from album '{album_id}'...")
            photos_result = client.get_album_photos(album_id)
            if photos_result:
                print(f"✅ Photos retrieval successful! Found {len(photos_result.photos)} photos")
                for i, photo in enumerate(photos_result.photos[:3], 1):
                    print(f"  {i}. Photo ID: {photo.id}")
                    if photo.pathLarge:
                        print(f"     Large: {photo.pathLarge}")
            else:
                print("❌ Photos retrieval failed!")
        
    except AuthenticationError as e:
        print(f"\n❌ Authentication failed: {e}")
    except ClickEduError as e:
        print(f"\n❌ ClickEdu error: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
