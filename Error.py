"""
    Custom Exceptions:
        - InitError
            Runs when an Initialization Fails

        - NotFoundError
            Runs when a function can't find an input
            Replacement for a less suitable "TypeError"
"""


class InitError(Exception):
    def __init__(self, message, class_name):
        self.message = f"{class_name} initialization failed: {message}."
        super().__init__(self.message)


class InputNotFoundError(Exception):
    def __init__(self, message):
        self.message = f"{message}"
        super().__init__(self.message)
