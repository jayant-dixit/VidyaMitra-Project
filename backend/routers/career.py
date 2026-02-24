from fastapi import APIRouter, Depends

from schemas.career import CareerRequest, CareerRoadmap
from .auth import UserInDB, get_current_user
from services.ai import generate_career_support_summary
from services.groq_ai import generate_career_roadmap_with_groq

router = APIRouter()


@router.post("/roadmap", response_model=CareerRoadmap)
def generate_career_roadmap(
    request: CareerRequest,
    current_user: UserInDB = Depends(get_current_user),
) -> CareerRoadmap:
    """
    Generate a personalized career roadmap using Groq AI.
    The roadmap considers current role, target role, experience, interests, and optional resume_text.
    """
    data = generate_career_roadmap_with_groq(request)

    # Ensure summary is always present, using the text-focused helper if needed
    if not data.get("summary"):
        data["summary"] = generate_career_support_summary(request)

    return CareerRoadmap(**data)