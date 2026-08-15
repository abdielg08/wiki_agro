---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-15
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos ingestados (total) | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 11 | 0 |
| Falsos positivos acumulados | 12 (+5 hoy) | **0 nuevos** ⚠️ meta incumplida hoy |
| Páginas en wiki/ | 20 (8 topics, 3 entities, 6 summaries, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 67 | 46 (2015→hoy, ~trimestral) — ya superado, ver nota |
| Días sin artículos nuevos | **15** (desde 2026-07-30) | máx 3 antes de diagnosticar — ⚠️ **UMBRAL EXCEDIDO 5x** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con commit  : 2026-08-14 (corre diario, "chore(sources): 0 artículos nuevos [skip ci]")
Racha sin artículos nuevos : 2026-07-31 → 2026-08-14 (8 corridas consecutivas, 15 días) = 0 nuevos
Último artículo real nuevo : 2026-07-30 (3 artículos)

CAUSA RAÍZ CONFIRMADA (sesión 2026-08-15):
  scripts/fetch_news.py::fetch_ddg_search() (usada por web_searches.prensa_agro,
  config/sources.yaml, query con término ambiguo "MIDA") pasa `site:prensa.com` a
  ddgs.news(), pero DuckDuckGo no honra ese operador de forma confiable — retorna
  resultados de dominios no panameños (paultan.org, sltrib.com, msn.com) etiquetados
  como source="prensa.com". A diferencia de fetch_rss(), fetch_ddg_search() NO
  aplicaba _is_blocked_domain()/_is_panama_related() — por eso 5/5 artículos del
  lote de hoy fueron falsos positivos (colisión de acrónimo "MIDA" con Malasia/Utah).
  Esto probablemente explica buena parte de por qué el fetch automático "corre" pero
  no produce artículos reales nuevos hace 15 días: el pipeline probablemente está
  descargando falsos positivos que otros filtros descartan silenciosamente antes de
  guardarlos, o GDELT (ventanas ya en 67, más que las ~46 trimestrales esperadas para
  2015→hoy) está devolviendo resultados repetidos/duplicados sin cobertura nueva.

FIX APLICADO esta sesión: agregados _is_blocked_domain(url) y
  _is_panama_related(title, url) a fetch_ddg_search() en scripts/fetch_news.py
  (mismo guardrail que ya tenía fetch_rss()). Pendiente validar en la próxima
  corrida de GitHub Actions si esto restaura el flujo de artículos nuevos, o si
  el problema real está en el agotamiento de ventanas GDELT (67 completadas)
  y hace falta expandir/reiniciar el rango de backfill.
Estado post-fix: pendiente de validación (próxima corrida Actions).
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

> ⚠️ Tabla desactualizada: `sources/processed.json._gdelt_windows` ya tiene 67 ventanas
> completadas (más que las ~46 estimadas), pero esta tabla no se ha reconciliado con el
> detalle real por período. Pendiente para una sesión futura: recorrer `_gdelt_windows`
> y recalcular esta tabla por año/trimestre real.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-15 | 0 reales (5 revisados, 5 falsos positivos) | 11 | Fix de causa raíz en fetch_ddg_search() (faltaban filtros geo/dominio). 15 días sin artículos reales nuevos (desde 2026-07-30) — ver "Estado del Fetch". |

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
