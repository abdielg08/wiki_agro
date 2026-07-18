---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-18
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 22 | ↑ continuo |
| Artículos reales ingestados | 13 | = total sin falsos positivos |
| Falsos positivos acumulados | 16 (7 previos + 9 nuevos 2026-07-18) | **0 nuevos** — ver diagnóstico abajo |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + backfill parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 49 / ~46 estimadas | backfill histórico esencialmente completo |
| Días sin artículos nuevos en sources/ | 3 (2026-07-16, 17, 18 — el fetch de hoy aún no corre) | máx 3 antes de diagnosticar → **ALERTA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions       : 2026-07-17 12:02 UTC (schedule) — conclusion: success (pero 0 artículos)
Última corrida CON artículos : 2026-07-15 (commit 5f4d667, 1 artículo)
Runs recientes (actions_list): 07-17 success/0, 07-16 success/0, 07-15 success/1,
                                07-14 success, 07-13 FAILURE, 07-12..07-03 success
Causa identificada (logs job 87879498680, run 29578858522, 2026-07-17):
  1. GDELT API devuelve "GET blocked (403/429)" o "error de red" en CASI TODAS las
     ventanas intentadas — incluyendo la ventana incremental más reciente
     (2026-06-18 → 2026-07-16), que es la que traería noticias nuevas de Panamá.
     No es agotamiento de rango (ver ventanas completadas abajo) — es bloqueo/
     rate-limit activo del runner IP de GitHub Actions contra api.gdeltproject.org.
  2. RSS: IICA (0 entradas) y La Prensa (0 entradas) ese día — feeds vacíos, no error.
  3. DDG: 7 de 8 búsquedas "site:X ..." devuelven "No results found" (probablemente
     normal / sin novedades). Solo "prensa_agro" (site:prensa.com) devuelve resultados,
     y el bug de fetch_ddg_search() (ver wiki/log.md 2026-07-18 01:20) permitía que
     colaran resultados fuera de dominio/tema — YA CORREGIDO en este commit.
Backfill histórico          : 49 ventanas GDELT trimestrales completadas — cubre
                               ~2015-2026 casi en su totalidad. El backfill masivo
                               está esencialmente terminado; el problema activo es
                               la ventana incremental diaria bloqueada por GDELT.
Acción recomendada           : GDELT bloquea por IP/rate-limit, no por código —
                               no hay fix de código disponible desde esta sesión.
                               Monitorear próximas corridas; si persiste >5-7 días
                               considerar backoff/retry más largo en fetch_gdelt_window()
                               o reducir frecuencia de la ventana incremental.
Fix de código aplicado hoy   : scripts/fetch_news.py fetch_ddg_search() ahora aplica
                               _is_blocked_domain()/_is_panama_related() (paridad con
                               fetch_rss()) — evita que resultados DDG fuera de tema/
                               dominio entren al pipeline. scripts/ingest.py corregido
                               para que mark-all-ingested marque exactamente el batch
                               mostrado a Claude (ver wiki/log.md).
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
| 2026-07-18 | 0 (9/9 falsos positivos, 0 páginas creadas) | 0 | Bug de mark-all-ingested corregido (marcaba artículo incorrecto); fix de fetch_ddg_search() sin filtro Panamá; diagnóstico: GDELT bloqueado (403/429) en runner de Actions, 3 días sin artículos nuevos |

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
