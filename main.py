import argparse
from Interpreter.interpretation import interpret


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('path', type=str)
    return parser.parse_args()


def main(args):
    interpret(args.path, args.debug)


if __name__ == '__main__':
    main(get_args())
