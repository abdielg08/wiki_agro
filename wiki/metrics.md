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
| Artículos reales ingestados | 11 | = total sin falsos positivos |
| Falsos positivos acumulados | 8 (+1 esta sesión) | **0 nuevos en el lote procesado** |
| Pendientes de ingesta | 38 | 0 |
| Páginas en wiki/ | 27 (10 topics, 3 entidades, 11 resúmenes) | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + real, arroz/MIDA 2022-2025) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 (`_gdelt_windows`) | 45 (2015→hoy) — **ya superado**, ver nota |
| Días sin artículos nuevos | 2 (último commit sources/: 2026-09-06) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con artículos nuevos : 2026-09-06 (6 artículos)
Días sin artículos nuevos           : 2 (09-07, 09-08 sin commit en sources/)
Ventanas GDELT completadas          : 79 — muy por encima de las ~45 estimadas
                                       para cubrir 2015→hoy. Posible causa:
                                       el fetcher re-corre ventanas ya completadas
                                       en vez de expandir a fechas nuevas, o el
                                       cálculo de "~45 estimadas" original era
                                       incorrecto. Pendiente investigar
                                       scripts/fetch_gdelt.py (o equivalente).
Contaminación de la cola de pending : 15+ artículos con source="prensa.com" que
                                       en realidad vienen de dominios ajenos
                                       (thestar.com.my, sltrib.com, heraldo.es,
                                       clubofmozambique.com, archive.org,
                                       ieeexplore.ieee.org, whc.unesco.org,
                                       maine.gov, nyfb.org, agenciabrasil.ebc.com.br,
                                       spa.gov.sa, paultan.org, msn.com, fox13now.com).
                                       Coinciden por el acrónimo "MIDA" (usado
                                       también por la Malaysian Investment
                                       Development Authority) o términos genéricos
                                       de agro/plagas sin filtro de país real.
                                       Recomendación: validar dominio real de la
                                       URL contra el "source" declarado antes de
                                       guardar en sources/articles/.
Bug de código corregido esta sesión : mark-all-ingested usaba un orden distinto
                                       al de `ingest`, marcando lotes equivocados
                                       como ingestados sin procesarlos realmente
                                       (ver wiki/log.md 2026-09-08 para detalle).
                                       Corregido en scripts/ingest.py.
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
| **TOTAL** | **79/46** | **?** | **Ventanas ya superan la meta original — requiere recálculo por trimestre** |

> Esta tabla trimestral quedó desactualizada: `_gdelt_windows` en `processed.json` ya
> registra 79 ventanas completadas, muy por encima de las ~45 estimadas. Antes de
> confiar en esta tabla hay que recalcular la distribución real por trimestre a partir
> de `_gdelt_windows` (formato `YYYYMMDD_YYYYMMDD`) y confirmar si el exceso se debe a
> ventanas duplicadas/reprocesadas o a que la estimación original de 45 era baja.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-08 | 5 reales + 1 falso positivo documentado | 38 | Cluster arroz/MIDA 2022-2025; fix de bug en mark-all-ingested/mark-ingested (scripts/ingest.py) |

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
