class SecScriptError(Exception):
    def __init__(self, message, line=None):
        self.message = message
        self.line = line
        super().__init__(self.format())

    def format(self):
        if self.line is not None:
            return f"[Line {self.line}] SecScriptError: {self.message}"
        return f"SecScriptError: {self.message}"