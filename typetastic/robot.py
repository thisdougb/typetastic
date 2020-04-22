"""TypeTastic"""

import time
import os
import pexpect
from pexpect import pxssh
import yaml

from . import bot_handlers as bothan
import typetastic.text_colors as text_colors


class Robot:
    """Robot that runs the commands."""

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

    @staticmethod
    def setup_shell(prompt, shell="/bin/bash"):
        """Returns a pexpect spawn object.

        TODO: unit test
        """

        session = pexpect.spawn(shell, timeout=None, encoding='utf-8', echo=False)
        while True:
            session.expect_exact([prompt, '\r\n', pexpect.EOF, pexpect.TIMEOUT])
            # print(session.before)
            if not session.buffer:
                break

        session.sendline("export PS1='{0}'".format(prompt))
        time.sleep(0.2)
        while True:
            session.expect_exact([prompt, '\r\n', pexpect.EOF, pexpect.TIMEOUT])
            # print(session.before)
            if not session.buffer:
                break

        return session

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

            local_directory = None
            prompt = self._get_config("prompt-string")
            bothan.emit_prompt(prompt)

            shell = Robot.setup_shell(prompt)

            for command in self.__data["commands"]:

                if isinstance(command, dict) and "ssh" in command:
                    ssh_conn = pxssh.pxssh()  # must be shared across all commands
                    remote_directory = None

                    for remote_command in command["ssh"]:

                        handler_data = {
                            "remote": ssh_conn,
                            "local": None,
                            "command": remote_command,
                            "typing_speed": self._get_typing_speeds(typing_speed),
                            "current_directory": remote_directory,
                            "config": self.__data["config"]
                        }

                        result = self.run_task(handler_data)

                        if result:
                            self.__successful_commands += 1

                        if result and remote_command.startswith("cd "):
                            (_, path) = remote_command.split(" ")
                            remote_directory = path

                else:

                    handler_data = {
                        "remote": None,
                        "local": shell,
                        "command": command,
                        "typing_speed": self._get_typing_speeds(typing_speed),
                        "current_directory": local_directory,
                        "config": self.__data["config"]
                    }

                    if self.run_task(handler_data):
                        self.__successful_commands += 1

                        # change dir, under the hood. we pass this into the shell
                        # spawn.
                        if command.startswith("cd "):
                            local_directory = handler_data["current_directory"]

            print()  # run ends, tidy up
            shell.close()
            time.sleep(1)

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

        color_reset = text_colors.TextColors.get_color_code("reset")
        if "typing-color" in config:
            color = text_colors.TextColors.get_color_code(config["typing-color"])
        else:
            color = ""

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
