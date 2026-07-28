# Checklist STREAMS — Diversidad Microbiana en Aguas Subterráneas (ENIGMA)

Autoevaluación siguiendo las **guías STREAMS** (Standards for Technical Reporting in Environmental and host-Associated Microbiome Studies), Kelliher, J.M. et al. (2025), *Nature Microbiology* 10, 3059–3068. [10.1038/s41564-025-02186-2](https://doi.org/10.1038/s41564-025-02186-2). Guía completa y plantilla oficial: [streamsmicrobiome.org](https://streamsmicrobiome.org) · Zenodo: [10.5281/zenodo.15014818](https://doi.org/10.5281/zenodo.15014818).

> **Nota importante sobre el alcance de este checklist:** este proyecto es un **reanálisis de datos públicos ya publicados** (Duvallet, C. 2018, ENIGMA Study, Zenodo), no una colección primaria de muestras. Por lo tanto, los ítems de diseño de muestreo, extracción de ácidos nucleicos, secuenciación y controles de laboratorio (secciones 3–6) corresponden al estudio original y se documentan aquí solo como referencia/citación — no fueron realizados por mí. Los ítems que sí describen mi trabajo directo son los de **análisis de datos (7.0–7.9)**, **acceso y reproducibilidad (8.0–8.5)**, **resultados (9.0–10.3)** y **discusión (11.0–13.0)**. Presentar este checklist con esa distinción clara es, en sí mismo, parte de la buena práctica que STREAMS pide (Item 3.0: declarar si el estudio reutiliza datos previamente publicados).

---

## 1. Resumen (Abstract)

| Ítem | Descripción | Estado |
|---|---|---|
| 1.0 | Resumen general del estudio | ✅ En `README.md` del proyecto |
| 1.1 | Diseño del estudio | ✅ Reanálisis de datos públicos (declarado) |
| 1.2 | Ambiente y muestras | ✅ 67 pozos de agua subterránea, tabla de OTUs 16S rRNA V4 |
| 1.3 | Información del hospedero | N/A — no aplica (muestras ambientales, no asociadas a hospedero) |
| 1.4 | Análisis realizados | ✅ Diversidad alfa/beta, correlación ambiental |
| 1.5 | Resultado principal e importancia | ✅ Correlación con metales poco monitoreados (Al, Cd, K, Cu, Li, Na) |

## 2. Introducción

| Ítem | Descripción | Estado |
|---|---|---|
| 2.0 | Antecedentes y justificación | ✅ En README — conexión con monitoreo ambiental de acuíferos |
| 2.1 | Hipótesis/pregunta de investigación | ✅ Pregunta analítica explícita en README |

## 3–6. Métodos — muestreo, experimentales y de control (dataset original, no propio)

| Ítem | Descripción | Estado |
|---|---|---|
| 3.0 | Diseño del estudio (¿reutiliza datos?) | ✅ **Sí, declarado explícitamente** — dataset de Duvallet (2018), DOI 10.5281/zenodo.1455792 |
| 3.1–3.9 | Tipo de muestra, ubicación geográfica, fechas, ética/permisos, colecta | ⚠️ Pertenecen al estudio original (ENIGMA/LBNL) — no reportados aquí porque no fueron generados por mí. Ver cita original para el detalle. |
| 4.0–4.6 | Preservación, extracción de ácidos nucleicos, preparación de librerías, primers | ⚠️ Idem — parte del protocolo original del estudio ENIGMA, no de este reanálisis |
| 5.0–6.2 | Controles positivos/negativos, calidad, réplicas | ⚠️ Idem |
| 6.3–6.6 | Generación de datos ómicos (secuenciación) | ⚠️ Idem — plataforma y parámetros de secuenciación no reportados por mí |

## 7. Análisis de datos (mi contribución directa)

| Ítem | Descripción | Estado |
|---|---|---|
| 7.0 | Pasos bioinformáticos reportados | ✅ Notebook completo, 18 secciones documentadas paso a paso |
| 7.1 | Control de calidad de los datos de entrada | ✅ Documentado (nulos por variable, hasta 83.6% en `po4_mgl`) |
| 7.2 | Normalización | ✅ Dataset ya rarefaccionado a 10,000 lecturas/pozo (documentado en README) |
| 7.3 | Bases de datos de referencia (nombre, versión) | N/A — no se requirió asignación taxonómica adicional (tabla de OTUs ya generada) |
| 7.4 | Métodos estadísticos | ✅ Shannon, Simpson, Chao1 (fórmula y cita documentadas en el código), Bray-Curtis + PCoA (Gower 1966), correlación de Spearman |
| 7.5 | Datos faltantes | ✅ Documentado explícitamente en la sección de diagnóstico |
| 7.6 | Sesgos y variables de confusión | ✅ Discutido en limitaciones (PCoA explica solo 17.6% de varianza; ver nota sobre naturaleza composicional de los datos) |
| 7.7 | Subgrupos de análisis | N/A — no se formaron subgrupos |
| 7.8 | Análisis de sensibilidad | ⚠️ No realizado — área de mejora futura |
| 7.9 | Umbrales de significancia | ✅ Reportado en la sección de correlación de Spearman |

## 8. Acceso y reproducibilidad (mi contribución directa)

| Ítem | Descripción | Estado |
|---|---|---|
| 8.0 | Acceso a metadatos | ✅ `enigma.metadata.txt` incluido en el repositorio, con cita a la fuente |
| 8.2–8.3 | Datos crudos y procesados públicos | ✅ Incluidos en el repositorio + DOI de Zenodo del dataset original |
| 8.4 | Software, herramientas y código | ✅ `requirements.txt`, notebook completo, versiones de librerías documentadas |
| 8.5 | Reproducibilidad general | ✅ Notebook re-ejecutado de principio a fin sin errores; instrucciones de reproducción en el README |

## 9–10. Resultados

| Ítem | Descripción | Estado |
|---|---|---|
| 9.0 | Resultados del contexto ambiental/muestras | ✅ 67 pozos, variabilidad en diversidad alfa |
| 10.0 | Resultados de secuenciación | ✅ Riqueza, Shannon, Simpson, Chao1 por pozo (tabla y gráficos) |
| 10.2 | Resultados estadísticos | ✅ Correlaciones de Spearman con variables ambientales, PCoA con % de varianza explicada |
| 10.3 | Figuras y tablas | ✅ Gráficos de diversidad alfa/beta, tabla de correlaciones |

## 11–13. Discusión

| Ítem | Descripción | Estado |
|---|---|---|
| 11.0 | Resumen de resultados clave | ✅ En README y notebook (sección de conclusiones) |
| 11.1 | Interpretación en contexto | ✅ Comparación con variables clásicamente monitoreadas |
| 11.2 | Limitaciones | ✅ Documentadas (naturaleza composicional de los datos, PCoA con baja varianza explicada) |
| 11.3 | Generalización de resultados | ⚠️ Mencionado brevemente — se podría ampliar |
| 12.0 | Trabajo futuro | ✅ En README (ampliar panel de monitoreo ambiental) |
| 13.0 | Conclusiones | ✅ En notebook, sección final |

## 14–18. Otra información

| Ítem | Descripción | Estado |
|---|---|---|
| 16.0 | Información suplementaria (DOIs, datos) | ✅ DOI del dataset original citado en README |
| 17.0 | Acceso a todos los datos del estudio | ✅ Repositorio público en GitHub |
| 18.0 | Uso de IA | ✅ Ver nota de transparencia en el README maestro del portafolio |

---

## Qué falta para cumplimiento STREAMS completo (si se somete como manuscrito real)

1. Citar explícitamente el protocolo experimental original de ENIGMA/LBNL (secciones 3–6) en vez de solo el dataset — requiere ubicar la publicación primaria asociada al proyecto ENIGMA.
2. Análisis de sensibilidad (Item 7.8) — por ejemplo, repetir el análisis excluyendo variables con >50% de datos faltantes.
3. Discusión más extensa de generalización (Item 11.3) — ¿aplican estos hallazgos a otros acuíferos, o son específicos de esta red de pozos?

Este checklist se completó como ejercicio de rigor científico, no porque el proyecto vaya a someterse a publicación — pero deja documentado exactamente qué faltaría si esa decisión se tomara en el futuro.
