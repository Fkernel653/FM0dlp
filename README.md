# fm-dlp - YouTube & SoundCloud Music Downloader

A powerful command-line tool for searching and downloading high-quality audio from YouTube, YouTube Music, and SoundCloud. Built with Python, using `yt-dlp` for downloads and native search implementations with automatic metadata embedding.

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-lightgrey)
![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-red.svg)

## 📋 Features

### Search Capabilities
- **YouTube Video Search**: Search using `yt-dlp` with rich metadata (views, duration, channel)
- **YouTube Music Search**: Dedicated music search via `ytmusicapi` for song-only results
- **SoundCloud Search**: Async search with 30-second timeout and track details

### Download Features
- **High-Quality Audio Extraction**: Download best available audio stream
- **Multiple Audio Formats**: M4A, MP3, FLAC, Opus via `--codec` parameter
- **Configurable Bitrate**: Adjust quality from 64-320 kbps with `--kbps`
- **Automatic Metadata Embedding**: Adds title, artist, and album tags to downloaded files
- **Thumbnail Embedding**: Album art automatically embedded into audio files
- **Browser Cookie Support**: Pass cookies from Chrome/Firefox/Edge for restricted content

### Configuration & UX
- **Persistent Configuration**: Save download directory in `config.json`
- **Colorful Terminal Output**: ANSI color codes for better readability
- **Async Search Operations**: Non-blocking SoundCloud search with timeout
- **Formatted Results**: Tree structure output with metadata
- **Cross-Platform Support**: Works on Linux, macOS, and Windows

## 🚀 Installation

### Prerequisites

- **Python 3.9 or higher** (uses `match` statement from Python 3.10+)
- **FFmpeg** - Required for audio conversion and thumbnail embedding

### Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
1. Download from [FFmpeg.org](https://ffmpeg.org/download.html)
2. Add the `bin` folder to your system PATH
3. Verify installation: `ffmpeg -version`

### Install fm-dlp

```bash
# Clone the repository
git clone https://github.com/Fkernel653/fm-dlp.git
cd fm-dlp

# Install dependencies
pip install -r requirements.txt
```

## 🔧 Configuration

### Set Download Directory

```bash
python fm-dlp.py config /path/to/your/music/folder
```

View current config:
```bash
python fm-dlp.py config
```

The path is saved in `config.json` in the project root:
```json
{
    "path": "/home/user/Music/Downloads"
}
```

## 📖 Usage

```bash
python fm-dlp.py <command> [arguments] [options]
```

### Commands Overview

| Command | Description |
|---------|-------------|
| `search` | Search for music across platforms |
| `download` | Download audio from URL |
| `config` | Set or view download directory |
| `help` | Display help menu |

### 1. Search for Music

```bash
# YouTube video search (default)
python fm-dlp.py search "your query" --limit=10

# YouTube Music search
python fm-dlp.py search "your query" --variable=yt-music --limit=5

# SoundCloud search
python fm-dlp.py search "your query" --variable=soundcloud --limit=5
```

**Parameters:**
- `query` (required) - Search term
- `--limit` - Max results (default: 10)
- `--variable` - Platform: `yt-video`, `yt-music`, or `soundcloud` (default: `yt-video`)

**Examples:**
```bash
# Search YouTube videos
python fm-dlp.py search "Sewerslvt"

# Search YouTube Music
python fm-dlp.py search "lofi hip hop" --variable=yt-music --limit=5

# Search SoundCloud
python fm-dlp.py search "breakcore" --variable=soundcloud --limit=5
```

**Output Example:**
```
1. Song Title
   ├─ Artist Name
   ├─ 1,234,567 views | 3:45
   └─ https://youtu.be/VIDEO_ID
   ──────────────────────────────────────────────────
```

### 2. Download Audio

```bash
# Basic download (M4A, 256 kbps)
python fm-dlp.py download "https://youtu.be/VIDEO_ID"

# Custom format and quality
python fm-dlp.py download "URL" --codec=mp3 --kbps=320

# Lossless FLAC download
python fm-dlp.py download "URL" --codec=flac --kbps=320

# With browser cookies for age-restricted content
python fm-dlp.py download "URL" --cookies=chrome

# Opus format for best compression
python fm-dlp.py download "URL" --codec=opus --kbps=128
```

**Parameters:**
- `url` (required) - YouTube video URL
- `--codec` - Output format: `m4a`, `mp3`, `flac`, `opus` (default: `m4a`)
- `--kbps` - Bitrate in kbps (default: 256)
- `--cookies` - Browser for cookies: `chrome`, `firefox`, `edge`, `safari` (optional)
- `--ffmpeg` - Reserved for future use (default: "True")

**Supported Codecs & Bitrates:**

| Codec | Extension | Recommended Bitrate | Best For |
|-------|-----------|---------------------|----------|
| M4A (AAC) | .m4a | 256 kbps | General use, good quality/size |
| MP3 | .mp3 | 320 kbps | Maximum compatibility |
| FLAC | .flac | variable (lossless) | Archiving, audiophiles |
| Opus | .opus | 128 kbps | Best compression, modern players |

**Note:** Download path must be configured first with `config` command.

### 3. Configure Download Path

```bash
# Set download directory
python fm-dlp.py config ~/Music/Downloads

# Windows path example
python fm-dlp.py config "C:\Users\Username\Music\Downloads"

# View current configuration
python fm-dlp.py config
```

### 4. Get Help

```bash
# Full help menu
python fm-dlp.py help

# Quick help (if implemented)
python fm-dlp.py --help
```

## 📁 Project Structure

```
fm-dlp/
├── fm-dlp.py              # Main CLI entry point (clite framework)
├── config.json            # Persistent configuration (auto-generated)
├── requirements.txt       # Python dependencies
├── README.md              # Documentation
├── LICENSE                # MIT License
└── modules/
    ├── __init__.py        # Package initializer
    ├── search.py          # YouTube, YouTube Music & SoundCloud search
    ├── download.py        # Audio download with yt-dlp & metadata
    ├── add_metadata.py    # Metadata tagging for all formats
    ├── configer.py        # Config management (JSON)
    ├── help.py            # Help menu generation
    └── colors.py          # ANSI color constants
```

## 🛠️ Technical Details

### Search Implementation

| Platform | Method | Library | Features |
|----------|--------|---------|----------|
| **YouTube Video** | yt-dlp flat extraction | `yt-dlp` | Views, duration, channel, URL |
| **YouTube Music** | API search with filter | `ytmusicapi` | Song-only results, artists |
| **SoundCloud** | Async wrapper with timeout | `soundcloud-v2` | Date, duration, artist, permalink |

### Download Pipeline

```
1. Extract video info (yt-dlp)
2. Download best audio stream
3. Download thumbnail
4. Convert audio (FFmpeg)
5. Embed thumbnail
6. Add metadata tags (mutagen)
7. Save to configured directory
```

### Metadata Support by Format

| Format | Library | Tags Added |
|--------|---------|-------------|
| M4A/MP4 | mutagen.mp4 | `\xa9nam`, `\xa9ART`, `\xa9alb` |
| MP3 | mutagen.id3 | TIT2, TPE1, TALB |
| FLAC | mutagen.flac | title, artist, album |
| Opus | mutagen.oggopus | title, artist, album |

### Color Scheme

| Color | Usage |
|-------|-------|
| 🔴 Red | Errors, URLs, video IDs |
| 🟢 Green | Success messages, config status |
| 🟡 Yellow | Command names, warnings |
| 🔷 Cyan | Result numbering, headers, command names |
| ⚪ Gray | Tree lines, separators, descriptions |
| 🟣 Magenta | Help section headers, GitHub info |

## ⚠️ Requirements

### Python Dependencies (from `requirements.txt`)

| Package | Version | Purpose |
|---------|---------|---------|
| `yt-dlp` | latest | YouTube downloading and audio extraction |
| `mutagen` | latest | Audio metadata tagging for all formats |
| `soundcloud-v2` | latest | SoundCloud API wrapper |
| `ytmusicapi` | latest | YouTube Music search API |
| `fake-useragent` | latest | Random user agent rotation |
| `clite` | latest | CLI framework for command routing |

### System Dependencies

- **FFmpeg** - Required for audio conversion and thumbnail embedding (must be in PATH)
- **Python 3.9+** - Runtime environment

## 🔥 Usage Examples

### Complete Workflow Example

```bash
# 1. Configure download directory
python fm-dlp.py config ~/Music/Downloads

# 2. Search for a song
python fm-dlp.py search "midnight city m83" --limit=3

# Output:
# 1. M83 - Midnight City
#    ├─ M83
#    ├─ 123,456,789 views | 4:03
#    └─ https://youtu.be/dX3k_QDnzHE

# 3. Download the song in high-quality MP3
python fm-dlp.py download https://youtu.be/dX3k_QDnzHE --codec=mp3 --kbps=320

# Output:
# Download completed successfully!
# Metadata added successfully!
```

### Advanced Examples

```bash
# Download entire playlist (via URL)
python fm-dlp.py download "https://youtube.com/playlist?list=PL..."

# Age-restricted video with Firefox cookies
python fm-dlp.py download "URL" --cookies=firefox

# Lossless FLAC for archiving
python fm-dlp.py download "URL" --codec=flac

# Small file size with Opus
python fm-dlp.py download "URL" --codec=opus --kbps=96

# Search YouTube Music for specific genre
python fm-dlp.py search "chill synthwave" --variable=yt-music --limit=10
```

## 🐛 Troubleshooting

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| **"Config file not found!"** | Run `python fm-dlp.py config /your/download/path` first |
| **Download fails with FFmpeg error** | Ensure FFmpeg is installed: `ffmpeg -version` |
| **Age-restricted video error** | Use cookies from logged-in browser: `--cookies=chrome` |
| **SoundCloud search timeout** | Reduce limit: `--limit=3` or try again |
| **Metadata not added** | Check file permissions and format support |
| **"No video found"** | Video may be private, deleted, or region-restricted |
| **Invalid download path** | Ensure directory exists and is writable |

### Debug Mode

For verbose output, yt-dlp will show download progress. Check the console for specific error messages.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests if available
5. Commit with clear messages: `git commit -m 'Add amazing feature'`
6. Push to branch: `git push origin feature/amazing-feature`
7. Submit a Pull Request

### Code Style Guidelines
- Follow PEP 8 conventions
- Use type hints for function parameters and returns
- Add docstrings for all functions and classes
- Use color constants from `colors.py` for terminal output
- Handle exceptions gracefully with user-friendly messages

## 📄 License

Distributed under the MIT License. See `LICENSE` file for details.

## 👨‍💻 Author

**Fkernel653** - [GitHub](https://github.com/Fkernel653)

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Feature-rich YouTube downloading library
- [mutagen](https://github.com/quodlibet/mutagen) - Audio metadata handling
- [soundcloud-v2](https://github.com/7x11x13/soundcloud-v2) - SoundCloud API wrapper
- [ytmusicapi](https://github.com/sigma67/ytmusicapi) - YouTube Music API
- [clite](https://pypi.org/project/clite/) - Simple CLI framework
- [fake-useragent](https://github.com/hellysmile/fake-useragent) - User agent rotation

## ⚠️ Disclaimer

**For educational purposes only.** Users are responsible for complying with platform Terms of Service and applicable copyright laws. Download only content you have permission to download.

---

### Quick Reference Card

```bash
# Common commands cheat sheet
fm-dlp config ~/Music/Downloads          # Set download path
fm-dlp search "song name"                 # Search YouTube
fm-dlp download URL                       # Download as M4A 256kbps
fm-dlp download URL --codec=mp3 --kbps=320  # Download as MP3
fm-dlp help                               # Show help
```

**Star ⭐ this repository if you find it useful!**