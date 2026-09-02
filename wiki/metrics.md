---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-02
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 51 | ↑ continuo |
| Artículos ingestados | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 33 | 0 |
| Falsos positivos detectados (no ingestados) | ≥8 (documentados en log.md; quedan en processed.json con `ingested:false`, sin contar como ingestados) | **0 ingestados como si fueran válidos** |
| Páginas en wiki/ | 26 | ↑ continuo |
| Cobertura temporal | 2015-2026 (parcial: fuerte en 2017-2026, sin cobertura 2015-2016 aún) | 2015 → hoy real |
| Ventanas GDELT completadas | 77 / ~46 estimadas para 2015–hoy | cobertura completa 2015→hoy |
| Días sin artículos nuevos | **6** (último artículo nuevo: 2026-08-27) | máx 3 antes de diagnosticar — **⚠ SUPERADO** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions   : 2026-09-02 (run #99, https://github.com/abdielg08/wiki_agro/actions/runs/33644553540)
Resultado                : 0 artículos nuevos (igual que runs #92, #93, #98 — mayoría de días recientes)
Duración del step fetch  : ~6 min 14s

DIAGNÓSTICO (basado en logs reales de Actions, no solo inferencia):

1. RSS — ROTO
   - IICA (https://www.iica.int/es/rss/noticias): GET bloqueado con 403/429 todos los días recientes
   - La Prensa (https://www.prensa.com/feed/): devuelve 0 entradas en el feed (posible feed vacío o URL desactualizada)

2. Búsqueda Web DuckDuckGo (ddgs) — ROTO
   - Las 7 queries configuradas (prensa_agro, oirsa_alertas, mida_noticias, idiap_investigacion,
     bda_credito, fao_panama, banco_mundial_pa, iica_panama) devuelven "No results found" en la
     corrida del 2026-09-02. Posible bloqueo/rate-limit del proveedor DDG hacia la IP de GitHub
     Actions, o cambio en la librería `ddgs`. Sin resultados en NINGUNA query = sospechoso de bloqueo
     total, no de falta real de resultados.

3. GDELT — PARCIALMENTE ROTO (timeouts de conexión, no 403)
   - Ventanas 2015-01-01 → 2016-12-28 (8 ventanas trimestrales): fallan con
     `ConnectTimeoutError` / `Read timed out` en TODAS las corridas registradas desde el inicio del
     proyecto (0/8 completadas en ~99 corridas). Nunca se han descargado artículos de este rango.
   - Ventanas 2017-01-01 → 2026-06-17 (36 ventanas): YA completadas exitosamente en corridas pasadas
     (se saltan con "ya descargado", sin nueva llamada de red).
   - Ventana viva más reciente (2026-06-18 → hoy): **también falla con timeout** en la corrida del
     2026-09-02 (`ConnectTimeoutError`, 30s), igual que las de 2015-2016.
   - Conclusión: la falla NO es específica de fechas antiguas (no es "GDELT no cubre 2015-2016");
     es una falla de conectividad/rate-limit hacia `api.gdeltproject.org` que afecta TODAS las
     llamadas de red en la corrida actual, tanto pasado lejano como ventana reciente. Consistente con
     rate-limiting de GDELT hacia la IP de los runners de GitHub Actions tras ~99 corridas diarias
     acumuladas, o inestabilidad temporal del servicio GDELT.
   - Efecto colateral: cada corrida diaria gasta ~3-4 min reintentando las 8 ventanas 2015-2016 que
     nunca han funcionado, sin avanzar el backfill.

4. World Bank API: corre sin errores visibles en el log, pero no se ve que aporte artículos nuevos
   recientemente.

5. Infraestructura: las corridas #94-#97 (2026-08-28 a 2026-08-31) terminaron en "failure" en ~4
   segundos (antes de completar el checkout), consistente con una falla transitoria del runner de
   GitHub Actions no relacionada con el código — no hay logs disponibles para confirmar la causa raíz
   (HTTP 404 al pedirlos). Esto explica parte de la falta de commits en esos días.

RECOMENDACIONES (no aplicadas aún — requieren validación contra la red real, no disponible desde
esta sesión de Claude Code, que corre en un entorno con egress restringido a api.gdeltproject.org):
   - Añadir backoff/circuit-breaker en `fetch_gdelt_historical()` (scripts/fetch_news.py) para dejar
     de reintentar ventanas 2015-2016 en cada corrida si llevan N fallos consecutivos (revisar
     periódicamente, no en cada ejecución diaria) — liberaría tiempo de ejecución.
   - Investigar si `api.gdeltproject.org` requiere un intervalo mínimo entre requests mayor al
     REQUEST_DELAY actual, o si hay un límite diario de requests por IP.
   - Revisar por qué el feed RSS de La Prensa devuelve 0 entradas (¿URL cambió? ¿requiere headers
     distintos?) y por qué IICA devuelve 403/429 (¿user-agent bloqueado?).
   - Revisar la librería `ddgs` — 0/7 queries con resultados es atípico incluso para búsquedas de
     nicho.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 Q1-Q4 | 0/4 | **Bloqueado — timeout de conexión en cada intento, nunca ha funcionado** |
| 2016 Q1-Q4 | 0/4 | **Bloqueado — mismo problema** |
| 2017 Q1-Q4 | 4/4 | ✓ Completado |
| 2018 Q1-Q4 | 4/4 | ✓ Completado |
| 2019 Q1-Q4 | 4/4 | ✓ Completado |
| 2020 Q1-Q4 | 4/4 | ✓ Completado |
| 2021 Q1-Q4 | 4/4 | ✓ Completado |
| 2022 Q1-Q4 | 4/4 | ✓ Completado |
| 2023 Q1-Q4 | 4/4 | ✓ Completado |
| 2024 Q1-Q4 | 4/4 | ✓ Completado |
| 2025 Q1-Q4 | 4/4 | ✓ Completado |
| 2026 (hasta 2026-06-17) | 4/4 | ✓ Completado |
| 2026-06-18 → hoy (ventana viva) | 0/1 | **Bloqueado — timeout, reintentada cada día sin éxito desde ~2026-06-18** |
| **TOTAL** | **36/46 ventanas históricas completas + ventana viva estancada** | **2015-2016 nunca cubiertos; sin artículos nuevos desde 2026-08-27** |

> **BUG CONFIRMADO en `sources/processed.json["_gdelt_windows"]`** (verificado contando las 77
> entradas): 36 corresponden a las ventanas trimestrales 2017-2025 (4/año, normal) + 1 a
> `20260319_20260617` (Q1-Q2 2026, normal) + **40 entradas todas con el mismo inicio `20260618`
> y fin distinto** (`20260623`, `20260624`, `20260626`, ... hasta `20260831`, casi una por día).
> Esto revela el bug de raíz en `fetch_gdelt_historical()` (scripts/fetch_news.py): la ventana
> "viva" (más reciente) usa `end = min(config_end, ayer)`, que crece un día cada corrida, pero
> `current` (el inicio de la ventana) solo avanza cuando la ventana COMPLETA tiene éxito. Como el
> `window_key` incluye la fecha de fin, cada día que la ventana tiene éxito genera una clave NUEVA
> (con el mismo inicio pero un fin mayor) en vez de reutilizar/avanzar la anterior — así, casi cada
> día de fines de junio a agosto 2026 se volvió a descargar por completo un rango que ya se había
> descargado el día anterior (trabajo redundante), Y la ventana nunca "cierra" un trimestre real:
> sigue creciendo indefinidamente (ya lleva 76+ días, `20260618`→`20260901`) hasta que un día falla
> (como hoy, 2026-09-02) y queda atascada — y como el rango a reintentar es cada vez más grande,
> cada vez es más probable que vuelva a fallar por timeout. Esto explica tanto el desperdicio de
> requests como el estancamiento total desde ~2026-08-31/09-01.
> **Recomendación de fix** (no aplicado — requiere prueba contra la red real de GDELT, no
> disponible desde este entorno): usar ventanas de tamaño fijo también para el tramo "vivo" (p.ej.
> trimestres de 90 días igual que el resto, aceptando quedarse unos días detrás de "hoy"), en vez
> de una ventana que crece con `end = ayer` cada corrida.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-02 | 5 (0 falsos positivos ingestados; 3 falsos positivos adicionales detectados y documentados) | 33 | Ingesta + bugfix `mark-ingested` + diagnóstico completo del fetch con logs reales de Actions (RSS roto, DDG roto, GDELT con timeouts en 2015-2016 y en la ventana viva) |

---

## Instrucciones para la Routine

Al ejecutar, la routine DEBE:

1. Correr `python wiki_agro.py stats` y copiar los números aquí
2. Si ingestó artículos: actualizar la tabla "Historial de Sesiones"
3. Si pendientes = 0: actualizar "Estado del Fetch" con diagnóstico
4. Actualizar "last_updated" en el frontmatter
5. Si `Ventanas GDELT completadas` subió: actualizar tabla de Backfill

**Señal de alarma**: si "Días sin artículos nuevos" llega a 3, la routine debe:
- Revisar el último log de GitHub Actions (ver wiki/log.md para contexto) — usar las herramientas
  MCP de GitHub (`actions_list` + `get_job_logs`) para leer el log real del step "Fetch artículos
  nuevos", no solo el mensaje del commit
- Identificar si el problema es GDELT rate-limit, RSS caído, o config
- Documentar el diagnóstico en wiki/log.md con pasos para resolverlo

**Estado 2026-09-02**: la señal de alarma está activa (6 días sin artículos nuevos, supera el
máximo de 3). Diagnóstico completo documentado arriba y en wiki/log.md. Causa raíz: fallas de
conectividad hacia GDELT y bloqueos en RSS/DDG, no un problema del wiki en sí. Acción pendiente:
alguien con acceso a modificar y probar `scripts/fetch_news.py` contra la red real debe aplicar las
recomendaciones de backoff/investigación listadas arriba.
