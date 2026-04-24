"""
CLI entry point for fm-dlp using Clite library.
Commands: search, download, config, help
"""

import sys
from typing import Optional
import asyncio

from clite import Clite
from modules.help import Help

fm_dlp = Clite(
    name="fm-dlp",
    description="Search and download music from YouTube",
)

helper = Help()


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
        query: Search term
        limit: Max results (default: 10)
        platform: "yt-video" or "yt-music" (default: "yt-music")
        type: "track" or "album" (default: "track")
        proxy: Proxy URL (e.g., http://proxy:port or socks5://proxy:port)
    """
    from modules.search import Search

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
        kbps: Bitrate in kbps (default: 256)
        quiet: Suppress yt-dlp output, showing only download progress and results (default: False)
        max_concurrent: Maximum simultaneous downloads (default: 5)
        cookies: Browser to extract cookies from - chrome, firefox, edge, etc. (optional)
        proxy: Proxy URL (e.g., http://proxy:port or socks5://proxy:port)
    """
    if codec is None:
        codec = "m4a" if sys.platform == "darwin" else "opus"

    from modules.download import Download

    program = Download(urls, codec, kbps, quiet, max_concurrent, cookies, proxy)

    async def async_download_classic():
        async for result in program.main():
            print(result)

    try:
        asyncio.run(async_download_classic())
    except KeyboardInterrupt:
        pass


@fm_dlp.command()
def config(path: str):
    """
    Set or display the download directory configuration.

    Args:
        path: Directory path. If empty, displays current config.
    """
    from modules.configer import configer

    print(configer(path))


@fm_dlp.command()
def help():
    """Display the help menu."""
    print(helper.command())


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(helper.file_run())
    else:
        fm_dlp()
