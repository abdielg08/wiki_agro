---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-26
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados (en wiki) | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 18 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal real (artículos reales) | 2015-2024 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 37 (limpiadas de 55) / ~39 estimadas hasta hoy | 39-40 (2015→hoy) |
| Días sin artículos nuevos | 3 (2026-07-23 a 07-25) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-25 (SÍ está corriendo diariamente)
Resultado               : 0 artículos nuevos ingestados al wiki en 3+ corridas seguidas
Causa identificada (nueva, 2026-07-26):
  1. web_searches.prensa_agro (config/sources.yaml) tenía la query
     "site:prensa.com agropecuario OR agricultura OR ganadería OR MIDA OR cosecha Panamá"
     SIN paréntesis. El operador OR sin agrupar rompe el site:, así que DDG devolvía
     resultados de CUALQUIER dominio que mencionara alguno de esos términos sueltos
     (Utah "MIDA" = Military Installation Development Authority, Malasia MITI/MIDA,
     Arabia Saudita, Irán, EE.UU., papers IEEE, catálogos de zoología, etc.)
     → 18/18 artículos de la fuente "prensa.com" en sources/ resultaron ser
     falsos positivos (100% de esa fuente).
  2. fetch_ddg_search() no aplicaba el filtro _is_panama_related()/_is_blocked_domain()
     como respaldo, a diferencia de fetch_rss() y fetch_gdelt_batch().
  3. Bug independiente en scripts/ingest.py: mark_ingested() iteraba processed.items()
     sin excluir la clave interna "_gdelt_windows" (una lista), lo que lanzaba
     AttributeError antes de poder marcar cualquier artículo como procesado.
  4. Bug independiente en fetch_gdelt_historical(): la ventana final (parcial, con
     end = ayer) se marcaba "completa" cada corrida con una clave nueva cada día
     (20260618_20260623, _20260624, _20260626, ...) porque `end` crece un día por
     corrida — nunca cerraba una ventana real de 90 días y solo inflaba el conteo
     de ventanas sin aportar cobertura real. Se limpiaron 18 claves basura de
     sources/processed.json (_gdelt_windows bajó de 55 a 37 ventanas genuinas).
Fixes aplicados (2026-07-26):
  - config/sources.yaml: query de prensa_agro reescrita con paréntesis
  - scripts/fetch_news.py: fetch_ddg_search() ahora filtra dominio + relación con Panamá;
    fetch_gdelt_historical() ya no marca como completa una ventana parcial/creciente
  - scripts/ingest.py: mark_ingested() usa article_entries() para excluir claves internas
  - sources/processed.json: _gdelt_windows limpiado (55 → 37 ventanas genuinas)
Estado post-fix         : Pendiente validación en la próxima corrida de Actions —
                          debería empezar a traer artículos reales de agro panameño
                          en vez de ruido de dominios no relacionados.
Gap detectado (sin resolver): las ventanas GDELT completadas empiezan en 2017-03-30;
  no hay ninguna ventana marcada para 2015-2016 (~8 trimestres). No está claro si
  GDELT no tiene resultados para esos trimestres o si nunca se intentaron por
  errores de red no persistidos. A investigar en próxima sesión.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas completadas | Estado |
|---------|----------------------|--------|
| 2015 | 0/4 | **Pendiente — gap sin explicar, ver diagnóstico arriba** |
| 2016 | 0/4 | **Pendiente — gap sin explicar, ver diagnóstico arriba** |
| 2017 (desde marzo) | 4/4 | Completo |
| 2018 | 4/4 | Completo |
| 2019 | 4/4 | Completo |
| 2020 | 4/4 | Completo |
| 2021 | 4/4 | Completo |
| 2022 | 4/4 | Completo |
| 2023 | 4/4 | Completo |
| 2024 | 4/4 | Completo |
| 2025 | 4/4 | Completo |
| 2026 (hasta 2026-06-17) | 1/1 | Completo |
| 2026-06-18 → hoy | 0/1 | Ventana abierta (parcial, se re-consulta cada corrida hasta llegar a 90 días) |
| **TOTAL** | **37 ventanas genuinas** (2017-03 → 2026-06) | **GDELT no aporta artículos reales de agro — 0 de las 24 en sources/ vienen de gdelt=true** |

> Nota: los artículos GDELT descargados no pasaron el filtro `is_agro_relevant`/panamá en
> ninguna ventana hasta ahora (0 artículos con `"gdelt": true` en sources/articles/), o
> simplemente no hay cobertura de medios panameños en GDELT para agro. A confirmar
> revisando los logs de Actions de próximas corridas.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-26 | 0 reales / 11 falsos positivos revisados | 0 | Root-cause del bug de query DDG (site: roto por OR sin paréntesis) + fix de fetch_ddg_search, fetch_gdelt_historical y mark_ingested + limpieza de _gdelt_windows (55→37) |

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
