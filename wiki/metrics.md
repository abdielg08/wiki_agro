---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-18
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 22 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 16 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2016-2024 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 50 / ~46 estimadas | rango 2015→hoy alcanzado |
| Días sin artículos NUEVOS (sources/) | 3 (16, 17, 18 jul) | máx 3 antes de diagnosticar |
| Días sin artículos REALES en wiki/ | ~55 (desde 2026-05-24) | 1 día hábil |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-18 (corrió correctamente, 0 artículos nuevos)
Racha sin artículos nuevos en sources/ : 3 días (2026-07-16, 17, 18) — límite de alarma alcanzado hoy

HALLAZGO PRINCIPAL (sesión 2026-07-18):
  De los 16 artículos "prensa.com" acumulados desde el seed (2026-05-24),
  el 100% resultaron ser falsos positivos al revisarlos esta sesión (9 de
  9 pendientes). Ninguno mencionaba Panamá. Todos venían de la búsqueda DDG
  `prensa_agro` (config/sources.yaml) pero de dominios ajenos a prensa.com
  (paultan.org, sltrib.com, whc.unesco.org, nyfb.org, spa.gov.sa,
  ieeexplore.ieee.org) — la librería `ddgs` no respeta el operador `site:`
  en `ddgs.news()`, y `is_agro_relevant()` no verificaba el dominio real.
  Resultado: 0 artículos reales nuevos han entrado al wiki desde el seed,
  pese a que Actions corre a diario.

CAUSA RAÍZ                : fetch_ddg_search() no validaba que el dominio de la
                             URL devuelta coincidiera con `site:` — aceptaba
                             cualquier resultado global que matcheara términos
                             genéricos como "MIDA" o "agricultura".
FIX aplicado (2026-07-18) : scripts/fetch_news.py — fetch_ddg_search() ahora
                             descarta resultados cuyo dominio no sea el
                             configurado en `site` (o subdominio). Aplica a
                             las 5 búsquedas DDG restringidas por sitio
                             (prensa_agro, mida_noticias, idiap_investigacion,
                             bda_credito, iica_panama).
Bugs adicionales corregidos: mark_ingested() crasheaba siempre (AttributeError
                             sobre `_gdelt_windows`); mark_all_ingested()
                             podía marcar un artículo NO revisado por Claude
                             como ingestado (orden distinto al de `ingest`).
                             Ver wiki/log.md 2026-07-18 16:06 para detalle.
Estado post-fix            : pendiente validar en próxima corrida real de
                             fetch_ddg_search (Actions o sesión manual) que
                             ya no aparezcan falsos positivos por dominio.

GDELT — ventanas: 50 completadas, rango 2015→hoy ya cubierto (se abrirán
  nuevas ventanas trimestrales automáticamente con el paso del tiempo). Pero
  0 artículos han sido guardados vía GDELT en 50 ventanas — no confirmado si
  es cobertura real 0 de GDELT para fuentes panameñas pequeñas o si los
  filtros (_is_blocked_domain / _is_panama_related / sourcelang:spa) son
  demasiado agresivos. Pendiente investigar en próxima sesión: correr
  fetch_gdelt_batch() para una ventana suelta y loggear el conteo crudo de
  `data["articles"]` antes de aplicar filtros.

RSS: solo IICA y LaPrensaGeneral (prensa.com/feed/) están configuradas con
  feed activo; ninguna ha aportado artículos en el dataset actual (0 con
  method=rss). No se pudo verificar alcanzabilidad de los feeds desde esta
  sesión (sin acceso saliente a internet en este entorno) — revisar logs de
  GitHub Actions del job "Fetch artículos nuevos" para confirmar si las
  fuentes RSS responden 200 y cuántas entradas devuelven.
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
| 2026-07-18 | 0 | 0 | 9 falsos positivos revisados y descartados (0 reales). Causa raíz corregida en fetch_ddg_search() (validación de dominio `site:`) + 2 bugs de mark-ingested corregidos. Ver log.md 16:03–16:06. |

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
