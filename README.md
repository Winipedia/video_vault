# video-vault

(This project uses [pyrig](https://github.com/Winipedia/pyrig))

A secure desktop application for downloading and managing videos from any platform. Built with PySide6, Video Vault downloads videos using yt-dlp, encrypts them with AES-GCM for secure storage, and provides an intuitive interface for playback with automatic position tracking and resume functionality.

## Pages

Video Vault consists of three main pages that provide a complete video download and playback workflow:

### Downloads Page

The **Downloads** page is the home screen and central hub of the application. It displays all your downloaded videos in a scrollable list, with each video represented by a button showing its display name.

**Features:**
- **Video List**: Scrollable area showing all downloaded videos ordered by creation date (newest first)
- **Context Menu**: Right-click or click any video button to access a menu with:
  - **Play**: Opens the video in the Player page, resuming from the last watched position
  - **Delete**: Removes the video from both the database and encrypted storage
- **Add Download Button**: Navigate to the Add Downloads page to download new videos (plus icon, top-right)
- **Delete All Button**: Removes all downloaded videos at once (garbage can icon, top-center)

**How it works:**
- Queries all `File` objects from the Django database
- Creates a button for each video with an attached context menu
- Coordinates with the Player page to manage playback state
- Automatically saves the current video's playback position before switching to a different video
- Stops playback if the currently playing video is deleted

### Add Downloads Page

The **Add Downloads** page provides an embedded web browser for navigating to video platforms and downloading content.

**Features:**
- **Embedded Browser**: Full-featured web browser for navigating to any video site (YouTube, Vimeo, etc.)
- **Download Button**: Extracts the current page URL and browser cookies to download the video (download arrow icon, top-right)
- **Cookie Support**: Automatically captures browser cookies for authenticated downloads (e.g., private videos, age-restricted content)

**How it works:**
- Extends the `BrowserPage` component from winipyside
- When the download button is clicked:
  1. Extracts the current URL from the browser
  2. Captures HTTP cookies for the current domain
  3. Spawns a `DownloadWorker` thread to handle the download asynchronously
  4. The worker uses yt-dlp to download the video in a temporary directory
  5. Converts the video to MP4 format using FFmpeg
  6. Encrypts the video file with AES-GCM encryption
  7. Saves the encrypted file to the media directory
  8. Creates a Django `File` model entry in the database
  9. Shows a toast notification when complete
  10. Updates the Downloads page with the new video

### Player Page

The **Player** page provides video playback with encrypted file support and automatic position tracking.

**Features:**
- **Video Playback**: Plays encrypted videos with transparent decryption
- **Position Tracking**: Automatically saves your playback position when you stop or switch videos
- **Resume Functionality**: Videos automatically resume from where you left off
- **Playback Controls**: Standard media controls (play/pause, seek, volume, etc.)

**How it works:**
- Extends the `PlayerPage` component from winipyside
- Uses a custom `EncryptedPyQFile` QIODevice that decrypts video data on-the-fly during playback
- Retrieves the AES-GCM encryption key from the system keyring
- Tracks the current file being played in `current_file` attribute
- On playback stop or video switch:
  1. Reads the current playback position from the media player
  2. Saves the position to the `File` model's `last_position` field
  3. Updates the database
- On playback start:
  1. Loads the encrypted file from disk
  2. Sets up the encrypted QIODevice with the decryption key
  3. Seeks to the saved `last_position`
  4. Begins playback

## Code Architecture

The `src` package contains the core application logic organized into three main packages:

### Core Package (`src/core`)

The **core** package contains the fundamental business logic and utilities for the application.

#### `downloads.py`

Handles the video download workflow with asynchronous processing.

**Key Components:**
- **`DownloadWorker`**: A `QThread` subclass that performs downloads in the background
  - Maintains a class-level registry (`ALL_WORKERS`) to track all active download threads
  - Accepts a URL and list of cookies for authenticated downloads
  - Executes the download in the `run()` method
  - Emits signals on completion to show notifications and update the UI
  - Automatically removes itself from the registry when finished

- **`add_download(url, cookies)`**: Orchestrates the complete download process
  - Creates a temporary directory for the download
  - Calls `do_download()` to fetch the video
  - Calls `save_download()` to encrypt and persist the file
  - Returns the created `File` model instance

- **`do_download(tempdir, url, cookies)`**: Performs the actual video download
  - Configures yt-dlp with FFmpeg location and format preferences
  - Downloads the best quality MP4 video and audio streams
  - Merges streams and converts to MP4 format
  - Returns the path to the downloaded file
  - Raises `DownloadError` on failure

- **`save_download(path)`**: Encrypts and saves the downloaded video
  - Calls `File.create_encrypted()` to encrypt the video file
  - Returns the created database record

#### `security.py`

Manages encryption keys and cryptographic operations.

**Key Components:**
- **`get_or_create_app_aes_gcm()`**: Retrieves or creates the application's AES-GCM cipher
  - Uses the system keyring to securely store the encryption key
  - Key is stored under the app name "VideoVault" and author "Winipedia"
  - Returns an `AESGCM` cipher instance from the cryptography library

- **`get_app_key_as_str()`**: Retrieves the encryption key as a string
  - Used by Django for the `SECRET_KEY` setting
  - Ensures the key exists in the keyring
  - Returns the key in string format

**Security Model:**
- All encryption keys are stored in the OS-level keyring (Keychain on macOS, Credential Manager on Windows, Secret Service on Linux)
- Uses AES-GCM (Authenticated Encryption with Associated Data) for strong encryption
- Keys are never stored in plaintext in the application code or configuration files

#### `ffmpeg.py`

Provides FFmpeg integration for video processing.

**Key Components:**
- **`get_ffmpeg_path()`**: Locates the FFmpeg executable
  - Uses the `imageio-ffmpeg` package which bundles FFmpeg binaries
  - Returns a `Path` object pointing to the FFmpeg executable
  - Returns `None` if FFmpeg is not found
  - Logs the FFmpeg location for debugging

#### `consts.py`

Defines application-wide constants.

**Constants:**
- **`APP_NAME`**: "VideoVault" - derived from the package name using pyrig utilities
- **`AUTHOR`**: "Winipedia" - used for keyring storage and platformdirs

### Database Package (`src/db`)

The **db** package manages data persistence using Django ORM with SQLite.

#### `models.py`

Defines the database schema and model methods.

**Models:**
- **`File`**: Represents a downloaded and encrypted video file
  - Extends `BaseModel` from winidjango (provides `id`, `created_at`, `updated_at` fields)
  - **Fields:**
    - `file`: `FileField` storing the encrypted video file (uploaded to "downloads" directory)
    - `last_position`: `BigIntegerField` tracking playback position in milliseconds (default: 0)

  - **Methods:**
    - `delete_file(*args, **kwargs)`: Deletes both the file from disk and the database record
    - `create_encrypted(path, **kwargs)`: Class method that encrypts a video file and creates a database entry
      - Reads the unencrypted file data
      - Encrypts using `EncryptedPyQFile.encrypt_data_static()` with AES-GCM
      - Saves the encrypted data to the media directory
      - Creates and returns a `File` instance

  - **Properties:**
    - `display_name`: Returns the filename without extension for UI display

#### `setup.py`

Configures Django settings and initializes the database.

**Key Components:**
- **`setup_django()`**: Initializes Django with application-specific settings
  - Checks if Django is already configured to avoid re-initialization
  - Handles frozen app environments (PyInstaller) by setting up stdout/stderr
  - Configures paths using `platformdirs` for cross-platform compatibility:
    - Database: `~/.local/share/VideoVault/db/db.sqlite3` (Linux/macOS) or equivalent on Windows
    - Media files: `~/.local/share/VideoVault/media/`
  - Configures Django settings:
    - SQLite database backend
    - Registers the `db` app for migrations
    - Sets media root and URL
    - Uses the encryption key as Django's `SECRET_KEY`
  - Calls `django.setup()` to initialize the ORM
  - Runs migrations automatically to ensure database schema is up-to-date

#### `make_migrations.py`

Script for creating database migrations during development.

**Usage:**
- Run directly to generate new migration files when models change
- Calls Django's `makemigrations` command for the `db` app
- Migrations are stored in `migrations/` directory and included in version control

### UI Package (`src/ui`)

The **ui** package contains all user interface components.

#### `stylesheet.py`

Defines the global application stylesheet with a Netflix-inspired dark theme.

**Design System:**
- **Colors:**
  - Background: `#221F1F` (dark charcoal)
  - Text: `#FFFFFF` (white)
  - Primary accent: `#E50914` (Netflix red)
  - Hover state: `#B20710` (darker red)
  - Pressed state: `#830F10` (darkest red)
  - Borders: `#555555` (subtle gray)

- **Typography:**
  - Font family: Segoe UI, sans-serif
  - Base font size: 14px

- **Components Styled:**
  - `QMainWindow` and `QWidget`: Dark background with white text
  - `QPushButton`: Red buttons with hover and pressed states
  - `QMenu`: Red context menus with hover effects and styled separators

**Usage:**
- Applied globally to the entire application via `QApplication.setStyleSheet()` in `main.py`

#### `windows/main.py`

Defines the main application window.

**Key Components:**
- **`VideoVault`**: Main window class extending `BaseWindow` from winipyside
  - **`get_all_page_classes()`**: Auto-discovers all page classes from the `pages` package
  - **`get_start_page_cls()`**: Returns `DownloadsPage` as the initial page
  - **`pre_setup()`**: Sets the window icon to a play icon SVG
  - **`setup()`**: Empty hook for additional setup (currently unused)
  - **`post_setup()`**: Empty hook for post-initialization setup (currently unused)

**Architecture:**
- Uses the winipyside framework's page-based navigation system
- Pages are automatically registered and can navigate between each other
- Window is shown maximized on startup

#### `pages/` Package

Contains the three main page classes (documented in the "Pages" section above):
- `downloads.py`: Downloads management page
- `add_downloads.py`: Browser-based download page
- `player.py`: Video playback page

Each page extends base classes from winipyside and implements the pre_setup/setup/post_setup lifecycle hooks.
