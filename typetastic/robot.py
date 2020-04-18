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

    # min typing speed, max typing speed, return key delay
    TypingSpeeds = {
        "slow": [0.1, 0.4, 1.0],
        "moderate": [0.05, 0.2, 0.5],
        "supersonic": [0, 0, 0]
    }

    def __init__(self):
        self.__data = {}
        self.__data["config"] = {
            "typing-color": "cyan",
            "typing-speed": "moderate",
            "prompt-string": "$ "
        }
        self.__successful_commands = 0

    def load(self, data_source):
        """Loads data either from file, dict or an array.

        Inputs:

        list of commands: ['ls', 'uptime']
        dict of commands: {"commands": ['ls', 'uptime']}
        dict of config: {"config": {'typing-color': 'red'} }
        str of file path: "myfiledata.yaml"
        """
        if isinstance(data_source, dict):
            if "commands" in data_source or "config" in data_source:
                result = data_source
            else:
                result = None

        if isinstance(data_source, list):
            result = {"commands": data_source}

        if isinstance(data_source, str):
            result = self._load_file(data_source)

        if result:
            if "commands" in result:
                self.__data["commands"] = result["commands"]
            if "config" in result:
                # we .update() to merge into existing config defaults
                self.__data["config"].update(result["config"])

    def run(self):
        """Run the currently loaded commands.

        Returns:
        The number of commands with a success exit code.
        """
        typing_speed = None
        if "config" in self.__data:
            if "typing-speed" in self.__data["config"]:
                typing_speed = self.__data["config"]["typing-speed"]

        self.__successful_commands = 0  # reset this

        if "commands" in self.__data:
            for command in self.__data["commands"]:
                str_to_type = self._string_to_type(self.__data["config"], command)
                prompt = self._get_config("prompt-string")
                self._simulate_typing(prompt, str_to_type, typing_speed)

                if self._run_command(command):
                    self.__successful_commands += 1

    def _get_config(self, key):
        """Lookup and return the config value for key."""
        if "config" in self.__data:
            if key in self.__data["config"]:
                return self.__data["config"][key]
        return None

    def _get_data(self):
        """Return the data dict."""
        return self.__data

    def _get_successful_commands(self):
        """Return the successful commands run."""
        return self.__successful_commands

    @staticmethod
    def _simulate_typing(prompt, command, speed=None):
        """Simulates typing to stdout."""
        if speed not in Robot.TypingSpeeds:
            speed = "moderate"

        (speed_min, speed_max, return_key_delay) = Robot.TypingSpeeds[speed]

        # the prompt is not a thing we type
        print(prompt, end="")
        sys.stdout.flush()

        for char in command:
            print(char, end="")
            sys.stdout.flush()
            char_delay = random.uniform(speed_min, speed_max)
            time.sleep(char_delay)

        time.sleep(return_key_delay)
        print()  # newline required after typing command

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

        command_string = "{0}{1}{2}".format(color, command, color_reset)
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

        # 0 = success, 1 = failure in Unix, so invert result
        return not bool(child.exitstatus)
