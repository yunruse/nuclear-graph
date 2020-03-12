from itertools import product

import numpy as np
from matplotlib import pyplot, colors, lines

from data_shell_gap import *
 
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

E = gathers(shell_comb)(N, Z)
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
pyplot.savefig('shell_gap_mod.png', transparency=True)
