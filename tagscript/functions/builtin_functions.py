from .core import Function, FunctionError
import re

TAG_FUNCTION_PAYLOAD_REGEX = re.compile(r"(?<!\\)(\\\\)*\|")


class Variable(Function):
    declaration = ["=", "var"]

    def get_value(self, parameters: list[str], payload: str) -> str:
        if len(parameters) != 1:
            raise FunctionError("Invalid parameter amount.")
        elif not payload:
            raise FunctionError("Variable statements requires a payload.")

        variable_content = self.interpreter.interpret(payload)
        self.interpreter.variables[parameters[0]] = variable_content
        return ""


class IFunction(Function):
    declaration = "if"

    def get_value(self, parameters: list[str], payload: str) -> str:
        if len(parameters) != 1:
            raise FunctionError("Invalid parameter amount.")
        elif not payload:
            raise FunctionError("If statements requires a payload.")

        payload = TAG_FUNCTION_PAYLOAD_REGEX.split(payload)
        first = payload[0]
        rest = ''.join([i for i in payload[1:] if i])

        if self.interpreter.interpret(parameters[0]) == "1":
            return self.interpreter.interpret(first)
        else:
            return self.interpreter.interpret(rest)


class Equal(Function):
    declaration = ["eq", "=="]

    def get_value(self, parameters: list[str], _: str) -> str:
        if len(parameters) not in {1, 2}:
            raise FunctionError("Invalid parameter amount.")

        if len(parameters) == 1:  # this block is kinda redundant
            param = self.interpreter.interpret(parameters[0])
            if param not in {"0", "1"}:
                raise FunctionError("Invalid parameter value.")
            return str(int(param == "1"))
        else:
            first = self.interpreter.interpret(parameters[0])
            second = self.interpreter.interpret(parameters[1])
            return str(int(first == second))


class NotEqual(Function):
    declaration = ["neq", "!="]

    def get_value(self, parameters: list[str], _: str) -> str:
        if len(parameters) not in {1, 2}:
            raise FunctionError("Invalid parameter amount.")

        if len(parameters) == 1:
            param = self.interpreter.interpret(parameters[0])
            if param not in {"0", "1"}:
                raise FunctionError("Invalid parameter value.")
            return str(int(param == "0"))
        else:
            first = self.interpreter.interpret(parameters[0])
            second = self.interpreter.interpret(parameters[1])
            return str(int(first != second))
