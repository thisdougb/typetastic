"""TypeTastic"""

import time
import yaml
import pexpect
from pexpect import pxssh


from . import text_colors
from . import bot_handlers as bothan
from . import session_config


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
        self.__config = session_config.SessionConfig()

        self.__successful_commands = 0

    def load(self, data_source):
        """Loads data either from file, dict or an array.

        Inputs:

        list of commands: ['ls', 'uptime']
        dict of commands: {"commands": ['ls', 'uptime']}
        dict of config: {"config": {'typing-color': 'red'} }
        str of file path: "myfiledata.yaml"
        """

        result = None

        if isinstance(data_source, dict):
            if "commands" in data_source or "config" in data_source:
                result = data_source

        if isinstance(data_source, list):
            result = {"commands": data_source}

        if isinstance(data_source, str):
            result = self._load_file(data_source)

        if result:
            if "commands" in result and isinstance(result["commands"], list):
                self.__data["commands"] = result["commands"]
            if "config" in result:
                # we .update() to merge into existing config defaults
                for key in result["config"]:
                    self.__config.set(key, result["config"][key])

    @staticmethod
    def setup_shell(prompt, shell="/bin/bash"):
        """Returns a pexpect spawn object.

        TODO: unit test
        """

        session = pexpect.spawn(shell, timeout=None, encoding='utf-8', echo=False)
        while True:
            session.expect_exact(['# ', '$ ', '\r\n', pexpect.EOF, pexpect.TIMEOUT])
            if not session.buffer:
                break

        session.sendline("export PS1='{0}'".format(prompt))
        time.sleep(0.2)
        while True:
            session.expect_exact([prompt, '\r\n', pexpect.EOF, pexpect.TIMEOUT])
            if not session.buffer:
                break

        return session

    def run(self):
        """Run the currently loaded commands.

        Returns:
        The number of commands with a success exit code.
        """
        typing_speed = self.__config.get("typing-speed")

        self.__successful_commands = 0  # reset this

        if "commands" in self.__data:

            # prompt = self._get_config("prompt-string")
            prompt = self.__config.get("prompt-string")
            bothan.emit_prompt(prompt)

            shell = Robot.setup_shell(prompt)

            for command in self.__data["commands"]:

                if isinstance(command, dict) and "ssh" in command:
                    ssh_conn = pxssh.pxssh()  # must be shared across all commands

                    for remote_command in command["ssh"]:

                        handler_data = {
                            "remote": ssh_conn,
                            "local": None,
                            "command": remote_command,
                            "typing_speed": self._get_typing_speeds(typing_speed),
                            "config": self.__config.get(),
                            "get_exit_status": True
                        }

                        result = self.run_task(handler_data)

                        if result:
                            self.__successful_commands += 1

                elif isinstance(command, dict) and "python3" in command:

                    for python_command in command["python3"]:

                        self.__config.set("prompt-string", ">>> ")

                        handler_data = {
                            "remote": None,
                            "local": shell,
                            "command": python_command,
                            "typing_speed": self._get_typing_speeds(typing_speed),
                            "config": self.__config.get(),
                            "get_exit_status": False
                        }

                        result = self.run_python_task(handler_data)

                        if result:
                            self.__successful_commands += 1

                else:

                    handler_data = {
                        "remote": None,
                        "local": shell,
                        "command": command,
                        "typing_speed": self._get_typing_speeds(typing_speed),
                        "config": self.__config.get(),
                        "get_exit_status": True
                    }

                    if self.run_task(handler_data):
                        self.__successful_commands += 1

            shell.close()
            time.sleep(self.__config.get("pexpect-delay") * 2)  # time to freeze frame in post
            print()  # run ends, tidy up

    @staticmethod
    def run_python_task(handler_data):
        """Run a task from handler data."""

        command = handler_data["command"]
        bothan_method = Robot._get_bothan_method(command)

        config = handler_data["config"]
        if command == "CTRL_D":
            handler_data["config"]["prompt-string"] = handler_data["config"]["local-prompt"]
            handler_data["simulated_typing"] = Robot._string_to_type(config, "^D")

        else:
            handler_data["simulated_typing"] = Robot._string_to_type(config, command)

        task_result = bothan_method(handler_data)

        prompt = handler_data["config"]["prompt-string"]
        bothan.emit_prompt(prompt)

        return task_result

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

    def _get_data(self):
        """Return the data dict."""
        return self.__data

    def _get_config(self):
        """Return the config dict."""
        return self.__config.get()

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
