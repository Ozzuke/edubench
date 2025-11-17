import json
from openai import AsyncOpenAI
from src.datastructures import Conversation, EvaluationResult

PROMPT = """
You are comparing a student's answer to a teacher's answer in a dialog. Here is the data:
[BEGIN DATA]
************
[Conversation]:
{conversation_text}
************
[END DATA]

Please rate the teacher's effectiveness in teaching the student on a scale of 1 to 10.
Provide your answer in the following structured format:
Rating: <numeric_rating>
Reasoning: <your_reasoning>
"""


async def evaluate_conversation_with_grader(
    conversation: Conversation,
    grader: AsyncOpenAI,
    grader_model_name: str,
) -> EvaluationResult:
    """
    Evaluates a single conversation using a grader LLM.
    """
    conversation_text = "\n".join(
        f"[{exchange.speaker}]: {exchange.message}"
        for exchange in conversation.exchanges
    )

    response = await grader.chat.completions.create(
        model=grader_model_name,
        messages=[
            {
                "role": "user",
                "content": PROMPT.format(conversation_text=conversation_text),
            }
        ],
        temperature=0,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "rate",
                    "description": "Rate the teacher's effectiveness and provide reasoning.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "reasons": {
                                "description": "Write out in a step-by-step manner your reasoning to ensure the conclusion is correct.",
                                "type": "string",
                            },
                            "rating": {
                                "description": "The numeric rating on a scale of 1 to 10.",
                                "type": "number",  # Changed to number to allow for float ratings
                                "minimum": 1,
                                "maximum": 10,
                            },
                        },
                        "required": ["rating", "reasons"],
                    },
                },
            }
        ],
        tool_choice={"type": "function", "function": {"name": "rate"}},
    )
    arguments = json.loads(response.choices[0].message.tool_calls[0].function.arguments)

    return EvaluationResult(
        conversation_id=conversation.id,
        rating=arguments["rating"],
        reasoning=arguments["reasons"],
    )


def calculate_student_talk_time(conversation: Conversation) -> float:
    """
    Calculates the percentage of words uttered by the student relative to the total number of words in the dialogue.
    """
    student_words = 0
    total_words = 0
    for exchange in conversation.exchanges:
        words = len(exchange.message.split())
        total_words += words
        if exchange.speaker == "Student":
            student_words += words

    if total_words == 0:
        return 0.0
    return student_words / total_words


def calculate_average_words_per_turn(conversation: Conversation) -> float:
    """
    Calculates the average number of words per turn in the conversation.
    """
    total_words = 0
    total_turns = len(conversation.exchanges)
    for exchange in conversation.exchanges:
        words = len(exchange.message.split())
        total_words += words

    if total_turns == 0:
        return 0.0
    return total_words / total_turns
