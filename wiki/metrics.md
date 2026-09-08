---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-08
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 39 | 0 |
| Falsos positivos acumulados (confirmados en processed.json) | 2 | **0 nuevos** |
| Páginas en wiki/ | 27 (10 topics, 3 entidades, 11 resúmenes) | ↑ continuo |
| Cobertura temporal | 2015-2026 (mezcla semilla + backfill real) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 | 45 (2015→hoy) — **superada, ver nota** |
| Días sin nuevos artículos en sources/ | 2 (último commit: 2026-09-06) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con artículos nuevos : 2026-09-06 (6 artículos)
Commits en sources/ desde entonces  : ninguno (sin corridas registradas 09-07 ni 09-08)
Días sin commit en sources/         : 2 (dentro del umbral de 3 días — VIGILAR)
Ventanas GDELT completadas          : 79 (supera el estimado de 45 para 2015→hoy;
                                       varias ventanas recientes con fin "20260618"
                                       se repiten — posible solapamiento en el
                                       cálculo de ventanas incrementales, revisar
                                       si persiste en la próxima sesión)
Cola de pendientes                  : 39 artículos, incluye falsos positivos
                                       evidentes por título (ver nota abajo)
```

**Nota — calidad de la cola de pendientes**: al revisar los 39 artículos pendientes
restantes se identificaron por título varios que claramente NO son sobre agro
panameño (ej. centros de datos en Utah, "MIDA" de Malasia, agricultura en
Aragón/España, Finep en Brasil, vacuna aviar en Mozambique, New York Farm
Bureau). No se ingirieron en esta sesión porque el lote de 5 seleccionado por
`ingest --limit 5` no los incluyó (los 5 procesados fueron 100% sobre agro
panameño — ver `wiki/log.md`). Se recomienda que la próxima sesión los
revise y marque como falsos positivos para mantener la cola limpia; el
ruido sugiere que el filtro de relevancia del fetch (GDELT/RSS) coincide
con palabras clave genéricas ("agro", "MIDA", "farm").
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| **TOTAL** | **79/45 estimadas** | **57 descargados / 18 ingestados** | **Estimado original superado** |

> El conteo de ventanas GDELT (79) ya superó el estimado original de 45 para
> cubrir 2015→hoy. No se cuenta con el detalle por trimestre porque
> `processed.json._gdelt_windows` almacena una lista plana de rangos
> `YYYYMMDD_YYYYMMDD`, no un desglose por año/trimestre. Se detectó que varias
> ventanas recientes (fin `20260618`) se repiten, lo que sugiere que el
> backfill incremental podría estar re-consultando el mismo rango reciente en
> lugar de avanzar sobre huecos históricos. Recomendado para próxima sesión:
> inspeccionar `scripts/` (o el módulo de fetch) para confirmar si el avance
> del backfill histórico 2015-2021 está completo o si sigue pendiente pese al
> conteo alto de ventanas.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-08 | 5 (arroz/Mida: importaciones, inundaciones 2024, siembra 2022-23, compensaciones Panamá Este/Darién, revisión subsidios) | 39 | Sin falsos positivos en el lote. Detectados ~10+ falsos positivos evidentes por título en la cola restante (pendiente de revisión). 2 páginas topics nuevas creadas (precios_mercados.md, subsidios_programas.md). Sin commits en sources/ desde 2026-09-06 (2 días) — vigilar umbral de 3 días. **BUG encontrado y corregido**: `mark-all-ingested --limit N` no usa el mismo orden que `ingest --limit N` (score vs. alfabético) y marcó los artículos equivocados; además `mark-ingested <url>` individual falla por bug con `_gdelt_windows`. Ver detalle y corrección en wiki/log.md 2026-09-08 16:22. Requiere fix en `scripts/ingest.py` en una próxima sesión de mantenimiento de código. |

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
