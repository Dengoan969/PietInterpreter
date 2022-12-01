import unittest
from Semantics.tokenization import *
from Semantics.tokens import *
from Infrastructure.structures import *
import numpy as np


class TestAdditionalFunctions(unittest.TestCase):
    def test_get_next_position(self):
        position = Position(0, 0)
        assert Position(1, 0) == get_next_position(position, 0)
        assert Position(0, 1) == get_next_position(position, 1)
        assert Position(-1, 0) == get_next_position(position, 2)
        assert Position(0, -1) == get_next_position(position, 3)
        try:
            a = get_next_position(position, 100500)
        except Exception as e:
            assert isinstance(e, ValueError)

    def test_is_in_bounds(self):
        array = np.array([[1, 2, 3], [4, 5, 6]])
        assert is_in_bounds(Position(0, 0), array)
        assert is_in_bounds(Position(1, 1), array)
        assert not is_in_bounds(Position(3, 1), array)
        assert not is_in_bounds(Position(3, 3), array)
        assert not is_in_bounds(Position(-1, 3), array)

    def test_get_pixel(self):
        array = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                          [[10, 11, 12], [13, 14, 15], [16, 17, 18]]])

        assert (get_pixel(array, Position(0, 0)) == [1, 2, 3]).all()
        assert (get_pixel(array, Position(1, 1)) == [13, 14, 15]).all()

        try:
            get_pixel(array, Position(-1, 1))
        except Exception as e:
            assert isinstance(e, ValueError)

        try:
            get_pixel(array, Position(10, 10))
        except Exception as e:
            assert isinstance(e, ValueError)

    def test_get_locality(self):
        array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        expected = {Position(0, 1), Position(1, 0), Position(1, 2),
                    Position(2, 1)}
        assert get_locality(array, Position(1, 1)) == expected
        try:
            get_locality(array, Position(5, 1))
        except Exception as e:
            assert isinstance(e, ValueError)

        try:
            get_locality(array, Position(-1, 1))
        except Exception as e:
            assert isinstance(e, ValueError)

    def test_is_terminated(self):
        block_tokens = {Direction(1, 0): (Black_token(), Position(1, 2)),
                        Direction(2, 0): (Black_token(), Position(3, 4)),
                        Direction(2, 1): (Black_token(), Position(5, 2)),
                        Direction(0, 1): (Black_token(), Position(1, 5))}
        assert is_color_block_terminated(block_tokens)
        block_tokens = {Direction(1, 0): (Black_token(), Position(1, 25)),
                        Direction(5, 0): (Black_token(), Position(30, 4)),
                        Direction(20, 1): (Black_token(), Position(5, 21)),
                        Direction(30, 1): (Black_token(), Position(1, 50))}
        assert is_color_block_terminated(block_tokens)
        block_tokens = {Direction(1, 0): (White_token(), Position(1, 25)),
                        Direction(5, 0): (Black_token(), Position(30, 4)),
                        Direction(20, 1): (Black_token(), Position(5, 21)),
                        Direction(30, 1): (Black_token(), Position(1, 50))}
        assert not is_color_block_terminated(block_tokens)
        block_tokens = {Direction(1, 0): (Black_token(), Position(1, 25))}
        assert is_color_block_terminated(block_tokens)

    def test_get_terminated_tokens(self):
        block_tokens = {Direction(1, 0): (Black_token(), Position(1, 2)),
                        Direction(2, 0): (Black_token(), Position(3, 4)),
                        Direction(2, 1): (Black_token(), Position(5, 2)),
                        Direction(0, 1): (Black_token(), Position(1, 5))}
        expected = {Direction(1, 0): (Terminate_token(), Position(1, 2)),
                    Direction(2, 0): (Terminate_token(), Position(3, 4)),
                    Direction(2, 1): (Terminate_token(), Position(5, 2)),
                    Direction(0, 1): (Terminate_token(), Position(1, 5))}
        assert get_terminated_tokens(block_tokens) == expected


class TestTokenizeFunctions(unittest.TestCase):
    def test_get_token(self):
        array = np.array([[[255, 192, 192], [255, 0, 0], [255, 255, 0]],
                          [[0, 0, 0], [255, 255, 255], [42, 42, 42]]
                          ])
        assert get_token(array, Edge(Position(0, 0), Direction(2, 0))) == \
               Black_token("edge")
        assert get_token(array, Edge(Position(0, 0), Direction(1, 0))) == \
               Black_token("toBlack")
        assert get_token(array, Edge(Position(0, 1), Direction(0, 0))) == \
               White_token()
        try:
            get_token(array, Edge(Position(0, 1), Direction(0, 0)))
        except Exception as e:
            assert isinstance(e, SyntaxError)
        assert get_token(array, Edge(Position(0, 0), Direction(0, 0))) == \
               toColorToken('push', 1)
        assert get_token(array, Edge(Position(1, 0), Direction(2, 0))) == \
               toColorToken('pop', 1)
        assert get_token(array, Edge(Position(1, 0), Direction(0, 0))) == \
               toColorToken('add', 1)

    def test_get_edge_position(self):
        color_block = Color_Block({Position(0, 0), Position(0, 1),
                                   Position(0, 2), Position(1, 0),
                                   Position(2, 0), Position(1, 1)})
        assert get_edge_position(color_block, Direction(0, 0)) == \
               Position(2, 0)
        assert get_edge_position(color_block, Direction(0, 1)) == \
               Position(2, 0)
        assert get_edge_position(color_block, Direction(1, 0)) == \
               Position(0, 2)
        assert get_edge_position(color_block, Direction(1, 1)) == \
               Position(0, 2)
        assert get_edge_position(color_block, Direction(2, 0)) == \
               Position(0, 2)
        assert get_edge_position(color_block, Direction(2, 1)) == \
               Position(0, 0)
        assert get_edge_position(color_block, Direction(3, 0)) == \
               Position(0, 0)
        assert get_edge_position(color_block, Direction(3, 1)) == \
               Position(2, 0)

    def test_get_block_tokens(self):
        array = np.array([
            [[255, 192, 192], [255, 192, 192], [255, 0, 0], [255, 255, 0]],
            [[255, 192, 192], [0, 0, 0], [255, 255, 255], [42, 42, 42]]])
        color_block = Color_Block(
            {Position(0, 0), Position(1, 0), Position(0, 1)})
        expected = {Direction(0, 0): (toColorToken('push', 3), Position(1, 0)),
                    Direction(0, 1): (toColorToken('push', 3), Position(1, 0)),
                    Direction(1, 0): (Black_token("edge"), Position(0, 1)),
                    Direction(1, 1): (Black_token("edge"), Position(0, 1)),
                    Direction(2, 0): (Black_token("edge"), Position(0, 1)),
                    Direction(2, 1): (Black_token("edge"), Position(0, 0)),
                    Direction(3, 0): (Black_token("edge"), Position(0, 0)),
                    Direction(3, 1): (Black_token("edge"), Position(1, 0))}
        assert get_block_tokens(array, color_block) == expected

    def test_get_color_block(self):
        array = np.array([
            [[255, 192, 192], [255, 192, 192], [255, 0, 0], [255, 255, 0]],
            [[255, 192, 192], [0, 0, 0], [255, 255, 255], [42, 42, 42]]])
        color_block = Color_Block(
            {Position(0, 0), Position(1, 0), Position(0, 1)})
        assert get_color_block(array, Position(0, 0)) == color_block
        color_block = Color_Block({Position(2, 1)})
        assert get_color_block(array, Position(2, 1)) == color_block
