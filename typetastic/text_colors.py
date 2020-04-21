"""Simple class for text colors."""


class TextColors:
    """Simple class for text colors."""

    colors = {
        "reset": 0,
        "black": 30,
        "red": 31,
        "green": 32,
        "yellow": 33,
        "blue": 34,
        "purple": 35,
        "cyan": 36,
        "white": 37,
    }

    @staticmethod
    def get_color_code(color_name):
        """Return the ANSI color code."""

        # defaults - cyan, not bold, not bright
        color_index = 36
        bold = 0

        for color in TextColors.colors:
            if color in color_name.lower():
                color_index = TextColors.colors[color]
                break

        if "bold" in color_name.lower():
            bold = 1

        if "bright" in color_name.lower():
            color_index += 60  # index offset

        return "\033[{0};{1}m".format(bold, color_index)
