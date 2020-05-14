"""Test Command Runner."""

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

    @patch('typetastic.bot_handlers.bot_handler_default')
    def test_valid_command_runs(self, mock_bot_handler_default):
        """Test valid ls command calls default handler."""
        # pylint: disable=protected-access

        mock_bot_handler_default.return_value = True

        self.robot.load(["ls /etc/hosts"])
        self.robot.run()

        self.assertEqual(mock_bot_handler_default.call_count, 1)
        self.assertEqual(self.robot._get_successful_commands(), 1)

    @patch('typetastic.bot_handlers.bot_handler_default')
    def test_invalid_command_fails(self, mock_bot_handler_default):
        """Test invalid ls command calls default handler."""
        # pylint: disable=protected-access

        mock_bot_handler_default.return_value = False

        self.robot.load(["ls ["])
        self.robot.run()

        self.assertEqual(mock_bot_handler_default.call_count, 1)
        self.assertEqual(self.robot._get_successful_commands(), 0)

    @patch('typetastic.bot_handlers.pause_flow')
    def test_meta_pause_command_calls_handler(self, mock_pause_flow):
        """Test meta command PAUSE calls correct bot handler."""
        # pylint: disable=protected-access

        mock_pause_flow.return_value = True

        self.robot.load(["PAUSE"])
        self.robot.run()

        self.assertEqual(mock_pause_flow.call_count, 1)
        self.assertEqual(self.robot._get_successful_commands(), 1)

    @patch('typetastic.bot_handlers.bot_handler_editor')
    def test_editor_command(self, mock_bot_handler_editor):
        """Test vi command calls the correct handler."""
        # pylint: disable=protected-access

        mock_bot_handler_editor.return_value = True

        self.robot.load(["vi /tmp/test.txt"])
        self.robot.run()

        self.assertEqual(mock_bot_handler_editor.call_count, 1)

    @patch('typetastic.bot_handlers.pause_flow')
    def test_simple_command_set(self, mock_pause_flow):
        """Test all commands loaded from file run successfully."""
        # pylint: disable=protected-access

        mock_pause_flow.return_value = True

        data_file = "tests/data/typetastic-simple-command-set.yaml"
        self.robot.load(data_file)
        self.robot.run()

        expected_count = len(self.robot._get_data()["commands"])
        self.assertEqual(self.robot._get_successful_commands(), expected_count)

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


class TestSSHCommandRunner(unittest.TestCase):
    """Test SSH commands in the command runner method."""

    def setUp(self):
        """Configure the context."""

        # set pexpect-delay to 0 to speed up tests
        session_config = typetastic.session_config.SessionConfig()
        session_config.set("pexpect-delay", 0)
        session_config.set("typing-speed", "supersonic")
        config = {"config": session_config.get()}

        self.robot = typetastic.Robot()
        self.robot.load(config)

    @patch('typetastic.robot.pexpect.pxssh.pxssh.login')
    def test_ssh_login_command(self, mock_ssh):
        """Test ssh login command calls correct bot handler."""
        # pylint: disable=protected-access

        mock_ssh.return_value = True

        self.robot.load([{"ssh": ["ssh user@somehost.com"]}])
        self.robot.run()
        self.assertEqual(mock_ssh.call_count, 1)

    @patch('typetastic.bot_handlers.bot_handler_default')
    def test_run_task_with_handler(self, mock_default_handler):
        """Test run_task with handler_data using ls command."""

        handler_data = {
            "remote": None,
            "command": "ls",
            "typing_speed": (0, 0, 0),
            "config": {"prompt-string": "$ ", "typing-color": "cyan", "typing-speed": "supersonic"}
        }

        mock_default_handler.return_value = True
        expected_simulated_text = "\x1b[0;36mls\x1b[0;0m"

        robot = typetastic.Robot
        result = robot.run_task(handler_data)

        self.assertTrue(result)
        self.assertTrue("simulated_typing" in handler_data)
        self.assertEqual(handler_data["simulated_typing"], expected_simulated_text)

    @patch('typetastic.bot_handlers.bot_handler_default')
    def test_run_task_with_handler_is_bold_text(self, mock_default_handler):
        """Test run task with bold text."""

        handler_data = {
            "remote": None,
            "command": "ls",
            "typing_speed": (0, 0, 0),
            "config": {
                "prompt-string": "$ ",
                "typing-color": "bold-green",
                "typing-speed": "supersonic"
            }
        }

        mock_default_handler.return_value = True
        expected_simulated_text = "\x1b[1;32mls\x1b[0;0m"

        robot = typetastic.Robot
        result = robot.run_task(handler_data)

        self.assertTrue(result)
        self.assertTrue("simulated_typing" in handler_data)
        self.assertEqual(handler_data["simulated_typing"], expected_simulated_text)

    @patch('typetastic.bot_handlers.bot_handler_default')
    def test_run_task_with_handler_is_bright_text(self, mock_default_handler):
        """Test run_task with bright text."""

        handler_data = {
            "remote": None,
            "command": "ls",
            "typing_speed": (0, 0, 0),
            "config": {
                "prompt-string": "$ ",
                "typing-color": "bright-green",
                "typing-speed":
                "supersonic"
            }
        }

        mock_default_handler.return_value = True
        expected_simulated_text = "\x1b[0;92mls\x1b[0;0m"

        robot = typetastic.Robot
        result = robot.run_task(handler_data)

        self.assertTrue(result)
        self.assertTrue("simulated_typing" in handler_data)
        self.assertEqual(handler_data["simulated_typing"], expected_simulated_text)

    @patch('typetastic.bot_handlers.bot_handler_default')
    def test_run_task_with_handler_is_bold_bright_text(self, mock_default_handler):
        """Test run_task with bold and bright text."""

        handler_data = {
            "remote": None,
            "command": "ls",
            "typing_speed": (0, 0, 0),
            "config": {
                "prompt-string": "$ ",
                "typing-color": "bold-bright-green",
                "typing-speed":
                "supersonic"
            }
        }

        mock_default_handler.return_value = True
        expected_simulated_text = "\x1b[1;92mls\x1b[0;0m"

        robot = typetastic.Robot
        result = robot.run_task(handler_data)

        self.assertTrue(result)
        self.assertTrue("simulated_typing" in handler_data)
        self.assertEqual(handler_data["simulated_typing"], expected_simulated_text)


class TestChangeDirCommand(unittest.TestCase):
    """Test changing directory."""

    def setUp(self):

        self.prompt = "$ "
        self.text_color = "\033[1;36m"  # cyan
        self.text_reset = "\033[0;0m"

        self.handler_data = {
            "remote": None,
            "command": "cd /etc",
            "get_exit_status": True,
            "typing_speed": (0, 0, 0),
            "local": None,
            "config": {
                "prompt-string": "$ ",
                "typing-color": "cyan",
                "typing-speed": "supersonic"
            },
        }

        shell = typetastic.Robot.setup_shell(self.prompt)
        self.handler_data["local"] = shell

    def test_cd_command(self):
        """Test change dir return true."""
        # pylint: disable=protected-access

        self.handler_data["command"] = "cd /etc"
        robot = typetastic.Robot()

        self.assertTrue(robot.run_task(self.handler_data))

    def test_cd_command_bad_dir(self):
        """Test change dir return true."""
        # pylint: disable=protected-access

        self.handler_data["command"] = "cd ["
        robot = typetastic.Robot()

        self.assertFalse(robot.run_task(self.handler_data))


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
