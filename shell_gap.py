from itertools import product

import numpy as np
import pandas as pd
from matplotlib import pyplot, colors, lines

from helpers import grid, grid_data, magic_lines, LINE, LABEL, GRAPH, CONTOUR

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

## FIGURE

fig, ax, (N, Z) = grid(max_n-4+N_REL, max_z-4, minor=10, major=20)
ax.set_title('Empirical shell gaps for binding energy $E$')
ax.set_xlabel('Number of neutrons $N$ ($N+{}$ for neutron shell gaps)'.format(N_REL))

E = grid_data(shell_comb, N, Z)
contour = ax.contour(E, (0, 1), **CONTOUR)
img = ax.imshow(E, norm=colors.SymLogNorm(5), **GRAPH)

# tick marks are nonlinear
SHELL_TICKS = (-1, 0, 1, 2, 3, 4, 5, 10, 20)
SHELL_TICKMARKS = list(map(str, SHELL_TICKS))
SHELL_TICKMARKS[-1] += ' MeV'

cbar = fig.colorbar(img, ticks=SHELL_TICKS)
cbar.ax.set_yticklabels(SHELL_TICKMARKS)
cbar.ax.set_ylabel('Empirical shell gap')
cbar.add_lines(contour)

# MAGIC NUMBERS
LINE['axes'] = ax

for i, ((n0, n1), (z0, z1)) in magic_lines(s2p, -5, s2n, +5):
    if n0:
        n1 += N_REL
        ax.add_line(lines.Line2D((n0, n1), (i, i), **LINE))
        x = (n0+n1)/2
        ax.annotate("$Z={}$".format(i), (x*0.95 + 5, i+0.5), **LABEL)
    
    for n in 0, N_REL:
        ax.add_line(lines.Line2D((i+n, i+n), (z0, z1), **LINE))
    ax.annotate("$N={}$".format(i), (i+N_REL+0.5, z0), **LABEL)

NZ = NZ_LINE_STOPPER = 56
ax.add_line(lines.Line2D([    0,       NZ], [0, NZ], **LINE))
ax.add_line(lines.Line2D([N_REL, N_REL+NZ], [0, NZ], **LINE))

for l, xy in (
    ('Proton shell gap \n$Δ_{2p}(N,Z)=E_{N,Z+2}+E_{N,Z-2}-2E_{N,Z}$', (20, 90)),
    ('Neutron shell gap\n$Δ_{2n}(N,Z)=E_{N+2,Z}+E_{N-2,Z}-2E_{N,Z}$', (130, 20))
):
    ax.annotate(l, xy)

fig.set_size_inches(9, 4)
pyplot.savefig('shell_gap.png', transparency=True)
