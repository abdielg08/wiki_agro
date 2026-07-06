---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-06
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 19 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 13 | **0 nuevos** (causa raíz corregida hoy) |
| Pendientes de ingesta | 0 | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 45 / ~46 estimadas | 46 (2015→hoy) |
| Días sin artículos nuevos | 0 (llegaron artículos vía DDG hoy) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : ~2026-07-02 (fecha del último artículo guardado en sources/)
Resultado              : Los artículos SÍ están llegando, pero mayoría vía DDG search
                         eran falsos positivos (ver diagnóstico 2026-07-06 en log.md)
_gdelt_windows          : 45 ventanas completadas en sources/processed.json
                         → 45+ = rango de fechas GDELT ya agotado, necesita expansión
                         (CLAUDE.md Paso 4.2: revisar/ampliar rango de años consultado)
Causa raíz (histórica)  : fetch_ddg_search() no filtraba por dominio real ni exigía
                         mención de Panamá → 13 falsos positivos acumulados
Fix aplicado 2026-07-06 : scripts/fetch_news.py — fetch_ddg_search() y fetch_world_bank()
                         ahora aplican _is_blocked_domain()/_is_panama_related() igual
                         que fetch_rss()/fetch_gdelt_batch(). scripts/ingest.py —
                         mark_ingested() ya no crashea con la clave interna _gdelt_windows.
Estado post-fix         : Pendiente validar en la próxima corrida de Actions que ya no
                         se generen falsos positivos vía DDG; expandir ventanas GDELT.
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
| 2026-07-06 | 0 (6 revisados, 6 falsos positivos) | 0 | Fix causa raíz en fetch_ddg_search()/fetch_world_bank() (filtro de dominio + _is_panama_related); fix crash en mark_ingested(); 45 ventanas GDELT completadas → expandir rango |

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
