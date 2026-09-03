---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-03
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 51 | ↑ continuo |
| Artículos ingestados (marcados) | 18 (10 con página real + 8 falsos positivos marcados) | = total sin falsos positivos |
| Falsos positivos acumulados | 8 | **0 nuevos** |
| Páginas en wiki/ | 25 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + ingesta parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 77 / ~45-46 estimadas | 45 (2015→hoy) — meta ya superada en número, cobertura real sin confirmar |
| Días sin artículos nuevos | **7** (último real: 2026-08-27) | máx 3 antes de diagnosticar — **⚠ ALARMA ACTIVA** |
| Pendientes de ingesta | 33 | 0 |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions       : 2026-09-02 (run #99) — status: success
Resultado                    : 0 artículos nuevos
Última corrida con artículos : 2026-08-27 (run #93) — 1 artículo nuevo
Corridas recientes           : #98 (2026-09-01, success, 1 nuevo — commit previo)
                                #99 (2026-09-02, success, 0 nuevos)
                                #94-#97 (2026-08-28 a 2026-08-31): fallaron (`failure`),
                                pero no bloquearon el fetch — se recuperó el 2026-09-01
Causa del estancamiento       : Actions SÍ corre y SÍ tiene éxito, pero no encuentra
                                artículos nuevos que descargar la mayoría de los días.
Hipótesis principal           : las 77 ventanas GDELT completadas (vs. ~45-46 estimadas
                                para cubrir 2015→hoy) sugieren que fetch_gdelt_historical()
                                re-registra ventanas ya cubiertas en vez de avanzar el
                                backfill histórico real — requiere revisión de código
                                (no se modificó scripts/ en esta sesión).
Fuentes RSS                   : IICA y La Prensa (únicas activas por CLAUDE.md) — su
                                rendimiento no se validó directamente en esta sesión.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015-2016 | ? | ? | Sin datos desglosados por año — pendiente de auditoría del contenido de `_gdelt_windows` |
| 2017-2025 | ? | ? | Sin datos desglosados por año — pendiente de auditoría del contenido de `_gdelt_windows` |
| **TOTAL** | **77 ventanas completadas** | **51 artículos descargados** | Ventanas superan la meta original (~45-46), pero cobertura histórica real (2015-2016 en particular) no confirmada — ver diagnóstico arriba |

> Sesiones previas (PRs #235-#244, no fusionados) reportaron un hueco real en 2015-2016
> (0/8 ventanas) pese al alto conteo total. Esta sesión no tuvo egress a
> `api.gdeltproject.org` para verificarlo directamente contra la red real; confirmar en
> una sesión con acceso a GDELT o revisando `sources/processed.json._gdelt_windows`
> localmente.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-03 | 4 reales + 1 falso positivo marcado | 33 | Rutina programada — ver `wiki/log.md` para diagnóstico completo, incluyendo hallazgo de 10 PRs previos sin fusionar (#235-#244) que reprocesan el mismo backlog |

---

## ⚠ Hallazgo Operativo: PRs sin Fusionar

10 pull requests (#235–#244), generados por sesiones de routine entre 2026-08-30 y
2026-09-02, permanecen abiertos en modo draft sin fusionar a `main`. Cada uno reprocesa
el mismo lote de 5 artículos pendientes porque parte de `main` sin ver el trabajo de
sesiones anteriores. Mientras estos PRs no se fusionen (o se descarten los duplicados),
`main` seguirá mostrando el mismo backlog (33 pendientes) sesión tras sesión, aunque el
trabajo de ingesta ya se haya hecho repetidamente en ramas no fusionadas. Ver detalle en
`wiki/log.md` (entrada 2026-09-03).

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
