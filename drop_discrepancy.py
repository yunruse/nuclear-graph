import numpy as np
from matplotlib import pyplot, colors, lines

from helpers import magic_lines, grid_data
from drop_data import df, df_dict, binding_per_nucleon

df['difference'] = df.E - binding_per_nucleon(df.N, df.Z)

if __name__ == '__main__':
    fig, ax = pyplot.subplots(constrained_layout=True)
    ax.set_title('Binding energy discrepancy $E_{N,Z} - SEMF(N,Z)$')
    minZN, maxZ, maxN = 10, 90, 140

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
    data = df_dict('difference')
    E = grid_data(data, N, Z)
    E[N < minZN] = E[Z < minZN] = 0
    
    minE, maxE = -50, 150
    E[E > 152] = float('nan')
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
    pyplot.savefig('drop_discrepancy.png', transparency=True)
