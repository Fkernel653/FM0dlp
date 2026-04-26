"""
YouTube audio downloader using yt-dlp with FFmpeg post-processing.
"""

from dataclasses import dataclass
from typing import AsyncGenerator, AsyncIterator
from yt_dlp import YoutubeDL
from pathlib import Path
import asyncio
import threading

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
        from shutil import which

        if which("ffmpeg") is None:
            print(f"{RED}FFmpeg not found in PATH! Please install FFmpeg.{RESET}")
            exit(1)
        if not self.config_file.exists():
            print(
                f"{RED}\nConfig file not found!{RESET}\n{YELLOW}Run: fm-dlp config /path/to/downloads{RESET}\n"
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
        except (JSONDecodeError, UnicodeDecodeError) as e:
            print(f"{RED}\nConfig file corrupted or has wrong encoding: {e}{RESET}\n")
            exit(1)
        except Exception as e:
            print(f"{RED}\nError reading config file: {e}{RESET}\n")
            exit(1)

    def _create_base_opts(self, extra=None):
        opts = {
            "proxy": self.proxy or None,
            "cookiesfrombrowser": self.cookies or None,
            "quiet": self.quiet,
            "no_warnings": True,
        }
        if extra:
            opts.update(extra)
        return opts

    def __aiter__(self) -> AsyncIterator[str]:
        return self._run()

    async def _run(self) -> AsyncGenerator[str, None]:
        download_path = self._get_download_path()
        loop = asyncio.get_event_loop()
        thread_local = threading.local()

        def _download_single(entry, url):
            thread_local.downloaded_file = None

            def hook(d):
                if d["status"] == "finished":
                    thread_local.downloaded_file = Path(d["info_dict"]["filepath"])

            title = entry.get("title", "")
            video_url = entry.get("webpage_url") or entry.get("url") or url
            opts = self._create_base_opts(
                {
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
                }
            )

            try:
                with YoutubeDL(opts) as ydl:
                    ydl.download([video_url])

                if not thread_local.downloaded_file:
                    return f"{RED}\n✗ {title} (file not found after download){RESET}"

                artist = entry.get("uploader") or entry.get("channel") or ""
                album = entry.get("album") or entry.get("channel") or ""
                add_metadata(
                    file=thread_local.downloaded_file,
                    codec=self.codec,
                    title=title,
                    artist=artist,
                    album=album,
                )
                return f"{GREEN}\n✓ {title}{RESET}"

            except Exception as e:
                return f"{RED}\n✗ {title} - {type(e).__name__}: {e}{RESET}"

        def _cancel_tasks(tasks):
            for task in tasks:
                if not task.done():
                    task.cancel()

        async def process_tasks(tasks, url_prefix=""):
            results = []
            try:
                for t in asyncio.as_completed(tasks):
                    result = await t
                    if result:
                        results.append(result)
                result_str = "\n".join(results) if results else f"{RED}\nNothing downloaded for {url_prefix}{RESET}"
                return result_str
            except asyncio.CancelledError:
                _cancel_tasks(tasks)
                await asyncio.gather(*tasks, return_exceptions=True)
                return f"{YELLOW}\n⚠ Download cancelled for {url_prefix}{RESET}"

        async def download_url(url: str) -> str:
            def _get_entries():
                try:
                    with YoutubeDL(self._create_base_opts()) as ydl:
                        info = ydl.extract_info(url, download=False)
                except Exception as e:
                    return (
                        None,
                        f"{RED}\nFailed to extract info for {url}: {type(e).__name__}: {e}{RESET}",
                    )

                if info is None:
                    return None, f"{RED}\nFailed to get video info for {url}{RESET}"
                entries = info.get("entries", [info])
                return [e for e in entries if e is not None], None

            try:
                print(f"{YELLOW}\nStarting: {RESET}{BOLD}{url}{RESET}")
                entries, error = await loop.run_in_executor(None, _get_entries)
                if error:
                    return error
                if not entries:
                    return f"{RED}\nNo valid entries to download for {url}{RESET}"

                sem = asyncio.Semaphore(self.max_concurrent)

                async def limited(entry):
                    async with sem:
                        return await loop.run_in_executor(
                            None, _download_single, entry, url
                        )

                tasks = [asyncio.create_task(limited(e)) for e in entries]
                return await process_tasks(tasks, url)

            except Exception as e:
                return f"{RED}\n✗ URL processing failed for {url}: {type(e).__name__}: {e}{RESET}"

        urls = [url.strip() for url in self.urls.split() if url.strip()]
        if not urls:
            yield f"{RED}\nNo URLs provided{RESET}"
            return

        tasks = [asyncio.create_task(download_url(u)) for u in urls]
        try:
            for t in asyncio.as_completed(tasks):
                try:
                    result = await t
                    yield result
                except asyncio.CancelledError:
                    _cancel_tasks(tasks)
                    await asyncio.gather(*tasks, return_exceptions=True)
                    break
                except Exception as e:
                    yield f"{RED}\n✗ Critical error: {type(e).__name__}: {e}{RESET}"
        finally:
            _cancel_tasks(tasks)
            await asyncio.gather(*tasks, return_exceptions=True)