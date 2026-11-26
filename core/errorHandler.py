class SecScriptError(Exception):
    def __init__(self, message, line=None):
        self.message = message
        self.line = line
        super().__init__(self.format())

    def format(self):
        location = f"[Line {self.line}] " if self.line is not None else ""
        return f"{location}{type(self).__name__}: {self.message}"

    def __str__(self):
        return self.format()


class SecsSyntaxError(SecScriptError):
    pass

class SecsNameError(SecScriptError):
    pass

class SecsRuntimeError(SecScriptError):
    pass

class SecsTypeError(SecScriptError):
    pass

class SecsArgumentError(SecScriptError):
    pass

class SecsBuilderError(SecScriptError):
    pass