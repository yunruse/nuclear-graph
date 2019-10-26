import pandas as pd
import numpy as np

# http://www.oecd-nea.org/dbdata/data/mass-evals2003/mass.mas03
df = pd.read_fwf(
    'mass.mas03',
    usecols=(2, 3, 11),
    names=tuple('NZE'),
    widths=(1,3,5,5,5,1,3,4,1,13,11,11,9,1,2,11,9,1,3,1,12,11,1),
    header=39, index_col=False
)

# drop predicted values and convert to MeV
df['E_known'] = 1 - pd.isnull(df.E)
df.E = pd.to_numeric(df.E, errors='coerce')

def gathers(name, orelse):
    data = {(data.N, data.Z): data[name] for i, data in df.iterrows()}
    return np.vectorize(lambda n, z: data.get((n,z), orelse))

aV, aS, aC, aA, delta0 = 15750, 17800, 711, 23700, 11180  # MeV

@np.vectorize
def binding_per_nucleon(N, Z):
    A = Z + N
    sgn = 0 if A % 2 else (-1 if Z % 2 else +1)
    return ( aV - aS / A**(1/3)
                - aC * Z**2 / A**(4/3)
                - aA * (A-2*Z)**2/A**2
                + delta0 * sgn/A**(3/2)
    )

    delta = 0
    if N % 2:
        delta += rmac * Bs / N**(1/3)
    if Z % 2:
        delta += rmac * Bs / Z**(1/3)
    if N % 2 and Z % 2:
        delta -= h / (Bs *  A**(2/3))

    kFrp = (9*pi*Z/(4*A))**(1/3) * rp / r0
    fkr = -1/8 * (rp**2 *e2)/(r0**3) * (
        145/48
        - 327/2880 * kFrp**2
        + 1527/1209600 * kFrp**4
    )
    
    I = (N-Z)/A
    return (
        MH * Z + MN * N
        - aV * (1-kV*I**2)  * A
        + aS * (1-kS*I**2)  * A**(2/3) * b1
        + a0
        + c1*b3 * Z**2      * A**(-1/3)
        - c4    * Z**(4/3)  * A**(-1/3)
        + fkr   * Z**2      * A**(-1/3)
        + delta
        + ca * (N - Z)
        + W  * (abs(I) + (1/A if Z % 2 and Z==N else 0))
        - a_el  * Z**(2.39)
    ) / -A
