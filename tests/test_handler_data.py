"""Test Handler Data Class."""

import unittest

import typetastic.handler_data


class TestHandlerDataClass(unittest.TestCase):
    """Test HandlerData class."""

    def setUp(self):

        self.reference_dict = {
            "remote": None,
            "local": None,
            "command": None,
            "typing_speed": None,
            "config": None,
            "get_exit_status": True
        }

    def test_default_data(self):
        """Test get_data returns correct defaults."""

        handler_data = typetastic.handler_data.HandlerData()
        data = handler_data.get()

        self.assertEqual(data, self.reference_dict)

    def test_set_data_key(self):
        """Test set_config returns modified data."""

        handler_data = typetastic.handler_data.HandlerData()
        handler_data.set("command", "ls -l")
        command = handler_data.get(key="command")

        self.assertEqual(command, "ls -l")

    def test_get_typing_speed(self):
        """Test get typing speeds return correct values for slow typing."""
        # pylint: disable=protected-access

        slow_typing = [0.1, 0.4, 1.0]

        result = typetastic.handler_data.HandlerData._get_typing_speeds("slow")
        self.assertEqual(result, slow_typing)
