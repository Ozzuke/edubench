from pydantic import BaseModel
from typing import List


class Exchange(BaseModel):
    speaker: str  # "Student" or "Teacher"
    message: str


class Conversation(BaseModel):
    id: str
    scenario: str
    student: str
    exchanges: List[Exchange]


class Student(BaseModel):
    id: str
    system_prompt: str


class Teacher(BaseModel):
    id: str
    system_prompt: str


class Scenario(BaseModel):
    id: str
    grade_band: int
    initial_message: str


class EvaluationResult(BaseModel):
    conversation_id: str
    rating: float
    reasoning: str
    first_mile_score: float = 0.0
    retrieval_score: float = 0.0
    reflect_revisit_score: float = 0.0
    interleaved_practice_score: float = 0.0
    guided_examples_score: float = 0.0
    high_quality_feedback_score: float = 0.0
    socratic_reasoning_score: float = 0.0
    misconception_diagnosis_score: float = 0.0
    motivation_relevance_score: float = 0.0
    beliefs_attributions_score: float = 0.0
