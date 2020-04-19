"""Test Load Commands."""

import copy
from io import StringIO
from unittest.mock import patch
import unittest
import sys
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
            "config": {"prompt-string": "$ ", "typing-color": "cyan", "typing-speed": "supersonic"},
            "commands": ["echo 'Hello, World!'", "ls"]
        }
        robot = typetastic.Robot()
        robot.load(data)

        self.assertEqual(robot._get_data(), data)

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


class TestCommandRunner(unittest.TestCase):
    """Test running commands locally."""

    @patch('typetastic.bot_handlers.pause_flow')
    def test_valid_command_set(self, mock_pause_flow):
        """Test successful commands count run in valid set."""
        # pylint: disable=protected-access

        mock_pause_flow.return_value = True

        data = {
            "config": {"typing-speed": "supersonic"},
            "commands": ["echo 'Hello, World!'", "ls /etc/hosts"]
        }
        robot = typetastic.Robot()
        robot.load(data)
        robot.run()

        self.assertEqual(robot._get_successful_commands(), 2)

    def test_partial_command_set(self):
        """Test successful commands count run in partial set."""
        # pylint: disable=protected-access

        data = {
            "config": {"typing-speed": "supersonic"},
            "commands": ["echo 'Hello, World!'", "invalidcommand"]
        }
        robot = typetastic.Robot()
        robot.load(data)
        robot.run()

        self.assertEqual(robot._get_successful_commands(), 1)

    def test_invalid_command_set(self):
        """Test successful commands count run in partial set."""
        # pylint: disable=protected-access

        data_file = "tests/data/typetastic-invalid-command-set.yaml"
        robot = typetastic.Robot()
        robot.load(data_file)
        robot.run()

        print(robot._get_data())

        self.assertEqual(robot._get_successful_commands(), 0)

    @patch('typetastic.bot_handlers.pause_flow')
    def test_meta_command_set(self, mock_pause_flow):
        """Test successful commands count run in meta set."""
        # pylint: disable=protected-access

        mock_pause_flow.return_value = True

        data_file = "tests/data/typetastic-meta-command-set.yaml"
        robot = typetastic.Robot()
        robot.load(data_file)
        robot.run()

        expected_count = len(robot._get_data()["commands"])

        self.assertEqual(robot._get_successful_commands(), expected_count)

    @patch('typetastic.bot_handlers.pause_flow')
    def test_editor_command_set(self, mock_pause_flow):
        """Test successful commands count run in editor set."""
        # pylint: disable=protected-access

        mock_pause_flow.return_value = True

        data_file = "tests/data/typetastic-editor-command-set.yaml"
        robot = typetastic.Robot()
        robot.load(data_file)
        robot.run()

        expected_count = len(robot._get_data()["commands"])

        self.assertEqual(robot._get_successful_commands(), expected_count)

    @patch('typetastic.bot_handlers.pause_flow')
    def test_simple_command_set(self, mock_pause_flow):
        """Test successful commands count run in simple set."""
        # pylint: disable=protected-access

        mock_pause_flow.return_value = True

        data_file = "tests/data/typetastic-simple-command-set.yaml"
        robot = typetastic.Robot()
        robot.load(data_file)
        robot.run()

        expected_count = len(robot._get_data()["commands"])

        self.assertEqual(robot._get_successful_commands(), expected_count)

    @patch('typetastic.bot_handlers.pause_flow')
    def test_chdir_command_set(self, mock_pause_flow):
        """Test successful commands count run in chdir set."""
        # pylint: disable=protected-access

        mock_pause_flow.return_value = True

        data_file = "tests/data/typetastic-chdir-command-set.yaml"
        robot = typetastic.Robot()
        robot.load(data_file)
        robot.run()

        expected_count = len(robot._get_data()["commands"])

        self.assertEqual(robot._get_successful_commands(), expected_count)


class TestConfigLoading(unittest.TestCase):
    """Test loading config and defaults."""

    def test_default_config(self):
        """Test empty config uses defaults."""
        # pylint: disable=protected-access
        robot = typetastic.Robot()

        prompt_string = robot._get_config("prompt-string")
        typing_color = robot._get_config("typing-color")
        typing_speed = robot._get_config("typing-speed")

        self.assertEqual(prompt_string, "$ ")
        self.assertEqual(typing_color, "cyan")
        self.assertEqual(typing_speed, "moderate")

    def test_full_config_loaded_from_file(self):
        """Test loading config from file."""
        # pylint: disable=protected-access

        robot = typetastic.Robot()
        data_file = "tests/data/tt-hello-world.yaml"
        robot.load(data_file)

        prompt_string = robot._get_config("prompt-string")
        typing_color = robot._get_config("typing-color")
        typing_speed = robot._get_config("typing-speed")

        self.assertEqual(prompt_string, "% ")
        self.assertEqual(typing_speed, "supersonic")
        self.assertEqual(typing_color, "red")

    def test_partial_config_loaded(self):
        """Test loading partial config from file preserves defaults."""
        # pylint: disable=protected-access

        robot = typetastic.Robot()
        data_file = "tests/data/partial-config.yaml"
        robot.load(data_file)

        prompt_string = robot._get_config("prompt-string")
        typing_color = robot._get_config("typing-color")
        typing_speed = robot._get_config("typing-speed")

        self.assertEqual(prompt_string, "$ ")
        self.assertEqual(typing_color, "cyan")
        self.assertEqual(typing_speed, "supersonic")


class TestChangeDirCommand(unittest.TestCase):
    """Test changing directory."""

    def test_cd_command(self):
        """Test change dir sets __current_directory."""
        # pylint: disable=protected-access

        data = {
            "config": {"prompt-string": "$ ", "typing-speed": "supersonic"},
            "commands": ["cd /etc"]
        }

        robot = typetastic.Robot()
        robot.load(data)
        robot.run()

        self.assertEqual(robot._get_current_directory(), "/etc")


class TestHelperMethods(unittest.TestCase):
    """Test helper methods."""

    def test_get_command_name(self):
        """Test extracting the name of a command."""
        # pylint: disable=protected-access
        test_commands = [
            "ls:ls",
            "ls:ls -l",
            "ls:ls -l /etc/",
            "ls:/bin/ls -l /etc/",
            "cd:cd ..",
            "ssh:ssh root@somehost",
            "newline:NEWLINE"
        ]

        robot = typetastic.Robot
        for cmd in test_commands:
            (name, full_command) = cmd.split(":", 1)
            self.assertEqual(name, robot._get_command_name(full_command))