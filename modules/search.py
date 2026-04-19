"""
YouTube search handlers.
"""

from modules.colors import RESET, BOLD, RED, GREEN, CYAN, GRAY
from dataclasses import dataclass

from yt_dlp import YoutubeDL
from ytmusicapi import YTMusic


SEPARATE = f"{GRAY}|{RESET}"

@dataclass
class Search:
    """Handles searching across YouTube"""

    query: str
    limit: int
    proxy: str

    def get_duration(self, target, key, divisor=60, remainder_mod=60):
        if isinstance(target, dict):
            raw_duration = target.get(key)
        else:
            raw_duration = getattr(target, key, None)
        if raw_duration:
            minutes = int(raw_duration // divisor)
            seconds = int(raw_duration % remainder_mod)
            return f"{minutes}:{seconds:02d}"
        else:
            return "N/A"

    def get_info(self, num, title, artist, views, duration, url) -> str:
        track_info = (
            f"\n\n{BOLD}{CYAN}{num}. {RESET}{BOLD}{title}{RESET}\n"
            f"   {GRAY}├─ {RESET}{artist}\n"
            f"   {GRAY}├─ {RESET}{views} {SEPARATE} {duration}\n"
            f"   {GRAY}└─ {RESET}{RED}{url}{RESET}\n"
            f"   {GRAY}   {'─' * 50}{RESET}\n"
        )
        return track_info

    def yt_video(self):
        """Search YouTube videos using yt-dlp."""
        try:
            opts = {
                "proxy": self.proxy if self.proxy else None,
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
            with YoutubeDL(opts) as ydl:
                videos = ydl.extract_info(
                    f"ytsearch{self.limit}:video:{self.query}", download=False
                )["entries"]

            if not videos:
                yield f"{RED}\nNo videos matching {RESET}'{self.query}'"
                return

            for num, video in enumerate(videos, 1):
                video_id = video.get("id")
                if not video_id:
                    continue

                title = video.get("title", "N/A")
                channel = video.get("channel", "N/A")

                view_count = video.get("view_count")
                if view_count:
                    views = f"{int(view_count):,}"
                else:
                    views = "N/A"

                duration = self.get_duration(video, "duration")

                yield self.get_info(
                    num=num,
                    title=title,
                    artist=channel,
                    views=views,
                    duration=duration,
                    url=f"https://youtu.be/{video_id}"
                )

        except KeyboardInterrupt:
            yield f"{GREEN}Goodbye!{RESET}"
        except Exception as e:
            yield f"{RED}Youtube-Video error: {e}{RESET}"

    def yt_music(self):
        """Search YouTube Music for song tracks only."""
        try:
            from itertools import islice

            yt_kwargs = {}
            if self.proxy:
                yt_kwargs["proxies"] = {"http": self.proxy, "https": self.proxy}
            yt = YTMusic(**yt_kwargs)
            tracks = yt.search(query=self.query, limit=self.limit, filter="songs")

            if not tracks:
                yield f"{RED}\nNo tracks found for '{self.query}' on YouTube Music\n{RESET}"
                return

            tracks = islice(tracks, self.limit)
            for num, track in enumerate(tracks, 1):
                track_id = track.get("videoId")
                if not track_id:
                    continue

                title = track.get("title", "Unknown Track")

                artist = (
                    track.get("artists", [{}])[0].get("name")
                    if track.get("artists")
                    else "Unknown Artist"
                )
                views = track.get("views", "N/A")
                duration = track.get("duration", "N/A")

                yield self.get_info(
                    num=num,
                    title=title,
                    artist=artist,
                    views=views,
                    duration=duration,
                    url=f"https://music.youtube.com/watch?v={track_id}"
                )

        except KeyboardInterrupt:
            yield f"{GREEN}Goodbye!{RESET}"
        except Exception as e:
            yield f"{RED}Youtube-Music error: {e}{RESET}"