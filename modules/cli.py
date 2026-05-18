"""
CLI entry point for fm-dlp using cyclopts library.
Commands: search, download, config
"""

import sys

from modules.utils.colors import GREEN, RED, RESET


def get_version() -> str:
    """Get version from installed package metadata."""
    try:
        from importlib.metadata import version

        return version("fm-dlp")
    except Exception:
        return "unknown"


def main():
    from typing import Optional

    from cyclopts import App

    app = App(
        name="fm-dlp",
        version=get_version(),
        help="fm-dlp is a CLI tool for searching YouTube/YTMusic and downloading audio/video from 1000+ platforms",
    )

    @app.command()
    def search(
        query: str,
        limit: int = 10,
        platform: str = "yt-music",
        type: str = "track",
        proxy: Optional[str] = None,
    ):
        """Search for music on YouTube.

        Args:
            query: Search query string.
            limit: Number of results to return.
            platform: Search platform ('yt-video' or 'yt-music').
            type: Content type ('track' or 'album').
            proxy: Proxy URL.
                yt-video: http, https, socks4, socks5, socks5h
                yt-music: http, https only
                Example: 'socks5://127.0.0.1:9050'
        """
        try:
            from modules.commands.search import Search
            from modules.utils.validator import validate_input

            validate_input(
                limit=limit,
                platform=platform,
                type=type,
                proxy=proxy,
                proxy_only_http=(platform == "yt-music"),
            )

            program = Search(query, limit, type, proxy)

            match platform:
                case "yt-video":
                    for video_info in program.yt_video():
                        print(video_info)
                case "yt-music":
                    for track_info in program.yt_music():
                        print(track_info)

        except Exception as e:
            print(f"\n{RED}Search Error:{RESET} {e}")
            sys.exit(1)

    @app.command()
    def download(
        urls: str,
        codec: Optional[str] = None,
        kbps: int = 256,
        quiet: bool = False,
        max_concurrent: int = 5,
        metadata: bool = True,
        cookies: Optional[str] = None,
        proxy: Optional[str] = None,
    ):
        """Download audio or video from URLs.

        Args:
            urls: URL(s) - space or comma separated.
            codec: Audio codec or video container.
                Audio: mp3, aac, flac, m4a, opus, vorbis, wav
                Video: mp4, mkv, webm, mov, avi, flv
                Default: 'm4a' on macOS, 'opus' otherwise.
            kbps: Audio bitrate in kbps (64-320). Ignored for video.
            quiet: Suppress yt-dlp output.
            max_concurrent: Maximum parallel downloads.
            metadata: Embed metadata and thumbnail (audio only).
            cookies: Browser for cookies (chrome, firefox, edge, etc.).
            proxy: Proxy URL (http, https, socks4, socks5, socks5h).
        """
        try:
            from modules.utils.validator import (
                AUDIO_CODECS,
                DEFAULT_CODEC,
                validate_input,
                validate_with_shutil,
            )

            # Set default codec
            if codec is None:
                codec = DEFAULT_CODEC

            # Validate inputs
            validate_input(
                url=urls,
                codec=codec,
                kbps=kbps,
                max_concurrent=max_concurrent,
                proxy=proxy,
            )

            # Check ffmpeg only for audio codecs
            if codec in AUDIO_CODECS:
                validate_with_shutil("ffmpeg", "FFmpeg")

            # WAV doesn't support metadata
            if codec == "wav" and metadata:
                metadata = False
                print(
                    f"{GREEN}Note:{RESET} WAV format doesn't support metadata embedding"
                )

            import asyncio

            from modules.commands.download import Download

            async def run_download():
                async with Download(
                    urls, codec, kbps, quiet, max_concurrent, metadata, cookies, proxy
                ) as downloader:
                    await downloader.download_all()

            asyncio.run(run_download())

        except Exception as e:
            print(f"\n{RED}Download Error:{RESET} {e}")
            sys.exit(1)

    @app.command()
    def config(path: str):
        """Set or display the download directory.

        Args:
            path: Directory path for downloads. Empty to show current.
        """
        try:
            from modules.utils.configer import set_path

            print(set_path(path))
        except Exception as e:
            print(f"\n{RED}Configuration Error:{RESET} {e}")
            sys.exit(1)

    app()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{GREEN}Goodbye!{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}Unexpected Error:{RESET} {e}")
        sys.exit(1)
