"""
Configuration manager for download paths.

This module handles persistent storage of the user's preferred download directory
using a JSON configuration file stored in the project root. It provides both
setter functionality (when a path is provided) and getter functionality
(when called without arguments).
"""

from pathlib import Path
from modules.colors import RESET, RED, GREEN
import json


def configuring_path(path: str) -> str:
    """
    Manage persistent storage location for downloaded audio files.

    This function acts as both a setter and getter for the download directory.
    - When a valid path is provided: saves it to config.json and confirms success
    - When an empty string or falsy value is provided: reads and displays current config

    Args:
        path (str): Directory path to save files. If empty or falsy, acts as getter
                   and returns the current configuration. If provided, acts as setter
                   and saves the path to config.json.

    Returns:
        str: Status message indicating either:
             - Success confirmation with config file location (setter mode)
             - Current configuration display with download directory (getter mode)

    Raises:
        SystemExit: Exits with code 1 in the following cases:
                    - Config file exists but saved path is invalid/missing
                    - Config file is corrupted (invalid JSON format)
                    - Config file doesn't exist (when in getter mode)

    Note:
        The configuration file is stored as 'config.json' in the project root
        directory (one level above the 'modules' folder). The file uses UTF-8
        encoding and pretty-printed JSON formatting for human readability.
    """
    # Determine configuration file location
    # Path structure: project_root/config.json
    # This module is at: project_root/modules/configer.py
    parent_folder = Path(__file__).parent
    config_file = Path(parent_folder).parent / "config.json"

    # SETTER MODE: User provided a path to save
    if path:
        # Build configuration object with metadata
        config = {
            "path": str(path),  # Convert Path object to string for JSON serialization
        }

        # Write configuration to filesystem with human-readable formatting
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(
                config,
                f,
                ensure_ascii=False,  # Allow Unicode characters in paths
                indent=4,  # Pretty print with 4-space indentation
            )

        # Confirm successful save with the config file location
        return f"{GREEN}Configuration saved successfully to: {RESET}{Path(config_file)}"

    # GETTER MODE: User wants to see current configuration
    else:
        if config_file.exists():
            # Attempt to read existing configuration file
            with open(config_file, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)  # Parse JSON from file
                    saved_path = data.get("path")

                    # Validate that the saved path actually exists on filesystem
                    if saved_path and Path(saved_path).exists():
                        return (
                            f"{GREEN}Current download directory: {RESET}{saved_path}\n"
                            f"{GREEN}Configuration file: {RESET}{Path(config_file)}"
                        )
                    else:
                        # Config exists but path is invalid (directory was moved/deleted)
                        print(
                            f"{RED}\nConfig file exists but the saved path is invalid or missing!\n{RESET}"
                        )
                        return exit(1)

                except json.JSONDecodeError:
                    # Config file is corrupted (invalid JSON syntax)
                    print(
                        f"{RED}\nConfig file is corrupted! Please reconfigure with 'config <path>'.\n{RESET}"
                    )
                    return exit(1)
        else:
            # No configuration file exists yet
            print(
                f"{RED}\nConfig file not found! Please set a download path first with 'config <path>'.\n{RESET}"
            )
            return exit(1)
