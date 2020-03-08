import numpy as np
from matplotlib import pyplot, colors
import pandas as pd

df2 = pd.read_fwf(
    'rct1-16.txt',
    usecols=(1, 3, 4, 5, 6, 7),
    names='A Z s2n s2nd s2p s2pd'.split(),
    widths=(1,3,5,5,5,1,3,4,1,13,11,11,9,1,2,11,9,1,3,1,12,11,1),
    header=39, index_col=False
)

E = {}  # (N, Z): {}
maxN, maxZ = 0, 0

for A, Z, s2n, s2nd, s2p, s2pd in df2.values:
    try:
        s2n = float(s2n)
        s2p = float(s2p)
    except ValueError:
        continue
    N = A - Z
    E[N, Z] = {'s2n': s2n, 's2p': s2p}
    maxN = max(maxN, N)
    maxZ = max(maxZ, Z)

for N, Z in zip(range(maxN+1), range(maxZ+1)):
    if (N, Z) not in E:
        continue
    if (N, Z+2) in E:
        E[N, Z]['d2p'] = E[N,Z]['s2p'] - E[N,  Z+2]['s2p']
    if (N, Z+2) in E:
        E[N, Z]['d2n'] = E[N,Z]['s2p'] - E[N+2,Z  ]['s2n']

gathers = lambda k: np.vectorize(lambda n, z: (E[N,Z][k] if (N,Z) in E else float('nan')))

if __name__ == '__main__':
    fig, ax = pyplot.subplots(constrained_layout=True)
    ax.set_title('Binding energy discrepancy $E_{exp} - E_{pred}$')
    minZN = 4

    ax.set_ylabel('Number of protons $Z$')
    z = np.arange(0, maxZ+1)
    ax.set_ylim(minZN, maxZ)
    magicP = (20, 28, 50, 82)
    ax.set_yticks(magicP, minor=False)
    for y in magicP: ax.axhline(y, c='black', ls='dashed', lw=0.2)

    ax.set_xlabel('Number of neutrons $N$')
    n = np.arange(0, maxN+1)
    ax.set_xlim(minZN, maxN)
    magicN = (20, 28, 50, 82, 126)
    ax.set_xticks(magicN, minor=False)
    for x in magicN: ax.axvline(x, c='black', ls='dashed', lw=0.2)

    energy = 'Binding energy per nucleon (keV)'
    N, Z = np.meshgrid(n, z)
    E = gathers('s2p')(N, Z)
    E[N < minZN] = E[Z < minZN] = 0
    
    minE, maxE = -50, 150
    E[E > 152] = float('nan')  # Include doubly-magic (50, 50)
    contours = np.linspace(minE, maxE, (maxE-minE)//25+1)
    contour = ax.contour(
        E, contours, colors=('black', 'white'),
        linestyles='dotted', linewidths=0.5)

    E[E < minE] = minE
    E[E > maxE] = maxE

    image = ax.imshow(E, cmap='viridis', origin='lower')
    cbar = fig.colorbar(image)
    cbar.ax.set_ylabel(energy)
    cbar.set_ticks(contours)
    cbar.add_lines(contour)

    fig.set_size_inches(7.1, 4)
    pyplot.show()
    pyplot.savefig('s2n.png', transparency=True)
