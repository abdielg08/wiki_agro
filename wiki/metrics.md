---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-08
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 19 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 13 | **0 nuevos** |
| Pendientes de ingesta | 0 | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 45 | backfill alcanzó el presente |
| Días consecutivos sin artículos nuevos | 5 (2026-07-03 → 07-07) | máx 3 antes de diagnosticar — **SUPERADO** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-07 (run #42) — status: success
Resultado              : 0 artículos nuevos (5 días consecutivos: 07-03 a 07-07)
Causa identificada     : 1) GDELT: 45 ventanas completadas → backfill histórico alcanzó
                            el presente, ya no hay ventanas trimestrales nuevas hasta que
                            pase más tiempo real (self-limiting, no es un error).
                         2) RSS IICA y La Prensa devolvieron 0 entradas relevantes esos días.
                         3) La búsqueda DDG (única fuente aún activa) traía 100% falsos
                            positivos (13/13 artículos con source="prensa.com" NO eran de
                            Panamá — ver wiki/log.md 2026-07-08) por falta de filtro de
                            dominio/Panamá en fetch_ddg_search().
Fix aplicado 2026-07-08 : fetch_ddg_search() ahora exige que el dominio del resultado
                            coincida con el `site:` configurado y, para fuentes
                            internacionales, que el título/URL mencione Panamá.
                            mark_ingested() corregido (crasheaba con _gdelt_windows).
Estado post-fix         : Pendiente validación — probablemente 0 artículos/día de DDG hasta
                            ampliar queries o agregar fuentes RSS activas (IICA/La Prensa
                            son las únicas RSS funcionando).
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 Q1-Q4 | 0/4 | **Vacío — GAP no explicado** |
| 2016 Q1-Q4 | 0/4 | **Vacío — GAP no explicado** |
| 2017 Q1-Q4 | 3/4 | Falta Q1 (arranca en 2017-03-30) |
| 2018 Q1-Q4 | 4/4 | Completo |
| 2019 Q1-Q4 | 4/4 | Completo |
| 2020 Q1-Q4 | 4/4 | Completo |
| 2021 Q1-Q4 | 4/4 | Completo |
| 2022 Q1-Q4 | 4/4 | Completo |
| 2023 Q1-Q4 | 4/4 | Completo |
| 2024 Q1-Q4 | 4/4 | Completo |
| 2025 Q1-Q4 | 4/4 | Completo |
| 2026 Q1-Q2 | 2/2 | Completo |
| 2026 H2 (parcial) | 8 entradas redundantes | Ver nota "redundancia" abajo |
| **TOTAL** | **45 ventanas** | **Backfill llegó al presente, salvo gap 2015–2017Q1** |

> **GAP 2015-01-01 → 2017-03-29 (~2 años y 3 meses)**: `_gdelt_windows` no tiene ninguna
> ventana en ese rango pese a que `config/sources.yaml` fija `gdelt.date_range.start: 2015-01-01`.
> No se pudo determinar la causa exacta en esta sesión (sin acceso de red al sandbox para
> reproducir `fetch --mode gdelt`). Pendiente de investigar en una sesión con acceso a
> GDELT: correr `python wiki_agro.py fetch --mode gdelt --limit 0` y observar si las
> ventanas 2015–2017Q1 se marcan completas o siguen fallando silenciosamente.
>
> **Redundancia cerca del presente**: las 8 entradas `20260618_2026MMDD` en `_gdelt_windows`
> comparten el mismo inicio (2026-06-18) con fin creciente día a día — indica que
> `fetch_gdelt_historical()` re-consulta el mismo rango parcial cada día en vez de avanzar
> el inicio de forma incremental, porque `end` se recalcula como `hoy - 1` en cada corrida
> y nunca alcanza los 90 días completos para cerrar la ventana. No causa falsos positivos
> ni duplicados (se deduplica por URL), solo gasto redundante de cuota de la API GDELT.
> No se corrigió en esta sesión por falta de acceso de red para validar el fix con seguridad.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-08 | 0 | 0 | 6 falsos positivos nuevos rechazados (100% de la fuente DDG prensa_agro) + fix de `fetch_ddg_search()` (filtro dominio/Panamá) + fix de `mark_ingested()` (crash con `_gdelt_windows`) + diagnóstico de gap GDELT 2015–2017Q1 + redundancia de ventanas cerca del presente |

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
