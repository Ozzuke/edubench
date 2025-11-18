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
