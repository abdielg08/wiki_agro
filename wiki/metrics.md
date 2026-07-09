---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-09
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos descargados (sources/) | 19 | ↑ continuo |
| Artículos ingestados (total) | 19 | = total sin falsos positivos |
| Artículos reales ingestados (con páginas wiki) | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 13 (7 + 6 nuevos hoy) | **0 nuevos** — meta incumplida hoy |
| Pendientes de ingesta | 0 | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal real (contenido) | 2015-2024 (semilla, 6 artículos) | 2015-02-19 → hoy |
| Ventanas GDELT completadas | 47 (años 2017–2026; 2015–2016 ausentes) | ~46-47 (2015→hoy) |
| Días sin artículos REALES nuevos | 17 (desde 2026-06-22) | máx 3 antes de diagnosticar — **excedido** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-09 (corrió correctamente)
Resultado               : 0 artículos reales nuevos (6 candidatos, los 6 falsos positivos)
Causa raíz identificada : fetch_ddg_search() en scripts/fetch_news.py construye queries
                          "site:{dominio} keyword1 OR keyword2 OR ..." pero la vertical
                          "news" de DuckDuckGo (ddgs) no respeta site: de forma confiable,
                          devolviendo resultados de dominios ajenos (sltrib.com, spa.gov.sa,
                          thestar.com.my, ieeexplore.ieee.org, nyfb.org, worldbank.org)
                          cuando el texto coincide con keywords genéricos (MIDA, cultivo,
                          agricultura). El código etiquetaba esos resultados con el dominio
                          configurado ("prensa.com") en vez del dominio real, ocultando el
                          desajuste. "MIDA" en particular colisiona con la Military
                          Installation Development Authority (Utah) y la Malaysian
                          Investment Development Authority.
Impacto                 : 0 artículos reales nuevos desde el fix del 2026-06-22 (17 días) —
                          100% de lo capturado por el fetch automático en ese período fue
                          falso positivo de esta misma causa.
Fix aplicado (hoy)      : fetch_ddg_search() ahora verifica que el dominio real de la URL
                          devuelta coincida con `site` antes de aceptar el resultado;
                          descarta silenciosamente los que no coinciden.
Estado post-fix         : Pendiente validación en la próxima corrida de GitHub Actions —
                          confirmar que RSS (IICA, La Prensa) siga aportando candidatos y
                          que ya no aparezcan dominios ajenos a los sitios configurados.
Pendiente adicional     : Ventanas GDELT 2015-2016 nunca se completan (error de red/timeout
                          persistente) — bloquea el backfill histórico temprano. Investigar
                          en próxima sesión.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | ? | **Bloqueado** — nunca completa (error de red/timeout) |
| 2016 Q1-Q4 | 0/4 | ? | **Bloqueado** — nunca completa (error de red/timeout) |
| 2017 Q1-Q4 | 4/4 | ver sources/articles/ | Completo |
| 2018 Q1-Q4 | 4/4 | ver sources/articles/ | Completo |
| 2019 Q1-Q4 | 4/4 | ver sources/articles/ | Completo |
| 2020 Q1-Q4 | 4/4 | ver sources/articles/ | Completo |
| 2021 Q1-Q4 | 4/4 | ver sources/articles/ | Completo |
| 2022 Q1-Q4 | 4/4 | ver sources/articles/ | Completo |
| 2023 Q1-Q4 | 4/4 | ver sources/articles/ | Completo |
| 2024 Q1-Q4 | 4/4 | ver sources/articles/ | Completo |
| 2025 Q1-Q4 | 4/4 | ver sources/articles/ | Completo |
| 2026 (fragmentado) | 11 ventanas cortas superpuestas | ver sources/articles/ | Anómalo — ver nota |
| **TOTAL** | **47 ventanas completadas** | — | **2015-2016 pendientes; 2017-2026 cubiertos** |

> Corregido 2026-07-09: `_gdelt_windows` en `sources/processed.json` sí tiene 47 ventanas completadas
> (años 2017-2026) — la tabla anterior decía "0/46, backfill no iniciado", lo cual era incorrecto.
> Los años 2015-2016 son el hueco real: cada corrida los reintenta desde `start=2015-01-01` pero
> fallan con error de red antes de marcarse completos, así que nunca avanza.
> Nota sobre 2026: en vez de ~2 ventanas trimestrales limpias, hay 11 ventanas cortas y superpuestas
> que empiezan todas en 2026-06-18 con fecha de fin creciente día a día — sugiere que el fetch diario
> reciente está generando ventanas ad-hoc en vez de trimestres fijos. No investigado a fondo esta
> sesión; revisar `fetch_gdelt_historical()` / el modo usado por GitHub Actions en la próxima sesión.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-09 | 0 reales (6 falsos positivos descartados) | 0 | Root-cause del bug `site:` en `fetch_ddg_search()` (colisión "MIDA"); fix aplicado en `scripts/fetch_news.py` |

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
