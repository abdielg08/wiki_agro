---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-04
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 51 | ↑ continuo |
| Artículos reales ingestados (acumulado) | 10 | = total sin falsos positivos |
| Falsos positivos acumulados | 8 | **0 nuevos** |
| Pendientes de ingesta | 33 | 0 |
| Páginas en wiki/ | 25 (9 topics, 3 entidades, 10 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal real (artículos ingestados) | 2016-2024 | 2015-02-19 → hoy |
| Ventanas GDELT completadas | 78 (37 trimestrales + 41 "recientes" cuasi-duplicadas) | 46 (2015→hoy) |
| Días sin artículos nuevos reales | **8** (última: 2026-08-27) | máx 3 antes de diagnosticar — **⚠ ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions       : 2026-09-03 (0 artículos nuevos)
Último artículo nuevo real   : 2026-08-27 (1 artículo)
Días sin artículos nuevos    : 8 — supera el máximo de 3 (CLAUDE.md) → señal de alarma

Causa identificada (2026-09-04):
  - El backfill histórico NO cubre 2015-02-19 → 2017-03-29 (~2 años sin ninguna ventana GDELT).
  - La corrida diaria está re-escaneando una ventana "reciente" (desde 2026-06-18) cuyo `end`
    avanza ~1 día por corrida, generando una clave de ventana "nueva" aunque el contenido se
    solape casi totalmente con el día anterior → explica los "0 artículos nuevos" consecutivos.
  - RSS de IICA y La Prensa siguen activos pero aportan pocos artículos nuevos por día.

Acción recomendada:
  - Priorizar ventanas trimestrales faltantes de 2015-02-19 a 2017-03-29 en el fetcher GDELT.
  - Revisar generación de la ventana "reciente" para que no cree una clave nueva por cada `end`
    de un día distinto sin aportar cobertura real adicional.
  - Ver diagnóstico completo en wiki/log.md, entrada 2026-09-04 00:05.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015-02 a 2017-03 | 0 ventanas | **Pendiente — hueco confirmado en el objetivo de cobertura** |
| 2017-03 a 2026-06 | 37 ventanas trimestrales | Completado (cobertura continua confirmada) |
| 2026-06 a 2026-09 ("reciente") | 41 ventanas cuasi-duplicadas | Necesita corrección de lógica (ver diagnóstico arriba) |
| **TOTAL** | **78 ventanas** | **Backfill histórico incompleto — falta el tramo 2015-2017** |

> Reemplaza la tabla trimestral anterior (que asumía 46 ventanas 2015-2026) porque las claves reales
> de `_gdelt_windows` no siguen ese esquema de trimestres fijos. Ver detalle en wiki/log.md.

---

## Falsos Positivos Detectados

| Fecha detección | Artículo | Motivo |
|------------------|----------|--------|
| 2026-06-22 | (7 artículos, auditoría previa) | Ver wiki/log.md, entrada 2026-06-22 |
| 2026-09-04 | "MITI working on simplified NCM..." (paultan.org) | Medio automotriz de Malasia; MITI/MARii malayos, no MIDA panameño |
| Pendiente de revisión | "Mozambique: More than 1M doses of foot-and-mouth vaccine..." (clubofmozambique.com) | Trata sobre Mozambique, no Panamá — detectado pero fuera del batch procesado hoy |

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Falsos positivos | Pendientes restantes | Nota |
|-------|---------------------|-------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 7 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-04 | 4 | 1 | 33 | Sesión programada; diagnóstico de backfill incompleto 2015-2017 |

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

**Estado actual de la alarma (2026-09-04)**: ACTIVA — 8 días sin artículos nuevos reales.
Diagnóstico ya documentado (ver arriba y wiki/log.md); pendiente de que una sesión con acceso a
`scripts/` corrija la lógica de generación de ventanas GDELT.
