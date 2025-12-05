# video-vault

[![built with pyrig](https://img.shields.io/badge/built%20with-pyrig-3776AB?logo=python&logoColor=white)](https://github.com/Winipedia/pyrig)

A secure desktop application for downloading and managing videos from any platform with encrypted storage.

## Features

- **Download videos** from any platform (YouTube, Vimeo, etc.) using an embedded browser
- **Encrypted storage** with AES-GCM encryption for all downloaded videos
- **Built-in video player** with automatic position tracking and resume functionality
- **Cross-platform** support (Windows, macOS, Linux)
- **Dark theme** UI inspired by Netflix

## Installation

### Requirements

- Python 3.12 or 3.13
- [uv](https://github.com/astral-sh/uv) package manager

### Install

```bash
uv pip install video-vault
```

### Run

```bash
video-vault
```

## Quick Start

1. **Launch the application** - The Downloads page will open showing your video library
2. **Download a video**:
   - Click the "+" button in the top-right corner
   - Navigate to any video URL in the embedded browser
   - Click the download button (arrow icon)
   - Wait for the download and encryption to complete
3. **Play a video**:
   - Click on any video in your library
   - Select "Play" from the menu
   - The video will resume from where you left off

## Documentation

For more detailed information, see the [documentation](docs/index.md):

- [User Guide](docs/user-guide.md) - How to use the application
- [Development Guide](docs/development.md) - How to contribute and develop

## Security

All downloaded videos are encrypted using AES-GCM encryption. Encryption keys are stored securely in your system's keyring:
- **macOS**: Keychain
- **Windows**: Credential Manager
- **Linux**: Secret Service

## Tech Stack

- **UI Framework**: PySide6 (Qt for Python)
- **Video Download**: yt-dlp
- **Video Processing**: FFmpeg (bundled via imageio-ffmpeg)
- **Database**: Django ORM with SQLite
- **Encryption**: AES-GCM via cryptography library

## License

See [LICENSE](LICENSE) file for details.
