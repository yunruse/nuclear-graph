# Exploring current nuclear models

Graphs on the Semi-Empirical Mass Formula (SEMF), an approximation for binding energy, as configured with least-squares fit, and as contrasted to experimentally-obtained mass discrepancies<sup>2</sup>.

> [!INFO]
>
> These graphs are used on Wikipedia. Click a graph to see the relevant Wikimedia Commons article, including articles they are used on.
> They, and the source code, are in the public domain under the Creative Commons CC0 license.

## `drop`: Liquid drop model
<a href="https://commons.wikimedia.org/wiki/File:Semi-empirical_mass_formula.png">
  <img src="img/drop.png"/>
</a>

The mean binding energy of the semi-empirical mass formula. Observe that below 8 MeV nuclei rapidly become unstable outside the region of nuclei that have been discovered (as indicated by a dashed line). Contours double in energy difference as moving away from the maximum predicted binding energy. 

## `discrep`: Liquid drop model discrepancies
<a href="https://commons.wikimedia.org/wiki/File:Semi-empirical_mass_formula_discrepancy.png">
  <img src="img/discrep.png"/>
</a>

The discrepancy between experimentally-obtained binding energies and those predicted by the SEMF. Energy colours are trimmed to the range *-50 < E < 150* for contrast.

## `shell` Nuclear shell gaps

<a href="https://commons.wikimedia.org/wiki/File:Empirical_Shell_Gap.png">
  <img src="img/shell.png"/>
</a>

The empirical shell gaps are the kernel [1, 0, -2, 0, 1] applied to extract local features:
```
Δ2p(N,Z) = E(N,Z-2) - 2 E(N,Z) + E(N,Z+2) 
Δ2n(N,Z) = E(N-2,Z) - 2 E(N,Z) + E(N+2,Z)
```

This uses a distance of two nuclides to avoid spin effects.

## References

1. Rohlf, J.W. Modern Physics from &alpha; to Z<sup>0</sup>. Wiley (1994).
2. Wang, M., et al. The AME2016 mass evaluation.
