# fm-dlp — search engine and installer of videos/tracks from YouTube

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-lightgrey)]()
[![Ruff](https://img.shields.io/badge/code%20style-ruff-261230?logo=ruff&logoColor=white)](https://docs.astral.sh/ruff/)

A powerful CLI tool for searching and downloading high-quality audio from YouTube and YouTube Music with automatic metadata embedding.

## ✨ Features

- **Multi-platform Search** — YouTube, YouTube Music
- **Search by Type** — Tracks or albums
- **Parallel Downloads** — Async support for multiple URLs
- **Multiple Formats** — M4A, MP3, FLAC, Opus with configurable bitrate
- **Metadata Embedding** — Title, artist, album tags + thumbnail
- **Proxy Support** — HTTP, HTTPS, SOCKS5 for all requests
- **Cookie Support** — Browser cookies for restricted content
- **Self-updating** — Built-in update mechanism via Git

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ & FFmpeg & Git

### Installation

#### 1. Clone Repository

```bash
git clone https://github.com/Fkernel653/fm-dlp.git && cd fm-dlp
```

#### 2. Install Dependencies

**uv** (recommended)
```bash
uv sync
```

**pip**
```bash
pip install .
```

**Poetry**
```bash
poetry install
```

**PDM**
```bash
pdm install
```

### Usage
```bash
# Set download directory (required first)
python fm-dlp.py config ~/Music

# Search for tracks
python fm-dlp.py search "artist name"  --limit 5 --platform yt-music

# Search for albums
python fm-dlp.py search "album name" --platform yt-music --type album

# Download
python fm-dlp.py download "https://youtu.be/..." --codec mp3 --kbps 320
```

## 📋 Commands

### `search` — Find music
```bash
python fm-dlp.py search <query> [--limit 10] [--platform {yt-video|yt-music}] [--type {track|album}] [--proxy URL]
```
| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--platform` | `yt-video`, `yt-music` | `yt-music` | Search platform |
| `--type` | `track`, `album` | `track` | Content type to search |
| `--limit` | 1–∞ | 10 | Number of results |
| `--proxy` | URL | — | Proxy for requests |

### `download` — Download audio
```bash
python fm-dlp.py download <urls> [--codec {m4a|mp3|flac|opus}] [--kbps 256] [--quiet False] [--max-concurrent 5] [--cookies browser] [--proxy URL]
```
| Option | Values | Default |
|--------|--------|---------|
| `--codec` | m4a, mp3, flac, opus | m4a (macOS) / opus |
| `--kbps` | 64–320 | 256 |
| `--quiet` | True/False (flag) | False |
| `--max-concurrent` | 1–∞ | 5 |
| `--cookies` | chrome, firefox, edge, etc. | — |
| `--proxy` | http://, socks5:// | — |

### `config` — Set or view download path
```bash
python fm-dlp.py config <path>   # Set directory
python fm-dlp.py config          # View current setting
```

### `update` — Update the tool
```bash
python fm-dlp.py update          # Pull latest version via Git
```
Requires Git to be installed and the project to be a clone of the repository.

## 📁 Project Structure
```
fm-dlp/
├── fm-dlp.py           # CLI entry point
├── config.json         # Download path config
├── pyproject.toml      # Project metadata and dependencies
├── README.md           # Project documentation
└── modules/
    ├── search.py       # Search implementations (tracks & albums)
    ├── download.py     # Audio download logic
    ├── configer.py     # Config manager
    ├── update.py       # Self-update via Git
    └── colors.py       # Terminal colors
```

## 🔧 Requirements

| Dependency | Purpose |
|------------|---------|
| `yt-dlp` | YouTube extraction & download |
| `mutagen` | Audio metadata tagging |
| `ytmusicapi` | YouTube Music API |
| `cyclopts` | CLI framework |
| **FFmpeg** | Audio conversion (system) |
| **Git** | Self-update mechanism (system) |

## 📖 Examples

### Search Examples
```bash
# Search for tracks on YouTube Music
python fm-dlp.py search "Sewerslvt" --limit 10 --platform yt-music

# Search for albums on YouTube Music
python fm-dlp.py search "usedcvnt" --platform yt-music --type album

# Search for videos on YouTube
python fm-dlp.py search "breakcore mix" --platform yt-video --limit 5

# Search with proxy
python fm-dlp.py search "tokyona" --proxy socks5://127.0.0.1:9050
```

### Download Examples
```bash
# Basic download
python fm-dlp.py download "https://youtu.be/..." --codec flac

# Multiple URLs with custom quality
python fm-dlp.py download "URL1 URL2 URL3" --codec mp3 --kbps 320

# Age-restricted content with cookies
python fm-dlp.py download "URL" --cookies firefox

# Anonymous download via Tor
python fm-dlp.py download "URL" --proxy socks5://127.0.0.1:9050
```

### Maintenance
```bash
# Update to latest version
python fm-dlp.py update

# Check current config
python fm-dlp.py config
```

### Complete Workflow
```bash
# 1. Set download location
python fm-dlp.py config ~/Music

# 2. Search for an album
python fm-dlp.py search "we had good times together, don't forget that" --limit 1 --type album

# 3. Download from search result URL
python fm-dlp.py download "https://music.youtube.com/playlist?list=OLAK5uy_muvgxae_oLSvDyo0q_zp0JrkBS73nkLMM"

# 4. Or search and download tracks directly
python fm-dlp.py search "goreshit" --platform yt-video
python fm-dlp.py download "https://youtu.be/gnubBJ6dP4g" --codec mp3 --kbps 320
```

## ❓ FAQ
### Why does fm-dlp exist when yt-dlp already downloads audio?

Think of fm-dlp as a **purpose-built stereo system**, while yt-dlp is a universal
multimedia Swiss Army knife. Yes, yt-dlp can extract audio and embed metadata,
but it takes a long string of flags to get there:

```bash
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 320k \
  --embed-metadata --embed-thumbnail -o "~/Music/%(title)s.%(ext)s" "URL"
```

fm-dlp wraps all that into a clean, music-focused workflow:
- **Search** with human-readable, formatted output — no scraping IDs from text dumps
- **Download** with a single option — no memorising flag combinations
- **Cleaner tags** — when used with `search` results, artist and title come from
  structured music metadata rather than raw video descriptions with channel suffixes

### Why does macOS default to M4A while other platforms default to Opus?

The defaults are chosen to match the **native music player experience** on each
operating system:

| Platform | Default | Reasoning |
|----------|---------|-----------|
| **macOS / iOS** | `m4a` (AAC) | Apple's entire ecosystem — Finder, Music.app, QuickTime, GarageBand — treats M4A/AAC as the first-class audio format. Album artwork, tagging, and playback are seamless. |
| **Linux / Windows** | `opus` | Opus offers superior perceptual quality at equivalent bitrates. It's the codec modern Android devices, desktop players (VLC, foobar2000, audacious), and browsers use natively. |

You can always override the default with `--codec mp3` (universal, legacy
hardware), `--codec flac` (lossless archival), or any other supported format.

### How does the update command work?

`fm-dlp update` runs `git pull` inside the project directory. This means:
- You must have **Git installed** and accessible from the terminal
- The project must be a **Git clone** (not a downloaded ZIP)
- It pulls the latest commits from the remote repository
- No version checking or rollback — it's intentionally simple and transparent

### Why write this in Python instead of something faster?

The initial version was a personal script that solved a daily annoyance: finding
and tagging high-quality music without fighting CLI flags. Python allowed rapid
iteration and immediate real-world use.

Most of the actual "work" is performed by highly optimised native code:
`yt-dlp` for networking, `ffmpeg` (C/ASM) for transcoding. The Python layer
orchestrates these tools and handles metadata logic in **milliseconds** — the
network download and ffmpeg encoding dominate execution time regardless of the
language.

### Does this break YouTube's Terms of Service?

fm-dlp is an educational tool that demonstrates how public APIs and
open-source software can be combined. You are responsible for ensuring your
usage complies with the platform's Terms of Service and your local copyright
laws. Please support artists you enjoy.

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Config file not found | Run `config <path>` first |
| FFmpeg error | Install FFmpeg: `ffmpeg --version` |
| Git not found | Install Git: `git --version` |
| Update fails | Ensure project is a Git clone, not a ZIP download |
| Age-restricted video | Use `--cookies chrome` |
| Network blocked | Try `--proxy http://proxy:port` |
| Invalid path | Ensure directory exists |
| Album search returns no results | Try different platform or search term |

## 📄 License

MIT License — see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — YouTube extraction & download engine
- [ytmusicapi](https://github.com/sigma67/ytmusicapi) — YouTube Music API wrapper
- [mutagen](https://github.com/quodlibet/mutagen) — Audio metadata tagging
- [cyclopts](https://github.com/BrianPugh/cyclopts) — Modern CLI framework

## ⚠️ Disclaimer

For educational purposes only. Users are responsible for complying with platform Terms of Service and applicable copyright laws.

---

**Author:** [Fkernel653](https://github.com/Fkernel653)  
**Repository:** [github.com/Fkernel653/fm-dlp](https://github.com/Fkernel653/fm-dlp)
