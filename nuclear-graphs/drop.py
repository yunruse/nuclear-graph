#! /usr/bin/env python3
import numpy as np
from matplotlib import pyplot

from ._helpers import grid_data, grid, GRAPH
from ._data import AMEDataset, dataframe_dict
from ._parser import Args

ame = AMEDataset(2016)

def prediction(args: Args, do_ticks, show_title, do_contours, do_stable):
    fig, ax, (N, Z) = grid(140, 90, major=10, minor=20, min_nz=0, data_min=1)

    E = args.ame.semf(N, Z) / 1000
    E[E<0] = 0
    image = ax.imshow(E, **GRAPH)

    if not do_ticks:
        ax.set_xticks([]); ax.set_yticks([])

    if show_title:
        ax.set_title('Binding energy per nucleon $SEMF(N, Z)/A$')

    if do_contours:
        cbar = fig.colorbar(image)

        M = E.max()
        contours = (0, M-8, M-4, M-2, M-1, M-1/2, M-1/4, M-1/8)
    else:
        contours = (0, )

    ticks = np.arange(0, 9, 1)
    labels = [str(int(x)) for x in ticks]
    labels[-1] += ' MeV'
        
    contour_lines = ax.contour(E, contours, cmap='magma', zorder=5)
    if do_contours:
        cbar.add_lines(contour_lines)
    cbar.set_ticks(ticks)
    cbar.set_ticklabels(labels)

    if do_stable:
        E_known = grid_data(dataframe_dict(args.ame.df, 'E_known'), N, Z, orelse=0)
        experimental_contour = ax.contour(
            E_known, (-10, 0), zorder=5,
            cmap='gray', linestyles=('dashed', ), linewidths=(0.5, ))

    fig.set_size_inches(7, 4)
    pyplot.savefig(args.ame.imgdir / 'drop.png', transparent=args.transparent)

if __name__ == '__main__':
    prediction(Args.get(), do_ticks=True, show_title=True, do_contours=True, do_stable=True)
