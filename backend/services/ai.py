from typing import Optional

from openai import OpenAI

from core.config import settings
from schemas.career import CareerRequest


_openai_client: Optional[OpenAI] = None


def get_openai_client() -> Optional[OpenAI]:
    global _openai_client
    if not settings.openai_api_key:
        return None
    if _openai_client is None:
        _openai_client = OpenAI(api_key=settings.openai_api_key)
    return _openai_client


def generate_career_support_summary(request: CareerRequest) -> str:
    client = get_openai_client()
    if client is None:
        return (
            "AI summary: configure OPENAI_API_KEY in the backend .env to enable "
            "GPT-4 powered, deeply personalized career guidance."
        )

    prompt = (
        "You are an AI career coach inside the VidyaMitra platform. "
        "Given the user's current role, target role, years of experience, and interests, "
        "generate a concise, motivational summary (4–6 sentences) explaining the transition path, "
        "key strengths, and how the roadmap will help.\n\n"
        f"Current role: {request.current_role}\n"
        f"Target role: {request.target_role}\n"
        f"Years of experience: {request.experience_years}\n"
        f"Interests and strengths: {', '.join(request.interests)}"
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a precise, encouraging career mentor."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=350,
    )

    return completion.choices[0].message.content.strip()

