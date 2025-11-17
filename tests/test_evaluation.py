import unittest
from unittest.mock import AsyncMock
from src.evaluation import (
    evaluate_conversation_with_grader,
    calculate_student_talk_time,
    calculate_average_words_per_turn,
)
from src.datastructures import Conversation, Exchange, EvaluationResult


class TestEvaluation(unittest.TestCase):
    def setUp(self):
        self.conversation = Conversation(
            id="conv1",
            scenario="scenario1",
            student="student1",
            exchanges=[
                Exchange(
                    speaker="Student", message="Hello teacher! How are you?"
                ),  # 5 words
                Exchange(
                    speaker="Teacher", message="I am fine, thank you. And you?"
                ),  # 7 words
                Exchange(speaker="Student", message="I am good too."),  # 4 words
                Exchange(
                    speaker="Teacher", message="Great! Let's start the lesson."
                ),  # 6 words
            ],
        )

    async def test_evaluate_conversation_with_grader(self):
        conversation = Conversation(
            id="conv1",
            scenario="scenario1",
            student="student1",
            exchanges=[
                Exchange(speaker="Student", message="Hello teacher!"),
                Exchange(speaker="Teacher", message="Hello student!"),
            ],
        )

        # Mock the grader model
        grader_model = AsyncMock()
        grader_model.chat.completions.create.return_value.choices[0].message.tool_calls[
            0
        ].function.arguments = (
            '{"rating": 8.5, "reasoning": "The teacher was very clear and supportive."}'
        )

        evaluation_result = await evaluate_conversation_with_grader(
            conversation, grader_model
        )

        self.assertIsInstance(evaluation_result, EvaluationResult)
        self.assertEqual(evaluation_result.conversation_id, "conv1")
        self.assertEqual(evaluation_result.rating, 8.5)
        self.assertEqual(
            evaluation_result.reasoning, "The teacher was very clear and supportive."
        )

    def test_calculate_student_talk_time(self):
        student_talk_time = calculate_student_talk_time(self.conversation)
        # Student words: 5 + 4 = 9
        # Teacher words: 7 + 6 = 13
        # Total words: 22
        # Student talk time: 9 / 22 = 0.4090...
        self.assertAlmostEqual(student_talk_time, 9 / 22)

    def test_calculate_average_words_per_turn(self):
        avg_words_per_turn = calculate_average_words_per_turn(self.conversation)
        # Total words: 22
        # Total turns: 4
        # Average words per turn: 22 / 4 = 5.5
        self.assertEqual(avg_words_per_turn, 5.5)


if __name__ == "__main__":
    unittest.main()
