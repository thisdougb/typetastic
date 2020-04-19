"""TypeTastic"""

import os
import random
import sys
import time
import yaml

import getch
import pexpect

from . import bot_handlers as bothan


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

    Editors = ["vi", "vim", "emacs"]

    def __init__(self):
        self.__data = {}
        self.__data["config"] = {
            "typing-color": "cyan",
            "typing-speed": "moderate",
            "prompt-string": "$ "
        }
        self.__successful_commands = 0
        self.__current_directory = os.getcwd()

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

            prompt = self._get_config("prompt-string")
            print(prompt, end="")
            sys.stdout.flush()

            for command in self.__data["commands"]:

                if command == "PAUSE":
                    self._pause_flow()
                    self.__successful_commands += 1
                    continue

                elif command == 'NEWLINE':
                    print()
                    self.__successful_commands += 1

                else:
                    str_to_type = self._string_to_type(self.__data["config"], command)
                    self._simulate_typing(str_to_type, typing_speed)

                    # capture special commands, we don't want to execute
                    # but do want to type out.
                    if self._is_editor(command):
                        self._pause_flow()
                        self.__successful_commands += 1

                    elif command == "ls" or command.startswith("ls "):
                        bothan.bot_handler_ls(command)

                    elif self._run_command(command, self.__current_directory):
                        self.__successful_commands += 1

                        # change dir, under the hood. we pass this into the shell
                        # spawn.
                        if command.startswith("cd "):
                            (_, path) = command.split(" ")
                            self.__current_directory = path

                print(prompt, end="")
                sys.stdout.flush()

            print()  # run ends, tidy up

    @staticmethod
    def _get_command_name(command):
        """Returns name of the command."""
        name = command

        if " " in command:  # command has args
            (name, _) = command.lower().split(" ", 1)

        if "/" in name:  # command has path
            (_, name) = name.rsplit("/", 1)

        return name

    def _get_config(self, key):
        """Lookup and return the config value for key."""
        if "config" in self.__data:
            if key in self.__data["config"]:
                return self.__data["config"][key]
        return None

    def _get_data(self):
        """Return the data dict."""
        return self.__data

    def _get_current_directory(self):
        """Return the current directory."""
        return self.__current_directory

    def _get_successful_commands(self):
        """Return the successful commands run."""
        return self.__successful_commands

    @staticmethod
    def _is_editor(command):
        """Returns true if command starts an editor, otherwise false."""
        for editor in Robot.Editors:
            if command.startswith("{0} ".format(editor)):
                return True
        return False

    @staticmethod
    def _pause_flow():
        getch.getch()

    @staticmethod
    def _simulate_typing(command, speed=None):
        """Simulates typing to stdout."""
        if speed not in Robot.TypingSpeeds:
            speed = "moderate"

        (speed_min, speed_max, return_key_delay) = Robot.TypingSpeeds[speed]

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
    def _run_command(command, current_dir):
        """Run local command."""

        spawn_cmd = "/bin/bash -c '{0}'".format(command)
        child = pexpect.spawn(spawn_cmd, cwd=current_dir, timeout=None, encoding='utf-8')

        for line in child:
            print(line, end="")
        child.close()

        # 0 = success, 1 = failure in Unix, so invert result
        return not bool(child.exitstatus)
