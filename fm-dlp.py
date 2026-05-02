"""
CLI entry point for fm-dlp using cyclopts library.
Commands: search, download, config
"""

import sys

from modules.colors import GREEN, RESET


def main():
    from typing import Optional

    from cyclopts import App

    fm_dlp = App(name="fm-dlp", version="1.7.0")

    @fm_dlp.command()
    def search(
        query: str,
        limit: int = 10,
        platform: Optional[str] = "yt-music",
        type: Optional[str] = "track",
        proxy: Optional[str] = None,
    ):
        """Search for music on YouTube."""
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
        """Download audio from YouTube URLs."""
        if codec is None:
            codec = "m4a" if sys.platform == "darwin" else "opus"

        from asyncio import run

        from modules.download import Download

        program = Download(urls, codec, kbps, quiet, max_concurrent, cookies, proxy)
        run(program.download_all())

    @fm_dlp.command()
    def config(path: str):
        """Set or display the download directory configuration."""
        from modules.configer import configer

        print(configer(path))

    fm_dlp()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{GREEN}Goodbye!{RESET}")
        sys.exit(0)
