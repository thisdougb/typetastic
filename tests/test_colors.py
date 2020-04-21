"""Test Load Commands."""

import unittest

import typetastic.text_colors as text_colors


class TestColorCodes(unittest.TestCase):
    """Test running commands locally."""

    def setUp(self):
        self.color_reset = "\033[0;0m"

        self.simple_color_codes = {
            "reset": "\033[0;0m",
            "black": "\033[0;30m",
            "red": "\033[0;31m",
            "green": "\033[0;32m",
            "yellow": "\033[0;33m",
            "blue": "\033[0;34m",
            "purple": "\033[0;35m",
            "cyan": "\033[0;36m",
            "white": "\033[0;37m",
        }

        self.bold_color_codes = {
            "black": "\033[1;30m",
            "red": "\033[1;31m",
            "green": "\033[1;32m",
            "yellow": "\033[1;33m",
            "blue": "\033[1;34m",
            "purple": "\033[1;35m",
            "cyan": "\033[1;36m",
            "white": "\033[1;37m",
        }

        self.bright_color_codes = {
            "black": "\033[0;90m",
            "red": "\033[0;91m",
            "green": "\033[0;92m",
            "yellow": "\033[0;93m",
            "blue": "\033[0;94m",
            "purple": "\033[0;95m",
            "cyan": "\033[0;96m",
            "white": "\033[0;97m",
        }

        self.bold_bright_color_codes = {
            "black": "\033[1;90m",
            "red": "\033[1;91m",
            "green": "\033[1;92m",
            "yellow": "\033[1;93m",
            "blue": "\033[1;94m",
            "purple": "\033[1;95m",
            "cyan": "\033[1;96m",
            "white": "\033[1;97m",
        }

    def test_get_simple_color_codes(self):
        """Test the simple color code is correct for the color set."""

        name_formats = [
            "{0}",
            "{0} ",
            " {0}",
            " {0} ",
        ]

        color_set = self.simple_color_codes
        for name_format in name_formats:
            for color in color_set:
                color_name = name_format.format(color)
                color_code = text_colors.TextColors.get_color_code(color_name)
                self.assertEqual(color_set[color], color_code)

    def test_get_bold_color_codes(self):
        """Test the bold color code is correct for the color set."""

        name_formats = [
            "{0}-bold",
            "bold-{0}",
            "bold-{0} ",
            " bold-{0}",
            "bold {0}",
        ]

        color_set = self.bold_color_codes
        for name_format in name_formats:
            for color in color_set:
                color_name = name_format.format(color)
                color_code = text_colors.TextColors.get_color_code(color_name)
                self.assertEqual(color_set[color], color_code)

    def test_get_bright_color_codes(self):
        """Test the bold color code is correct for the color set."""

        name_formats = [
            "{0}-bright",
            "bright-{0}",
            "bright-{0} ",
            " bright-{0}",
            "bright {0}",
        ]

        color_set = self.bright_color_codes
        for name_format in name_formats:
            for color in color_set:
                color_name = name_format.format(color)
                color_code = text_colors.TextColors.get_color_code(color_name)
                self.assertEqual(color_set[color], color_code)

    def test_get_bold_bright_color_codes(self):
        """Test the bright-bold color code is correct for the color set."""

        name_formats = [
            "{0}-bold-bright",
            "{0}-bright-bold",
            "bold-bright-{0}",
            "bold-{0}-bright",
            "bright-bold-{0}",
            "bright-{0}-bold",
            "bright-{0}-bold ",
            " bright-{0}-bold",
            "bright {0} bold"
        ]

        color_set = self.bold_bright_color_codes
        for name_format in name_formats:
            for color in color_set:
                color_name = name_format.format(color)
                color_code = text_colors.TextColors.get_color_code(color_name)
                self.assertEqual(color_set[color], color_code)

    def test_get_default_color_codes(self):
        """Test the bright-bold color code is correct for the color set."""

        names = [
            "this is not a color",
            "==--===",
            "...---..."
        ]

        for name in names:
            color_code = text_colors.TextColors.get_color_code(name)
            self.assertEqual(self.simple_color_codes["cyan"], color_code)
