"""TypeTastic"""


class Robot:
    """Robot that runs the commands."""

    def __init__(self):
        Robot().hello()

    @staticmethod
    def hello():
        """Basic test method."""
        print("Hello World!")
