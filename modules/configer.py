# configer.py
"""
Persistent download path storage using JSON config file.
"""

from modules.colors import RESET, RED, GREEN
from pathlib import Path
import json


def configer(path: str) -> None:
    """
    Manage download directory storage.
    - With path: saves to config.json
    - Without path: displays current config
    """
    parent_folder = Path(__file__).parent
    config_file = Path(parent_folder).parent / "config.json"

    # Setter mode
    if path:
        config = {"path": str(path)}
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        return f"{GREEN}Configuration saved successfully to: {RESET}{Path(config_file)}"

    # Getter mode
    else:
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    saved_path = data.get("path")
                    if saved_path and Path(saved_path).exists():
                        return (
                            f"{GREEN}Current download directory: {RESET}{saved_path}\n"
                            f"{GREEN}Configuration file: {RESET}{Path(config_file)}"
                        )
                    else:
                        print(
                            f"{RED}\nConfig file exists but the saved path is invalid or missing!\n{RESET}"
                        )
                        return exit(1)
                except json.JSONDecodeError:
                    print(
                        f"{RED}\nConfig file is corrupted! Please reconfigure with 'config <path>'.\n{RESET}"
                    )
                    return exit(1)
        else:
            print(
                f"{RED}\nConfig file not found! Please set a download path first with 'config <path>'.\n{RESET}"
            )
            return exit(1)
