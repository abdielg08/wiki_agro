---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-26
---

> **Actualización 2026-09-26 (sesión de diagnóstico, ~08:10 UTC)**: 0 pendientes de
> ingesta (sin ingesta nueva esta sesión). Causa raíz del bug recurrente de
> `mark_all_ingested()` finalmente confirmada — ver "Estado del Fetch" y `wiki/log.md`
> para el detalle completo. Acción pendiente del usuario: mergear el PR con el fix de
> `scripts/ingest.py` (o uno de los 3 duplicados #313/#314/#315) para romper el ciclo.

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ (descargados) | 57 | ↑ continuo |
| Artículos reales ingestados (wiki) | 30 | = total sin falsos positivos |
| Falsos positivos acumulados (documentados) | 25 | **0 nuevos** desde el fix de `fetch_ddg_search` |
| Fuera de cobertura temporal (pre-2015) | 2 | — |
| Pendientes de ingesta (genuinos, verificados) | 0 | 0 |
| Páginas en wiki/ | 58 (20 topics, 5 entidades, 30 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (parcial, concentrada en 2019-2026) | 2015-02-19 → hoy |
| Ventanas GDELT completadas | 80 (sin cambio desde 2026-09-25, run #122) | 45+ (rango base ya cubierto) |
| Días sin artículos NUEVOS descargados | 20 (último con contenido nuevo: 2026-09-06) | máx 3 antes de diagnosticar |
| Estado del job de fetch (GitHub Actions) | Recuperado desde run #122 (2026-09-25, éxito); próxima corrida diaria programada aún no ha ocurrido al momento de esta sesión (~00:19 UTC) | corridas diarias exitosas |

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
Estado a 2026-09-26        : sin cambios respecto al 2026-09-25 (sesión 2). Verificado
                             vía GitHub Actions API (actions_list) que el run #122 sigue
                             siendo el más reciente (total_count=122) — la próxima
                             corrida diaria programada (~15:40 UTC) aún no ha ocurrido al
                             momento de esta sesión (~00:19 UTC del 2026-09-26). No hay
                             evidencia nueva que confirmar o refutar la estabilidad de la
                             recuperación todavía.
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
Re-fix #2 (2026-09-26)    : el mismo bug reapareció una TERCERA vez — el fix del
                             2026-09-25 tampoco llegó a persistir en main (mismo
                             mecanismo sospechado: pérdida en merges/ramas huérfanas).
                             4 de los 5 artículos marcados el 2026-09-25 16:16 eran
                             incorrectos (sin página de wiki creada); los 4 genuinos
                             (iica-cooperación, alerta zoosanitaria, agricultura
                             vertical IICA, cebolla) seguían en `ingested: false`.
                             Re-aplicado el fix por tercera vez y corregido
                             sources/processed.json. Ver wiki/log.md 2026-09-26,
                             entrada "FIX BUG mark_all_ingested, recurrencia" — incluye
                             nota para que sesiones futuras verifiquen el código fuente
                             de scripts/ingest.py directamente, no solo el log.
CAUSA RAÍZ CONFIRMADA
  (2026-09-26, sesión 2)  : el fix seguía ausente de main una CUARTA vez. Esta sesión
                             investigó el mecanismo en vez de solo re-parchar:
                             `.github/workflows/promote_wiki.yml` promueve `wiki/**` y
                             `sources/processed.json` de cualquier rama `claude/**` a
                             `main` automáticamente, pero EXCLUYE `scripts/` a propósito
                             ("rutas restringidas por seguridad"). Cualquier fix de
                             código queda atrapado en el Pull Request de la sesión hasta
                             que un humano lo mergea. Se confirmaron 3 PRs abiertos como
                             draft con el mismo fix aplicado independientemente y nunca
                             mergeados: #313, #314, #315 — su contenido de wiki/ ya está
                             en main (vía el bot), pero su fix de scripts/ingest.py no.
                             Esta sesión abrió un PR nuevo, limpio, solo con el fix de
                             código (sin contenido de wiki duplicado) para minimizar
                             conflictos de merge. **Requiere acción manual del usuario**:
                             mergear ese PR (o #313/#314/#315) y cerrar los duplicados.
                             Ver wiki/log.md 2026-09-26, entrada "DIAGNÓSTICO".
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
| 2026-09-26 | 4 | 0 | Routine automatizada. 0 falsos positivos (plan de contingencia MIDA Los Santos, sequía ganadera Panamá Este/Darién, agricultura familiar, trazabilidad). Páginas nuevas: topics/agua_riego.md, topics/azuero.md, topics/ganaderia_bovina.md, topics/comercio_exterior.md (resuelven 4 broken links preexistentes). Páginas actualizadas: topics/cambio_climatico.md, topics/darien_comarca.md, topics/seguridad_alimentaria.md, topics/politicas_agropecuarias.md, topics/tecnologia_innovacion.md, entities/mida.md. **Bug de `mark_all_ingested` recurrió por tercera vez** (ver arriba) y fue corregido de nuevo. Fetch de GitHub Actions: sin corridas nuevas desde run #122 al momento de esta sesión (~00:19 UTC) |
| 2026-09-26 (sesión 2) | 0 | 0 | Routine automatizada de solo-diagnóstico (0 pendientes al iniciar). **Causa raíz del bug recurrente de `mark_all_ingested` finalmente confirmada**: `promote_wiki.yml` excluye `scripts/` de la promoción automática por diseño; el fix de código queda atrapado en PRs de sesión que nadie ha mergeado (#313, #314, #315, todos duplicados del mismo fix). Re-aplicado el fix por cuarta vez y abierto un PR nuevo, limpio, solo de código. **Acción manual requerida del usuario**: mergear el PR y cerrar los duplicados. Fetch de GitHub Actions: sin corridas nuevas desde run #122 (próxima corrida diaria ~15:40 UTC aún no ocurre a esta hora, ~08:10 UTC) |

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

**Estado a 2026-09-26**: sin cambios en el fetch respecto al 2026-09-25 (sesión 2) — el
run #122 (2026-09-25, éxito) sigue siendo la corrida más reciente; la siguiente corrida
diaria programada (~15:40 UTC) todavía no ocurre al momento de esta sesión (~00:19 UTC).
"Días sin artículos NUEVOS descargados" subió a 20 (último contenido nuevo: 2026-09-06).
El backlog de artículos pendientes genuinos llegó a **0** esta sesión — el backfill
histórico depende ahora enteramente de que el fetch automático (GDELT/RSS) siga
trayendo artículos nuevos; sin corridas adicionales que confirmen la recuperación, no
hay backlog de respaldo para la próxima sesión de routine.
**Bug recurrente**: `mark_all_ingested()` volvió a desincronizarse por tercera vez esta
sesión (ver "Bug adicional corregido" arriba) — el fix aplicado el 2026-09-15 y de
nuevo el 2026-09-25 no había persistido en `scripts/ingest.py` de `main`. Re-aplicado.
**Acción recomendada**: (1) monitorear la próxima corrida diaria (~15:40 UTC,
2026-09-26) para confirmar que el fetch sigue estable; (2) en la próxima sesión,
verificar con `grep urls_from_pending_ingest scripts/ingest.py` que el fix del bug de
`mark_all_ingested` sigue presente en main antes de asumir que está resuelto. Ver
diagnóstico en wiki/log.md, entradas 2026-09-25 (sesión 2 — RECUPERACIÓN FETCH) y
2026-09-26 (FIX BUG mark_all_ingested, recurrencia).
