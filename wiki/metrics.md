---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-14
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 20 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 14 | **0 nuevos** desde el fix de dominio (2026-07-14) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 37 / 47 estimadas | faltan 9 ventanas 2015-01→2017-03 + ventana actual (todas bloqueadas por GDELT) |
| Días sin artículos nuevos | 4 (último: 2026-07-10) | **ALERTA: supera máx 3** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions       : 2026-07-13 (FAILURE — infraestructura del runner, no del código)
Últimas corridas exitosas    : 2026-07-11, 2026-07-12 (success, 0 artículos nuevos en ambas)
Causa "0 artículos nuevos"   : GDELT bloqueado/timeout en TODAS las ventanas intentadas
                                ("GET blocked (403/429)" y "Read timed out" / "Max retries exceeded")
                                RSS IICA y LaPrensaGeneral devolvieron 0 entradas
                                DDG búsquedas por sitio oficial (mida/idiap/bda/fao/bancomundial/
                                iica/oirsa) devolvieron "No results found" en las 7
Falsos positivos "prensa.com": 14/14 acumulados — ninguna de esas URLs pertenece al dominio
                                prensa.com; causado por que ddgs.news() no honra "site:" combinado
                                con is_agro_relevant() sin chequeo de dominio/Panamá
Fix aplicado (2026-07-14)    : fetch_ddg_search() ahora descarta resultados cuyo dominio no
                                coincide con el `site` solicitado (scripts/fetch_news.py)
                                mark_ingested() corregido — excluía mal la clave _gdelt_windows
                                y crasheaba en toda ejecución (scripts/ingest.py)
Estado post-fix               : Pendiente validación en próxima corrida Actions (2026-07-14 11:00 UTC)
Pendiente de revisar          : RSS IICA/La Prensa devuelven 0 entradas hace varias corridas —
                                posibles feeds caídos o URLs desactualizadas
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1 – 2017 Q1 | 0/9 | 0 | **Bloqueado** — GDELT devuelve 403/429/timeout en cada reintento, nunca se completó |
| 2017 Q2 – 2026 Q2 | 37/37 | 0 relevantes | Completo (ventanas descargadas sin producir artículos agro-Panamá) |
| 2026-06-18 → hoy (ventana en curso) | 0/1 | 0 | **Bloqueado** — 11 intentos parciales registrados (20260618_2026062x...0709), ninguno cerró la ventana |
| **TOTAL** | **37/47** | **0 reales** | **Backfill histórico NO produce contenido real; 0 de las 6 páginas del wiki vienen de GDELT (todas son semilla manual)** |

> Datos exactos de `sources/processed.json → _gdelt_windows` (48 claves): 37 ventanas trimestrales
> 2017-03-30→2026-06-17 completadas pero con 0 artículos agro-Panamá relevantes; 9 ventanas
> trimestrales 2015-01-01→2017-03-29 nunca completadas (bloqueo persistente); 11 entradas sueltas
> `20260618_202606xx`/`202607xx` que son reintentos parciales de la ventana "actual" con fecha de
> corte creciente día a día — nunca se cierra limpiamente porque GDELT bloquea/hace timeout antes
> de terminar. Esto último sugiere un bug menor: el fetcher no reutiliza/limpia la clave de la
> ventana en curso entre corridas, solo acumula entradas nuevas — revisar en próxima sesión de
> mantenimiento si no es urgente para el backfill en sí.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-14 | 0 (7 falsos positivos descartados) | 0 | Fix de dominio en fetch_ddg_search + fix de bug en mark_ingested; diagnóstico de bloqueo GDELT y RSS caído |

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
