from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from ._semf import SEMF, LITERATURE_SEMF

def dataframe_dict(df: pd.DataFrame, tag: str):
    return {(row.N, row.Z): row[tag] for _, row in df.iterrows()}

@dataclass
class AMEDataset:
    year: int

    @property
    def dir(self):
        p = Path(f'data/{self.year}')
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def imgdir(self):
        p = Path(f'img/{self.year}')
        p.mkdir(parents=True, exist_ok=True)
        return p

    # TODO: standardise a bit
    # and add full df table extraction

    def __post_init__(self):
        df = pd.read_fwf(
            self.dir / 'mass.txt',
            usecols=(2, 3, 11),
            names=tuple('NZE'),
            widths=(1,3,5,5,5,1,3,4,1,13,11,11,9,1,2,11,9,1,3,1,12,11,1),
            header=39, index_col=False
        )

        # drop predicted values and convert to MeV
        df['E_exp'] = pd.to_numeric(df.E, errors='coerce')
        df['E_known'] = 1 - pd.isnull(df.E_exp)
        df['E'] = pd.to_numeric(df.E.str.replace('#',''))

        self.df = df
        self._semf = None
    
    @property
    def semf(self) -> SEMF:
        if self._semf is None:
            self._semf = LITERATURE_SEMF.optimise(self.df)
        return self._semf
