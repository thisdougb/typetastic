"""Test Load Commands."""

from io import StringIO
from unittest.mock import patch
import unittest
import sys

import typetastic.bot_handlers as bothan


class TestHandlers(unittest.TestCase):
    """Test running commands locally."""

    def setUp(self):

        self.prompt = "$ "
        self.text_color = "\033[1;36m"  # cyan
        self.text_reset = "\033[0;0m"

        self.handler_data = {
            "command": "ls tests/data/typetastic-simple-command-set.yaml",
            "typing_speed": (0, 0, 0),
            "current_directory": None
        }

    def get_string_to_simulate(self, command):
        """Returns the string to simulate."""
        return "{0}{1}{2}{3}".format(self.prompt, self.text_color, command, self.text_reset)

    def test_newline_command(self):
        """Test newline command prints blank line."""

        temp_output = StringIO()

        sys.stdout = temp_output
        bothan.bot_handler_newline(self.handler_data)
        sys.stdout = sys.__stdout__

        self.assertEqual("\n", temp_output.getvalue())

    @patch('typetastic.bot_handlers.pause_flow')
    def test_pause_command(self, mock_pause_flow):
        """Test pause command calls pause_flow()."""

        mock_pause_flow.return_value = True
        bothan.bot_handler_pause(self.handler_data)

        self.assertEqual(mock_pause_flow.call_count, 1)

    def test_run_simple_ls_command(self):
        """Run basic command."""

        result = bothan.run_command("ls /etc/hosts", None)
        self.assertTrue(result)

    def test_run_invalid_ls_command(self):
        """Run basic ls command."""

        result = bothan.run_command("ls [", None)
        self.assertFalse(result)

    @patch('typetastic.bot_handlers.pause_flow')
    def test_editor_command(self, mock_pause_flow):
        """Test editor command calls pause_flow()."""

        mock_pause_flow.return_value = True
        bothan.bot_handler_editor(self.handler_data)

        self.assertEqual(mock_pause_flow.call_count, 1)

    @patch('typetastic.bot_handlers.pause_flow')
    def test_vi_command(self, mock_pause_flow):
        """Test vi command calls pause_flow()."""

        mock_pause_flow.return_value = True
        bothan.bot_handler_vi(self.handler_data)

        self.assertEqual(mock_pause_flow.call_count, 1)

    @patch('typetastic.bot_handlers.pause_flow')
    def test_emacs_command(self, mock_pause_flow):
        """Test emacs command calls pause_flow()."""

        mock_pause_flow.return_value = True
        bothan.bot_handler_emacs(self.handler_data)

        self.assertEqual(mock_pause_flow.call_count, 1)

    @patch('typetastic.bot_handlers.getch.getch')
    def test_pause_flow(self, mock_getch):
        """Test emacs command calls pause_flow()."""

        mock_getch.return_value = True
        bothan.bot_handler_pause(self.handler_data)

        self.assertEqual(mock_getch.call_count, 1)


class TestSimulatedTyping(unittest.TestCase):
    """Test output from simulated typing."""

    def setUp(self):

        self.prompt = "$ "
        self.text_color = "\033[1;36m"  # cyan
        self.text_reset = "\033[0;0m"

        self.handler_data = {
            "command": "ls tests/data/typetastic-simple-command-set.yaml",
            "typing_speed": (0, 0, 0),
            "current_directory": None
        }

    def get_string_to_simulate(self, command):
        """Returns the string to simulate."""
        return "{0}{1}{2}{3}".format(self.prompt, self.text_color, command, self.text_reset)

    def test_simulate_plain_text(self):
        """Test the typing simulation returns the correct plain text."""

        temp_output = StringIO()

        sys.stdout = temp_output
        bothan.simulate_typing("this is plain text", 0, 0, 0)
        sys.stdout = sys.__stdout__

        self.assertEqual("this is plain text\n", temp_output.getvalue())

    def test_simulate_text_with_color(self):
        """Test the typing simulation returns the correct colored text."""

        temp_output = StringIO()
        text_with_color = self.get_string_to_simulate("this is colored text")
        print(text_with_color)

        sys.stdout = temp_output
        bothan.simulate_typing(text_with_color, 0, 0, 0)
        sys.stdout = sys.__stdout__

        self.assertEqual("{0}\n".format(text_with_color), temp_output.getvalue())

    def test_emit_prompt(self):
        """Test emit prompt emits the prompt."""

        temp_output = StringIO()

        sys.stdout = temp_output
        bothan.emit_prompt("$ ")
        sys.stdout = sys.__stdout__

        self.assertEqual("$ ", temp_output.getvalue())
