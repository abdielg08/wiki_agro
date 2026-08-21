---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-21
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 30 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 24 (7 previos + 17 esta sesión) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 71 | 45+ (rango 2015→hoy agotado) |
| Días sin artículos nuevos | 1 (último real: 2026-08-19) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions  : 2026-08-20 (0 artículos nuevos)
Último día con artículos: 2026-08-19 (1 artículo)
Ventanas GDELT          : 71 completadas — supera el umbral de 45 →
                           el rango de fechas GDELT (2015 → hoy) ya está
                           agotado. Nuevos artículos futuros dependerán casi
                           exclusivamente de RSS (IICA, La Prensa) y de la
                           fuente de búsqueda "prensa.com" (ver hallazgo abajo).

Hallazgo crítico (2026-08-21): la fuente "prensa.com" (scripts/fetch_news.py,
                           búsqueda DDG con site:prensa.com) tiene una tasa
                           de falsos positivos del 100% observada: se
                           revisaron 17/17 artículos pendientes de esta
                           fuente en la sesión de hoy y NINGUNO trataba
                           sobre Panamá — son resultados globales (España,
                           Utah, Brasil, Irán, Arabia Saudita, etc.) que
                           solo coinciden en palabras clave genéricas como
                           "agriculture" o "MIDA". De los 24 artículos
                           acumulados bajo "prensa.com", 0 han producido
                           jamás contenido real en wiki/summaries/. El
                           filtro `site:` no funciona con `ddgs.news()`.
                           Detalle completo en wiki/log.md (2026-08-21 00:45).

Bug de tooling corregido: mark-all-ingested/mark-ingested en
                           scripts/ingest.py no coincidían con el orden de
                           `ingest` y además crasheaban con la clave
                           interna `_gdelt_windows`. Corregido — ver
                           wiki/log.md (2026-08-21 00:30).

Estado post-fix         : cola de pendientes en 0. Pendiente que un humano
                           revise/reescriba la búsqueda de la fuente
                           "prensa.com" — fuera del alcance de esta rutina.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | 0 | **Pendiente — sin cubrir** |
| 2016 Q1-Q4 | 0/4 | 0 | **Pendiente — sin cubrir** |
| 2017 Q1-Q4 | 4/4 | ? | Completado |
| 2018 Q1-Q4 | 4/4 | ? | Completado |
| 2019 Q1-Q4 | 4/4 | ? | Completado |
| 2020 Q1-Q4 | 4/4 | ? | Completado |
| 2021 Q1-Q4 | 4/4 | ? | Completado |
| 2022 Q1-Q4 | 4/4 | ? | Completado |
| 2023 Q1-Q4 | 4/4 | ? | Completado |
| 2024 Q1-Q4 | 4/4 | ? | Completado |
| 2025 Q1-Q4 | 4/4 | ? | Completado |
| 2026 Q1-Q2 | 35/2 | ? | En progreso (ver nota) |
| **TOTAL** | **71/46** | **30** | **2015-2016 sin cubrir; resto completado** |

> Datos reales extraídos de `_gdelt_windows` en `sources/processed.json` (71 ventanas,
> agrupadas por trimestre de fecha de inicio) el 2026-08-21.
>
> **Hallazgo**: 2015 y 2016 tienen **0 ventanas** — el backfill nunca cubrió el inicio
> del rango objetivo (2015-02-19). 2017-2025 están completos (4/4 ventanas cada año).
> 2026 Q2 muestra 34 ventanas (vs. ~1 esperada) — probablemente ventanas pequeñas o
> solapadas por reintentos, no una cobertura trimestral limpia; no se investigó a
> fondo esta sesión. **Recomendación**: priorizar backfill de 2015-2016 en la próxima
> corrida (`python wiki_agro.py fetch-historical --domain prensa.com --years 2015-2016`
> o equivalente) antes de seguir expandiendo 2026.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-21 | 0 reales | 0 | 17 falsos positivos rechazados (5+12), 0% ingestados; bug fix en `mark-all-ingested`/`mark-ingested` (scripts/ingest.py); hallazgo: fuente "prensa.com" 100% falsos positivos; 2015-2016 sin cubrir en backfill GDELT |

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
