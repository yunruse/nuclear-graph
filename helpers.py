import numpy as np

NaN = float('NaN')

def grid_data(dictionary, N, Z, orelse=NaN):
    f = np.vectorize(lambda n, z: dictionary.get((n, z), orelse))
    return f(N, Z)

MLT = MAGIC_LINE_EXTENSION = 5
magic_lines = lambda p_data, n_data: {
    i: {'n': [
        min(n for n, z in p_data if z == i) + MLT,
        max(n for n, z in p_data if z == i) - MLT
    ] if i < 100 else (0, 0),
        'z': [
        min(z for n, z in n_data if n == i) - MLT,
        max(z for n, z in n_data if n == i) + MLT
    ]} for i in (8, 20, 28, 50, 82, 126)
}
