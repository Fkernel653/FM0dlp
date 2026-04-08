"""
Main entry point for the fm-dlp CLI application using Clite library.
Commands: search, download, config, help
"""

from clite import Clite
import asyncio

from modules.search import Search
from modules.download import Download
from modules.configer import configuring_path
from modules.help import message


fm_dlp = Clite(
    name="fm-dlp",
    description="A utility for searching and downloading music from YouTube, based on yt-dlp",
)


@fm_dlp.command()
def search(
    query: str,
    limit: int = 10,
    variable: str = "yt-video",
):
    """
    Search for music on YouTube or SoundCloud.

    Args:
        query: Search term
        limit: Max results (default: 10)
        enable_filter: Filter invalid results - "True"/"False" (default: "False")
        variable: Platform - "youtube" or "soundcloud" (default: "youtube")
    """
    program = Search(query, limit)

    match variable:
        case "yt-video":
            for video_info in program.yt_video():
                print(video_info)

        case "yt-music":
            for track_info in program.yt_music():
                print(track_info)

        case "soundcloud":

            async def get_track_info():
                async for track_info in program.soundcloud():
                    print(track_info)

            asyncio.run(get_track_info())


@fm_dlp.command()
def download(
    url: str,
    ffmpeg: str = "True",
    codec: str = "m4a",
    kbps: int = 256,
    cookies: str = None,
):
    """
    Download audio from a YouTube video.

    Args:
        url: YouTube video URL
        ffmpeg: Use FFmpeg (reserved, default: "True")
        codec: Output format - m4a, mp3, aac, opus, wav (default: "m4a")
        kbps: Bitrate in kbps (default: 256)
        cookies: Browser for cookies - chrome, firefox, edge, etc. (optional)
    """
    program = Download(url)
    print(program.normal(ffmpeg, codec, kbps, cookies))


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
    """Display the help menu with usage instructions."""
    print(message())


if __name__ == "__main__":
    fm_dlp()
