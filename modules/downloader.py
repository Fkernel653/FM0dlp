"""Audio downloader module using yt-dlp.

Handles downloading audio from YouTube videos and extracting
the audio track to high-quality M4A format. Requires FFmpeg
to be installed on the system for audio extraction.
"""

from pathlib import (
    Path,
)  # Object-oriented filesystem paths that work on all operating systems
from fake_useragent import (
    UserAgent,
)  # Library for generating random browser User-Agent strings to prevent blocking
from yt_dlp import (
    YoutubeDL,
)  # Powerful YouTube downloading library with format selection and extraction
from yt_dlp.utils import DownloadError, ExtractorError, GeoRestrictedError
from modules.colors import RESET, RED, GREEN
import json


def download_audio(url: str) -> None:
    """
    Extract audio track from YouTube video and save as high-quality M4A file.

    Args:
        url (str): Complete YouTube URL (youtube.com/watch?v=... or youtu.be/...).

    Returns:
        None: The function prints status messages and exits on errors.

    Note:
        Requires FFmpeg to be installed on the system for audio extraction.
        The download path must be configured first using the config command.
        Audio is downloaded at 256 kbps bitrate in M4A format (AAC codec).
    """
    # Locate config file in the parent directory of this script
    # This ensures config is found regardless of where the script is executed from
    parent_folder = Path(__file__).parent
    config_file = Path(parent_folder).parent / "config.json"

    # Verify configuration exists before attempting download
    if not config_file.exists():
        print(
            f"{RED}\nConfig file not found! Please set download path first using 'config <path>'.{RESET}\n"
        )
        return exit(1)  # Exit with error code

    # Read and parse existing configuration
    with open(config_file, "r", encoding="utf-8") as f:
        data = json.load(f)  # Convert JSON to Python dict
        # Retrieve user's download directory using the correct key
        saved_path = data.get("path")

        # Generate a random User-Agent to mimic a real browser and avoid blocking
        ua = UserAgent()

        # yt-dlp configuration dictionary with all options
        opts = {
            "user_agent": ua.random,  # Rotate fingerprints to avoid rate limiting
            "format": "bestaudio/best",  # Select highest quality audio stream available
            "outtmpl": f"{saved_path}/%(title)s.%(ext)s",  # Naming pattern: title.extension
            "postprocessors": [
                {  # Array of post-processing steps
                    "key": "FFmpegExtractAudio",  # Built-in FFmpeg audio extraction
                    "preferredcodec": "m4a",  # Target format (AAC in MP4 container)
                    "preferredquality": "256",  # Bitrate in kbps (balance quality/size)
                }
            ],
            "quiet": False,  # Show detailed progress in terminal
        }

        try:
            # Context manager ensures proper cleanup of resources
            with YoutubeDL(opts) as ydl:
                return ydl.download(
                    [url]
                )  # Pass URL in list (supports multiple videos, though we only use one)

        except DownloadError:
            # General download failure (network issues, unavailable video, etc.)
            print(
                f"{RED}\nDownload error! The video may be unavailable or restricted.{RESET}\n"
            )
            return exit(1)

        except ExtractorError:
            # Error extracting video information from YouTube
            print(
                f"{RED}\nExtraction error! Unable to retrieve video information.{RESET}\n"
            )
            return exit(1)

        except GeoRestrictedError:
            # Video is blocked in the current country/region
            print(
                f"{RED}\nGeolocation error: This video is not available in your region. "
                f"Please try a different VPN server or proxy!\n{RESET}"
            )
            return exit(1)

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully during download
            print(f"{GREEN}\n\tGoodbye!\n{RESET}")
            return exit(0)
