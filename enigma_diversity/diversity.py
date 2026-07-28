"""Índices de diversidad alfa: Riqueza, Shannon, Simpson y Chao1.

Chao1 usa la versión sesgo-corregida estándar (Chao 1987; por defecto en
QIIME2 y mothur): S_obs + F1*(F1-1) / (2*(F2+1)), donde F1 = singletons y
F2 = doubletons. Referencia: Chao, A. (1984). Nonparametric estimation of
the number of classes in a population. Scandinavian Journal of Statistics,
11, 265-270.

Nota histórica: la implementación original en el notebook tenía un bug —
usaba F1^2 / (2*F2 + 1), que no corresponde ni a la fórmula clásica de Chao1
(F1^2 / (2*F2)) ni a la versión sesgo-corregida. Se corrigió y esta función
existe también para que un test de regresión (tests/test_diversity.py)
impida que el bug vuelva a introducirse sin que las pruebas fallen.

Ver también: Deng, Umbach & Neufeld (2024, ISME Journal) — advertencia sobre
el uso de Chao1/ACE con datos ASV donde ya se removieron los singletons
(no aplica aquí porque se trabaja con tabla OTU, no ASV post-DADA2).
"""

import numpy as np
import pandas as pd


def chao1(abundancias):
    """Estimador de riqueza Chao1 (versión sesgo-corregida, Chao 1987).

    Parameters
    ----------
    abundancias : array-like
        Abundancias (conteos) de cada especie/OTU en UNA muestra.

    Returns
    -------
    float
        Riqueza estimada (>= riqueza observada).
    """
    abundancias = np.asarray(abundancias)
    presentes = abundancias[abundancias > 0]
    riqueza = len(presentes)
    if riqueza == 0:
        return 0.0
    n1 = np.sum(presentes == 1)
    n2 = np.sum(presentes == 2)
    return riqueza + (n1 * (n1 - 1)) / (2 * (n2 + 1))


def shannon(abundancias):
    """Índice de Shannon-Wiener: H' = -sum(p_i * ln(p_i))."""
    abundancias = np.asarray(abundancias)
    presentes = abundancias[abundancias > 0]
    if presentes.sum() == 0:
        return 0.0
    p = presentes / presentes.sum()
    return -np.sum(p * np.log(p + 1e-12))


def simpson(abundancias):
    """Índice de Simpson invertido (Gini-Simpson): 1 - sum(p_i^2)."""
    abundancias = np.asarray(abundancias)
    presentes = abundancias[abundancias > 0]
    if presentes.sum() == 0:
        return 0.0
    p = presentes / presentes.sum()
    return 1 - np.sum(p ** 2)


def calcular_diversidad_alfa(otu_table):
    """Calcula riqueza, Shannon, Simpson y Chao1 por muestra (columna) de una tabla OTU.

    Parameters
    ----------
    otu_table : pandas.DataFrame
        Filas = OTUs, columnas = muestras (mismo formato que el dataset ENIGMA).

    Returns
    -------
    pandas.DataFrame
        Índice = muestras, columnas = Riqueza, Shannon, Simpson, Chao1.
    """
    resultados = {}
    for muestra in otu_table.columns:
        abundancias = otu_table[muestra].values
        presentes = abundancias[abundancias > 0]
        resultados[muestra] = {
            "Riqueza": len(presentes),
            "Shannon": round(shannon(abundancias), 4),
            "Simpson": round(simpson(abundancias), 4),
            "Chao1": round(chao1(abundancias), 1),
        }
    return pd.DataFrame(resultados).T
