from schemas.career import CareerRequest
from services.groq_ai import generate_career_summary_with_groq


def generate_career_support_summary(request: CareerRequest) -> str:
    summary = generate_career_summary_with_groq(request)
    if summary:
        return summary
    return (
        "AI summary: configure GROQ_API_KEY in the backend .env "
        "to enable deeply personalized career guidance based on your resume and goals."
    )

