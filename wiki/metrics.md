---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-30
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 26 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 20 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 58 (cubren 2017-03-30 → 2026-07-28) | 2015-02-19 → hoy |
| Días sin artículos nuevos | 0 (última corrida: 2026-07-29, +2 artículos) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-29
Resultado               : 2 artículos nuevos descargados (commit aa7d9eb)
Ventanas GDELT          : 58 completadas, rango 2017-03-30 → 2026-07-28
                          Falta cubrir 2015-02-19 → 2017-03-30 (~8 ventanas
                          trimestrales) para llegar al límite real de GDELT.
Bug encontrado (2026-07-30): fetch_ddg_search() en scripts/fetch_news.py no
  aplicaba los mismos filtros anti-falso-positivo que fetch_rss() (dominio
  bloqueado / término Panamá). El operador `site:` de DDGS no se respeta de
  forma estricta, así que la búsqueda "prensa_agro" (query incluye "MIDA"
  como término suelto) dejó pasar 13 artículos de dominios no relacionados
  (archive.org, ieeexplore.ieee.org, sltrib.com, heraldo.es, msn.com,
  nyfb.org, spa.gov.sa, whc.unesco.org, paultan.org) — todos sobre MIDA de
  Malasia o MIDA de Utah (Military Installation Development Authority), no
  sobre Panamá. Se etiquetaban incorrectamente con fuente "prensa.com".
  Fix aplicado: fetch_ddg_search() ahora aplica _is_blocked_domain() y
  _is_panama_related() igual que fetch_rss(). Ver wiki/log.md 2026-07-30.
Bug encontrado #2 (2026-07-30): mark_ingested() en scripts/ingest.py
  iteraba processed.items() sin filtrar la clave interna "_gdelt_windows"
  (una lista), causando AttributeError en cada invocación. Fix aplicado:
  ahora usa article_entries(processed) como ya hacía mark_all_ingested().
Estado post-fix         : Pendiente validación en próxima corrida Actions
  (la próxima búsqueda DDG "prensa_agro" no debería volver a filtrar MIDA
  Malasia/Utah)
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
| 2026-07-30 | 0 (13 falsos positivos revisados y rechazados) | 0 | Todos los 13 pendientes eran MIDA-Malasia/MIDA-Utah, no Panamá. Corregido bug en fetch_ddg_search() (faltaba filtro Panamá) y bug en mark_ingested() (crash por clave interna _gdelt_windows) |

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
