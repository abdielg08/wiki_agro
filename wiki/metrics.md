---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-17
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos descargados (sources/) | 57 | ↑ continuo |
| Artículos ingestados (wiki/) | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 39 | 0 |
| Falsos positivos acumulados | 7 (previos) + posibles nuevos sin auditar en pendientes (ver nota) | **0 nuevos ingestados** |
| Páginas en wiki/ | 27 (10 topics, 3 entidades, 11 resúmenes) | ↑ continuo |
| Cobertura temporal | 2015-2025 (parcial, con huecos) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 (ver nota de calidad abajo) | 45-46 (2015→hoy) |
| Días sin artículos nuevos en sources/ | **11 días** (último commit: 2026-09-06) | máx 3 antes de diagnosticar — **UMBRAL SUPERADO** |

---

## Estado del Fetch (GitHub Actions) — ⚠️ FALLA DETECTADA 2026-09-17

```
Último commit a sources/ : 2026-09-06 13:56 UTC ("6 artículos nuevos descargados")
Hoy                        : 2026-09-17
Días sin nuevos artículos  : 11 (supera el umbral de 3 días de CLAUDE.md)
Diagnóstico                : GitHub Actions no ha vuelto a commitear a sources/ desde el 06-09.
                              No es un caso de "0 artículos nuevos" (que sí se commitea igual con
                              [skip ci]) — es AUSENCIA TOTAL de commits, lo que sugiere que el
                              workflow (.github/workflows/wiki_daily.yml o wiki_historical.yml)
                              dejó de ejecutarse o está fallando antes de llegar al paso de commit.
Acción recomendada         : Revisar manualmente el historial de ejecuciones de Actions en GitHub
                              (pestaña Actions del repo) para el workflow wiki_daily.yml — esta
                              sesión no tiene acceso a esa pestaña vía CLI/API disponible.

Calidad de las ventanas GDELT (_gdelt_windows en processed.json):
  - 79 ventanas registradas (por encima de las ~45-46 esperadas para cubrir 2015→hoy),
    pero el formato es inconsistente: hay ventanas trimestrales normales (ej. 20220922_20221221)
    mezcladas con decenas de ventanas de 1-2 días todas ancladas a 20260618_2026MMDD.
    Esto sugiere un posible bug en fetch_gdelt_historical() generando micro-ventanas en vez de
    trimestres al acercarse a la fecha actual, lo que podría estar inflando el conteo de
    "ventanas completadas" sin aportar cobertura histórica real.

Falsos positivos potenciales en sources/articles/ (pendientes, NO ingestados):
  - Se detectaron URLs en sources/processed.json claramente ajenas al agro panameño, ej.:
    thestar.com.my (MIDA = Malaysian Investment Development Authority, no el ministerio panameño),
    fox13now.com / sltrib.com (data centers en Utah), heraldo.es (política aragonesa, España),
    agenciabrasil.ebc.com.br (Brasil), clubofmozambique.com (Mozambique), whc.unesco.org, etc.
  - Causa probable: colisión de acrónimo "MIDA" y/o keywords genéricas de "agro"/"agricultura"
    sin filtro de país (country=PA) o de contexto panameño en el paso de descarga/relevancia.
  - Estos NO fueron ingestados en esta sesión. Deben marcarse como falso positivo (NO ingestar)
    cuando aparezcan en un futuro pending_ingest.md, y se recomienda ajustar el filtro de
    relevancia del fetcher para exigir mención explícita de Panamá.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | ? | Pendiente |
| 2016 Q1-Q4 | 0/4 | ? | Pendiente |
| 2017 Q1-Q4 | 0/4 | ? | Pendiente |
| 2018 Q1-Q4 | 0/4 | ? | Pendiente |
| 2019 Q1-Q4 | 0/4 | ? | Pendiente |
| 2020 Q1-Q4 | 0/4 | ? | Pendiente |
| 2021 Q1-Q4 | 0/4 | ? | Pendiente |
| 2022 Q1-Q4 | 0/4 | ? | Pendiente |
| 2023 Q1-Q4 | 0/4 | ? | Pendiente |
| 2024 Q1-Q4 | 0/4 | ? | Pendiente |
| 2025 Q1-Q4 | 0/4 | ? | Pendiente |
| 2026 Q1-Q2 | 0/2 | ? | Pendiente |
| **TOTAL** | **0/46** | **0** | **Backfill no iniciado** |

> Una vez que Actions corra con el código corregido, actualizar esta tabla con los datos reales.
> El rendimiento real de GDELT (artículos/trimestre) determinará la duración del backfill.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-17 | 5 (0 falsos positivos) | 39 | Ingesta de 5 artículos sobre arroz/MIDA. Diagnóstico: GitHub Actions sin commits a sources/ desde hace 11 días (umbral superado); posibles falsos positivos sin auditar en el resto de pendientes (colisión "MIDA" Malasia/Panamá) |

---

## Instrucciones para la Routine

Al ejecutar, la routine DEBE:

1. Correr `python wiki_agro.py stats` y copiar los números aquí
2. Si ingestó artículos: actualizar la tabla "Historial de Sesiones"
3. Si pendientes = 0: actualizar "Estado del Fetch" con diagnóstico
4. Actualizar "last_updated" en el frontmatter
5. Si `Ventanas GDELT completadas` subió: actualizar tabla de Backfill

**Señal de alarma**: si "Días sin artículos nuevos" llega a 3, la routine debe:
- Revisar el último log de GitHub Actions (ver wiki/log.md para contexto)
- Identificar si el problema es GDELT rate-limit, RSS caído, o config
- Documentar el diagnóstico en wiki/log.md con pasos para resolverlo
