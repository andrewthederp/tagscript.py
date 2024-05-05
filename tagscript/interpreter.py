from .functions import Function, FunctionError


def remove_from_string(text, num, amount):
    return text[:num] + text[num+amount:]


class Match:
    __slots__ = ("string", "pos", "start", "end")

    def __init__(self, string, pos):
        self.string = string
        self.pos = self.start, self.end = pos

    def __repr__(self):
        return f'<Match string="{self.string}" pos={self.pos}>'


class InterpretingSession:
    def __init__(self, text: str, functions, *, variables):
        self.functions = [function(self) for function in functions]
        self.dtb: dict[str, Function] = {}
        self.variables: dict[str, str] = variables
        self.make_declaration_to_function()

        self.output = self.interpret(text)

    def make_declaration_to_function(self) -> None:
        for function in self.functions:
            declaration: str | list[str] = function.declaration
            if isinstance(declaration, str):
                self.dtb[declaration] = function
            else:
                for key in declaration:
                    self.dtb[key] = function

    def _get_function_value(self, *, name: str, parameters: list[str], payload: str) -> str | None:
        function = self.dtb.get(name)
        if function is None:
            variable = self.variables.get(name)
            return variable

        return function.get_value(parameters, payload)

    # def _get_function_value(self, *, name: str, parameters: list[str], payload: str) -> str | None:
    #     try:
    #         value = self.get_function(name, parameters or list(), payload)
    #         if value is None:
    #             variable = self.variables.get(name)
    #             return variable
    #         return value
    #     except Exception as e:
    #         raise FunctionError() from e

    @staticmethod
    def _get_everything_between(text: str, *, start_character: str, end_character: str, backslashes: bool = False):
        matches = []
        string = ""
        open = 0
        start = None
        backslashes_count = 0

        for num, character in enumerate(text):
            if character == "\\" and backslashes:
                backslashes_count += 1

            if character == start_character:
                string += character
                if open == 0 and backslashes_count % 2 != 1:
                    start = num
                open += 1
            elif character == end_character:
                open -= 1
                string += character
                if start is not None and not open:
                    match = Match(string, (start, num))
                    matches.append(match)
                    string = ""
                    start = None
            else:
                if open:
                    string += character

            if character != "\\":
                backslashes_count = 0

        return matches

    @staticmethod
    def _get_function_parameters(match: Match):
        text = match.string[1:-1]
        parameters = []
        current_parameter = ""
        backslashes = 0  # backslash behind a command means that it's part of the argument
        open_brackets = 0  # The reason I need this function is that the arguments can be other functions!

        for character in text:
            current_parameter += character

            if character == "\\":
                backslashes += 1

            if character == "(":
                open_brackets += 1
            elif character == ")":
                open_brackets -= 1

            if character == "," and backslashes % 2 != 1 and not open_brackets:
                parameters.append(current_parameter[:-1])  # [:-1] to remove the "," we added
                current_parameter = ""

            if character != "\\":
                backslashes = 0

        if current_parameter:
            parameters.append(current_parameter)

        return parameters

    def _get_function_data(self, match: Match):
        text = match.string[1:-1]
        parameters = []
        payload = None

        try:
            _ = text.index("(")
        except ValueError:  # assume there are no parameters, maybe payload
            pass
        else:
            parameters = self._get_everything_between(text, start_character="(", end_character=")", backslashes=False)
            param_match = parameters[0]
            parameters = self._get_function_parameters(param_match)
            # text = remove_from_string(text, len(name), len(param_match.string))
            text = text[:param_match.start] + text[param_match.end+1:]  # Remove the parameters to save some trouble

        try:
            paylaod_start = text.index(":")
            name = text[:paylaod_start]
        except ValueError:
            name = text
        else:
            payload = text[paylaod_start+1:]

        return {"name": name, "parameters": parameters, "payload": payload}

    def interpret(self, text) -> str:  # I wish I can do this with regex
        matches = self._get_everything_between(text, start_character="{", end_character="}", backslashes=True)

        offset = 0
        for match in matches:
            data = self._get_function_data(match)

            value = self._get_function_value(name=data['name'], parameters=data['parameters'], payload=data['payload'])
            if value is not None:
                text = text[:match.start + offset] + value + text[match.end+1+offset:]  # replacing the code with its value
                offset -= len(match.string) - len(value)
        return text


class Interpreter:
    def __init__(self, *functions):
        self.functions = functions

    def interpret(self, text, *, variables: dict | None = None) -> str:
        return InterpretingSession(text, self.functions, variables=variables or dict())
