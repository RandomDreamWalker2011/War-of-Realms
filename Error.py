"""
    Custom Exceptions:
        - InitError
            Runs when an Initialization Failed

"""
class InitError(Exception):
    def __init__(self, message, class_name):
        self.message = f"{class_name} initialization failed {message}."
        super().__init__(self.message)

