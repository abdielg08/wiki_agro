---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-30
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 51 | ↑ continuo |
| Artículos con ingested=true | 23 | = total sin falsos positivos |
| Falsos positivos acumulados | 9 | **0 nuevos** |
| Pendientes de ingesta | 28 | 0 |
| Páginas en wiki/ | 28 | ↑ continuo |
| Cobertura temporal | 2007, 2010, 2016–2026 | 2015 → hoy real |
| Ventanas GDELT completadas | 76 / ~45 estimadas | 45 (2015→hoy) — estimado superado, revisar cobertura real por año |
| Días sin artículos nuevos (sources/) | 3 (2026-08-28, 29, 30) | máx 3 antes de diagnosticar — **umbral alcanzado hoy** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida exitosa      : 2026-08-27 (run #93) — 1 artículo nuevo
Corridas fallidas           : 2026-08-28 (run #94) y 2026-08-29 (run #95)
Duración de las fallas      : ~3-4 segundos (demasiado rápido para timeout de
                               red/GDELT — steps de fetch tienen
                               continue-on-error: true, así que la falla real
                               ocurre en checkout/setup-python o en el commit)
Logs                        : no disponibles vía GitHub MCP (404) — revisar
                               manualmente en github.com/abdielg08/wiki_agro/actions
Corrida de hoy (2026-08-30) : aún no registrada al momento de esta sesión
Causa raíz                  : sin confirmar — requiere revisión manual del run
                               (este token no tiene permiso actions:write para
                               relanzarlo)
Acción recomendada          : revisar logs del run #94/#95 en la UI de GitHub y
                               corregir; considerar relanzar manualmente
                               (workflow_dispatch)
```

### Contaminación de falsos positivos — causa raíz encontrada y corregida hoy

```
Síntoma   : artículos claramente ajenos a Panamá/agro entrando a la cola con
            source="prensa.com", country="PA" (Malasia, Utah/EE.UU., España,
            Mozambique, catálogos taxonómicos antiguos de Brasil)
Causa     : scripts/fetch_news.py::fetch_ddg_search() no verificaba que la URL
            devuelta por ddgs.news() perteneciera realmente al dominio pedido
            con "site:". "MIDA" también es la sigla de la autoridad de
            inversiones de Malasia, y varios search_terms son genéricos.
Fix       : se agregó verificación de dominio (urlparse) antes de aceptar un
            resultado de fetch_ddg_search(). Aplicado 2026-08-30.
Pendiente : los artículos ya en cola no se limpian automáticamente
            (sources/ es inmutable) — se seguirán filtrando manualmente
            artículo por artículo en cada sesión de ingesta.
```

### Bug en mark-ingested / mark-all-ingested — encontrado y corregido hoy

```
Síntoma   : mark-all-ingested --limit 5 marcaba artículos DISTINTOS a los que
            ingest --limit 5 había mostrado en pending_ingest.md (los que
            Claude realmente procesó quedaban ingested=false, y otros 5 sin
            relación quedaban ingested=true sin contenido en wiki/).
Causa     : mark_all_ingested() no aplicaba prioritize(), a diferencia de
            ingest (run_prepare()); además mark_ingested() individual
            crasheaba con AttributeError por no excluir la clave interna
            _gdelt_windows de processed.json.
Fix       : scripts/ingest.py — mark_all_ingested() ahora usa prioritize()
            igual que run_prepare(); mark_ingested() ahora usa
            article_entries(). Aplicado 2026-08-30. Ver wiki/log.md para el
            detalle completo del incidente y la corrección de estado.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

76 ventanas GDELT completadas según `sources/processed.json` (`_gdelt_windows`),
superando el estimado original de 45. La tabla trimestral detallada de la
versión anterior de este archivo no reflejaba el estado real y se retira hasta
que una sesión futura audite `_gdelt_windows` año por año y reconstruya la
tabla con datos reales (ventanas cubiertas vs. faltantes, artículos por
ventana).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Falsos positivos rechazados | Pendientes restantes | Nota |
|-------|---------------------|------------------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 7 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-30 (routine) | 9 | 2 (1 detectado en pending_ingest.md + 1 recuperado del incidente mark-all-ingested) | 28 | Corrigió causa raíz de contaminación en fetch_news.py y un bug de selección en mark_all_ingested()/mark_ingested() (ver log.md) |

---

## Instrucciones para la Routine

Al ejecutar, la routine DEBE:

1. Correr `python wiki_agro.py stats` y copiar los números aquí
2. Si ingestó artículos: actualizar la tabla "Historial de Sesiones"
3. Si pendientes = 0: actualizar "Estado del Fetch" con diagnóstico
4. Actualizar "last_updated" en el frontmatter
5. Si `Ventanas GDELT completadas` subió: actualizar tabla de Backfill
6. **Nunca ejecutar `mark-all-ingested` sin haber creado antes el contenido
   correspondiente en `wiki/` para cada artículo real, ni sin documentar en
   `wiki/log.md` cada falso positivo rechazado.** Verificar con `stats`/`queue`
   que los URLs marcados coinciden con los de `pending_ingest.md` (ver bug
   corregido 2026-08-30 en el log)

**Señal de alarma**: si "Días sin artículos nuevos" llega a 3, la routine debe:
- Revisar el último log de GitHub Actions (ver wiki/log.md para contexto)
- Identificar si el problema es GDELT rate-limit, RSS caído, o config
- Documentar el diagnóstico en wiki/log.md con pasos para resolverlo

> **Activada 2026-08-30**: ver diagnóstico de "Estado del Fetch" arriba —
> 2 corridas consecutivas de GitHub Actions fallaron (2026-08-28, 2026-08-29).
> Requiere revisión manual de logs en GitHub (este agente no tiene permiso
> actions:write para relanzar el workflow ni acceso a los logs ya expirados).
