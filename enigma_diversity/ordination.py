"""PCoA (Principal Coordinates Analysis) vía doble centrado de Gower.

Implementación de referencia: Gower, J.C. (1966). Some distance properties
of latent root and vector methods used in multivariate analysis. Biometrika,
53(3-4), 325-338.

Sigue la misma convención que la implementación de referencia de scikit-bio
(skbio.stats.ordination.pcoa): solo se suman los autovalores no-negativos
para calcular la proporción de varianza explicada (los autovalores negativos
pueden aparecer cuando la matriz de distancias no es euclidiana, p. ej.
Bray-Curtis, y se descartan en vez de reportarse como varianza "negativa").

También sigue la práctica de scikit-bio de "aplanar a cero" los autovalores
que son numéricamente ~0 (ruido de punto flotante del orden de 1e-15) antes
de decidir cuáles son positivos — ver `skbio/stats/ordination/
_principal_coordinate_analysis.py`, donde se usa `np.isclose(eigvals, 0)`
para esto. Sin este paso, matrices de distancias euclidianas de baja
dimensión (p. ej. 3 muestras perfectamente colineales) pueden reportar un
eje espurio con varianza explicada ~0% pero autovalor nominalmente positivo,
lo cual una prueba de regresión (tests/test_ordination.py) detectó en este
proyecto.
"""

import numpy as np


def pcoa(dist_matrix):
    """Calcula el PCoA (ordenación de comunidades en 2D+) desde una matriz de distancias.

    Parameters
    ----------
    dist_matrix : pandas.DataFrame o numpy.ndarray
        Matriz de distancias cuadrada y simétrica (p. ej. Bray-Curtis entre muestras).

    Returns
    -------
    coords : numpy.ndarray
        Coordenadas de cada muestra en los ejes principales (autovalores > 0,
        tras aplanar a cero el ruido numérico cercano a 0).
    var_exp : numpy.ndarray
        Porcentaje de varianza explicada por cada eje (suma <= 100).
    """
    D = np.asarray(getattr(dist_matrix, "values", dist_matrix), dtype=float).copy()
    D2 = D ** 2
    row_mean = D2.mean(axis=1, keepdims=True)
    col_mean = D2.mean(axis=0, keepdims=True)
    grand_mean = D2.mean()
    B = -0.5 * (D2 - row_mean - col_mean + grand_mean)
    eigenvalues, eigenvectors = np.linalg.eigh(B)

    # Igual que scikit-bio: aplanar a 0 el ruido numérico antes de filtrar
    # por positividad (evita ejes espurios con autovalor ~1e-15).
    eigenvalues = np.where(np.isclose(eigenvalues, 0), 0, eigenvalues)

    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    pos = eigenvalues > 0
    coords = eigenvectors[:, pos] * np.sqrt(eigenvalues[pos])
    var_exp = eigenvalues[pos] / eigenvalues[pos].sum() * 100
    return coords, var_exp
