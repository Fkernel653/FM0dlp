# FM-dlp - YouTube Audio Downloader

A powerful command-line tool for searching and downloading audio from YouTube videos. Built with Python, this tool combines the YouTube Data API for searching with yt-dlp for high-quality audio extraction.

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-lightgrey)

## 📋 Features

- **YouTube Video Search**: Search for videos using the official YouTube Data API v3
- **Smart Result Filtering**: Automatically filters results to ensure query appears in title or channel name
- **High-Quality Audio Download**: Extract audio in M4A format at 256 kbps quality
- **Configurable Download Path**: Set and save your preferred download directory persistently
- **User-Friendly Interface**: Colorful terminal output with intuitive command system
- **Random User Agents**: Avoid detection by rotating user agents for each request
- **Comprehensive Error Handling**: Graceful handling of network errors, API limits, and user interruptions
- **Search Results Display**: View video titles, channels, upload dates, and direct URLs

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
git clone https://github.com/Fkernel653/FM0dlp.git
cd FM0dlp
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

### Requirements.txt

Create a `requirements.txt` file with:
```
fake-useragent
python-dotenv
yt-dlp
requests
clite
```

## 🔧 Configuration

### YouTube API Key

This tool requires a YouTube Data API key to function. **Note:** The API key in the code is a placeholder and must be replaced with your own:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **YouTube Data API v3**
4. Go to "Credentials" and create an API key
5. Copy the API key and replace it in `modules/searching.py`:
   ```python
   params = {
       # ... other parameters ...
       "key": os.getenv("YOUTUBE_DATA_API_KEY"),  # 
   }
   ```

### Download Path Configuration

Set your default download directory using the config command:
```bash
python fm-dlp.py config /path/to/your/music/folder
```

The path is saved in `config.json` for future sessions. To view the current configuration:
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
python fm-dlp.py search "your query here"
```
Example:
```bash
python fm-dlp.py search "Sewerslvt"
```
This will display up to 50 results with:
- Video title (in cyan)
- Channel name (in magenta)
- Upload date (in blue)
- Direct YouTube URL (in red)

#### Download Audio
```bash
python fm-dlp.py download "youtube_url"
```
Example:
```bash
python fm-dlp.py download "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```
Downloads will be saved to your configured directory as M4A files with 256 kbps quality.

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

The program uses consistent ANSI color codes for better readability:

| Color | Usage |
|-------|-------|
| 🔴 **Red** | Errors, warnings, and video URLs |
| 🟢 **Green** | Success messages and goodbye |
| 🔵 **Blue** | Upload dates and information |
| 🟣 **Magenta** | Channel names and metadata |
| 🔷 **Cyan** | Video titles and headings |
| **Bold White** | Numbers and emphasized text |

## 🛠️ Technical Architecture

### Module Structure

```
fm-dlp/
├── fm-dlp.py              # Main CLI entry point (using clite)
├── config.json            # Persistent configuration (auto-generated)
├── key.env                # A file containing an API key for the searching.py (Edit it)
├── requirements.txt       # Python dependencies
├── README.md              # This documentation
└── modules/
    ├── searching.py       # YouTube API search functionality
    ├── downloader.py      # Audio download with yt-dlp
    ├── configer.py        # Configuration management
    ├── helper.py          # Help menu display
    └── colors.py          # ANSI color constants
```

### Component Details

#### searching.py
- Interfaces with YouTube Data API v3
- Filters results to ensure query relevance
- Returns formatted, color-coded output
- Handles API errors and rate limiting

#### downloader.py
- Uses yt-dlp for robust video downloading
- Extracts best available audio stream
- Converts to M4A format with FFmpeg
- Implements random User-Agent rotation
- Handles georestrictions and extraction errors

#### configer.py
- Manages JSON-based configuration
- Validates path existence
- Acts as both getter and setter
- Provides clear error messages

### Audio Specifications

- **Format**: M4A (MPEG-4 Audio)
- **Codec**: AAC (Advanced Audio Coding)
- **Bitrate**: 256 kbps (high quality)
- **Source**: Best available audio stream from YouTube

### API Features

- **Max Results**: Up to 50 videos per search (configurable)
- **Video Duration**: Filtered to medium-length (4-20 minutes)
- **Content Type**: Videos only (excludes channels and playlists)
- **Response Format**: JSON with snippet and ID information

## ⚠️ Important Considerations

### API Key Requirements
- **Valid API Key Required**: The program won't work without a valid YouTube Data API key
- **Quota Limits**: YouTube API has daily quota limits (typically 10,000 units per day)
- **Each search costs**: Approximately 100 quota units

### System Requirements
- **Internet Connection**: Required for both search and download functions
- **FFmpeg**: Must be installed and accessible in system PATH
- **Disk Space**: Sufficient space for downloaded audio files
- **Write Permissions**: Download directory must be writable

### Legal and Ethical Considerations
- **Respect Copyright**: Only download content you have rights to
- **Terms of Service**: Comply with YouTube's Terms of Service
- **Personal Use**: This tool is intended for personal, educational use
- **Rate Limiting**: Avoid excessive requests that could be considered abuse

## 🐛 Troubleshooting Guide

### Common Issues and Solutions

#### 1. "No videos found" or Empty Results
**Possible causes:**
- Invalid API key
- Network connectivity issues
- No videos match your query
- API quota exceeded

**Solutions:**
- Verify your API key in `key.env`
- Check internet connection
- Try a different search query
- Wait for quota reset (24 hours) or get a new API key

#### 2. Download Fails
**Possible causes:**
- FFmpeg not installed
- Download path doesn't exist or isn't writable
- Video is private or age-restricted
- URL format is incorrect

**Solutions:**
- Install FFmpeg and verify with `ffmpeg -version`
- Check if download path exists: `python fm-dlp.py config`
- Ensure URL is complete and correct
- Try downloading with a different video

#### 3. Config File Errors
**Possible causes:**
- Corrupted JSON in config.json
- Manual editing of config file
- Permission issues

**Solutions:**
- Delete config.json and reconfigure: `python fm-dlp.py config /new/path`
- Check file permissions
- Ensure config.json is valid JSON

#### 4. API Key Errors (403 or 400)
**Possible causes:**
- Invalid API key
- YouTube Data API not enabled
- Billing not set up (for some projects)

**Solutions:**
- Regenerate API key in Google Cloud Console
- Enable YouTube Data API v3
- Check if billing is required for your quota

## 🤝 Contributing

Contributions are welcome and appreciated! Here's how you can help:

### Ways to Contribute
- **Report Bugs**: Open an issue with detailed description
- **Suggest Features**: Share ideas for improvements
- **Submit Pull Requests**: Fix bugs or add features
- **Improve Documentation**: Enhance README or code comments
- **Share Feedback**: Tell us about your experience

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests (if applicable)
5. Submit a pull request

### Coding Standards
- Follow PEP 8 style guide
- Add docstrings for all functions
- Include comments for complex logic
- Update documentation as needed

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
- Project Repository: [FM0dlp](https://github.com/Fkernel653/FM0dlp)

## 🙏 Acknowledgments

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - For the excellent, feature-rich downloading library
- **[Google YouTube Data API](https://developers.google.com/youtube/v3)** - For providing search functionality
- **[clite](https://pypi.org/project/clite/)** - For the simple CLI framework
- **[fake-useragent](https://github.com/hellysmile/fake-useragent)** - For User-Agent rotation
- All contributors and users of this tool

## 📊 Version History

**v1.0.0** (Current)
- Initial release
- YouTube search functionality
- Audio download with yt-dlp
- Configuration management
- Color-coded terminal output

**Planned Features**
- Playlist download support
- Search result pagination
- Download progress bar
- Multiple format options
- Batch download from file

## ⭐ Support the Project

If you find this tool useful, please consider:
- **Starring** the repository on GitHub
- **Forking** to contribute improvements
- **Sharing** with others who might find it useful
- **Reporting** issues you encounter
- **Donating** to support development (if options available)

---

**Disclaimer**: This tool is for educational purposes only. Users are responsible for complying with YouTube's Terms of Service, copyright laws, and all applicable regulations. The developers assume no liability for misuse of this software.