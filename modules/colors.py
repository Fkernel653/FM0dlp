"""ANSI color codes for terminal output formatting.

These constants provide consistent color styling across all modules.
Each code is an ANSI escape sequence that changes text appearance
in compatible terminals. Colors are used to distinguish different
types of information in the output.
"""

# Reset all formatting to default (removes all styles and colors)
RESET = "\033[01;0m"

# Text styles
BOLD = "\033[01;1m"  # Bold/Bright text - used for numbers and URLs
ITALIC = "\033[01;3m"  # Italic text (may not work in all terminals)

# Standard colors - each used consistently across the application
RED = "\033[01;31m"  # Error messages, warnings, and video URLs
GREEN = "\033[01;32m"  # Success messages, confirmations, and goodbye messages
YELLOW = "\033[01;33m"  # Warnings and cautions (reserved for future use)
BLUE = "\033[01;34m"  # Information and dates (creation dates)
MAGENTA = "\033[01;35m"  # Metadata and channel names
CYAN = "\033[01;36m"  # Titles and headings (video titles)
