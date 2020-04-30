"""Test Load Commands."""

import copy
import unittest
import typetastic


class TestLoadData(unittest.TestCase):
    """Test Load Command File."""

    def test_load_valid_yaml_file(self):
        """Test loading a valid yaml file."""
        # pylint: disable=protected-access

        test_file = "tests/data/typetastic-simple-command-set.yaml"
        result = typetastic.Robot._load_file(test_file)

        self.assertTrue(result)

    def test_load_invalid_yaml_file(self):
        """Test loading an invalid yaml file."""
        # pylint: disable=protected-access

        test_file = "tests/data/invalid_file.yaml"
        result = typetastic.Robot._load_file(test_file)

        self.assertFalse(result)

    def test_load_valid_yaml_dict(self):
        """Test loading a valid yaml file."""
        # pylint: disable=protected-access

        data = {
            "config": {
                "local-prompt": "$ ",
                "pexpect-delay": 0.2,  # delay required for response to be read
                "prompt-string": "$ ",
                "remote-prompt": "[ssh] $ ",
                "typing-color": "cyan",
                "typing-speed": "moderate"
            },
            "commands": ["echo 'Hello, World!'", "ls"]
        }

        robot = typetastic.Robot()
        robot.load(data)

        robot_data = robot._get_data()
        robot_data["config"] = robot._get_config()

        self.assertEqual(robot_data, data)

    def test_load_invalid_yaml_dict(self):
        """Test loading an invalid yaml file does not change data."""
        # pylint: disable=protected-access
        data = {
            "my": "test dict"
        }
        robot = typetastic.Robot()
        pre_test_copy = copy.deepcopy(robot._get_data())
        robot.load(data)

        self.assertEqual(robot._get_data(), pre_test_copy)

    def test_load_valid_commands_array(self):
        """Test loading a valid array updates commands."""
        # pylint: disable=protected-access
        data = ["echo 'Hello, World!'", "ls"]
        robot = typetastic.Robot()
        robot.load(data)
        robot_data = robot._get_data()

        self.assertEqual(robot_data["commands"], data)

    def test_load_ssh_commands(self):
        """Test loading ssh commands as nested arrays."""
        # pylint: disable=protected-access

        data = ["ls", {"ssh": ["ssh user@host", "ls", "exit"]}, "whoami"]

        robot = typetastic.Robot()
        robot.load(data)
        robot_data = robot._get_data()

        self.assertEqual(robot_data["commands"], data)
