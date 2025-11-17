import unittest
from src.datastructures import (
    Exchange,
    Conversation,
    Student,
    Scenario,
    EvaluationResult,
)


class TestDataStructures(unittest.TestCase):
    def test_exchange(self):
        exchange = Exchange(speaker="Student", message="Hello")
        self.assertEqual(exchange.speaker, "Student")
        self.assertEqual(exchange.message, "Hello")

    def test_conversation(self):
        conversation = Conversation(
            id="conv1",
            scenario="scenario1",
            student="student1",
            exchanges=[Exchange(speaker="Student", message="Hello")],
        )
        self.assertEqual(conversation.id, "conv1")
        self.assertEqual(conversation.scenario, "scenario1")
        self.assertEqual(conversation.student, "student1")
        self.assertEqual(len(conversation.exchanges), 1)

    def test_student(self):
        student = Student(id="student1", system_prompt="You are a helpful student.")
        self.assertEqual(student.id, "student1")
        self.assertEqual(student.system_prompt, "You are a helpful student.")

    def test_scenario(self):
        scenario = Scenario(
            id="scenario1",
            grade_band=11,
            initial_message=r"i have this stupid ahh integral, pls solve: \int{2x^3 dx}",
        )
        self.assertEqual(scenario.id, "scenario1")
        self.assertEqual(scenario.grade_band, 11)
        self.assertEqual(
            scenario.initial_message,
            r"i have this stupid ahh integral, pls solve: \int{2x^3 dx}",
        )

    def test_evaluation_result(self):
        evaluation_result = EvaluationResult(
            conversation_id="conv1", rating=4.5, reasoning="The teacher was helpful."
        )
        self.assertEqual(evaluation_result.conversation_id, "conv1")
        self.assertEqual(evaluation_result.rating, 4.5)
        self.assertEqual(evaluation_result.reasoning, "The teacher was helpful.")


if __name__ == "__main__":
    unittest.main()
