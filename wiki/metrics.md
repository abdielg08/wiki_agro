---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-22
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 30 | ↑ continuo |
| Artículos reales ingestados | 13 | = total sin falsos positivos |
| Falsos positivos acumulados | 28 (7 previos + 21 esta sesión) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal real | 2017-03 → hoy (parcial) | 2015-02-19 → hoy |
| Ventanas GDELT completadas | 72 | cobertura 2015→hoy |
| Días sin artículos nuevos | **3** (2026-08-20, 08-21, 08-22 en 0; último real: 08-19) | ⚠️ máx 3 antes de diagnosticar — **UMBRAL ALCANZADO** |

---

## ⚠️ Señal de alarma activa (2026-08-22)

`Días sin artículos nuevos` llegó a 3. Diagnóstico ejecutado — ver detalle abajo y en `wiki/log.md`.

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-21 (corre diario, 11:24 UTC — a tiempo)
Resultado               : 0 artículos nuevos (patrón: 0 en la mayoría de días,
                          ocasional 1-3; sin corrida de hoy 08-22 aún al momento
                          de esta sesión)
Causa identificada      : (1) La cola de ingesta pendiente estaba 100% contaminada
                          por un bug real en fetch_ddg_search() (ver detalle abajo) —
                          21/21 artículos revisados en esta sesión eran falsos
                          positivos, ninguno sobre agro panameño.
                          (2) El backfill histórico (wiki_historical.yml) NUNCA se ha
                          ejecutado para 2015-02-19 → 2017-03-29 — hueco real de
                          ~2 años en la cobertura declarada como objetivo.
                          (3) Este entorno de sesión (Claude Code cloud) tiene la
                          API de GDELT bloqueada por su proxy saliente (403 en el
                          túnel) — GitHub Actions sí tiene acceso (ventanas GDELT
                          avanzan a diario), así que el fetch diario de GDELT no
                          está bloqueado en producción, solo aquí.
Fix aplicado esta sesión : fetch_ddg_search() ahora descarta resultados de DDG cuyo
                          dominio real no coincide con el `site:` consultado —
                          bloqueará los falsos positivos tipo "MIDA" (homónimos:
                          Malaysia MIDA, Utah Military Installation Development
                          Authority) y artículos de otros países que colaban por
                          match de substring genérico.
                          mark_all_ingested() e mark_ingested() en scripts/ingest.py
                          tenían bugs de selección/filtrado — corregidos (ver log.md
                          2026-08-22 08:30 para detalle completo).
Acción recomendada      : Disparar manualmente el workflow `wiki_historical.yml`
                          (workflow_dispatch) con years="2015-2017" mode="gdelt"
                          para cerrar el hueco de cobertura 2015-02-19→2017-03-29.
                          No se disparó desde esta sesión (corre hasta 6h y hace
                          push directo a main fuera del flujo de PR de esta sesión) —
                          requiere confirmación humana.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015-02-19 → 2017-03-29 | 0 | **Nunca ejecutado — hueco real de cobertura** |
| 2017-03-30 → 2026-06-17 | ~68 (trimestrales) | Completado |
| 2026-06-18 → hoy | ~4 (incrementales diarias) | En progreso (fetch diario) |
| **TOTAL** | **72** | **Backfill histórico incompleto — falta 2015-2017** |

> Fuente: `sources/processed.json` → `_gdelt_windows` (72 ventanas, la más antigua
> inicia en 2017-03-30). El objetivo declarado en CLAUDE.md es 2015-02-19 → hoy;
> ese arranque nunca se cubrió. Ejecutar `wiki_historical.yml` con years=2015-2017
> para cerrarlo.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-22 | 0 (21/21 revisados = falsos positivos) | 0 | Cola completa contaminada por bug de dominio en DDG search (corregido). 2 bugs adicionales corregidos en ingest.py (selección de mark-all-ingested y filtrado de claves internas). Hueco de cobertura 2015-2017 identificado. |

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

**Pendiente de seguimiento (próxima sesión)**:
- Validar que el fix de `fetch_ddg_search()` (dominio real vs. `site:` consultado)
  efectivamente reduce los falsos positivos en la próxima corrida de `fetch --mode all`.
- Confirmar con el usuario si se debe disparar `wiki_historical.yml` para
  years=2015-2017 (hueco de cobertura real, ver arriba).
