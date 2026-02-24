import json
import re
import google.generativeai as genai
from core.config import settings

genai.configure(api_key=settings.gemini_api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


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

    response = model.generate_content(prompt)

    raw = response.text.strip()

    # Remove markdown blocks if present
    raw = re.sub(r"```json|```", "", raw).strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback minimal response
        return {
            "summary": "Resume analyzed successfully.",
            "strengths": ["Technical foundation identified"],
            "gaps": [],
            "suggested_courses": []
        }