"""
YouTube and SoundCloud search handlers.
"""

from modules.colors import RESET, BOLD, RED, GREEN, CYAN, GRAY
from fake_useragent import UserAgent
from dataclasses import dataclass

from yt_dlp import YoutubeDL
from ytmusicapi import YTMusic
from soundcloud import SoundCloud

from itertools import islice

USER_AGENT = UserAgent().random
SEPARATE = f"{GRAY}|{RESET}"


@dataclass
class Search:
    """Handles searching across YouTube and SoundCloud."""

    query: str
    limit: int

    def yt_video(self):
        """Search YouTube videos using yt-dlp."""
        try:
            opts = {
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
                view_count = video.get("view_count")
                if view_count:
                    views = f"{int(view_count):,}"
                else:
                    views = "N/A"

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
                    f"   {GRAY}├─ {RESET}{views} {SEPARATE} {duration_str}\n"
                    f"   {GRAY}└─ {RESET}{RED}https://youtu.be/{video.get('id')}{RESET}\n"
                    f"   {GRAY}   {'─' * 50}{RESET}"
                )
                yield video_info
        except KeyboardInterrupt:
            yield f"{GREEN}Goodbye!{RESET}"
        except Exception as e:
            yield f"{RED}Youtube-Video error: {e}{RESET}"

    def yt_music(self):
        """Search YouTube Music for song tracks only."""
        try:
            yt = YTMusic()
            tracks = yt.search(
                query=self.query, limit=self.limit, filter="songs"
            )

            if not tracks:
                yield f"{RED}\nNo tracks found for '{self.query}' on YouTube Music\n{RESET}"

            for num, track in enumerate(tracks, 1):
                video_id = track.get("videoId")
                if not video_id:
                    continue

                artist = (
                    track.get("artists", [{}])[0].get("name")
                    if track.get("artists")
                    else "Unknown Artist"
                )

                track_info = (
                    f"\n{BOLD}{CYAN}{num}. {RESET}{BOLD}{track.get('title', 'Unknown Track')}{RESET}\n"
                    f"   {GRAY}├─ {RESET}{artist}\n"
                    f"   {GRAY}├─ {RESET}{track.get('duration', 'N/A')}\n"
                    f"   {GRAY}└─ {RESET}{RED}{f'https://music.youtube.com/watch?v={video_id}'}{RESET}\n"
                    f"   {GRAY}   {'─' * 50}{RESET}\n"
                )
                yield track_info
        except KeyboardInterrupt:
            yield f"{GREEN}Goodbye!{RESET}"
        except Exception as e:
            yield f"{RED}Youtube-Music error: {e}{RESET}"

    def soundcloud(self):
        """Search SoundCloud for tracks."""
        try:
            sc = SoundCloud(user_agent=USER_AGENT)
            tracks = islice(sc.search(query=self.query), self.limit)

            if not tracks:
                yield f"{RED}\nNo tracks found for '{self.query}' on SoundCloud\n{RESET}"

            for num, track in enumerate(tracks, 1):
                if track.kind != "track":
                    continue
                title = track.title if track.title else "Unknown Track"
                artist = (
                    track.user.full_name if track.user.full_name else "Unknown Artist"
                )

                try:
                    date = track.created_at.date() if track.created_at else "N/A"
                except AttributeError:
                    date = "N/A"

                duration_ms = getattr(track, "duration", 0)
                minutes = duration_ms // 60000
                seconds = (duration_ms % 60000) // 1000
                duration_str = f"{minutes}:{seconds:02d}"

                track_url = (
                    track.permalink_url
                    if hasattr(track, "permalink_url")
                    else track.uri
                    if hasattr(track, "uri")
                    else "N/A"
                )

                track_info = (
                    f"\n{BOLD}{CYAN}{num}. {RESET}{BOLD}{title}{RESET}\n"
                    f"   {GRAY}├─ {RESET}{artist}\n"
                    f"   {GRAY}├─ {RESET}{date} {SEPARATE} {duration_str}\n"
                    f"   {GRAY}└─ {RESET}{RED}{track_url}{RESET}\n"
                    f"   {GRAY}   {'─' * 50}{RESET}\n"
                )
                yield track_info

        except KeyboardInterrupt:
            yield f"{GREEN}Goodbye!{RESET}"
        except Exception as e:
            yield f"{RED}SoundCloud error: {e}{RESET}"