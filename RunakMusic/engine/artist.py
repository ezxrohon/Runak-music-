"""YouTube search (py-yt) + stream download (Meow API), thumbnail
branding, and the /broadcast helper."""

import asyncio
import os

import aiohttp
from py_yt import VideosSearch

import config
from RunakMusic.engine.thumbnail import generate_thumbnail

os.makedirs("downloads", exist_ok=True)
os.makedirs("thumbnails", exist_ok=True)


async def get_info(query: str) -> dict | None:
    """Search YouTube (accepts a search term or a youtube link) and
    return the top result's info, or None if nothing was found."""
    search = VideosSearch(query, limit=1)
    result = (await search.next())["result"]
    if not result:
        return None

    video = result[0]
    duration = video.get("duration") or "Live"
    seconds = 0
    if duration != "Live":
        parts = [int(p) for p in duration.split(":")]
        for part in parts:
            seconds = seconds * 60 + part

    return {
        "id": video["id"],
        "title": video["title"],
        "duration": duration,
        "duration_seconds": seconds,
        "thumbnail": video["thumbnails"][0]["url"].split("?")[0],
        "link": video["link"],
    }


async def download(video_id: str, video: bool = False) -> str | None:
    """Download audio (or video) for a video id via the Meow API, reusing
    a cached file if we already grabbed this id before."""
    ext = "mp4" if video else "mp3"
    file_path = os.path.join("downloads", f"{video_id}.{ext}")

    if os.path.exists(file_path) and os.path.getsize(file_path) > 10000:
        return file_path

    kind = "video" if video else "audio"
    quality = "480" if video else "128"
    stream_url = (
        f"{config.MEOW_API_URL}/stream/{video_id}"
        f"?key={config.MEOW_API_KEY}&type={kind}&quality={quality}"
    )
    timeout = aiohttp.ClientTimeout(total=600 if video else 300)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(stream_url, timeout=timeout) as resp:
                if resp.status != 200:
                    return None
                with open(file_path, "wb") as f:
                    async for chunk in resp.content.iter_chunked(131072):
                        f.write(chunk)
    except Exception:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass
        return None

    if os.path.exists(file_path) and os.path.getsize(file_path) > 10000:
        return file_path
    return None


async def get_thumbnail(video_id: str, title: str, duration: str, thumbnail_url: str) -> str | None:
    """Build (and cache) the branded 'now playing' thumbnail for a track.
    Returns None on any failure — callers should fall back to plain text."""
    cached = os.path.join("thumbnails", f"{video_id}.png")
    if os.path.exists(cached):
        return cached
    loop = asyncio.get_event_loop()
    try:
        return await loop.run_in_executor(
            None, generate_thumbnail, video_id, title, duration, thumbnail_url
        )
    except Exception:
        return None


async def broadcast(app, text: str) -> tuple[int, int]:
    """Send `text` to every chat the bot has served, return (sent, failed)."""
    from RunakMusic.engine.data import get_served_chats

    sent = failed = 0
    for chat_id in get_served_chats():
        try:
            await app.send_message(chat_id, text)
            sent += 1
        except Exception:
            failed += 1
    return sent, failed
