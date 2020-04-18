"""Test Load Commands."""

import unittest
import typetastic


class TestLoadFile(unittest.TestCase):
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


class TestRunLocalCommands(unittest.TestCase):
    """Test running commands locally."""

    def test_run_ls_command(self):
        """Run basic ls command."""
        # pylint: disable=protected-access

        robot = typetastic.Robot()
        command = "ls tests/data/tt-hello-world.yaml"
        result = robot._run_command(command)

        self.assertEqual(result, 0)

    def test_run_invalid_ls_command(self):
        """Run basic ls command."""
        # pylint: disable=protected-access

        robot = typetastic.Robot()
        command = "ls []"
        result = robot._run_command(command)

        self.assertNotEqual(result, 0)

    def test_run_valid_command_set(self):
        """Run basic ls command."""

        commands = {
            "config": {"typing-color": "cyan", "typing-speed": "supersonic"},
            "commands": ["echo 'Hello, World!'", "ls"]
        }
        robot = typetastic.Robot()
        robot.data = commands
        result = robot.run()

        self.assertNotEqual(result, 2)

    def test_run_partial_command_set(self):
        """Run basic ls command."""

        commands = {
            "config": {"typing-speed": "supersonic"},
            "commands": ["echo 'Hello, World!'", "invalidcommand"]
        }
        robot = typetastic.Robot()
        robot.data = commands
        result = robot.run()

        self.assertEqual(result, 1)


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

    def test_full_config_loaded(self):
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
    """Test printing command strings."""

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
