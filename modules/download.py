"""
YouTube audio downloader using yt-dlp with FFmpeg post-processing.
"""

from dataclasses import dataclass
from typing import AsyncGenerator
from yt_dlp import YoutubeDL
from pathlib import Path
import asyncio

from modules.colors import RESET, BOLD, RED, GREEN, YELLOW
from modules.add_metadata import add_metadata


@dataclass
class Download:
    """Manages audio download operations from YouTube URLs."""

    urls: str
    codec: str
    kbps: int
    quiet: bool
    max_concurrent: int
    cookies: str
    proxy: str

    config_file = Path(__file__).parent.parent / "config.json"

    def __post_init__(self):
        self._validate_ffmpeg()
        self._validate_config_file()

    def _validate_ffmpeg(self):
        from shutil import which

        if which("ffmpeg") is None:
            print(f"{RED}FFmpeg not found in PATH! Please install FFmpeg.{RESET}")
            exit(1)

    def _validate_config_file(self):
        if not self.config_file.exists():
            print(
                f"{RED}\nConfig file not found!{RESET}\n"
                f"{YELLOW}Run: fm-dlp config /path/to/downloads{RESET}\n"
            )
            exit(1)

    def _get_download_path(self):
        from json import loads, JSONDecodeError

        try:
            data = loads(self.config_file.read_text(encoding="utf-8"))
            path = data.get("path")
            if not path or not Path(path).exists():
                print(f"{RED}\nDownload path '{path}' does not exist.{RESET}\n")
                exit(1)
            return path
        except JSONDecodeError:
            print(f"{RED}\nConfig file corrupted!{RESET}\n")
            exit(1)

    async def main(self) -> AsyncGenerator[str, None]:
        download_path = self._get_download_path()
        loop = asyncio.get_event_loop()

        def _download_single(entry, url):
            """Download a single entry (video/song) and return result message."""
            downloaded_file = None

            def hook(d):
                nonlocal downloaded_file
                if d["status"] == "finished":
                    downloaded_file = Path(d["info_dict"]["filepath"])

            title = entry.get("title", "Unknown")
            video_url = entry.get("webpage_url") or entry.get("url") or url

            opts = {
                "proxy": self.proxy or None,
                "format": "bestaudio/best",
                "outtmpl": f"{download_path}/%(title)s.%(ext)s",
                "writethumbnail": True,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": self.codec,
                        "preferredquality": str(self.kbps),
                    },
                    {"key": "EmbedThumbnail"},
                ],
                "postprocessor_hooks": [hook],
                "cookiesfrombrowser": self.cookies or None,
                "quiet": self.quiet,
                "no_warnings": True,
            }

            try:
                with YoutubeDL(opts) as ydl:
                    ydl.download([video_url])

                if downloaded_file:
                    artist = entry.get("uploader") or entry.get("channel") or "Unknown"
                    album = entry.get("album") or entry.get("channel") or "Unknown"
                    try:
                        add_metadata(
                            file=downloaded_file,
                            codec=self.codec,
                            title=title,
                            artist=artist,
                            album=album,
                        )
                        return f"{GREEN}\n✓ {title}{RESET}"
                    except Exception as e:
                        return f"{YELLOW}\n⚠ {title} (metadata: {e}){RESET}"
                else:
                    return f"{RED}\n✗ {title} (file not found){RESET}"
            except Exception as e:
                return f"{RED}\n✗ {title} - {e}{RESET}"

        async def download_url(url: str) -> str:
            def _get_entries():
                try:
                    with YoutubeDL(
                        {
                            "proxy": self.proxy or None,
                            "cookiesfrombrowser": self.cookies or None,
                            "quiet": self.quiet,
                            "no_warnings": True,
                        }
                    ) as ydl:
                        info = ydl.extract_info(url, download=False)
                except Exception as e:
                    return None, f"{RED}\nFailed to extract info: {e}{RESET}"

                if not info:
                    return None, f"{RED}\nFailed to get video info{RESET}"

                entries = info.get("entries", [info])
                return entries, None

            print(f"{YELLOW}\nStarting: {RESET}{BOLD}{url}{RESET}")
            entries, error = await loop.run_in_executor(None, _get_entries)

            if error:
                return error

            if not entries:
                return f"{RED}\nNothing to download{RESET}"

            sem = asyncio.Semaphore(self.max_concurrent)

            async def limited(entry):
                async with sem:
                    return await loop.run_in_executor(
                        None, _download_single, entry, url
                    )

            tasks = [asyncio.create_task(limited(e)) for e in entries if e]
            results = []
            for t in asyncio.as_completed(tasks):
                results.append(await t)

            return (
                "\n".join(results) if results else f"{RED}\nNothing downloaded{RESET}"
            )

        urls = self.urls.split()
        if not urls:
            yield f"{RED}\nNo URLs provided{RESET}"
            return

        tasks = [asyncio.create_task(download_url(u)) for u in urls]
        for t in asyncio.as_completed(tasks):
            yield await t
