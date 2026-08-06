---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-06
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 | **0 nuevos desde el fix del 2026-08-06** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 62 (36 trimestres reales + 26 re-registros de la ventana final, ver diagnóstico) | 46-47 (2015→hoy) |
| Días sin artículos nuevos reales | 7 (último real: 2026-07-30) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-06 12:51 UTC — completed / success
Resultado               : Actions corre diariamente sin errores, pero casi todo
                          lo que trae la fuente DDG "prensa_agro" son falsos
                          positivos (0 artículos reales aprovechables desde 2026-07-30)
Causa identificada      : fetch_ddg_search() (fuente "prensa_agro", búsqueda
                          DuckDuckGo site:prensa.com) no aplicaba el filtro
                          _is_panama_related() que sí tienen RSS y GDELT. El
                          filtro site: de DDGS no se respeta de forma confiable
                          en el endpoint de noticias, así que colaban artículos
                          de agricultura de España, Arabia Saudita, Brasil, Irán,
                          Malasia y EE.UU. — muchos coincidiendo solo por la
                          sigla "MIDA" (homónima en Utah/EE.UU. y en el
                          ministerio malasio MITI/MARii).
Fix aplicado             : scripts/fetch_news.py, fetch_ddg_search() ahora aplica
                          _is_blocked_domain() y _is_panama_related() antes de
                          aceptar un resultado, igual que RSS/GDELT.
Estado post-fix          : Pendiente validación en próxima corrida Actions
                          (2026-08-07). Si sigue trayendo 0 artículos reales tras
                          el fix, el problema sería falta de cobertura real de
                          agro panameño en prensa.com, no un bug.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 (completo) | 0/4 | Pendiente — aún no alcanzado por el backfill |
| 2016 (completo) | 0/4 | Pendiente — aún no alcanzado por el backfill |
| 2017-03 → 2026-06 | 36/36 | Completo — ventanas trimestrales cerradas, sin nuevos artículos GDELT relevantes de Panamá encontrados en la mayoría |
| 2026-06-18 → hoy (ventana final, abierta) | 1 en progreso | Se re-consulta cada corrida diaria hasta cumplir 90 días; ver nota de bug abajo |

> **Nota (2026-08-06, verificado con logs reales de Actions run 31103200058)**:
> `processed.json._gdelt_windows` tiene 62 entradas, no 46-47, porque la ventana
> final (iniciada 2026-06-18) genera una window_key nueva cada día — su `end` es
> `utcnow()-1d`, que avanza a diario, y el key incluye esa fecha. Son 26
> re-registros de la misma ventana abierta, no 26 ventanas nuevas.
>
> Las 8 ventanas de 2015-2016 **SÍ fallan por bloqueo real de GDELT (HTTP 403/429)**
> — confirmado en el log de la corrida de hoy: cada ventana de 2015-2016 devuelve
> `GET blocked (403/429)` o error de red y se reintenta (sin éxito) en cada corrida
> diaria. Esto contradice el comentario en el código ("IPs de GitHub Actions no
> bloqueadas") — GDELT SÍ está limitando la tasa incluso desde Actions. La ventana
> final de hoy (2026-06-18 → 2026-08-05) también fue bloqueada con 403/429,
> probablemente por acumulación de rate-limit dentro de la misma corrida (8+
> intentos seguidos a la misma API en ~5 minutos antes de llegar a ella).
> El backfill real 2017-03→2026-06 (36 ventanas) sí está completo. No es
> agotamiento del rango de fechas — es un problema de rate-limiting de GDELT que
> desperdicia ~5 de los ~6 minutos del step de fetch diario reintentando ventanas
> viejas que nunca cerrarán así. Recomendación para una futura sesión: agregar
> backoff/espera más larga entre ventanas de GDELT, o saltar directamente a la
> ventana más reciente cuando las más viejas fallan repetidamente, para no gastar
> el tiempo de la corrida diaria reintentando 2015-2016 sin éxito.
>
> Hallazgo adicional: los feeds RSS (IICA, La Prensa) devolvieron 0 entradas hoy,
> y 7 de las 8 búsquedas DDG configuradas (`oirsa_alertas`, `mida_noticias`,
> `idiap_investigacion`, `bda_credito`, `fao_panama`, `banco_mundial_pa`,
> `iica_panama`) devuelven sistemáticamente "No results found" — solo `prensa_agro`
> devolvía resultados (y eran los falsos positivos ya corregidos). Esto sugiere que
> el filtro `site:` de DDGS no funciona de forma confiable para ninguna búsqueda
> configurada; no es solo el problema de falsos positivos ya corregido, sino que
> probablemente estas 7 fuentes nunca han aportado un solo artículo. Queda como
> diagnóstico para una futura sesión — no se tocó en esta sesión más allá del fix
> de `_is_panama_related()`.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-06 | 0 | 0 | 16/16 pendientes eran falsos positivos (0 páginas nuevas). Bugfix `mark_ingested()`. Fix root-cause en `fetch_ddg_search()` (faltaba filtro `_is_panama_related`). Diagnóstico confirmado con logs de Actions: GDELT 403/429 en ventanas 2015-2016; 7/8 búsquedas DDG nunca devuelven resultados; RSS IICA/La Prensa en 0 hoy |

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
