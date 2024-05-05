class Function:
    declaration = NotImplemented

    def __init__(self, interpreter):
        self.interpreter = interpreter

    def get_value(self, _: list[str], __: str) -> str:
        raise NotImplementedError("This method must be implemented.")


class FunctionError(Exception):
    """Error raised when a function is used wrong"""
