---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-02
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 18 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 12 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 42 / ~46 estimadas | 46 (2015→hoy) |
| Días sin artículos nuevos | 2 (2026-06-30, 2026-07-01) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions       : 2026-07-01 13:31 UTC (run #36) — completed/success
Última corrida con commit    : 2026-06-29 14:50 UTC (f4223e5, +1 artículo)
Resultado runs #35 y #36     : 0 artículos nuevos, 0 commits (ni siquiera cambió
                                processed.json — ninguna ventana GDELT se completó)
Causa identificada            : GDELT bloqueando/timeouteando casi todas las
                                requests del runner de GitHub Actions:
                                "GET blocked (403/429): api.gdeltproject.org" y
                                "Read timed out" / "Max retries exceeded" en
                                prácticamente cada ventana consultada (incluida
                                la ventana rodante 2026-06-18→hoy).
                                RSS (IICA, La Prensa) devolvió "0 entradas en el
                                feed" en el run #36.
                                Búsqueda DDG (7 queries: prensa_agro, oirsa,
                                mida, idiap, bda, fao_panama, banco_mundial_pa)
                                devolvió "No results found" en todas — DDG
                                también está bloqueando/limitando al runner.
Ventanas GDELT completadas    : 42 — pero las 8 ventanas de 2015-2016 (el inicio
                                real del backfill) llevan varias corridas
                                fallando por timeout/403 y NUNCA se han
                                completado. Las ventanas 2017→2026 sí están
                                completas. Además hay 5 entradas duplicadas de
                                una "ventana rodante" (20260618_2026062{3,4,6,7,8})
                                que se regeneran cada día con fecha final
                                distinta sin aportar artículos — no son ventanas
                                nuevas reales, inflan el contador.
Diagnóstico                   : caso #2 del checklist de CLAUDE.md (GDELT
                                bloqueado), confirmado con evidencia directa de
                                logs de Actions run #36. No es agotamiento del
                                rango — aún faltan 2015-2016 por completar.
Recomendación                 : (a) agregar backoff/retry con espera entre
                                ventanas GDELT para evitar 429; (b) reducir
                                ventanas consultadas por corrida o espaciar
                                requests; (c) revisar por qué DDG devuelve 0
                                resultados en las 7 queries — posible bloqueo
                                por IP compartida de GitHub Actions; (d)
                                deduplicar la lógica de "ventana rodante" para
                                que no infle `_gdelt_windows` sin aportar
                                cobertura real.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | 0 | **Bloqueado** — GDELT 403/timeout en cada intento |
| 2016 Q1-Q4 | 0/4 | 0 | **Bloqueado** — GDELT 403/timeout en cada intento |
| 2017 Q1-Q4 | 4/4 | 0 | Completo (sin artículos PA relevantes) |
| 2018 Q1-Q4 | 4/4 | 0 | Completo (sin artículos PA relevantes) |
| 2019 Q1-Q4 | 4/4 | 0 | Completo (sin artículos PA relevantes) |
| 2020 Q1-Q4 | 4/4 | 0 | Completo (sin artículos PA relevantes) |
| 2021 Q1-Q4 | 4/4 | 0 | Completo (sin artículos PA relevantes) |
| 2022 Q1-Q4 | 4/4 | 0 | Completo (sin artículos PA relevantes) |
| 2023 Q1-Q4 | 4/4 | 0 | Completo (sin artículos PA relevantes) |
| 2024 Q1-Q4 | 4/4 | 0 | Completo (sin artículos PA relevantes) |
| 2025 Q1-Q4 | 4/4 | 0 | Completo (sin artículos PA relevantes) |
| 2026 Q1-Q2 | 2/2 | 0 | Completo (sin artículos PA relevantes) |
| **TOTAL** | **38/46 ventanas reales** | **0** | **GDELT no ha aportado artículos aún; 2015-2016 bloqueados** |

> Nota: `_gdelt_windows` en processed.json reporta 42 entradas, pero 5 son
> duplicados de una "ventana rodante" (2026-06-18 → hoy) que se regenera cada
> día con fecha final distinta — no cuentan como ventanas nuevas. Las 38
> ventanas trimestrales reales de 2017-2026 completaron sin errores pero no
> devolvieron ningún artículo relevante de Panamá vía GDELT hasta ahora; todo
> el contenido ingestado hasta hoy vino de RSS (IICA, La Prensa) y de la
> búsqueda DDG en corridas anteriores, no de GDELT.
> 2015-2016 (8 ventanas) siguen sin completarse — bloqueadas por 403/429 y
> timeouts de la API de GDELT desde el runner de GitHub Actions.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-02 | 0 (5/5 falsos positivos) | 0 | Cola vaciada: 5 artículos de prensa.com sobre Utah/Malasia/NY/Arabia Saudita, ninguno sobre Panamá. Diagnóstico: fetch GitHub Actions corriendo OK pero GDELT bloqueado (403/429/timeout) 2 días seguidos, DDG sin resultados, RSS vacío |

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
