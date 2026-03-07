# FM0dlp - YouTube Audio Downloader

A powerful command-line tool for searching and downloading audio from YouTube videos. Built with Python, this tool combines the YouTube Data API for searching with yt-dlp for high-quality audio extraction.

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Features

- **YouTube Video Search**: Search for videos using the official YouTube Data API
- **High-Quality Audio Download**: Extract audio in M4A format at 192 kbps quality
- **Configurable Download Path**: Set and save your preferred download directory
- **User-Friendly Interface**: Colorful terminal output with intuitive menu system
- **Random User Agents**: Avoid detection by rotating user agents
- **Search Results Display**: View video titles, channels, upload dates, and URLs

## 🚀 Installation

### Prerequisites

- Python 3.6 or higher
- FFmpeg (required for audio extraction)

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
Download from [FFmpeg official website](https://ffmpeg.org/download.html) and add to PATH

### Install FM0dlp

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
yt-dlp
requests
readline
```

## 🔧 Configuration

### YouTube API Key

This tool requires a YouTube Data API key to function:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the YouTube Data API v3
4. Create credentials (API key)
5. Copy the API key and add it to the `api_key` variable in the `FM0dlp` class

```python
class FM0dlp:
    def __init__(self):
        self.api_key = "YOUR_API_KEY_HERE"  # Add your API key here
        self.api = "https://www.googleapis.com/youtube/v3/search"
        self.ua = UserAgent()
```

### Download Path

Set your default download directory:
- Use option 3 in the menu to configure the download path
- The path is saved in `config.json` for future sessions

## 📖 Usage

Run the program:
```bash
python fm0dlp.py
```

### Main Menu

```
1: Search     - Search for videos on YouTube
2: Download   - Download audio from a YouTube URL  
3: Boot path configuration - Set or view download directory
```

### Search Videos

1. Select option 1
2. Enter your search query
3. View results with numbered entries including:
   - Video title
   - Channel name
   - Upload date
   - Direct YouTube URL

### Download Audio

1. Select option 2
2. Paste the YouTube video URL
3. Audio will be downloaded to your configured path as M4A (192 kbps)

### Configure Download Path

1. Select option 3
2. Enter your desired download directory (e.g., `/home/user/Music` or `C:\Users\User\Music`)
3. Path is saved and will be used for future downloads

## 🎨 Terminal Colors

The program uses ANSI color codes for better readability:
- 🔴 Red: Errors and important messages
- 🟢 Green: Success messages
- 🔵 Cyan: Titles and headings
- 🟣 Magenta: Channel information
- ⚪ White: Numbers and URLs

## 🛠️ Technical Details

### Dependencies

- **yt-dlp**: Advanced YouTube downloading with format selection
- **requests**: HTTP requests to YouTube API
- **fake-useragent**: Random user agent generation
- **readline**: Enhanced command line input
- **json**: Configuration file handling

### Audio Quality

- **Format**: M4A (AAC audio)
- **Bitrate**: 192 kbps
- **Source**: Best available audio stream

### API Features

- **Max Results**: Up to 50 videos per search
- **Video Duration**: Filtered to medium-length videos
- **Content Type**: Videos only (no channels or playlists)

## 📁 Project Structure

```
FM0dlp/
├── fm0dlp.py          # Main program file
├── config.json        # Configuration file (auto-generated)
├── requirements.txt   # Python dependencies
└── README.md         # This documentation
```

## ⚠️ Important Notes

- **API Key Required**: The program won't work without a valid YouTube Data API key
- **Internet Connection**: Required for both search and download functions
- **FFmpeg**: Must be installed for audio extraction to work
- **Rate Limits**: YouTube API has daily quota limits
- **Respect Copyright**: Only download content you have rights to

## 🐛 Troubleshooting

### Common Issues

1. **"No videos found"**
   - Check your API key
   - Verify internet connection
   - Try a different search query

2. **Download fails**
   - Ensure FFmpeg is installed
   - Check if download path exists and is writable
   - URL might be invalid or video unavailable

3. **Config file errors**
   - Delete config.json and reconfigure
   - Check file permissions

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Fkernel653**
- GitHub: [@Fkernel653](https://github.com/Fkernel653)

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for the excellent downloading library
- [Google YouTube Data API](https://developers.google.com/youtube/v3) for search functionality
- All contributors and users of this tool

## ⭐ Support

If you find this tool useful, please consider:
- Starring the repository on GitHub
- Sharing it with others
- Contributing to the project

---

**Disclaimer**: This tool is for educational purposes. Users are responsible for complying with YouTube's Terms of Service and copyright laws.
