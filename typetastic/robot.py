"""TypeTastic"""

import os
from pexpect import pxssh
import yaml

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
            "prompt-string": "$ ",
            "remote-prompt": "[ssh] $ "
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
            if "commands" in result and isinstance(result["commands"], list):
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
            bothan.emit_prompt(prompt)

            for command in self.__data["commands"]:

                if isinstance(command, dict) and "ssh" in command:
                    # set up session

                    remote_directory = None
                    for remote_command in command["ssh"]:

                        handler_data = {
                            "remote": pxssh.pxssh(),
                            "command": remote_command,
                            "typing_speed": self._get_typing_speeds(typing_speed),
                            "current_directory": remote_directory,
                            "config": self.__data["config"]
                        }

                        result = self.run_task(handler_data)

                        if result:
                            self.__successful_commands += 1

                        if result and remote_command.startswith("cd "):
                            (_, path) = command.split(" ")
                            remote_directory = path

                else:

                    handler_data = {
                        "remote": None,
                        "command": command,
                        "typing_speed": self._get_typing_speeds(typing_speed),
                        "current_directory": self.__current_directory,
                        "config": self.__data["config"]
                    }

                    if self.run_task(handler_data):
                        self.__successful_commands += 1

                        # change dir, under the hood. we pass this into the shell
                        # spawn.
                        if command.startswith("cd "):
                            (_, path) = command.split(" ")
                            self.__current_directory = path

            print()  # run ends, tidy up

    @staticmethod
    def run_task(handler_data):
        """Run a task from handler data."""

        command = handler_data["command"]
        bothan_method = Robot._get_bothan_method(command)

        config = handler_data["config"]
        handler_data["simulated_typing"] = Robot._string_to_type(config, command)

        task_result = bothan_method(handler_data)

        # trailing emit prompt, to setup the next line. pause is a special case.
        if command.startswith("PAUSE"):
            return task_result

        prompt = handler_data["config"]["prompt-string"]
        # override prompt if we are still in a remote session
        if handler_data["remote"] and not command == "exit":
            prompt = handler_data["config"]["remote-prompt"]

        bothan.emit_prompt(prompt)

        return task_result

    @staticmethod
    def _get_bothan_method(command):
        """Returns bothan method for command."""

        name = Robot._get_command_name(command)
        fn_lookup = "bot_handler_{0}".format(name)
        bothan_method = getattr(bothan, fn_lookup, bothan.bot_handler_default)

        return bothan_method

    @staticmethod
    def _get_command_name(command):
        """Returns name of the command."""
        name = command.lower()

        if " " in command:  # command has args
            (name, _) = command.split(" ", 1)

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
    def _get_typing_speeds(speed):
        """Returns typing speeds."""
        if speed not in Robot.TypingSpeeds:
            speed = "moderate"

        return Robot.TypingSpeeds[speed]

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
