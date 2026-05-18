"""
CLI entry point for fm-dlp using cyclopts library.
Commands: search, download, config
"""

import sys

from modules.utils.colors import GREEN, RED, RESET


def main():
    from typing import Optional

    from cyclopts import App

    from modules.utils.validator import (
        AUDIO_CODECS,
        validate_input,
        validate_with_shutil,
    )

    fm_dlp = App(
        name="fm-dlp",
        version="2.3.3",
        help="fm-dlp is a CLI tool for searching YouTube/YTMusic and downloading audio/video from 1000+ platforms",
    )

    @fm_dlp.command()
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
        from modules.commands.search import Search

        try:
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

    @fm_dlp.command()
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
            # Set default codec
            if codec is None:
                codec = "m4a" if sys.platform == "darwin" else "opus"

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

    @fm_dlp.command()
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

    @fm_dlp.command()
    def update():
        """Update fm-dlp to the latest version via Git."""
        try:
            validate_with_shutil("git", "Git")
            from modules.utils.update import update_project

            print(update_project())
        except Exception as e:
            print(f"\n{RED}Update Error:{RESET} {e}")
            sys.exit(1)

    fm_dlp()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{GREEN}Goodbye!{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}Unexpected Error:{RESET} {e}")
        sys.exit(1)
