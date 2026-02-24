import json
import re
from typing import Any, Dict, List, Optional

import google.generativeai as genai

from core.config import settings
from schemas.career import CareerRequest


if settings.gemini_api_key:
    genai.configure(api_key=settings.gemini_api_key)
    _model: Optional[genai.GenerativeModel] = genai.GenerativeModel("gemini-2.0-flash")
else:
    _model = None


def _call_gemini_json(prompt: str) -> Optional[Dict[str, Any]]:
    if _model is None:
        return None
    response = _model.generate_content(prompt)
    raw = (response.text or "").strip()
    raw = re.sub(r"```json|```", "", raw).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def analyze_resume_with_gemini(resume_text: str) -> dict:
    prompt = f"""
You are an AI career assistant.

Return ONLY valid JSON (no markdown, no explanation).

Format:

{{
  "summary": "short paragraph",
  "strengths": ["skill1", "skill2"],
  "gaps": [
    {{"skill":"Data Visualization","level":"Needs improvement","recommendation":"Learn Tableau or Power BI"}}
  ],
  "suggested_courses": ["course1","course2"]
}}

Resume:
{resume_text}
"""

    data = _call_gemini_json(prompt) or {}
    if data:
        return data

    return {
        "summary": "Resume analyzed successfully.",
        "strengths": ["Technical foundation identified"],
        "gaps": [],
        "suggested_courses": [],
    }


def generate_career_summary_with_gemini(request: CareerRequest) -> Optional[str]:
    prompt = f"""
You are an AI career coach inside the VidyaMitra platform.

Generate a concise, motivational summary (4–6 sentences) for a working professional
who wants to transition careers.

Return ONLY plain text (no JSON, no bullet points).

Current role: {request.current_role}
Target role: {request.target_role}
Years of experience: {request.experience_years}
Interests and strengths: {", ".join(request.interests)}
"""

    if _model is None:
        return None
    response = _model.generate_content(prompt)
    text = (response.text or "").strip()
    return text or None


def generate_interview_feedback_with_gemini(qa_pairs: List[Dict[str, str]]) -> Optional[Dict[str, Any]]:
    """
    qa_pairs: [{"question": "...", "answer": "...", "id": 1}, ...]
    """
    prompt = f"""
You are an AI interview coach.

Given interview questions and the candidate's answers, return structured feedback.

Return ONLY valid JSON.

Format:
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
    data = _call_gemini_json(prompt)
    return data
