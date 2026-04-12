"""
CLI entry point for fm-dlp using Clite library.
Commands: search, download, config, help
"""

from typing import Optional
import asyncio

from clite import Clite
from modules.configer import configuring_path
from modules.download import Download
from modules.help import message
from modules.search import Search

fm_dlp = Clite(
    name="fm-dlp",
    description="Search and download music from YouTube and SoundCloud",
)


@fm_dlp.command()
def search(
    query: str,
    limit: Optional[int] = 10,
    platform: Optional[str] = "yt-video",
):
    """
    Search for music on YouTube or SoundCloud.

    Args:
        query: Search term
        limit: Max results (default: 10)
        platform: "yt-video", "yt-music", or "soundcloud" (default: "yt-video")
    """
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
        codec: Output format - m4a, mp3, aac, opus, flac, wav (default: "m4a")
        kbps: Bitrate in kbps (default: 256)
        cookies: Browser for cookies - chrome, firefox, edge, etc. (optional)
    """
    program = Download(urls)

    async def async_download_classic():
        async for result in program.classic(ffmpeg, codec, kbps, cookies):
            print(result)

    asyncio.run(async_download_classic())


@fm_dlp.command()
def config(path: str):
    """
    Set or display the download directory configuration.

    Args:
        path: Directory path. If empty, displays current config.
    """
    print(configuring_path(path))


@fm_dlp.command()
def help():
    """Display the help menu."""
    print(message())


if __name__ == "__main__":
    fm_dlp()