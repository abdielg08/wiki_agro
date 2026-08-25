---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-25
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 50 | ↑ continuo |
| Artículos reales ingestados | 10 (resúmenes en wiki/) | = total sin falsos positivos |
| Falsos positivos acumulados | 8 | **0 nuevos** |
| Páginas en wiki/ | 25 (9 topics, 3 entidades, 10 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (backfill parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 74 / ~46 estimadas | 45 (2015→hoy) — **rango agotado, requiere expansión** |
| Días sin artículos nuevos | 1 (último fetch: 2026-08-24) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-24 (20 artículos nuevos descargados)
Cadencia observada      : ~1 corrida/día (no 3x/día como asume CLAUDE.md);
                          irregular, con días sin commit (ej. 2026-08-23)
Ventanas GDELT          : 74 completadas — supera el estimado original de ~45-46
                          ventanas para cubrir 2015→hoy. El rango original parece agotado.
Diagnóstico             : el backfill sigue trayendo artículos nuevos (20 el 2026-08-24),
                          por lo que no está bloqueado, pero el conteo de ventanas (74)
                          sugiere que necesita expandirse más allá del rango 2015-2026
                          original o que hay reintentos/duplicados en el conteo.
                          Revisar scripts/fetch.py para confirmar el mecanismo de
                          expansión de ventanas GDELT.
Pendientes tras sesión  : 32 (se procesaron 5: 4 ingestados + 1 falso positivo)
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| **TOTAL** | **74/~46 estimadas** | **50 en sources/** | **En progreso — rango original superado** |

> `processed.json._gdelt_windows` registra 74 ventanas completadas, más de las ~45-46
> estimadas originalmente para cubrir 2015→hoy en trimestres. El desglose por período no
> está disponible en `processed.json` (solo se guarda la lista plana de ventanas
> `YYYYMMDD_YYYYMMDD`); si se requiere el desglose trimestral, hay que parsear esa lista.
> Prioridad: confirmar en `scripts/fetch.py` si las 74 ventanas cubren 2015-2026 sin
> huecos o si hay reintentos/duplicados inflando el conteo.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-25 | 4 (+1 falso positivo documentado) | 32 | Fix de bug en `mark-ingested` (scripts/ingest.py); creada página subsidios_programas.md |

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
