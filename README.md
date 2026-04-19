# fm-dlp — YouTube Music Downloader

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-lightgrey)]()
[![Ruff](https://img.shields.io/badge/code%20style-ruff-261230?logo=ruff&logoColor=white)](https://docs.astral.sh/ruff/)

A powerful CLI tool for searching and downloading high-quality audio from YouTube and YouTube Music with automatic metadata embedding.

## ✨ Features

- **Multi-platform Search** — YouTube, YouTube Music
- **Parallel Downloads** — Async support for multiple URLs
- **Multiple Formats** — M4A, MP3, FLAC, Opus with configurable bitrate
- **Metadata Embedding** — Title, artist, album tags + thumbnail
- **Proxy Support** — HTTP, HTTPS, SOCKS5 for all requests
- **Cookie Support** — Browser cookies for restricted content

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ & FFmpeg

### Installation
```bash
git clone https://github.com/Fkernel653/fm-dlp.git && cd fm-dlp
pip install -r requirements.txt
```

### Basic Usage
```bash
# Set download directory (required first)
python fm-dlp.py config ~/Music

# Search
python fm-dlp.py search "artist name" --platform=yt-music --limit=5

# Download
python fm-dlp.py download "https://youtu.be/..." --codec=mp3 --kbps=320
```

## 📋 Commands

### `search` — Find music
```bash
python fm-dlp.py search <query> [--limit=10] [--platform={yt-video|yt-music}] [--proxy=URL]
```
| Platform | Description |
|----------|-------------|
| `yt-video` | YouTube videos (default) |
| `yt-music` | YouTube Music songs only |

### `download` — Download audio
```bash
python fm-dlp.py download <urls> [--codec={m4a|mp3|flac|opus}] [--kbps=256] [--cookies=browser] [--proxy=URL]
```
| Option | Values | Default |
|--------|--------|---------|
| `--codec` | m4a, mp3, flac, opus | m4a |
| `--kbps` | 64–320 | 256 |
| `--cookies` | chrome, firefox, edge, etc. | — |
| `--proxy` | http://, socks5:// | — |

### `config` — Set download path
```bash
python fm-dlp.py config <path>   # Set directory
python fm-dlp.py config          # Show current
```

### `help` — Display documentation
```bash
python fm-dlp.py help
```

## 📁 Project Structure
```
fm-dlp/
├── fm-dlp.py           # CLI entry point
├── config.json         # Download path config
├── requirements.txt    # Dependencies
└── modules/
    ├── search.py       # Search implementations
    ├── download.py     # Audio download logic
    ├── add_metadata.py # Tagging handler
    ├── configer.py     # Config manager
    ├── help.py         # Help generator
    └── colors.py       # Terminal colors
```

## 🔧 Requirements

| Dependency | Purpose |
|------------|---------|
| `yt-dlp` | YouTube extraction & download |
| `mutagen` | Audio metadata tagging |
| `ytmusicapi` | YouTube Music API |
| `fake-useragent` | User agent rotation |
| `clite` | CLI framework |
| **FFmpeg** | Audio conversion (system) |

## 📖 Examples

```bash
# Basic search and download workflow
python fm-dlp.py search "sewerslvt" --platform=yt-music
python fm-dlp.py download "https://youtu.be/..." --codec=flac

# Multiple URLs with custom quality
python fm-dlp.py download "URL1 URL2 URL3" --codec=mp3 --kbps=320

# Age-restricted content with cookies
python fm-dlp.py download "URL" --cookies=firefox

# Anonymous download via Tor
python fm-dlp.py download "URL" --proxy=socks5://127.0.0.1:9050
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Config file not found | Run `config <path>` first |
| FFmpeg error | Install FFmpeg: `ffmpeg --version` |
| Age-restricted video | Use `--cookies=chrome` |
| Network blocked | Try `--proxy=http://proxy:port` |
| Invalid path | Ensure directory exists |

## 📄 License

MIT License — see [LICENSE](LICENSE) file.

## ⚠️ Disclaimer

For educational purposes only. Users are responsible for complying with platform Terms of Service and applicable copyright laws.

---

**Author:** [Fkernel653](https://github.com/Fkernel653)  
**Repository:** [github.com/Fkernel653/fm-dlp](https://github.com/Fkernel653/fm-dlp)