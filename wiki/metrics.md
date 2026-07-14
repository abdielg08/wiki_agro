---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-14
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 20 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 14 | **0 nuevos** desde el fix de esta sesión |
| Pendientes de ingesta | 0 | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 48 / ~46 estimadas | rango agotado — 0 artículos reales producidos |
| Días sin artículos nuevos reales | 51 (desde 2026-05-24) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions  : 2026-07-14 (commit 88389fe, 1 artículo nuevo descargado)
Resultado                : Actions SÍ corre y descarga regularmente (ver git log de sources/),
                           pero el 100% de lo descargado bajo la fuente "prensa.com" (búsqueda
                           web_searches.prensa_agro vía DuckDuckGo) ha sido falso positivo:
                           14/14 histórico, 7/7 en esta sesión.
Causa identificada       : fetch_ddg_search() usa `site:prensa.com` en la query de DDGS.news(),
                           pero DuckDuckGo no respeta ese operador de forma confiable y devuelve
                           resultados de dominios no relacionados (sltrib.com, thestar.com.my,
                           fox13now.com, ieeexplore.ieee.org, worldbank.org, whc.unesco.org,
                           spa.gov.sa, nyfb.org). is_agro_relevant() hace matching de substring
                           contra "MIDA" sin contexto de país, dejando pasar agencias homónimas
                           de EEUU (Military Installation Development Authority) y Malasia.
                           GDELT: 48 ventanas completadas (rango 2015→hoy agotado) pero 0
                           artículos reales producidos — nunca ha aportado contenido al wiki.
Fix aplicado (2026-07-14): scripts/fetch_news.py::fetch_ddg_search() ahora valida que el
                           dominio (netloc) de cada URL devuelta coincida con `site` antes de
                           aceptarla; descarta silenciosamente lo que no coincide.
Estado post-fix          : Pendiente validación en la próxima corrida de GitHub Actions.
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
| 2026-07-14 | 0 | 0 | 7/7 pendientes eran falsos positivos (Utah/Malasia/Arabia Saudita/EEUU/UNESCO); fix de raíz aplicado en fetch_ddg_search() (validación de dominio) |

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
