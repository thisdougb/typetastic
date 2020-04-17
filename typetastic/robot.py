"""TypeTastic"""

import yaml


class Robot:
    """Robot that runs the commands."""

    def __init__(self):
        pass

    @staticmethod
    def load_file(inputfile):
        """Load YML file.

        Returns:
        A dictionary containing the data.
        False if data could not be loaded.
        """
        with open(inputfile, 'r') as stream:
            try:
                print(stream)
                commands = yaml.load(stream, Loader=yaml.FullLoader)
                return commands

            except yaml.YAMLError as error:
                print(error)
                return False
