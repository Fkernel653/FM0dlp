"""Entry point for the fm-dlp YouTube Music Downloader.

This module initializes the CLI interface using the 'clite' library and
defines the main commands: search, download, config, and help.
It serves as the main entry point for the application.
"""

from clite import Clite
from modules.searching import searching
from modules.downloader import download_audio
from modules.configer import configuring_path
from modules.helper import message


# Initialize the CLI application with metadata
# This creates the command-line interface with the specified name and description
fm_dlp = Clite(
    name="fm-dlp",
    description="A utility for searching and downloading music from YouTube, based on yt-dlp",
)


@fm_dlp.command()
def search(limit: int = None, query: str = None):
    """
    Search for videos on YouTube and display results in a formatted list.

    This command connects to the YouTube Data API, performs a search with the
    given query, and displays up to 50 results with titles, channels, dates, and URLs.

    Args:
        query (str): The search term(s). Defaults to "world" as a placeholder
                     when no query is provided.

    Returns:
        None: Results are printed directly to the console.
    """
    # Iterate through the generator from searching() and print each video info
    for video_info in searching(limit, query):
        print(video_info)


@fm_dlp.command()
def download(url: str = None):
    """
    Download audio from a YouTube video as a high-quality M4A file.

    This command extracts audio from the specified YouTube URL and saves it
    as an M4A file in the configured download directory.

    Args:
        url (str): The full YouTube URL (e.g., https://youtube.com/watch?v=...).
                  Defaults to "world" as a placeholder when no URL is provided.

    Returns:
        None: Download progress and status are printed to the console.
    """
    print(download_audio(url))


@fm_dlp.command()
def config(path: str = None):
    """
    Set or view the download directory path.

    Acts as a setter when a valid path is provided, saving it to config.json.
    Acts as a getter when called without arguments (or with placeholder value),
    displaying the current configuration.

    Args:
        path (str): The directory path where audio files should be saved.
                    If "world" (placeholder), it triggers the getter mode.

    Returns:
        None: Configuration status is printed to the console.
    """
    print(configuring_path(path))


@fm_dlp.command()
def help():
    """Display the help menu with usage instructions for all commands."""
    print(message())


if __name__ == "__main__":
    # Run the CLI application when this script is executed directly
    # This parses command-line arguments and dispatches to the appropriate function
    fm_dlp()