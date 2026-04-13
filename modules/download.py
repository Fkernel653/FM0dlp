"""
YouTube audio downloader using yt-dlp with FFmpeg post-processing.
"""

from dataclasses import dataclass
from pathlib import Path

from fake_useragent import UserAgent
import asyncio
from yt_dlp import YoutubeDL

from modules.add_metadata import add_metadata
from modules.colors import RESET, BOLD, GREEN, RED, MAGENTA

USER_AGENT = UserAgent().random


@dataclass
class Download:
    """Manages audio download operations from YouTube URLs."""

    urls: str
    this_file_folder = Path(__file__).parent
    config_file = Path(this_file_folder).parent / "config.json"

    def _validate_config_file(self) -> None:
        """Check if config file exists, exit if not found."""
        if not self.config_file.exists():
            print(
                f"{RED}\nConfig file not found! Please set download path first using 'config <path>'.{RESET}\n"
            )
            return exit(1)

    def _withdrawal_of_the_path(self) -> str:
        """Read and validate download path from config file."""
        import json

        with open(self.config_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                path = data.get("path")
                if not path or not Path(path).exists():
                    print(
                        f"{RED}\nDownload path '{path}' does not exist or is invalid. Please reconfigure.{RESET}\n"
                    )
                    return exit(1)
                return path
            except json.JSONDecodeError:
                print(f"{RED}\nConfig file is corrupted! Please reconfigure.{RESET}\n")
                return exit(1)

    async def classic(self, ffmpeg: str, codec: str, kbps: int, cookies: str):
        """Download audio using yt-dlp with FFmpeg processing (parallel)."""
        self._validate_config_file()

        opts = {
            "user_agent": USER_AGENT,
            "format": "bestaudio/best",
            "outtmpl": f"{self._withdrawal_of_the_path()}/%(title)s.%(ext)s",
            "writethumbnail": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": codec,
                    "preferredquality": str(kbps),
                },
                {"key": "EmbedThumbnail"},
            ],
            "cookiesfrombrowser": cookies if cookies else None,
            "quiet": False,
            "no_warnings": True,
        }

        loop = asyncio.get_event_loop()
        urls_list = self.urls.split()

        async def download_single_url(url: str):
            def sync_download():
                try:
                    with YoutubeDL(opts) as ydl:
                        info = ydl.extract_info(url, download=True)

                        if not info:
                            return f"{RED}\nFailed: {url}{RESET}"

                        base_filename = ydl.prepare_filename(info)
                        file_path = None

                        for ext in [codec, "mp3", "m4a", "opus", "flac"]:
                            test_path = Path(base_filename).with_suffix(f".{ext}")
                            if test_path.exists():
                                file_path = test_path
                                break

                        if not file_path or not file_path.exists():
                            return f"{RED}\nFile not found: {url}{RESET}\n"

                        title = info.get("title", "Unknown Title")
                        artist = info.get(
                            "uploader", info.get("channel", "Unknown Artist")
                        )
                        album = info.get("album", info.get("channel"))

                        add_metadata(
                            file=file_path,
                            codec=codec,
                            title=title,
                            artist=artist,
                            album=album,
                        )

                        return f"{GREEN}\n✓ Downloaded: {title}{RESET}\n"

                except Exception as e:
                    return f"{RED}\n✗ Error ({url}): {e}{RESET}\n"

            print(f"{MAGENTA}\nStarting: {RESET}{BOLD}{url}{RESET}\n")
            result = await loop.run_in_executor(None, sync_download)
            return result

        tasks = [download_single_url(url) for url in urls_list]

        for completed_task in asyncio.as_completed(tasks):
            try:
                result = await completed_task
                yield result
            except KeyboardInterrupt:
                yield f"{GREEN}\nDownload cancelled.{RESET}\n"
                break
