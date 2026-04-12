# help.py
"""
Help menu display module for fm-dlp CLI.

This module generates a formatted help message with all available commands,
options, examples, and requirements. The help text is dynamically built to
match the current implementation of search, download, and config commands.
"""

from modules.colors import RESET, BOLD, GREEN, CYAN, YELLOW, MAGENTA, GRAY


def message() -> str:
    """Generate and return the complete help menu text.
    
    Returns:
        str: Formatted help message with command descriptions, options,
             examples, and system requirements.
    """
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
        {CYAN}--limit=<n>{RESET}        {GRAY}Number of results to show (default: 10){RESET}
        {CYAN}--platform=<platform>{RESET}  {GRAY}Platform: yt-video, yt-music, soundcloud (default: yt-video){RESET}
    {GRAY}Note:{RESET} {GRAY}'all' platform is currently not implemented; use specific platform instead.{RESET}
    {GRAY}Examples:{RESET}
        {CYAN}fm-dlp search "Sewerslvt"{RESET}
        {CYAN}fm-dlp search "usedcvnt" --limit=10 --platform=yt-music{RESET}
        {CYAN}fm-dlp search "tokyona" --platform=yt-video --limit=3{RESET}
        {CYAN}fm-dlp search "drum and bass" --platform=soundcloud --limit=5{RESET}

{BOLD}{YELLOW}download <urls> [--ffmpeg=<bool>] [--codec=<format>] [--kbps=<bitrate>] [--cookies=<browser>]{RESET}
    {GRAY}Download audio from one or more YouTube URLs (space-separated).{RESET}
    {GRAY}Supports parallel downloads and automatic metadata embedding.{RESET}
    {GRAY}Options:{RESET}
        {CYAN}--ffmpeg=<bool>{RESET}     {GRAY}Enable FFmpeg processing (default: "True"){RESET}
        {CYAN}--codec=<format>{RESET}    {GRAY}Output format: m4a, mp3, aac, opus, flac, wav (default: m4a){RESET}
        {CYAN}--kbps=<bitrate>{RESET}    {GRAY}Bitrate quality: 64-320 (default: 256){RESET}
        {CYAN}--cookies=<browser>{RESET} {GRAY}Browser for cookies: chrome, firefox, edge, safari (optional){RESET}
    {GRAY}Examples:{RESET}
        {CYAN}fm-dlp download https://youtu.be/dWn5DBo33ds{RESET}
        {CYAN}fm-dlp download "https://youtu.be/abc123 https://youtu.be/def456" --codec=mp3 --kbps=320{RESET}
        {CYAN}fm-dlp download https://music.youtube.com/... --codec=flac --cookies=firefox{RESET}

{BOLD}{YELLOW}config <path>{RESET}
    {GRAY}Set or display the download directory configuration.{RESET}
    {GRAY}If path is empty, displays current config from config.json.{RESET}
    {GRAY}Examples:{RESET}
        {CYAN}fm-dlp config ~/Music{RESET}
        {CYAN}fm-dlp config{RESET}              {GRAY}# Show current config path{RESET}

{BOLD}{YELLOW}help{RESET}
    {GRAY}Display this detailed help message.{RESET}

{BOLD}{GREEN}SUPPORTED FORMATS & METADATA:{RESET}
    {GRAY}• {RESET}{BOLD}M4A/AAC{RESET} {GRAY}(iTunes-style metadata: title, artist, album){RESET}
    {GRAY}• {RESET}{BOLD}MP3{RESET}       {GRAY}(ID3 tags: TIT2, TPE1, TALB){RESET}
    {GRAY}• {RESET}{BOLD}FLAC{RESET}      {GRAY}(Vorbis comments){RESET}
    {GRAY}• {RESET}{BOLD}Opus{RESET}      {GRAY}(Ogg container with metadata){RESET}

{BOLD}{GREEN}REQUIREMENTS:{RESET}
    {GRAY}• {RESET}{BOLD}FFmpeg{RESET}      {GRAY}(Required for audio conversion and thumbnail embedding){RESET}
    {GRAY}• {RESET}{BOLD}yt-dlp{RESET}      {GRAY}(Required for YouTube downloads and search){RESET}
    {GRAY}• {RESET}{BOLD}ytmusicapi{RESET}  {GRAY}(Required for YouTube Music search){RESET}
    {GRAY}• {RESET}{BOLD}soundcloud-lib{RESET} {GRAY}(Required for SoundCloud search){RESET}
    {GRAY}• {RESET}{BOLD}Python 3.8+{RESET} {GRAY}(Required runtime){RESET}
    {GRAY}• {RESET}{BOLD}fake-useragent{RESET} {GRAY}(For realistic HTTP headers){RESET}
    {GRAY}• {RESET}{BOLD}mutagen{RESET}     {GRAY}(For metadata embedding){RESET}

{BOLD}{GREEN}NOTES:{RESET}
    {GRAY}• {RESET}Configuration is stored in {BOLD}config.json{RESET} {GRAY}next to the executable.{RESET}
    {GRAY}• {RESET}The download command supports multiple space-separated URLs with parallel async downloads.{RESET}
    {GRAY}• {RESET}Metadata is automatically added to all supported formats except WAV.{RESET}
    {GRAY}• {RESET}Thumbnails are embedded automatically when available via yt-dlp.{RESET}
    {GRAY}• {RESET}Cookies from browser can help bypass age restrictions or region blocks.{RESET}
    {GRAY}• {RESET}If config.json is missing or invalid, download will exit with an error.{RESET}

{BOLD}{GREEN}EXAMPLES:{RESET}
    {GRAY}1. Search on YouTube video and download the first result:{RESET}
       {CYAN}fm-dlp search "breakcore" --limit=3 --platform=yt-video{RESET}
       {CYAN}fm-dlp download <URL_FROM_SEARCH>{RESET}

    {GRAY}2. High quality MP3 download from multiple URLs:{RESET}
       {CYAN}fm-dlp download "URL1 URL2 URL3" --codec=mp3 --kbps=320{RESET}

    {GRAY}3. Lossless FLAC with custom download path:{RESET}
       {CYAN}fm-dlp config ~/Music{RESET}
       {CYAN}fm-dlp download https://youtu.be/example --codec=flac{RESET}

    {GRAY}4. Search only YouTube Music for a track:{RESET}
       {CYAN}fm-dlp search "de kini" --platform=yt-music --limit=5{RESET}

    {GRAY}5. Download with browser cookies to access age-restricted content:{RESET}
       {CYAN}fm-dlp download https://youtu.be/restricted --cookies=chrome{RESET}

    {GRAY}6. Search SoundCloud for ambient mixes:{RESET}
       {CYAN}fm-dlp search "ambient mix" --platform=soundcloud --limit=10{RESET}

{BOLD}{MAGENTA}For issues, bugs, or feature requests, please report on GitHub.{RESET}
{BOLD}{MAGENTA}Repository: https://github.com/Fkernel653/fm-dlp{RESET}
"""