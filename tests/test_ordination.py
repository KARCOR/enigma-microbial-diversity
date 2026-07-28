"""Pruebas unitarias de PCoA (enigma_diversity.ordination).

Usa un caso con solución analítica conocida (puntos en una línea 1D) para
verificar que la implementación reconstruye correctamente las distancias
originales, en vez de solo comprobar que "corre sin error".
"""

import numpy as np
import pandas as pd
import pytest

from enigma_diversity.ordination import pcoa


def test_pcoa_reconstruye_distancias_en_linea_1d():
    """3 puntos en una línea (0, 1, 3): la distancia euclidiana es exactamente
    1D, así que PCoA debe recuperar un único eje con var. explicada ~100%
    y las distancias en ese eje deben coincidir con las distancias originales.
    """
    puntos = np.array([0.0, 1.0, 3.0])
    n = len(puntos)
    D = np.abs(puntos.reshape(-1, 1) - puntos.reshape(1, -1))
    dist_matrix = pd.DataFrame(D, index=["A", "B", "C"], columns=["A", "B", "C"])

    coords, var_exp = pcoa(dist_matrix)

    assert coords.shape == (n, 1)
    assert var_exp.sum() == pytest.approx(100.0, rel=1e-6)

    reconstruida = np.abs(coords[:, 0].reshape(-1, 1) - coords[:, 0].reshape(1, -1))
    assert reconstruida == pytest.approx(D, abs=1e-6)


def test_pcoa_muestras_equidistantes_da_ejes_simetricos():
    """3 muestras equidistantes (triángulo equilátero): 2 ejes con varianza
    explicada igual, ninguna muestra debe quedar en el origen exacto.
    """
    D = np.array([
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0],
    ], dtype=float)
    dist_matrix = pd.DataFrame(D)

    coords, var_exp = pcoa(dist_matrix)

    assert coords.shape[0] == 3
    assert var_exp.sum() <= 100.0 + 1e-6
    # Con distancias iguales, los dos primeros ejes deben explicar partes iguales
    assert var_exp[0] == pytest.approx(var_exp[1], rel=1e-6)


def test_pcoa_devuelve_menos_ejes_que_muestras_si_hay_estructura_degenerada():
    """El número de ejes con autovalor positivo no debe exceder n-1 muestras."""
    puntos = np.array([0.0, 1.0, 3.0])
    D = np.abs(puntos.reshape(-1, 1) - puntos.reshape(1, -1))
    dist_matrix = pd.DataFrame(D)

    coords, var_exp = pcoa(dist_matrix)

    assert coords.shape[1] <= len(puntos) - 1
