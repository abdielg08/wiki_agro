---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-06
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Falsos positivos acumulados | 12 (7 previos + 5 nuevos hoy) | **0 nuevos** |
| Pendientes de ingesta | 11 | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 62 (`_gdelt_windows` en processed.json) | 45+ (2015→hoy) — rango agotado, considerar expansión de queries |
| Días sin artículos nuevos | 0 (Actions corrió 2026-08-05, éxito) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-05T12:47:46Z (run 31007205881) — status: success
Corridas recientes     : 2026-08-01 a 2026-08-05, todas "success" (diario, cron 11:00 UTC)
Resultado               : Actions SÍ está corriendo correctamente todos los días.
                          El problema NO es que el fetch esté caído — es que produce
                          falsos positivos y pocos artículos reales nuevos.

Causa raíz identificada (2026-08-06):
  fetch_ddg_search() en scripts/fetch_news.py NO aplicaba los filtros
  _is_blocked_domain() / _is_panama_related() que sí tienen fetch_rss() y
  fetch_gdelt_batch()/fetch_gdelt_historical(). La búsqueda DDG usa
  "site:prensa.com" + query con el acrónimo "MIDA" (config/sources.yaml:160),
  pero el backend de DDG no respeta el filtro site: de forma confiable —
  regresó resultados de paultan.org (Malaysia MITI/MIDA), sltrib.com (Utah,
  Military Installation Development Authority = MIDA) y msn.com, todos
  etiquetados incorrectamente con source="prensa.com", country="PA",
  language="es" porque fetch_ddg_search() hardcodea esos campos.
  is_agro_relevant() solo compara contra search_terms (incluye "MIDA" como
  término suelto, sin desambiguar), así que estos artículos pasaron el
  único filtro que sí se aplicaba.

Fix aplicado (2026-08-06) : scripts/fetch_news.py fetch_ddg_search() ahora
  aplica _is_blocked_domain(url) y _is_panama_related(title, url) igual que
  fetch_rss() y fetch_gdelt_batch(). Ver wiki/log.md 2026-08-06 para detalle.
Estado post-fix            : Pendiente validación en próxima corrida Actions (11:00 UTC).
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 | 0/4 | ? | **Pendiente — hueco real, no cubierto aún** |
| 2016 | 0/4 | ? | **Pendiente — hueco real, no cubierto aún** |
| 2017 | 4/4 | ? | Completado |
| 2018 | 4/4 | ? | Completado |
| 2019 | 4/4 | ? | Completado |
| 2020 | 4/4 | ? | Completado |
| 2021 | 4/4 | ? | Completado |
| 2022 | 4/4 | ? | Completado |
| 2023 | 4/4 | ? | Completado |
| 2024 | 4/4 | ? | Completado |
| 2025 | 4/4 | ? | Completado |
| 2026 | 26 ventanas (irregulares, se solapan) | ? | En curso |
| **TOTAL** | **62 ventanas en `_gdelt_windows`** | — | **2015-2016 son el hueco pendiente; 2017-2025 ya cubiertos por trimestre** |

> Fuente: conteo real de `sources/processed.json["_gdelt_windows"]` (2026-08-06).
> 2026 tiene 26 ventanas registradas en vez de ~2-3 trimestrales — sugiere que el
> fetch diario (wiki_daily.yml) está generando/registrando ventanas propias que se
> solapan con las del backfill histórico (wiki_historical.yml). Revisar si ambos
> workflows comparten el mismo namespace de ventanas sin necesidad.
> Próximo paso de backfill: correr `wiki_historical.yml` (workflow_dispatch) apuntado
> a 2015-2016 para cerrar el hueco real de cobertura.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-06 | 0 (5/5 procesados eran falsos positivos, 0% ingestados al wiki) | 11 | Root cause identificado: fetch_ddg_search() sin filtro Panama/dominio → fix aplicado en scripts/fetch_news.py. Ver wiki/log.md. |

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
