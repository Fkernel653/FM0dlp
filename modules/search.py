"""
YouTube search handlers.
"""

from modules.colors import RESET, BOLD, RED, GREEN, CYAN, GRAY
from dataclasses import dataclass
from typing import Generator, Literal

from yt_dlp import YoutubeDL
from ytmusicapi import YTMusic


SEPARATE = f"{GRAY}|{RESET}"
DIVIDER = f"   {GRAY}   {'─' * 50}{RESET}\n"


@dataclass
class Search:
    """Handles searching across YouTube"""

    query: str
    limit: int
    type: Literal["track", "album"]
    proxy: str

    def __post_init__(self):
        if self.limit <= 0:
            raise ValueError("Limit must be positive")
        if self.type not in ("track", "album"):
            raise ValueError(f"Invalid type: {self.type}")

    def extract_ytvideo_info(self, item) -> dict | None:
        """Extract and format video information."""
        id = item.get("id")
        if not id:
            return None

        return {
            "title": item.get("title", "N/A"),
            "artist": item.get("channel", "N/A"),
            "views": self._format_views(item.get("view_count")),
            "duration": self._format_duration(item.get("duration")),
            "url": f"https://youtu.be/{id}",
        }

    def _format_views(self, view_count) -> str:
        """Format view count with commas."""
        if view_count:
            return f"{int(view_count):,}"
        return "N/A"

    def _format_duration(self, raw_duration) -> str:
        """Format duration to HH:MM:SS, MM:SS, or SS depending on length."""
        if not raw_duration:
            return "N/A"
        
        total_seconds = int(raw_duration)
        
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"

    def extract_ytmusic_info(self, item) -> dict | None:
        """Extract and format track information."""
        match self.type:
            case "track":
                track_id = item.get("videoId")
                if not track_id:
                    return None

                return {
                    "title": item.get("title", "Unknown Track"),
                    "artist": self._extract_artist(item),
                    "views": item.get("views", "N/A"),
                    "duration": item.get("duration", "N/A"),
                    "url": f"https://music.youtube.com/watch?v={track_id}",
                }

            case "album":
                pl_id = item.get("playlistId")
                if not pl_id:
                    return None

                return {
                    "title": item.get("title", "Unknown Track"),
                    "artist": self._extract_artist(item),
                    "year": item.get("year", "N/A"),
                    "url": f"https://music.youtube.com/playlist?list={pl_id}",
                }

    def _extract_artist(self, item) -> str:
        """Extract artist name from track data."""
        artists = item.get("artists")
        if artists and isinstance(artists, list):
            return artists[0].get("name", "Unknown Artist")
        return "Unknown Artist"
    
    def _format_ytvideo(
        self, num, title, artist, views=None, duration=None, url=None
    ) -> str:
        """Format search result for display."""
        return (
            f"\n\n{BOLD}{CYAN}{num}. {RESET}{BOLD}{title}{RESET}\n"
            f"   {GRAY}├─ {RESET}{artist}\n"
            f"   {GRAY}├─ {RESET}{views} {SEPARATE} {duration}\n"
            f"   {GRAY}└─ {RESET}{RED}{url}{RESET}\n"
            f"{DIVIDER}"
        )
    
    def _format_ytmusic(
        self, num, title, artist, views=None, duration=None, year=None, url=None
    ) -> str:
        """Format search result for display."""
        match self.type:
            case "track":
                return (
                    f"\n\n{BOLD}{CYAN}{num}. {RESET}{BOLD}{title}{RESET}\n"
                    f"   {GRAY}├─ {RESET}{artist}\n"
                    f"   {GRAY}├─ {RESET}{views} {SEPARATE} {duration}\n"
                    f"   {GRAY}└─ {RESET}{RED}{url}{RESET}\n"
                    f"{DIVIDER}"
                )
            case "album":
                return (
                    f"\n\n{BOLD}{CYAN}{num}. {RESET}{BOLD}{title}{RESET}\n"
                    f"   {GRAY}├─ {RESET}{artist}\n"
                    f"   {GRAY}├─ {RESET}{year}\n"
                    f"   {GRAY}└─ {RESET}{RED}{url}{RESET}\n"
                    f"{DIVIDER}"
                )

    def _yt_video_opts(self) -> dict:
        return {
            "proxy": self.proxy or None,
            "quiet": True,
            "extract_flat": True,
            "cachedir": False,
            "extractor_args": {
                "youtube": {
                    "player_client": ["web"],
                    "player_skip": ["configs", "js", "webpage", "authcheck"],
                }
            },
        }

    def yt_video(self) -> Generator[str, None, None]:
        """Search YouTube videos using yt-dlp."""
        try:
            match self.type:
                case "track":
                    search_type = "video"
                case "album":
                    search_type = "playlist"
                case _:
                    yield f"{RED}Unsupported type for yt_video: {self.type}{RESET}"
                    return

            with YoutubeDL(self._yt_video_opts()) as ydl:
                videos = ydl.extract_info(
                    f"ytsearch{self.limit}:{search_type}:{self.query}", download=False
                )["entries"]

            if not videos:
                yield f"{RED}\nNo videos matching {RESET}'{self.query}'"
                return

            for num, video in enumerate(videos, 1):
                if item := self.extract_ytvideo_info(video):
                    yield self._format_ytvideo(num=num, **item)

        except KeyboardInterrupt:
            yield f"{GREEN}Goodbye!{RESET}"
        except Exception as e:
            yield f"{RED}Youtube-Video error: {e}{RESET}"

    def _yt_music_kwargs(self) -> dict:
        if self.proxy:
            return {"proxies": {"http": self.proxy, "https": self.proxy}}
        return {}

    def yt_music(self) -> Generator[str, None, None]:
        """Search YouTube Music for song tracks only."""
        try:
            from itertools import islice

            yt = YTMusic(**self._yt_music_kwargs())

            match self.type:
                case "track":
                    search_type = "songs"
                case "album":
                    search_type = "albums"
                case _:
                    yield f"{RED}Unsupported type for yt_music: {self.type}{RESET}"
                    return

            tracks = yt.search(query=self.query, limit=self.limit, filter=search_type)

            if not tracks:
                yield f"{RED}\nNo tracks found for '{self.query}' on YouTube Music\n{RESET}"
                return

            tracks = islice(tracks, self.limit)
            for num, track in enumerate(tracks, 1):
                if item := self.extract_ytmusic_info(track):
                    yield self._format_ytmusic(num=num, **item)

        except KeyboardInterrupt:
            yield f"{GREEN}Goodbye!{RESET}"
        except Exception as e:
            yield f"{RED}Youtube-Music error: {e}{RESET}"
