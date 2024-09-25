from argparse import ArgumentParser
from ._data import AMEDataset

parser = ArgumentParser()
parser.add_argument(
    'year',
    choices=['2016', '2020'],
    help="Dataset year to use.",
)
parser.add_argument(
    '--transparent', '-t',
    action='store_true',
    help="Use transparent backing",
)

class Args:
    transparent: bool
    year: int

    ame: AMEDataset

    @classmethod
    def get(cls) -> 'Args':
        args = parser.parse_args()
        args.ame = AMEDataset(
            year=args.year
        )
        return args

if __name__ == '__main__':
    print(Args.get())