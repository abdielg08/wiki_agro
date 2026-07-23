---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-23
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 18 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 37 históricas / ~46 estimadas (+15 diarias redundantes) | 46 (2015→hoy) |
| Días sin artículos nuevos reales | ~60 (desde carga semilla 2026-05-24) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-22 (success) — verificado vía GitHub API
Resultado               : Actions corre en success diariamente, pero desde la
                          carga semilla (2026-05-24) NO ha aportado ningún
                          artículo real: 18/18 artículos descargados desde
                          entonces son falsos positivos, y el 100% de ellos
                          viene de la fuente web_searches.prensa_agro
                          (DDG site:prensa.com) en config/sources.yaml.
Causa identificada      : El operador `site:` de ddgs.news() no filtra —
                          devuelve resultados de dominios arbitrarios
                          (sltrib.com, paultan.org, msn.com, archive.org,
                          ieeexplore.org, spa.gov.sa, nyfb.org, whc.unesco.org)
                          que solo coinciden por palabra clave ("MIDA",
                          "agriculture"), y se guardan mal etiquetados como
                          fuente "prensa.com" sin validar el dominio real.
                          RSS (IICA, La Prensa) y GDELT no aportaron artículos
                          reales en este período tampoco.
Fix recomendado         : validar en fetch_news.py que el dominio de la URL
                          devuelta coincida con el `site:` configurado antes
                          de guardar, o deshabilitar prensa_agro hasta
                          corregir el filtro. No aplicado — requiere cambio
                          de código fuera del alcance de la routine de ingesta.
Backfill GDELT          : 37/46 ventanas trimestrales históricas completas
                          (2017 Q1 → hoy); faltan ~8 ventanas de 2015-2016.
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
| 2026-07-23 | 0 | 0 | 11 falsos positivos nuevos detectados y descartados (fuente prensa_agro/DDG rota). Total falsos positivos acumulados: 18 |

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
