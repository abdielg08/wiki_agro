---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-10
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 | **0 nuevos** (fix aplicado hoy, ver abajo) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 63 / ~45 estimadas | 45 (2015→hoy) — **rango agotado** |
| Días sin artículos nuevos REALES | ~78 (desde semilla 2026-05-24) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions verificada : 2026-08-09 11:20 UTC — completed/success
Estado de Actions                 : Corriendo diariamente sin fallar (cron 11:00 UTC)
Resultado                         : 0 artículos reales nuevos (antes del fix de hoy,
                                     todo lo "nuevo" era falso positivo vía DDG)

Causa raíz (identificada 2026-08-10):
  1. fetch_ddg_search() en scripts/fetch_news.py NO aplicaba los filtros
     _is_panama_related()/_is_blocked_domain() que sí usan RSS y GDELT.
  2. El operador site:prensa.com de DuckDuckGo no restringe el dominio real
     de los resultados (llegaban de sltrib.com, heraldo.es, paultan.org...).
  3. La query de "prensa_agro" incluye el término "MIDA", que colisiona con
     Malaysian Investment Development Authority y Utah Military Installation
     Development Authority — ninguno es MIDA Panamá.
  → Resultado: 100% de los 23 artículos aportados por la fuente prensa.com
    desde el inicio del proyecto son falsos positivos. Cero contenido real.

Fix aplicado: se agregaron los mismos filtros de RSS/GDELT a fetch_ddg_search().

Otros hallazgos del diagnóstico (logs de Actions, run 31310552769):
  - RSS IICA → 0 entradas. RSS LaPrensaGeneral → 0 entradas. Ambos feeds
    llevan tiempo sin devolver nada (posible cambio de URL o feed vacío).
  - DDG a sitios oficiales (oirsa.org, mida.gob.pa, idiap.gob.pa,
    bda.gob.pa, fao.org, bancomundial.org, iica.int) → "No results found"
    en las 7 búsquedas. Ninguna aporta actualmente.
  - GDELT: ventanas 2015-01-01→2017-03-29 (7) y la ventana actual
    (2026-06-18→hoy) reciben 403/429 en cada corrida — rate-limited, no
    agotamiento de rango. Ventanas 2017-03-30→2026-06-17 (33) ya completas.

Estado post-fix : Pendiente validación en próxima corrida Actions (2026-08-11).
                   Si RSS/DDG oficiales y GDELT siguen sin aportar, el
                   backfill automático seguirá estancado — requiere revisión
                   de por qué esas fuentes específicas no responden.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Estado |
|---------|--------|
| 2015-01-01 → 2017-03-29 (7 ventanas trimestrales) | **Bloqueado** — 403/429 en cada corrida, se reintenta a diario sin éxito |
| 2017-03-30 → 2026-06-17 (33 ventanas trimestrales) | **Completado** — descargadas, se saltan en corridas futuras |
| 2026-06-18 → hoy (ventana actual) | **Bloqueado** — 403/429 en cada corrida |
| **TOTAL** | **63 ventanas marcadas completas** (33 confirmadas + 30 heredadas de corridas previas al 2026-06-22) |

> El rango 2015-2017 no está agotado por fechas — GDELT lo está bloqueando
> (403/429) en cada intento desde al menos el 2026-08-08. Si esto persiste,
> revisar si hace falta backoff más largo entre requests o si la API cambió
> límites de rate-limiting.
> Ver detalle en `wiki/log.md` (entrada 2026-08-10) y logs de Actions.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-10 | 0 | 0 | Auditoría + rechazo de 16 falsos positivos + fix de raíz en fetch_ddg_search() (faltaban filtros Panamá/dominio bloqueado) |

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
