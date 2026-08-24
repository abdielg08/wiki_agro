---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-24
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 30 | ↑ continuo |
| Artículos reales ingestados | 30 (6 semilla + 24 evaluados, 0% con contenido de agro-Panamá válido nuevo hoy) | = total sin falsos positivos |
| Falsos positivos acumulados | 24 (7 previos + 17 nuevos hoy) | **0 nuevos** ⚠️ ver diagnóstico |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 73 / ~46 estimadas | rango agotado — ver diagnóstico |
| Días sin artículos nuevos | 5 (último real: 2026-08-19) | máx 3 antes de diagnosticar — **⚠️ EXCEDIDO** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions        : 2026-08-22 (0 artículos nuevos; sin corrida detectada 08-23/08-24)
Último artículo real nuevo    : 2026-08-19 (1 artículo) → 5 días sin artículos nuevos, EXCEDE el umbral de 3
Ventanas GDELT completadas    : 73 (más de las ~46 estimadas para 2015→hoy) → rango histórico agotado
                                 vía este método; nueva cobertura debe venir de RSS/DDG diarios, no de
                                 más ventanas GDELT.

CAUSA RAÍZ DE LOS FALSOS POSITIVOS (sesión 2026-08-24, ver wiki/log.md 00:00 y 08:45):
  17 de 17 artículos pendientes evaluados hoy eran falsos positivos, todos con
  `source: "prensa.com"` incorrecto. Causa real: `fetch_news.py::fetch_ddg_search`
  arma `site:prensa.com <query>` para DuckDuckGo pero nunca valida que la URL
  devuelta pertenezca de verdad a prensa.com — el operador `site:` de la librería
  `ddgs` no es 100% confiable. Resultado: artículos de sltrib.com, paultan.org,
  heraldo.es, maine.gov, nyfb.org, spa.gov.sa, ieeexplore.org, archive.org,
  whc.unesco.org y agenciabrasil.ebc.com.br quedaron etiquetados como si fueran
  de La Prensa (fuente Nivel 3 de confianza), y colisionaron además con el
  acrónimo "MIDA" (Malaysia/Utah) en el scoring de prioridad.
  Bug secundario (mismo síntoma, ruta distinta): `fetch_historical.py::fetch_gdelt_window`
  tampoco exigía mención de Panamá ni filtraba dominios bloqueados.

FIX APLICADO ESTA SESIÓN (scripts/fetch_news.py y scripts/fetch_historical.py):
  1. fetch_ddg_search(): verifica que el dominio de la URL devuelta termine en
     `site` antes de aceptarla; agrega `_is_blocked_domain()`.
  2. fetch_gdelt_window(): ahora exige mención de Panamá en la query
     (`_AGRO_QUERY_PA`) y filtra con `_is_blocked_domain()` + `_is_panama_related()`.
  3. fetch_cdx_domain(): agrega `_is_blocked_domain()` como red de seguridad.
  4. ingest.py::mark_all_ingested(): ahora usa el mismo orden por score
     (`prioritize()`) que `run_prepare()` — antes marcaba un conjunto de
     artículos distinto al que realmente se le mostraba a Claude para revisar
     (ver wiki/log.md 08:19), causando que artículos nunca revisados quedaran
     marcados "ingested" sin pasar por el filtro de falso positivo.
Estado post-fix                : pendiente validación en la próxima corrida de
                                  GitHub Actions / próxima sesión de ingest.

SIGUIENTE DIAGNÓSTICO NECESARIO (para la próxima routine):
  Confirmar si GitHub Actions corrió el 2026-08-23 y 2026-08-24 (revisar el
  workflow en GitHub, no visible desde este repo local). Si no corrió, el
  problema es de scheduling/CI, no de las fuentes de datos.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

> Datos reales tomados de `sources/processed.json::_gdelt_windows` el 2026-08-24
> (73 ventanas registradas como completas en total).

| Período | Ventanas completas | Estado |
|---------|---------------------|--------|
| 2015 | 0/4 | **Pendiente — sin cubrir** |
| 2016 | 0/4 | **Pendiente — sin cubrir** |
| 2017 | 4/4 | Completo |
| 2018 | 4/4 | Completo |
| 2019 | 4/4 | Completo |
| 2020 | 4/4 | Completo |
| 2021 | 4/4 | Completo |
| 2022 | 4/4 | Completo |
| 2023 | 4/4 | Completo |
| 2024 | 4/4 | Completo |
| 2025 | 4/4 | Completo |
| 2026 | 37 (anómalo — ver nota) | Ver nota |
| **TOTAL** | **73** | Ver hallazgos |

**Hallazgos**:
1. **Gap real de cobertura 2015-2016**: nunca se corrió `fetch-historical` para
   estos años (0 ventanas). El objetivo de CLAUDE.md es cobertura desde
   2015-02-19 — falta ejecutar `python scripts/fetch_historical.py --years 2015-2016 --mode gdelt`
   (con el filtro de Panamá ya corregido esta sesión).
2. **2026 tiene 37 ventanas registradas** en vez de las ~2-3 esperadas para un
   año en curso — indica que `fetch_gdelt_years` corrió varias veces con
   rangos de fecha distintos/traslapados, generando claves de ventana
   duplicadas en vez de reutilizar las mismas. No se investigó a fondo esta
   sesión; queda como diagnóstico pendiente para una futura routine.
3. Del total de artículos descargados hasta hoy vía este pipeline histórico
   (24 bajo `source: prensa.com`), **17 resultaron falsos positivos** (ver
   diagnóstico arriba) — es decir, el backfill 2017-2025 vía GDELT/DDG
   produjo muy poca señal real hasta ahora. Con el fix de filtrado aplicado
   hoy, no se recomienda re-correr las ventanas ya completas (desperdicia
   cuota de API); el fix aplica a artículos nuevos hacia adelante.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-24 | 0 (17/17 evaluados eran falsos positivos) | 0 | Fix de causa raíz: `fetch_ddg_search` no validaba dominio real de resultados DDG; `mark_all_ingested` no usaba el mismo orden que `run_prepare`. Ver wiki/log.md. |

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
