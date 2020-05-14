"""Handler Data Class."""


class HandlerData:
    """Handler Data Class."""

    # min typing speed, max typing speed, return key delay
    TypingSpeeds = {
        "slow": [0.1, 0.4, 1.0],
        "moderate": [0.05, 0.2, 0.5],
        "supersonic": [0, 0, 0]
    }

    def __init__(self):
        """Returns a default handler data object."""

        self.__handler_data = {
            "remote": None,
            "local": None,
            "command": None,
            "typing_speed": None,
            "config": None,
            "get_exit_status": True
        }

    def get(self, key=None):
        """Returns the handler data as a dict."""
        if not key:
            return self.__handler_data

        if key in self.__handler_data:
            return self.__handler_data[key]

        return None

    def set(self, key=None, value=None):
        """Sets key to value, and returns True."""
        if key in self.__handler_data:
            self.__handler_data[key] = value

            if key == "typing-speed":
                self.__handler_data["typing_speed"] = self._get_typing_speeds(typing_speed)
            return True

        return False

    @staticmethod
    def _get_typing_speeds(speed):
        """Returns typing speeds."""
        if speed not in HandlerData.TypingSpeeds:
            speed = "moderate"

        return HandlerData.TypingSpeeds[speed]
