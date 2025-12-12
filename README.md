# video-vault

<!-- tooling -->
[![pyrig](https://img.shields.io/badge/built%20with-pyrig-3776AB?logo=buildkite&logoColor=black)](https://github.com/Winipedia/pyrig)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://pre-commit.com/)
<!-- code-quality -->
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![mypy](https://img.shields.io/badge/type%20checked-mypy-039dfc.svg)](https://mypy-lang.org/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![pytest](https://img.shields.io/badge/tested%20with-pytest-46a2f1.svg?logo=pytest)](https://pytest.org/)
[![codecov](https://codecov.io/gh/Winipedia/video-vault/branch/main/graph/badge.svg)](https://codecov.io/gh/Winipedia/video-vault)
<!-- package-info -->
[![PyPI](https://img.shields.io/pypi/v/video-vault?logo=pypi&logoColor=white)](https://pypi.org/project/video-vault/)
[![Python](https://img.shields.io/badge/python-3.12|3.13-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/github/license/Winipedia/video-vault?v=2)](https://github.com/Winipedia/video-vault/blob/main/LICENSE)
<!-- ci/cd -->
[![CI](https://img.shields.io/github/actions/workflow/status/Winipedia/video-vault/health_check.yaml?label=CI&logo=github)](https://github.com/Winipedia/video-vault/actions/workflows/health_check.yaml)
[![CD](https://img.shields.io/github/actions/workflow/status/Winipedia/video-vault/release.yaml?label=CD&logo=github)](https://github.com/Winipedia/video-vault/actions/workflows/release.yaml)


---

> An application to download any video

---


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
