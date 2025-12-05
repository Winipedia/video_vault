# User Guide

This guide covers everything you need to know to use Video Vault effectively.

## Installation

### Requirements

- Python 3.12 or 3.13
- [uv](https://github.com/astral-sh/uv) package manager

### Installing Video Vault

```bash
uv pip install video-vault
```

### Running Video Vault

```bash
video-vault
```

The application will launch in maximized mode showing the Downloads page.

## Application Overview

Video Vault has three main pages:

1. **Downloads Page** - Your video library (home page)
2. **Add Downloads Page** - Embedded browser for downloading videos
3. **Player Page** - Video playback with position tracking

## Downloading Videos

### Step-by-Step

1. Click the **"+"** button in the top-right corner of the Downloads page
2. The embedded browser will open
3. Navigate to any video URL (e.g., YouTube, Vimeo)
4. Click the **download arrow** button in the top-right corner
5. Wait for the download to complete - you'll see a notification when done
6. The video will appear in your Downloads page library

### Supported Platforms

Video Vault uses yt-dlp, which supports hundreds of video platforms including:

- YouTube
- Vimeo
- Dailymotion
- Twitter/X
- Facebook
- Instagram
- And many more

### Cookie Support

The embedded browser automatically captures cookies, allowing you to download:

- Private videos
- Age-restricted content
- Videos requiring authentication

Simply log in to the platform in the embedded browser before downloading.

## Playing Videos

### Starting Playback

1. From the Downloads page, click on any video button
2. Select **"Play"** from the menu
3. The video will open in the Player page
4. Playback automatically resumes from your last position

### Playback Controls

The player includes standard media controls:

- **Play/Pause**: Space bar or click the play button
- **Seek**: Click on the timeline or use arrow keys
- **Volume**: Adjust with the volume slider
- **Fullscreen**: Click the fullscreen button

### Position Tracking

Video Vault automatically saves your playback position when you:

- Stop playback
- Switch to a different video
- Close the application

When you return to a video, it will resume exactly where you left off.

## Managing Videos

### Deleting a Video

1. Click on a video button in the Downloads page
2. Select **"Delete"** from the menu
3. The video will be removed from both the database and disk

### Deleting All Videos

1. Click the **garbage can** button at the top-center of the Downloads page
2. All videos will be removed from your library

**Note**: Deleted videos cannot be recovered. The encrypted files are permanently removed.

## Data Storage

### File Locations

Video Vault stores data in platform-specific locations:

**Linux/macOS**:
- Database: `~/.local/share/VideoVault/db/db.sqlite3`
- Videos: `~/.local/share/VideoVault/media/downloads/`

**Windows**:
- Database: `%LOCALAPPDATA%\VideoVault\db\db.sqlite3`
- Videos: `%LOCALAPPDATA%\VideoVault\media\downloads\`

### Encryption

All downloaded videos are encrypted using AES-GCM encryption. The encryption key is stored securely in your system's keyring:

- **macOS**: Keychain
- **Windows**: Credential Manager
- **Linux**: Secret Service (via keyring library)

Videos are encrypted before being saved to disk and decrypted on-the-fly during playback.

## Troubleshooting

### Download Fails

If a download fails:

1. Check your internet connection
2. Verify the video URL is accessible in a regular browser
3. Try logging in to the platform in the embedded browser
4. Check the notification message for specific error details

### Video Won't Play

If a video won't play:

1. Ensure the video downloaded completely (check the notification)
2. Try deleting and re-downloading the video
3. Check that the video file exists in the media directory

### Application Won't Start

If the application won't launch:

1. Verify Python 3.12 or 3.13 is installed
2. Reinstall Video Vault: `uv pip install --force-reinstall video-vault`
3. Check for error messages in the terminal

## Tips and Best Practices

- **Video Quality**: Videos are downloaded in the best available MP4 format
- **Storage Space**: Monitor your disk space - encrypted videos take the same space as unencrypted ones
- **Backup**: The database and media files can be backed up from the data storage locations
- **Privacy**: All videos are stored locally and encrypted - nothing is uploaded to external servers

