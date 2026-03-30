"""
Audio downloader module using yt-dlp.

This module handles downloading audio from YouTube videos and extracting
the audio track to high-quality M4A format. It reads the download path
from a JSON configuration file and uses yt-dlp with FFmpeg for audio processing.

Requirements:
    - FFmpeg must be installed on the system and available in PATH
    - A valid configuration file must exist with a 'path' key pointing
      to an existing directory for downloads
"""

from pathlib import Path
from fake_useragent import UserAgent
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError, ExtractorError
from modules.colors import RESET, RED, GREEN
import json


def download_audio(url: str) -> None:
    """
    Extract audio track from YouTube video and save as high-quality M4A file.

    This function performs the following steps:
        1. Locates and validates the configuration file (config.json)
        2. Reads the saved download directory path from the config
        3. Generates a random User-Agent to avoid rate limiting
        4. Configures yt-dlp with optimal audio extraction settings
        5. Downloads and extracts audio using FFmpeg

    Args:
        url (str): Complete YouTube URL. Accepts various formats:
                   - https://youtube.com/watch?v=VIDEO_ID
                   - https://youtu.be/VIDEO_ID
                   - https://www.youtube.com/watch?v=VIDEO_ID

    Returns:
        None: The function prints status messages to the console and exits
              with appropriate error codes on failure. Does not return any value.

    Note:
        - Requires FFmpeg to be installed on the system for audio extraction.
        - The download path must be configured first using the config command.
        - Audio is downloaded at 256 kbps bitrate in M4A format (AAC codec).
        - The configuration file is expected at ../config.json relative to
          this module's location (project root directory).
        - This function terminates the process with sys.exit() codes:
          0 on success or user cancellation, 1 on configuration or download errors.

    Raises:
        SystemExit: Exits with code 1 on configuration or download errors,
                    code 0 on successful completion or keyboard interrupt.
    """
    # Locate config file in the parent directory of this script's parent
    # Path structure: project_root/config.json
    # This module is at: project_root/modules/downloader.py
    parent_folder = Path(__file__).parent
    config_file = Path(parent_folder).parent / "config.json"

    # Verify configuration exists before attempting download
    if not config_file.exists():
        print(
            f"{RED}\nConfig file not found! Please set download path first using 'config <path>'.{RESET}\n"
        )
        return exit(1)

    # Read and parse existing configuration
    with open(config_file, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            saved_path = data.get("path")

            # Validate that the saved path exists on the filesystem
            if not saved_path or not Path(saved_path).exists():
                print(
                    f"{RED}\nDownload path '{saved_path}' does not exist or is invalid. "
                    f"Please reconfigure with 'config <path>'.{RESET}\n"
                )
                return exit(1)

        except json.JSONDecodeError:
            print(
                f"{RED}\nConfig file is corrupted! Please reconfigure with 'config <path>'.{RESET}\n"
            )
            return exit(1)

    # Generate a random User-Agent string to mimic a real browser
    # This helps prevent YouTube from blocking or rate-limiting requests
    ua = UserAgent()

    # yt-dlp configuration dictionary with all options
    opts = {
        "user_agent": ua.random,  # Rotate fingerprints to avoid detection
        "format": "bestaudio/best",  # Select highest quality audio stream available
        "outtmpl": f"{saved_path}/%(title)s.%(ext)s",  # Save pattern: video_title.extension
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",  # Use FFmpeg for audio extraction
                "preferredcodec": "m4a",  # Output format (AAC in MP4 container)
                "preferredquality": "256",  # Bitrate in kbps (good quality/size balance)
            }
        ],
        "quiet": False,  # Show detailed progress in terminal
        "no_warnings": False,  # Display warnings for troubleshooting
    }

    try:
        # Context manager ensures proper cleanup of resources after download
        with YoutubeDL(opts) as ydl:
            # Download audio from the provided URL
            # ydl.download() expects a list, even for single videos
            ydl.download([url])
            print(f"{GREEN}\nDownload completed successfully!{RESET}\n")
            return exit(0)

    except DownloadError:
        # General download failure (network issues, unavailable video, age restriction, etc.)
        print(
            f"{RED}\nDownload error! The video may be unavailable, private, or restricted.{RESET}\n"
        )
        return exit(1)

    except ExtractorError:
        # Error extracting video information from YouTube's servers
        print(
            f"{RED}\nExtraction error! Unable to retrieve video information. "
            f"The video ID may be invalid or YouTube's API may have changed.{RESET}\n"
        )
        return exit(1)

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully during download process
        print(f"{GREEN}\nDownload cancelled. Goodbye!\n{RESET}")
        return exit(0)
