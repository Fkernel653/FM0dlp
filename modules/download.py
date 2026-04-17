"""
YouTube audio downloader using yt-dlp with FFmpeg post-processing.
"""

from dataclasses import dataclass
from pathlib import Path
import asyncio
from yt_dlp import YoutubeDL

from modules.add_metadata import add_metadata
from modules.colors import RESET, BOLD, RED, GREEN, YELLOW, MAGENTA


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
            exit(1)

    def _withdrawal_of_the_path(self) -> str:
        """Read and validate download path from config file."""
        import json

        try:
            data = json.loads(self.config_file.read_text(encoding="utf-8"))
            path = data.get("path")
            if not path or not Path(path).exists():
                print(
                    f"{RED}\nDownload path '{path}' does not exist or is invalid. Please reconfigure.{RESET}\n"
                )
                exit(1)
            return path
        except json.JSONDecodeError:
            print(f"{RED}\nConfig file is corrupted! Please reconfigure.{RESET}\n")
            exit(1)

    async def classic(self, ffmpeg: str, codec: str, kbps: int, cookies: str, proxy: str):
        """Download audio using yt-dlp with FFmpeg processing (parallel)."""
        self._validate_config_file()

        opts = {
            "proxy": proxy if proxy else None,
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

        tasks = []

        async def download_single_url(url: str):
            def sync_download():
                try:
                    with YoutubeDL(opts) as ydl:
                        info = ydl.extract_info(url, download=True)

                        if not info:
                            return f"{RED}\nFailed to extract info: {url}{RESET}"

                        file_path = None
                        if (
                            "requested_downloads" in info
                            and info["requested_downloads"]
                        ):
                            file_path = Path(info["requested_downloads"][0]["filepath"])
                        else:
                            base = ydl.prepare_filename(info)
                            for ext in [codec, "m4a", "mp3", "flac", "opus"]:
                                test = Path(base).with_suffix(f".{ext}")
                                if test.exists():
                                    file_path = test
                                    break

                        if not file_path or not file_path.exists():
                            return f"{RED}\nFile not found after download: {url}{RESET}"

                        title = info.get("title", "")
                        channel = info.get("channel", "")
                        artist = info.get("uploader") or channel
                        album = info.get("album") or channel

                        try:
                            add_metadata(
                                file=file_path,
                                codec=codec,
                                title=title,
                                artist=artist,
                                album=album,
                            )
                        except Exception as meta_err:
                            return f"{YELLOW}\n⚠ Downloaded but metadata failed: {title} - {meta_err}{RESET}"

                        return f"{GREEN}\n✓ Downloaded: {title}{RESET}"

                except Exception as e:
                    return f"{RED}\n✗ Error ({url}): {e}{RESET}"

            print(f"{MAGENTA}\nStarting: {RESET}{BOLD}{url}{RESET}")
            result = await loop.run_in_executor(None, sync_download)
            return result

        tasks = [asyncio.create_task(download_single_url(url)) for url in urls_list]

        try:
            for completed_task in asyncio.as_completed(tasks):
                result = await completed_task
                yield result
        except KeyboardInterrupt:
            for task in tasks:
                if not task.done():
                    task.cancel()
            yield f"{GREEN}\nDownload cancelled by user.{RESET}"
        except Exception as e:
            yield f"{RED}\nUnexpected error: {e}{RESET}"
