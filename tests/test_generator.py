import unittest
import asyncio
from unittest.mock import AsyncMock
from src.generator import generate_conversation
from src.datastructures import Student, Scenario, Conversation


class TestGenerator(unittest.TestCase):
    def test_generate_conversation(self):
        student = Student(id="student1", system_prompt="You are a helpful student.")
        scenario = Scenario(
            id="scenario1", grade_band=11, initial_message="Start the conversation."
        )

        # Mock the teacher and student models
        teacher_model = AsyncMock()
        teacher_model.chat.completions.create.return_value.choices[
            0
        ].message.content = "The teacher's response."
        student_model = AsyncMock()
        student_model.chat.completions.create.return_value.choices[
            0
        ].message.content = "The student's response."

        conversation = asyncio.run(
            generate_conversation(
                student, scenario, teacher_model, student_model, max_turns=2
            )
        )

        self.assertIsInstance(conversation, Conversation)
        self.assertEqual(conversation.student, student.id)
        self.assertEqual(conversation.scenario, scenario.id)
        # 1 initial student message + 2 turns of (teacher + student)
        self.assertEqual(len(conversation.exchanges), 5)
        self.assertEqual(conversation.exchanges[0].speaker, "Student")
        self.assertEqual(conversation.exchanges[1].speaker, "Teacher")
        self.assertEqual(conversation.exchanges[2].speaker, "Student")
        self.assertEqual(conversation.exchanges[3].speaker, "Teacher")
        self.assertEqual(conversation.exchanges[4].speaker, "Student")


if __name__ == "__main__":
    unittest.main()
