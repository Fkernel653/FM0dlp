from fake_useragent import UserAgent  # Library for generating random browser User-Agent strings to prevent blocking
from pathlib import Path  # Object-oriented filesystem paths that work on all operating systems
from yt_dlp import YoutubeDL  # Powerful YouTube downloading library with format selection and extraction
import requests  # Simple HTTP library for making API requests to YouTube's servers
import readline  # GNU readline integration for better command line editing (arrow keys, history)
import json  # JSON encoder/decoder for storing configuration data persistently
import os  # Operating system interfaces for screen clearing and path operations

class FM0dlp:
    """
    Core class that encapsulates all YouTube video search and download functionality.
    Provides methods for API-based search, audio extraction, and configuration persistence.
    """
    
    def __init__(self):
        """
        Constructor that initializes the YouTube API connection and user agent generator.
        Sets up the foundation for all subsequent operations.
        
        Security Note: API key is now loaded from environment variable instead of hardcoded,
        preventing accidental exposure in source code repositories.
        """
        # WARNING: Set environment variable YOUR_API_KEY_HOME with your YouTube Data API v3 key
        # Get it from: https://console.cloud.google.com/apis/credentials
        self.api_key = os.environ.get("YOUR_API_KEY_HOME")  # Authentication credential loaded from environment
        self.api = "https://www.googleapis.com/youtube/v3/search"  # Google's REST endpoint for video search
        self.ua = UserAgent()  # Generator that provides random browser fingerprints (Chrome, Firefox, etc.)
        
    def search(self, query, maxResults=50):
        """
        Execute a YouTube search using the official Google API and format results.
        
        Args:
            query (str): User's search terms (e.g., "python tutorial")
            maxResults (int): Number of videos to return, capped at YouTube's 50 limit
        
        Returns:
            str: Color-coded terminal output with video details or error message
            
        Note: This method now exits on errors instead of returning error strings,
        ensuring cleaner error handling flow.
        """
        # Build query parameters according to YouTube API v3 specification
        params = {
            'part': 'snippet',  # Request basic metadata (title, description, thumbnails)
            'q': query,  # URL-encoded search string from user
            'videoDuration': 'medium',  # Filter: medium = 4-20 minutes (also 'short' or 'long')
            'maxResults': min(maxResults, 50),  # Enforce API limit to avoid rejection
            'type': 'video',  # Exclude channels and playlists from results
            'key': self.api_key  # Quota tracking and authentication
        }

        try:
            # Execute HTTP GET with 10-second timeout to prevent hanging
            r = requests.get(self.api, params=params, timeout=10)

            # HTTP 200 means successful response with data
            if r.status_code == 200:
                # Convert JSON response to Python dictionary
                data = r.json()
                # Extract the list of video items, default to empty if missing
                results = data.get('items', [])

                # Handle empty result sets gracefully
                if not results:
                    return "\033[01;31m\nNo videos found\n\033[01;0m"  # Red text for errors

                all_videos = []  # Accumulator for formatted video entries
                
                # Enumerate with 1-based indexing for user-friendly numbering
                for num, item in enumerate(results, start=1):
                    # Safely extract nested dictionaries with fallbacks
                    ids = item.get('id', {})  # Contains videoId, playlistId, etc.
                    snippets = item.get('snippet', {})  # Contains title, channel, date

                    # Extract metadata with 'N/A' fallback for missing fields
                    channel_title = snippets.get('channelTitle', 'N/A')  # Uploader's channel name
                    title = snippets.get('title', 'N/A')  # Video title (may contain emojis)
                    creation_date = snippets.get('publishedAt', 'N/A')  # ISO 8601 timestamp
                    video_id = ids.get('videoId', 'N/A')  # 11-character unique identifier

                    # Format with ANSI escape sequences for terminal colors
                    # 37=white, 36=cyan, 35=purple, 34=blue, 31=red, 0=reset
                    video_info = f"""
\033[01;37m{num}. \033[01;36mTitle: \033[01;0m'{title}'
\033[01;35mChannel Title: \033[01;0m'{channel_title}'
\033[01;34mCreation Date: \033[01;0m'{creation_date}'
\033[01;31mURL: \033[01;37mhttps://www.youtube.com/watch?v={video_id}\033[01;0m
"""
                    all_videos.append(video_info)  # Collect formatted string

                # Combine all entries with newline separators
                return '\n'.join(all_videos)

            else:
                # Non-200 status code indicates API problem (quota exceeded, invalid key, etc.)
                print(f"\033[01;31m\nError\033[01;0m {r.status_code}\n")
                return exit(1)  # Exit with error code
                
            
        except requests.exceptions.RequestException as e:
            # Catch network errors, DNS failures, connection timeouts
            print(f"\033[01;31m\nRequest error:\033[01;0m {e}\n")
            return exit(1)  # Exit with error code


    def download_audio(self, url: str) -> None:
        """
        Extract audio track from YouTube video and save as high-quality M4A file.
        
        Args:
            url (str): Complete YouTube URL (youtube.com/watch?v=... or youtu.be/...)
        
        Returns:
            str: Confirmation message with filesystem location or error details
            
        Note: Requires FFmpeg to be installed on the system for audio extraction.
        """
        # Locate config file in the same directory as this script
        config_file = Path(__file__).parent / 'config.json'

        # Verify configuration exists before attempting download
        if not config_file.exists():
            print("\033[01;31m\nConfig file not found! Please set download path first.\n\033[01;0m")
            return exit(1)  # Exit with error code

        # Read and parse existing configuration
        with open(config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)  # Convert JSON to Python dict
            # FIXED: Changed key from 'configuring_path' to 'download_path' to match config structure
            saved_path = data.get('download_path')  # Retrieve user's download directory

            # yt-dlp configuration dictionary with all options
            opts = {
                'user_agent': self.ua.random,  # Rotate fingerprints to avoid rate limiting
                'format': 'bestaudio/best',  # Select highest quality audio stream available
                'outtmpl': f'{saved_path}/%(title)s.%(ext)s',  # Naming pattern: title.extension
                'postprocessors': [{  # Array of post-processing steps
                    'key': 'FFmpegExtractAudio',  # Built-in FFmpeg audio extraction
                    'preferredcodec': 'm4a',  # Target format (AAC in MP4 container)
                    'preferredquality': '256',  # Bitrate in kbps (balance quality/size)
                }],
                "quiet": False  # Show detailed progress in terminal
            }

            try:
                # Context manager ensures proper cleanup of resources
                with YoutubeDL(opts) as ydl:
                    ydl.download([url])  # Pass URL in list (supports multiple videos)
                    
                # Success message with italicized path (ANSI 3)
                return f"\033[01;32m\tThe video was uploaded to: \033[01;0m\033[01;3m{saved_path}\033[01;0m"
            
            except Exception as e:
                # Catch all yt-dlp exceptions (unavailable video, geo-block, etc.)
                print(f"\033[01;31m\nDownload error: \033[01;0m{e}\n")
                return exit(1)  # Exit with error code


    def configuring_path(self, path):
        """
        Manage persistent storage location for downloaded audio files.
        Acts as both setter and getter for the download directory.
        
        Args:
            path (str): Directory path to save files, or empty string to query current
        
        Returns:
            str: Status message with current or newly set path
            
        Note: When path is empty, acts as getter and returns current configuration.
        When path is provided, acts as setter and saves to config.json.
        """
        # Configuration file location (same directory as script)
        config_file = Path(__file__).parent / 'config.json'

        # SETTER MODE: User provided a path to save
        if path:
            # Build configuration object with metadata
            config = {
                'download_path': str(path),  # Convert Path object to string if needed
                # Note: Removed 'last_updated' field for simplicity
            }

            # Write to filesystem with human-readable formatting
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)  # Pretty print with indentation

            # Confirm successful save
            return f"\033[01;32mPath saved: \033[01;0m\033[01;3m{path}\033[01;0m"

        # GETTER MODE: User wants to see current configuration
        else:
            if config_file.exists():
                # Attempt to read existing config
                with open(config_file, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)  # Parse JSON
                        # FIXED: Changed key to match the actual config structure
                        saved_path = data.get('download_path')  # Extract path value

                        # Validate that path exists on filesystem
                        if saved_path and Path(saved_path).exists():
                            return f"\033[01;32mLoaded path: \033[01;0m\033[01;3m{saved_path}\033[01;0m"
                        else:
                            # Config exists but path is invalid
                            print(f"\033[01;31m\nConfig file is corrupted! Use the current folder: \033[01;0m\033[01;03m{os.getcwd()}\n\033[01;0m")
                            # Spare folder - home directory as fallback
                            return os.getcwd()
                    
                    except json.JSONDecodeError:
                        # Config file is corrupted (invalid JSON)
                        print(f"\033[01;31m\nConfig file is corrupted! Use the current folder: \033[01;0m\033[01;03m{os.getcwd()}\n\033[01;0m")
                        return os.getcwd()  # Return current directory as fallback
            else:
                # No config file exists yet
                print(f"\033[01;31m\nConfig file not found, use the current folder: \033[01;0m\033[01;3m{os.getcwd()}\n\033[01;0m")
                return os.getcwd()  # Return current directory as fallback


def clear():
    """
    Perform clean program termination with screen clearing and history wiping.
    Ensures no sensitive data remains in memory or terminal.
    
    Called on normal exit (option 4) and on KeyboardInterrupt (Ctrl+C).
    """
    # Platform-specific screen clearing (cls for Windows, clear for Unix)
    os.system('cls' if os.name == 'nt' else 'clear')
    readline.clear_history()  # Remove all command history from memory
    print("\033[01;32mGoodbye!\033[01;0m")  # Green farewell message
    exit(0)  # Successful exit status


def get_selections_menu():
    """
    Generate interactive menu with color-coded options.
    
    Returns:
        str: Formatted menu string with ANSI color codes
        
    Note: Colors are now consistent: Blue for Search, Green for Download,
    Gray for Configuration, Red for Exit.
    """
    selections = """
    1: \033[01;34mSearch\033[01;0m
    2: \033[01;32mDownload\033[01;0m
    3: \033[01;90mDownload folder configuration\033[01;0m
    4: \033[01;31mExit\033[01;0m
    """
    return selections


def inputs():
    """
    Handle user interaction loop for menu selection and operation execution.
    Recursively returns to menu after each operation until exit.
    
    This function implements the main user interface logic and routes
    user choices to the appropriate FM0dlp methods.
    """
    print(get_selections_menu())  # Display the menu options
    
    # Capture user's choice with colored prompt
    user_option = input("\033[01;37m\tPlease enter your option: \033[01;0m")
    
    # Instantiate the main class for each operation (ensures fresh state)
    downloader = FM0dlp()

    # Route user choice to appropriate method
    if user_option == '1':
        # SEARCH: Query YouTube and display results
        user_query = input("\033[01;37m\t\tEnter your query: \033[01;0m")
        print(downloader.search(user_query))  # Execute search
        return inputs()  # Return to menu (recursive)

    elif user_option == '2':
        # DOWNLOAD: Extract audio from URL
        user_url = input("\033[01;37m\t\tEnter the video link: \033[01;0m")

        result = downloader.download_audio(user_url)
        print(result)  # Display download result

        return inputs()  # Back to menu
    
    elif user_option == '3':
        # CONFIG: Set or view download location
        user_path = input("\033[01;37m\t\tEnter the path: \033[01;0m")
        print(downloader.configuring_path(user_path))  # Update config
        return inputs()  # Return to menu

    elif user_option == '4':
        # EXIT: Clean termination
        clear()  # Goodbye sequence


def main():
    """
    Main program controller with infinite loop and interrupt handling.
    Sets up the environment and enters the user interaction cycle.
    
    Wrapped in try-except to catch KeyboardInterrupt (Ctrl+C) gracefully.
    """
    try:
        while True:  # Continuous operation until explicit exit
            # Clear screen for fresh display each iteration
            os.system('cls' if os.name == 'nt' else 'clear')
    
            # ASCII art banner with developer credit
            banner = f"""\033[01;31m
 88888888b 8888ba.88ba                    oo         
 88        88  `8b  `8b                              
a88aaaa    88   88   88 dP    dP .d8888b. dP .d8888b.
 88        88   88   88 88    88 Y8ooooo. 88 88'  `""
 88        88   88   88 88.  .88       88 88 88.  ...
 dP        dP   dP   dP `88888P' `88888P' dP `88888P'

                             \033[01;0mdev = "\033[01;3mFkernel653\033[01;0m" """
            print(banner)  # Show the banner

            inputs()  # Enter the main interaction loop

    # Handle Ctrl+C gracefully (no traceback)
    except KeyboardInterrupt:
        clear()  # Clean shutdown on interrupt

# Standard Python guard to prevent execution on import
if __name__ == "__main__":
    main()
