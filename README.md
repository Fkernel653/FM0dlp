# FM-dlp - YouTube & SoundCloud Music Downloader

A powerful command-line tool for searching and downloading audio from YouTube and SoundCloud. Built with Python, this tool uses `scrapetube` for YouTube searching (no API key required!) and `yt-dlp` for high-quality audio extraction.

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-lightgrey)
![Code Style](https://img.shields.io/badge/code%20style-ruff-000000.svg)

## 📋 Features

- **YouTube & SoundCloud Search**: Search for videos/tracks using `scrapetube` (YouTube, no API key) or `soundcloud-v2` (SoundCloud)
- **Smart Result Filtering**: Optionally filter results to ensure query appears in title or channel name (`--enable_filter`)
- **High-Quality Audio Download**: Extract audio in M4A format at 256 kbps quality using `yt-dlp` + FFmpeg
- **Browser Cookie Support**: Pass cookies from Chrome/Firefox/Edge for age-restricted content (`--cookies`)
- **Configurable Download Path**: Set and save your preferred download directory persistently in `config.json`
- **Terminal Image Previews**: Show thumbnail previews in search results when `term-image` is installed
- **User-Friendly Interface**: Colorful terminal output with intuitive command system powered by `clite`
- **Random User Agents**: Avoid detection by rotating user agents via `fake-useragent`
- **Comprehensive Error Handling**: Graceful handling of network errors, timeouts, and user interruptions
- **Formatted Search Results**: View titles, channels, dates, view counts (YouTube), durations, and URLs with tree structure

## 🚀 Installation

### Prerequisites

- **Python 3.6 or higher** - Check with `python --version`
- **FFmpeg** - Required for audio extraction (must be installed system-wide)

### Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS (with Homebrew):**
```bash
brew install ffmpeg
```

**Windows:**
1. Download from [FFmpeg official website](https://ffmpeg.org/download.html)
2. Extract the archive
3. Add the `bin` folder to your system PATH
4. Verify with `ffmpeg -version` in Command Prompt

### Install FM-dlp

1. Clone the repository:
```bash
git clone https://github.com/Fkernel653/fm-dlp.git
cd fm-dlp
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

### Requirements

The `requirements.txt` file includes:
```
fake-useragent
soundcloud-v2
term-image
scrapetube
yt-dlp
clite
```

## 🔧 Configuration

### Download Path Configuration

Set your default download directory using the `config` command:
```bash
python fm-dlp.py config /path/to/your/music/folder
```

The path is saved in `config.json` in the project root directory for future sessions. To view the current configuration:
```bash
python fm-dlp.py config
```

## 📖 Usage

Run the program with any of the following commands:

```bash
python fm-dlp.py <command> [arguments]
```

### Available Commands

#### Search for Videos/Tracks
```bash
# YouTube search (default)
python fm-dlp.py search "your query here" --limit=10

# SoundCloud search
python fm-dlp.py search "your query here" --variable=soundcloud --limit=5

# With result filtering (ensures query appears in title or channel)
python fm-dlp.py search "tokyona" --enable_filter=true --limit=5
```

**Parameters:**
- `query` (required) - Search term
- `--limit=<n>` - Maximum results (default: 10)
- `--enable_filter=<bool>` - Filter results by title/channel relevance (default: false)
- `--variable=<platform>` - Platform: `youtube` or `soundcloud` (default: youtube)

**Examples:**
```bash
python fm-dlp.py search "Sewerslvt" --limit=5
python fm-dlp.py search "breakcore" --variable=soundcloud --limit=3
python fm-dlp.py search "ambient" --enable_filter=true
```

Each result displays:
- Thumbnail preview (if `term-image` is installed)
- Result number (bold + cyan)
- Title (bold)
- Channel/artist name (with tree lines)
- Metadata (date, views/duration)
- URL (red)
- Visual tree structure with `├─` and `└─` characters

#### Download Audio
```bash
# Standard download
python fm-dlp.py download "youtube_url"

# With browser cookies (for age-restricted content)
python fm-dlp.py download "youtube_url" --cookies=chrome
```

**Parameters:**
- `url` (required) - YouTube video URL
- `--cookies=<browser>` - Browser name: `chrome`, `firefox`, `edge`, etc. (optional)

**Examples:**
```bash
python fm-dlp.py download "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
python fm-dlp.py download "https://youtu.be/VIDEO_ID" --cookies=firefox
```

Downloads will be saved to your configured directory as M4A files with 256 kbps AAC quality.

**Note:** The download path must be configured first using the `config` command, and FFmpeg must be installed.

#### Configure Download Path
```bash
# Set a new download path
python fm-dlp.py config "/absolute/path/to/download/folder"

# View current configuration
python fm-dlp.py config
```

#### Get Help
```bash
python fm-dlp.py help
```

## 🎨 Terminal Color Scheme

The program uses consistent ANSI color codes from `modules/colors.py`:

| Color | ANSI Code | Usage |
|-------|-----------|-------|
| 🔴 Red | `\033[01;31m` | Errors, warnings, video URLs |
| 🟢 Green | `\033[01;32m` | Success messages, confirmations |
| 🔵 Blue | `\033[01;34m` | Informational messages |
| 🟣 Magenta | `\033[01;35m` | Alternative highlight (help footer) |
| 🟡 Yellow | `\033[01;33m` | Command names in help menu |
| 🔷 Cyan | `\033[01;36m` | Result numbering, section headers, help title |
| ⚪ Gray | `\033[01;90m` | Tree lines (`├─`, `└─`, `─`), metadata labels, help descriptions |
| **Bold** | `\033[01;1m` | Emphasis, titles, important text |
| *Italic* | `\033[01;3m` | (Reserved for future use) |

## 🛠️ Technical Architecture

### Module Structure

```
fm-dlp/
├── fm-dlp.py              # Main CLI entry point (using clite)
├── config.json            # Persistent configuration (auto-generated)
├── requirements.txt       # Python dependencies
├── README.md              # This documentation
└── modules/
    ├── search.py          # YouTube + SoundCloud search (asynchronous)
    ├── download.py        # Audio download with yt-dlp + FFmpeg
    ├── configer.py        # Configuration management (JSON-based)
    ├── help.py            # Help menu text generation (colorized)
    └── colors.py          # ANSI color constants
```

### Component Details

#### `fm-dlp.py`
- Main CLI entry point using the `clite` framework
- Defines commands: `search`, `download`, `config`, `help`
- Uses type hints for automatic argument parsing and validation
- Delegates each command to its corresponding module function
- Handles async search operations for both YouTube and SoundCloud

#### `modules/search.py`
- **YouTube**: Uses `scrapetube.get_search()` to fetch results (no API key required!)
- **SoundCloud**: Uses `soundcloud.SoundCloud` API wrapper
- Asynchronous execution with configurable timeouts (10s for YouTube, 30s for SoundCloud)
- Optional result filtering (`enable_filter`) to ensure query relevance
- Terminal image previews via `term-image`
- Returns formatted, color-coded output via async generator
- Comprehensive error handling with traceback on unexpected failures

#### `modules/download.py`
- Uses `yt-dlp.YoutubeDL` for robust video downloading
- Reads download path from `config.json` in the parent directory
- Extracts best available audio stream via FFmpeg
- Converts to M4A format with 256 kbps AAC
- Implements random User-Agent rotation via `fake-useragent.UserAgent()`
- Browser cookie support for age-restricted content
- Handles `DownloadError`, `ExtractorError`, and `KeyboardInterrupt`
- Validates config file existence and JSON integrity

#### `modules/configer.py`
- Manages JSON-based configuration at `../config.json` (project root)
- Validates path existence on filesystem
- Acts as both getter (when `path` is falsy) and setter (when `path` is provided)
- Provides clear error messages for corrupted JSON or missing configs

#### `modules/help.py`
- Provides `message()` function returning colorized help menu
- Uses ANSI color constants for improved readability
- Displays commands, arguments, examples, and requirements

#### `modules/colors.py`
- Defines ANSI color codes for consistent terminal styling
- Includes: `RESET`, `BOLD`, `ITALIC`, `RED`, `GREEN`, `YELLOW`, `BLUE`, `MAGENTA`, `CYAN`, `GRAY`
- Used across all modules for uniform output formatting

### Audio Specifications

- **Format**: M4A (MPEG-4 Audio in MP4 container)
- **Codec**: AAC (Advanced Audio Coding)
- **Bitrate**: 256 kbps (high quality/size balance)
- **Source**: Best available audio stream from YouTube (`bestaudio/best`)

### Search Features

- **YouTube**: No API key required, uses `scrapetube` scraping
- **SoundCloud**: Uses official `soundcloud-v2` package
- **Result Filtering**: Optional filtering by title OR channel name relevance
- **Video/Track Information**: Title, channel/artist, date, views (YouTube), duration, URL
- **Terminal Images**: Thumbnail previews when `term-image` is installed
- **Async/Await**: Non-blocking search with configurable timeouts

## 💻 Code Quality

This project follows modern Python best practices:

- **Formatted with [Ruff](https://github.com/astral-sh/ruff)** - An extremely fast Python linter and formatter
- **Type Hints** - All functions include type annotations for better IDE support
- **Docstrings** - Google-style docstrings for all public functions and classes
- **Error Handling** - Comprehensive try/except blocks with user-friendly messages
- **Consistent Imports** - Organized imports (standard library → third-party → local modules)

To format the code yourself:
```bash
# Install ruff
pip install ruff

# Run formatter
ruff format .

# Run linter
ruff check .
```

## ⚠️ Important Considerations

### System Requirements
- **Internet Connection**: Required for both search and download functions
- **FFmpeg**: Must be installed and accessible in system PATH
- **Disk Space**: Sufficient space for downloaded audio files (approx. 3-5 MB per minute)
- **Write Permissions**: Download directory must be writable

### Dependencies
- **fake-useragent** - Random browser user agents
- **soundcloud-v2** - SoundCloud API wrapper
- **term-image** - Terminal image previews (optional)
- **scrapetube** - YouTube search scraping (no API key)
- **yt-dlp** - YouTube downloading and audio extraction
- **clite** - Simple CLI framework

### Legal and Ethical Considerations
- **Respect Copyright**: Only download content you have rights to
- **Terms of Service**: Comply with YouTube's and SoundCloud's Terms of Service
- **Personal Use**: This tool is intended for personal, educational use
- **Rate Limiting**: Avoid excessive requests that could be considered abuse

## 🐛 Troubleshooting Guide

### Common Issues and Solutions

#### 1. "No videos matching 'query' after filtering"
**Possible causes:**
- Search query doesn't appear in any video titles or channel names
- Network connectivity issues
- YouTube may be blocking scrapetube requests

**Solutions:**
- Try a different search query (use fewer words or broader terms)
- Disable filtering: `--enable_filter=false`
- Check your internet connection
- Wait a few minutes and try again

#### 2. Download Fails
**Possible causes:**
- FFmpeg not installed
- Download path doesn't exist or isn't writable
- Video is private, age-restricted, or deleted
- URL format is incorrect
- Config file missing or corrupted

**Solutions:**
- Install FFmpeg and verify with `ffmpeg -version`
- For age-restricted videos, try: `--cookies=chrome`
- Check if download path exists: `python fm-dlp.py config`
- Ensure URL is complete and correct
- Reconfigure download path: `python fm-dlp.py config /valid/path`

#### 3. Config File Errors
**Possible causes:**
- Corrupted JSON in `config.json`
- Manual editing of config file with syntax errors
- Permission issues

**Solutions:**
- Delete `config.json` and reconfigure
- Check file permissions (must be readable and writable)

#### 4. SoundCloud Search Timeout
**Possible causes:**
- Slow network connection
- SoundCloud API rate limiting
- Large limit value

**Solutions:**
- Reduce `--limit` parameter (e.g., `--limit=3`)
- Check your internet connection
- Try again later

#### 5. Import Errors
**Possible causes:**
- Missing dependencies
- Incorrect Python path

**Solutions:**
- Run `pip install -r requirements.txt`
- Ensure you're running from the project root directory

## 🤝 Contributing

Contributions are welcome and appreciated!

### Ways to Contribute
- **Report Bugs**: Open an issue with detailed description and error logs
- **Suggest Features**: Share ideas for improvements
- **Submit Pull Requests**: Fix bugs or add features
- **Improve Documentation**: Enhance README or code comments

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run `ruff format .` to format code
5. Run `ruff check .` to lint
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Coding Standards
- Follow PEP 8 style guide (enforced by Ruff)
- Add docstrings for all functions (Google-style)
- Include type hints for all parameters and return values
- Use existing color constants from `modules/colors.py`

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Fkernel653**
- GitHub: [@Fkernel653](https://github.com/Fkernel653)

## 🙏 Acknowledgments

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - Feature-rich downloading library
- **[scrapetube](https://github.com/dermasmid/scrapetube)** - YouTube search without API keys
- **[soundcloud-v2](https://github.com/7x11x13/soundcloud-v2)** - SoundCloud API wrapper
- **[clite](https://pypi.org/project/clite/)** - Simple CLI framework
- **[term-image](https://github.com/AnonymouX47/term-image)** - Terminal image rendering
- **[Ruff](https://github.com/astral-sh/ruff)** - Fast Python linter and formatter

## 📊 Version History

**v1.0.0** (Current)
- YouTube search with scrapetube (no API key!)
- SoundCloud search with soundcloud-v2
- Audio download with yt-dlp + FFmpeg (256 kbps M4A)
- Browser cookie support for age-restricted content
- Terminal thumbnail previews
- Configuration management via JSON
- Color-coded terminal output
- Async/await search with configurable timeouts
- Code formatted with Ruff

**Planned Features**
- Playlist download support
- Multiple audio format options (MP3, OGG, FLAC)
- Download progress bar improvements
- Batch download from file
- Search result pagination

---

**Disclaimer**: This tool is for educational purposes only. Users are responsible for complying with YouTube's and SoundCloud's Terms of Service, copyright laws, and all applicable regulations.