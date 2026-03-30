"""
Helper module for displaying usage information.

This module provides the help menu text that shows all available
commands and their usage instructions to the user. The help menu
is displayed when the user runs the 'help' command or provides
no arguments.
"""


def message() -> str:
    """
    Generate the help menu text for the fm-dlp application.

    Returns:
        str: A formatted string containing all available commands
             and their usage instructions. Each command is displayed
             with a brief description of its function and expected arguments.

    Command Descriptions:
        search <query> --limit=<integer> - Searches YouTube for videos matching
            the query and displays up to 'limit' results with titles, channels,
            views, durations, and URLs.

        download <url> - Downloads audio from a YouTube video as a high-quality
            M4A file (256 kbps AAC) to the configured download directory.

        config <path> - Sets the download directory to the specified path.
            When called without a path, displays the current configuration.

        help - Displays this help message with all command descriptions.

    Note:
        The download command requires FFmpeg to be installed on the system
        for audio extraction. The config command must be used before downloading
        to set a valid download directory.
    """
    menu = """fm-dlp commands:
    search <query> --limit=<integer>    - Search for videos on YouTube and display results
    download <url>                      - Download audio from a YouTube video as M4A file
    config <path>                       - Set download directory (or view current if no path)
    help                                - Show this help message with command descriptions"""
    return menu
