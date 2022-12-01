class Token:
    def __init__(self, token_type):
        self.token_type = token_type

    def __str__(self):
        return f"type = {self.token_type}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return other and other.token_type == self.token_type


class Black_token(Token):
    def __init__(self, token_type: str = "black"):
        super().__init__(token_type)


class White_token(Token):
    def __init__(self):
        super().__init__("white")


class Terminate_token(Token):
    def __init__(self):
        super().__init__("terminate")


class toColorToken(Token):
    def __init__(self, token_type, block_size):
        super().__init__(token_type)
        self.block_size = block_size

    def __str__(self):
        return f"{super().__str__()}, block_size = {self.block_size}"


def get_token_type(hue, light):
    tokens = [
        ["noop", "push", "pop"],
        ["add", "subtract", "multiply"],
        ["divide", "mod", "not"],
        ["greater", "pointer", "switch"],
        ["duplicate", "roll", "inN"],
        ["inC", "outN", "outC"],
    ]
    return tokens[hue][light]
