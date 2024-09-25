#! /usr/bin/env python3
import numpy as np
from matplotlib import pyplot, lines

from ._data import AMEDataset, dataframe_dict
from ._helpers import grid, grid_data, magic_lines, LINE, LABEL, GRAPH, CONTOUR
from ._parser import Args

ame = AMEDataset(2016)

def discrep(args: Args):
    args.ame.df['difference'] = args.ame.df.E - args.ame.semf(args.ame.df.N, args.ame.df.Z)

    max_n, max_z = 140, 90
    fig, ax, (N, Z) = grid(max_n, max_z, minor=10, major=20, min_nz=10)
    ax.set_title('Binding energy discrepancy $E_{N,Z} - SEMF(N,Z)$')
    
    data = dataframe_dict(args.ame.df, 'difference')
    E = grid_data(data, N, Z)
    
    minE, maxE = -200, 150
    E[E > 152] = float('nan')
    contours = np.linspace(minE, maxE, (maxE-minE)//25+1)
    contour = ax.contour(E, contours, **CONTOUR)

    E[E < minE] = minE
    E[E > maxE] = maxE

    image = ax.imshow(E, **GRAPH)
    cbar = fig.colorbar(image)
    cbar.ax.set_ylabel('Binding energy per nucleon')
    cbar.set_ticks(contours)
    labels = [str(int(x)) for x in contours]
    labels[-2] += ' keV'
    cbar.set_ticklabels(labels)
    cbar.add_lines(contour)

    # MAGIC NUMBERS
    LINE['axes'] = ax

    for i, ((n0, n1), (z0, z1)) in magic_lines(data, +5, data, +5):
        if n0:
            ax.add_line(lines.Line2D((n0, n1), (i, i), **LINE))
            x = n1 if n1 < max_n else n0 
            ax.annotate("$Z={}$".format(i), (x-2, i+0.5), **LABEL)
        if z0:
            ax.add_line(lines.Line2D((i, i), (z0, z1), **LINE))
            ax.annotate("$N={}$".format(i), (i+0.5, max(z0, 10)), **LABEL)

    fig.set_size_inches(7.4, 4)
    pyplot.savefig(args.ame.imgdir / 'discrep.png', transparent=args.transparent)

if __name__ == '__main__':
    discrep(Args.get())
