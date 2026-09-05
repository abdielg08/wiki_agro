---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-05
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 51 | ↑ continuo |
| Artículos ingestados (processed.json) | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 33 | 0 |
| Falsos positivos acumulados | 8 (7 previos + 1 el 2026-09-05: MITI/MARii Malasia) | **0 nuevos reales ingestados como si fueran agro** |
| Páginas en wiki/ | 24 (8 topics, 3 entities, 10 summaries, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + ingesta real) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 | 45+ (2015→hoy) — meta original ya superada |
| Días sin artículos nuevos reales | 8 (desde 2026-08-27) | máx 3 antes de diagnosticar — **ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions       : 2026-09-04 (commit bcc74c2, "0 artículos nuevos descargados")
Historial reciente           : 2026-08-27 (+1), 2026-09-01 (0), 2026-09-03 (0), 2026-09-04 (0)
Días sin artículos nuevos    : 8 (desde 2026-08-27) — supera umbral de alarma (3 días)
Ventanas GDELT completadas   : 79 (ya superó la meta original de ~45 → rango 2015-hoy
                                probablemente ya cubierto o en re-procesamiento sin resultados nuevos)
Causa probable              : (1) agotamiento del rango de fechas útil en GDELT, o
                               (2) RSS de IICA/La Prensa sin entradas nuevas relevantes, o
                               (3) el filtro de keywords "MIDA"/"agro" está trayendo ruido
                               internacional (Malasia MIDA/MITI, data centers, IEEE, etc. —
                               ver wiki/log.md 2026-09-05) en vez de artículos panameños válidos
Diagnóstico completo         : ver wiki/log.md, entrada 2026-09-05 00:15
Estado                       : sin resolver — requiere revisión de fetch_gdelt / filtros de fuente
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| **TOTAL** | **79 ventanas completadas** | **51 descargados / 18 ingestados** | **En curso — ritmo de artículos nuevos muy bajo desde 2026-08-27** |

> El contador `_gdelt_windows` en `sources/processed.json` marca 79 ventanas completadas, por encima
> de la estimación original de ~45 para cubrir 2015→hoy. No hay desglose por trimestre disponible en
> este momento porque `processed.json` solo guarda el contador agregado, no el detalle por ventana.
> El estancamiento en artículos nuevos (8 días sin ingreso real) pese a que las ventanas GDELT siguen
> "completándose" sugiere que el backfill está reprocesando rangos ya cubiertos sin encontrar
> contenido adicional, o que el filtro de relevancia está descartando/mezclando resultados no
> panameños (ver "Estado del Fetch" arriba). Requiere revisión del script de fetch para desglosar
> el progreso real por período.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-05 | 4 (1 falso positivo excluido) | 33 | Routine automática; detectado falso positivo Malasia MIDA/MITI; alarma por 8 días sin artículos nuevos reales |

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
