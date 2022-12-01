import unittest
from Interpreter.interpretation import *
from Infrastructure.structures import *
from Semantics.tokens import *
import numpy as np


class TestTokenizeFunctions(unittest.TestCase):
    def test_get_next_token(self):
        array = np.array([
            [[255, 192, 192], [255, 192, 192], [255, 0, 0], [255, 255, 0]],
            [[255, 192, 192], [0, 0, 0], [255, 255, 255], [42, 42, 42]]])
        tokens = {Direction(0, 0): (toColorToken('push', 3), Position(1, 0)),
                  Direction(0, 1): (toColorToken('push', 3), Position(1, 0)),
                  Direction(1, 0): (Black_token("edge"), Position(0, 1)),
                  Direction(1, 1): (Black_token("edge"), Position(0, 1)),
                  Direction(2, 0): (Black_token("edge"), Position(0, 1)),
                  Direction(2, 1): (Black_token("edge"), Position(0, 0)),
                  Direction(3, 0): (Black_token("edge"), Position(0, 0)),
                  Direction(3, 1): (Black_token("edge"), Position(1, 0))}
        commands = {Color_Block({Position(0, 0),
                                 Position(0, 1), Position(1, 0)}): tokens}
        start = Position(0, 0)
        direction = Direction(0, 0)
        state = State(commands, start, direction)
        next_token = get_next_token(array, state)
        self.assertEqual(next_token, (toColorToken('push', 3), Position(1, 0)))

    def test_make_step(self):
        array = np.array([
            [[255, 192, 192], [255, 192, 192], [255, 0, 0], [255, 255, 0]],
            [[255, 192, 192], [0, 0, 0], [255, 255, 255], [42, 42, 42]]])
        tokens = {Direction(0, 0): (toColorToken('push', 3), Position(1, 0)),
                  Direction(0, 1): (toColorToken('push', 3), Position(1, 0)),
                  Direction(1, 0): (Black_token("edge"), Position(0, 1)),
                  Direction(1, 1): (Black_token("edge"), Position(0, 1)),
                  Direction(2, 0): (Black_token("edge"), Position(0, 1)),
                  Direction(2, 1): (Black_token("edge"), Position(0, 0)),
                  Direction(3, 0): (Black_token("edge"), Position(0, 0)),
                  Direction(3, 1): (Black_token("edge"), Position(1, 0))}
        commands = {Color_Block({Position(0, 0),
                                 Position(0, 1), Position(1, 0)}): tokens}
        start = Position(0, 0)
        direction = Direction(0, 0)
        state = State(commands, start, direction)
        next_token = get_next_token(array, state)
        next_state = make_step(state, next_token)
        expected_state = State(commands, Position(2, 0), direction, [3])
        self.assertTrue(next_state == expected_state)
