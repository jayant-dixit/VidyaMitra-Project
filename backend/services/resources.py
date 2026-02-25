from typing import List, Optional

import httpx
from supabase import create_client, Client

from core.config import settings


_supabase_client: Optional[Client] = None


def get_supabase() -> Optional[Client]:
    global _supabase_client
    if not settings.supabase_url or not settings.supabase_anon_key:
        return None
    if _supabase_client is None:
        _supabase_client = create_client(str(settings.supabase_url), settings.supabase_anon_key)
    return _supabase_client


async def fetch_youtube_videos(query: str, max_results: int = 5) -> List[dict]:
    if not settings.youtube_api_key:
        return []
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": settings.youtube_api_key,
        "part": "snippet",
        "type": "video",
        "q": query,
        "maxResults": max_results,
    }
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

    results: List[dict] = []
    for item in data.get("items", []):
        vid = item["id"]["videoId"]
        snippet = item["snippet"]
        results.append(
            {
                "title": snippet.get("title"),
                "channel": snippet.get("channelTitle"),
                "thumbnail": snippet.get("thumbnails", {}).get("medium", {}).get("url"),
                "url": f"https://www.youtube.com/watch?v={vid}",
            }
        )
    return results


async def fetch_google_results(query: str, max_results: int = 5) -> List[dict]:
    if not settings.google_api_key:
        return []
    # This uses Google Custom Search JSON API; you must configure CX in .env.
    # For demo we read it from GOOGLE_CX if present.
    import os

    cx = settings.google_cx
    if not cx:
        print("Google Custom Search Engine ID is not set")
        return []

    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": settings.google_api_key, "cx": cx, "q": query, "num": max_results}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

    return [
        {"title": item.get("title"), "snippet": item.get("snippet"), "url": item.get("link")}
        for item in data.get("items", [])
    ]


async def fetch_pexels_images(query: str, per_page: int = 6) -> List[dict]:
    if not settings.pexels_api_key:
        return []
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": settings.pexels_api_key}
    params = {"query": query, "per_page": per_page}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()

    return [
        {
            "url": photo.get("url"),
            "alt": photo.get("alt"),
            "src": photo.get("src", {}).get("medium"),
            "photographer": photo.get("photographer"),
        }
        for photo in data.get("photos", [])
    ]


async def fetch_news(query: str, page_size: int = 5) -> List[dict]:
    if not settings.news_api_key:
        return []
    url = "https://newsapi.org/v2/everything"
    params = {"q": query, "pageSize": page_size, "apiKey": settings.news_api_key, "language": "en"}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

    return [
        {
            "title": art.get("title"),
            "source": (art.get("source") or {}).get("name"),
            "url": art.get("url"),
            "published_at": art.get("publishedAt"),
        }
        for art in data.get("articles", [])
    ]


async def fetch_exchange_rates(base: str = "USD") -> dict:
    if not settings.exchange_api_key:
        return {}
    url = f"https://v6.exchangerate-api.com/v6/{settings.exchange_api_key}/latest/{base}"
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()
    return {
        "base": data.get("base_code"),
        "date": data.get("time_last_update_utc"),
        "rates": data.get("conversion_rates", {}),
    }


def persist_learning_event(user_id: int, topic: str, metadata: dict) -> None:
    supabase = get_supabase()
    if supabase is None:
        return
    supabase.table("learning_events").insert(
        {
            "user_id": user_id,
            "topic": topic,
            "metadata": metadata,
        }
    ).execute()
