---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-21
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos reales ingestados (con contenido en wiki/) | 11 | = total sin falsos positivos |
| Falsos positivos acumulados (marcados `ingested:true`, sin contenido en wiki) | 7 | **0 nuevos** |
| Pendientes de ingesta | 39 | 0 |
| Páginas en wiki/ | 27 (10 topics, 3 entities, 11 summaries, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (parcial) | 2015-02-19 → hoy real |
| Ventanas GDELT en processed.json | 79 (37 trimestrales reales + 42 registros redundantes por bug — ver abajo) | ~46 (2015→hoy) |
| Días sin artículos nuevos en sources/ | **15** (último commit real: 2026-09-06) | máx 3 antes de diagnosticar — **ALARMA ACTIVA** |

---

## 🚨 Estado del Fetch (GitHub Actions) — FALLA CRÍTICA

```
Último commit exitoso a sources/  : 2026-09-06 (run #103, "6 artículos nuevos descargados")
Corridas consecutivas en FAILURE  : 14 (runs #104–#117, 2026-09-07 → 2026-09-21)
Duración de cada corrida fallida  : ~3 segundos
Evidencia                         : job "Fetch artículos → Commit a sources/" con
                                     runner_id=0 y runner_name="" — el job NUNCA
                                     llegó a ejecutar ningún paso (falla antes de
                                     actions/checkout)
Workflow                          : "active" (no deshabilitado); YAML sin cambios recientes
Logs del job                      : no disponibles vía API (HTTP 404) — consistente
                                     con job que nunca inició
Diagnóstico más probable          : cuota/minutos de GitHub Actions agotados para la
                                     cuenta abdielg08, o problema de facturación/billing
                                     que bloquea la asignación de runners
ACCIÓN REQUERIDA (usuario)        : revisar Settings → Billing and plans → Actions
                                     minutes (o Settings → Actions → General) en GitHub
```

**Nota secundaria (no bloqueante, se autoresuelve)**: `sources/processed.json._gdelt_windows`
acumuló 42 registros `"20260618_XXXXXXXX"` con el mismo inicio y fin creciente día a día,
en vez de una sola ventana trimestral. Causa: `fetch_gdelt_historical()` en
`scripts/fetch_news.py` recalcula `end = min(config_end, utcnow()-1d)` en cada corrida sin
persistir el cursor `current` entre ejecuciones. El bug se autoresuelve una vez que
"ayer" supera el límite de 90 días desde 2026-06-18 (~2026-09-16, ya alcanzado). Progreso
real del backfill trimestral: **37/~46 ventanas** (cobertura 2017-03 → 2026-06); faltan
~8 trimestres al inicio del rango (2015-02 → 2017-03). Ver `wiki/log.md` (2026-09-21 08:25)
para el detalle completo.

---

## Bug de scripts/ingest.py (documentado, no corregido esta sesión)

```
1. `mark-all-ingested --limit N` selecciona artículos por orden de archivo/fecha
   (find_pending), NO por los mismos artículos que `ingest --limit N` mostró en
   pending_ingest.md (que usa strategy=score). Puede marcar como "ingestados"
   artículos que Claude nunca procesó — incluyendo falsos positivos reales.
2. `mark-ingested '<url>'` (comando individual) falla siempre con
   AttributeError porque itera processed.items() incluyendo la clave
   `_gdelt_windows` (una lista, no un dict).
```
Ver `wiki/log.md` (2026-09-21 08:22) para el diagnóstico completo y la corrección manual
aplicada esta sesión (edición directa de `sources/processed.json`).

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas trimestrales completas | Estado |
|---------|----------------------------------|--------|
| 2015 Q1 – 2017 Q1 | 0/~8 | Pendiente (inicio del rango histórico) |
| 2017 Q2 – 2026 Q2 | 37/37 | Completado |
| 2026 Q3 (2026-06-18 → 2026-09-16) | 1/1 (bug de registros redundantes, ver arriba) | Completado (efectivamente) |
| **TOTAL trimestral real** | **~37-38 / ~46** | En progreso — bloqueado por falla de Actions |

> El backfill no puede avanzar mientras el fetch de GitHub Actions siga fallando
> (ver sección de arriba). Los artículos pendientes de ingesta (39) son el remanente
> del último lote descargado el 2026-09-06; no hay artículos nuevos desde entonces.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-21 | 5 (arroz: crisis 2025, inundaciones nov-2024, siembra 2022-2023, transición Linares, compensaciones Panamá Este/Darién) | 39 | 0 falsos positivos nuevos. Se detectó y corrigió bug de mark-all-ingested/mark-ingested. Se detectó falla crítica del fetch de GitHub Actions (14 días sin artículos nuevos) — requiere acción del usuario en GitHub Billing/Actions. |

---

## Instrucciones para la Routine

Al ejecutar, la routine DEBE:

1. Correr `python wiki_agro.py stats` y copiar los números aquí
2. Si ingestó artículos: actualizar la tabla "Historial de Sesiones"
3. Si pendientes = 0: actualizar "Estado del Fetch" con diagnóstico
4. Actualizar "last_updated" en el frontmatter
5. Si `Ventanas GDELT completadas` subió: actualizar tabla de Backfill
6. **Verificar con `git diff sources/processed.json` que los artículos marcados
   como `ingested: true` sean EXACTAMENTE los procesados en la sesión** — no confiar
   ciegamente en `mark-all-ingested` (ver bug documentado arriba)

**Señal de alarma**: si "Días sin artículos nuevos" llega a 3, la routine debe:
- Revisar el último log de GitHub Actions (ver wiki/log.md para contexto)
- Identificar si el problema es GDELT rate-limit, RSS caído, o config
- Documentar el diagnóstico en wiki/log.md con pasos para resolverlo

**Estado actual de la alarma (2026-09-21): ACTIVA desde hace 15 días.** Causa
identificada (falla de asignación de runners en GitHub Actions, ver arriba);
requiere que el usuario revise la cuota/facturación de GitHub Actions de su cuenta.
