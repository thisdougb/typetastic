"""Test Python Command Runner.

Note, this is excluded from CircleCI running Python interactive seems to hang.
"""

from unittest.mock import patch
import unittest
import typetastic


class TestCommandRunner(unittest.TestCase):
    """Test the command runner method."""

    def setUp(self):

        # set pexpect-delay to 0 to speed up tests
        session_config = typetastic.session_config.SessionConfig()
        session_config.set("pexpect-delay", 0)

        self.robot = typetastic.Robot()
        self.robot.load(session_config.get())


class TestPythonCommandRunner(unittest.TestCase):
    """Test Python shell commands in the command runner method."""

    def setUp(self):
        """Configure the context."""

        # set pexpect-delay to 0 to speed up tests
        session_config = typetastic.session_config.SessionConfig()
        session_config.set("pexpect-delay", 0)
        session_config.set("typing-speed", "supersonic")
        config = {"config": session_config.get()}

        self.robot = typetastic.Robot()
        self.robot.load(config)

    def test_python_command_set(self):
        """Test successful commands count running python set."""
        # pylint: disable=protected-access

        data_file = "tests/data/typetastic-python-command-set.yaml"

        robot = typetastic.Robot()
        robot.load(data_file)
        robot.run()

        self.assertEqual(robot._get_successful_commands(), 5)
