---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-03
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 19 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 13 | **0 nuevos** (meta no cumplida esta sesión: +6) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 43 / 47 esperadas | 47 (2015→hoy) |
| Días sin artículos nuevos | 1 (última corrida Actions: 2026-07-02) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-02 (corrió también 06-26, 27, 28, 29)
Resultado 2026-07-02   : 1 artículo nuevo (falso positivo: "Reef Saudi", Arabia Saudita)
Causa identificada     : fetch_ddg_search() en scripts/fetch_news.py NO aplicaba los
                         filtros _is_blocked_domain()/_is_panama_related() que sí
                         tienen fetch_rss() y fetch_gdelt_historical(). Resultado:
                         13/13 artículos traídos por búsqueda DDG han sido falsos
                         positivos (Malasia, Utah, Arabia Saudita, genéricos) — 100%.
Fix aplicado (hoy)     : se agregaron ambos filtros a fetch_ddg_search()
                         (scripts/fetch_news.py). Se corrigió también
                         mark_ingested() en scripts/ingest.py, que crasheaba
                         siempre por iterar la clave interna _gdelt_windows
                         (lista) como si fuera metadata de artículo (dict).
Estado post-fix        : pendiente validar en próxima corrida Actions que
                         fetch_ddg_search() deje de producir falsos positivos.
                         Si sigue en 0% de aceptación tras el fix, considerar
                         deshabilitar `web_searches` en config/sources.yaml.
Gap GDELT identificado : ventanas 2015-01-01 → 2017-03-29 (9 ventanas) nunca se
                         han completado — ver detalle en wiki/log.md 2026-07-03.
                         No se pudo probar la GDELT API desde este sandbox
                         (proxy bloquea api.gdeltproject.org, fuera de allowlist).
```

---

## Progreso del Backfill GDELT (2015 → hoy)

Calculado comparando `sources/processed.json["_gdelt_windows"]` contra el calendario
esperado de ventanas de 90 días desde 2015-01-01 hasta hoy-1 día.

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 completo | 0/4 | **Pendiente — nunca completado** |
| 2016 completo | 0/4 | **Pendiente — nunca completado** |
| 2017 Q1 | 0/1 | **Pendiente — nunca completado** |
| 2017 Q2-Q4 → 2025 completo | 36/36 | Completo |
| 2026 (hasta 07-02) | 7/7 (con fragmentos de cola) | Completo hasta la fecha |
| **TOTAL** | **43/47** | **Backfill con hueco 2015–2017-Q1** |

> El hueco de 9 ventanas está concentrado al inicio (2015-01-01 a 2017-03-29), no
> distribuido al azar — sugiere timeout/bloqueo persistente en esas fechas
> específicas, o cobertura real más débil de GDELT para ese período (ver log.md).
> Próxima corrida de Actions debe revisarse para confirmar si esas 9 ventanas
> avanzan o siguen fallando.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-03 | 0 (6 falsos positivos descartados) | 0 | Fix de bug raíz en fetch_ddg_search() (0% aceptación en esa fuente) + fix de mark_ingested() + diagnóstico de hueco GDELT 2015-2017 Q1 |

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
