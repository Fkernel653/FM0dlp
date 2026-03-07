from fake_useragent import UserAgent  # Import UserAgent for generating random user agents
from pathlib import Path  # Import Path for cross-platform path handling
from yt_dlp import YoutubeDL  # Import YoutubeDL for downloading YouTube content
import requests  # Import requests for making HTTP requests to YouTube API
import readline  # Import readline for better command line input handling
import json  # Import json for handling JSON configuration files
import os  # Import os for operating system operations

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
        self.api_key = ""  # YouTube Data API key (needs to be filled by user)
        self.api = "https://www.googleapis.com/youtube/v3/search"  # YouTube API endpoint URL
        self.ua = UserAgent()  # Create UserAgent instance for generating random user agents
        
    def search(self, query, maxResults=10):
        """
        Search for videos on YouTube using the official YouTube Data API.
        
        Args:
            query (str): The search query string
            maxResults (int): Maximum number of results to return (default: 10, max: 50)
        
        Returns:
            str: Formatted string containing video search results or error message
        """
        # Prepare parameters for YouTube API request
        params = {
            'part': 'snippet',  # Request snippet part containing video metadata
            'q': query,  # Search query string
            'videoDuration': 'medium',  # Filter for medium-length videos
            'maxResults': min(maxResults, 50),  # Limit results, ensuring not to exceed API limit
            'type': 'video',  # Search only for videos (not channels or playlists)
            'key': self.api_key  # API authentication key
        }

        try:
            # Make HTTP GET request to YouTube API with timeout
            r = requests.get(self.api, params=params, timeout=10)

            # Check if request was successful
            if r.status_code == 200:
                # Parse JSON response from API
                data = r.json()
                # Extract video items from response, default to empty list if not found
                results = data.get('items', [])

                # Check if any results were found
                if not results:
                    return "\033[01;31m No videos found\033[01;0m"  # Red error message

                all_videos = []  # Initialize list to store formatted video information
                
                # Iterate through search results with enumeration starting at 1
                for num, item in enumerate(results, start=1):
                    # Extract ID and snippet sections from each result item
                    ids = item.get('id', {})
                    snippets = item.get('snippet', {})

                    # Extract relevant video metadata with default values
                    channel_title = snippets.get('channelTitle', 'N/A')  # Channel name
                    title = snippets.get('title', 'N/A')  # Video title
                    creation_date = snippets.get('publishedAt', 'N/A')  # Upload date
                    video_id = ids.get('videoId', 'N/A')  # Unique video identifier

                    # Format video information with ANSI color codes for terminal display
                    video_info = f"""
\033[01;37m{num}. \033[01;36mTitle: \033[01;0m'{title}'
\033[01;35mChannel Title: \033[01;0m'{channel_title}'
\033[01;34mCreation Date: \033[01;0m'{creation_date}'
\033[01;31mURL: \033[01;37mhttps://www.youtube.com/watch?v={video_id}\033[01;0m
"""
                    all_videos.append(video_info)  # Add formatted info to list

                # Join all video information with newlines and return
                return '\n'.join(all_videos)

            else:
                # Return error message with status code if request failed
                return f"\033[01;31m Error\033[01;0m {r.status_code}"
            
        except requests.exceptions.RequestException as e:
            # Handle network or request-related errors
            return "\033[01;31m Request error:\033[01;0m {e}"


    def download_audio(self, url: str) -> None:
        """
        Download audio from a YouTube video using yt-dlp.
        
        Args:
            url (str): YouTube video URL to download audio from
        
        Returns:
            str: Success message with download path or error message
        """
        # Construct path to configuration file in same directory as script
        config_file = Path(__file__).parent / 'config.json'

        # Check if configuration file exists
        if not config_file.exists():
            return "\033[01;31mConfig file not found! Please set download path first.\033[01;0m"

        # Open and read configuration file
        with open(config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)  # Parse JSON configuration
            saved_path = data.get('download_path')  # Extract download path from config

            # Configure yt-dlp options for audio extraction
            opts = {
                'user_agent': self.ua.random,  # Use random user agent to avoid detection
                'format': 'bestaudio/best',  # Download best available audio quality
                'outtmpl': f'{saved_path}/%(title)s.%(ext)s',  # Output template for filename
                'postprocessors': [{  # Post-processing configuration
                    'key': 'FFmpegExtractAudio',  # Extract audio using FFmpeg
                    'preferredcodec': 'm4a',  # Convert to m4a audio format
                    'preferredquality': '192',  # Set audio quality to 192 kbps
                }],

                'remote_components': 'ejs:github',  # Remote components configuration

                'extractor_args': {  # Additional extractor arguments
                    'youtube': {
                        'js_runtime': 'deno'  # Use deno JavaScript runtime for extraction
                    }
                },
                "quiet": False  # Show download progress in console
            }
            
            # Create YoutubeDL instance with configured options and download
            with YoutubeDL(opts) as ydl:
                ydl.download([url])  # Download the video and extract audio
                
                # Return success message with download path
                return f"\033[01;32m\tThe video was uploaded to: \033[01;0m\033[01;3m{saved_path}\033[01;0m"


    def download_path(self, path):
        """
        Set or retrieve the download path configuration.
        
        Args:
            path (str): Path to set as download directory, or None to retrieve current path
        
        Returns:
            str: Success message or current path information
        """
        # Construct path to configuration file
        config_file = Path(__file__).parent / 'config.json'

        # Check if path was provided (setting new path)
        if path:
            # Create configuration dictionary
            config = {
                'download_path': str(path),  # Save provided path
                'last_updated': str(Path(path).resolve())  # Store resolved absolute path
            }

            # Write configuration to JSON file
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)  # Pretty print JSON

            # Return success message with saved path
            return f"\033[01;32mPath saved: \033[01;0m\033[01;3m{path}"

        else:
            # No path provided - retrieve current configuration
            if config_file.exists():
                # Open and read existing configuration file
                with open(config_file, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)  # Parse JSON
                        saved_path = data.get('download_path')  # Extract saved path

                        # Check if path exists and is valid
                        if saved_path and Path(saved_path).exists():
                            return f"\033[01;32mLoaded path: \033[01;0m\033[01;3m{saved_path}\033;01;0m"
                        else:
                            # Path invalid or not found, return current working directory
                            return f"\033[01;31mConfig file not found, use the current folder: \033[01;0m\033[01;03m{os.getcwd()}\033[01;0m"
                    
                    except json.JSONDecodeError:
                        # Handle corrupted JSON file
                        print("\033[01;31mFile config.json corrupted!\033[01;0m")
                        return os.getcwd()  # Return current directory as fallback
            else:
                # No configuration file exists
                return f"\033[01;31mConfig file not found, use the current folder: \033[01;0m\033[01;3m{os.getcwd()}\033[01;3m"

def end():
    """
    Handle program termination and restart logic.
    Asks user if they want to continue or exit the program.
    """
    # Prompt user for continuation choice
    user_variant = input("\033[01;91m\tDo you want to continue? \033[01;0m(Y/n): ")
    
    # Check if user wants to continue (case-insensitive)
    if user_variant == 'Y'.lower():
        main()  # Restart the main function
    else:
        # Clean up and exit
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen (Windows vs Unix)
        readline.clear_history()  # Clear command history
        print("\033[01;32mGoodbye!\033[01;0m")  # Print goodbye message
        exit(0)  # Exit program with success code

def main():
    """
    Main program entry point.
    Displays banner, handles user input, and routes to appropriate functionality.
    """
    # Clear terminal screen (cls for Windows, clear for Unix-like systems)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # ASCII art banner with ANSI color codes
    banner = """\033[01;31m
 88888888b 8888ba.88ba                    oo         
 88        88  `8b  `8b                              
a88aaaa    88   88   88 dP    dP .d8888b. dP .d8888b.
 88        88   88   88 88    88 Y8ooooo. 88 88'  `""
 88        88   88   88 88.  .88       88 88 88.  ...
 dP        dP   dP   dP `88888P' `88888P' dP `88888P'

                             \033[01;0mdev = "\033[01;3mFkernel653\033[01;0m"
    1: Search
    2: Download
    3: Boot path configuration
"""
    print(banner)  # Display banner to user

    # Get user's menu choice
    user_option = input("\033[01;37m\tPlease enter your option: \033[01;0m")
    
    # Create instance of FM0dlp class
    root = FM0dlp()

    # Handle user's menu selection
    if user_option == '1':
        # Search option selected
        user_query = input("\033[01;37m\t\tEnter your query \033[01;0m")
        print(root.search(user_query))  # Perform search and display results
        end()  # Ask if user wants to continue

    elif user_option == '2':
        # Download option selected
        user_url = input("\033[01;37m\t\tEnter the video link: \033[01;0m")
        print(root.download_audio(user_url))  # Download audio from provided URL
        end()  # Ask if user wants to continue
    
    elif user_option == '3':
        # Path configuration option selected
        user_path = input("\033[01;37m\t\tEnter the download path: \033[01;0m")
        print(root.download_path(user_path))  # Set or display download path
        end()  # Ask if user wants to continue

# Standard Python idiom to ensure main() runs only when script is executed directly
if __name__ == "__main__":
    main()