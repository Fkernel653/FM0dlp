"""Helper module for displaying usage information.

This module provides the help menu text that shows all available
commands and their usage instructions to the user.
"""


def message():
    """
    Generate the help menu text for the fm-dlp application.

    Returns:
        str: A formatted string containing all available commands
             and their usage instructions. Each command is displayed
             with a brief description of its function.
    """
    menu = """fm-dlp commands:
    search <query>    - Search for videos on YouTube and display results
    download <url>    - Download audio from a YouTube video as M4A file
    config <path>     - Set download directory (or view current if no path)
    help              - Show this help message with command descriptions"""
    return menu
