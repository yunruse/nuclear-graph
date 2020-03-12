from itertools import product

import numpy as np
import pandas as pd
from matplotlib import pyplot, colors, lines

from helpers import grid_data, magic_lines

N_REL = 60  # separation between n and p shell gaps as displayed

df2 = pd.read_fwf(
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

MAGIC = magic_lines(s2p, s2n)

## FIGURE
 
fig = pyplot.figure(constrained_layout=True)
ax = fig.add_subplot()
ax.set_title('Proton and neutron empirical shell gaps')
ax.set_ylabel('Number of protons $Z$')
ax.set_ylim(0, max_z-4)

N_TICKS = 1 + (max_n + N_REL) // 10
ax.set_xticks(range(0, 10*N_TICKS, 10), minor=True)
ax.set_xticks(range(0, 10*N_TICKS, 20))

Z_TICKS = 1 + (max_z) // 10
ax.set_yticks(range(0, 10*Z_TICKS, 10), minor=True)
ax.set_yticks(range(0, 10*Z_TICKS, 20))

ax.set_xlabel('Number of neutrons $N$ ($N+{}$ for neutron shell gaps)'.format(N_REL))
ax.set_xlim(0, max_n-4 + N_REL)

E = grid_data(shell_comb, N, Z)
img = ax.imshow(
    E, norm=colors.SymLogNorm(5), cmap='viridis', zorder=3)

# tick marks are nonlinear
SHELL_TICKS = (-1, 0, 1, 2, 3, 4, 5, 10, 20)
SHELL_TICKMARKS = list(map(str, SHELL_TICKS))
SHELL_TICKMARKS[-1] += ' MeV'

cbar = fig.colorbar(img, ticks=SHELL_TICKS)
cbar.ax.set_yticklabels(SHELL_TICKMARKS)
cbar.ax.set_ylabel('Empirical shell gap')

# MAGIC NUMBERS
LINE = dict(axes=ax, zorder=1, c='black', lw=0.4)
LABEL = dict(xycoords='data', color='gray', size=6)

for i, line in MAGIC.items():
    if i < 100:
        line['n'][1] += N_REL
        ax.add_line(lines.Line2D(line['n'], [i, i], **LINE))
        x = sum(line['n'])*0.5
        ax.annotate("$Z={}$".format(i), (x*0.95 + 5, i+0.5), **LABEL)
    
    for n in 0, N_REL:
        ax.add_line(lines.Line2D([i+n, i+n], line['z'], **LINE))
    ax.annotate("$N={}$".format(i), (i+N_REL+0.5, line['z'][0]), **LABEL)

NZ = NZ_LINE_STOPPER = 56
ax.add_line(lines.Line2D([    0,       NZ], [0, NZ], **LINE))
ax.add_line(lines.Line2D([N_REL, N_REL+NZ], [0, NZ], **LINE))

fig.set_size_inches(8.2, 4)
pyplot.savefig('shell_gap.png', transparency=True)
