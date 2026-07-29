---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-29
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 18 | **0 nuevos** (fix aplicado esta sesión) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 57 / ~47 estimadas | rango agotado — trickle ~1 ventana/90d |
| Días sin artículos reales nuevos | ~65 (desde semilla 2026-05-24) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-28 (commit chore(sources), 0 artículos nuevos)
Resultado               : commits diarios corriendo, pero 100% del volumen histórico desde la
                          semilla (18 artículos, 2026-05-26→2026-07-28) resultó ser falsos
                          positivos de fetch_ddg_search() (fuente "prensa.com")
Causa identificada      : fetch_ddg_search() no aplicaba _is_blocked_domain()/_is_panama_related()
                          (sí presentes en fetch_rss() y GDELT) → "MIDA" (Malasia/Utah) y
                          agricultura genérica global pasaban el filtro is_agro_relevant()
Fix aplicado            : se agregaron los mismos guards a fetch_ddg_search() (scripts/fetch_news.py)
                          + fix de bug en mark_ingested() (crasheaba con claves _meta de processed.json)
Estado post-fix         : pendiente validación en próxima corrida Actions (¿el yield real de DDG
                          cae a ~0 tras el fix, o sigue aportando contenido genuino?)
GDELT                   : 57 ventanas completadas — rango 2015→hoy ya cubierto, comportamiento
                          normal es ~0 artículos/día hasta que se abra la próxima ventana trimestral
RSS (IICA, La Prensa)   : no verificable desde esta sesión (sin acceso de red saliente); pendiente
                          confirmar en próxima corrida de Actions si están aportando algo real
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
| 2026-07-29 | 0 (real) | 0 | 11/11 pendientes eran falsos positivos (MIDA Malasia/Utah + agro global genérico); fix de raíz en `fetch_ddg_search()` |

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
