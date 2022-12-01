import numpy as np
import Semantics.colors as colors
import Semantics.tokens as tokens
from Infrastructure.structures import *


def get_next_position(position, dp):
    if dp == 0:
        return Position(position.x + 1, position.y)
    if dp == 1:
        return Position(position.x, position.y+1)
    if dp == 2:
        return Position(position.x - 1, position.y)
    if dp == 3:
        return Position(position.x, position.y - 1)
    raise ValueError


def get_token(pixel_data, edge):
    next_position = get_next_position(edge.position, edge.direction.dp)
    if not is_in_bounds(next_position, pixel_data):
        return tokens.Black_token("edge")
    pixel = get_pixel(pixel_data, next_position)
    if colors.is_black(pixel):
        return tokens.Black_token("toBlack")
    if colors.is_white(pixel):
        return tokens.White_token()
    if not colors.is_main_color(pixel):
        raise SyntaxError
    color_change = colors.get_color_diff(get_pixel(pixel_data, edge.position),
                                         get_pixel(pixel_data, next_position))
    token_type = tokens.get_token_type(color_change['hue'],
                                       color_change['light'])
    block_size = len(get_color_block(pixel_data, edge.position).positions)
    return tokens.toColorToken(token_type, block_size)


def get_edge_position(color_block, direction):
    dp = direction.dp
    cc = direction.cc
    if dp == 0:
        edge_position = max(color_block.positions,
                            key=lambda p: p.x)
        edge_positions = list(filter(lambda p: p.x == edge_position.x,
                                     color_block.positions))
        if cc == 0:
            return min(edge_positions, key=lambda p: p.y)
        else:
            return max(edge_positions, key=lambda p: p.y)
    elif dp == 1:
        edge_position = max(color_block.positions, key=lambda p: p.y)
        edge_positions = list(filter(lambda p: p.y == edge_position.y,
                                     color_block.positions))
        if cc == 0:
            return max(edge_positions, key=lambda p: p.x)
        else:
            return min(edge_positions, key=lambda p: p.x)
    elif dp == 2:
        edge_position = min(color_block.positions, key=lambda p: p.x)
        edge_positions = list(filter(lambda p: p.x == edge_position.x,
                                     color_block.positions))
        if cc == 0:
            return max(edge_positions, key=lambda p: p.y)
        else:
            return min(edge_positions, key=lambda p: p.y)
    else:
        edge_position = min(color_block.positions, key=lambda p: p.y)
        edge_positions = list(filter(lambda p: p.y == edge_position.y,
                                     color_block.positions))
        if cc == 0:
            return min(edge_positions, key=lambda p: p.x)
        else:
            return max(edge_positions, key=lambda p: p.x)


def is_color_block_terminated(block_tokens):
    return all(map(lambda x: isinstance(x[1][0], tokens.Black_token),
                   block_tokens.items()))


def get_terminated_tokens(block_tokens):
    return dict(map(lambda x: (x[0], (tokens.Terminate_token(), x[1][1])),
                    block_tokens.items()))


def get_block_tokens(pixel_data, color_block):
    edge_pointers = list(
        map(lambda i: Direction(i % 4, int(i / 4)), iter(range(8))))
    edges = list(map(lambda pointers: Edge(
        get_edge_position(color_block, pointers), pointers), edge_pointers))
    block_tokens = dict(map(lambda x: (x.direction, (get_token(pixel_data, x),
                                                     x.position)), edges))
    if is_color_block_terminated(block_tokens):
        block_tokens = get_terminated_tokens(block_tokens)
    return block_tokens


def is_in_bounds(position, array):
    return 0 <= position.x < array.shape[1]\
           and 0 <= position.y < array.shape[0]


def get_pixel(pixel_data, position):
    if is_in_bounds(position, pixel_data):
        return pixel_data[position.y][position.x]
    raise ValueError


def get_locality(pixel_data, position):
    if not is_in_bounds(position, pixel_data):
        raise ValueError
    neighbours = set()
    for dy in range(-1, 2, 1):
        for dx in range(-1, 2, 1):
            if abs(dx+dy) % 2 == 0:
                continue
            new_x = position.x + dx
            new_y = position.y + dy
            new_position = Position(new_x, new_y)
            if is_in_bounds(new_position, pixel_data):
                neighbours.add(Position(new_x, new_y))
    return neighbours


def get_color_block(pixel_data, position):
    positions = {position}
    result = Color_Block({position})
    color = get_pixel(pixel_data, position)
    if colors.is_white(color):
        return result
    while len(positions) != 0:
        locality = get_locality(pixel_data, positions.pop())
        for next_position in locality:
            next_color = get_pixel(pixel_data, next_position)
            if colors.is_equal(next_color, color)\
                    and next_position not in result.positions:
                result.positions.add(next_position)
                positions.add(next_position)
    return result


def get_color_blocks(pixel_data, positions):
    result = set()
    while len(positions) != 0:
        next_position = positions.pop()
        if colors.is_black(get_pixel(pixel_data, next_position)):
            continue
        next_color_block = get_color_block(pixel_data, next_position)
        positions = list(set(positions) - next_color_block.positions)
        result.add(next_color_block)
    return result


def get_all_tokens(pixel_data):
    all_coordinates = np.ndindex(pixel_data.shape[1], pixel_data.shape[0])
    all_positions = set(map(lambda c: Position(c[0], c[1]), all_coordinates))
    color_blocks = get_color_blocks(pixel_data, all_positions)
    result = dict()
    for block in color_blocks:
        result[block] = get_block_tokens(pixel_data, block)
    return result
