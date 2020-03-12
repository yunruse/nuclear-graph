import numpy as np
from matplotlib import pyplot

from drop_data import gathers, binding_per_nucleon

def prediction(do_ticks, show_title, do_contours, do_stable):
    fig, ax = pyplot.subplots(constrained_layout=True)

    ax.set_xlabel('Number of neutrons $N$')
    ax.set_xlim(0, 140)
    n = np.arange(1, 143)

    ax.set_ylabel('Number of protons $Z$')
    ax.set_ylim(0, 90)
    z = np.arange(1, 93)

    N, Z = np.meshgrid(n, z)
    E = binding_per_nucleon(N, Z) / 1000
    E[E<0] = 0
    image = ax.imshow(E, cmap='viridis', origin='lower', alpha=1)

    if do_ticks:
        ax.set_xticks(range(10, 140, 10), minor=True)
    else:
        ax.set_xticks([])
        ax.set_yticks([])

    if show_title:
        ax.set_title('Semi-empirical mass formula $SEMF(N, Z)$')

    if do_contours:

        cbar = fig.colorbar(image)
        cbar.ax.set_ylabel('Binding energy per nucleon (MeV)')

        M = E.max()
        contours = (0, M-8, M-4, M-2, M-1, M-1/2, M-1/4, M-1/8)
    else:
        contours = (0, )
        
    contour_lines = ax.contour(E, contours, cmap='magma')
    if do_contours:
        cbar.add_lines(contour_lines)

    if do_stable:
        E_known = gathers('E_known', 0)(N, Z)
        experimental_contour = ax.contour(E_known, (0,), cmap='gray',
            linestyles=('dashed', ), linewidths=(0.5, ))
    

    fig.set_size_inches(7.1, 4)
    pyplot.savefig('drop_prediction.png', transparent=True)

if __name__ == '__main__':
    prediction(do_ticks=False, show_title=True, do_contours=True, do_stable=False)
