from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr

from .auth import UserInDB, get_current_user
from core.supabase import supabase


router = APIRouter()


class Profile(BaseModel):
  full_name: str
  email: EmailStr
  resume_filename: Optional[str] = None
  profile_summary: Optional[str] = None
  strengths: List[str] = []
  interests: List[str] = []


class ProfileUpdate(BaseModel):
  profile_summary: Optional[str] = None
  strengths: Optional[List[str]] = None
  interests: Optional[List[str]] = None


def _get_profile_row(user_id: int) -> Optional[dict]:
  res = (
      supabase.table("profiles")
      .select("*")
      .eq("user_id", user_id)
      .limit(1)
      .execute()
  )
  if not res.data:
    return None
  return res.data[0]


def _row_to_profile(user: UserInDB, row: Optional[dict]) -> Profile:
  strengths = row.get("strengths") if row else []
  interests = row.get("interests") if row else []
  return Profile(
      full_name=user.full_name,
      email=user.email,
      resume_filename=(row or {}).get("resume_filename"),
      profile_summary=(row or {}).get("profile_summary"),
      strengths=strengths or [],
      interests=interests or [],
  )


@router.get("/me", response_model=Profile)
def get_profile(current_user: UserInDB = Depends(get_current_user)) -> Profile:
  row = _get_profile_row(current_user.id)
  return _row_to_profile(current_user, row)


@router.patch("/me", response_model=Profile)
def update_profile(
  payload: ProfileUpdate,
  current_user: UserInDB = Depends(get_current_user),
) -> Profile:
  update_data: dict = {"user_id": current_user.id}

  if payload.profile_summary is not None:
    update_data["profile_summary"] = payload.profile_summary
  if payload.strengths is not None:
    update_data["strengths"] = payload.strengths
  if payload.interests is not None:
    update_data["interests"] = payload.interests

  supabase.table("profiles").upsert(update_data, on_conflict="user_id").execute()

  row = _get_profile_row(current_user.id)
  return _row_to_profile(current_user, row)

