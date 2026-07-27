---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-27
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 18 (+5 esta sesión, 0 ingestados) | **0 nuevos** — ⚠️ ver causa raíz abajo |
| Pendientes de ingesta | 6 | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 56 / ~46 estimadas | 45-46 (2015→hoy) — **umbral superado** |
| Días sin artículos nuevos (reales) | ≥6 (desde 2026-07-20; commits Actions 07-21 a 07-26 = "0 nuevos") | máx 3 antes de diagnosticar — **⚠️ alarma activa** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-26 (corre diariamente, workflow OK — no está caído)
Resultado               : 0-3 artículos "nuevos" por día, pero desde finales de mayo la
                          inmensa mayoría (18/24 = 75% del total histórico) son falsos
                          positivos — no es un problema de que el fetch no corra, es que
                          lo que trae es basura.
Causa raíz (2026-07-27) : scripts/fetch_news.py::fetch_ddg_search() arma queries DDG con
                          "site:<dominio> <términos>", pero DuckDuckGo News no respeta el
                          operador site: de forma confiable. Resultado: llegan artículos de
                          dominios totalmente ajenos (sltrib.com, paultan.org, thestar.com.my,
                          msn.com, fox13now.com, ieeexplore.ieee.org, nyfb.org, archive.org,
                          whc.unesco.org, spa.gov.sa) etiquetados como source="prensa.com" (o
                          el site configurado), simplemente porque el cuerpo del artículo
                          contiene una palabra suelta como "MIDA" o "agricultura"
                          (is_agro_relevant() no exige relación con Panamá, solo substring).
                          Ejemplo: "MIDA" también es la Malaysian Investment Development
                          Authority y la Utah Military Installation Development Authority.
Fix aplicado (2026-07-27): fetch_ddg_search() ahora verifica que el dominio real del resultado
                          coincida con el `site:` configurado (usando _url_domain() +
                          _is_blocked_domain(), igual que ya hacía fetch_rss()). Debería
                          eliminar la gran mayoría de falsos positivos futuros vía DDG.
Estado post-fix         : Pendiente validación en próxima corrida Actions / próxima sesión.
Pendiente adicional     : revisar por qué GDELT (56 ventanas completadas) no está aportando
                          artículos reales — mismo patrón de causa raíz podría aplicar a
                          fetch_gdelt_historical(), no auditado en esta sesión.

Bug adicional (2026-07-27) en scripts/ingest.py, también corregido esta sesión:
  mark_all_ingested() seleccionaba por orden alfabético de archivo (glob), mientras que
  `ingest --limit N` selecciona por score de relevancia — los dos comandos podían marcar
  conjuntos de artículos distintos entre sí. Se detectó porque marcó 3 artículos nunca
  revisados por Claude y dejó 3 revisados sin marcar. Corregido para usar prioritize()
  igual que run_prepare(). También se corrigió mark_ingested(url) que fallaba con
  AttributeError al no excluir la clave interna _gdelt_windows.
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

> ⚠️ 2026-07-27: `sources/processed.json._gdelt_windows` reporta **56 ventanas completadas**,
> ya por encima del estimado de 46 en esta tabla — pero las ventanas no son 1:1 con
> "trimestre" (se ven pares con el mismo inicio y distinto fin, ej. `20260618_20260626` y
> `20260618_20260723`, lo que sugiere re-división adaptativa de ventanas grandes). La tabla de
> abajo quedó desactualizada y no se puede reconstruir de forma confiable sin auditar
> `fetch_historical.py` a fondo — pendiente para una próxima sesión. Lo que sí es seguro: casi
> ninguno de los artículos reales en el wiki vino de GDELT (todos los 6 artículos reales
> ingestados son semilla manual del 2026-05-24), así que aunque las ventanas se están
> completando, no están aportando contenido útil — revisar si sufre el mismo problema de
> relevancia que se encontró y corrigió en `fetch_ddg_search()` esta sesión.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-27 | 0 (5 revisados, 5 falsos positivos) | 6 | Causa raíz encontrada y corregida: `fetch_ddg_search()` no verificaba dominio real del resultado vs. `site:` configurado. Alarma: ≥6 días sin artículos reales nuevos. |

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
