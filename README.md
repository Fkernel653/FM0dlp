# fm-dlp - YouTube & SoundCloud Music Downloader

A powerful command-line tool for searching and downloading high-quality audio from YouTube, YouTube Music, and SoundCloud. Built with Python, using `yt-dlp` for downloads and native search implementations with automatic metadata embedding.

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-lightgrey)
![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-red.svg)

## 📋 Features

### Search Capabilities
- **YouTube-Video Search**: Search using `yt-dlp` with rich metadata (views, duration, channel)
- **YouTube-Music Search**: Dedicated music search via `ytmusicapi` for song-only results
- **SoundCloud Search**: Search from SoundCloud using `soundcloud-v2`

### Download Features
- **Parallel Downloads**: Download multiple URLs simultaneously with async support
- **High-Quality Audio Extraction**: Download best available audio stream
- **Multiple Audio Formats**: M4A, AAC, MP3, FLAC, Opus via `--codec` parameter
- **Configurable Bitrate**: Adjust quality from 64-320 kbps with `--kbps`
- **Automatic Metadata Embedding**: Adds title, artist, and album tags to downloaded files
- **Thumbnail Embedding**: Album art automatically embedded into audio files
- **Browser Cookie Support**: Pass cookies from Chrome/Firefox/Edge for restricted content

### Configuration & UX
- **Persistent Configuration**: Save download directory in `config.json`
- **Colorful Terminal Output**: ANSI color codes for better readability
- **Formatted Results**: Tree structure output with metadata
- **Cross-Platform Support**: Works on Linux, macOS, and Windows

## 🚀 Installation

### Prerequisites

- **Python 3.10 or higher** (uses `match` statement from Python 3.10+)
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
    "path": "/home/<YOUR_USERNAME>/Music"
}
```

**Note:** The download directory must be configured before downloading any audio.

## 📖 Usage

```bash
python fm-dlp.py <command> [arguments] [options]
```

### Commands Overview

| Command | Description |
|---------|-------------|
| `search` | Search for music across platforms |
| `download` | Download audio from one or more URLs |
| `config` | Set or view download directory |
| `help` | Display help menu |

### 1. Search for Music

```bash
# YouTube video search (default)
python fm-dlp.py search "<YOUR QUERY>" --limit=10

# YouTube Music search
python fm-dlp.py search "<YOUR QUERY>" --platform=yt-music --limit=5

# SoundCloud search
python fm-dlp.py search "<YOUR QUERY>" --platform=soundcloud --limit=5
```

**Parameters:**
- `query` (required) - Search term
- `--limit` - Max results (default: 10)
- `--platform` - Platform: `yt-video`, `yt-music`, or `soundcloud` (default: `yt-video`)

**Note:** The `all` platform is not currently implemented. Use specific platforms instead.

**Examples:**
```bash
# Search YouTube videos
python fm-dlp.py search "Sewerslvt"

# Search YouTube Music
python fm-dlp.py search "usedcvnt" --platform=yt-music --limit=5

# Search SoundCloud
python fm-dlp.py search "tokyona" --platform=soundcloud --limit=5
```

**Output Example:**
```
1. Song Title
   ├─ Artist Name
   ├─ 1,234,567 views | 3:45
   └─ https://youtu.be/<VIDEO_ID>
   ──────────────────────────────────────────────────
```

### 2. Download Audio

```bash
# Basic download (M4A, 256 kbps)
python fm-dlp.py download "https://youtu.be/<VIDEO_ID>"

# Download multiple URLs (space-separated, quoted)
python fm-dlp.py download "https://youtu.be/abc123 https://youtu.be/def456"

# Custom format and quality
python fm-dlp.py download "URL" --codec=mp3 --kbps=320

# Lossless FLAC download
python fm-dlp.py download "URL" --codec=flac

# With browser cookies for age-restricted content
python fm-dlp.py download "URL" --cookies=chrome

# Opus format for best compression
python fm-dlp.py download "URL" --codec=opus --kbps=128
```

**Parameters:**
- `urls` (required) - Space-separated YouTube URLs (must be quoted)
- `--codec` - Output format: `m4a`, `aac`, `mp3`, `flac`, `opus` (default: `m4a`)
- `--kbps` - Bitrate in kbps (default: 256)
- `--cookies` - Browser for cookies: `chrome`, `firefox`, `edge`, `safari` (optional)
- `--ffmpeg` - Reserved for future use (default: "True")

**Supported Codecs & Bitrates:**

| Codec | Extension | Recommended Bitrate | Best For |
|-------|-----------|---------------------|----------|
| M4A (AAC) | .m4a | 256 kbps | General use, good quality/size |
| AAC | .aac | 256 kbps | Apple ecosystem, streaming |
| MP3 | .mp3 | 320 kbps | Maximum compatibility |
| FLAC | .flac | lossless | Archiving, audiophiles |
| Opus | .opus | 128 kbps | Best compression, modern players |

**Note:** Download path must be configured first with `config` command.

### 3. Configure Download Path

```bash
# Set download directory
python fm-dlp.py config ~/Music

# Windows path example
python fm-dlp.py config "C:\Users\<YOUR_USERNAME>\Music"

# View current configuration
python fm-dlp.py config
```

### 4. Get Help

```bash
# Full help menu
python fm-dlp.py help
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
| **SoundCloud** | Search Wrapper with SoundCloud | `soundcloud-v2` | Date, duration, artist, permalink |

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

| Format | Metadata Library | Tags Added |
|--------|------------------|-------------|
| M4A/AAC | mutagen.mp4 | `©nam` (title), `©ART` (artist), `©alb` (album) |
| MP3 | mutagen.id3 | TIT2 (title), TPE1 (artist), TALB (album) |
| FLAC | mutagen.flac | title, artist, album (Vorbis comments) |
| Opus | mutagen.oggopus | title, artist, album (Ogg container) |

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
- **Python 3.10+** - Runtime environment

## 🔥 Usage Examples

### Complete Workflow Example

```bash
# 1. Configure download directory
python fm-dlp.py config ~/Music

# 2. Search for a song
python fm-dlp.py search "tonight, lucar joins the hunt" --limit=3

# Output:
# 1. tonight, lucar joins the hunt
#    ├─ Sqarz - Topic
#    ├─ 395,424 views | 2:56
#    └─ https://youtu.be/BB_d2-WVgXI

# 3. Download the song in high-quality MP3
python fm-dlp.py download "https://youtu.be/BB_d2-WVgXI" --codec=mp3 --kbps=320

# Output:
# Starting: https://youtu.be/BB_d2-WVgXI
# ✓ Downloaded: tonight, lucar joins the hunt
```

### Advanced Examples

```bash
# Age-restricted video with Firefox cookies
python fm-dlp.py download "<YOUR_URL>" --cookies=firefox

# Lossless FLAC for archiving
python fm-dlp.py download "<YOUR_URL>" --codec=flac

# Small file size with Opus
python fm-dlp.py download "<YOUR_URL>" --codec=opus --kbps=96

# Download multiple tracks at once
python fm-dlp.py download "https://youtu.be/abc123 https://youtu.be/def456" --codec=mp3

# Search YouTube Music for specific genre
python fm-dlp.py search "breakcore" --platform=yt-music --limit=10
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
| **Config file corrupted** | Delete `config.json` and reconfigure with `config <path>` |

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