import copy


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return other and other.x == self.x and other.y == self.y

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return str(self)

    def __deepcopy__(self, memodict):
        return Position(self.x, self.y)


class Direction:
    def __init__(self, dp, cc):
        self.dp = dp
        self.cc = cc

    def __eq__(self, other):
        return self.dp == other.dp and self.cc == other.cc

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.dp, self.cc))

    def __str__(self):
        return f"{self.dp},{self.cc}"

    def __repr__(self):
        return str(self)

    def __deepcopy__(self, memodict):
        return Direction(self.dp, self.cc)


class Color_Block:
    def __init__(self, positions):
        self.positions = positions

    def __eq__(self, other):
        return other.positions == self.positions

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(frozenset(self.positions))

    def __str__(self):
        return str(self.positions)

    def __repr__(self):
        return str(self)

    def __copy__(self):
        return Color_Block(copy.copy(self.positions))


class State:
    def __init__(self, commands, position, direction, stack=None):
        self.commands = commands
        self.position = position
        self.direction = direction
        self.is_final = False
        self.next_token = None
        if not stack:
            stack = []
        self.stack = stack

    def __deepcopy__(self, memodict):
        return State(self.commands, copy.deepcopy(self.position),
                     copy.deepcopy(self.direction), copy.deepcopy(self.stack))

    def __eq__(self, other):
        return other and other.commands == self.commands and \
               other.position == self.position and \
               other.direction == self.direction


class Edge:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
