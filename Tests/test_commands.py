import unittest
from Interpreter.commands import *
from Semantics.tokens import *


class TestAdditionalFunctions(unittest.TestCase):
    def test_rotate_cc(self):
        assert rotate_cc(0) == 1
        assert rotate_cc(1) == 0

    def test_rotate_dp(self):
        assert rotate_dp(0) == 1
        assert rotate_dp(3) == 0

    def test_change_direction(self):
        assert change_direction(Direction(0, 0)) == Direction(0, 1)
        assert change_direction(Direction(0, 1)) == Direction(1, 1)

    def test_invert_rotate_dp(self):
        assert invert_rotate_dp(3, -2) == 1
        assert invert_rotate_dp(3, 0) == 3

    def test_execute_token(self):
        assert execute_token(Black_token(), Direction(0, 0), []) == \
               (Direction(0, 1), [])
        assert execute_token(White_token(), Direction(0, 0), []) == \
               (Direction(0, 0), [])
        assert execute_token(Terminate_token(), Direction(0, 0), []) == \
               (Direction(0, 0), [])
        assert execute_token(toColorToken("push", 2), Direction(0, 0), []) == \
               (Direction(0, 0), [2])
        try:
            execute_token(None, Direction(0, 0), []) == \
             (Direction(0, 0), [2])
        except Exception as e:
            assert isinstance(e, ValueError)

    def test_noop_operator(self):
        assert noop_operator(Direction(2, 0), []) == (Direction(2, 0), [])

    def test_add_operator(self):
        assert add_operator(Direction(0, 0), [1, 2]) == (Direction(0, 0), [3])

    def test_subtract_operator(self):
        assert subtract_operator(Direction(0, 0), [5, 1]) == \
               (Direction(0, 0), [4])

    def test_multiply_operator(self):
        assert multiply_operator(Direction(0, 0), [5, 4]) == \
               (Direction(0, 0), [20])

    def test_divide_operator(self):
        assert divide_operator(Direction(0, 0), [10, 2]) == \
               (Direction(0, 0), [5])
        try:
            divide_operator(Direction(0, 0), [10, 0])
        except Exception as e:
            assert isinstance(e, ZeroDivisionError)

    def test_mod_operator(self):
        assert mod_operator(Direction(0, 0), [5, 2]) == \
               (Direction(0, 0), [1])
        try:
            divide_operator(Direction(0, 0), [10, 0])
        except Exception as e:
            assert isinstance(e, ZeroDivisionError)

    def test_greater_operator(self):
        assert greater_operator(Direction(0, 0), [5, 2]) == \
               (Direction(0, 0), [1])
        assert greater_operator(Direction(0, 0), [2, 5]) == \
               (Direction(0, 0), [0])

    def test_not_operator(self):
        assert not_operator(Direction(0, 0), [0]) == \
               (Direction(0, 0), [1])
        assert not_operator(Direction(0, 0), [5]) == \
               (Direction(0, 0), [0])

    def test_pointer_operator(self):
        assert pointer_operator(Direction(0, 0), [5]) == \
               (Direction(1, 0), [])
        assert pointer_operator(Direction(1, 0), [-1]) == \
               (Direction(0, 0), [])

    def test_switch_operator(self):
        assert switch_operator(Direction(1, 0), [4]) == \
               (Direction(1, 0), [])
        assert switch_operator(Direction(1, 0), [1]) == \
               (Direction(1, 1), [])

    def test_push_operator(self):
        assert push_operator(toColorToken("push", 5), Direction(0, 0), []) == \
               (Direction(0, 0), [5])
        assert push_operator(toColorToken("push", 2), Direction(0, 0), [1]) ==\
               (Direction(0, 0), [1, 2])

    def test_pop_operator(self):
        assert pop_operator(Direction(0, 0), [1]) == \
               (Direction(0, 0), [])
        assert pop_operator(Direction(0, 0), [1, 2]) == \
               (Direction(0, 0), [1])

    def test_duplicate_operator(self):
        assert duplicate_operator(Direction(0, 0), [1]) == \
               (Direction(0, 0), [1, 1])
        assert duplicate_operator(Direction(0, 0), [1, 2]) == \
               (Direction(0, 0), [1, 2, 2])

    def test_execute_color_token(self):
        assert execute_color_token(toColorToken("push", 2),
                                   Direction(0, 0), []) == \
               (Direction(0, 0), [2])

        assert execute_color_token(toColorToken("pop", 2),
                                   Direction(0, 0), [5]) == \
               (Direction(0, 0), [])

        assert execute_color_token(toColorToken("noop", 2),
                                   Direction(0, 0), []) == \
               (Direction(0, 0), [])

        assert execute_color_token(toColorToken("add", 2),
                                   Direction(0, 0), [5, 4]) == \
               (Direction(0, 0), [9])

        assert execute_color_token(toColorToken("subtract", 2),
                                   Direction(0, 0), [5, 4]) == \
               (Direction(0, 0), [1])

        assert execute_color_token(toColorToken("multiply", 2),
                                   Direction(0, 0), [5, 4]) == \
               (Direction(0, 0), [20])

        assert execute_color_token(toColorToken("divide", 2),
                                   Direction(0, 0), [4, 2]) == \
               (Direction(0, 0), [2])

        assert execute_color_token(toColorToken("mod", 2),
                                   Direction(0, 0), [5, 2]) == \
               (Direction(0, 0), [1])

        assert execute_color_token(toColorToken("not", 2),
                                   Direction(0, 0), [5]) == \
               (Direction(0, 0), [0])

        assert execute_color_token(toColorToken("greater", 2),
                                   Direction(0, 0), [5, 2]) == \
               (Direction(0, 0), [1])

        assert execute_color_token(toColorToken("pointer", 2),
                                   Direction(0, 0), [3]) == \
               (Direction(3, 0), [])

        assert execute_color_token(toColorToken("switch", 2),
                                   Direction(0, 0), [1]) == \
               (Direction(0, 1), [])

        assert execute_color_token(toColorToken("duplicate", 2),
                                   Direction(0, 0), [5, 2]) == \
               (Direction(0, 0), [5, 2, 2])

        try:
            execute_color_token(toColorToken("Unknown", 2), Direction(0, 0),
                                [5, 2])
        except Exception as e:
            assert isinstance(e, ValueError)
