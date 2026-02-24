from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .auth import UserInDB, get_current_user


router = APIRouter()


class InterviewQuestion(BaseModel):
    id: int
    question: str
    competency: str


class InterviewAnswer(BaseModel):
    question_id: int
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


QUESTIONS: list[InterviewQuestion] = [
    InterviewQuestion(
        id=1,
        question="Tell me about yourself and your career goals.",
        competency="Communication",
    ),
    InterviewQuestion(
        id=2,
        question="Describe a challenging project and how you handled ambiguity.",
        competency="Problem Solving",
    ),
    InterviewQuestion(
        id=3,
        question="Why are you interested in this role and this industry?",
        competency="Motivation",
    ),
]


@router.get("/questions", response_model=List[InterviewQuestion])
def get_questions(current_user: UserInDB = Depends(get_current_user)) -> List[InterviewQuestion]:
    return QUESTIONS


@router.post("/feedback", response_model=InterviewSessionFeedback)
def submit_answers(
    answers: List[InterviewAnswer],
    current_user: UserInDB = Depends(get_current_user),
) -> InterviewSessionFeedback:
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

