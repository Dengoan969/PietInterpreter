import numpy as np
from PIL import Image
import Semantics.colors as colors
import Semantics.tokenization as tokenization
import Semantics.tokens as tokens
import Interpreter.commands as commands
from Infrastructure.structures import *
import copy


def make_step(state, token):
    if isinstance(token[0], tokens.Terminate_token):
        state.is_final = True
        return state
    next_state = copy.deepcopy(state)
    result = commands.execute_token(token[0], next_state.direction,
                                    next_state.stack)
    if isinstance(token[0], (tokens.White_token, tokens.toColorToken)):
        next_state.position = tokenization.get_next_position(
            token[1], next_state.direction.dp)
    next_state.direction = result[0]
    next_state.stack = result[1]
    return next_state


def run(pixel_data, state):
    pixel_color = tokenization.get_pixel(pixel_data, state.position)
    if colors.is_black(pixel_color):
        raise RuntimeError("Start on black pixel")
    while True:
        token = get_next_token(pixel_data, state)
        state = make_step(state, token)
        if state.is_final:
            return state


def run_in_debug(pixel_data, state):
    pixel_color = tokenization.get_pixel(pixel_data, state.position)
    if colors.is_black(pixel_color):
        raise RuntimeError("Start on black pixel")
    steps = 0
    is_run = False
    break_points = set()
    while True:
        if state.is_final:
            print_program_state(state)
            print(f'Total steps: {steps}')
            break
        token = get_next_token(pixel_data, state)
        print()
        print(f'STEP {steps}')
        print_next_step(token, state)
        print_program_state(state)
        if is_run and token[1] not in break_points:
            state = make_step(state, token)
            steps += 1
        else:
            command = input()
            while command.split()[0] == 'breakpoint':
                coords = command.split()[1:]
                break_point = Position(int(coords[0]), int(coords[1]))
                break_points.add(break_point)
                command = input()
            if command == 'step':
                is_run = False
                state = make_step(state, token)
                steps += 1
            elif command == 'run':
                if token[1] in break_points:
                    state = make_step(state, token)
                is_run = True


def get_next_token(pixel_data, state):
    color_block = tokenization.get_color_block(pixel_data, state.position)
    next_tokens = state.commands[color_block]
    return next_tokens[state.direction]


def print_next_step(next_token, state):
    next_position = tokenization.get_next_position(next_token[1],
                                                   state.direction.dp)
    print(f'Command To Execute: {next_token[0]}\n'
          f'Next Position: {next_position}')


def print_program_state(state):
    print(f'Current Position: {state.position}\n'
          f'Current Direction: {get_current_direction(state.direction)}\n'
          f'Current Stack: {state.stack}')
    print('-----------------------------')


def get_current_direction(direction):
    dp = direction.dp
    cc = direction.cc
    if dp == 0:
        result = 'Right-'
    elif dp == 1:
        result = 'Down-'
    elif dp == 2:
        result = 'Left-'
    else:
        result = 'Up-'
    if cc == 0:
        result += 'Left'
    else:
        result += 'Right'
    return result


def process_image(path):
    with Image.open(path) as img:
        image_data = img.convert('RGB')
        pixel_data = np.array(image_data)
    return pixel_data


def interpret(path, is_debug):
    pixel_data = process_image(path)
    all_tokens = tokenization.get_all_tokens(pixel_data)
    start = Position(0, 0)
    direction = Direction(0, 0)
    state = State(all_tokens, start, direction)
    if is_debug:
        return run_in_debug(pixel_data, state)
    return run(pixel_data, state)
