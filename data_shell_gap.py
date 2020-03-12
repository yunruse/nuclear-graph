from itertools import product

import pandas
import numpy as np

N_REL = 60

def gathers(k):
    return np.vectorize(lambda n, z: k.get((n,z), float('nan')) )

df2 = pandas.read_fwf(
    'rct1-16.txt',
    usecols=(1, 3, 4, 6),
    names='A Z s2n s2p'.split(),
    widths=(1,3,4,4,11,8,10,8),
    header=39, index_col=False
)

s2n = {}
s2p = {}
max_n, max_z = 0, 0

for a, z, *s2 in df2.values:
    try:
        n_, p_ = (float(str(x).replace('#', '')) for x in s2)
    except ValueError:
        continue
    n = a - z
    s2n[n, z] = n_ / 1000
    s2p[n, z] = p_ / 1000
    max_n = max(max_n, n)
    max_z = max(max_z, z)

shell_p = {}
shell_n = {}
shell_comb = {}

for n, z in product(range(max_n+1), range(max_z+1)):
    if (n, z) not in s2p:
        continue
    
    if (n,   z+2) in s2p:
        shell_p[n, z] = shell_comb[n,       z] = s2p[n,z] - s2p[n,  z+2]
    if (n+2, z  ) in s2n:
        shell_n[n, z] = shell_comb[n+N_REL, z] = s2n[n,z] - s2n[n+2,z  ]

z = np.arange(0, max_z+1)
n = np.arange(0, max_n+1 + N_REL)
N, Z = np.meshgrid(n, z)

MAGIC_ = ()
MLT = MAGIC_LINE_EXTENSION = 5
MAGIC = {
    i: {'n': (
        min(n for n, z in s2p if z == i) + MLT,
        max(n for n, z in s2p if z == i) - MLT + N_REL
    ) if i < 100 else (0, 0),
        'z': (
        min(z for n, z in s2n if n == i) - MLT,
        max(z for n, z in s2n if n == i) + MLT
    )} for i in (8, 20, 28, 50, 82, 126)
}
