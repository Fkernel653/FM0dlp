"""
YouTube search module using the scrapetube library.

This module handles searching for videos on YouTube without requiring an API key.
It includes filtering to ensure results match the original query in title or channel name,
and formats the results for display in the terminal with color-coding.
"""

from modules.colors import RESET, BOLD, RED, GREEN, CYAN, GRAY
import scrapetube


def searching(query: str, limit: int):
    """
    Search YouTube for videos matching the given query and yield formatted results.

    This function uses scrapetube to fetch up to `limit` raw video results from YouTube.
    It then filters these results to only include videos where the query string appears
    in either the video title or the channel name. Each matching video is formatted with
    color-coded information for terminal display.

    Args:
        query (str): The search term to look for on YouTube (case-insensitive matching).
        limit (int): Maximum number of raw results to fetch from YouTube before filtering.
                     Note: The actual number of yielded results may be less than this limit
                     due to the filtering process.

    Yields:
        str: Formatted string containing video information (title, channel, date,
             views, duration, and URL) with ANSI color codes for terminal display.
             If no results match after filtering, yields an error message and exits.
             If a keyboard interrupt occurs, yields a goodbye message.

    Note:
        The function uses relevance sorting and only returns video-type results.
        Filtering ensures that the query appears in the title OR channel name (case-insensitive).
        Network-related exceptions are caught and reported as error messages.

    Raises:
        SystemExit: Exits with code 1 if no videos match the query after filtering.
    """
    try:
        # Fetch raw search results from YouTube using scrapetube
        # Parameters: query string, result limit, sorting method, content type
        videos = scrapetube.get_search(
            query, limit, sort_by="relevance", results_type="video"
        )

        filtered_results = []

        # Filter videos to ensure query appears in title OR channel name
        for video in videos:
            # Extract title text safely, defaulting to "N/A" if missing or malformed
            title = (
                video["title"]["runs"][0]["text"]
                if "runs" in video.get("title", {})
                else "N/A"
            ).lower()

            # Extract channel name safely, defaulting to "N/A" if missing
            channel = (
                video["ownerText"]["runs"][0]["text"] if "ownerText" in video else "N/A"
            ).lower()

            query_lower = query.lower()

            # Keep video if query matches title OR channel name (case-insensitive)
            if query_lower in title or query_lower in channel:
                filtered_results.append(video)

        # Handle case where no videos pass the filter criteria
        if not filtered_results:
            yield f"{RED}\nNo videos matching '{query}' after filtering\n{RESET}"
            return exit(1)

        # Format and yield each filtered video's information
        for num, video in enumerate(filtered_results, start=1):
            # Safely extract all video metadata with fallback values to avoid KeyError
            video_id = video.get("videoId", "N/A")
            title = (
                video["title"]["runs"][0]["text"]
                if "runs" in video.get("title", {})
                else "N/A"
            )
            channel = (
                video["ownerText"]["runs"][0]["text"] if "ownerText" in video else "N/A"
            )
            date = (
                video["publishedTimeText"]["simpleText"]
                if "publishedTimeText" in video
                else "N/A"
            )
            views = (
                video["viewCountText"]["simpleText"]
                if "viewCountText" in video
                else "N/A"
            )
            duration = (
                video["lengthText"]["accessibility"]["accessibilityData"]["label"]
                if "lengthText" in video
                else "N/A"
            )

            # Build formatted output with visual tree structure using Unicode box-drawing characters
            video_info = (
                f"\n{BOLD}{CYAN}{num}. {RESET}{BOLD}{title}{RESET}\n"
                f"   {GRAY}├─ {RESET}{channel}\n"
                f"   {GRAY}├─ {RESET}{date} | {views} | {duration}\n"
                f"   {GRAY}└─ {RESET}{RED}https://youtu.be/{video_id}{RESET}\n"
                f"   {GRAY}   {'─' * 50}{RESET}\n"
            )
            yield video_info

    except KeyboardInterrupt:
        # Graceful exit when user presses Ctrl+C during search operation
        yield f"{GREEN}Goodbye!{RESET}"

    except (
        ConnectionAbortedError,
        ConnectionError,
        ConnectionRefusedError,
        ConnectionResetError,
    ) as e:
        # Handle various network-related connection errors uniformly
        yield f"{RED}Error: {RESET}{e}\n{RED}Check your internet connection{RESET}"
        return
