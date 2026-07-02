---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-02
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 18 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 12 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 42 / ~46 estimadas | 46 (2015→hoy) |
| Días sin artículos nuevos | 3 (2026-06-30, 07-01, 07-02) | máx 3 antes de diagnosticar — **ALERTA activa** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions   : 2026-07-01 13:31 UTC (run 28521328453) — completed/success, pero 0 artículos
Corridas previas         : 2026-06-30 (run 28446473296) también 0 artículos
Última vez con artículos : 2026-06-29 (1 artículo nuevo)

Diagnóstico (Actions SÍ corre, todos los días, con éxito "success" — el problema
es que las 3 fuentes de descarga están fallando simultáneamente):
  1. RSS (IICA, La Prensa)  → 0 entradas en ambos feeds (feeds vacíos o URLs rotas)
  2. Búsqueda Web (DDG)     → "No results found" en las 7 queries configuradas
                              (mida_noticias, idiap_investigacion, bda_credito,
                              fao_panama, banco_mundial_pa, iica_panama, oirsa_alertas)
                              → ddgs probablemente rate-limited/bloqueado desde IPs de GH Actions
  3. GDELT histórico        → 42/46 ventanas ya completadas (skip). Las 4 ventanas
                              restantes (2015 completo + la ventana actual 2026-06-18→06-30)
                              fallan con "GET blocked (403/429)" o timeout de conexión/lectura
                              → confirma diagnóstico de CLAUDE.md: GDELT bloqueado/timeout
                              (menos de 45 ventanas completadas)

Causa raíz              : GDELT sigue bloqueando/limitando IPs de GitHub Actions para las
                           ventanas pendientes; RSS feeds configurados ya no devuelven
                           entradas; DDG (ddgs) no devuelve resultados para ninguna query.
Recomendación            : (a) revisar si las URLs de RSS IICA/La Prensa siguen vigentes,
                           (b) probar ddgs con backoff/rotación de user-agent o alternativa
                           a DuckDuckGo, (c) para GDELT, reintentar con backoff mayor o
                           reducir frecuencia de requests por corrida.
Estado                   : Pendiente de intervención — no requiere acción del LLM en la
                           sesión de ingesta (es un problema de scripts/fetch, no de datos).
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 (4 ventanas ~trimestrales) | 0/4 | **Bloqueado** — GDELT devuelve 403/429/timeout en cada corrida |
| 2016 (4 ventanas ~trimestrales) | 0/4 | **Bloqueado** — mismo motivo |
| 2017 | 4/4 | Completo |
| 2018 | 4/4 | Completo |
| 2019 | 4/4 | Completo |
| 2020 | 4/4 | Completo |
| 2021 | 4/4 | Completo |
| 2022 | 4/4 | Completo |
| 2023 | 4/4 | Completo |
| 2024 | 4/4 | Completo |
| 2025 | 4/4 | Completo |
| 2026 (hasta 2026-06-30) | 6/6 | Completo — ventana actual (2026-06-18→06-30) no trae artículos nuevos por bloqueo GDELT |
| **TOTAL** | **42/46** | **2015-2016 pendientes por bloqueo de GDELT desde IPs de GitHub Actions** |

> 0 artículos guardados de GDELT en las últimas 2 corridas (2026-06-30, 2026-07-01) — todas las
> ventanas nuevas (2015-2016 + ventana actual) fallaron con 403/429 o timeout de conexión/lectura.
> Las 42 ventanas ya completadas se saltan correctamente (no vuelven a pedirse).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-02 | 0 | 0 | 5 artículos revisados, los 5 falsos positivos (Utah data centers, NY Farm Bureau, Reef Saudi) — 0% falsos positivos ingestados. Diagnóstico: RSS/DDG/GDELT fallando simultáneamente desde IPs de Actions (ver Estado del Fetch). BUGFIX en scripts/ingest.py `mark_ingested()`. |

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
