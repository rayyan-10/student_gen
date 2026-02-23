from pydantic import BaseModel
from typing import Any, Optional


class AdvisorRequest(BaseModel):
    """Request body for the /ask_advisor endpoint."""
    query: str
    dataset_id: Optional[str] = "default"


class MCQ(BaseModel):
    question: str
    options: list[str]
    correct_answer: str
    difficulty: str


class QuizContent(BaseModel):
    target_student: str
    risk_level: str
    weakest_topics: list[str]
    mcqs: list[MCQ]
    coding_problem: str
    conceptual_explanation: str


class StudentAnalysis(BaseModel):
    student_id: int
    attendance: float
    internal_marks: float
    assignment_marks: float
    previous_gpa: float
    topic_scores: dict[str, float]
    pass_probability: float
    risk_level: str
    weak_topics: list[str]


class AdvisorResponse(BaseModel):
    """Structured response from the advisor."""
    response_type: str  # intervention | student_risk | generate_quiz | general
    message: str
    data: Optional[Any] = None
