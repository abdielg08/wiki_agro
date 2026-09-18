---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-18
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 39 | 0 |
| Falsos positivos acumulados (detectados, no ingestados) | ~7 (semilla) + ~15 nuevos detectados en pool 2026-09-18 (ver log) | **0 ingestados** |
| Páginas en wiki/ | 25 (8 topics, 3 entities, 11 summaries, ~3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2025 (artículos reales, vía GDELT + prensa.com) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 / ~45 estimadas | 45 (2015→hoy) — **umbral superado, backfill agotado** |
| Días sin artículos nuevos en sources/ | **12** (último commit real: 2026-09-06) | máx 3 antes de diagnosticar → **⚠ ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con commit real     : 2026-09-06 (6 artículos nuevos) [sha 24cfc3c]
Corridas desde entonces            : 10 corridas diarias consecutivas (2026-09-09 → 2026-09-18)
Resultado de las 10 corridas       : conclusion=failure, ~3-4 seg de duración, 0 ms billable
Causa identificada (2026-09-18)    : GitHub Actions NO asigna runner al job (runner_id=0,
                                      runner_name=""). El job muere antes del primer step
                                      (checkout). No es un fallo de GDELT/RSS/código —
                                      es un problema de infraestructura/cuenta:
                                      minutos de Actions agotados, spending limit alcanzado,
                                      o Actions deshabilitado/pausado en el repo.
Verificación de logs crudos        : bloqueada — el proxy de red de esta sesión no permite
                                      egress a productionresultssa0.blob.core.windows.net
Acción requerida (fuera de Claude) : el usuario debe revisar GitHub Settings → Billing/Plans
                                      and usage → Actions (spending limit / minutos disponibles)
                                      y confirmar que Actions esté habilitado para
                                      abdielg08/wiki_agro.
Estado GDELT (independiente)       : 79 ventanas completadas, por encima del umbral de 45 —
                                      backfill histórico por GDELT agotado; expansión de rango
                                      necesaria cuando el fetch vuelva a correr.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

**Ventanas GDELT completadas (`_gdelt_windows` en `sources/processed.json`): 79.**
Esto supera el umbral de 45 definido en CLAUDE.md como señal de que "el rango de fechas está
agotado (necesita expansión)". La tabla trimestral detallada de abajo quedó desactualizada
desde la auditoría de 2026-06-22 (marcaba 0/46) y no refleja las 79 ventanas reales — no se
reconstruye aquí trimestre a trimestre porque `processed.json` no expone el detalle por
trimestre, solo el conteo agregado. **Próxima acción cuando el fetch se restablezca**: expandir
el rango de ventanas GDELT más allá del histórico ya cubierto, o confirmar cobertura real
2015-2025 con un script que desglose `_gdelt_windows` por fecha.

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015–2025 (agregado) | 79 completadas | 57 en sources/ | Umbral 45 superado — backfill GDELT agotado |

> Una vez que Actions vuelva a correr, recalcular esta tabla por trimestre real a partir de
> `_gdelt_windows` y decidir si expandir el rango o cambiar de fuente (RSS adicionales).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-18 | 5 (arroz, transición MIDA, lluvias Veraguas) | 39 | 0 falsos positivos ingestados; detectado fetch de Actions caído 12 días (ver Estado del Fetch) |

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
