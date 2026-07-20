---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-20
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 22 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 16 | **0 nuevos** — 9 nuevos detectados el 2026-07-20 |
| Pendientes de ingesta | 0 | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 51 / ~45 estimadas | 45 (2015→hoy) — **umbral superado, ver nota** |
| Días sin artículos nuevos | 5 (último real: 2026-07-15) | máx 3 antes de diagnosticar — **⚠ excedido** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-19 (commit sources/ ese día, 0 artículos nuevos)
Corridas recientes     : 07-15 (1 nuevo), 07-16 sin commit, 07-17 sin commit,
                         07-18 (0 nuevos), 07-19 (0 nuevos)
Resultado               : 5 días sin artículos NUEVOS desde el 2026-07-15 → señal de alarma
                         de CLAUDE.md (máx 3 días) ACTIVADA
Causa identificada (1)  : GDELT — 51 ventanas completadas (`_gdelt_windows` en
                         processed.json), supera el umbral de 45 de CLAUDE.md Paso 4.2 →
                         el rango 2015-hoy ya fue cubierto; GDELT esencialmente agotado
                         para los términos de búsqueda actuales, necesita expansión
                         (nuevos términos/queries) para seguir aportando artículos.
Causa identificada (2)  : RSS/DDG "prensa.com" — todos los artículos recientes de esta
                         fuente (16 de 22 descargados) son falsos positivos por
                         ambigüedad del término "MIDA" (Malasia, Utah) o son contenido
                         agrícola genérico sin relación con Panamá. Ver wiki/log.md
                         2026-07-20 para el detalle completo y la causa raíz en
                         scripts/fetch_news.py (country="PA" hardcodeado, sin
                         verificación real de origen).
Fix aplicado esta sesión: bug en `mark_ingested()` (scripts/ingest.py) que rompía el
                         comando `mark-ingested <url>` para cualquier URL — corregido
                         (no relacionado con el fetch).
Pendiente (fuera de alcance de rutina): ajustar scripts/fetch_news.py para exigir
                         contexto agropecuario panameño real en la ruta RSS/DDG, y
                         expandir/renovar los términos de búsqueda GDELT.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | ? | Pendiente |
| 2016 Q1-Q4 | 0/4 | ? | Pendiente |
| 2017 Q1-Q4 | 0/4 | ? | Pendiente |
| 2018 Q1-Q4 | 0/4 | ? | Pendiente |
| 2019 Q1-Q4 | 0/4 | ? | Pendiente |
| 2020 Q1-Q4 | 0/4 | ? | Pendiente |
| 2021 Q1-Q4 | 0/4 | ? | Pendiente |
| 2022 Q1-Q4 | 0/4 | ? | Pendiente |
| 2023 Q1-Q4 | 0/4 | ? | Pendiente |
| 2024 Q1-Q4 | 0/4 | ? | Pendiente |
| 2025 Q1-Q4 | 0/4 | ? | Pendiente |
| 2026 Q1-Q2 | 0/2 | ? | Pendiente |
| **TOTAL** | **0/46** | **0** | **Backfill no iniciado** |

> **2026-07-20**: `processed.json._gdelt_windows` registra **51 ventanas ya completadas**
> (más que las 46 estimadas arriba), pero esta tabla trimestral no se ha actualizado con el
> detalle real por ventana — pendiente de reconciliar. El rendimiento real ha sido bajo:
> de los artículos traídos por GDELT/RSS, la inmensa mayoría resultaron falsos positivos
> (ver "Estado del Fetch" arriba). No se recomienda seguir invirtiendo en más ventanas GDELT
> con los mismos términos de búsqueda sin antes revisar `config/sources.yaml`.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-20 | 0 reales / 9 falsos positivos revisados | 0 | 9/9 pendientes eran falsos positivos (Malasia/Utah MIDA, agro genérico sin Panamá); fix de bug en `mark-ingested`; diagnóstico: GDELT agotado (51 ventanas) + fetch RSS sin filtro geográfico |

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
