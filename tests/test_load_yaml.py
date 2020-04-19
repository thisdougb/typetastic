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

        test_file = "tests/data/tt-hello-world.yaml"
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


class TestRunLocalCommands(unittest.TestCase):
    """Test running commands locally."""

    def test_run_ls_command(self):
        """Run basic ls command."""
        # pylint: disable=protected-access

        robot = typetastic.Robot()
        command = "ls tests/data/tt-hello-world.yaml"
        current_directory = None
        result = robot._run_command(command, current_directory)

        self.assertTrue(result)

    def test_run_invalid_ls_command(self):
        """Run basic ls command."""
        # pylint: disable=protected-access

        robot = typetastic.Robot()
        command = "ls []"
        current_directory = None
        result = robot._run_command(command, current_directory)

        self.assertFalse(result)

    @patch('typetastic.Robot._pause_flow')
    def test_run_valid_command_set(self, mock_pause_flow):
        """Run basic ls command."""
        # pylint: disable=protected-access

        mock_pause_flow.return_value = True

        data_file = "tests/data/tt-list-of-commands-for-test.yaml"
        robot = typetastic.Robot()
        robot.load(data_file)
        robot.run()

        expected_count = len(robot._get_data()["commands"])
        self.assertEqual(robot._get_successful_commands(), expected_count)

    def test_run_partial_command_set(self):
        """Run basic ls command."""
        # pylint: disable=protected-access

        commands = {
            "config": {"typing-speed": "supersonic"},
            "commands": ["echo 'Hello, World!'", "invalidcommand"]
        }
        robot = typetastic.Robot()
        robot.load(commands)
        robot.run()

        self.assertEqual(robot._get_successful_commands(), 1)


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


class TestPrintingCommands(unittest.TestCase):
    """Test printing command strings.

    string_to_type is somewhat confusing, need a better name.
    """

    def test_string_to_type_echo_hello_world(self):
        """Test command string format for typing."""
        # pylint: disable=protected-access

        robot = typetastic.Robot()
        config = {"prompt-string": "$ ", "typing-color": "cyan"}
        command = "echo 'Hello, World!'"

        result = robot._string_to_type(config, command)
        expected_result = "\x1b[1;36mecho 'Hello, World!'\x1b[0;0m"

        self.assertEqual(result, expected_result)

    def test_string_to_type_with_no_color_config(self):
        """Test command string format for typing."""
        # pylint: disable=protected-access

        robot = typetastic.Robot()
        config = {"prompt-string": "$ "}
        command = "echo 'Hello, World!'"

        result = robot._string_to_type(config, command)
        expected_result = "echo 'Hello, World!'"

        self.assertEqual(result, expected_result)

    def test_ls_command_response(self):
        """Test command string format for typing."""

        temp_output = StringIO()
        commands = {
            "config": {"prompt-string": "$ ", "typing-color": "cyan", "typing-speed": "supersonic"},
            "commands": ["ls tests/data/tt-hello-world.yaml"]
        }

        robot = typetastic.Robot()
        robot.load(commands)

        sys.stdout = temp_output
        robot.run()
        sys.stdout = sys.__stdout__

        (cmd, response, _) = temp_output.getvalue().split("\n", 2)

        self.assertEqual(cmd, "$ \x1b[1;36mls tests/data/tt-hello-world.yaml\x1b[0;0m")
        self.assertEqual(response, "tests/data/tt-hello-world.yaml\r")


class TestMetaCommands(unittest.TestCase):
    """Test typetastic meta commands."""

    def test_newline_command(self):
        """Test newline command."""

        temp_output = StringIO()
        commands = {
            "config": {"prompt-string": "$ ", "typing-speed": "supersonic"},
            "commands": ["NEWLINE"]
        }

        robot = typetastic.Robot()
        robot.load(commands)

        sys.stdout = temp_output
        robot.run()
        sys.stdout = sys.__stdout__

        self.assertEqual(temp_output.getvalue(), "$ \n$ \n")

    @patch('typetastic.Robot._pause_flow')
    def test_pause_command(self, mock_pause_flow):
        """Test pause command."""
        mock_pause_flow.return_value = True

        data = {
            "config": {"prompt-string": "$ ", "typing-speed": "supersonic"},
            "commands": ["PAUSE"]
        }

        robot = typetastic.Robot()
        robot.load(data)
        robot.run()

        self.assertEqual(mock_pause_flow.call_count, 1)


class TestEditorCommands(unittest.TestCase):
    """Test typetastic meta commands."""

    def test_newline_command(self):
        """Test command string format for typing."""
        # pylint: disable=protected-access

        robot = typetastic.Robot()

        self.assertTrue(robot._is_editor("vi test"))
        self.assertTrue(robot._is_editor("vim test"))
        self.assertTrue(robot._is_editor("emacs test"))

        self.assertFalse(robot._is_editor("ls test"))

    @patch('typetastic.Robot._pause_flow')
    def test_run_editor_command(self, mock_pause_flow):
        """Test running an editor command causes PAUSE."""

        mock_pause_flow.return_value = True
        data = {
            "config": {"prompt-string": "$ ", "typing-speed": "supersonic"},
            "commands": ["vi test"]
        }

        robot = typetastic.Robot()
        robot.load(data)
        robot.run()

        self.assertEqual(mock_pause_flow.call_count, 1)


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
            "ssh:ssh root@somehost"
        ]

        robot = typetastic.Robot
        for cmd in test_commands:
            (name, full_command) = cmd.split(":", 1)
            self.assertEqual(name, robot._get_command_name(full_command))
