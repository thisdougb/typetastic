"""TypeTastic"""

import pexpect
import yaml


class Robot:
    """Robot that runs the commands."""

    def __init__(self):
        self.data = {}

    def load(self, inputfile):
        """Public wrapper for load_file()."""
        result = self.load_file(inputfile)
        if result:
            self.data = result

        return result

    def run(self):
        """Run the currently loaded commands.

        Returns:
        The number of commands with a success exit code.
        """
        successful_commands = 0
        if "commands" in self.data:
            for command in self.data["commands"]:
                if self.run_command(command):
                    successful_commands += 1
        return successful_commands

    @staticmethod
    def load_file(inputfile):
        """Load YML file.

        Returns:
        A dictionary containing the data.
        False if data could not be loaded.
        """
        with open(inputfile, 'r') as stream:
            try:
                commands = yaml.load(stream, yaml.SafeLoader)
                return commands

            except yaml.YAMLError as error:
                print("load_file: {0}".format(error))
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
