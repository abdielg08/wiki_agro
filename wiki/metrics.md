---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-11
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 64 / ~45 estimadas | 45 (2015→hoy) |
| Días sin artículos nuevos | 12 (desde 2026-07-30) | máx 3 antes de diagnosticar |

**Alarma activa**: 12 días consecutivos sin artículos nuevos reales — muy por encima
del umbral de 3 días de CLAUDE.md. Ver diagnóstico en `wiki/log.md` (2026-08-11 16:20).

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-10 (0 artículos nuevos)
Última corrida con artículos nuevos : 2026-07-30 (3 artículos)
Ventanas GDELT completadas : 64 — el umbral de 45 ya se superó, backfill
                              GDELT no está limitado por ventanas pendientes.

Causa raíz identificada (2026-08-11): fetch_ddg_search() en
  scripts/fetch_news.py (fuente "prensa_agro", config/sources.yaml:157-161)
  - El operador site:prensa.com no es respetado por DDGS().news()
  - La query usa OR entre términos globales ("MIDA", "agricultura") sin
    exigir contexto Panamá → capta MIDA-Utah, MIDA-Malasia, agro de España/
    Brasil/Arabia Saudita, etc.
  - _is_panama_related() y _is_blocked_domain() ya existen en el código
    (fetch_news.py líneas 72-81) pero NUNCA se llaman dentro de
    fetch_ddg_search() — solo se usa is_agro_relevant()
  - El campo "source" se fija como "prensa.com" para todo resultado de esta
    búsqueda sin verificar el dominio real
  Resultado: 16/16 artículos pendientes revisados en esta sesión (2026-08-11)
  fueron falsos positivos (100%), todos provenientes de esta fuente.
  Fix recomendado: detallado en wiki/log.md (2026-08-11 16:20) — requiere
  editar scripts/fetch_news.py, fuera del alcance de una sesión de ingesta.
Estado post-fix        : NO aplicado — pendiente de una sesión de mantenimiento de código
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

> Una vez que Actions corra con el código corregido, actualizar esta tabla con los datos reales.
> El rendimiento real de GDELT (artículos/trimestre) determinará la duración del backfill.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-11 | 0 | 0 | 16 artículos revisados, 16 falsos positivos (100%). Causa raíz localizada en fetch_ddg_search() — ver log.md |

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
