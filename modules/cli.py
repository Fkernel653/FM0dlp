import sys

from color_kiss import GREEN, RED, RESET


def get_version() -> str:
    """Get version from installed package metadata."""
    try:
        from importlib.metadata import version

        return version("fm-dlp")
    except Exception:
        return "unknown"


def main():
    from typing import Optional

    from cliss import CLI

    app = CLI(
        name="fm-dlp",
        description="fm-dlp is a CLI tool for searching YouTube/YTMusic and downloading audio/video from 1000+ platforms",
        version=get_version(),
    )

    @app.command()
    def search(
        query: str,
        limit: int = 10,
        platform: Optional[str] = "yt-music",
        type: Optional[str] = "track",
        proxy: Optional[str] = None,
    ):
        """Search for music tracks or videos on YouTube/YTMusic.

        Args:
            query: Search query string for finding tracks or videos.
            limit: Maximum number of search results to return. Defaults to 10.
            platform: Platform to search on. Options: 'yt-music' for YouTube Music
                or 'yt-video' for YouTube videos. Defaults to 'yt-music'.
            type: Type of content to search for. Defaults to 'track'.
            proxy: Optional proxy URL for making requests.
                Must be an HTTP proxy when platform is 'yt-music'.

        Raises:
            SystemExit: If validation fails or search encounters an error.
        """
        try:
            from modules.commands.search import Search
            from modules.utils.validator import validate_input

            validate_input(
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
        max_concurrent: int = 5,
        quiet: Optional[bool] = False,
        metadata: Optional[bool] = True,
        cookies: Optional[str] = None,
        proxy: Optional[str] = None,
    ):
        """Download audio or video content from supported platforms.

        Downloads media files from provided URLs with configurable codec,
        quality, and concurrency settings. Supports metadata embedding
        and proxy configuration.

        Args:
            urls: One or more URLs to download from, separated by commas or spaces.
            codec: Audio/video codec for the downloaded file.
                If None, uses default codec. Common audio codecs: 'mp3', 'flac', 'wav'.
            kbps: Audio bitrate in kbps. Defaults to 256.
            max_concurrent: Maximum number of concurrent downloads. Defaults to 5.
            quiet: Suppress progress output if True. Defaults to False.
            metadata: Embed metadata into downloaded files if True.
                Defaults to True. Automatically disabled for WAV format.
            cookies: Path to cookies file for authenticated downloads.
            proxy: Optional proxy URL for download requests.

        Note:
            WAV format does not support metadata embedding.
            FFmpeg is required for audio codec processing.

        Raises:
            SystemExit: If validation fails, FFmpeg is missing, or download fails.
        """
        try:
            from modules.utils.validator import (
                AUDIO_CODECS,
                DEFAULT_CODEC,
                validate_input,
                validate_with_shutil,
            )

            if codec is None:
                codec = DEFAULT_CODEC

            validate_input(
                url=urls,
                codec=codec,
                kbps=kbps,
                max_concurrent=max_concurrent,
                proxy=proxy,
            )

            if codec in AUDIO_CODECS:
                validate_with_shutil("ffmpeg", "FFmpeg")

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
        """Configure the application settings path.

        Sets the configuration directory path for storing application
        settings and data files.

        Args:
            path: Directory path where configuration files will be stored.

        Raises:
            SystemExit: If configuration operation fails.
        """
        try:
            from modules.utils.configer import set_path

            print(set_path(path))
        except Exception as e:
            print(f"\n{RED}Configuration Error:{RESET} {e}")
            sys.exit(1)

    app.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{GREEN}Goodbye!{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}Unexpected Error:{RESET} {e}")
        sys.exit(1)
