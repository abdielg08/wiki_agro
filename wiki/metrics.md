---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-08
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 19 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 14 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 46 registradas, pero gap real 2015-2017 (ver tabla de Backfill) | cobertura continua 2015→hoy |
| Días sin artículos nuevos | 3+ (07-08, 07-04, 07-03 sin nuevos) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-08 (b46e6af) — corrió, 0 artículos nuevos
Corridas previas        : 2026-07-04 (0), 2026-07-03 (0), 2026-07-02 (1)
Causa raíz identificada (sesión 2026-07-08):
  1) _gdelt_windows = 46 (>= 45 estimadas) → el backfill GDELT 2015-hoy está
     AGOTADO. Ya no hay ventanas nuevas que consultar; necesita expansión de
     rango o cambio de estrategia de fetch para seguir avanzando.
  2) Bug en fetch_ddg_search() (scripts/fetch_news.py): la búsqueda DDG con
     "site:prensa.com <query>" NO estaba filtrando resultados por dominio —
     ddgs.news() ignora el operador site: y devuelve resultados de cualquier
     dominio. Combinado con la keyword "MIDA" en la query (pensada para
     Ministerio de Desarrollo Agropecuario de Panamá), esto trajo artículos de
     sltrib.com (Utah, "MIDA" = Military Installation Development Authority) y
     spa.gov.sa (Arabia Saudita), todos mal-etiquetados con source="prensa.com"
     y country="PA" por el propio fetcher (source/country se asignan desde el
     config, no desde la URL real).
     Resultado: 7/7 artículos pendientes de esta sesión fueron falsos
     positivos (100%) — ver wiki/log.md 2026-07-08.
  3) Bug adicional en mark_all_ingested() (scripts/ingest.py): usaba un orden
     distinto al de `ingest`, por lo que `mark-all-ingested --limit 5` podía
     marcar como ingestado un artículo que Claude Code nunca revisó (ocurrió
     con nyfb.org / "New York Farm Bureau" en esta sesión). Corregido para
     usar el mismo orden por score que `ingest`.
Fix aplicado (esta sesión):
  - fetch_ddg_search() ahora valida que el dominio real de cada resultado
    (urlparse(url).netloc) coincida con el `site` configurado antes de
    aceptarlo; descarta silenciosamente lo que no coincide.
  - mark_all_ingested() ahora usa prioritize(strategy="score"), igual que
    ingest, para que --limit N marque exactamente lo que se mostró.
  - mark_ingested() ahora excluye claves internas (_gdelt_windows) al iterar
    processed.json, corrigiendo un AttributeError.
Pendiente: expandir el rango de ventanas GDELT (o definir nueva fuente de
  backfill) ya que faltan ~2 años de cobertura real (ver tabla de Backfill).
Estado post-fix: Pendiente validación en próxima corrida Actions.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

Basado en `_gdelt_windows` de `sources/processed.json` (46 ventanas registradas, 2026-07-08):

| Período | Estado |
|---------|--------|
| 2015-02-19 → 2017-03-29 | **NO cubierto — gap real, nunca se consultó GDELT** |
| 2017-03-30 → 2026-06-17 | Cubierto — 37 ventanas trimestrales consecutivas completadas |
| 2026-06-18 → 2026-07-07 | Cubierto (con redundancia) — 9 ventanas con el mismo ancla de inicio (20260618) y fin creciente día a día, en vez de ventanas trimestrales limpias |
| **TOTAL** | **46 ventanas registradas, pero cobertura real 2015→hoy incompleta** |

**Hallazgo (sesión 2026-07-08)**: el conteo de 46 ventanas hizo pensar que el
backfill estaba "agotado" (≥45 estimadas), pero en realidad:
- Faltan ~2 años (2015-02-19 a 2017-03-29) que nunca se consultaron — el
  primer `fetch-historical` documentado empezó en 2017-03-30, no en 2015.
- Las 9 ventanas recientes (`20260618_*`) son casi duplicadas entre sí (mismo
  inicio, fin incremental un día a la vez) en vez de avanzar el inicio — esto
  infla el conteo sin aportar cobertura nueva real.

**Acción recomendada para próxima sesión**: disparar manualmente el workflow
`Wiki Agropecuario — Crawl Histórico 15 Años` (`wiki_historical.yml`) con
`years: "2015-2017"`, `mode: gdelt` para cerrar el gap 2015-2017. Requiere
`workflow_dispatch` manual — no se ejecutó en esta sesión porque puede tardar
horas y consumir minutos de Actions; se documenta aquí para decisión humana.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-08 | 0 | 0 | 7/7 pendientes eran falsos positivos (bug DDG site: filter) + fixes en fetch_news.py y ingest.py (mark_ingested, mark_all_ingested) |

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
