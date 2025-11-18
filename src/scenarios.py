import yaml
import os
from typing import List
from src.datastructures import Student, Scenario, Teacher


def load_student(file_path: str) -> Student:
    """
    Loads a student from a YAML file.
    """
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
    return Student(**data)


def load_all_students(directory: str) -> List[Student]:
    """
    Loads all students from a directory of YAML files.
    """
    students = []
    for filename in os.listdir(directory):
        if filename.endswith(".yaml"):
            file_path = os.path.join(directory, filename)
            students.append(load_student(file_path))
    return students


def load_teacher(file_path: str) -> Teacher:
    """
    Loads a teacher from a YAML file.
    """
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
    return Teacher(**data)


def load_scenario(file_path: str) -> Scenario:
    """
    Loads a scenario from a YAML file.
    """
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
    return Scenario(**data)


def load_all_scenarios(directory: str) -> List[Scenario]:
    """
    Loads all scenarios from a directory of YAML files.
    """
    scenarios = []
    for filename in os.listdir(directory):
        if filename.endswith(".yaml"):
            file_path = os.path.join(directory, filename)
            scenarios.append(load_scenario(file_path))
    return scenarios
