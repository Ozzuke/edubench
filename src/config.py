import os
from dotenv import load_dotenv


def load_config(env_file=".eduenv"):
    """
    Loads configuration from a .env file.
    """
    load_dotenv(dotenv_path=env_file)
    return {
        "student": {
            "api_key": os.getenv("STUDENT_API_KEY"),
            "base_url": os.getenv("STUDENT_BASE_URL"),
            "model": os.getenv("STUDENT_MODEL"),
        },
        "teacher": {
            "api_key": os.getenv("TEACHER_API_KEY"),
            "base_url": os.getenv("TEACHER_BASE_URL"),
            "model": os.getenv("TEACHER_MODEL"),
        },
        "grader": {
            "api_key": os.getenv("GRADER_API_KEY"),
            "base_url": os.getenv("GRADER_BASE_URL"),
            "model": os.getenv("GRADER_MODEL"),
        },
        "moderator": {
            "api_key": os.getenv("MODERATOR_API_KEY"),
            "base_url": os.getenv("MODERATOR_BASE_URL"),
            "model": os.getenv("MODERATOR_MODEL"),
        },
        "braintrust": {
            "api_key": os.getenv("BRAINTRUST_API_KEY"),
        }
    }
