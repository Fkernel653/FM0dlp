# search.py
"""
YouTube and SoundCloud search module with async support.
"""

from modules.colors import RESET, BOLD, RED, GREEN, CYAN, GRAY
from dataclasses import dataclass
import asyncio


@dataclass
class Search:
    """Handles searching across YouTube and SoundCloud."""

    query: str
    limit: int
    enable_filter: str
    sep = f"{GRAY}|{RESET}"

    def youtube(self):
        """Search YouTube using yt-dlp."""
        from yt_dlp import YoutubeDL

        try:
            opts = {"quiet": True, "extract_flat": True, "simulate": True}
            with YoutubeDL(opts) as ydl:
                videos = ydl.extract_info(f"ytsearch{self.limit}:{self.query}", download=False)["entries"]

            if self.enable_filter == "True":
                filtered_videos = []
                for video in videos:
                    title = video.get("title", "N/A").lower()
                    keywords = ["official", "full album", "hd"]
                    if any(keyword in title for keyword in keywords):
                        filtered_videos.append(video)
                        videos = filtered_videos

            if not videos:
                yield f"{RED}\nNo videos matching {RESET}'{self.query}'"
                return

            for num, video in enumerate(videos, 1):
                views = video.get("view_count", "N/A")
                if views and isinstance(views, int):
                    views = f"{views:,}"

                duration_sec = video.get("duration")
                if duration_sec:
                    minutes = int(duration_sec // 60)
                    seconds = int(duration_sec % 60)
                    duration_str = f"{minutes}:{seconds:02d}"
                else:
                    duration_str = "N/A"

                video_info = (
                    f"\n\n{BOLD}{CYAN}{num}. {RESET}{BOLD}{video.get('title', 'N/A')}{RESET}\n"
                    f"   {GRAY}├─ {RESET}{video.get('channel', 'N/A')}\n"
                    f"   {GRAY}├─ {RESET}{views} {self.sep} {duration_str}\n"
                    f"   {GRAY}└─ {RESET}{RED}https://youtu.be/{video.get('id')}{RESET}\n"
                    f"   {GRAY}   {'─' * 50}{RESET}"
                )
                yield video_info

        except Exception as e:
            yield f"{RED}Error: {e}{RESET}"
        except KeyboardInterrupt:
            yield f"{GREEN}Goodbye!{RESET}"

    async def soundcloud(self):
        """Search SoundCloud for tracks."""
        from soundcloud import SoundCloud
        from fake_useragent import UserAgent
        from itertools import islice

        try:
            loop = asyncio.get_event_loop()

            def sync_search():
                ua = UserAgent().random
                sc = SoundCloud(user_agent=ua)
                tracks = sc.search_tracks(self.query)

                if self.enable_filter == "True":
                    filtered_tracks = []
                    for track in tracks:
                        if hasattr(track, "id") and track.id and hasattr(track, "title") and track.title:
                            filtered_tracks.append(track)
                            if len(filtered_tracks) >= self.limit:
                                break
                    return list(islice(filtered_tracks, self.limit))
                else:
                    return list(islice(tracks, self.limit))

            tracks = await asyncio.wait_for(loop.run_in_executor(None, sync_search), timeout=30.0)

            if not tracks:
                yield f"{RED}\nNo tracks found for '{self.query}' on SoundCloud\n{RESET}"
                return

            for num, track in enumerate(tracks, 1):
                duration_ms = getattr(track, "duration", 0)
                minutes = duration_ms // 60000
                seconds = (duration_ms % 60000) // 1000
                duration_str = f"{minutes}:{seconds:02d}"
                track_url = getattr(track, "permalink_url", None) or getattr(track, "uri", "N/A")

                track_info = (
                    f"\n{BOLD}{CYAN}{num}. {RESET}{BOLD}{track.title}{RESET}\n"
                    f"   {GRAY}├─ {RESET}{track.user.full_name}\n"
                    f"   {GRAY}├─ {RESET}{track.created_at.date()} {self.sep} {duration_str}\n"
                    f"   {GRAY}└─ {RESET}{RED}{track_url}{RESET}\n"
                    f"   {GRAY}   {'─' * 50}{RESET}\n"
                )
                yield track_info

        except asyncio.TimeoutError:
            yield f"{RED}SoundCloud search timeout (30 seconds){RESET}"
        except Exception as e:
            yield f"{RED}SoundCloud error: {e}{RESET}"