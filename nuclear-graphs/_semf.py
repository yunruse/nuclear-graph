from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.optimize import least_squares

@dataclass(frozen=True, slots=True)
class SEMF:
    """
    Semi-empirical binding formula coefficients.
    
    Stored in keV and can be optimised to a dataset.
    """
    # in keV
    aV: float
    aS: float
    aC: float
    aA: float
    aP: float

    def __call__(self, N: int, Z: int):
        A = Z + N
        sgn = np.where(A % 2 == 0, np.where(Z % 2 == 0, 1, -1), 0)
        return ( self.aV - self.aS / A**(1/3)
                    - self.aC * Z**2 / A**(4/3)
                    - self.aA * (N-Z)**2/A**2
                    + self.aP * sgn/A**1.5) 

    def __iter__(self):
        yield self.aV
        yield self.aS
        yield self.aC
        yield self.aA
        yield self.aP
    
    def _optimise(self, df: pd.DataFrame):
        A = df.N + df.Z
        # Reduce weight of error for small nuclei with linear cutoff
        clamp = np.vectorize(lambda x: 0 if x < 0 else 1 if x > 1 else x)
        CUTOFF = 5
        weights = clamp((A-CUTOFF)/CUTOFF)

        cls = type(self)
        def optfunc(params):
            semf = np.vectorize(cls(*params))
            return weights * (df.E - semf(df.N, df.Z))

        return least_squares(
            optfunc,
            list(self),
            verbose=1,
            loss="soft_l1")
    
    def optimise(self, df: pd.DataFrame):
        return type(self)(*self._optimise(df).x)



# The following constants were obtained from J.W. Rohlf.
# All except the last constant are keV.
LITERATURE_SEMF = SEMF(
    15750, 17800, 711,
    23700, 11180.01)

# This is what results from on AME 2016:
# SEMF_2016 = SEMF(
#     15123.31226824,
#     15791.00504405,
#     671.88325277,
#     21733.36561414,
#     10672.59798895
# )

if __name__ == '__main__':
    from ._parser import Args
    print(LITERATURE_SEMF._optimise(Args.get().ame.df))