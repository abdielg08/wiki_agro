---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-15
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 21 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 15 | **0 nuevos en el wiki** (15/15 descartados antes de crear páginas) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2017-03-30 → 2026-07-09 (GDELT) + semilla 2015-2024 | 2015 → hoy real |
| Ventanas GDELT completadas | 48 / 47 esperadas | 47 (2015→hoy) — **gap: faltan 9 ventanas de 2015-01-01 a 2017-03-29** |
| Días sin artículos nuevos | 1 (última corrida Actions: 2026-07-14) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-14 (1 artículo nuevo descargado)
Días sin artículos     : 1 — dentro de rango normal (umbral de alarma: 3)

Hallazgo 2026-07-15    : 8/8 artículos pendientes de la búsqueda DDG
                         "prensa_agro" resultaron ser falsos positivos
                         (dominios ajenos a Panamá: paultan.org, sltrib.com,
                         whc.unesco.org, nyfb.org, spa.gov.sa) — ver
                         wiki/log.md para el detalle completo.
Causa raíz             : fetch_ddg_search() en scripts/fetch_news.py no
                         aplicaba los filtros _is_panama_related() /
                         _is_blocked_domain() que sí tienen fetch_rss() y
                         fetch_gdelt_batch(). El acrónimo "MIDA" en la query
                         también nombra entidades de Malasia y Utah, y el
                         operador site: de DDG no se respeta estrictamente.
Fix aplicado           : se agregaron los mismos filtros a fetch_ddg_search()
                         (commit de esta sesión). Deberá validarse que la
                         próxima corrida diaria ya no traiga estos falsos
                         positivos.
Bug secundario         : mark_ingested() en scripts/ingest.py fallaba con
                         AttributeError al iterar processed.items() sin
                         filtrar la clave interna "_gdelt_windows" (lista,
                         no dict). Corregido para usar article_entries().

Gap de backfill        : faltan 9 ventanas GDELT trimestrales cubriendo
                         2015-01-01 → 2017-03-29 (ver detalle en log.md).
                         No se pudo diagnosticar la causa exacta desde el
                         sandbox de Claude Code (sin salida de red a
                         api.gdeltproject.org). Revisar logs de Actions o
                         disparar wiki_historical.yml (years=2015-2017,
                         mode=gdelt) si el fetch diario sigue sin poder
                         completarlas.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015-01-01 → 2017-03-29 (9 ventanas trimestrales) | 0/9 | **Pendiente — gap identificado 2026-07-15** |
| 2017-03-30 → 2025-12-31 (36 ventanas trimestrales) | 36/36 | Completo |
| 2026-01-01 → 2026-07-09 (3 ventanas trimestrales) | 3/3 | Completo (hasta la fecha) |
| **TOTAL** | **39/48 ventanas fijas + 9 pendientes = 48/47 esperadas** | **Gap 2015-2017 sin resolver** |

> Conteo real leído de `sources/processed.json._gdelt_windows` el 2026-07-15.
> El número de ventanas ya no coincide exactamente con calendario Q1-Q4 porque
> las ventanas son bloques fijos de 90 días desde `2015-01-01`, no trimestres
> calendario — por eso el conteo de 2026 no es "Q1-Q2" limpio.
> Ver `wiki/log.md` (entrada 2026-07-15) para el diagnóstico del gap de 2015-2017.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-15 | 0 (8 revisados, 8 falsos positivos) | 0 | Fix de fetch_ddg_search() (filtro Panamá faltante) + fix de mark_ingested() (bug `_gdelt_windows`) + diagnóstico de gap 2015-2017 en backfill GDELT |

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
