---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-21
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 18 | **0 nuevos** (ver nota) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 52 registradas, pero cobertura real inicia 2017-03-30 | 2015-02-19 → hoy |
| Días sin artículos nuevos | 1 (2026-07-21, ver commits) | máx 3 antes de diagnosticar |

> Nota falsos positivos: los 18 acumulados son todos artículos correctamente
> DESCARTADOS (no ingestados al wiki) — la meta "0 nuevos" se refiere a no
> ingestar contenido incorrecto al wiki, no a evitar que el fetch traiga
> ruido. El fetch SÍ sigue trayendo ruido (ver diagnóstico abajo) — eso es
> lo que hay que arreglar, no el proceso de descarte manual.

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con contenido : 2026-07-20 (2 artículos nuevos)
Última corrida (hoy)         : 2026-07-21 (0 artículos nuevos) — Actions SÍ corrió
                                (commit e1fd563 "0 artículos nuevos descargados [skip ci]")
Actions está corriendo diariamente de forma consistente (ver git log de sources/).

PROBLEMA 1 — Ruido en la fuente "prensa.com" (11 falsos positivos esta sesión, 100% del lote):
  Causa raíz A: colisión de la sigla "MIDA" — trae artículos sobre Malaysian
    Investment Development Authority (Malasia) y Military Installation
    Development Authority (Utah, EE.UU.), ninguno relacionado a Panamá.
  Causa raíz B: keyword "agriculture" genérico sin filtro de país — trae
    artículos de agro de Irán (qanats), EE.UU. (NY Farm Bureau), Arabia
    Saudita (Reef Saudi), papers IEEE genéricos, catálogos de archive.org.
  Ninguno de los 24 artículos en sources/articles/ atribuidos a "prensa.com"
  parece venir de prensa.com (nombres de archivo referencian paultan.org,
  sltrib.com, msn.com, whc.unesco.org, nyfb.org, spa.gov.sa, archive.org,
  ieeexplore.ieee.org) — el label de fuente "prensa.com" no coincide con
  el dominio real del artículo. Sugiere que la búsqueda/fetch está mal
  etiquetada o usando un motor de búsqueda genérico (ver ddgs en
  requirements.txt) sin restringir dominio ni país.
  RECOMENDACIÓN: revisar scripts/fetch.py (o equivalente) — agregar filtro
  de relevancia Panamá (dominio .pa, o texto que contenga "Panamá"/
  "panameño") ANTES de guardar en sources/articles/, para no seguir
  generando falsos positivos que consumen cupo de ingesta cada sesión.

PROBLEMA 2 — Gap de cobertura histórica 2015-02-19 → 2017-03-29 (~2 años):
  _gdelt_windows tiene 52 entradas, pero la más antigua inicia en
  2017-03-30. El objetivo de cobertura (CLAUDE.md) es 2015-02-19 → hoy.
  Las primeras ~8 ventanas trimestrales (2015-2017) nunca se procesaron —
  no aparecen ni como completadas ni parecen haberse reintentado.
  Las últimas 15 entradas de _gdelt_windows son ventanas diarias con
  start=20260618 fijo y end creciente día a día (20260623 → 20260720),
  no ventanas trimestrales — son parte del fetch incremental normal, no
  del backfill histórico. Es decir: de las 52 entradas, solo 37 son
  ventanas de backfill trimestral real (2017-03 → 2026-06), y el umbral
  de "45+ = rango agotado" de CLAUDE.md no aplica limpiamente aquí porque
  mezcla dos tipos de ventana.
  RECOMENDACIÓN: revisar por qué el backfill nunca generó ventanas para
  2015-02-19 → 2017-03-29 — posible bug en la fecha de inicio del backfill
  o ventanas que fallaron silenciosamente y no se reintentan.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015-02 → 2017-03 | 0/~8 | 0 | **Pendiente — nunca iniciado (ver Problema 2 arriba)** |
| 2017-03 → 2026-06 | 37/37 | ? | Completado (ventanas trimestrales ~3 meses c/u) |
| 2026-06 → hoy | 15 entradas diarias | ? | Fetch incremental normal (no es backfill histórico) |
| **TOTAL backfill trimestral** | **37/~45** | **?** | **Falta cubrir 2015-02 → 2017-03** |

> Tabla reconstruida el 2026-07-21 a partir de `sources/processed.json` →
> `_gdelt_windows` (52 entradas totales, ver desglose en Problema 2 arriba).
> No hay conteo de artículos por ventana individual en processed.json —
> solo el total global (`Artículos en sources/` arriba).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-21 | 0 (11 falsos positivos descartados) | 0 | Ver Problemas 1 y 2 arriba. Fix de bug en `mark_ingested()` (crasheaba con `_gdelt_windows`). Ver wiki/log.md 2026-07-21 para detalle completo. |

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
