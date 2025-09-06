# ClickEdu Python Client

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, clean Python client for interacting with the ClickEdu API. ClickEdu is a comprehensive school management platform that provides APIs for accessing student information, news, photo albums, and other educational data.

## ⚠️ DISCLAIMER

**This is NOT an official ClickEdu client.** This is an unofficial, third-party library created for educational and development purposes. The authors are not affiliated with ClickEdu and assume no liability for any issues, data loss, or problems that may arise from using this software. Use at your own risk.

**AI-Generated Code:** Most of this codebase was generated using AI assistance through Cursor IDE. While the code has been tested and reviewed, please be aware that AI-generated code may contain errors or unexpected behavior. Always review and test thoroughly before using in production environments.

## Features

- 🏗️ **Clean architecture**: Modular, maintainable codebase
- ⚡ **Modern Python**: Type hints, dataclasses, proper error handling
- 🔧 **Configurable**: Environment-based configuration

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd clickedu

# Install dependencies
uv install
# or
pip install -e .
```

### Basic Usage

```python
from clickedu import ClickEduClient

# Initialize client
client = ClickEduClient('your-school.clickedu.eu', log_level='INFO')

# Authenticate
user = client.authenticate('username', 'password')

# Get news
news = client.get_news()
print(f'Found {news.total} news items')

# Get photo albums
albums = client.get_photo_albums()
print(f'Found {albums.total} photo albums')
```

## Configuration

The client can be configured using environment variables or by passing parameters directly.

### Environment Variables

Create a `.env` file in your project root (see `.env.example` for reference):

```bash
# ClickEdu Configuration
CLICKEDU_DOMAIN=your-school.clickedu.eu
LOG_LEVEL=WARNING
DEFAULT_LANGUAGE=ca

# API Credentials
CLICKEDU_CONS_KEY=your_cons_key
CLICKEDU_CONS_SECRET=your_cons_secret
CLICKEDU_API_KEY=your_api_key
CLICKEDU_CLIENT_SECRET=your_client_secret
```

### Direct Configuration

```python
from clickedu import ClickEduClient

# Using environment variables
client = ClickEduClient()  # Reads from .env

# Or pass parameters directly
client = ClickEduClient(
    domain='your-school.clickedu.eu',
    log_level='INFO'
)
```
