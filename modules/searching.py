"""YouTube search module using the official Google API v3.

This module handles searching for videos and formatting the results
for display in the terminal with color-coding. It includes filtering
to ensure results match the original query in title or channel name.
"""

from modules.colors import RESET, BOLD, RED, GREEN, BLUE, MAGENTA, CYAN
from pathlib import Path
from dotenv import load_dotenv
import requests
import os


def searching(limit, query):
    """
    Execute a YouTube search using the official Google API and format results.

    Args:
        query (str): User's search terms (e.g., "python tutorial").
        maxResults (int): Number of videos to return, capped at YouTube's 50 limit.

    Returns:
        Generator: Yields formatted video information strings one at a time.

    Yields:
        str: Color-coded terminal output with video details for each result.

    Note:
        The function exits on errors instead of returning error strings,
        ensuring cleaner error handling flow in the CLI. Results are filtered
        to only include videos where the query appears in title or channel name.
    """
    # Build query parameters according to YouTube API v3 specification

    parent_folder = Path(__file__).parent
    env_file = Path(parent_folder).parent / "key.env"

    load_dotenv(env_file)

    params = {
        "part": "snippet",  # Request basic metadata (title, description, thumbnails)
        "q": query,  # URL-encoded search string from user
        "videoDuration": "medium",  # Filter: medium = 4-20 minutes (also 'short' or 'long')
        "maxResults": min(limit, 50),  # Enforce API limit to avoid rejection
        "type": "video",  # Exclude channels and playlists from results
        "key": os.getenv(
            "YOUTUBE_DATA_API_KEY"
        ),  # API key for authentication and quota tracking
    }

    try:
        # Execute HTTP GET with 10-second timeout to prevent hanging
        r = requests.get(
            "https://www.googleapis.com/youtube/v3/search", params=params, timeout=10
        )

        # HTTP 200 means successful response with data
        if r.status_code == 200:
            # Convert JSON response to Python dictionary
            data = r.json()
            # Extract the list of video items, default to empty if missing
            results = data.get("items", [])

            # Handle empty result sets gracefully
            if not results:
                yield f"{RED}\nNo videos found\n{RESET}"
                return

            # Filter results to ensure query appears in title or channel name
            filtered_results = []
            for item in results:
                snippets = item.get("snippet", {})

                title = snippets.get("title", "").lower()
                channel = snippets.get("channelTitle", "").lower()
                query_lower = query.lower()

                if query_lower in title or query_lower in channel:
                    filtered_results.append(item)

            if not filtered_results:
                yield f"{RED}\nNo videos matching '{query}' after filtering\n{RESET}"
                return

            # Enumerate with 1-based indexing for user-friendly numbering
            for num, item in enumerate(filtered_results, start=1):
                # Safely extract nested dictionaries with fallbacks
                ids = item.get("id", {})  # Contains videoId, playlistId, etc.
                snippets = item.get("snippet", {})  # Contains title, channel, date

                # Extract metadata with 'N/A' fallback for missing fields
                channel_title = snippets.get(
                    "channelTitle", "N/A"
                )  # Uploader's channel name
                title = snippets.get("title", "N/A")  # Video title (may contain emojis)
                creation_date = snippets.get("publishedAt", "N/A")  # ISO 8601 timestamp
                video_id = ids.get("videoId", "N/A")  # 11-character unique identifier

                # Format with ANSI escape sequences for terminal colors
                # Each color constant provides visual distinction for different data types
                video_info = f"""
{BOLD}{num}. {CYAN}Title: {RESET}'{title}'
{MAGENTA}Channel Title: {RESET}'{channel_title}'
{BLUE}Creation Date: {RESET}'{creation_date}'
{RED}URL: {RESET}{BOLD}https://www.youtube.com/watch?v={video_id}{RESET}
"""
                yield video_info

        else:
            # Non-200 status code indicates API problem (quota exceeded, invalid key, etc.)
            print(f"{RED}\nError{RESET} {r.status_code}\n")
            return exit(1)  # Exit with error code to prevent further execution

    except requests.exceptions.RequestException as e:
        # Catch network errors, DNS failures, connection timeouts
        print(f"{RED}\nRequest error:{RESET} {e}\n")
        return exit(1)  # Exit with error code

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully with user-friendly message
        print(f"{GREEN}\n\tGoodbye!\n{RESET}")
        return exit(0)