---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-28
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados (con contenido en wiki/) | 6 | = total sin falsos positivos |
| Marcados ingested:true en processed.json (incl. falsos positivos despejados) | 18 | — |
| Pendientes de ingesta | 6 | 0 |
| Falsos positivos acumulados | 12 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 0 / ~45 estimadas | 45 (2015→hoy) |
| Días sin artículos nuevos | ver "Estado del Fetch" | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con commit  : 2026-07-26 (Actions corre casi a diario, ver git log de sources/)
Último artículo NUEVO real : 2026-07-20 (2 artículos) — 8 días sin artículos nuevos al 2026-07-28
Resultado sesión 2026-07-28: Pendientes=6 al llegar, 5 evaluados → 5/5 falsos positivos (0 reales)

Causa raíz identificada (2026-07-28):
  config/sources.yaml → web_searches → "prensa_agro" busca en DDG con
  `site:prensa.com` + query OR-amplia (incluye el acrónimo "MIDA"). El
  filtro de sitio no se aplica de forma efectiva: los resultados vienen de
  dominios arbitrarios (paultan.org, sltrib.com, msn.com, spa.gov.sa,
  nyfb.org, whc.unesco.org, ieeexplore.ieee.org, archive.org) que
  simplemente mencionan agricultura o el acrónimo "MIDA" en otro país
  (Malasia, Utah). Ver wiki/log.md 2026-07-28 08:04 para el detalle completo
  y la recomendación de fix en scripts/fetch_news.py.
  Efecto: la fuente "prensa.com" (18 de 24 artículos descargados) es casi
  en su totalidad ruido — de los 18, ~12 confirmados falsos positivos.
  El backfill real de agro panameño avanza casi exclusivamente por
  MIDA/IICA/TVNNoticias/LaPrensaEco/BDA (6 artículos reales a la fecha).

Fix histórico previo (2026-06-22): fetch_gdelt_historical() limitó end a
  datetime.utcnow()-1d; ventanas GDELT reseteadas a [] para backfill real.
  Estado: GDELT sigue en 0/~45 ventanas completadas — no validado aún.
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
| 2026-07-28 | 0 reales (5 falsos positivos despejados) | 6 | Diagnóstico causa raíz: bug de `site:` filter en DDG rompe la fuente "prensa_agro" (ver Estado del Fetch); GDELT sigue en 0/~45 ventanas |

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
