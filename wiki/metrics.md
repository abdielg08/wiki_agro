---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-24
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 15 | **0 nuevos** (8 nuevos detectados y bloqueados hoy) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 53 / ~46 estimadas | rango 2015→hoy cubierto |
| Días sin artículos nuevos | 4 (último: 2026-07-20) | máx 3 antes de diagnosticar |

**Pendientes de ingesta: 0** (los 8 artículos revisados hoy fueron falsos positivos, no wiki content).

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-23 (corre casi a diario, incl. días con 0 artículos)
Resultado reciente     : mayoría de corridas devuelven 0-2 artículos nuevos
Último artículo real   : 2026-07-20 (2 guardados) → 4 días sin nuevos al momento de esta sesión
Ventanas GDELT         : 53 completadas, superan la estimación original de 46 —
                         el rango 2015→hoy ya está cubierto por GDELT; el bajo
                         rendimiento reciente es normal (ventanas incrementales
                         cerca de tiempo real capturan poco volumen por día).

CAUSA RAÍZ IDENTIFICADA Y CORREGIDA HOY (2026-07-24):
  scripts/fetch_news.py::fetch_ddg_search() (fuente DDG "site:prensa.com") NO
  aplicaba los filtros _is_blocked_domain() / _is_panama_related() que sí tienen
  fetch_rss() y fetch_gdelt_batch(). Además, el operador `site:` de DDG no se
  respeta de forma confiable, así que resultados de dominios totalmente ajenos
  (sltrib.com, paultan.org, ieeexplore.ieee.org, archive.org, msn.com,
  unesco.org, nyfb.org, spa.gov.sa) se guardaban etiquetados como
  source="prensa.com", country="PA" solo por contener términos agro genéricos
  (p.ej. "MIDA", "agriculture") sin ninguna señal geográfica de Panamá.
  Esto explica los 8 falsos positivos consecutivos encontrados en esta sesión.
Fix aplicado           : fetch_ddg_search() ahora verifica que el dominio del
                         resultado coincida con `site`, rechaza dominios
                         bloqueados (_is_blocked_domain) y, para búsquedas sin
                         `site` fijo, exige término Panamá explícito
                         (_is_panama_related) — mismo estándar que RSS/GDELT.
Estado post-fix        : pendiente validación en la próxima corrida de GitHub
                         Actions (debería dejar de traer artículos no panameños
                         etiquetados "prensa.com").
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
| 2026-07-24 | 0 (8/8 revisados = falsos positivos) | 0 | Bugfix `mark-all-ingested` (lote desalineado con `ingest`); root-cause fix en `fetch_ddg_search()` (faltaban filtros de dominio/Panamá) |

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
