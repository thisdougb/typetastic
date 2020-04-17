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
