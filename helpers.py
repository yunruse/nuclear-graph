from matplotlib import pyplot
import numpy as np

NaN = float('NaN')

def grid_data(dictionary, N, Z, orelse=NaN):
    f = np.vectorize(lambda n, z: dictionary.get((n, z), orelse))
    return f(N, Z)

# style

def grid(max_n, max_z, minor, major, min_nz=0, data_min=0):
    '''
    Create a typical NZ grid with minor and major ticks.
    '''
    fig, ax = pyplot.subplots(constrained_layout=True)
    ax.set_xlabel('Number of neutrons $N$')
    ax.set_ylabel('Number of protons $Z$')
    ax.set_xlim(min_nz, max_n)
    ax.set_ylim(min_nz, max_z)
    r = lambda m, b: range(min_nz, 10*(1+m//10), b)
    for m, f in (max_n, ax.set_xticks), (max_z, ax.set_yticks):
        f(r(m, major)); f(r(m, minor), minor=True)
    n = np.arange(data_min, max_n+2)
    z = np.arange(data_min, max_z+2)
    return fig, ax, np.meshgrid(n, z)

LINE    = dict(zorder=1, c='black', lw=0.4)
GRAPH   = dict(zorder=3, cmap='viridis', origin='lower')
CONTOUR = dict(zorder=5, colors=('white', 'black'), linestyles='dotted', linewidths=0.5)
LABEL   = dict(zorder=7, c='gray',  size=6, xycoords='data')

magic_lines = lambda p_data, p_width, n_data, n_width: {
    i: ((
        min(n for n, z in p_data if z == i) - p_width,
        max(n for n, z in p_data if z == i) + p_width
    ) if i < 100 else (None, None),
        (  
        min(z for n, z in n_data if n == i) - n_width,
        max(z for n, z in n_data if n == i) + n_width
    )) for i in (8, 20, 28, 50, 82, 126)
}.items()
