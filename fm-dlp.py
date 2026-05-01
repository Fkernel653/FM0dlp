"""
CLI entry point for fm-dlp using cyclopts library.
Commands: search, download, config
"""

import sys
from typing import Optional

from cyclopts import App

from modules.colors import GREEN, RESET

fm_dlp = App(name="fm-dlp", version="1.5.3")


@fm_dlp.command()
def search(
    query: str,
    limit: int = 10,
    platform: Optional[str] = "yt-music",
    type: Optional[str] = "track",
    proxy: Optional[str] = None,
):
    """
    Search for music on YouTube.

    Args:
        query: Search for your query
        limit: Max results
        platform: "yt-video" or "yt-music"
        type: "track" or "album"
        proxy: Proxy URL (e.g., http://proxy:port or socks5://proxy:port)
    """
    try:
        from modules.search import Search
    except KeyboardInterrupt:
        print(f"\n{GREEN}Goodbye!{RESET}")
        sys.exit(0)

    program = Search(query, limit, type, proxy)

    match platform:
        case "yt-video":
            for video_info in program.yt_video():
                print(video_info)

        case "yt-music":
            for track_info in program.yt_music():
                print(track_info)


@fm_dlp.command()
def download(
    urls: str,
    codec: Optional[str] = None,
    kbps: Optional[int] = 256,
    quiet: Optional[bool] = False,
    max_concurrent: Optional[int] = 5,
    cookies: Optional[str] = None,
    proxy: Optional[str] = None,
):
    """
    Download audio from YouTube URLs.

    Args:
        urls: Space-separated YouTube URLs
        codec: Output format - m4a, mp3, opus, flac.
            Defaults to "m4a" on macOS, "opus" on other platforms.
        kbps: Bitrate in kbps
        quiet: Suppress yt-dlp output, showing only download progress and results
        max_concurrent: Maximum simultaneous downloads
        cookies: Browser to extract cookies from - chrome, firefox, edge, etc. (optional)
        proxy: Proxy URL (e.g., http://proxy:port or socks5://proxy:port)
    """
    if codec is None:
        codec = "m4a" if sys.platform == "darwin" else "opus"

    import asyncio

    try:
        from modules.download import Download
    except KeyboardInterrupt:
        print(f"\n{GREEN}Goodbye!{RESET}")
        sys.exit(0)

    program = Download(urls, codec, kbps, quiet, max_concurrent, cookies, proxy)

    async def async_download_classic():
        async for r in program:
            print(r)

    try:
        asyncio.run(async_download_classic())
    except KeyboardInterrupt:
        print(f"\n{GREEN}Download interrupted. Goodbye!{RESET}")
        sys.exit(0)


@fm_dlp.command()
def config(path: str):
    """
    Set or display the download directory configuration.

    Args:
        path: Directory path. If empty, displays current config.
    """
    try:
        from modules.configer import configer
    except KeyboardInterrupt:
        print(f"\n{GREEN}Goodbye!{RESET}")
        sys.exit(0)

    print(configer(path))


def main():
    try:
        fm_dlp()
    except KeyboardInterrupt:
        print(f"\n{GREEN}Goodbye!{RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()
