"""Test Load Commands."""

import unittest
import typetastic


class TestLoadFile(unittest.TestCase):
    """Test Load Command File."""

    def test_load_valid_yaml_file(self):
        """Test loading a valid yaml file."""

        test_file = "tests/data/tt-hello-world.yaml"
        result = typetastic.Robot.load_file(test_file)

        self.assertTrue(result)

    def test_load_invalid_yaml_file(self):
        """Test loading an invalid yaml file."""

        test_file = "tests/data/invalid_file.yaml"
        result = typetastic.Robot.load_file(test_file)

        self.assertFalse(result)
