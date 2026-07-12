---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-12
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 20 | ↑ continuo |
| Artículos reales ingestados | 13 | = total sin falsos positivos |
| Falsos positivos acumulados | 14 (7 del 2026-06-22 + 7 del 2026-07-12) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 48 / ~45-46 estimadas | 45 (2015→hoy) — **rango agotado, evaluar expansión** |
| Días sin artículos nuevos | 2 (última descarga: 2026-07-10) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con commit  : 2026-07-10 (88389fe) — 1 artículo nuevo, resultó falso positivo
Corridas sin commit        : 2026-07-11 y 2026-07-12 (hoy) — el workflow normalmente commitea
                              incluso con 0 artículos nuevos, así que la ausencia de commit sugiere
                              que la Action no corrió o falló antes del paso de commit (sin
                              confirmar desde esta sesión — revisar historial de runs de Actions)
Causa raíz (2026-07-12)     : fetch_ddg_search() en scripts/fetch_news.py no aplicaba los filtros
                              _is_blocked_domain()/_is_panama_related() que RSS y GDELT sí tienen
                              desde el fix del 2026-06-22 (#20). Resultado: 7/7 artículos pendientes
                              eran falsos positivos (MIDA de Utah, agro de EE.UU./Arabia
                              Saudita/Irán) — 0% de la cola era contenido válido de Panamá.
Fix aplicado (2026-07-12)   : fetch_ddg_search() ahora exige que el dominio del resultado
                              contenga el `site` configurado, aplica _is_blocked_domain(), y exige
                              _is_panama_related() en título/URL/cuerpo — igual que RSS y GDELT.
                              También se corrigió mark_ingested() en scripts/ingest.py, que
                              crasheaba (AttributeError) al iterar la clave interna _gdelt_windows.
Estado post-fix             : Pendiente validación en la próxima corrida de Actions
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
| 2026-07-12 | 0 | 0 | 7/7 pendientes eran falsos positivos (bug en fetch_ddg_search sin filtro Panamá/dominio) — 0 agregados al wiki, fix de código aplicado |

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
