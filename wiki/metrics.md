---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-30
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 26 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 20 (7 previos + 13 hoy) | **0 nuevos al wiki** (mantenido) |
| Pendientes de ingesta | 0 | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 0 / ~45 estimadas | 45 (2015→hoy) — backfill histórico no se ha disparado (workflow manual `wiki_historical.yml` sin ejecutar) |
| Días sin artículos nuevos | 1 (última descarga: 2026-07-29, 2 artículos) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-29 (2 artículos nuevos descargados)
Resultado              : Fetch diario corriendo con cadencia normal (0-2 artículos/día)
                         pero ~100% de lo descontado vía web_searches DDG resultó
                         ser falso positivo (13/13 esta sesión, 7 en auditoría previa)
Causa raíz (2026-07-30): fetch_ddg_search() (scripts/fetch_news.py) no aplicaba
                         _is_blocked_domain() ni _is_panama_related(), a diferencia
                         de fetch_rss() y el crawl GDELT. El operador DDG "site:"
                         no se respeta de forma confiable → resultados de dominios
                         no panameños (thestar.com.my, sltrib.com, heraldo.es,
                         ieeexplore.org, spa.gov.sa, whc.unesco.org, etc.)
                         entraban re-etiquetados a ciegas como prensa.com/PA/es.
                         El acrónimo "MIDA" colisiona con agencias de Malasia y
                         Utah (EE.UU.) — mismo patrón detectado el 2026-06-22.
Fix aplicado (2026-07-30): fetch_ddg_search() ahora aplica los mismos dos filtros
                         que fetch_rss(); _is_panama_related() exime dominios
                         .gob.pa. Ver wiki/log.md 2026-07-30 08:09 para detalle.
Bug adicional corregido : mark_all_ingested() usaba orden distinto (alfabético
                         por archivo) al de ingest/prioritize() (por score),
                         marcando ingestados artículos nunca revisados.
                         mark_ingested() fallaba con AttributeError si
                         processed.json tiene la clave _gdelt_windows. Ambos
                         corregidos en scripts/ingest.py.
Backfill histórico GDELT: sigue en 0/46 ventanas — el workflow
                         wiki_historical.yml es solo manual (workflow_dispatch)
                         y no se ha disparado desde que se creó. Requiere que
                         el usuario lo ejecute manualmente (o autorice a la
                         routine a hacerlo vía Actions) para avanzar el
                         objetivo de cobertura 2015→hoy.
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
| 2026-07-30 | 0 (13 revisados, 13/13 falsos positivos) | 0 | Auditoría de 13 pendientes; fix de raíz en fetch_ddg_search() (faltaban filtros anti-FP); fix de mark_all_ingested()/mark_ingested() en scripts/ingest.py |

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
