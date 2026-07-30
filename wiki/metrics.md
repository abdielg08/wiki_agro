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
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 12 (7 previos + 5 hoy) | **0 nuevos** (ver diagnóstico) |
| Pendientes de ingesta | 11 (todos falsos positivos conocidos, fuente `prensa.com` rota) | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 59 / ~45-46 estimadas | rango agotado — necesita expansión |
| Días sin artículos nuevos | 0 (Actions corrió hoy, 2026-07-30) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-30 (corrió correctamente, 3 artículos nuevos)
Resultado               : 3/3 artículos nuevos = falsos positivos (0 útiles)
Causa identificada       : scripts/fetch_news.py::fetch_ddg_search — el motor de
                          búsqueda de noticias de DDG (ddgs.news) NO respeta el
                          operador "site:", así que la búsqueda "prensa_agro"
                          (site:prensa.com ... OR MIDA OR ...) trae noticias
                          globales que solo calzan por la sigla suelta "MIDA"
                          (Malasia, Utah, etc.) — NINGUNO de los 23 artículos
                          guardados bajo source="prensa.com" es realmente de
                          prensa.com (auditoría 2026-07-30: 0/23).
Fix aplicado (hoy)      : se agregó el mismo filtro de dominio/Panamá que ya
                          usan RSS y GDELT (_is_blocked_domain, _is_panama_related)
                          a fetch_ddg_search — antes solo corría is_agro_relevant.
Ventanas GDELT           : 59 registradas en _gdelt_windows, pero NO distribuidas
                          uniformemente 2015→hoy:
                            - 2017-2025: 4/4 ventanas completas cada año (36 total)
                            - 2015-2016: 0/8 ventanas — el objetivo real de cobertura
                              (2015-02-19) NUNCA se ha alcanzado
                            - 2026: 23 ventanas casi-duplicadas, todas con el mismo
                              inicio (~2026-06-18) y fin creciente día a día
Causa (ventanas 2015-16) : fetch_gdelt_historical() no marca completa una ventana
                          si fetch_gdelt_batch() devuelve None (error de red), pero
                          sí avanza `current` DENTRO de esa misma corrida — así que
                          cada día reintenta 2015-2016 desde cero y sigue avanzando
                          por el resto del rango en la misma ejecución. Si GDELT
                          falla consistentemente para esas fechas (posible límite
                          de antigüedad de la API), quedan huérfanas para siempre
                          sin quedar registradas como error en ningún log persistente.
Causa (ventanas 2026)    : el `end` del rango se recalcula cada día como
                          `utcnow()-1día`, así que la ventana final (aún no cerrada
                          por 90 días) genera una clave nueva casi idéntica cada
                          ejecución en vez de extender/reemplazar la anterior —
                          no pierde artículos, pero infla _gdelt_windows sin sentido.
Pendiente                : (1) validar en próxima corrida de Actions que la fuente
                          "prensa_agro" deje de traer basura; (2) investigar por qué
                          GDELT falla para 2015-2016 (correr fetch --mode gdelt
                          manualmente y revisar el error real, no solo el log de
                          consola); (3) opcional: dedupear/limpiar las ventanas
                          2026 con el mismo inicio.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 | 0/4 | **Pendiente — nunca completado, falla de red persistente** |
| 2016 | 0/4 | **Pendiente — nunca completado, falla de red persistente** |
| 2017 | 4/4 | Completo |
| 2018 | 4/4 | Completo |
| 2019 | 4/4 | Completo |
| 2020 | 4/4 | Completo |
| 2021 | 4/4 | Completo |
| 2022 | 4/4 | Completo |
| 2023 | 4/4 | Completo |
| 2024 | 4/4 | Completo |
| 2025 | 4/4 | Completo |
| 2026 (hasta hoy) | 23 ventanas (con solapes, ver diagnóstico) | En progreso |
| **TOTAL** | **59 registradas** | **2015-2016 son el bloqueo real para la meta de cobertura** |

> Nota: ninguna de las ventanas GDELT (2017-2026) generó artículos nuevos en el wiki —
> el filtro `_is_panama_related`/`_is_blocked_domain` ya se aplica ahí, así que su score
> de falsos positivos es 0%, pero tampoco se han revisado los artículos crudos que sí
> trajeron (si trajeron alguno) — ver `sources/articles/` con `source` distinto de
> `prensa.com`, `MIDA`, `BDA`, `IICA`, `TVNNoticias`, `LaPrensaEco`.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-30 | 0 reales, 5 falsos positivos revisados y descartados | 11 (todos falsos positivos conocidos) | Encontrado y corregido bug raíz en `fetch_ddg_search` (no filtraba por dominio/Panamá); corregido bug en `mark-ingested` (crasheaba con `_gdelt_windows`); diagnosticado hueco GDELT 2015-2016 (0/8 ventanas, nunca completadas) |

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
