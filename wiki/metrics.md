---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-18
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 22 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 16 (7 previos + 9 nuevos el 2026-07-18) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 37 / ~46 estimadas (+12 entradas de "ventana actual" duplicadas, ver nota) | 46 (2015→hoy) |
| Días sin artículos nuevos | 3 (2026-07-16, 17, 18 hasta la hora de esta sesión) | máx 3 antes de diagnosticar — **ALERTA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-17 12:02 UTC (run 29578858522) — status: success (workflow), 0 artículos
Corrida de hoy          : 2026-07-18 aún no ejecuta — cron "0 11 * * *" dispara a las 11:00 UTC,
                          esta sesión corrió ~08:10 UTC, antes del cron de hoy.
Racha sin artículos     : 2026-07-16 (0), 2026-07-17 (0) confirmados por logs de Actions.
                          2026-07-15 sí trajo 1 artículo nuevo (rompió racha anterior).

CAUSA RAÍZ CONFIRMADA (logs de Actions, jobs 29497396400 y 29578858522):
  1. RSS IICA (iica.int/es/rss/noticias) → 0 entradas en el feed (roto o feed vacío)
  2. RSS La Prensa (prensa.com/feed/) → 0 entradas en el feed (roto o feed vacío)
  3. Búsqueda DDG → 6/7 queries devuelven "No results found" (site:mida.gob.pa, site:idiap.gob.pa,
     site:bda.gob.pa, site:fao.org, site:bancomundial.org, site:iica.int); solo "prensa_agro" corre
     sin error pero sin guardar artículos nuevos relevantes.
  4. GDELT → "GET blocked (403/429): https://api.gdeltproject.org/api/v2/doc/doc" en CASI TODAS
     las ventanas, incluyendo:
       - Las 5 ventanas históricas más antiguas (2015 Q1–Q4 y 2016 Q1, hasta 2016-03-30) que
         NUNCA han logrado completarse — GDELT las bloquea en cada corrida desde hace semanas.
       - La ventana "actual" (rolling, ~último mes) se regenera cada día con una fecha de fin
         distinta (día-1), por lo que nunca coincide con una ventana ya completada y siempre
         reintenta — y GDELT la bloquea (403/429) cada vez.
     37 ventanas históricas de 2017-03-30 a 2026-06-17 SÍ están completas (skip ya descargado).

DIAGNÓSTICO: no es que el rango de fechas esté agotado — es un bloqueo activo de GDELT (probable
rate-limit por IP compartida de GitHub Actions) combinado con feeds RSS de IICA/La Prensa que ya
no devuelven entradas. Las 3 fuentes de datos configuradas (RSS, DDG, GDELT) están efectivamente
inoperantes para artículos NUEVOS de Panamá, aunque el workflow de Actions sigue corriendo con éxito
todos los días (no es un problema de scheduling/cron).

Recomendación para el usuario:
  - Revisar por qué los feeds RSS de iica.int y prensa.com devuelven 0 entradas (¿URL cambiada?
    ¿feed movido? ¿bloqueo por user-agent?).
  - Considerar añadir backoff/retry con delay entre ventanas GDELT para evitar el rate-limit 403/429,
    o reducir la frecuencia de la corrida diaria.
  - Las 5 ventanas históricas 2015 Q1–2016 Q1 pueden necesitar una estrategia distinta (ej. mirror
    de GDELT, u otra fuente) ya que llevan semanas sin poder completarse.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | 0 | **Bloqueado — GDELT 403/429 en cada corrida** |
| 2016 Q1-Q1 (parcial, hasta 03-30) | 0/1 | 0 | **Bloqueado — GDELT 403/429 en cada corrida** |
| 2016 Q1(resto)-Q4 a 2017 Q1(parcial) | 4/4 | ver sources/ | Completo (20170330 en adelante) |
| 2017 Q2-Q4 | 3/3 | ver sources/ | Completo |
| 2018 Q1-Q4 | 4/4 | ver sources/ | Completo |
| 2019 Q1-Q4 | 4/4 | ver sources/ | Completo |
| 2020 Q1-Q4 | 4/4 | ver sources/ | Completo |
| 2021 Q1-Q4 | 4/4 | ver sources/ | Completo |
| 2022 Q1-Q4 | 4/4 | ver sources/ | Completo |
| 2023 Q1-Q4 | 4/4 | ver sources/ | Completo |
| 2024 Q1-Q4 | 4/4 | ver sources/ | Completo |
| 2025 Q1-Q4 | 4/4 | ver sources/ | Completo |
| 2026 Q1-Q2 (hasta 2026-06-17) | 2/2 | ver sources/ | Completo |
| 2026 (ventana actual, rolling) | 0/1 | 0 | **Bloqueado — GDELT 403/429 cada día, ventana se regenera diario** |
| **TOTAL** | **37/46** | **22 (todas las fuentes, incl. falsos positivos)** | **Backfill al 80%; las 9 ventanas faltantes están bloqueadas por GDELT, no por rango de fechas agotado** |

> Nota: 37 ventanas completas cubren 2017-03-30 → 2026-06-17. Las 5 ventanas 2015 Q1–2016 Q1
> (hasta 2016-03-30) y la ventana rolling actual llevan varias corridas consecutivas sin poder
> completarse por bloqueo 403/429 de GDELT. Ver "Estado del Fetch" arriba para diagnóstico completo.
> El conteo de "artículos" por trimestre no está desglosado — sources/articles/ no incluye metadata
> de qué ventana originó cada archivo.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-18 | 0 reales (9 falsos positivos descartados) | 0 | Cola de 9 pendientes eran 100% falsos positivos (ruido en inglés sobre MIDA Malaysia/Utah, agro genérico no-Panamá). Diagnóstico: RSS IICA/La Prensa devuelven 0 entradas, DDG sin resultados, GDELT bloqueando 403/429 la mayoría de ventanas incl. 5 históricas nunca completadas y la ventana rolling actual. 3 días consecutivos sin artículos nuevos reales (16, 17, 18-jul) — **alerta de sistema activa**. |

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
