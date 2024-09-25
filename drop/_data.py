import pandas as pd
import numpy as np

df = pd.read_fwf(
    'data/mass16.txt',
    usecols=(2, 3, 11),
    names=tuple('NZE'),
    widths=(1,3,5,5,5,1,3,4,1,13,11,11,9,1,2,11,9,1,3,1,12,11,1),
    header=39, index_col=False
)

df_dict = lambda tag: {(d.N, d.Z): d[tag] for i, d in df.iterrows()}

# drop predicted values and convert to MeV
df['E_exp'] = pd.to_numeric(df.E, errors='coerce')
df['E_known'] = 1 - pd.isnull(df.E_exp)
df['E'] = pd.to_numeric(df.E.str.replace('#',''))

# The following constants were obtained from J.W. Rohlf.
# All except the last constant are keV.
DEFAULT_CONSTS = np.array([
    15750, 17800, 711,
    23700, 11180.01])

def binding(consts):
    aV, aS, aC, aA, aP = consts
    def func(N, Z):
        A = Z + N
        sgn = 0 if A % 2 else (-1 if Z % 2 else +1)
        return ( aV - aS / A**(1/3)
                    - aC * Z**2 / A**(4/3)
                    - aA * (N-Z)**2/A**2
                    + aP * sgn/A**1.5)                  
    return np.vectorize(func)

# as obtained through the optimisation below
CONSTS = np.array([
    15123.31226824,
    15791.00504405,
    671.88325277,
    21733.36561414,
    10672.59798895
])

binding_per_nucleon = binding(CONSTS)

A = df.N + df.Z
# Reduce weight of error for small nuclei with linear cutoff
clamp = np.vectorize(lambda x: 0 if x < 0 else 1 if x > 1 else x)
Q = 5
weights = clamp((A-Q)/Q)

def optimise():
    from scipy.optimize import least_squares
    return least_squares(
        lambda param: weights * (df.E - binding(param)(df.N, df.Z) ),
        DEFAULT_CONSTS,
        verbose=1,
        loss="soft_l1")

if __name__ == '__main__':
    print(optimise())
