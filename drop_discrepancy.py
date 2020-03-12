import numpy as np
from matplotlib import pyplot, colors, lines

from drop_data import df, df_dict, binding_per_nucleon
from helpers import grid, grid_data, magic_lines, LINE, LABEL, GRAPH, CONTOUR

df['difference'] = df.E - binding_per_nucleon(df.N, df.Z)

if __name__ == '__main__':
    max_n, max_z = 140, 90
    fig, ax, (N, Z) = grid(max_n, max_z, minor=10, major=20, min_nz=10)
    ax.set_title('Binding energy discrepancy $E_{N,Z} - SEMF(N,Z)$')
    
    data = df_dict('difference')
    E = grid_data(data, N, Z)
    
    minE, maxE = -50, 150
    E[E > 152] = float('nan')
    contours = np.linspace(minE, maxE, (maxE-minE)//25+1)
    contour = ax.contour(E, contours, **CONTOUR)

    E[E < minE] = minE
    E[E > maxE] = maxE

    image = ax.imshow(E, **GRAPH)
    cbar = fig.colorbar(image)
    cbar.ax.set_ylabel('Binding energy per nucleon (keV)')
    cbar.set_ticks(contours)
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

    fig.set_size_inches(7.1, 4)
    pyplot.savefig('drop_discrepancy.png', transparency=True)
