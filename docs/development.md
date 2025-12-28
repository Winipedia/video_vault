# Development Guide

This guide covers how to set up a development environment
and contribute to Video Vault.

## Development Setup

### Requirements

- Python 3.12 or 3.13
- [uv](https://github.com/astral-sh/uv) package manager
- Git

### Clone the Repository

```bash
git clone <repository-url>
cd video-vault
```

### Install Dependencies

```bash
# Install all dependencies including dev dependencies
uv sync
```

### Run in Development Mode

```bash
# Run the application
uv run video-vault

# Or run directly with Python
uv run python -m video_vault.main
```

## Project Structure

```text
video-vault/
├── video_vault/           # Main package
│   ├── main.py           # Application entry point
│   └── src/              # Source code
│       ├── core/         # Core business logic
│       │   ├── downloads.py    # Download functionality
│       │   ├── security.py     # Encryption/keyring
│       │   ├── ffmpeg.py       # FFmpeg integration
│       │   └── consts.py       # Constants
│       ├── db/           # Database layer
│       │   ├── models.py       # Django models
│       │   ├── setup.py        # Django configuration
│       │   └── migrations/     # Database migrations
│       └── ui/           # User interface
│           ├── stylesheet.py   # Global styles
│           ├── windows/        # Main window
│           └── pages/          # UI pages
│               ├── downloads.py      # Downloads page
│               ├── add_downloads.py  # Browser page
│               └── player.py         # Player page
├── tests/                # Test suite
├── docs/                 # Documentation
└── pyproject.toml        # Project configuration
```

## Key Technologies

### UI Framework

- **PySide6**: Qt for Python - provides the UI framework
- **winipyside**: Custom framework built on PySide6 for page-based navigation

### Video Processing

- **yt-dlp**: Downloads videos from various platforms
- **FFmpeg**: Video format conversion (bundled via imageio-ffmpeg)

### Database

- **Django ORM**: Database abstraction layer
- **SQLite**: Local database storage
- **winidjango**: Custom Django utilities

### Security

- **cryptography**: AES-GCM encryption
- **keyring**: Secure key storage in system keyring

## Development Tasks

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_video_vault/test_main.py

# Run with coverage
uv run pytest --cov=video_vault
```

### Code Quality

```bash
# Run linter
uv run ruff check .

# Auto-fix linting issues
uv run ruff check --fix .

# Run type checker
uv run mypy .

# Run security checks
uv run bandit -r video_vault/
```

### Database Migrations

When you modify models in `video_vault/src/db/models.py`:

```bash
# Create new migration
uv run python video_vault/src/db/make_migrations.py

# Migrations are automatically applied on app startup
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
uv run pre-commit install

# Run hooks manually
uv run pre-commit run --all-files
```

## Architecture Overview

### Application Flow

1. **Startup** (`main.py`):
   - Initialize Django and database
   - Create Qt application
   - Apply global stylesheet
   - Show main window

2. **Main Window** (`ui/windows/main.py`):
   - Discovers all page classes
   - Sets up page navigation
   - Shows Downloads page by default

3. **Page Lifecycle**:
   - `pre_setup()`: Initialize UI components
   - `setup()`: Configure layout and widgets
   - `post_setup()`: Final setup and connections

### Download Workflow

1. User clicks download button in browser page
2. `DownloadWorker` thread spawns
3. yt-dlp downloads video to temp directory
4. FFmpeg converts to MP4 format
5. Video is encrypted with AES-GCM
6. Encrypted file saved to media directory
7. Database record created
8. UI updated with new video

### Encryption Flow

1. **Key Management**:
   - Key stored in system keyring
   - Retrieved via `get_or_create_app_aes_gcm()`
   - Same key used for all videos

2. **Encryption** (during download):
   - Read unencrypted video data
   - Encrypt with `EncryptedPyQFile.encrypt_data_static()`
   - Save encrypted data to disk

3. **Decryption** (during playback):
   - `EncryptedPyQFile` QIODevice wraps encrypted file
   - Decrypts data on-the-fly as player reads
   - No unencrypted data written to disk

## Contributing

### Code Style

- Follow PEP 8 guidelines
- Use Google-style docstrings
- Type hints required for all functions
- Maximum line length: 88 characters (Ruff default)

### Commit Messages

Use conventional commit format:

```text
feat: add new feature
fix: fix bug
docs: update documentation
test: add tests
refactor: refactor code
```

### Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## Building for Distribution

### Create Executable

```bash
# Build with PyInstaller
uv run pyinstaller video_vault.spec
```

The executable will be in the `dist/` directory.

## Troubleshooting Development Issues

### Qt/PySide6 Issues

If you encounter Qt-related errors:

```bash
# Reinstall PySide6
uv pip install --force-reinstall PySide6
```

### Database Issues

If database migrations fail:

```bash
# Delete database and start fresh
rm -rf ~/.local/share/VideoVault/db/
```

### Import Errors

Ensure you're running commands with `uv run`
to use the correct virtual environment.
