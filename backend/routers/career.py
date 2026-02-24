from fastapi import APIRouter, Depends

from schemas.career import CareerRequest, CareerRoadmap
from .auth import UserInDB, get_current_user
from services.ai import generate_career_support_summary

router = APIRouter()


@router.post("/roadmap", response_model=CareerRoadmap)
def generate_career_roadmap(
    request: CareerRequest,
    current_user: UserInDB = Depends(get_current_user),
) -> CareerRoadmap:

    transferable: list[str] = []
    interests_lower = [i.lower() for i in request.interests]

    if "communication" in interests_lower or "presentation" in interests_lower:
        transferable.append("Stakeholder communication")

    if "excel" in interests_lower or "analysis" in interests_lower:
        transferable.append("Analytical thinking and business insights")

    if request.experience_years >= 2:
        transferable.append("Industry domain knowledge")

    if request.target_role.lower() == "data scientist":
        steps = [
            {
                "title": "Solidify Python and data fundamentals",
                "description": "Revise Python, statistics, and SQL with hands-on exercises.",
                "duration_weeks": 4,
            },
            {
                "title": "Build ML foundations",
                "description": "Cover regression, classification, and model evaluation.",
                "duration_weeks": 6,
            },
            {
                "title": "Create a portfolio of projects",
                "description": "Build 2–3 end-to-end ML projects.",
                "duration_weeks": 8,
            },
        ]
        certs = ["Google Data Analytics", "AWS Machine Learning Specialty"]
    else:
        steps = [
            {
                "title": "Clarify target skills",
                "description": "List top skills from job descriptions.",
                "duration_weeks": 2,
            },
            {
                "title": "Plan structured learning blocks",
                "description": "Study 6–8 hours weekly.",
                "duration_weeks": 6,
            },
        ]
        certs = []

    summary = generate_career_support_summary(request)

    return CareerRoadmap(
        summary=summary,
        transferable_skills=transferable or ["Strong base for transition."],
        steps=steps,
        recommended_certifications=certs,
    )