# help.py
"""
Help menu display module for fm-dlp CLI.
"""

from modules.colors import RESET, BOLD, GREEN, CYAN, YELLOW, MAGENTA, GRAY


def message() -> str:
    """Generate the help menu text with all available commands and options."""
    return f"""
{BOLD}{GREEN}DESCRIPTION:{RESET}
    {GRAY}A powerful CLI tool to search and download music from YouTube, YouTube Music,{RESET}
    {GRAY}and SoundCloud with automatic metadata embedding and format conversion.{RESET}

{BOLD}{GREEN}USAGE:{RESET}
    {BOLD}fm-dlp <command> [arguments] [options]{RESET}

{BOLD}{GREEN}COMMANDS:{RESET}

{BOLD}{YELLOW}search <query> [--limit=<n>] [--platform=<platform>]{RESET}
    {GRAY}Search for music across YouTube, YouTube Music, and SoundCloud{RESET}
    {GRAY}Options:{RESET}
        {CYAN}--limit=<n>{RESET}        {GRAY}Number of results to show (default: 5){RESET}
        {CYAN}--platform=<platform>{RESET}  {GRAY}Filter by platform: youtube, ytmusic, soundcloud{RESET}
    {GRAY}Examples:{RESET}
        {CYAN}fm-dlp search "Sewerslvt"{RESET}
        {CYAN}fm-dlp search "usedcvnt" --limit=10{RESET}
        {CYAN}fm-dlp search "tokyona" --platform=yt-video --limit=3{RESET}

{BOLD}{YELLOW}download <url> [--ffmpeg=<bool>] [--codec=<format>] [--kbps=<bitrate>] [--cookies=<browser>]{RESET}
    {GRAY}Download audio from a URL with optional format conversion{RESET}
    {GRAY}Options:{RESET}
        {CYAN}--ffmpeg=<bool>{RESET}     {GRAY}Enable FFmpeg processing (default: True){RESET}
        {CYAN}--codec=<format>{RESET}    {GRAY}Audio format: m4a, aac, mp3, flac, opus (default: m4a){RESET}
        {CYAN}--kbps=<bitrate>{RESET}    {GRAY}Bitrate quality: 64-320 (default: 256){RESET}
        {CYAN}--cookies=<browser>{RESET} {GRAY}Browser for cookies: chrome, firefox, edge, safari{RESET}
    {GRAY}Examples:{RESET}
        {CYAN}fm-dlp download https://youtu.be/dWn5DBo33ds{RESET}
        {CYAN}fm-dlp download https://youtu.be/... --codec=mp3 --kbps=320{RESET}
        {CYAN}fm-dlp download https://music.youtube.com/... --codec=flac --cookies=firefox{RESET}

{BOLD}{YELLOW}config <path>{RESET}
    {GRAY}Set or display the download directory path{RESET}
    {GRAY}Examples:{RESET}
        {CYAN}fm-dlp config ~/Music{RESET}
        {CYAN}fm-dlp config{RESET}              {GRAY}# Show current config{RESET}

{BOLD}{YELLOW}help{RESET}
    {GRAY}Display this detailed help message{RESET}

{BOLD}{YELLOW}version{RESET}
    {GRAY}Show version information{RESET}

{BOLD}{GREEN}SUPPORTED FORMATS & METADATA:{RESET}
    {GRAY}• {RESET}{BOLD}M4A{RESET} {GRAY}(iTunes-style metadata: title, artist, album){RESET}
    {GRAY}• {RESET}{BOLD}AAC{RESET}       {GRAY}(iTunes-style metadata in M4A container){RESET}
    {GRAY}• {RESET}{BOLD}MP3{RESET}       {GRAY}(ID3 tags: TIT2, TPE1, TALB){RESET}
    {GRAY}• {RESET}{BOLD}FLAC{RESET}      {GRAY}(Vorbis comments){RESET}
    {GRAY}• {RESET}{BOLD}Opus{RESET}      {GRAY}(Ogg container with metadata){RESET}

{BOLD}{GREEN}REQUIREMENTS:{RESET}
    {GRAY}• {RESET}{BOLD}FFmpeg{RESET}      {GRAY}(Required for audio conversion and thumbnail embedding){RESET}
    {GRAY}• {RESET}{BOLD}yt-dlp{RESET}      {GRAY}(Required for YouTube downloads){RESET}
    {GRAY}• {RESET}{BOLD}Python 3.8+{RESET} {GRAY}(Required runtime){RESET}

{BOLD}{GREEN}EXAMPLES:{RESET}
    {GRAY}1. Search and then download:{RESET}
       {CYAN}fm-dlp search "breakcore" --limit=3{RESET}
       {CYAN}fm-dlp download <YOUR_URL>{RESET}

    {GRAY}2. High quality MP3 download:{RESET}
       {CYAN}fm-dlp download <YOUR_URL> --codec=mp3 --kbps=320{RESET}

    {GRAY}3. Lossless FLAC with custom download path:{RESET}
       {CYAN}fm-dlp config ~/Music{RESET}
       {CYAN}fm-dlp download <YOUR_URL> --codec=flac{RESET}

    {GRAY}4. WAV lossless download:{RESET}
       {CYAN}fm-dlp download <YOUR_URL> --codec=wav{RESET}

{BOLD}{MAGENTA}For issues, bugs, or feature requests, please report on GitHub.{RESET}
{BOLD}{MAGENTA}Repository: https://github.com/Fkernel653/fm-dlp{RESET}
"""