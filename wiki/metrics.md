---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-11
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 20 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 14 | **0 nuevos** (bug de origen corregido hoy) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 0 / ~45 estimadas | 45 (2015→hoy) |
| Días sin artículos nuevos reales | ≥48 (desde 2026-06-22) | máx 3 antes de diagnosticar |
| Pendientes de ingesta | 0 | 0 |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-10 (chore(sources): 1 artículo nuevo)
Resultado              : 1 artículo descargado — era falso positivo (Persian Qanat, UNESCO/Irán)
Causa raíz identificada: fetch_ddg_search() en scripts/fetch_news.py buscaba
                         "site:prensa.com ... MIDA ... agricultura" vía DuckDuckGo
                         News, pero el operador site: de DDG no se respeta de forma
                         confiable → devuelve noticias globales que matchean
                         términos ambiguos ("MIDA" = Utah/Malasia, "agricultura"
                         = cualquier país). A diferencia de fetch_rss() y
                         fetch_gdelt_batch() en el mismo archivo, fetch_ddg_search()
                         NO tenía los filtros _is_blocked_domain()/_is_panama_related().
                         Esto explica que 7/7 artículos pendientes de esta sesión
                         (y 7/7 de la sesión 2026-06-22) fueran falsos positivos.
Fix aplicado (hoy)     : fetch_ddg_search() ahora aplica _is_blocked_domain() y
                         _is_panama_related() antes de aceptar un resultado.
                         fetch_historical.py (fetch_gdelt_window, aún sin usar en
                         producción) recibió el mismo fix + AND-requerimiento de
                         mención de Panamá en la query GDELT.
                         ingest.py: mark_ingested() ya no crashea con la clave
                         interna _gdelt_windows.
Estado post-fix        : Pendiente validar en la próxima corrida de Actions
                         (mañana) que ya no lleguen falsos positivos de DDG.
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
| 2026-07-11 | 0 (7 falsos positivos descartados) | 0 | Causa raíz encontrada y corregida: fetch_ddg_search() sin filtro Panamá |

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
