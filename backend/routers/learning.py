from typing import List

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from .auth import UserInDB, get_current_user
from services.resources import (
    fetch_youtube_videos,
    fetch_google_results,
    fetch_pexels_images,
    fetch_news,
    fetch_exchange_rates,
    persist_learning_event,
)


router = APIRouter()


class LearningResource(BaseModel):
    title: str
    url: str
    kind: str
    extra: dict | None = None


class LearningResponse(BaseModel):
    topic: str
    videos: List[dict]
    articles: List[dict]
    visuals: List[dict]
    news: List[dict]
    market: dict


@router.get("/resources", response_model=LearningResponse)
async def get_learning_resources(
    topic: str = Query(..., description="Learning goal, e.g. 'data visualization basics'"),
    current_user: UserInDB = Depends(get_current_user),
) -> LearningResponse:
    videos, articles, visuals, news_items, market = await _gather_resources(topic)

    persist_learning_event(
        user_id=current_user.id,
        topic=topic,
        metadata={
            "videos_count": len(videos),
            "articles_count": len(articles),
            "visuals_count": len(visuals),
            "news_count": len(news_items),
        },
    )

    return LearningResponse(
        topic=topic,
        videos=videos,
        articles=articles,
        visuals=visuals,
        news=news_items,
        market=market,
    )


async def _gather_resources(topic: str):
    videos = await fetch_youtube_videos(topic)
    articles = []
    visuals = await fetch_pexels_images(topic)
    news_items = await fetch_news(topic)
    market = await fetch_exchange_rates()
    return videos, articles, visuals, news_items, market

