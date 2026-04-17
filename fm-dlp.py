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
    description="Search and download music from YouTube and SoundCloud",
)

helper = Help()


@fm_dlp.command()
def search(
    query: str,
    limit: int = 10,
    platform: Optional[str] = "yt-video",
):
    """
    Search for music on YouTube or SoundCloud.

    Args:
        query: Search term
        limit: Max results (default: 10)
        platform: "yt-video", "yt-music", or "soundcloud" (default: "yt-video")
    """
    from modules.search import Search

    program = Search(query, limit)

    match platform:
        case "yt-video":
            for video_info in program.yt_video():
                print(video_info)

        case "yt-music":
            for track_info in program.yt_music():
                print(track_info)

        case "soundcloud":
            for track_info in program.soundcloud():
                print(track_info)


@fm_dlp.command()
def download(
    urls: str,
    ffmpeg: Optional[str] = "True",
    codec: Optional[str] = "m4a",
    kbps: Optional[int] = 256,
    cookies: Optional[str] = None,
):
    """
    Download audio from YouTube URLs.

    Args:
        urls: Space-separated YouTube URLs
        ffmpeg: Use FFmpeg (default: "True")
        codec: Output format - m4a, mp3, opus, flac (default: "m4a")
        kbps: Bitrate in kbps (default: 256)
        cookies: Browser for cookies - chrome, firefox, edge, etc. (optional)
    """
    from modules.download import Download

    program = Download(urls)

    async def async_download_classic():
        async for result in program.classic(ffmpeg, codec, kbps, cookies):
            print(result)

    asyncio.run(async_download_classic())


@fm_dlp.command()
def config(path: str):
    """
    Set or display the download directory configuration.

    Args:q
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
