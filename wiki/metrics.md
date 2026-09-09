---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-09
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos descargados en sources/ | 57 | ↑ continuo |
| Artículos ingestados | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 39 | **0** |
| Falsos positivos acumulados | 7 (previos a esta sesión) | **0 nuevos** |
| Páginas en wiki/ | 26 (9 topics, 3 entidades, 11 resúmenes, 2 overview + índice/log/métricas) | ↑ continuo |
| Cobertura temporal | 2015–2025 (artículos con fecha real) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 (`_gdelt_windows`) | ~45 estimadas (2015→hoy) — **ya superadas** |
| Días sin artículos nuevos en sources/ | 3 (última descarga: 2026-09-06) | máx 3 antes de diagnosticar — **umbral alcanzado hoy** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con commit  : 2026-09-06 13:56 UTC — "6 artículos nuevos descargados"
Historial reciente         : commits casi diarios desde 2026-08-14 (incluso con "0 artículos nuevos")
Resultado hoy (2026-09-09) : SIN commits nuevos en sources/ desde 2026-09-06 (3 días corridos)
Causa identificada         : No verificable desde esta sesión (sin acceso a logs de GitHub Actions).
                              El patrón de commits previos era casi diario, por lo que la ausencia total
                              de commits (ni siquiera "0 artículos nuevos") sugiere que el workflow dejó
                              de correr, más que un fetch que corrió y no encontró nada.
Ventanas GDELT              : 79 completadas, muy por encima de las ~45 estimadas para cubrir 2015→hoy.
                              Esto sugiere que el backfill histórico GDELT ya cubrió el rango objetivo
                              y que las fuentes activas ahora son mayormente RSS (IICA, La Prensa).
Acción recomendada          : Revisar directamente en GitHub → pestaña Actions si el workflow programado
                              se ejecutó y su resultado (éxito/fallo/no disparado) — no verificable desde
                              esta sesión de Claude Code.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Estado |
|---------|--------|
| 2015–2025 | Ventanas GDELT: **79/~45 estimadas — objetivo superado** |

> `_gdelt_windows` en `sources/processed.json` registra 79 ventanas ya completadas, por encima del
> estimado original de ~45 para cubrir 2015→hoy. La tabla detallada por trimestre de versiones
> anteriores de este archivo no pudo reconstruirse desde `processed.json` (no almacena rango de
> fechas por ventana, solo el identificador `YYYYMMDD_YYYYMMDD`); se sustituye por el conteo agregado
> hasta que el script exponga el desglose. El foco de progreso pendiente (39 artículos) es la
> **ingesta al wiki**, no el fetch de fuentes.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-09 | 5 (0 falsos positivos) | 39 | Routine automatizada; arroz/MIDA (importaciones, inundaciones, compensaciones, transición ministerial, proyección de siembra 2022-2023); detectado corte de 3 días en el fetch automático |

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
