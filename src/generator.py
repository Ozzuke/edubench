from typing import Any
from src.datastructures import Student, Scenario, Conversation, Exchange, Teacher
from openai import AsyncOpenAI

MODERATOR_PROMPT = """
You are a moderator for a conversation between a student and a teacher.
Your task is to determine if the conversation has reached a natural conclusion.
The conversation is about a specific topic, and the student is trying to learn.
The conversation should stop if the student has understood the topic, or if the conversation is going in circles, or if it seems like student and teacher model try to teach each other.
The conversation should also stop if the student and teacher say goodbye to each other.

Here is the conversation so far:
{conversation_history}

Do you think the conversation should stop?
Answer with only one word: "STOP" or "CONTINUE".
"""


async def generate_conversation(
    student: Student,
    scenario: Scenario,
    teacher: Teacher,
    teacher_model: Any,
    student_model: Any,
    moderator_model: Any,
    student_model_name: str,
    teacher_model_name: str,
    moderator_model_name: str,
    max_turns: int = 10,
) -> Conversation:
    """
    Generates a conversation between a student and a teacher.
    """
    exchanges: list[Exchange] = []

    # The initial student message is directly from the scenario
    student_message = scenario.initial_message
    exchanges.append(Exchange(speaker="Student", message=student_message))

    # System prompts for student and teacher
    student_system_prompt = student.system_prompt
    teacher_system_prompt = teacher.system_prompt

    # Initialize message histories for both models
    student_messages = [
        {"role": "system", "content": student_system_prompt},
    ]
    teacher_messages = [
        {"role": "system", "content": teacher_system_prompt},
        {"role": "user", "content": student_message},
    ]

    for _ in range(max_turns):
        # Teacher's turn
        teacher_response = await teacher_model.chat.completions.create(
            model=teacher_model_name,
            messages=teacher_messages,
        )
        teacher_message = teacher_response.choices[0].message.content
        exchanges.append(Exchange(speaker="Teacher", message=teacher_message))
        student_messages.append({"role": "assistant", "content": student_message})
        student_messages.append({"role": "user", "content": teacher_message})
        teacher_messages.append({"role": "assistant", "content": teacher_message})

        # Student's turn
        student_response = await student_model.chat.completions.create(
            model=student_model_name,
            messages=student_messages,
        )
        student_message = student_response.choices[0].message.content
        exchanges.append(Exchange(speaker="Student", message=student_message))
        teacher_messages.append({"role": "user", "content": student_message})

        # Moderator's turn
        conversation_history = "\n".join(
            [f"{ex.speaker}: {ex.message}" for ex in exchanges]
        )
        moderator_response = await moderator_model.chat.completions.create(
            model=moderator_model_name,
            messages=[
                {
                    "role": "user",
                    "content": MODERATOR_PROMPT.format(
                        conversation_history=conversation_history
                    ),
                }
            ],
            max_tokens=5,
        )
        moderator_decision = moderator_response.choices[0].message.content.strip().upper()
        if "STOP" in moderator_decision:
            break

    return Conversation(
        id=f"{student.id}_{scenario.id}",
        student=student.id,
        scenario=scenario.id,
        exchanges=exchanges,
    )
