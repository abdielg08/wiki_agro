---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-19
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 22 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 16 | **0 nuevos** (0 llegaron al wiki) |
| Pendientes de ingesta | 0 | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 51 / ~46-47 estimadas | rango 2015→hoy agotado |
| Días sin artículos REALES nuevos | ~56 (desde semilla 2026-05-24) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions       : 2026-07-19 (0 artículos nuevos)
Racha de falsos positivos    : 16 tandas consecutivas (2026-05-30 → 2026-07-19)
                                100% de lo descargado por fetch_ddg_search() era ruido
                                internacional (Malasia, Utah EEUU, Arabia Saudita, IEEE,
                                UNESCO, NY Farm Bureau) — 0 artículos reales de Panamá
                                desde la semilla manual del 2026-05-24.
Causa raíz identificada      : fetch_ddg_search() (búsqueda DDG "prensa_agro" en
                                config/sources.yaml) NO aplicaba _is_blocked_domain()
                                ni _is_panama_related() — filtros que sí usan fetch_rss()
                                y fetch_gdelt_batch() en el mismo archivo. Solo exigía
                                coincidencia de un término genérico ("MIDA", "agricultura")
                                sin exigir mención de Panamá. El operador site:prensa.com
                                de DDG tampoco se respeta de forma confiable.
Fix aplicado (2026-07-19)    : scripts/fetch_news.py::fetch_ddg_search() ahora aplica los
                                mismos filtros de dominio/Panamá que fetch_rss/fetch_gdelt.
Estado post-fix               Pendiente validación en próxima corrida de GitHub Actions —
                                revisar si el fetch diario vuelve a traer artículos reales.
Ventanas GDELT                51 completadas, por encima de la estimación de ~46-47 para
                                cubrir 2015→hoy en trimestres de 90 días — el rango de
                                fechas está prácticamente agotado. GDELT en sí SÍ aplicaba
                                los filtros correctos, pero no está claro si ha encontrado
                                artículos reales (no se pudo confirmar en esta sesión sin
                                ejecutar un fetch en vivo) — revisar en la próxima corrida.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | 0 | **Nunca completadas** — ver nota |
| 2016 Q1-Q4 | 0/4 | 0 | **Nunca completadas** — ver nota |
| 2017 Q1-Q4 | 4/4 | 0 reales (todo filtrado) | Completo |
| 2018 Q1-Q4 | 4/4 | 0 reales (todo filtrado) | Completo |
| 2019 Q1-Q4 | 4/4 | 0 reales (todo filtrado) | Completo |
| 2020 Q1-Q4 | 4/4 | 0 reales (todo filtrado) | Completo |
| 2021 Q1-Q4 | 4/4 | 0 reales (todo filtrado) | Completo |
| 2022 Q1-Q4 | 4/4 | 0 reales (todo filtrado) | Completo |
| 2023 Q1-Q4 | 4/4 | 0 reales (todo filtrado) | Completo |
| 2024 Q1-Q4 | 4/4 | 0 reales (todo filtrado) | Completo |
| 2025 Q1-Q4 | 4/4 | 0 reales (todo filtrado) | Completo |
| 2026 (parcial, hasta 2026-07-18) | 15 ventanas (cola irregular) | 0 reales (todo filtrado) | Estancado en 2026-06-18 — ver nota |
| **TOTAL** | **51 ventanas completadas** | **0 artículos reales vía GDELT** | **2015–2016 sin cubrir; cola 2026 estancada** |

> Nota 1 — brecha 2015–2016: las 9 ventanas trimestrales de 2015-01-01 a 2017-03-29 nunca
> se marcaron como completadas (0/9). No se pudo confirmar la causa exacta sin ejecutar un
> fetch en vivo en esta sesión (posible: GDELT DOC 2.0 no indexa de forma fiable tan atrás
> pese a que CLAUDE.md fija 2015-02-19 como límite teórico, o son timeouts persistentes).
> Requiere una corrida de diagnóstico dedicada.
> Nota 2 — cola 2026 estancada: `fetch_gdelt_historical()` calcula la ventana final como
> `min(current + 90d, end)` con `end` = ayer, que cambia cada día. Como la ventana de cola
> nunca coincide con una ya completada, se re-consulta y re-marca como "completa" cada
> corrida con un rango apenas más ancho, sin que el cursor avance más allá de 2026-06-18.
> Ver `wiki/log.md` (entrada 2026-07-19) para el detalle — no corregido aún.
> GDELT sí aplica correctamente los filtros de Panamá (`_is_blocked_domain`,
> `_is_panama_related`), por eso 0 artículos reales no es un problema de falsos positivos
> — es que, dentro de las ventanas ya cubiertas, no ha encontrado noticias de agro
> panameño que superen esos filtros.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-19 | 0 reales / 9 revisados | 0 | 9 falsos positivos rechazados (0 al wiki); fix de raíz en `fetch_ddg_search()` (faltaban filtros Panamá/dominio); documentado estancamiento cola GDELT y brecha 2015–2016 |

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
