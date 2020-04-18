"""TypeTastic"""

import random
import sys
import time
import yaml
import pexpect


class Robot:
    """Robot that runs the commands."""

    TextColors = {
        "blue": "\033[1;34m",
        "cyan": "\033[1;36m",
        "green": "\033[0;32m",
        "red": "\033[1;31m",
        "reset": "\033[0;0m"
    }
    TypingSpeeds = {
        "moderate": [0.01, 0.4],
        "supersonic": [0, 0]
    }

    def __init__(self):
        self.data = {}
        self.data["config"] = {
            "typing-color": "cyan",
            "typing-speed": "moderate",
            "prompt-string": "$ "
        }

    def load(self, inputfile):
        """Public wrapper for load_file()."""
        result = self._load_file(inputfile)
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
        speed_to_type = None
        if "config" in self.data:
            if "typing-speed" in self.data["config"]:
                speed_to_type = self.data["config"]["typing-speed"]

        successful_commands = 0
        if "commands" in self.data:
            for command in self.data["commands"]:
                str_to_type = self._string_to_type(self.data["config"], command)
                self._simulate_typing(str_to_type, speed_to_type)

                if self._run_command(command):
                    successful_commands += 1

        return successful_commands

    def _get_config(self, key):
        """Lookup and return the config value for key."""
        if "config" in self.data:
            if key in self.data["config"]:
                return self.data["config"][key]
        return None

    @staticmethod
    def _simulate_typing(command, speed=None):
        """Simulates typing to stdout."""
        if speed not in Robot.TypingSpeeds:
            speed = "moderate"

        (speed_min, speed_max) = Robot.TypingSpeeds[speed]

        for char in command:
            print(char, end="")
            sys.stdout.flush()
            char_delay = random.uniform(speed_min, speed_max)
            time.sleep(char_delay)

    @staticmethod
    def _string_to_type(config, command):
        """Returns the formatted string to type."""

        color = ""
        color_reset = ""
        if "typing-color" in config:
            if config["typing-color"] in Robot.TextColors:
                color_name = config["typing-color"]
                color = Robot.TextColors[color_name]
                color_reset = Robot.TextColors["reset"]

        prompt = ""
        if "typing-color" in config:
            prompt = config["prompt-string"]

        command_string = "{0}{1}{2}{3}".format(prompt, color, command, color_reset)
        return command_string

    @staticmethod
    def _load_file(inputfile):
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
    def _run_command(command):
        """Run local command."""

        spawn_cmd = "/bin/bash -c '{0}'".format(command)
        child = pexpect.spawn(spawn_cmd, timeout=None, encoding='utf-8')

        for line in child:
            print(line, end="")
        child.close()

        return child.exitstatus  # 0 = success, 1 = failure
