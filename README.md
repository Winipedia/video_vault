# VideoVault

A secure desktop application for downloading, storing, and watching videos offline. VideoVault provides an encrypted local storage solution with an integrated video player, allowing you to save videos from various online sources and watch them later with a Netflix-inspired dark theme interface.

## Features

### 🔐 Security & Privacy
- **Encrypted Storage**: All downloaded videos are encrypted using AES-GCM encryption before being stored locally
- **Secure Key Management**: Uses system keyring for secure key storage and management
- **Local-Only**: No cloud storage - all videos remain on your device

### 📺 Video Management
- **Universal Downloads**: Download videos from any supported platform using yt-dlp
- **Integrated Browser**: Built-in web browser for easy video discovery and downloading
- **Smart Organization**: Automatic file naming and organization
- **Resume Playback**: Remembers your last position in each video

### 🎬 Media Player
- **Built-in Player**: Integrated video player with full media controls
- **Encrypted Playback**: Seamlessly plays encrypted videos without temporary decryption
- **Position Memory**: Automatically saves and resumes from your last watched position
- **Full-Screen Support**: Immersive viewing experience

### 🎨 User Interface
- **Netflix-Inspired Design**: Dark theme with red accents for comfortable viewing
- **Single-Window Architecture**: Clean, organized interface with hamburger menu navigation
- **Responsive Layout**: Adapts to different window sizes and screen resolutions
- **Context Menus**: Right-click menus for quick actions (play, delete)

## Installation

### Prerequisites
- Python 3.12 or higher
- Poetry (for dependency management)
- FFmpeg (automatically handled by the application)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/video_vault.git
   cd video_vault
   ```

2. **Install dependencies**:
   ```bash
   poetry install
   ```

3. **Run the application**:
   ```bash
   poetry run python -m video_vault.main
   ```

### Building Executable

To create a standalone executable:

```bash
poetry run python -m video_vault.build.build
```

## Usage

### Getting Started

1. **Launch VideoVault**: Run the application and it will open maximized with the Downloads page
2. **Add Downloads**: Click the "+" button to open the integrated browser
3. **Browse & Download**: Navigate to any video site and click the download button
4. **Watch Videos**: Return to the Downloads page and click any video to start playing

### Main Interface

#### Downloads Page
- **Video Library**: Scrollable list of all downloaded videos
- **Quick Actions**: Right-click any video for play/delete options
- **Add Button**: Plus icon in top-right to access the download browser

#### Add Downloads Page
- **Integrated Browser**: Full web browser for navigating video sites
- **Download Button**: Download arrow icon to save the current page's video
- **Cookie Support**: Automatically handles authentication cookies

#### Player Page
- **Video Playback**: Full-featured media player with standard controls
- **Resume Feature**: Automatically resumes from your last position
- **Encrypted Streaming**: Plays encrypted files without exposing decrypted data

### Supported Sites

VideoVault uses yt-dlp under the hood, supporting hundreds of video platforms including:
- YouTube
- Vimeo
- Twitch
- Facebook
- Instagram
- TikTok
- And many more...

## Architecture

### Technology Stack
- **Frontend**: PySide6 (Qt for Python) for cross-platform GUI
- **Backend**: Django ORM for database management
- **Encryption**: Cryptography library with AES-GCM
- **Downloads**: yt-dlp for video extraction
- **Media**: Qt Multimedia for video playback

### Project Structure
```
video_vault/
├── core/           # Core functionality (downloads, security, constants)
├── db/             # Database models and setup
├── ui/             # User interface components
│   ├── pages/      # Application pages (downloads, player, browser)
│   └── windows/    # Main window management
├── externals/      # External tool integration (FFmpeg)
└── main.py         # Application entry point
```

### Security Model
- Videos are encrypted immediately after download using AES-GCM
- Encryption keys are stored securely in the system keyring
- No plaintext video data is stored on disk
- Temporary files are automatically cleaned up

## Development

### Setting up Development Environment

1. **Install development dependencies**:
   ```bash
   poetry install --with dev
   ```

2. **Install pre-commit hooks**:
   ```bash
   poetry run pre-commit install
   ```

3. **Run tests**:
   ```bash
   poetry run pytest
   ```

4. **Code quality checks**:
   ```bash
   poetry run ruff check .
   poetry run mypy .
   poetry run bandit -r video_vault/
   ```

### Testing
- **Framework**: pytest with pytest-qt for GUI testing
- **Coverage**: Comprehensive test suite covering core functionality
- **Mocking**: Uses pytest-mock for isolated unit tests
- **Structure**: Mirror test structure following source code organization

### Code Style
- **Linting**: Ruff for code formatting and style enforcement
- **Type Checking**: MyPy for static type analysis
- **Security**: Bandit for security vulnerability scanning
- **Pre-commit**: Automated checks before each commit

## Configuration

### Database
- **Type**: SQLite database stored in user data directory
- **Location**: `%APPDATA%/VideoVault/db/db.sqlite3` (Windows)
- **Models**: File model with encryption support and playback position tracking

### Storage
- **Media Files**: Stored in `%APPDATA%/VideoVault/media/downloads/`
- **Encryption**: All files encrypted with unique keys
- **Cleanup**: Automatic cleanup of temporary download files

**VideoVault** - Your personal, secure video library.
