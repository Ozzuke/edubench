import unittest
import os
import shutil
from click.testing import CliRunner
from src.edubench import cli


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.output_dir = "test_results"
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir)

        # Create a dummy .eduenv file for testing
        with open(".eduenv", "w") as f:
            f.write("API_KEY=dummy_api_key\n")
            f.write("MODEL_NAME=gpt-4o\n")

    def tearDown(self):
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        if os.path.exists(".eduenv"):
            os.remove(".eduenv")

    def test_full_pipeline(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["run", "--output-dir", self.output_dir])

        self.assertEqual(result.exit_code, 0)
        self.assertTrue(
            os.path.exists(os.path.join(self.output_dir, "conversations.jsonl"))
        )
        self.assertTrue(
            os.path.exists(os.path.join(self.output_dir, "evaluations.jsonl"))
        )
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, "report.md")))

        # Basic check of the report content
        with open(os.path.join(self.output_dir, "report.md"), "r") as f:
            report_content = f.read()
            self.assertIn("# EduBench Evaluation Report", report_content)
            self.assertIn("Average Rating:", report_content)
            self.assertIn("Number of Evaluations:", report_content)
            self.assertIn("Student Talk Time:", report_content)
            self.assertIn("Average Words per Turn:", report_content)


if __name__ == "__main__":
    unittest.main()

