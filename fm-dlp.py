"""
Entry point for the fm-dlp YouTube Music Downloader.

This module initializes the CLI interface using the 'clite' library and
defines the main commands: search, download, config, and help. It serves
as the main entry point for the application and handles command-line
argument parsing and dispatch.

Architecture:
    - Commands are defined as methods decorated with @fm_dlp.command()
    - Each command delegates to its corresponding module function
    - The CLI framework automatically generates --help for each command
    - Type hints are used for automatic argument parsing and validation

Dependencies:
    - clite: CLI framework for command dispatch and argument parsing
    - modules.searching: YouTube search functionality
    - modules.downloader: Audio download functionality
    - modules.configer: Configuration management
    - modules.helper: Help menu generation
"""

from clite import Clite
from modules.searching import searching
from modules.downloader import download_audio
from modules.configer import configuring_path
from modules.helper import message


# Initialize the CLI application with metadata
# This creates the command-line interface with the specified name and description
# The clite library will parse sys.argv and route to the appropriate command
fm_dlp = Clite(
    name="fm-dlp",
    description="A utility for searching and downloading music from YouTube, based on yt-dlp",
)


@fm_dlp.command()
def search(query: str, limit: int = 10):
    """
    Search for videos on YouTube and display results in a formatted list.

    This command connects to YouTube (via scrapetube), performs a search with the
    given query, filters results to ensure the query appears in the title or channel name,
    and displays up to 'limit' results with titles, channels, dates, views, durations, and URLs.

    Args:
        query (str): The search term(s) to look for on YouTube. This is a required parameter.
        limit (int): Maximum number of raw results to fetch. Defaults to 10.
                    Note that filtering may reduce the actual number of displayed results.

    Returns:
        None: Results are printed directly to the console with color formatting.

    Example:
        fm-dlp search "rick astley" --limit=5
    """
    # Iterate through the generator from searching() and print each video info
    for video_info in searching(query, limit):
        print(video_info)


@fm_dlp.command()
def download(url: str):
    """
    Download audio from a YouTube video as a high-quality M4A file.

    This command extracts audio from the specified YouTube URL and saves it
    as an M4A file (AAC codec, 256 kbps) in the configured download directory.
    Requires FFmpeg to be installed on the system.

    Args:
        url (str): The full YouTube URL. Supported formats:
                   - https://youtube.com/watch?v=VIDEO_ID
                   - https://youtu.be/VIDEO_ID
                   - https://www.youtube.com/watch?v=VIDEO_ID

    Returns:
        None: Download progress and status are printed to the console.

    Example:
        fm-dlp download "https://youtube.com/watch?v=dQw4w9WgXcQ"

    Note:
        The download path must be configured first using the 'config' command.
        If FFmpeg is not installed, yt-dlp will fail with an error message.
    """
    print(download_audio(url))


@fm_dlp.command()
def config(path: str):
    """
    Set or view the download directory path.

    Acts as a setter when a valid path is provided, saving it to config.json.
    Acts as a getter when called without arguments (or with a placeholder),
    displaying the current configuration.

    Args:
        path (str): The directory path where audio files should be saved.
                   If "world" (placeholder from clite), it triggers the getter mode.

    Returns:
        None: Configuration status is printed to the console.

    Examples:
        fm-dlp config "/home/user/Music"    # Set download directory
        fm-dlp config                        # View current configuration

    Note:
        The configuration is stored in config.json in the application root directory.
        The path must be an existing directory on the filesystem.
    """
    print(configuring_path(path))


@fm_dlp.command()
def help():
    """
    Display the help menu with usage instructions for all commands.

    This command prints a comprehensive help message showing all available
    commands, their arguments, and brief descriptions of what each command does.

    Returns:
        None: Help text is printed directly to the console.

    Note:
        This is also the default command shown when the user runs
        fm-dlp without any arguments or with invalid commands.
    """
    print(message())


if __name__ == "__main__":
    # Run the CLI application when this script is executed directly
    # This parses command-line arguments (sys.argv) and dispatches to the appropriate function
    # If no valid command is provided, clite automatically shows the help menu
    fm_dlp()
