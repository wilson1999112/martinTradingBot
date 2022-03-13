""" Custom Error TODO"""
class UserInputError(Exception):
    """User Input Wrong"""
    def __init__(self, err: str):
        self.err = err
        super().__init__(self.err)
