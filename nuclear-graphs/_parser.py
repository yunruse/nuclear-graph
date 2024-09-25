from argparse import ArgumentParser
from typing import TypedDict

parser = ArgumentParser()
parser.add_argument(
    '--transparent', '-t', action='store_true',
    help="Use a transparent backing to the graph."
)

class Args:
    transparent: bool

    @classmethod
    def get(cls) -> 'Args':
        return parser.parse_args()

if __name__ == '__main__':
    print(Args.get())