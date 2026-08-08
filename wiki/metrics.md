---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-08
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 (7 previos + 16 hoy) | **0 nuevos reales** — causa raíz corregida hoy |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 63 / 47 esperadas (ver nota) | 47 (2015→hoy) |
| Días sin artículos nuevos reales | Indefinido — ningún fetch automático ha producido un artículo real todavía | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-07 (0 artículos nuevos ese día)
Resultado sesión hoy    : 16 pendientes revisados, 16/16 falsos positivos (0 reales)
Causa identificada      : scripts/fetch_news.py::fetch_ddg_search() — el operador
                          `site:` de DuckDuckGo no se respeta de forma confiable;
                          las búsquedas "site:prensa.com ..." devolvían artículos de
                          heraldo.es, sltrib.com, ieeexplore.ieee.org, archive.org,
                          agenciabrasil.ebc.com.br, whc.unesco.org, etc. — todos
                          mal etiquetados como fuente "prensa.com" / país PA porque
                          el código no verificaba el dominio real de la URL.
Fix aplicado hoy         : filtro de dominio real (urlparse) antes de aceptar un
                          resultado DDG; "source" ahora usa el nombre de búsqueda,
                          no el `site` sin validar. Ver scripts/fetch_news.py.
Bug separado corregido   : scripts/ingest.py::mark_ingested() fallaba con
                          AttributeError al iterar la clave interna "_gdelt_windows"
                          (lista) como si fuera un dict de artículo — corregido para
                          usar article_entries().
Pendiente de validar     : la próxima corrida de GitHub Actions (mañana ~6am Panamá)
                          debería dejar de traer falsos positivos de DDG. Si vuelven
                          a aparecer, el bug no está en site:/dominio sino en otra
                          fuente de búsqueda — revisar de nuevo.
Diagnóstico GDELT        : 63 ventanas marcadas "completas" pero (a) faltan las
                          ventanas 2015-01-01→2017-03-29 (~9), debería autocompletarse
                          la próxima corrida; (b) desde 2026-06-18 el trimestre en
                          curso se re-marca completo casi a diario con distinta fecha
                          final, inflando el conteo sin cobertura nueva — no corregido
                          hoy, bajo impacto (no genera falsos positivos). Ningún
                          artículo real ha venido de GDELT todavía.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | 0 | **Pendiente — nunca procesado** |
| 2016 Q1-Q4 | 0/4 | 0 | **Pendiente — nunca procesado** |
| 2017 Q1-Q4 | 4/4 | 0 | Completo, sin resultados |
| 2018 Q1-Q4 | 4/4 | 0 | Completo, sin resultados |
| 2019 Q1-Q4 | 4/4 | 0 | Completo, sin resultados |
| 2020 Q1-Q4 | 4/4 | 0 | Completo, sin resultados |
| 2021 Q1-Q4 | 4/4 | 0 | Completo, sin resultados |
| 2022 Q1-Q4 | 4/4 | 0 | Completo, sin resultados |
| 2023 Q1-Q4 | 4/4 | 0 | Completo, sin resultados |
| 2024 Q1-Q4 | 4/4 | 0 | Completo, sin resultados |
| 2025 Q1-Q4 | 4/4 | 0 | Completo, sin resultados |
| 2026 Q1-Q3 | 27 ventanas marcadas (infladas, ver nota) | 0 | En curso |
| **TOTAL** | **63 marcadas / 47 esperadas** | **0** | **2015-01→2017-03 pendiente; resto de 2015-2025 exhaustivamente consultado en GDELT sin encontrar artículos** |

> Hallazgo clave: GDELT no ha aportado NINGÚN artículo real hasta ahora (0 de 63 ventanas
> consultadas), a pesar de tener el filtro Panamá correcto (`sourcecountry:PA` + términos
> AND Panamá/Chiriquí/Veraguas/Azuero). Posibles causas a investigar en una futura sesión:
> cobertura de GDELT sobre medios panameños es escasa, o el filtro AND-Panamá es demasiado
> estricto para cómo GDELT indexa el texto. Los 6 artículos reales del wiki son datos
> semilla manuales (2026-05-24), no fetches automáticos confirmados.
> Ventanas 2015-01-01 → 2017-03-29 (~9) faltan por completo — el loop de
> `fetch_gdelt_historical()` siempre reintenta desde `start`, así que deberían
> procesarse solas en la próxima corrida de Actions.
> El conteo de 2026 (27 ventanas) está inflado por un bug de re-marcado diario del
> trimestre en curso (ver `Estado del Fetch` arriba) — no representa 27 trimestres reales.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-08 | 0 (16/16 falsos positivos) | 0 | Causa raíz del bug de falsos positivos identificada y corregida (fetch_ddg_search domain leak); fix de crash en mark_ingested |

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
