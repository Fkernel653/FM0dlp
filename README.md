# fm-dlp is a CLI tool for searching YouTube/YTMusic and downloading audio/video from 1000+ platforms

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/fm-dlp.svg)](https://pypi.org/project/fm-dlp/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-lightgrey)]()
[![Ruff](https://img.shields.io/badge/code%20style-ruff-261230?logo=ruff&logoColor=white)](https://docs.astral.sh/ruff/)

Download and tag high-quality music and video from YouTube, YouTube Music, and 1000+ sites — all from your terminal.

## ✨ Features

- **Multi-platform Search** — YouTube, YouTube Music
- **Search by Type** — Tracks or albums
- **Parallel Downloads** — Async support for multiple URLs
- **1000+ Supported Sites** — Any site yt-dlp supports (YouTube, SoundCloud, Bandcamp, etc.)
- **Audio Formats** — MP3, AAC, FLAC, M4A, Opus, Vorbis, WAV with configurable bitrate
- **Video Formats** — MP4, MKV, WebM, MOV, AVI, FLV with automatic audio codec selection
- **Metadata Embedding** — Title, artist, album tags + thumbnail (audio only)
- **Proxy Support** — HTTP, HTTPS, SOCKS4, SOCKS5, SOCKS5h for all requests (download supports all protocols; search via yt-music requires HTTP/HTTPS)
- **Cookie Support** — Browser cookies for restricted content
- **Cross-platform Config** — Stores config in standard app config directory (XDG, AppData, Application Support)

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ & FFmpeg

### Installation

#### Via pip (recommended)
```bash
pip install fm-dlp
```

#### Via uv
```bash
uv pip install fm-dlp
```

#### Via pipx (isolated environment)
```bash
pipx install fm-dlp
```

#### From source (development)

```bash
git clone https://github.com/Fkernel653/fm-dlp.git && cd fm-dlp
```

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
fm-dlp config ~/Music

# Search for tracks
fm-dlp search "artist name" --limit 5 --platform yt-music

# Search for albums
fm-dlp search "album name" --platform yt-music --type album

# Download audio
fm-dlp download "https://youtu.be/..." --codec mp3 --kbps 320

# Download video
fm-dlp download "https://youtu.be/..." --codec mp4
```

> **Note:** If installed from source, replace `fm-dlp` with `python modules/cli.py` in all examples.

## 📋 Commands

### `search` — Find music
```bash
fm-dlp search <query> [--limit 10] [--platform {yt-video|yt-music}] [--type {track|album}] [--proxy URL]
```
| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--platform` | `yt-video`, `yt-music` | `yt-music` | Search platform |
| `--type` | `track`, `album` | `track` | Content type to search |
| `--limit` | 1–∞ | 10 | Number of results |
| `--proxy` | URL | — | Proxy for requests |

### `download` — Download audio or video
```bash
fm-dlp download <urls> [--codec CODEC] [--kbps 256] [--quiet] [--max-concurrent 5] [--cookies browser] [--proxy URL]
```
| Option | Values | Default |
|--------|--------|---------|
| `--codec` | **Audio:** `mp3`, `aac`, `flac`, `m4a`, `opus`, `vorbis`, `wav`<br>**Video:** `mp4`, `mkv`, `webm`, `mov`, `avi`, `flv` | `m4a` (macOS) / `opus` |
| `--kbps` | 64–320 (audio only) | 256 |
| `--quiet` | Flag | False |
| `--max-concurrent` | 1–∞ | 5 |
| `--no-metadata` | Flag | False (metadata on) |
| `--cookies` | chrome, firefox, edge, etc. | — |
| `--proxy` | http://, socks5:// | — |

### Supported Proxies

fm-dlp supports the following proxy protocols:

| Protocol | Download | Search (yt-video) | Search (yt-music) |
|----------|:--------:|:-----------------:|:-----------------:|
| `http://` | ✅ | ✅ | ✅ |
| `https://` | ✅ | ✅ | ✅ |
| `socks4://` | ✅ | ✅ | ❌ |
| `socks5://` | ✅ | ✅ | ❌ |
| `socks5h://` | ✅ | ✅ | ❌ |

> **Note:** `socks5h://` performs DNS resolution through the proxy (remote DNS), while `socks5://` resolves DNS locally. Use `socks5h://` for better privacy with Tor.

**Examples:**
```bash
# HTTP proxy
fm-dlp download "URL" --proxy http://user:pass@proxy.example.com:8080

# SOCKS5 (Tor)
fm-dlp download "URL" --proxy socks5://127.0.0.1:9050

# SOCKS5h with remote DNS (recommended for Tor)
fm-dlp download "URL" --proxy socks5h://127.0.0.1:9050

# SOCKS5 for video search
fm-dlp search "query" --platform yt-video --proxy socks5://127.0.0.1:9050
```

**Video container audio codec mapping:**

| Video Container | Audio Codec | Typical Use |
|-----------------|-------------|-------------|
| `mp4` | `m4a` (AAC) | Universal compatibility |
| `mkv` | `opus` | High quality, modern |
| `webm` | `opus` | Web, streaming |
| `mov` | `m4a` (AAC) | Apple ecosystem |
| `avi` | `mp3` | Legacy hardware |
| `flv` | `aac` | Legacy web |

### `config` — Set or view download path
```bash
fm-dlp config <path>   # Set directory
fm-dlp config          # View current setting
```

Configuration is stored in the standard application config directory:
- **Linux:** `~/.config/fm-dlp/config.json`
- **macOS:** `~/Library/Application Support/fm-dlp/config.json`
- **Windows:** `%APPDATA%\fm-dlp\config.json`

## 📁 Project Structure
```
fm-dlp/
├── modules/
│   ├── __init__.py          # Package initializer
│   ├── __main__.py          # CLI entry point
│   ├── cli.py               # CLI entry point (cliss library)
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── search.py        # YouTube & YT Music search (tracks & albums)
│   │   └── download.py      # Async audio/video download engine (yt-dlp)
│   └── utils/
│       ├── __init__.py
│       ├── configer.py      # JSON config manager (read/write)
│       └── validator.py     # Input validation (URLs, codecs, proxies, bitrate)
│                            # + system dependency checks (ffmpeg)
├── pyproject.toml           # Project metadata & dependencies
├── README.md                # Project documentation
└── LICENSE                  # MIT License
```

> **Config file location:** `config.json` is automatically created in your system's standard application config directory on first run. See the `config` command section for OS-specific paths.

## 🔧 Requirements

| Dependency | Purpose |
|------------|---------|
| `yt-dlp` | YouTube extraction & download |
| `mutagen` | Audio metadata tagging |
| `ytmusicapi` | YouTube Music API |
| `platformdirs` | Cross-platform config paths |
| `color-kiss` | KISS-library for colors |
| `cliss` | KISS-library for CLI |
| **FFmpeg** | Audio/video conversion (system) |

## 📖 Examples

### Search Examples
```bash
# Search for tracks on YouTube Music
fm-dlp search "Sewerslvt" --limit 10 --platform yt-music

# Search for albums on YouTube Music
fm-dlp search "usedcvnt" --platform yt-music --type album

# Search for videos on YouTube
fm-dlp search "breakcore mix" --platform yt-video --limit 5

# Search with proxy
fm-dlp search "tokyona" --proxy socks5://127.0.0.1:9050
```

### Download Examples

**Audio:**
```bash
# Basic audio download
fm-dlp download "https://youtu.be/..." --codec flac

# Multiple URLs with custom quality
fm-dlp download "URL1 URL2 URL3" --codec mp3 --kbps 320

# Lossless download
fm-dlp download "URL" --codec wav
```

**Video:**
```bash
# Download as MP4
fm-dlp download "https://youtu.be/..." --codec mp4

# Download as MKV with Opus audio
fm-dlp download "https://youtu.be/..." --codec mkv

# Download as MOV for Apple devices
fm-dlp download "https://youtu.be/..." --codec mov
```

**Advanced:**
```bash
# Age-restricted content with cookies
fm-dlp download "URL" --cookies firefox

# Anonymous download via Tor
fm-dlp download "URL" --proxy socks5://127.0.0.1:9050

# Quiet mode with increased parallelism
fm-dlp download "URL1 URL2 URL3 URL4 URL5" --quiet --max-concurrent 10

# Download without metadata
fm-dlp download "URL" --no-metadata
```

### Maintenance
```bash
# Update to latest version
pip install --upgrade fm-dlp
```

### Complete Workflow
```bash
# 1. Set download location
fm-dlp config ~/Music

# 2. Search for an album
fm-dlp search "we had good times together, don't forget that" --limit 1 --type album

# 3. Download audio from album
fm-dlp download "https://music.youtube.com/playlist?list=OLAK5uy_muvgxae_oLSvDyo0q_zp0JrkBS73nkLMM" --codec flac

# 4. Search and download a video
fm-dlp search "goreshit" --platform yt-video
fm-dlp download "https://youtu.be/gnubBJ6dP4g" --codec mkv
```

## ❓ FAQ

### Why does fm-dlp exist when yt-dlp already downloads audio and video?

Think of fm-dlp as a **purpose-built stereo system**, while yt-dlp is a universal
multimedia Swiss Army knife. Yes, yt-dlp can extract audio, embed metadata,
and download video, but it takes a long string of flags to get there:

```bash
# Audio with yt-dlp
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 320k \
  --embed-metadata --embed-thumbnail -o "~/Music/%(title)s.%(ext)s" "URL"

# Video with yt-dlp
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best" --merge-output-format mp4 \
  -o "~/Videos/%(title)s.%(ext)s" "URL"
```

fm-dlp wraps all that into a clean, music-focused workflow:
- **Search** with human-readable, formatted output — no scraping IDs from text dumps
- **Download audio or video** with a single option — no memorising flag combinations
- **Cleaner tags** — when used with `search` results, artist and title come from
  structured music metadata rather than raw video descriptions with channel suffixes
- **Automatic format selection** — video containers automatically pick the best compatible audio codec

### Why does macOS default to M4A while other platforms default to Opus?

The defaults are chosen to match the **native music player experience** on each
operating system:

| Platform | Default | Reasoning |
|----------|---------|-----------|
| **macOS / iOS** | `m4a` (AAC) | Apple's entire ecosystem — Finder, Music.app, QuickTime, GarageBand — treats M4A/AAC as the first-class audio format. Album artwork, tagging, and playback are seamless. |
| **Linux / Windows** | `opus` | Opus offers superior perceptual quality at equivalent bitrates. It's the codec modern Android devices, desktop players (VLC, foobar2000, audacious), and browsers use natively. |

You can always override the default with `--codec mp3` (universal, legacy
hardware), `--codec flac` (lossless archival), or any other supported format.

### What video formats are supported and how do they work?

fm-dlp supports six video containers: `mp4`, `mkv`, `webm`, `mov`, `avi`, and `flv`.
When you choose a video format, fm-dlp automatically:
1. Downloads the best available video stream
2. Selects the optimal audio codec for that container (see mapping table above)
3. Merges them together using FFmpeg

For example, `--codec mkv` downloads VP9 video + Opus audio and packs them into an MKV container,
while `--codec mp4` prefers H.264 video + AAC audio for maximum device compatibility.

### Why is metadata embedding only available for audio?

Metadata embedding (title, artist, album, thumbnail) works only with audio codecs
(`mp3`, `aac`, `flac`, `m4a`, `opus`, `vorbis`, `wav`) using the `mutagen` library.
Video containers don't get automatic metadata tagging — this keeps the download
fast and avoids potential issues with video metadata standards.

### Why write this in Python instead of something faster?

The initial version was a personal script that solved a daily annoyance: finding
and tagging high-quality music without fighting CLI flags. Python allowed rapid
iteration and immediate real-world use.

Most of the actual "work" is performed by highly optimised native code:
`yt-dlp` for networking, `ffmpeg` (C/ASM) for transcoding. The Python layer
orchestrates these tools and handles metadata logic in **milliseconds** — the
network download and ffmpeg encoding dominate execution time regardless of the
language.

### How does the CLI argument parsing work?

fm-dlp uses [cliss](https://github.com/Fkernel653/cliss) — a lightweight, zero-dependency
wrapper over Python's standard `argparse` library. cliss provides:

- Type-driven argument generation from function signatures
- Automatic `--help` with colours (Python 3.12+)
- Async command support
- Clean error handling

This keeps the dependency footprint minimal (stdlib only) while eliminating
argparse boilerplate.

### Does this break YouTube's Terms of Service?

fm-dlp is an educational tool that demonstrates how public APIs and
open-source software can be combined. You are responsible for ensuring your
usage complies with the platform's Terms of Service and your local copyright
laws. Please support artists you enjoy.

## 🐛 Troubleshooting

### Configuration
| Issue | Solution |
|-------|----------|
| **Config file not found** | Run `fm-dlp config /your/download/path` first |
| **"Invalid path" error** | Ensure the directory exists and is writable |
| **Config reset after update** | `config.json` is preserved across updates — no action needed |

### Dependencies
| Issue | Solution |
|-------|----------|
| **"FFmpeg is not installed"** | Install FFmpeg and verify: `ffmpeg -version`<br>• macOS: `brew install ffmpeg`<br>• Linux: `sudo apt install ffmpeg`<br>• Windows: `winget install ffmpeg` |

### Search Issues
| Issue | Solution |
|-------|----------|
| **Album search returns no results** | Try different `--platform` (`yt-video` vs `yt-music`) or `--type` (`album` vs `track`) |
| **Too few results** | Increase limit: `--limit 20` |
| **Wrong content type** | Music search defaults to `track`. Use `--type album` for albums |

### Download Issues
| Issue | Solution |
|-------|----------|
| **Age-restricted video** | Use browser cookies: `--cookies chrome` (or `firefox`, `edge`, `brave`) |
| **Network blocked / 403 error** | Use a proxy: `--proxy socks5://127.0.0.1:9050` |
| **Slow downloads** | Increase concurrent downloads: `--max-concurrent 10` |
| **Audio codec error in video** | Video containers auto-select compatible audio. Use `mp4` or `mkv` for best compatibility |
| **Video format not supported** | Supported containers: `mp4`, `mkv`, `webm`, `mov`, `avi`, `flv` |
| **WAV has no metadata** | WAV doesn't support embedded tags. Use `flac` or `m4a` instead |
| **Codec not available** | yt-dlp selects best available. Try `opus` (best quality) or `mp3` (compatibility) |

### Proxy
| Issue | Solution |
|-------|----------|
| **"Invalid proxy URL"** | Format: `protocol://host:port`<br>• HTTP: `http://127.0.0.1:8080`<br>• SOCKS5: `socks5://127.0.0.1:9050` |
| **Proxy not working with yt-music** | yt-music only supports `http://` and `https://` proxies |

---

### Still stuck?
Run with verbose output to see detailed errors:
```bash
fm-dlp download "URL" --no-quiet
```

Check yt-dlp version compatibility:
```bash
yt-dlp --version
```

## 📄 License

MIT License — see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — YouTube extraction & download engine
- [ytmusicapi](https://github.com/sigma67/ytmusicapi) — YouTube Music API wrapper
- [mutagen](https://github.com/quodlibet/mutagen) — Audio metadata tagging
- [platformdirs](https://github.com/platformdirs/platformdirs) — Cross-platform config directory detection
- [color-kiss](https://github.com/Fkernel653/color-kiss) — KISS-library for colors
- [cliss](https://github.com/Fkernel653/cliss) — KISS-library for CLI

## ⚠️ Disclaimer

For educational purposes only. Users are responsible for complying with platform Terms of Service and applicable copyright laws.

---

**Author:** [Fkernel653](https://github.com/Fkernel653)
**Repository:** [github.com/Fkernel653/fm-dlp](https://github.com/Fkernel653/fm-dlp)
**PyPI:** [pypi.org/project/fm-dlp](https://pypi.org/project/fm-dlp/)
