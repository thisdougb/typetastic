"""Test Load Commands."""

import unittest

import typetastic.session_config


class TestSessionConfig(unittest.TestCase):
    """Test running commands locally."""

    def setUp(self):

        self.reference_config = {
            "typing-color": "cyan",
            "typing-speed": "moderate",
            "local-prompt": "$ ",
            "remote-prompt": "[ssh] $ ",
            "prompt-string": "$ ",
        }

    def test_default_config(self):
        """Test get_config returns correct defaults."""

        session_config = typetastic.session_config.SessionConfig()
        config = session_config.get()

        self.assertEqual(config, self.reference_config)

    def test_set_config_key(self):
        """Test set_config returns modified configuration."""

        session_config = typetastic.session_config.SessionConfig()
        session_config.set("typing-color", "green")
        color = session_config.get(key="typing-color")

        self.assertEqual(color, "green")
