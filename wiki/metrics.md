---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-02
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 12 | **0 nuevos** (5 nuevos hoy — ver diagnóstico) |
| Pendientes de ingesta | 11 | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 60 (38 rangos únicos, 2017-03-30 → 2026-06-18) | 2015-02-19 → hoy |
| Días sin artículos nuevos | 3 (últimos nuevos: 2026-07-30) | máx 3 antes de diagnosticar → **ALARMA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con commit : 2026-07-31 (0 artículos nuevos)
Última corrida con nuevos : 2026-07-30 (3 artículos nuevos)
Sin commits de sources/   : 2026-08-01 y 2026-08-02 (2 días sin ninguna corrida registrada,
                            ni siquiera un commit "0 artículos nuevos") — el cron corre
                            diario (0 11 * * *), así que esperaríamos un commit por día
                            aunque no haya artículos nuevos. Revisar el historial de
                            Actions en GitHub directamente para confirmar si el workflow
                            está fallando silenciosamente o si dejó de dispararse.
```

### Diagnóstico de esta sesión (2026-08-02)

**1. Falsos positivos por colisión de sigla "MIDA"** — de los 5 artículos pendientes
procesados, los 5 resultaron ser falsos positivos: "MIDA" coincide con la Malaysian
Investment Development Authority y con la Military Installation Development Authority
de Utah, ninguno relacionado con Panamá. Ver `wiki/log.md` (2026-08-02) para detalle.

**2. Causa raíz encontrada y corregida**: `fetch_ddg_search()` en
`scripts/fetch_news.py` no aplicaba los filtros `_is_panama_related()` /
`_is_blocked_domain()` que sí protegen las rutas RSS y GDELT (el comentario en el
código ya advertía "no acronyms (MIDA matches Malaysia too)" pero el filtro nunca
se conectó al buscador DDG). Resultado: el 100% de los 11 artículos pendientes
restantes al final de la sesión son de dominios no panameños (sltrib.com, heraldo.es,
ieeexplore.org, archive.org, whc.unesco.org, agenciabrasil.ebc.com.br, spa.gov.sa,
nyfb.org) — la búsqueda `site:prensa.com` de DuckDuckGo no está siendo respetada
estrictamente y sin el filtro de términos panameños, todo lo que contuviera "MIDA"
u otro término agro genérico pasaba. **Corregido**: se agregó el mismo filtro de
`_is_panama_related()` / `_is_blocked_domain()` a `fetch_ddg_search()`.

**3. Bug de herramienta encontrado y corregido**: `mark_ingested()` (comando
`mark-ingested <url>`) iteraba `processed.items()` sin excluir la clave interna
`_gdelt_windows` (una lista, no un dict) — esto causaba `AttributeError` en
**toda** invocación, es decir, el comando estaba roto. Corregido usando
`article_entries(processed)`.

**4. Bug de herramienta encontrado y corregido**: `mark_all_ingested()` (comando
`mark-all-ingested --limit N`) seleccionaba los primeros N pendientes ordenados
por nombre de archivo, mientras que `ingest --limit N` (el que genera
`pending_ingest.md`) selecciona por score de relevancia — dos órdenes distintos.
Al ejecutar `mark-all-ingested --limit 5` esta sesión, marcó 5 artículos
**diferentes** a los 5 realmente revisados (solo 1 coincidió), sin que ninguno
de esos 4 tuviera página de wiki creada. Se revirtieron esos 4 a `ingested: false`
y se corrigió `mark_all_ingested()` para usar la misma priorización por score
que `run_prepare()`, evitando que vuelva a ocurrir.

**Recomendación para próxima sesión**: validar que el próximo commit de Actions
(esperado ~11:00 UTC) traiga artículos y que ya no haya falsos positivos por
"MIDA"/dominios no panameños gracias al fix de `fetch_ddg_search()`. Si
`sources/` sigue sin nuevos commits, escalar como posible fallo del workflow
de GitHub Actions (no solo de contenido).

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
| 2026-08-02 | 0 reales, 5 falsos positivos documentados | 11 | Colisión sigla "MIDA" (Malasia/Utah); causa raíz corregida en `fetch_ddg_search()`; 2 bugs de `mark-ingested`/`mark-all-ingested` encontrados y corregidos |

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
