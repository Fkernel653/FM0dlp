"""Configuration manager for download paths.

Handles persistent storage of the user's preferred download directory
using a JSON configuration file. Acts as both a setter (when path provided)
and getter (when called without arguments).
"""

from pathlib import (
    Path,
)  # Object-oriented filesystem paths that work on all operating systems
from modules.colors import RESET, RED, GREEN
import json  # JSON encoder/decoder for storing configuration data persistently


def configuring_path(path):
    """
    Manage persistent storage location for downloaded audio files.

    Acts as both setter and getter for the download directory.
    Configuration is stored in config.json in the application root.

    Args:
        path (str): Directory path to save files, or empty string to query current.

    Returns:
        str: Status message with current or newly set path location.

    Note:
        When path is empty, acts as getter and returns current configuration.
        When path is provided, acts as setter and saves to config.json.
        The function exits on errors (corrupted config, missing file) instead of returning.
    """
    # Configuration file location (same directory as script)
    # Navigate up from modules/configer.py to the project root
    parent_folder = Path(__file__).parent
    config_file = Path(parent_folder).parent / "config.json"

    # SETTER MODE: User provided a path to save
    if path:
        # Build configuration object with metadata
        config = {
            "path": str(
                path
            ),  # Convert Path object to string if needed for JSON serialization
        }

        # Write to filesystem with human-readable formatting
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(
                config, f, ensure_ascii=False, indent=4
            )  # Pretty print with indentation for readability

        # Confirm successful save with the config file location
        return f"{GREEN}Configuration saved successfully to: {RESET}{Path(config_file)}"

    # GETTER MODE: User wants to see current configuration
    else:
        if config_file.exists():
            # Attempt to read existing config
            with open(config_file, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)  # Parse JSON from file
                    # Extract path value using the correct key
                    saved_path = data.get("path")

                    # Validate that the saved path actually exists on filesystem
                    if saved_path and Path(saved_path).exists():
                        return (
                            f"{GREEN}Current download directory: {RESET}{saved_path}\n"
                            f"{GREEN}Configuration file: {RESET}{Path(config_file)}"
                        )
                    else:
                        # Config exists but path is invalid (directory deleted or moved)
                        print(
                            f"{RED}\nConfig file exists but the saved path is invalid or missing!\n{RESET}"
                        )
                        # Exit on error to prevent downloads to non-existent location
                        return exit(1)

                except json.JSONDecodeError:
                    # Config file is corrupted (invalid JSON format)
                    print(
                        f"{RED}\nConfig file is corrupted! Please reconfigure with 'config <path>'.\n{RESET}"
                    )
                    return exit(1)  # Exit on error
        else:
            # No config file exists yet
            print(
                f"{RED}\nConfig file not found! Please set a download path first with 'config <path>'.\n{RESET}"
            )
            return exit(1)  # Exit on error
