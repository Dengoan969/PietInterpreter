class Possible_colors:
    def __init__(self):
        self.main_colors = [
            [255, 192, 192],  # Light red
            [255, 0, 0],  # Red
            [192, 0, 0],  # Dark red
            [255, 255, 192],  # Light yellow
            [255, 255, 0],  # Yellow
            [192, 192, 0],  # Dark yellow
            [192, 255, 192],  # Light green
            [0, 255, 0],  # Green
            [0, 192, 0],  # Dark green
            [192, 255, 255],  # Light cyan
            [0, 255, 255],  # Cyan
            [0, 192, 192],  # Dark cyan
            [192, 192, 255],  # Light blue
            [0, 0, 255],  # Blue
            [0, 0, 192],  # Dark blue
            [255, 192, 255],  # Light magenta
            [255, 0, 255],  # Magenta
            [192, 0, 192]  # Dark magenta
        ]
        self.white = [255, 255, 255]
        self.black = [0, 0, 0]


possible_colors = Possible_colors()


def get_color_diff(current_color, next_color):
    current_color = list(current_color)
    next_color = list(next_color)
    if is_white(current_color) or is_white(next_color):
        return {"hue": 0, "light": 0}
    if not is_main_color(current_color) or not is_main_color(next_color):
        raise SyntaxError('Color not supported in current palette')
    current_index = possible_colors.main_colors.index(current_color)
    next_index = possible_colors.main_colors.index(next_color)
    hue = (int(next_index / 3) - int(current_index / 3)) % 6
    light = (next_index - current_index) % 3
    return {"hue": hue, "light": light}


def is_equal(color1, color2):
    return list(color1) == list(color2)


def is_white(color):
    return list(color) == possible_colors.white


def is_black(color):
    return list(color) == possible_colors.black


def is_main_color(color):
    return list(color) in possible_colors.main_colors
