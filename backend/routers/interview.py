from typing import List, Dict

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from .auth import UserInDB, get_current_user
from services.groq_ai import (
    generate_interview_questions_with_groq,
    generate_interview_feedback_with_groq,
)


router = APIRouter()


class InterviewQuestion(BaseModel):
    id: int
    question: str
    competency: str


class InterviewAnswer(BaseModel):
    question_id: int
    question: str
    answer: str


class InterviewFeedback(BaseModel):
    question_id: int
    feedback: str
    tone_score: int
    confidence_score: int
    accuracy_score: int
    suggestions: List[str]


class InterviewSessionFeedback(BaseModel):
    overall_summary: str
    feedback: List[InterviewFeedback]


@router.get("/questions", response_model=List[InterviewQuestion])
def get_questions(
    target_role: str = Query("Data Scientist", description="Target role for the mock interview."),
    current_user: UserInDB = Depends(get_current_user),
) -> List[InterviewQuestion]:
    raw_questions = generate_interview_questions_with_groq(target_role) or []
    if not raw_questions:
        # Minimal fallback if GROQ_API_KEY is not configured
        raw_questions = [
            {"question": f"Why are you interested in the {target_role} role?", "competency": "Motivation"}
        ]
    result: List[InterviewQuestion] = []
    for idx, item in enumerate(raw_questions, start=1):
        result.append(
            InterviewQuestion(
                id=idx,
                question=item.get("question", ""),
                competency=item.get("competency", "General"),
            )
        )
    return result


@router.post("/feedback", response_model=InterviewSessionFeedback)
def submit_answers(
    answers: List[InterviewAnswer],
    current_user: UserInDB = Depends(get_current_user),
) -> InterviewSessionFeedback:
    qa_pairs: List[Dict[str, str]] = [
        {"id": ans.question_id, "question": ans.question, "answer": ans.answer} for ans in answers
    ]

    ai_data = generate_interview_feedback_with_groq(qa_pairs)

    if ai_data and "feedback" in ai_data:
        return InterviewSessionFeedback(**ai_data)

    # Fallback simple scoring if Groq is not configured
    feedback_items: list[InterviewFeedback] = []

    for ans in answers:
        base_text = ans.answer.lower()
        tone_score = 70
        confidence_score = 70
        accuracy_score = 70
        suggestions: list[str] = []

        if len(base_text) < 40:
            suggestions.append("Provide more detailed, structured responses using the STAR method.")
            confidence_score -= 10
        if "team" not in base_text:
            suggestions.append("Highlight collaboration and impact on the team or business.")
        if "learn" not in base_text and "improve" not in base_text:
            suggestions.append("Mention what you learned and how you evolved from the experience.")

        feedback_items.append(
            InterviewFeedback(
                question_id=ans.question_id,
                feedback="AI-generated feedback focusing on clarity, structure, and relevance.",
                tone_score=max(0, min(100, tone_score)),
                confidence_score=max(0, min(100, confidence_score)),
                accuracy_score=max(0, min(100, accuracy_score)),
                suggestions=suggestions or ["Good answer—consider refining examples for even more impact."],
            )
        )

    overall_summary = (
        "Your mock interview shows good potential. Focus on expanding your examples, making outcomes measurable, "
        "and explicitly stating what you learned from each experience to strengthen your narrative."
    )

    return InterviewSessionFeedback(overall_summary=overall_summary, feedback=feedback_items)

