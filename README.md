# Diversidad Microbiana en Aguas Subterráneas — Estudio ENIGMA

**Pregunta:** ¿qué variables fisicoquímicas explican la diversidad bacteriana de un pozo de agua subterránea, y qué tan distintas son las comunidades entre pozos?

**Resultado en una frase:** en 67 pozos, la diversidad bacteriana correlaciona más fuerte con metales poco monitoreados (aluminio, cadmio, potasio, cobre, litio, sodio) que con las variables clásicas (pH, Fe, Mn, U) — hallazgo con implicación directa para rediseñar un panel de monitoreo ambiental.

Análisis de diversidad bacteriana (16S rRNA V4) en 67 pozos de agua subterránea, usando datos reales de secuenciación masiva y su relación con variables fisicoquímicas ambientales.

> Esta es la pieza que más conecta mi trabajo previo en microbiología con análisis de datos: mismo tipo de pregunta que trabajaba en el laboratorio — qué factores ambientales explican la composición de una comunidad microbiana — resuelta aquí con un flujo de datos completo en Python en vez de solo con herramientas de wet-lab.

---

## Dataset

| | |
|---|---|
| Fuente | [ENIGMA Study](https://enigma.lbl.gov/) — Zenodo, DOI: [10.5281/zenodo.1455792](https://doi.org/10.5281/zenodo.1455792) |
| Datos | Tabla de OTUs (abundancias bacterianas, 16S rRNA V4) + metadatos ambientales (pH, metales, gases disueltos, conductividad, etc.) |
| Autoría del dataset | Duvallet, C. (2018). *OTU table: Ecosystems and Networks Integrated with Genes and Molecular Assemblies (ENIGMA)*. Zenodo. Publicado bajo licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| Muestras | 67 pozos de agua subterránea, rarefaccionados a una profundidad común de 10,000 lecturas/pozo |

## Pregunta analítica

¿Cuáles variables fisicoquímicas del agua subterránea (pH, metales, conductividad, gases disueltos) están asociadas con la diversidad bacteriana de cada pozo, y qué tan distintas son las comunidades entre pozos?

## Metodología

1. **Carga y diagnóstico**: alineación de tabla de OTUs y metadatos ambientales por pozo; documentación de valores faltantes (13 variables ambientales, hasta 83.6% en `po4_mgl`).
2. **Diversidad alfa**: riqueza de OTUs, Shannon, Simpson y Chao1 por pozo.
3. **Diversidad beta**: matriz de distancias Bray-Curtis + ordenación PCoA.
4. **Asociación ambiental**: correlación de Spearman entre diversidad Shannon y variables fisicoquímicas.
5. Interpretación biológica de cada resultado, limitaciones y recomendaciones para monitoreo ambiental futuro.

## Hallazgos principales

- Los 67 pozos muestran variabilidad considerable en las cuatro métricas de diversidad alfa — no explicada por diferencias en profundidad de secuenciación (ya rarefaccionada).
- La mayoría de los pares de pozos presentan disimilitud media-alta en composición bacteriana (Bray-Curtis); el PCoA solo explica 17.6% de la varianza total (PC1: 10.3%, PC2: 7.3%), señal de que la estructura de las comunidades es compleja y no se reduce a 2 ejes.
- Las correlaciones más fuertes con la diversidad Shannon no fueron con las variables clásicamente monitoreadas (pH, Fe, Mn, U), sino con **aluminio, cadmio, potasio, cobre, litio y sodio** — hallazgo que sugiere ampliar el panel de monitoreo ambiental de estos pozos.

## Herramientas

Python (pandas, NumPy, SciPy) · Matplotlib/Seaborn · Plotly · Bray-Curtis/PCoA

## Fundamento científico y metodológico

Cada métrica se implementó siguiendo su formulación estándar en ecología microbiana, no una aproximación genérica:

- **Chao1**: versión sesgo-corregida `S_obs + F1(F1-1) / (2(F2+1))`, el estándar actual (es la versión por defecto en QIIME2 y mothur). Chao1 es apropiado aquí porque los datos son una **tabla de OTUs** clásica, no ASVs — un [artículo reciente en *The ISME Journal*](https://doi.org/10.1093/ismejo/wrae106) (Deng, Umbach & Neufeld, 2024) advierte que Chao1/ACE **no deben usarse sobre datos de ASVs** (p. ej. salidas de DADA2) porque estos pipelines eliminan los singletons por defecto, invalidando el supuesto estadístico del estimador. Cita original: Chao, A. (1984). *Nonparametric estimation of the number of classes in a population.* Scandinavian Journal of Statistics, 11, 265–270.
- **Shannon y Simpson**: fórmulas estándar (Shannon-Wiener; índice de Simpson invertido, 1-D).
- **Bray-Curtis**: Bray, J.R. & Curtis, J.T. (1957). *An Ordination of the Upland Forest Communities of Southern Wisconsin.* Ecological Monographs, 27, 325–349.
- **PCoA**: doble-centrado de Gower sobre distancias al cuadrado (Gower, J.C. (1966). *Some distance properties of latent root and vector methods used in multivariate analysis.* Biometrika, 53, 325–338) — el mismo algoritmo que usa `skbio.stats.ordination.pcoa`. La varianza explicada se calcula solo sobre autovalores positivos, igual que la implementación de referencia de scikit-bio; además, antes de filtrar por positividad se aplanan a cero los autovalores numéricamente insignificantes (ruido de punto flotante ~1e-15), tal como hace `skbio` internamente con `np.isclose`, para evitar ejes espurios en matrices de distancias de baja dimensión.
- **Limitación metodológica reconocida**: Bray-Curtis + PCoA sobre abundancias relativas no corrige por la naturaleza composicional de los datos de microbioma. Gloor et al. (2017), *Microbiome Datasets Are Compositional: And This Is Not Optional* (Frontiers in Microbiology, 8, 2224), recomienda transformación CLR + distancia de Aitchison como alternativa más rigurosa. Se documenta como una mejora futura, no como una corrección silenciosa — es una discusión activa en el campo, no un error.

## Rigor de reporte científico

Este proyecto se autoevaluó contra las **guías STREAMS** (Standards for Technical Reporting in Environmental and host-Associated Microbiome Studies — Kelliher et al. 2025, *Nature Microbiology*), el estándar vigente para reporte técnico de estudios de microbioma ambiental. Ver [`STREAMS_checklist.md`](STREAMS_checklist.md) para el detalle ítem por ítem, incluyendo qué partes corresponden al dataset original (muestreo, extracción, secuenciación) y cuáles son mi contribución directa (análisis, reproducibilidad, resultados, discusión).

## Código testeado: `enigma_diversity/`

Las funciones de diversidad alfa (Chao1, Shannon, Simpson) y de ordenación (PCoA) viven en un paquete Python separado del notebook, con pruebas unitarias en `tests/`:

```bash
pip install -r requirements.txt
pytest -q      # 9 pruebas — Chao1, Shannon, Simpson, PCoA
```

Esta separación existe por una razón concreta, no solo por estilo: la implementación original de Chao1 en el notebook tenía un error de fórmula (detectado y corregido durante la auditoría de este proyecto — usaba `F1² / (2·F2 + 1)` en vez de la versión sesgo-corregida `F1(F1-1) / (2(F2+1))`). `tests/test_diversity.py` incluye una prueba de regresión que falla explícitamente si esa fórmula incorrecta vuelve a aparecer. De la misma forma, `tests/test_ordination.py` verifica el PCoA contra un caso con solución analítica conocida (puntos colineales), lo que llevó a encontrar y corregir un segundo problema numérico (ejes espurios por ruido de punto flotante, ver sección anterior).

## Estructura del repositorio

```
├── README.md
├── STREAMS_checklist.md                          # Autoevaluación contra el estándar de reporte STREAMS (2025)
├── requirements.txt                               # Dependencias Python (pip install -r requirements.txt)
├── analisis_diversidad_microbiana_ENIGMA.ipynb   # Notebook completo (18 secciones: intro → conclusiones → guion de sustentación)
├── enigma_diversity/                             # Paquete Python: Chao1, Shannon, Simpson, PCoA (testeado)
│   ├── __init__.py
│   ├── diversity.py
│   └── ordination.py
├── tests/                                         # Pruebas unitarias (pytest), incluye regresión del bug de Chao1
│   ├── test_diversity.py
│   └── test_ordination.py
├── enigma.metadata.txt                           # Metadatos ambientales por pozo
├── otu_table_resampled_updated_r.txt             # Tabla de OTUs (16S rRNA V4)
└── feedback_profesor.pdf                         # Retroalimentación recibida (evidencia de evaluación externa)
```

## Autora

Karina Correa — [LinkedIn](https://linkedin.com/in/karina-correa-aparicio) · [GitHub](https://github.com/KARCOR)
