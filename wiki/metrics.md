---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-10
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
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 47 total (37 backfill trimestral + 10 fetch diario) | ver detalle abajo — 2015-2016 sin crawlear |
| Días sin artículos nuevos (reales) | 8+ (desde 2026-07-02) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-09 (corrió; commits "0 artículos nuevos" 07-03/04/08/09)
Resultado              : 0 artículos REALES desde 2026-07-02 (8 días)
Causa identificada     : (1) El backfill histórico (2017-03-30→2026-06-17, 37/37 ventanas)
                             ya no aporta artículos nuevos por rango — pero 2015-2016 nunca
                             se crawleó (ver tabla de Backfill abajo), así que SÍ queda
                             historia real por recuperar, solo que el fetch diario no la toca.
                         (2) RSS IICA/La Prensa: 0 entradas relevantes en corridas recientes.
                         (3) Búsqueda DDG (config/sources.yaml: web_searches) era la única
                             fuente activa, pero fetch_ddg_search() no verificaba dominio real
                             del resultado ni aplicaba _is_panama_related() → devolvió 6 falsos
                             positivos de EE.UU./Arabia Saudita etiquetados como "prensa.com"/PA
                             en vez de artículos reales (ver wiki/log.md 2026-07-10).
Fix aplicado            : fetch_ddg_search() ahora descarta resultados fuera del dominio
                          buscado y aplica _is_blocked_domain()/_is_panama_related() (salvo
                          dominios .gob.pa). mark_ingested() corregido (crasheaba con
                          _gdelt_windows).
Estado post-fix         : Pendiente validación en próxima corrida Actions (2026-07-11 ~06:00
                          hora Panamá). Acción recomendada de mayor impacto: correr
                          `wiki_historical.yml` manualmente para el rango 2015-02-19 →
                          2017-03-29 (2015-2016 nunca crawleado — ver tabla de Backfill).
                          Si el fetch diario sigue sin artículos reales tras el fix de DDG,
                          revisar por qué IICA/La Prensa RSS no arrojan entradas.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

> Recalculado el 2026-07-10 a partir de `sources/processed.json:_gdelt_windows` (47 entradas
> reales). La tabla anterior (`0/46`) estaba desactualizada — nunca se sincronizó con las
> corridas reales de Actions.

| Período | Ventanas (90 días) | Estado |
|---------|--------------------|--------|
| **2015 Q1-Q4** | **0/4** | **⚠ NUNCA CRAWLEADO** |
| **2016 Q1-Q4** | **0/4** | **⚠ NUNCA CRAWLEADO** |
| 2017-03-30 → 2026-06-17 | 37/37 | Completo (continuo, sin huecos) |
| **TOTAL histórico trimestral** | **37/45** | **2015–2017-03-29 pendiente (~8 ventanas)** |

**Hallazgo importante**: el crawler histórico (`fetch_historical.py`) arrancó en 2017-03-30,
NO en 2015-02-19 como indica el objetivo de cobertura de CLAUDE.md. Los ~2 años de 2015–2016
nunca se han crawleado. Se recomienda correr `wiki_historical.yml` (workflow_dispatch) con un
rango explícito 2015-02-19 → 2017-03-29 para cerrar el hueco.

Las otras 10 entradas de `_gdelt_windows` (`20260618_2026MMDD...`) NO son parte del backfill
trimestral — son ventanas incrementales del fetch **diario** (`wiki_daily.yml`, modo `all`),
que usa un inicio fijo (2026-06-18) y extiende el final cada día. Esto infla el conteo total
de "ventanas completadas" (47) y hace que el heurístico de CLAUDE.md ("45+ ventanas → rango
agotado") dé un falso positivo: el histórico real solo tiene 37/45 ventanas trimestrales, no
está agotado — simplemente nunca cubrió 2015–2016.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-10 | 0 (6 falsos positivos descartados) | 0 | Fix bug fetch_ddg_search (sin filtro de dominio/Panamá) + fix mark_ingested crash. Hallazgo: backfill 2015-2016 nunca corrió (37/45 ventanas trimestrales, no 47/46 como parecía) |

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
