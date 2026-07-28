"""Pruebas unitarias de los índices de diversidad alfa (enigma_diversity.diversity).

Incluye una prueba de regresión explícita para el bug de Chao1 detectado
durante la auditoría de este proyecto: la fórmula original en el notebook
era `riqueza + n1**2 / (2*n2 + 1)`, que no corresponde a ninguna versión
publicada de Chao1. Esta prueba falla si esa fórmula (u otra incorrecta)
vuelve a introducirse por error al editar el código.
"""

import math

import numpy as np
import pandas as pd
import pytest

from enigma_diversity.diversity import calcular_diversidad_alfa, chao1, shannon, simpson


def test_chao1_valor_correcto_sesgo_corregido():
    """Chao1 debe usar S_obs + F1*(F1-1) / (2*(F2+1)), NO F1^2 / (2*F2+1)."""
    # 3 singletons (valor 1), 2 doubletons (valor 2), riqueza total = 7
    abundancias = np.array([1, 1, 1, 2, 2, 5, 10])

    esperado_correcto = 7 + (3 * 2) / (2 * 3)  # = 8.0
    esperado_formula_buggy = 7 + (3 ** 2) / (2 * 2 + 1)  # = 8.8 (fórmula incorrecta, no debe salir esto)

    resultado = chao1(abundancias)

    assert resultado == pytest.approx(esperado_correcto)
    assert resultado != pytest.approx(esperado_formula_buggy)


def test_chao1_sin_singletons_ni_doubletons_es_riqueza_observada():
    """Sin F1 ni F2, Chao1 no debe corregir nada: Chao1 = riqueza observada."""
    abundancias = np.array([5, 8, 12, 20])
    assert chao1(abundancias) == pytest.approx(4.0)


def test_chao1_vacio_es_cero():
    assert chao1(np.array([0, 0, 0])) == 0.0


def test_shannon_uniforme_da_ln_n():
    counts = np.array([10, 10, 10, 10])
    assert shannon(counts) == pytest.approx(math.log(4), rel=1e-4)


def test_simpson_rango_valido():
    counts = np.array([7, 3, 15, 1, 0, 9])
    valor = simpson(counts)
    assert 0.0 <= valor <= 1.0


def test_calcular_diversidad_alfa_columnas_esperadas():
    otu_table = pd.DataFrame({
        "pozo_1": [10, 0, 5, 1, 1],
        "pozo_2": [10, 20, 0, 2, 2],
    })

    resultado = calcular_diversidad_alfa(otu_table)

    assert list(resultado.columns) == ["Riqueza", "Shannon", "Simpson", "Chao1"]
    assert resultado.loc["pozo_1", "Riqueza"] == 4  # 4 OTUs presentes de 5
    assert resultado.loc["pozo_1", "Chao1"] >= resultado.loc["pozo_1", "Riqueza"]
