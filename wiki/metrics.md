---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-11
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
| Falsos positivos acumulados | 7 | **0 nuevos** |
| Páginas en wiki/ | 25 (8 topics, 3 entidades, 11 summaries) | ↑ continuo |
| Cobertura temporal | 2015-2026 | 2015 → hoy real |
| Ventanas GDELT completadas | 79 / ~46 estimadas originalmente | rango agotado con el estimado original — necesita expansión (ver abajo) |
| Días sin artículos nuevos (sources/) | 5 (último commit: 2026-09-06) | máx 3 antes de diagnosticar — **ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions EXITOSA : 2026-09-06 13:56 UTC (run #103) — 6 artículos nuevos descargados
Corridas fallidas consecutivas : 2026-09-07, 09-08, 09-09, 09-10 (runs #104-#107) — 4 días seguidos
Patrón de falla                : las 4 corridas fallidas completaron en ~4 segundos cada una
                                  (demasiado rápido para ser timeout de GDELT o rate-limit de red;
                                  apunta a una falla temprana en el job — checkout/setup/permisos)
Logs                            : no disponibles vía API (HTTP 404 — logs expirados/purgados)
Causa raíz                     : NO CONFIRMADA — requiere revisión manual en
                                  https://github.com/abdielg08/wiki_agro/actions/workflows/wiki_daily.yml
Próxima corrida programada     : 2026-09-11 11:00 UTC (cron diario "0 11 * * *")
Ventanas GDELT                 : 79 completadas — por encima del estimado original de ~45/46,
                                  lo que según CLAUDE.md indica rango de fechas agotado y necesita
                                  expansión de la tabla de backfill (ver sección siguiente)
```

---

## Progreso del Backfill GDELT (2015 → hoy)

> **Nota 2026-09-11**: `sources/processed.json._gdelt_windows` reporta **79 ventanas** completadas,
> más del doble del estimado original (~45/46). El detalle por período/trimestre no está disponible
> en processed.json (solo se guarda la lista plana de ventanas, sin desglose por año); la tabla de
> abajo queda como referencia histórica del estimado original y debe reconstruirse con un script que
> cruce `_gdelt_windows` contra trimestres reales antes de confiar en ella. 57 artículos descargados
> en total hasta la fecha (todas las fuentes), 51 de ellos vía prensa.com.

| Período | Ventanas (estimado original) | Estado |
|---------|-------------------------------|--------|
| 2015–2026 | 79 ventanas completadas (vs. ~46 estimadas) | **Estimado original agotado — recalcular tabla por trimestre** |

> Acción pendiente para una próxima sesión: escribir un script que derive cobertura real
> por trimestre a partir de `_gdelt_windows` (formato `YYYYMMDD_YYYYMMDD`) para reemplazar
> esta tabla con datos verificables en vez de estimados.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-11 | 5 | 39 | Routine automática; 0 falsos positivos; detectadas 4 corridas de Actions fallidas consecutivas (09-07 a 09-10) |

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
