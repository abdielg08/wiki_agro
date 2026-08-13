---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-13
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 30 (7 previos + 23 hoy) | **0 nuevos** (bug corregido hoy) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 66 / ~46 estimadas | 45 (2015→hoy) — rango agotado |
| Días sin artículos nuevos reales | ≥14 (desde 2026-07-30) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-13 (corre regularmente, ver commits "chore(sources)")
Resultado               : 0 artículos REALES nuevos desde 2026-07-30 (≥14 días)
Ventanas GDELT           : 66 completadas → rango 2015→hoy AGOTADO (backfill histórico terminado)
Causa raíz identificada  : la búsqueda DDG "prensa_agro" (config/sources.yaml) traía
                            artículos NO panameños. Query original:
                            site:prensa.com agropecuario OR agricultura OR ... OR MIDA OR cosecha Panamá
                            El operador "OR" sin paréntesis anula el "site:" para los términos
                            siguientes → DDG devolvía resultados globales que solo coinciden
                            en palabras sueltas ("MIDA", "agricultura", "cosecha").
                            Ejemplos reales capturados: MIDA de Utah (Military Installation
                            Development Authority), MIDA/MITI de Malasia, agricultura de Aragón
                            (España), "Reef Saudi" (Arabia Saudita), Finep (Brasil), IEEE paper
                            genérico, UNESCO qanat persa, New York Farm Bureau, catálogo de
                            dípteros 1966. Ninguno mencionaba Panamá.
                            Además, fetch_ddg_search() (scripts/fetch_news.py) no aplicaba los
                            filtros _is_blocked_domain()/_is_panama_related() que sí usa
                            fetch_rss() — sin defensa secundaria contra el bug del query.
Fix aplicado (2026-08-13) : 1) config/sources.yaml: query reescrita con paréntesis —
                               "(agropecuario OR agricultura OR ganadería OR MIDA OR cosecha) Panamá"
                            2) scripts/fetch_news.py fetch_ddg_search(): agregados los mismos
                               filtros _is_blocked_domain()/_is_panama_related() que fetch_rss()
                            3) scripts/ingest.py mark_ingested(): bug separado corregido —
                               iteraba processed.items() crudo y crasheaba con la key interna
                               "_gdelt_windows" (lista, no dict); ahora usa article_entries()
Estado post-fix            : Pendiente validación en la próxima corrida de Actions/routine
Acción pendiente            : dado que GDELT (66 ventanas) y DDG están agotados/rotos, evaluar
                            agregar más fuentes RSS oficiales (MIDA, IDIAP, BDA no tienen RSS
                            activo — ver sources.yaml línea ~150) para sostener ~1 artículo/día hábil
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
| 2026-08-13 | 0 reales (23 falsos positivos descartados) | 0 | Los 23 pendientes eran 100% falsos positivos de la búsqueda DDG "prensa_agro" (bug de query sin paréntesis). Root cause corregido en config/sources.yaml + scripts/fetch_news.py. Bug adicional corregido en scripts/ingest.py (mark_ingested crasheaba con `_gdelt_windows`). GDELT: 66/46 ventanas — backfill histórico agotado. |

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
