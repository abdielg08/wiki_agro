---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-01
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 18 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 12 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 42 / ~46 estimadas | 46 (2015→hoy) |
| Días sin artículos nuevos | 2 (último fetch: 2026-06-29) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-06-29 (1 artículo nuevo descargado)
Resultado sesión 2026-07-01 : 5 pendientes revisados → 5/5 falsos positivos, 0 reales
Causa identificada     : _AGRO_QUERY en fetch_historical.py incluye el acrónimo suelto
                         "MIDA" sin desambiguar. GDELT lo matchea contra:
                           - Malaysian Investment Development Authority (falsos previos)
                           - Utah Military Installation Development Authority (3 de los 5
                             nuevos: data centers de Kevin O'Leary / Box Elder / Gov. Cox)
                         Además 2 falsos más sin relación con "MIDA": New York Farm Bureau
                         y programa "Reef Saudi" (Arabia Saudita) — coincidencia por
                         términos genéricos de agricultura, no específicos de Panamá.
                         GDELT etiqueta erróneamente source="prensa.com"/country="PA" en
                         estos 5 aunque las URLs reales son sltrib.com, nyfb.org, spa.gov.sa
                         — sourcecountry:PA de GDELT no garantiza contenido panameño.
Fix pendiente (no aplicado en esta sesión, requiere confirmación del usuario):
                         quitar "MIDA" de _AGRO_QUERY en fetch_historical.py (fetch_news.py
                         ya evita acrónimos sueltos por el mismo motivo) y/o validar el
                         dominio real de la URL contra el país esperado antes de aceptar
                         un resultado de GDELT.
Backfill GDELT         : 42/~46 ventanas trimestrales completadas — no está agotado ni
                         bloqueado, avanza con normalidad.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 (feb) - 2017 Q1 | 0 | **Pendiente — hueco sin cubrir** |
| 2017 Q2-Q4 | 3 | Completo |
| 2018 Q1-Q4 | 4 | Completo |
| 2019 Q1-Q4 | 4 | Completo |
| 2020 Q1-Q4 | 4 | Completo |
| 2021 Q1-Q4 | 4 | Completo |
| 2022 Q1-Q4 | 4 | Completo |
| 2023 Q1-Q4 | 4 | Completo |
| 2024 Q1-Q4 | 4 | Completo |
| 2025 Q1-Q4 | 4 | Completo |
| 2026 (hasta jun) | 5 (incluye ventanas cortas de reintento) | Completo hasta 2026-06-28 |
| **TOTAL** | **42/~46** | **Casi completo — falta el hueco 2015–2017 Q1** |

> Hallazgo de esta sesión (2026-07-01): `sources/processed.json._gdelt_windows` no tiene
> ninguna ventana con fecha de inicio anterior a 2017-03-30. La cobertura objetivo del
> proyecto es 2015-02-19 → hoy (ver CLAUDE.md), así que falta hacer backfill explícito de
> 2015-02-19 a 2017-03-29 antes de poder decir que el backfill histórico está completo.
> El rendimiento real de GDELT (artículos/ventana) para ese período aún no se ha medido.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-01 | 0 (5 revisados, 5/5 falsos positivos) | 0 | Falsos positivos por acrónimo "MIDA" ambiguo (Utah, Malaysia) + 2 artículos internacionales sin relación con Panamá (NY Farm Bureau, Reef Saudi). Ver wiki/log.md para detalle y causa raíz. |

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
