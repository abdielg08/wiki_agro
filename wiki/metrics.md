---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-16
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 22 | ↑ continuo |
| Artículos reales ingestados (con página wiki) | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 16 (7 previos + 9 esta sesión) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 49 / ~46 estimadas | 45 (2015→hoy) |
| Días sin artículos nuevos | 0 (último fetch: 2026-07-15) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-15 (1 artículo nuevo); sin corrida registrada aún
                         hoy 2026-07-16 al momento de esta sesión (08:05 UTC)
Resultado               : 9/9 artículos recibidos en esta y la sesión anterior
                          reciente resultaron ser falsos positivos (0 incorporados al wiki)
Causa raíz identificada : fetch_ddg_search() (búsqueda DDG "prensa_agro" en
                          config/sources.yaml) no aplicaba los filtros
                          _is_blocked_domain()/_is_panama_related() que sí usan
                          los fetchers de RSS y GDELT. Coincidencias genéricas con
                          "MIDA"/"agricultura"/"agriculture" traían artículos de
                          Malasia, Utah, Irán, Arabia Saudita y EE.UU. sin relación
                          con Panamá.
Fix aplicado (sesión 2026-07-16): fetch_ddg_search() ahora exige
                          _is_panama_related(title, url), descarta
                          _is_blocked_domain(url), y usa el dominio real de la URL
                          como "source" (antes se hardcodeaba a "prensa.com").
                          También se corrigió mark_ingested() en scripts/ingest.py,
                          que fallaba (AttributeError) al iterar la clave de
                          metadatos "_gdelt_windows" (una lista) como si fuera dict.
Ventanas GDELT           : 49 completadas (>= 45) → rango de fechas agotado según
                          umbral definido en CLAUDE.md. El backfill vía GDELT ya
                          cubre aprox. 2017-03-30 → 2026-07-14; falta expandir el
                          rango histórico 2015-02-19 → 2017-03-29 (ejecutar
                          workflow "Wiki Agropecuario — Crawl Histórico 15 Años"
                          manualmente con years=2015-2017) para completar la
                          cobertura objetivo.
Estado post-fix         : Pendiente validar en la próxima corrida de Actions que
                          ya no se generen falsos positivos vía DDG search.
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
| 2024 Q1-Q4 | ~4/4 | ? | Completo (vía fetch diario) |
| 2025 Q1-Q4 | ~4/4 | ? | Completo (vía fetch diario) |
| 2026 Q1-Q3 | ~4/3 | ? | Completo (vía fetch diario) |
| **TOTAL** | **49/46** | **~13 reales (resto FP)** | **2017-03 → hoy cubierto; falta 2015-02-19 → 2017-03-29** |

> El fetch diario (wiki_daily.yml) viene generando ventanas GDELT rodantes que ya cubren
> 2017-03-30 → 2026-07-14 (49 ventanas). Falta disparar manualmente el workflow
> "Wiki Agropecuario — Crawl Histórico 15 Años" con years=2015-2017 para cerrar el
> tramo más antiguo de la cobertura objetivo (2015-02-19 en adelante).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-16 | 0 (9 revisados, 9 falsos positivos) | 0 | Fix de bug raíz en fetch_ddg_search() (sin filtro Panamá) + fix de mark_ingested() (AttributeError en `_gdelt_windows`) |

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
