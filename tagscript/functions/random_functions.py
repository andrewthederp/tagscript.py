from .core import Function, FunctionError
import random


class FiftyFifty(Function):
    declaration = "5050"

    def get_value(self, _, __: str):
        return str(random.randrange(0, 2))


class RandomChoice(Function):
    declaration = "random_choice"

    def get_value(self, parameters: list[str], _: str):
        return random.choice(parameters)


class RandomNumber(Function):
    declaration = "random_number"

    def get_value(self, parameters: list[str], _: str):
        match len(parameters):
            case 1:
                start = 0
                end = int(parameters[0])
                step = 1
            case 2:
                start = int(parameters[0])
                end = int(parameters[1])
                step = 1
            case 3:
                start = int(parameters[0])
                end = int(parameters[1])
                step = int(parameters[2])
            case _:
                raise FunctionError("Invalid parameter amount.")

        return str(random.randrange(start, end, step))
