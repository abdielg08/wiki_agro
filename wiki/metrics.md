---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-17
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 22 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 16 (7 previos + 9 hoy) | **0 nuevos** (bug causante corregido hoy) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 49 (36 trimestres reales 2017Q1–2026Q2 + 13 duplicados de cola, ver abajo) | 45 (2015→hoy) |
| Días sin artículos nuevos (reales) | 54+ (desde 2026-05-24) | máx 3 antes de diagnosticar |

**Alerta activa**: el pipeline automático (GitHub Actions, 3 corridas configuradas) no ha
producido NINGÚN artículo real desde el lote semilla del 2026-05-24. Los 16 artículos
recolectados automáticamente desde entonces fueron 100% falsos positivos por un bug en
`fetch_ddg_search()` (ver abajo) — corregido en esta sesión (2026-07-17). El rendimiento
real del fix se validará en la próxima corrida del workflow diario.

---

## Estado del Fetch (GitHub Actions) — actualizado 2026-07-17

```
Última corrida Actions      : 2026-07-17 12:02 UTC (run 29578858522) — status: success (exit 0)
Resultado                   : 0 artículos nuevos guardados
Corridas recientes (7d)     : todas "success" excepto 2026-07-13 (failure) — pero
                               "success" NO implica artículos nuevos: el job puede
                               terminar en verde sin guardar nada.

Causas identificadas HOY:

1. [CRÍTICO — CORREGIDO] fetch_ddg_search() no validaba el dominio real de los
   resultados de DDGS().news() contra el `site:` configurado, ni aplicaba
   _is_blocked_domain()/_is_panama_related() (filtros que sí tienen fetch_rss() y
   fetch_gdelt_historical()). Con el término ambiguo "MIDA" en search_terms.primary
   (coincide con Panamá, Utah "Military Installation Development Authority" y Malaysia
   "Investment Development Authority"), la búsqueda "site:prensa.com ... MIDA ..." dejó
   pasar 16 artículos de sltrib.com, paultan.org, unesco.org, nyfb.org, spa.gov.sa,
   ieeexplore.ieee.org — ninguno de prensa.com ni de Panamá.
   Fix: scripts/fetch_news.py::fetch_ddg_search() ahora rechaza resultados fuera del
   dominio configurado y aplica los mismos filtros de dominio/Panamá que RSS y GDELT.

2. [ACTIVO — sin resolver] GDELT devuelve error de red / 403 en la mayoría de las
   ventanas en cada corrida reciente. La corrida del 2026-07-17 hizo 10 requests a
   GDELT — las 10 fallaron (9 ventanas 2015-01→2017-03 + la ventana incremental
   2026-06-18→2026-07-16). Las ventanas 2015-01-01→2017-03-29 (9 ventanas) NUNCA han
   completado desde el inicio del proyecto — cada corrida las reintenta desde cero y
   vuelve a fallar antes de llegar a ventanas más recientes. Posible rate-limit/bloqueo
   de GDELT hacia las IPs de GitHub Actions, agravado por reintentar siempre las mismas
   9 ventanas fallidas primero. Sin datos suficientes aún para descartar bloqueo
   permanente vs. transitorio — monitorear próximas 3 corridas.

3. [ACTIVO — sin resolver] 7 de 8 búsquedas DDG restringidas a sitio (oirsa.org,
   mida.gob.pa, idiap.gob.pa, bda.gob.pa, fao.org, bancomundial.org, iica.int)
   devuelven "No results found" de forma consistente. Solo "prensa_agro" devuelve
   resultados (antes del fix de hoy, fuera de dominio). Posible que ddgs no soporte
   bien `site:` para estos dominios, o que genuinamente no haya contenido reciente
   indexado — requiere prueba manual fuera de CI para diferenciar.

4. [Sin diagnosticar aún] RSS IICA y LaPrensaGeneral devolvieron 0 entradas en la
   corrida del 2026-07-17. Podría ser normal (sin posts nuevos) o señal de feed roto —
   monitorear si persiste 3+ días.

Bug adicional corregido: `mark_ingested` (scripts/ingest.py) fallaba con
AttributeError al iterar processed.items() sin filtrar `_gdelt_windows` (lista interna).
Corregido para usar article_entries().

Estado post-fix: pendiente validar en la corrida de mañana si fetch_ddg_search() ahora
sí trae artículos reales de prensa.com (o si, al aplicar los filtros correctos, el
volumen cae a ~0 — lo cual sería correcto si no hay contenido agro-Panamá disponible
ese día, y preferible a seguir acumulando falsos positivos).
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1 – 2017 Q1 | 0/9 | 0 | **Bloqueado** — cada corrida reintenta y falla (red/403) antes de llegar a ventanas más nuevas |
| 2017 Q2-Q4 | 3/3 | ? | Completo |
| 2018 Q1-Q4 | 4/4 | ? | Completo |
| 2019 Q1-Q4 | 4/4 | ? | Completo |
| 2020 Q1-Q4 | 4/4 | ? | Completo |
| 2021 Q1-Q4 | 4/4 | ? | Completo |
| 2022 Q1-Q4 | 4/4 | ? | Completo |
| 2023 Q1-Q4 | 4/4 | ? | Completo |
| 2024 Q1-Q4 | 4/4 | ? | Completo |
| 2025 Q1-Q4 | 4/4 | ? | Completo |
| 2026 Q1 | 1/1 | ? | Completo (20260319–20260617) |
| 2026 Q2 (parcial) | 0/1 | 0 | **Bloqueado** — ventana 20260618→hoy reintentada diariamente con fecha final creciente, nunca completa (13 entradas de cola en `_gdelt_windows`, ver log 2026-07-17) |
| **TOTAL real** | **36/46 trimestres** | **0 artículos GDELT en wiki (todos vía DDG/RSS semilla)** | **Backfill 2017-Q2→2026-Q1 aparentemente completo; 2015–2017Q1 y la cola 2026-Q2 bloqueados** |

> "Artículos" quedó en "?" porque no hay forma de atribuir, en `sources/processed.json`,
> qué artículos entraron por GDELT vs. RSS vs. DDG una vez guardados (no se registra la
> fuente del fetcher). Los 6 artículos reales en el wiki son del lote semilla manual, no
> de GDELT. Investigar si GDELT ha aportado artículos reales alguna vez, o si los
> "0/46 → 36/46" ventanas completas solo devolvieron 0 resultados cada vez
> (`fetch_gdelt_batch` marca la ventana completa aunque el batch esté vacío).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-17 | 0 | 0 | 9/9 pendientes eran falsos positivos (bug de fuga de dominio en DDG, ver log). Fix aplicado a fetch_ddg_search() + bug de mark_ingested corregido. GDELT bloqueado (0 artículos, 10/10 requests fallidas). |

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
