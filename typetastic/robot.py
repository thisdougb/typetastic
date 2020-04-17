"""TypeTastic"""

import pexpect
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

    @staticmethod
    def run_command(command):
        """Run local command."""

        spawn_cmd = "/bin/bash -c '{0}'".format(command)
        child = pexpect.spawn(spawn_cmd, timeout=None, encoding='utf-8')

        for line in child:
            print(line, end="")
        child.close()

        return child.exitstatus  # 0 = success, 1 = failure
