import json
import re
from typing import Any, Dict, List, Optional

from groq import Groq

from core.config import settings
from schemas.career import CareerRequest


_client: Optional[Groq] = None


def get_groq_client() -> Optional[Groq]:
    global _client
    if not settings.groq_api_key:
        return None
    if _client is None:
        _client = Groq(api_key=settings.groq_api_key)
    return _client


def _chat_json(prompt: str):
    groq_client = get_groq_client()
    if groq_client is None:
        return fallback_response()
    completion = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You are a strict JSON generator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=800
    )

    text = completion.choices[0].message.content.strip()

    try:
        return json.loads(text)
    except:
        return None

def fallback_response():
    return {
        "summary": "Resume analyzed successfully.",
        "strengths": [],
        "gaps": [],
        "suggested_courses": []
    }

MAX_RESUME_CHARS = 6000

def trim_resume(text: str) -> str:
    return text[:MAX_RESUME_CHARS]

def analyze_resume_with_groq(resume_text: str) -> dict:
    resume_text = trim_resume(resume_text)

    print("resume_text", resume_text)
    prompt = f"""
You are a career advisor AI.

Analyze the resume and return ONLY valid JSON.

Format:

{{
  "summary": "1-2 sentence overview",
  "strengths": ["skill1","skill2"],
  "gaps": [
    {{"skill":"X","level":"Beginner|Intermediate|Advanced","recommendation":"What to learn"}}
  ],
  "suggested_courses": ["course1","course2"]
}}

Resume:
{resume_text}
"""

    data = _chat_json(prompt)
    return data or fallback_response()

def generate_career_summary_with_groq(request: CareerRequest) -> Optional[str]:
    client = get_groq_client()
    if client is None:
        return None

    prompt = f"""
You are an AI career coach inside the VidyaMitra platform.

Generate a concise, motivational summary (4–6 sentences) for a working professional
who wants to transition careers, using their context.

Return ONLY plain text (no JSON, no bullet points).

Current role: {request.current_role}
Target role: {request.target_role}
Years of experience: {request.experience_years}
Interests and strengths: {", ".join(request.interests)}
Additional resume context (may be empty): {getattr(request, "resume_text", "")}
"""

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You are a precise, encouraging career mentor."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=400,
    )

    text = (completion.choices[0].message.content or "").strip()
    return text or None


def generate_career_roadmap_with_groq(request: CareerRequest) -> Dict[str, Any]:
    prompt = f"""
You are an AI career coach designing a personalized career transition roadmap for VidyaMitra.

Use this data to generate a roadmap:

Current role: {request.current_role}
Target role: {request.target_role}
Years of experience: {request.experience_years}
Interests and strengths: {", ".join(request.interests)}
Additional resume context (may be empty): {getattr(request, "resume_text", "")}

Return ONLY valid JSON in this exact format:

{{
  "summary": "overall narrative of the transition and plan",
  "transferable_skills": ["Communication", "Stakeholder management"],
  "steps": [
    {{"title": "Step title", "description": "What to do in this phase", "duration_weeks": 4}}
  ],
  "recommended_certifications": ["Certification 1", "Certification 2"]
}}
"""
    data = _chat_json(prompt) or {}
    if data:
        return data

    # Fallback minimal structure if Groq is not configured or returns invalid JSON
    return {
        "summary": "Configure GROQ_API_KEY in the backend .env to enable AI-generated, personalized career roadmaps.",
        "transferable_skills": ["Strong base for transition"],
        "steps": [
            {
                "title": "Clarify goals and required skills",
                "description": "Review job descriptions for your target role and list required skills.",
                "duration_weeks": 2,
            }
        ],
        "recommended_certifications": [],
    }


def generate_interview_questions_with_groq(target_role: str, count: int = 3) -> List[Dict[str, str]]:
    prompt = f"""
Generate {count} realistic interview questions for a candidate targeting the role: "{target_role}".

Return ONLY valid JSON as a list of objects:

[
  {{"question": "question text", "competency": "Communication"}},
  ...
]
"""
    data = _chat_json(prompt)
    if not isinstance(data, list):
        return []
    cleaned: List[Dict[str, str]] = []
    for item in data:
        q = str(item.get("question", "")).strip()
        comp = str(item.get("competency", "General")).strip()
        if q:
            cleaned.append({"question": q, "competency": comp or "General"})
    return cleaned


def generate_interview_feedback_with_groq(qa_pairs: List[Dict[str, str]]) -> Optional[Dict[str, Any]]:
    """
    qa_pairs: [{"id": 1, "question": "...", "answer": "..."}]
    """
    prompt = f"""
You are an AI interview coach.

Given interview questions and the candidate's answers, return structured feedback.

Return ONLY valid JSON in this exact format:

{{
  "overall_summary": "text",
  "feedback": [
    {{
      "question_id": 1,
      "feedback": "short paragraph",
      "tone_score": 0,
      "confidence_score": 0,
      "accuracy_score": 0,
      "suggestions": ["tip1","tip2"]
    }}
  ]
}}

Data:
{json.dumps(qa_pairs, ensure_ascii=False)}
"""
    return _chat_json(prompt)

