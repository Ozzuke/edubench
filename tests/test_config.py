import os
import unittest
from src.config import load_config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.test_env_file = ".test_eduenv"
        with open(self.test_env_file, "w") as f:
            f.write("API_KEY=test_api_key\n")
            f.write("MODEL_NAME=test_model_name\n")

    def tearDown(self):
        os.remove(self.test_env_file)

    def test_load_config(self):
        config = load_config(self.test_env_file)
        self.assertEqual(config["API_KEY"], "test_api_key")
        self.assertEqual(config["MODEL_NAME"], "test_model_name")


if __name__ == "__main__":
    unittest.main()
