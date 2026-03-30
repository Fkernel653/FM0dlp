# FM-dlp - YouTube Music Downloader

A powerful command-line tool for searching and downloading audio from YouTube videos. Built with Python, this tool uses `scrapetube` for searching (no API key required!) and `yt-dlp` for high-quality audio extraction.

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-lightgrey)

## 📋 Features

- **YouTube Video Search**: Search for videos using `scrapetube` (no API key needed!)
- **Smart Result Filtering**: Automatically filters results to ensure query appears in title or channel name
- **High-Quality Audio Download**: Extract audio in M4A format at 256 kbpяs quality using `yt-dlp` + FFmpeg
- **Configurable Download Path**: Set and save your preferred download directory persistently in `config.json`
- **User-Friendly Interface**: Colorful terminal output with intuitive command system powered by `clite`
- **Random User Agents**: Avoid detection by rotating user agents via `fake-useragent`
- **Comprehensive Error Handling**: Graceful handling of network errors, connection issues, and user interruptions
- **Search Results Display**: View video titles, channels, upload dates, view counts, durations, and direct YouTube URLs

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

#### Search for Videos
```bash
python fm-dlp.py search "your query here" --limit=10
```
Example:
```bash
python fm-dlp.py search "Sewerslvt" --limit=5
```

The `--limit` parameter is optional (defaults to 10). Results are filtered to ensure your search query appears in either the video title or channel name.

Each result displays:
- Video title (bold + cyan)
- Channel name (gray tree lines + white)
- Upload date, view count, and duration (gray tree lines + white)
- YouTube URL (red)
- Visual tree structure with `├─` and `└─` characters

#### Download Audio
```bash
python fm-dlp.py download "youtube_url"
```
Example:
```bash
python fm-dlp.py download "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
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
| 🔴 Red | `\033[01;31m` | Errors, warnings, and video URLs |
| 🟢 Green | `\033[01;32m` | Success messages, goodbye messages |
| 🔵 Blue | `\033[01;34m` | (Reserved for future use) |
| 🟣 Magenta | `\033[01;35m` | (Reserved for future use) |
| 🟡 Yellow | `\033[01;33m` | (Reserved for future use) |
| 🔷 Cyan | `\033[01;36m` | Video titles and headings |
| ⚪ Gray | `\033[01;90m` | Tree lines (`├─`, `└─`, `─`) and decorative elements |
| **Bold White** | `\033[01;1m` | Numbers, emphasized text, and video titles |
| *Italic* | `\033[01;3m` | (Reserved for future use) |

**Note:** The current implementation uses `GRAY` for tree lines, `CYAN` for titles, `RED` for URLs, and `BOLD` + `CYAN` for numbered list items. Other colors are defined but not yet used.

## 🛠️ Technical Architecture

### Module Structure

```
fm-dlp/
├── fm-dlp.py              # Main CLI entry point (using clite)
├── config.json            # Persistent configuration (auto-generated)
├── requirements.txt       # Python dependencies
├── README.md              # This documentation
└── modules/
    ├── searching.py       # YouTube search with scrapetube + result filtering
    ├── downloader.py      # Audio download with yt-dlp + FFmpeg
    ├── configer.py        # Configuration management (JSON-based)
    ├── helper.py          # Help menu text generation
    └── colors.py          # ANSI color constants (RESET, BOLD, ITALIC, RED, GREEN, etc.)
```

### Component Details

#### `fm-dlp.py`
- Main CLI entry point using the `clite` framework
- Defines commands: `search`, `download`, `config`, `help`
- Uses type hints for automatic argument parsing and validation
- Delegates each command to its corresponding module function

#### `modules/searching.py`
- Uses `scrapetube.get_search()` to fetch YouTube results (no API key required!)
- Filters results to ensure query relevance in title OR channel name
- Returns formatted, color-coded output via generator
- Handles network errors (`ConnectionAbortedError`, `ConnectionError`, etc.) and `KeyboardInterrupt` gracefully
- Exits with code 1 if no videos match after filtering

#### `modules/downloader.py`
- Uses `yt-dlp.YoutubeDL` for robust video downloading
- Reads download path from `config.json` in the parent directory
- Extracts best available audio stream via FFmpeg
- Converts to M4A format with 256 kbps AAC
- Implements random User-Agent rotation via `fake-useragent.UserAgent()`
- Handles `DownloadError`, `ExtractorError`, and `KeyboardInterrupt`
- Validates config file existence and JSON integrity

#### `modules/configer.py`
- Manages JSON-based configuration at `../config.json` (project root)
- Validates path existence on filesystem
- Acts as both getter (when `path` is falsy) and setter (when `path` is provided)
- Provides clear error messages for corrupted JSON or missing configs
- Exits with code 1 on validation failures

#### `modules/helper.py`
- Provides `message()` function returning help menu text with command descriptions
- Used by the `help` command in the main CLI

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

- **No API Key Required**: Uses `scrapetube` to scrape YouTube search results
- **Result Filtering**: Automatic filtering by title OR channel name relevance
- **Video Information**: Title, channel name, upload date, view count, duration, YouTube URL
- **Graceful Error Handling**: Network errors, connection issues, keyboard interrupts
- **Generator-based Output**: Yields results one by one for memory efficiency

## ⚠️ Important Considerations

### System Requirements
- **Internet Connection**: Required for both search and download functions
- **FFmpeg**: Must be installed and accessible in system PATH
- **Disk Space**: Sufficient space for downloaded audio files (approx. 3-5 MB per minute)
- **Write Permissions**: Download directory must be writable

### Dependencies
- **scrapetube** (no version specified) - Scrapes YouTube search results (no API key needed)
- **yt-dlp** (no version specified) - Downloads and extracts audio from YouTube videos
- **fake-useragent** (no version specified) - Provides random browser user agents
- **clite** (no version specified) - Simple CLI framework for command parsing

### Legal and Ethical Considerations
- **Respect Copyright**: Only download content you have rights to
- **Terms of Service**: Comply with YouTube's Terms of Service
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
- Check your internet connection
- Wait a few minutes and try again (YouTube may temporarily block aggressive scraping)

#### 2. Download Fails
**Possible causes:**
- FFmpeg not installed
- Download path doesn't exist or isn't writable
- Video is private, age-restricted, or deleted
- URL format is incorrect
- Config file missing or corrupted

**Solutions:**
- Install FFmpeg and verify with `ffmpeg -version`
- Check if download path exists: `python fm-dlp.py config`
- Ensure URL is complete and correct (e.g., `https://youtu.be/VIDEO_ID`)
- Reconfigure download path: `python fm-dlp.py config /valid/path`
- Delete `config.json` and reconfigure

#### 3. Config File Errors
**Possible causes:**
- Corrupted JSON in `config.json`
- Manual editing of config file with syntax errors
- Permission issues

**Solutions:**
- Delete `config.json` and reconfigure: `python fm-dlp.py config /new/path`
- Check file permissions (must be readable and writable)
- Ensure config.json contains valid JSON with a `"path"` key

#### 4. Connection Errors
**Possible causes:**
- Network issues
- YouTube blocking requests
- Proxy/firewall restrictions

**Solutions:**
- Check internet connection with `ping youtube.com`
- Try using a VPN
- Wait and retry (rate limiting may be temporary)
- The error message will show the specific connection exception

#### 5. Import Errors
**Possible causes:**
- Missing dependencies
- Incorrect Python path

**Solutions:**
- Run `pip install -r requirements.txt`
- Ensure you're running from the project root directory
- Check that the `modules/` folder contains all `.py` files

## 🤝 Contributing

Contributions are welcome and appreciated! Here's how you can help:

### Ways to Contribute
- **Report Bugs**: Open an issue with detailed description and error logs
- **Suggest Features**: Share ideas for improvements
- **Submit Pull Requests**: Fix bugs or add features
- **Improve Documentation**: Enhance README or code comments
- **Share Feedback**: Tell us about your experience

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (if applicable)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Coding Standards
- Follow PEP 8 style guide
- Add docstrings for all functions (Google-style as shown in existing code)
- Include comments for complex logic
- Update documentation as needed
- Use existing color constants from `modules/colors.py`

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

**MIT License Summary:**
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ❌ Liability
- ❌ Warranty

## 👨‍💻 Author

**Fkernel653**
- GitHub: [@Fkernel653](https://github.com/Fkernel653)
- Project Repository: [fm-dlp](https://github.com/Fkernel653/fm-dlp)

## 🙏 Acknowledgments

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - For the excellent, feature-rich downloading library
- **[scrapetube](https://github.com/dermasmid/scrapetube)** - For YouTube search without API keys
- **[clite](https://pypi.org/project/clite/)** - For the simple CLI framework
- **[fake-useragent](https://github.com/hellysmile/fake-useragent)** - For User-Agent rotation
- All contributors and users of this tool

## 📊 Version History

**v1.0.0** (Current)
- Initial release
- YouTube search with scrapetube (no API key!)
- Audio download with yt-dlp + FFmpeg (256 kbps M4A)
- Configuration management via JSON
- Color-coded terminal output with tree structure
- Command-line interface with clite

**Planned Features**
- Playlist download support
- Search result pagination
- Download progress bar improvements
- Multiple audio format options (MP3, OGG, FLAC)
- Batch download from file
- Search result caching

## ⭐ Support the Project

If you find this tool useful, please consider:
- **Starring** the repository on GitHub
- **Forking** to contribute improvements
- **Sharing** with others who might find it useful
- **Reporting** issues you encounter

---

**Disclaimer**: This tool is for educational purposes only. Users are responsible for complying with YouTube's Terms of Service, copyright laws, and all applicable regulations. The developers assume no liability for misuse of this software.