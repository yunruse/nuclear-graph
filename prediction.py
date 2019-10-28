import numpy as np
from matplotlib import pyplot

from data import gathers, binding_per_nucleon

if __name__ == '__main__':
    fig, ax = pyplot.subplots(constrained_layout=True)
    ax.set_title('Semi-empirical mass formula $SEMF(N, Z)$')

    ax.set_xlabel('Number of neutrons $N$')
    ax.set_xlim(0, 140)
    n = np.arange(1, 143)
    ax.set_xticks(range(10, 140, 10), minor=True)

    ax.set_ylabel('Number of protons $Z$')
    ax.set_ylim(0, 90)
    z = np.arange(1, 93)

    N, Z = np.meshgrid(n, z)
    E = binding_per_nucleon(N, Z)
    E[E<0] = 0
    image = ax.imshow(E, cmap='viridis', origin='lower', alpha=1)
    
    E_known = gathers('E_known', 0)(N, Z)
    experimental_contour = ax.contour(E_known, (0,), cmap='gray',
        linestyles=('dashed', ), linewidths=(0.5, ))

    cbar = fig.colorbar(image)
    cbar.ax.set_ylabel('Binding energy per nucleon (keV)')

    M = E.max()
    contours = (0, M-8000, M-4000, M-2000, M-1000, M-500, M-250, M-125)
    cbar.add_lines(ax.contour(E, contours, cmap='magma'))

    pyplot.show()