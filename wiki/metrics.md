---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-06
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados (al wiki) | 13 | = total sin falsos positivos |
| Falsos positivos acumulados (flag `false_positive` en processed.json) | 16 | **0 nuevos publicados al wiki** (cumplido: 0 de 16 se publicaron) |
| Pendientes de ingesta | 0 | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 62 / ~45 estimadas | 45 (2015→hoy) — **superado, ver nota** |
| Días sin artículos nuevos reales en wiki/ | 1 (2026-08-06, sesión sin ingestas reales) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions verificada : 2026-08-05 12:47 UTC (status: success)
Corrida de hoy (2026-08-06)       : aún no ejecutada (cron 11:00 UTC / 6am Panamá)
Resultado sesión 2026-08-06       : 16/16 artículos pendientes = falsos positivos (0 reales)

Causa raíz identificada:
  El web_search "prensa_agro" (scripts/fetch_news.py::fetch_ddg_search) arma la
  query como "site:prensa.com agropecuario OR agricultura OR ganadería OR MIDA
  OR cosecha Panamá", pero el backend de DDG News NO respeta el operador
  "site:" de forma confiable. Además is_agro_relevant() solo hace substring
  match de términos genéricos (incl. "MIDA", "agro") sin verificar dominio ni
  geografía. Resultado: 16 artículos de heraldo.es (Aragón, España),
  sltrib.com (Utah — "MIDA" = Military Installation Development Authority),
  paultan.org (Malasia — "MIDA"/"MITI" = Ministry of Investment Trade and
  Industry), archive.org, ieeexplore.ieee.org, nyfb.org, spa.gov.sa,
  agenciabrasil.ebc.com.br y whc.unesco.org quedaron mal etiquetados como
  country=PA/source=prensa.com y entraron a la cola de pendientes.

Fix aplicado (2026-08-06, este commit):
  scripts/fetch_news.py::fetch_ddg_search ahora valida que el netloc real de
  cada resultado coincida con el dominio configurado en `site` antes de
  aceptarlo — descarta cualquier resultado fuera de ese dominio.
Estado post-fix: pendiente de validación en la próxima corrida de Actions
  (2026-08-06 11:00 UTC o siguiente).
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
| 2026-08-06 | 0 reales / 16 falsos positivos rechazados | 0 | Root cause: bug en filtro `site:` de fetch_ddg_search (prensa_agro). Fix aplicado en scripts/fetch_news.py. Ventanas GDELT (62) ya superan la estimación de 45 — revisar rango/estrategia de backfill en próxima sesión. |

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
