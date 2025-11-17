import unittest
import os
from src.scenarios import (
    load_student,
    load_scenario,
    load_all_students,
    load_all_scenarios,
)
from src.datastructures import Student, Scenario


class TestScenarios(unittest.TestCase):
    def setUp(self):
        self.students_dir = "data/students"
        self.scenarios_dir = "data/scenarios"

    def test_load_all_students(self):
        students = load_all_students(self.students_dir)
        self.assertEqual(len(students), 2)
        self.assertIsInstance(students[0], Student)

    def test_load_all_scenarios(self):
        scenarios = load_all_scenarios(self.scenarios_dir)
        self.assertEqual(len(scenarios), 2)
        self.assertIsInstance(scenarios[0], Scenario)

    def test_load_student(self):
        student = load_student(os.path.join(self.students_dir, "student1.yaml"))
        self.assertIsInstance(student, Student)
        self.assertEqual(student.id, "student1")
        self.assertEqual(
            student.system_prompt, "You are a helpful student.\nYou are in 11th grade."
        )

    def test_load_scenario(self):
        scenario = load_scenario(os.path.join(self.scenarios_dir, "scenario1.yaml"))
        self.assertIsInstance(scenario, Scenario)
        self.assertEqual(scenario.id, "scenario1")
        self.assertEqual(scenario.grade_band, 11)
        self.assertEqual(
            scenario.initial_message,
            r"i have this stupid ahh integral, pls solve: \int{2x^3 dx}",
        )


if __name__ == "__main__":
    unittest.main()
