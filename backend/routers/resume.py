from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel

from .auth import UserInDB, get_current_user
from services.groq_ai import analyze_resume_with_groq
from services.resume_parser import extract_text
from core.supabase import supabase


UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

router = APIRouter()


class SkillGap(BaseModel):
    skill: str
    level: str
    recommendation: str


class ResumeInsight(BaseModel):
    summary: str
    strengths: List[str]
    gaps: List[SkillGap]
    suggested_courses: List[str]


@router.post("/upload", response_model=ResumeInsight)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: UserInDB = Depends(get_current_user),
) -> ResumeInsight:

    if not file.filename.lower().endswith((".pdf", ".doc", ".docx", ".txt")):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file type")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty file")

    save_path = UPLOAD_DIR / f"user_{current_user.id}_{file.filename}"
    save_path.write_bytes(content)

    resume_text = extract_text(content, file.filename)

    ai_result = analyze_resume_with_groq(resume_text)

    print("ai_result", ai_result)

    # Persist profile summary & strengths to Supabase for later use
    try:
        supabase.table("profiles").upsert(
            {
                "user_id": current_user.id,
                "resume_path": str(save_path),
                "resume_filename": file.filename,
                "profile_summary": ai_result.get("summary"),
                "strengths": ai_result.get("strengths", []),
            },
            on_conflict="user_id",
        ).execute()
    except Exception as e:
        # Fail silently if profiles table or columns are not configured
        print("Error persisting profile summary and strengths to Supabase")
        print("Error details:", e)
        pass

    return ResumeInsight(**ai_result)
