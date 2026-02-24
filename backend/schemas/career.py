from typing import List
from pydantic import BaseModel


class CareerRequest(BaseModel):
    current_role: str
    target_role: str
    experience_years: int
    interests: List[str]
    # Optional plain-text resume content or summary to enrich analysis
    resume_text: str | None = None


class RoadmapStep(BaseModel):
    title: str
    description: str
    duration_weeks: int


class CareerRoadmap(BaseModel):
    summary: str
    transferable_skills: List[str]
    steps: List[RoadmapStep]
    recommended_certifications: List[str]