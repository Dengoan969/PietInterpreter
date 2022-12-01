import unittest
from Interpreter.interpretation import *
from Infrastructure.structures import *
from Semantics.tokens import *
import numpy as np


class TestInterpretFunctions(unittest.TestCase):
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
        assert next_token == (toColorToken('push', 3), Position(1, 0))

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
        assert next_state == expected_state

    def test_interpret(self):
        result = interpret("Examples/Add.png", False)
        assert result.is_final and result.position == Position(7, 3)\
               and result.direction == Direction(1, 1) and result.stack == []
        result = interpret("Examples/Add.bmp", False)
        assert result.is_final and result.position == Position(7, 3) \
               and result.direction == Direction(1, 1) and result.stack == []
        result = interpret("Examples/HelloWorld.png", False)
        assert result.is_final and result.position == Position(4, 8) \
               and result.direction == Direction(3, 1) and result.stack == []
        result = interpret("Examples/artistic_hello_world3.gif", False)
        assert result.is_final and result.position == Position(80, 4) \
               and result.direction == Direction(1, 1) and result.stack == []
        result = interpret("Examples/artistic_hello_world4.gif", False)
        assert result.is_final and result.position == Position(72, 12) \
               and result.direction == Direction(0, 0) and result.stack == []

    def test_run(self):
        try:
            run(np.array([
                [[0, 0, 0], [0, 0, 0]],
                [[255, 192, 192], [5, 4, 3]]
            ]), State([], Position(0, 0), Direction(0, 0)))
        except Exception as e:
            assert isinstance(e, RuntimeError)

    def test_run_in_debug(self):
        try:
            run_in_debug(np.array([
                [[0, 0, 0], [0, 0, 0]],
                [[255, 192, 192], [5, 4, 3]]
            ]), State([], Position(0, 0), Direction(0, 0)))
        except Exception as e:
            assert isinstance(e, RuntimeError)

    def test_get_current_direction(self):
        assert get_current_direction(Direction(0, 0)) == "Right-Left"
        assert get_current_direction(Direction(1, 0)) == "Down-Left"
        assert get_current_direction(Direction(2, 0)) == "Left-Left"
        assert get_current_direction(Direction(3, 0)) == "Up-Left"
        assert get_current_direction(Direction(0, 1)) == "Right-Right"
        assert get_current_direction(Direction(1, 1)) == "Down-Right"
        assert get_current_direction(Direction(2, 1)) == "Left-Right"
        assert get_current_direction(Direction(3, 1)) == "Up-Right"
