from fake_useragent import UserAgent  # Import for generating random User-Agent strings to avoid detection
from pathlib import Path  # Import for cross-platform path handling (Windows/Linux/Mac compatible)
from yt_dlp import YoutubeDL  # Import yt-dlp library for downloading YouTube videos and extracting audio
import requests  # Import requests library for making HTTP requests to YouTube API
import readline  # Import readline for better command line input handling (history, arrow keys)
import json  # Import json module for reading and writing configuration files
import os  # Import os for operating system operations (clearing screen, path operations)

class FM0dlp:
    """
    Main class for YouTube video searching and downloading functionality.
    Handles API searches, audio downloads, and configuration management.
    """
    
    def __init__(self):
        """
        Initialize the FM0dlp class with API credentials and user agent generator.
        Sets up the YouTube Data API endpoint and creates a UserAgent instance.
        """
        # YouTube Data API v3 key - required for search functionality
        # WARNING: This key is visible in the code, consider using environment variables for security
        self.api_key = "AIzaSyBnWX6jA6qOqSVAo_vzsr6Nnpdg5NHFK5s"
        # YouTube API endpoint URL for search operations
        self.api = "https://www.googleapis.com/youtube/v3/search"
        # Create UserAgent instance for generating random browser user agents
        self.ua = UserAgent()
        
    def search(self, query, maxResults=50):
        """
        Search for videos on YouTube using the official YouTube Data API.
        
        Args:
            query (str): The search query string (what user wants to find)
            maxResults (int): Maximum number of results to return (default: 50, max: 50 due to API limit)
        
        Returns:
            str: Formatted string containing video search results or error message with ANSI colors
        """
        # Prepare parameters for YouTube API request according to API documentation
        params = {
            'part': 'snippet',  # Request snippet part containing video metadata (title, channel, etc.)
            'q': query,  # Search query string entered by user
            'videoDuration': 'medium',  # Filter for medium-length videos (4-20 minutes)
            'maxResults': min(maxResults, 50),  # Limit results to 50 max (YouTube API limitation)
            'type': 'video',  # Search only for videos (exclude channels and playlists)
            'key': self.api_key  # API authentication key for quota tracking
        }

        try:
            # Make HTTP GET request to YouTube API with 10 second timeout
            r = requests.get(self.api, params=params, timeout=10)

            # Check if request was successful (HTTP 200 OK)
            if r.status_code == 200:
                # Parse JSON response from API into Python dictionary
                data = r.json()
                # Extract video items from response, default to empty list if 'items' key not found
                results = data.get('items', [])

                # Check if any results were found
                if not results:
                    return "\033[01;31m No videos found\033[01;0m"  # Red error message

                all_videos = []  # Initialize list to store formatted video information
                
                # Iterate through search results with enumeration starting at 1 for user-friendly numbering
                for num, item in enumerate(results, start=1):
                    # Extract ID and snippet sections from each result item
                    # Using .get() with empty dict default to avoid KeyError if fields are missing
                    ids = item.get('id', {})
                    snippets = item.get('snippet', {})

                    # Extract relevant video metadata with 'N/A' as default value if field is missing
                    channel_title = snippets.get('channelTitle', 'N/A')  # Name of the channel that uploaded video
                    title = snippets.get('title', 'N/A')  # Title of the video
                    creation_date = snippets.get('publishedAt', 'N/A')  # Upload date in ISO 8601 format
                    video_id = ids.get('videoId', 'N/A')  # Unique YouTube video identifier (11 characters)

                    # Format video information with ANSI color codes for better terminal readability
                    # Color codes: 37=white, 36=cyan, 35=magenta, 34=blue, 31=red
                    video_info = f"""
\033[01;37m{num}. \033[01;36mTitle: \033[01;0m'{title}'
\033[01;35mChannel Title: \033[01;0m'{channel_title}'
\033[01;34mCreation Date: \033[01;0m'{creation_date}'
\033[01;31mURL: \033[01;37mhttps://www.youtube.com/watch?v={video_id}\033[01;0m
"""
                    all_videos.append(video_info)  # Add formatted info to list

                # Join all video information with newlines and return as single string
                return '\n'.join(all_videos)

            else:
                # Return error message with HTTP status code if request failed
                return f"\033[01;31m Error\033[01;0m {r.status_code}"
            
        except requests.exceptions.RequestException as e:
            # Handle network-related errors (timeout, connection error, etc.)
            return "\033[01;31m Request error:\033[01;0m {e}"


    def download_audio(self, url: str) -> None:
        """
        Download audio from a YouTube video using yt-dlp library.
        Converts video to M4A audio format at 192 kbps quality.
        
        Args:
            url (str): YouTube video URL to download audio from
        
        Returns:
            str: Success message with download path or error message
        """
        # Construct path to configuration file in same directory as script
        # Path(__file__).parent gets the directory containing this script
        config_file = Path(__file__).parent / 'config.json'

        # Check if configuration file exists before attempting to read
        if not config_file.exists():
            return "\033[01;31mConfig file not found! Please set download path first.\033[01;0m"

        # Open and read configuration file with UTF-8 encoding for special characters
        with open(config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)  # Parse JSON configuration into Python dictionary
            saved_path = data.get('download_path')  # Extract download path from config

            # Configure yt-dlp options for optimal audio extraction
            opts = {
                'user_agent': self.ua.random,  # Use random user agent to avoid YouTube blocking
                'format': 'bestaudio/best',  # Download best available audio quality
                'outtmpl': f'{saved_path}/%(title)s.%(ext)s',  # Output template: path/title.extension
                'postprocessors': [{  # Post-processing configuration array
                    'key': 'FFmpegExtractAudio',  # Use FFmpeg to extract audio stream
                    'preferredcodec': 'm4a',  # Convert to m4a (AAC) audio format
                    'preferredquality': '192',  # Set audio quality to 192 kbps
                }],
                "quiet": False  # Show download progress in console (False = show progress)
            }

            try:
                # Create YoutubeDL instance with configured options
                with YoutubeDL(opts) as ydl:
                    ydl.download([url])  # Download the video and extract audio (accepts list of URLs)
                    
                # Return success message with download path (italic text with ANSI code 3)
                return f"\033[01;32m\tThe video was uploaded to: \033[01;0m\033[01;3m{saved_path}\033[01;0m"
            except Exception as e:
                # Catch any yt-dlp related errors (network issues, unavailable video, etc.)
                return f"\033[01;31mDownload error: \033[01;0m{e}"


    def download_path(self, path):
        """
        Set or retrieve the download path configuration.
        If path is provided, saves it to config.json.
        If path is empty/None, displays current configuration.
        
        Args:
            path (str): Path to set as download directory, or None/empty to retrieve current path
        
        Returns:
            str: Success message or current path information with ANSI colors
        """
        # Construct path to configuration file in script directory
        config_file = Path(__file__).parent / 'config.json'

        # Check if path was provided (setting new path mode)
        if path:
            # Create configuration dictionary with metadata
            config = {
                'download_path': str(path),  # Save provided path as string
                'last_updated': str(Path(path).resolve())  # Store resolved absolute path (resolves .. and .)
            }

            # Write configuration to JSON file with pretty formatting
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)  # indent=4 for human readability

            # Return success message with saved path
            return f"\033[01;32mPath saved: \033[01;0m\033[01;3m{path}\033[01;0m"

        else:
            # No path provided - retrieve current configuration mode
            if config_file.exists():
                # Open and read existing configuration file
                with open(config_file, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)  # Parse JSON
                        saved_path = data.get('download_path')  # Extract saved path

                        # Check if path exists and is valid directory
                        if saved_path and Path(saved_path).exists():
                            return f"\033[01;32mLoaded path: \033[01;0m\033[01;3m{saved_path}\033[01;0m"
                        else:
                            # Path invalid or not found, return current working directory as fallback
                            return f"\033[01;31mConfig file not found, use the current folder: \033[01;0m\033[01;03m{os.getcwd()}\033[01;0m"
                    
                    except json.JSONDecodeError:
                        # Handle corrupted JSON file (invalid syntax)
                        print("\033[01;31mFile config.json corrupted!\033[01;0m")
                        return os.getcwd()  # Return current directory as fallback
            else:
                # No configuration file exists, return current working directory
                return f"\033[01;31mConfig file not found, use the current folder: \033[01;0m\033[01;3m{os.getcwd()}\033[01;0m"


def clear_screen():
    """
    Clear the terminal screen and clear readline history.
    Works on both Windows and Unix-like systems.
    """
    # cls for Windows (nt), clear for Unix/Linux/Mac
    os.system('cls' if os.name == 'nt' else 'clear')
    readline.clear_history()  # Clear command line history for privacy


def show_goodbye():
    """
    Display goodbye message and exit the program with success code.
    """
    print("\033[01;32mGoodbye!\033[01;0m")  # Green goodbye message
    exit(0)  # Exit with success code


def get_selections_menu():
    """
    Return the main menu options as a formatted string.
    Separated into function for easy modification.
    
    Returns:
        str: Menu options with numbers
    """
    return """
1: Search
2: Download
3: Boot path configuration
4: Exit
"""


def get_banner():
    """
    Generate and return the complete banner with ASCII art and menu.
    Combines ASCII art with menu options.
    
    Returns:
        str: Complete banner with colors
    """
    selections = get_selections_menu()  # Get menu options
    # ASCII art banner with red color (31) and dev name in italic (3)
    banner = f"""\033[01;31m
88888888b 8888ba.88ba                    oo         
 88        88  `8b  `8b                              
a88aaaa    88   88   88 dP    dP .d8888b. dP .d8888b.
 88        88   88   88 88    88 Y8ooooo. 88 88'  `""
 88        88   88   88 88.  .88       88 88 88.  ...
 dP        dP   dP   dP `88888P' `88888P' dP `88888P'

                            \033[01;0mdev = "\033[01;3mFkernel653\033[01;0m"
    {selections}
            """
    return banner


def process_option(option, downloader):
    """
    Process user's menu selection and execute corresponding action.
    
    Args:
        option (str): User's menu choice (1, 2, 3, or 4)
        downloader (FM0dlp): Instance of FM0dlp class to handle operations
    
    Returns:
        bool: True if should continue, False if should exit
    """
    if option == '1':
        # Search option selected
        query = input("\033[01;37m\t\tEnter your query: \033[01;0m")  # White prompt
        result = downloader.search(query)  # Perform search
        print(result)  # Display results
        
    elif option == '2':
        # Download option selected
        url = input("\033[01;37m\t\tEnter the video link: \033[01;0m")  # White prompt
        result = downloader.download_audio(url)  # Download audio
        print(result)  # Show result message
        
    elif option == '3':
        # Path configuration option selected
        path = input("\033[01;37m\t\tEnter the download path: \033[01;0m")  # White prompt
        result = downloader.download_path(path)  # Set or display path
        print(result)  # Show path information
        
    elif option == '4':
        # Exit option selected
        return False  # Signal to exit main loop
        
    return True  # Signal to continue


def main():
    """
    Main program entry point and control loop.
    Handles program initialization, user interaction loop, and cleanup.
    """
    # Create instance of FM0dlp class to handle all operations
    downloader = FM0dlp()
    
    try:
        # Main program loop - continues until user chooses to exit
        while True:
            clear_screen()  # Clear screen at start of each iteration
            print(get_banner())  # Display banner with ASCII art and menu
            
            # Get user's menu choice with white prompt
            user_option = input("\033[01;37m\tPlease enter your option: \033[01;0m")
            
            # Process the selected option
            should_continue = process_option(user_option, downloader)
            
            # Check if user chose to exit
            if not should_continue:
                break  # Exit main loop
            
            # Pause before next iteration so user can read results
            input("\n\033[01;33mPress Enter to continue...\033[01;0m")  # Yellow prompt
            
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully - just pass to finally block
        # Print newline to clean up the terminal
        print()
    
    finally:
        # Always show goodbye message, even if interrupted
        show_goodbye()


# Standard Python idiom to ensure main() runs only when script is executed directly
# Not executed when imported as module
if __name__ == "__main__":
    main()
