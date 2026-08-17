---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-17
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 33 / ~45 estimadas (7 bloqueadas 403/429, resto vivas) | 45 (2015→hoy) |
| Días sin artículos nuevos | 17 (2026-07-31 → 2026-08-16) | máx 3 antes de diagnosticar — **⚠ excedido** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-16 (success, pero 0 artículos guardados)
Racha sin artículos     : 17 corridas diarias consecutivas en 0 (desde 2026-07-30)
Causas identificadas (las 4 fuentes de fetch degradadas simultáneamente):
  1. RSS (IICA, La Prensa)  : "0 entradas en el feed" — request HTTP ok, parser sin items.
                               No verificado directamente (proxy de red de esta sesión
                               bloquea egress a iica.int y prensa.com).
  2. DDG búsqueda web        : 7/8 queries oficiales (.gob.pa, oirsa.org, fao.org,
                               bancomundial.org, iica.int) → "No results found."
                               Solo site:prensa.com daba resultados, pero sin
                               restricción real de dominio → 100% falsos positivos.
  3. GDELT                   : ventanas 2015-01→2017-03 (7) bloqueadas 403/429 en
                               cada corrida (reintento diario que gasta ~6 min sin
                               progreso). Ventanas 2017-2026 (33) ya completas.
                               Ventana viva 2026-06-18→2026-08-15 responde OK con
                               0 artículos.
  4. World Bank API          : corre sin error, sin artículos nuevos detectados.

Fix aplicado esta sesión:
  - scripts/fetch_news.py::fetch_ddg_search — ahora valida que el dominio del
    resultado coincida con `site:` solicitado + aplica _is_panama_related() como
    respaldo. Elimina la fuga que causaba 100% falsos positivos en site:prensa.com.
  - scripts/ingest.py::mark_ingested — corregido AttributeError al iterar la clave
    interna _gdelt_windows (lista) como si fuera metadata de artículo.

Pendiente (no resuelto esta sesión, requiere acceso de red sin restricciones):
  - Verificar si las URLs de RSS de IICA/La Prensa cambiaron o el feed cambió de
    formato.
  - Evaluar backoff más largo para ventanas GDELT bloqueadas (evitar reintento
    diario inútil de las mismas 7 ventanas 2015-2017).
  - Revisar sintaxis de queries DDG site: para dominios .gob.pa (0 resultados en
    7/8 queries podría ser problema de sintaxis, no solo falta de contenido).
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
| 2026-08-17 | 0 (16 revisados, 16 falsos positivos) | 0 | Fix de bug DDG site: sin restricción de dominio (causa raíz de los FP) + fix mark_ingested + diagnóstico de 17 días sin fetch nuevo (RSS/DDG/GDELT degradados) |

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
