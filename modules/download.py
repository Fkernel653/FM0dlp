"""
Async YouTube audio downloader using yt-dlp.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field

from modules.colors import GREEN, RED, RESET, YELLOW


@dataclass
class Download:
    urls: str
    codec: str
    kbps: int
    quiet: bool
    max_concurrent: int
    cookies: str
    proxy: str

    _executor: ThreadPoolExecutor = field(init=False, repr=False)

    def __post_init__(self):
        from json import loads
        from pathlib import Path
        from shutil import which

        if which("ffmpeg") is None:
            exit(f"{RED}FFmpeg not found in PATH!{RESET}")

        config_file = Path(__file__).parent.parent / "config.json"
        if not config_file.exists():
            exit(f"{RED}Config file not found! Run: fm-dlp config /path{RESET}")

        data = loads(config_file.read_text(encoding="utf-8"))
        self.download_path = data.get("path")
        if not self.download_path or not Path(self.download_path).exists():
            exit(f"{RED}Download path does not exist.{RESET}")

        self._executor = ThreadPoolExecutor(max_workers=self.max_concurrent)

    def _get_opts(self) -> dict:
        opts = {
            "quiet": self.quiet,
            "no_warnings": True,
            "format": "bestaudio/best",
            "outtmpl": f"{self.download_path}/%(title)s.%(ext)s",
            "concurrent_fragment_downloads": self.max_concurrent,
            "embedmetadata": True,
            "writethumbnail": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": self.codec,
                    "preferredquality": str(self.kbps),
                },
                {"key": "FFmpegMetadata"},
                {"key": "EmbedThumbnail"},
            ],
        }
        if self.proxy:
            opts["proxy"] = self.proxy
        if self.cookies:
            opts["cookiesfrombrowser"] = self.cookies

        return opts

    async def download_all(self):
        urls = [u.strip() for u in self.urls.replace(",", " ").split() if u.strip()]
        if not urls:
            return

        sem = asyncio.Semaphore(self.max_concurrent)

        async def download_one(url: str):
            async with sem:
                return await self._download_url(url)

        tasks = [download_one(url) for url in urls]
        results = await asyncio.gather(*tasks)

        for result in results:
            print(result)

    async def _download_url(self, url: str) -> str:
        loop = asyncio.get_event_loop()

        print(f"{YELLOW}Starting: {url}{RESET}")

        try:
            await loop.run_in_executor(self._executor, self._sync_download, url)
            return f"{GREEN}✅ Done: {url}{RESET}"
        except Exception as e:
            return f"{RED}❌ Failed: {url} — {e}{RESET}"

    def _sync_download(self, url: str):
        from yt_dlp import YoutubeDL

        opts = self._get_opts()
        with YoutubeDL(opts) as ydl:
            ydl.download([url])

    def __del__(self):
        if hasattr(self, "_executor"):
            self._executor.shutdown(wait=False, cancel_futures=True)

    async def __aiter__(self):
        urls = [u.strip() for u in self.urls.replace(",", " ").split() if u.strip()]
        sem = asyncio.Semaphore(self.max_concurrent)

        async def download_one(url):
            async with sem:
                return await self._download_url(url)

        tasks = [asyncio.create_task(download_one(u)) for u in urls]

        for task in asyncio.as_completed(tasks):
            yield await task
