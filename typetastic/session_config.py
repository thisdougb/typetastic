"""SessionConfig Class."""


class SessionConfig:
    """Configuration that controls the command session.

    Public Interface:
        get_config(): Get config dict, or one key/value
        set_config(): Set a config key to a value

    """

    def __init__(self):
        """Sets up a default config object."""
        self.__config = {
            "config": {
                "local-prompt": "$ ",
                "pexpect-delay": 0.2,  # delay required for response to be read
                "prompt-string": "$ ",
                "remote-prompt": "[ssh] $ ",
                "typing-color": "cyan",
                "typing-speed": "moderate",
            }
        }

    def get(self, key=None):
        """Returns the config as a dict, the root dict if no key given."""

        config = self.__config["config"]

        if not key:
            return self.__config

        if key in config:
            return config[key]

        return None

    def set(self, key=None, value=None):
        """Sets key to value, and returns True."""

        config = self.__config

        if key in config:
            config[key] = value
            return True

        return False
