"""
ANSI color codes for terminal output formatting.

These constants provide consistent color styling across all modules of the application.
Each code is an ANSI escape sequence that changes text appearance in compatible terminals.
Colors are used to distinguish different types of information in the output, improving
readability and user experience.

Usage Example:
    from modules.colors import RED, GREEN, RESET
    print(f"{RED}Error message{RESET}")
    print(f"{GREEN}Success message{RESET}")

Note:
    - These escape sequences work on most Unix-like terminals (Linux, macOS)
    - Windows terminals: require ANSI support (Windows 10 version 1511+ with VT sequences enabled)
      Older Windows versions may not display colors correctly.
    - Not all terminals support the ITALIC style (e.g., basic consoles may ignore it)
    - Always use RESET after applying colors to prevent formatting from affecting subsequent output
"""

# Reset all formatting to default (removes all styles and colors)
# This should be used after applying any color or style to prevent bleeding
RESET = "\033[01;0m"

# Text styles - these modify the appearance regardless of color
BOLD = "\033[01;1m"  # Makes text thicker/brighter
ITALIC = "\033[01;3m"  # Slanted text (may not render in all terminals)

# Standard colors - each used consistently across the application
RED = "\033[01;31m"  # Error messages, warnings, URLs
GREEN = "\033[01;32m"  # Success messages, confirmations
YELLOW = "\033[01;33m"  # Warnings, non-critical notices
BLUE = "\033[01;34m"  # Informational messages
MAGENTA = "\033[01;35m"  # Alternative highlight color
CYAN = "\033[01;36m"  # Search result numbering, section headers
GRAY = "\033[01;90m"  # Metadata labels, decorative characters (├─ └─)
