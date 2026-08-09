---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-09
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 (+16 hoy) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 63 | 45 (2015→hoy) — **rango agotado, ver diagnóstico** |
| Días sin artículos nuevos | 2 (última corrida 2026-08-07) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-07 (0 artículos nuevos; commits previos 08-04, 08-02 también en 0)
Ventanas GDELT completadas : 63 → supera el umbral de 45 de CLAUDE.md: el rango de fechas
                         2015-02-19→hoy está efectivamente agotado para GDELT. Backfill
                         histórico vía GDELT ya no es la fuente principal de artículos nuevos;
                         depender más de RSS (La Prensa, IICA) y de la búsqueda DDG corregida.

Causa raíz identificada hoy (2026-08-09) — contaminación total de la cola de ingesta:
  Los 16 artículos pendientes al inicio de esta sesión eran 100% falsos positivos
  (0 sobre agro de Panamá). Todos venían de la búsqueda DDG `site:prensa.com` en
  fetch_ddg_search() (scripts/fetch_news.py), que:
    1. No aplicaba los guards `_is_blocked_domain()` / `_is_panama_related()` que sí
       tienen fetch_rss() y fetch_gdelt_batch() — solo filtraba por keyword suelta
       (ej. "MIDA"), causando colisión de acrónimo (Panamá / Malaysia Investment
       Development Authority / Utah Military Installation Development Authority).
    2. El operador `site:prensa.com` de DDGS no se respeta de forma confiable — los
       resultados venían de paultan.org, sltrib.com, heraldo.es (Aragón/España),
       agenciabrasil.ebc.com.br, spa.gov.sa, whc.unesco.org, nyfb.org, ieeexplore.ieee.org
       y archive.org — ningún dominio de prensa.com.
  FIX aplicado (commit de esta sesión): se agregaron los mismos guards a
  fetch_ddg_search(). Los 16 falsos positivos se marcaron ingested=true (revisados/
  descartados) para no reaparecer en la cola; 0 se agregaron al wiki.

  Bug adicional encontrado y corregido: mark_all_ingested() usaba un orden
  (find_pending, orden de filesystem) distinto al de ingest --limit N (prioritize,
  orden por score), por lo que `mark-all-ingested --limit 5` marcaba 5 artículos
  DIFERENTES a los 5 realmente revisados por Claude Code — incluyendo artículos
  nunca leídos, sin ninguna verificación humana/LLM. Corregido para usar el mismo
  orden de prioridad. También se corrigió un crash en mark_ingested() (iteraba
  processed.items() sin filtrar la clave interna _gdelt_windows, que es una lista).

Estado post-fix         : cola de ingesta en 0 pendientes. Próxima corrida de fetch
                         (RSS/DDG) debería producir candidatos más limpios gracias al
                         fix de fetch_ddg_search(). Validar en próxima sesión.
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
| 2026-08-09 | 0 (16 falsos positivos descartados) | 0 | Cola 100% contaminada por bug en fetch_ddg_search() (sin guards Panamá) — fix aplicado; también corregido bug de orden en mark_all_ingested() y crash en mark_ingested() |

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
