from pydantic_settings import BaseSettings
from pydantic import AnyUrl
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "VidyaMitra API"
    secret_key: str = "CHANGE_THIS_SECRET_KEY_IN_PRODUCTION"
    frontend_origin: str = "http://localhost:5173"

    groq_api_key: Optional[str] = None

    google_api_key: Optional[str] = None
    youtube_api_key: Optional[str] = None
    google_cx: Optional[str] = None

    supabase_url: Optional[AnyUrl] = None
    supabase_anon_key: Optional[str] = None
    supabase_key: Optional[str] = None
    supabase_service_role_key: Optional[str] = None

    pexels_api_key: Optional[str] = None
    news_api_key: Optional[str] = None
    exchange_api_key: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
