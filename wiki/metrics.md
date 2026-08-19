---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-19
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 13 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 (7 previos + 16 nuevos 2026-08-19) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 38 reales / ~46 estimadas (70 brutas, ver nota) | 46 (2015→hoy) |
| Días sin artículos nuevos | 20 (desde 2026-07-30) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions   : 2026-08-17 (0 artículos nuevos)
Último día con artículos : 2026-07-30 (3 artículos) — 20 días sin novedades reales
Causa identificada       : 1) fetch_ddg_search() no filtraba por relevancia a Panamá
                              (le faltaba el guard _is_panama_related/_is_blocked_domain
                              que sí tienen fetch_rss y fetch_gdelt_batch) → 100% de la
                              cola de pendientes (16/16) eran falsos positivos: Malasia
                              (MIDA), Utah (MIDA), Arabia Saudita, España (Aragón),
                              Brasil, UNESCO, IEEE. Ver wiki/log.md 2026-08-19.
                           2) _gdelt_windows tenía 70 entradas pero solo 38 eran
                              ventanas trimestrales reales; 33 eran claves casi-
                              duplicadas de una ventana final que se re-generaba cada
                              día porque su límite era "ayer" (dinámico) en vez de un
                              borde trimestral fijo — inflaba el conteo sin avanzar
                              el backfill real.
                           3) Falta el tramo 2015-02-19 → 2017-03-29 (~8 trimestres)
                              en el backfill GDELT — nunca se marcó como completado.
                              No se pudo probar en vivo (este sandbox no tiene salida
                              de red a GDELT — solo funciona desde runners de Actions).
Fix aplicado              : fetch_ddg_search() ahora exige _is_panama_related() y
                              rechaza _is_blocked_domain() antes de aceptar un
                              resultado (scripts/fetch_news.py).
                           fetch_gdelt_historical() ya no marca como "completada" la
                              ventana final mientras su límite sea "ayer" — solo se
                              persiste cuando cierra en un borde trimestral real.
                           mark_ingested() (scripts/ingest.py) tenía un bug que
                              rompía con AttributeError al iterar la clave interna
                              _gdelt_windows — corregido para usar article_entries().
Estado post-fix           : Pendiente validación en próxima corrida de Actions (fetch
                              diario) y en la próxima corrida manual de fetch-historical
                              (para confirmar si 2015-2017 responde con datos o error).
```

---

## Progreso del Backfill GDELT (2015 → hoy)

> Ventanas de 90 días desde 2015-01-01 (no son trimestres calendario exactos).
> Recalculado el 2026-08-19 leyendo `processed.json["_gdelt_windows"]` directamente
> (70 claves brutas → 38 ventanas reales distintas tras descartar 33 duplicados de
> la ventana final "abierta", ver Estado del Fetch arriba).

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015-01 → 2017-03 (~8 ventanas) | 0/8 | **Faltante** — nunca se completó, causa sin confirmar (sin acceso a red GDELT en este sandbox) |
| 2017-03 → 2026-03 (~37 ventanas) | 37/37 | Completado |
| 2026-03 → hoy (ventana en curso) | en progreso | Se re-consulta cada corrida hasta cerrar en un borde de 90 días real (fix 2026-08-19) |
| **TOTAL histórico (2015→2026-03)** | **37/45** | **82% — falta el tramo inicial 2015-2017** |

> Próximo paso recomendado: correr `fetch-historical --years 2015-2017 --mode gdelt`
> manualmente (vía GitHub Actions, no desde este sandbox) y revisar si GDELT
> devuelve 0 resultados, error HTTP, o simplemente no tiene cobertura de texto
> completo tan atrás. Documentar el resultado en wiki/log.md.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-19 | 0 reales (16 falsos positivos purgados) | 0 | Fix de raíz en fetch_ddg_search (sin filtro Panamá) + fix mark_ingested + fix inflado de ventanas GDELT. Ver wiki/log.md |

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
