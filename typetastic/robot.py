"""TypeTastic"""

import pexpect
import yaml


class Robot:
    """Robot that runs the commands."""

    def __init__(self):
        self.data = {}
        self.data["config"] = {
            "typing-color": "cyan",
            "typing-speed": "moderate",
            "prompt-string": "$ "
        }

    def load(self, inputfile):
        """Public wrapper for load_file()."""
        result = self.load_file(inputfile)
        if result:
            if "commands" in result:
                self.data["commands"] = result["commands"]
            if "config" in result:
                # we .update() to merge into existing config defaults
                self.data["config"].update(result["config"])

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

    def get_config(self, key):
        """Lookup and return the config value for key."""
        if "config" in self.data:
            if key in self.data["config"]:
                return self.data["config"][key]
        return None

    @staticmethod
    def load_file(inputfile):
        """Load YML file.

        Returns:
        A dictionary containing the data.
        False if data could not be loaded.
        """
        with open(inputfile, 'r') as stream:
            try:
                data = yaml.load(stream, yaml.SafeLoader)
                return data

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
