import unittest
from src.reporting import aggregate_results, generate_markdown_report
from src.datastructures import EvaluationResult


class TestReporting(unittest.TestCase):
    def test_aggregate_results(self):
        evaluation_results = [
            EvaluationResult(conversation_id="conv1", rating=7.0, reasoning="Good"),
            EvaluationResult(
                conversation_id="conv2", rating=8.0, reasoning="Excellent"
            ),
            EvaluationResult(conversation_id="conv3", rating=6.0, reasoning="Fair"),
        ]

        aggregated_data = aggregate_results(evaluation_results)
        self.assertIn("average_rating", aggregated_data)
        self.assertAlmostEqual(aggregated_data["average_rating"], 7.0)
        self.assertIn("num_evaluations", aggregated_data)
        self.assertEqual(aggregated_data["num_evaluations"], 3)

    def test_generate_markdown_report(self):
        aggregated_data = {
            "average_rating": 7.5,
            "num_evaluations": 10,
            "metrics": {"student_talk_time": 0.45, "average_words_per_turn": 7.2},
        }
        report = generate_markdown_report(aggregated_data)
        self.assertIsInstance(report, str)
        self.assertIn("# EduBench Evaluation Report", report)
        self.assertIn("Average Rating: 7.5", report)
        self.assertIn("Number of Evaluations: 10", report)
        self.assertIn("Student Talk Time: 45.00%", report)
        self.assertIn("Average Words per Turn: 7.20", report)


if __name__ == "__main__":
    unittest.main()
