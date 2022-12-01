import Semantics.tokens as tokens
from Infrastructure.structures import *
import copy


def rotate_cc(cc):
    return (cc + 1) % 2


def rotate_dp(dp):
    return (dp + 1) % 4


def change_direction(direction):
    if direction.dp % 2 == direction.cc:
        return Direction(direction.dp, rotate_cc(direction.cc))
    return Direction(rotate_dp(direction.dp), direction.cc)


def invert_rotate_dp(dp, count=0):
    if count >= 0:
        return dp
    else:
        if dp != 0:
            return invert_rotate_dp(dp - 1, count + 1)
        return invert_rotate_dp(3, count + 1)


def execute_token(token, direction, stack):
    if isinstance(token, tokens.Black_token):
        new_direction = change_direction(direction)
        return new_direction, stack
    if isinstance(token, tokens.White_token):
        return direction, stack
    if isinstance(token, tokens.toColorToken):
        return execute_color_token(token, direction, stack)
    if isinstance(token, tokens.Terminate_token):
        return direction, stack
    raise ValueError


def execute_color_token(token, direction, stack):
    if token.token_type == "noop":
        return noop_operator(direction, stack)
    elif token.token_type == "push":
        return push_operator(token, direction, stack)
    elif token.token_type == "pop":
        return pop_operator(direction, stack)

    elif token.token_type == "add":
        return add_operator(direction, stack)
    elif token.token_type == "subtract":
        return subtract_operator(direction, stack)
    elif token.token_type == "multiply":
        return multiply_operator(direction, stack)

    elif token.token_type == "divide":
        return divide_operator(direction, stack)
    elif token.token_type == "mod":
        return mod_operator(direction, stack)
    elif token.token_type == "not":
        return not_operator(direction, stack)

    elif token.token_type == "greater":
        return greater_operator(direction, stack)
    elif token.token_type == "pointer":
        return pointer_operator(direction, stack)
    elif token.token_type == "switch":
        return switch_operator(direction, stack)

    elif token.token_type == "duplicate":
        return duplicate_operator(direction, stack)
    elif token.token_type == "roll":
        return roll_operator(direction, stack)
    elif token.token_type == "inN":
        return in_num_operator(direction, stack)

    elif token.token_type == "inC":
        return in_char_operator(direction, stack)
    elif token.token_type == "outN":
        return out_num_operator(direction, stack)
    elif token.token_type == "outC":
        return out_char_operator(direction, stack)
    else:
        raise ValueError


def noop_operator(direction, stack):
    return copy.deepcopy(direction), stack.copy()


def add_operator(direction, stack):
    stack = stack.copy()
    direction = copy.deepcopy(direction)
    if len(stack) < 2:
        return direction, stack
    stack.append(stack.pop() + stack.pop())
    return direction, stack


def subtract_operator(direction, stack):
    stack = stack.copy()
    direction = copy.deepcopy(direction)
    if len(stack) < 2:
        return direction, stack

    first = stack.pop()
    second = stack.pop()
    stack.append(second - first)
    return direction, stack


def multiply_operator(direction, stack):
    stack = list(stack)
    direction = copy.deepcopy(direction)
    if len(stack) < 2:
        return direction, stack
    stack.append(stack.pop() * stack.pop())
    return direction, stack


def divide_operator(direction, stack):
    stack = stack.copy()
    direction = copy.deepcopy(direction)
    if len(stack) < 2:
        return direction, stack
    first = stack.pop()
    second = stack.pop()
    if first == 0:
        return ZeroDivisionError
    stack.append(int(second / first))
    return direction, stack


def mod_operator(direction, stack):
    stack = stack.copy()
    direction = copy.deepcopy(direction)
    if len(stack) < 2:
        return direction, stack
    first = stack.pop()
    second = stack.pop()
    if first == 0:
        return ZeroDivisionError
    stack.append(second % first)
    return direction, stack


def greater_operator(direction, stack):
    stack = stack.copy()
    direction = copy.deepcopy(direction)
    if len(stack) < 2:
        return direction, stack

    first = stack.pop()
    second = stack.pop()

    stack.append(int(second > first))
    return direction, stack


def not_operator(direction, stack):
    stack = stack.copy()
    direction = copy.deepcopy(direction)
    if len(stack) < 1:
        return direction, stack

    result = 1 if stack.pop() == 0 else 0
    stack.append(result)
    return direction, stack


def pointer_operator(direction, stack):
    stack = stack.copy()
    direction = copy.deepcopy(direction)
    if len(stack) < 1:
        return direction, stack

    dp = direction.dp
    cc = direction.cc
    turn_count = stack.pop()
    if turn_count < 0:
        new_dp = invert_rotate_dp(dp, turn_count)
        return Direction(new_dp, cc), stack
    else:
        new_dp = (dp + (turn_count % 4)) % 4
        return Direction(new_dp, cc), stack
    pass


def switch_operator(direction, stack):
    stack = stack.copy()
    direction = copy.deepcopy(direction)
    if len(stack) < 1:
        return direction, stack
    turn_count = abs(stack.pop()) % 2
    new_cc = (direction.cc + turn_count) % 2
    return Direction(direction.dp, new_cc), stack


def in_num_operator(direction, stack):
    stack = stack.copy()
    direction = copy.deepcopy(direction)
    value = input("Input number: ")
    if value.isdigit():
        stack.append(int(value))
    return direction, stack


def in_char_operator(direction, stack):
    stack = stack.copy()
    direction = copy.deepcopy(direction)
    value = input("Input character")
    if len(value) < 1:
        return direction, stack

    stack.append(ord(value[0]))
    return direction, stack


def out_num_operator(direction, stack):
    stack = stack.copy()
    direction = copy.deepcopy(direction)
    if len(stack) < 1:
        return direction, stack
    print(stack.pop(), end="")
    return direction, stack


def out_char_operator(direction, stack):
    stack = stack.copy()
    direction = copy.deepcopy(direction)
    if len(stack) < 1:
        return direction, stack
    value = stack.pop()
    if value < 0:
        stack.append(value)
        return direction, stack

    print(chr(value), end="")
    return direction, stack


def push_operator(token, direction, stack):
    stack = stack.copy()
    direction = copy.deepcopy(direction)
    stack.append(token.block_size)
    return direction, stack


def pop_operator(direction, stack):
    stack = stack.copy()
    direction = copy.deepcopy(direction)
    if len(stack) < 1:
        return direction, stack
    stack.pop()
    return direction, stack


def duplicate_operator(direction, stack):
    stack = stack.copy()
    direction = copy.deepcopy(direction)
    if len(stack) < 1:
        return direction, stack

    value = stack.pop()
    stack.append(value)
    stack.append(value)
    return direction, stack


def roll_operator(direction, stack):
    stack = stack.copy()
    direction = copy.deepcopy(direction)
    if len(stack) < 2:
        return direction, stack
    rolls = stack.pop()
    depth = stack.pop()
    insert_index = len(stack) - depth
    stack = roll_stack(stack, rolls, insert_index)
    return direction, stack


def roll_stack(stack, rolls_count, insert_index):
    stack = stack.copy()
    if rolls_count > 0:
        stack.insert(insert_index, stack.pop())
        return roll_stack(stack, rolls_count - 1, insert_index)
    elif rolls_count < 0:
        stack.append(stack.pop(insert_index))
        return roll_stack(stack, rolls_count + 1, insert_index)
    else:
        return stack
