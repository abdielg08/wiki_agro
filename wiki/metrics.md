---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-01
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 | **0 nuevos ingestados** (16 detectados y bloqueados hoy) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 60 (2015-2016: 0; 2017-2026: 60) | ver nota — falta backfill 2015-2016 |
| Días sin artículos nuevos | 1 (última corrida 07-31, 0 nuevos) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions      : 2026-07-31 — 0 artículos nuevos
Última corrida con contenido: 2026-07-30 — 3 artículos nuevos
Ventanas GDELT              : 60 completadas, pero desbalanceadas: 2015-2016
                               tienen 0 ventanas (backfill nunca llegó al
                               inicio de la cobertura objetivo), mientras
                               2017-2026 están completos/sobre-cubiertos.
                               Ver tabla "Progreso del Backfill GDELT" abajo
                               — acción sugerida: priorizar 2015-2016 en la
                               próxima corrida histórica.

CAUSA RAÍZ DE FALSOS POSITIVOS (encontrada y corregida 2026-08-01):
  Los 23 artículos con fuente "prensa.com" NO venían del RSS real de La
  Prensa — venían de fetch_ddg_search() (búsqueda DuckDuckGo "prensa_agro",
  config/sources.yaml). El operador `site:prensa.com` de DDG News no se
  respetaba de forma confiable y el resultado se etiquetaba como
  "prensa.com" sin verificar el dominio real. De los 23, los 16 que
  estaban pendientes se revisaron uno por uno en esta sesión y el 100% eran
  de dominios ajenos (sltrib.com, paultan.org, heraldo.es, nyfb.org, spa.gov.sa,
  agenciabrasil.ebc.com.br, whc.unesco.org, ieeexplore.ieee.org, archive.org,
  msn.com) — ninguno sobre agro de Panamá.
Fix aplicado : scripts/fetch_news.py::fetch_ddg_search ahora verifica que el
               dominio real de la URL devuelta coincida con `site` antes de
               aceptarla.
Bug adicional: scripts/ingest.py — mark_ingested() crasheaba siempre
               (iteraba sobre _gdelt_windows como si fuera dict de artículo);
               mark_all_ingested() marcaba artículos distintos a los
               mostrados en pending_ingest.md (criterios de orden distintos
               entre `ingest` y `mark-all-ingested`). Ambos corregidos.
Estado post-fix: pendiente validación en la próxima corrida real de Actions
                 y en la próxima sesión de ingesta (ver wiki/log.md 08:15-08:30).
```

---

## Progreso del Backfill GDELT (2015 → hoy)

Recalculado el 2026-08-01 desde `_gdelt_windows` en `sources/processed.json`
(60 ventanas registradas, formato `YYYYMMDD_YYYYMMDD`, conteo por año de inicio):

| Año | Ventanas completadas | Estado |
|-----|----------------------|--------|
| 2015 | 0 | **Pendiente — sin empezar** |
| 2016 | 0 | **Pendiente — sin empezar** |
| 2017 | 4 | Completo |
| 2018 | 4 | Completo |
| 2019 | 4 | Completo |
| 2020 | 4 | Completo |
| 2021 | 4 | Completo |
| 2022 | 4 | Completo |
| 2023 | 4 | Completo |
| 2024 | 4 | Completo |
| 2025 | 4 | Completo |
| 2026 | 24 | Completo (sobre-representado, ventanas más finas cerca de hoy) |
| **TOTAL** | **60** | — |

> **Corrección del diagnóstico automático**: el umbral simple de "45+
> ventanas = rango agotado" (CLAUDE.md Paso 4) es engañoso aquí — el total
> es alto pero está muy desbalanceado. **2015 y 2016 tienen 0 ventanas
> completadas**, es decir el inicio real de la cobertura objetivo
> (2015-02-19) nunca se ha procesado. La "expansión necesaria" no es hacia
> adelante (2026 ya está sobre-cubierto) sino hacia atrás: priorizar el
> backfill de 2015-2016 en la próxima corrida (`fetch-historical --years
> 2015-2016` o equivalente).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-01 | 0 | 0 | 16 artículos revisados, 16 falsos positivos (0% ingestados al wiki, correcto: ninguno era agro-Panamá). Causa raíz encontrada y corregida (filtro de dominio roto en DDG "prensa_agro"). 2 bugs de `mark-ingested`/`mark-all-ingested` corregidos. Gap de backfill 2015-2016 detectado. |

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
