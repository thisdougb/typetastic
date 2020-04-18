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


class TestRunLocalCommands(unittest.TestCase):
    """Test running commands locally."""

    def test_run_ls_command(self):
        """Run basic ls command."""

        robot = typetastic.Robot()
        command = "ls tests/data/tt-hello-world.yaml"
        result = robot.run_command(command)

        self.assertEqual(result, 0)

    def test_run_invalid_ls_command(self):
        """Run basic ls command."""

        robot = typetastic.Robot()
        command = "ls []"
        result = robot.run_command(command)

        self.assertNotEqual(result, 0)

    def test_run_valid_command_set(self):
        """Run basic ls command."""

        commands = {
            "config": {"typing-speed": "moderate"},
            "commands": ["echo 'Hello, World!'", "ls"]
        }
        robot = typetastic.Robot()
        robot.data = commands
        result = robot.run()

        self.assertNotEqual(result, 2)

    def test_run_partial_command_set(self):
        """Run basic ls command."""

        commands = {
            "config": {"typing-speed": "moderate"},
            "commands": ["echo 'Hello, World!'", "invalidcommand"]
        }
        robot = typetastic.Robot()
        robot.data = commands
        result = robot.run()

        self.assertEqual(result, 1)


class TestTypeCommands(unittest.TestCase):
    """Test typing commands."""

    def test_default_config(self):
        """Test empty config uses defaults."""
        robot = typetastic.Robot()

        prompt_string = robot.get_config("prompt-string")
        typing_color = robot.get_config("typing-color")
        typing_speed = robot.get_config("typing-speed")

        self.assertEqual(prompt_string, "$ ")
        self.assertEqual(typing_color, "cyan")
        self.assertEqual(typing_speed, "moderate")

    def test_full_config_loaded(self):
        """Test loading config from file."""
        robot = typetastic.Robot()
        data_file = "tests/data/tt-hello-world.yaml"
        robot.load(data_file)

        prompt_string = robot.get_config("prompt-string")
        typing_color = robot.get_config("typing-color")
        typing_speed = robot.get_config("typing-speed")

        self.assertEqual(prompt_string, "% ")
        self.assertEqual(typing_speed, "slow")
        self.assertEqual(typing_color, "red")

    def test_partial_config_loaded(self):
        """Test loading partial config from file preserves defaults."""
        robot = typetastic.Robot()
        data_file = "tests/data/partial-config.yaml"
        robot.load(data_file)

        prompt_string = robot.get_config("prompt-string")
        typing_color = robot.get_config("typing-color")
        typing_speed = robot.get_config("typing-speed")

        self.assertEqual(prompt_string, "$ ")
        self.assertEqual(typing_color, "cyan")
        self.assertEqual(typing_speed, "fast")
