---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-28
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 51 | ↑ continuo |
| Artículos ingestados (processed.json) | 18 | = total sin falsos positivos |
| Artículos reales en wiki (summaries) | 10 | = ingestados − falsos positivos marcados |
| Falsos positivos acumulados (marcados ingested pero fuera del wiki) | 8 | **0 nuevos añadidos al wiki** |
| Pendientes de ingesta | 33 | 0 |
| Páginas en wiki/ | 24 (8 topics, 3 entities, 10 summaries, 3 overview) | ↑ continuo |
| Cobertura temporal real (sources/) | 2007-11-04 → 2026-08-21 (incluye ruido pre-2015, ver nota) | 2015-02-19 → hoy |
| Ventanas GDELT completadas | 76 | ~45-46 estimadas (ya superado) |
| Días sin artículos nuevos | 1 (último commit sources/: 2026-08-27) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-27 (commit "1 artículos nuevos descargados")
Resultado               : Fetch activo, backfill avanzando (76 ventanas GDELT completadas)
Días sin artículos      : 1 — dentro de umbral normal (falla a los 3 días consecutivos)
```

### Problema de calidad detectado (2026-08-28): colisión de acrónimos en el fetch

El pipeline de fetch está trayendo artículos NO relacionados con Panamá que
colisionan por acrónimo o keyword con términos agro panameños:

- **"MIDA"**: colisiona con Malaysian Investment Development Authority (Malasia,
  medio thestar.com.my) y con Military Installation Development Authority
  (Utah, medio fox13now.com). Confirmados 8 falsos positivos con este patrón
  (7 históricos + 1 nuevo el 2026-08-28: paultan.org/MITI Malasia).
- Otros falsos positivos sospechosos vistos en sources/ sin confirmar aún:
  `ieeexplore.ieee.org/document/10945742` (pendiente), artículo fechado
  2026-08-21 sobre "Mozambique foot-and-mouth vaccine" (no es Panamá),
  y artículos con fecha 2007 (fuera del rango objetivo 2015→hoy).
- Ninguno de estos contaminó el wiki (topics/entities/summaries) — el filtro
  humano/LLM en el paso de ingesta los detecta y descarta correctamente.
  El costo es operativo: infla "artículos descargados" e "ingestados" con
  ruido que hay que revisar manualmente en cada sesión.

**Recomendación**: agregar filtro de relevancia más estricto en el fetch
(ej. exigir `country:PA` en GDELT y/o lista negra de dominios no panameños
como thestar.com.my, fox13now.com, paultan.org) antes de guardar en sources/.

---

## Progreso del Backfill GDELT (2015 → hoy)

| Métrica | Valor |
|---------|-------|
| Ventanas GDELT completadas | 76 (superó la estimación original de ~45-46) |
| Artículos totales en sources/ | 51 |
| Cobertura de fechas observada | 2007-11-04 → 2026-08-21 (incluye ruido pre-2015 y falsos positivos internacionales) |

> El desglose trimestral detallado no se recalculó esta sesión — pendiente para
> una sesión de mantenimiento dedicada a reconstruir la tabla por período a
> partir de `_gdelt_windows` en `sources/processed.json`.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-28 | 4 reales + 1 falso positivo descartado | 33 | Rutina automatizada; 1 nuevo falso positivo (paultan.org/MITI, colisión "MIDA") documentado y NO ingestado al wiki |

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
