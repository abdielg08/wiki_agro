---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-25 (sesión 2)
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ (descargados) | 57 | ↑ continuo |
| Artículos reales ingestados (wiki) | 26 | = total sin falsos positivos |
| Falsos positivos acumulados (documentados) | 25 | **0 nuevos** desde el fix de `fetch_ddg_search` |
| Fuera de cobertura temporal (pre-2015) | 2 | — |
| Pendientes de ingesta (genuinos, verificados) | 4 | 0 |
| Páginas en wiki/ | 50 (16 topics, 5 entidades, 26 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (parcial, concentrada en 2019-2026) | 2015-02-19 → hoy |
| Ventanas GDELT completadas | 80 (+1 desde 2026-09-15, run #122) | 45+ (rango base ya cubierto) |
| Días sin artículos NUEVOS descargados | 19 (último con contenido nuevo: 2026-09-06) | máx 3 antes de diagnosticar |
| Estado del job de fetch (GitHub Actions) | **RECUPERADO hoy** (run #122, 2026-09-25, éxito, ~8m44s) tras 18 corridas fallidas consecutivas | corridas diarias exitosas |

---

## Estado del Fetch (GitHub Actions)

```
RECUPERADO (2026-09-25)   : Run #122 (id 36155796208, 2026-09-25 15:40:48-15:49:32 UTC,
                             ~8m44s, conclusion=success) — primera corrida exitosa desde
                             run #103 (2026-09-06). El paso interno "Fetch artículos
                             nuevos" corrió ~8m22s (ciclo real GDELT/RSS, no un fallo de
                             arranque), coincide con el avance de ventanas GDELT (79→80)
                             y terminó con un commit normal "0 artículos nuevos
                             descargados" (resultado legítimo — no todas las ventanas
                             traen contenido nuevo, no es señal de fallo).
Última ejecución EXITOSA
  antes de la racha        : 2026-09-06 (run #103, id 34037328987) → 6 artículos nuevos
Racha de fallos (cerrada)  : 2026-09-07 → 2026-09-24 (18 corridas diarias consecutivas,
                             runs #104-#121; confirmado vía GitHub Actions API que TODAS
                             completaron en 4-40s con conclusion=failure, patrón de
                             fallo de arranque del job, nunca llegaron a ejecutar el
                             fetch real)
Causa raíz probable        : el run #121 (2026-09-24) incluyó el commit
                             "fix(promote): checkout completo de rama en vez de fetch
                             por SHA (#306)", pero ESE run igual falló en 4s — el efecto
                             del fix solo se reflejó a partir del run #122 (2026-09-25).
                             La causa exacta del fallo de arranque en #104-#121 sigue sin
                             confirmarse desde esta sesión (logs de esas corridas ya
                             expiraron), pero el problema desapareció al mismo tiempo que
                             el fix de #306 tomó efecto.
Acción recomendada         : monitorear las próximas 1-2 corridas diarias programadas
                             (~15:40 UTC) para confirmar que la recuperación es estable
                             y no un caso aislado.
Ver diagnóstico completo   : wiki/log.md, entradas 2026-09-15 08:30, 2026-09-25 y
                             2026-09-25 (sesión 2 — RECUPERACIÓN FETCH)
```

```
Fix aplicado esta sesión  : fetch_ddg_search() en scripts/fetch_news.py no aplicaba
                             el filtro _is_panama_related()/_is_blocked_domain() que sí
                             usan fetch_rss() y fetch_gdelt_batch(). Esto permitía que
                             resultados de DuckDuckGo de dominios no panameños (ej.
                             "MIDA" de Malasia o de Utah) se guardaran como artículos
                             pendientes. Corregido — ver wiki/log.md 2026-09-15 08:25.
Bug adicional corregido   : mark_all_ingested() marcaba un conjunto de artículos
                             distinto al que ingest realmente mostraba a Claude (los
                             dos usaban órdenes de prioridad distintos). Corregido para
                             leer las URLs directamente de pending_ingest.md — ver
                             wiki/log.md 2026-09-15 08:20 y scripts/ingest.py.
Re-fix (2026-09-25)       : el fix del 2026-09-15 arriba descrito NO estaba presente
                             en scripts/ingest.py de main (se perdió en el problema de
                             ramas huérfanas resuelto el 2026-09-23) — el bug había
                             vuelto a ocurrir: 4 de 5 artículos marcados por esta misma
                             sesión de routine eran incorrectos. Re-aplicado el fix
                             (urls_from_pending_ingest() en scripts/ingest.py) y
                             corregido sources/processed.json manualmente. Ver
                             wiki/log.md 2026-09-25, entrada "FIX BUG mark_all_ingested".
```

---

## Progreso del Backfill GDELT (2015 → hoy)

> 80 ventanas GDELT completadas según `sources/processed.json` (`_gdelt_windows`), por
> encima del umbral de 45 que CLAUDE.md usa como señal de "rango base agotado". La
> cobertura real de artículos, sin embargo, sigue concentrada en 2019-2026; años
> 2015-2018 tienen cobertura escasa (solo los artículos semilla). Pendiente de una
> auditoría detallada de qué ventanas específicas (por trimestre) ya se cubrieron vs.
> cuáles devolvieron 0 resultados por falta de cobertura mediática de esa época.

| Período | Estado |
|---------|--------|
| 2015-2018 | Cobertura escasa — solo artículos semilla (1 por año aprox.) |
| 2019-2026 | Cobertura activa — mayoría de artículos ingestados y pendientes |

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-15 | 10 (2 lotes de 5) | 14 | Routine automatizada. Además: fix de bug crítico en `mark_all_ingested` (marcaba artículos equivocados), 17 falsos positivos nuevos detectados y documentados, 7 falsos positivos antiguos re-etiquetados, fix de raíz en `fetch_ddg_search` (faltaba filtro Panamá), y diagnóstico de 8 fallos consecutivos de GitHub Actions |
| 2026-09-25 | 5 | 9 | Routine automatizada. 0 falsos positivos (los 5 artículos eran genuinamente sobre agro panameño, aunque con `full_text` truncado en la fuente). Páginas nuevas: topics/darien_comarca.md, topics/cafe_cacao.md, entities/ima.md (resuelven broken links preexistentes). Diagnóstico confirmado vía GitHub Actions API: 18 fallos consecutivos del fetch diario desde 2026-09-07 (empeoró de 8 a 18 desde el diagnóstico anterior) |
| 2026-09-25 (sesión 2) | 5 | 4 | Routine automatizada. 0 falsos positivos (cooperación IICA-Argentina, alerta influenza aviar 2022, agricultura vertical IICA, cebolla importada, caso Valderrama). Páginas nuevas: entities/iica_panama.md, topics/hortalizas.md (resuelven 2 broken links preexistentes en index.md). Páginas actualizadas: topics/avicultura.md, topics/plagas_enfermedades.md, topics/tecnologia_innovacion.md, topics/precios_mercados.md, entities/mida.md. **Fetch de GitHub Actions RECUPERADO**: run #122 (2026-09-25) exitoso tras 18 corridas fallidas consecutivas (#104-#121, 2026-09-07 a 2026-09-24) — confirmado vía GitHub Actions API, duración real ~8m44s |

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

**Estado a 2026-09-25 (sesión 2)**: el **job de fetch de GitHub Actions se recuperó**
esta sesión — run #122 (2026-09-25, ~8m44s, éxito) rompió la racha de 18 corridas
fallidas consecutivas (#104-#121, 2026-09-07 → 2026-09-24), confirmado vía GitHub
Actions API con desglose por paso (el fetch real corrió ~8m22s, no fue un fallo de
arranque). Sin embargo, la señal de "días sin artículos NUEVOS descargados" sigue en
19 (último contenido nuevo: 2026-09-06), porque la corrida de hoy, aunque exitosa,
no encontró artículos nuevos en la ventana procesada (resultado normal, no un fallo).
El backlog de 4 artículos pendientes genuinos alcanza para ~1 sesión más de routine.
**Acción recomendada**: monitorear las próximas 1-2 corridas diarias para confirmar
que la recuperación del fetch es estable; si vuelven a aparecer fallos de 3-6s, revisar
de nuevo cuota de Actions / permisos. Ver diagnóstico en wiki/log.md, entrada
2026-09-25 (sesión 2 — RECUPERACIÓN FETCH).
