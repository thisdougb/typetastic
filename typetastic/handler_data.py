"""Handler Data Class."""


class HandlerData:
    """Handler Data Class."""

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
            return True

        return False
