---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-23
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 30 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 24 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 73 / ~46 estimadas | 46 (2015→hoy) |
| Días sin artículos nuevos reales | ≥5 (desde 2026-05-24) | máx 3 antes de diagnosticar |

**Pendientes de ingesta: 0** (los 17 pendientes al inicio de la sesión 2026-08-23 eran
falsos positivos; ver `wiki/log.md` para el detalle y el diagnóstico de causa raíz).

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-22 (commit "0 artículos nuevos")
Resultado               : 24/30 artículos históricos acumulados son falsos positivos (80%)
Causa raíz identificada : scripts/fetch_news.py::fetch_ddg_search() arma la consulta como
                          "site:{site} ..." pero ddgs.news() no respeta ese filtro de forma
                          confiable — devuelve resultados de dominios ajenos (thestar.com.my,
                          sltrib.com, heraldo.es, nyfb.org, spa.gov.sa, agenciabrasil.ebc.com.br,
                          whc.unesco.org, paultan.org, msn.com, maine.gov) y el código los
                          etiquetaba igual como fuente "prensa.com" sin validar el dominio.
                          Además, is_agro_relevant() aceptaba cualquier término genérico
                          ("MIDA", "agricultura", "riego") sin exigir contexto de Panamá,
                          por lo que "MIDA" (Malasia/Utah) colaba sistemáticamente.
Fix aplicado             : fetch_ddg_search() ahora descarta resultados cuyo dominio real
                          (urlparse(url).netloc) no contenga el site configurado.
                          mark_all_ingested() corregido para usar la misma prioritize()
                          que run_prepare()/ingest (antes usaba find_pending() crudo,
                          un orden distinto — arriesgaba marcar como ingestados artículos
                          reales que Claude nunca procesó).
                          mark_ingested() corregido: crasheaba al iterar la clave
                          _gdelt_windows (lista) de processed.json como si fuera dict.
Estado post-fix          : Pendiente validación en próxima corrida de GitHub Actions —
                          debería reducir drásticamente el ruido de falsos positivos.
                          El backfill GDELT (73 ventanas completadas, ya supera el
                          estimado) no ha aportado artículos reales adicionales — requiere
                          revisión separada de fetch_gdelt_historical() en próxima sesión.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | 0 | **Pendiente — nunca corrido** |
| 2016 Q1-Q4 | 0/4 | 0 | **Pendiente — nunca corrido** |
| 2017 Q1-Q4 | 4/4 | 0 reales | Completo, sin artículos reales |
| 2018 Q1-Q4 | 4/4 | 1 real (gusano cogollero, semilla) | Completo |
| 2019 Q1-Q4 | 4/4 | 0 reales | Completo, sin artículos reales |
| 2020 Q1-Q4 | 4/4 | 0 reales | Completo, sin artículos reales |
| 2021 Q1-Q4 | 4/4 | 0 reales | Completo, sin artículos reales |
| 2022 Q1-Q4 | 4/4 | 0 reales | Completo, sin artículos reales |
| 2023 Q1-Q4 | 4/4 | 0 reales | Completo, sin artículos reales |
| 2024 Q1-Q4 | 4/4 | 0 reales | Completo, sin artículos reales |
| 2025 Q1-Q4 | 4/4 | 0 reales | Completo, sin artículos reales |
| 2026 | 37 (repetidas) | 0 reales | Re-corriendo ventanas de 2026 en vez de avanzar a 2015-2016 |
| **TOTAL** | **73 ventanas** | **1 real (vía GDELT) + 24 falsos positivos** | **2015-2016 sin cubrir; el resto solo produjo falsos positivos** |

**Diagnóstico (2026-08-23)**: las ventanas de 2015-2016 nunca se han ejecutado, mientras
que 2026 acumula 37 ventanas repetidas — la lógica de generación de ventanas en
`scripts/fetch_historical.py` no está avanzando sistemáticamente hacia atrás en el tiempo.
Además, de las 73 ventanas completadas, prácticamente ninguna produjo un artículo real de
Panamá (el único hallazgo real, 2018, es dato semilla manual, no confirmado como
proveniente de GDELT). Pendiente investigar `fetch_gdelt_historical()` en una próxima
sesión para corregir el orden de avance del backfill y revisar por qué la tasa de
artículos reales por ventana es ~0.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-23 | 0 al wiki (12 falsos positivos marcados) | 0 | Auditoría completa: 24/30 históricos son FP; fix de causa raíz en fetch_ddg_search() (validación de dominio); fix de mark_all_ingested() (orden de prioridad inconsistente con ingest); fix de mark_ingested() (crash en _gdelt_windows) |

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

**Activada 2026-08-23**: ≥5 días sin artículos reales nuevos (solo falsos positivos desde
2026-05-24). Diagnóstico y fix de causa raíz documentados arriba y en `wiki/log.md`.
Pendiente de validar en la próxima corrida de GitHub Actions.
