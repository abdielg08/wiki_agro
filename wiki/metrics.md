---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-07
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados (con contenido en wiki/) | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 30 (7 previos + 23 esta sesión) | **0 nuevos** — 100% del batch de hoy lo fue |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 63 | 45-46 estimadas → rango agotado, necesita expansión |
| Días sin artículos nuevos | 0 (Actions corrió hoy) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-07 (commit ff8157d, "0 artículos nuevos")
Resultado               : Actions SÍ corre a diario (ver git log de sources/)

Causa raíz encontrada 2026-08-07 (bug nuevo, distinto al de GDELT 2026-06-22):
  fetch_ddg_search() en scripts/fetch_news.py arma la query como
  `site:{site} {query}`, y {query} trae cláusulas "OR" (ej. "agropecuario
  OR agricultura OR ganadería OR MIDA OR cosecha Panamá"). DuckDuckGo no
  aplica `site:` de forma confiable junto con OR, y el código no validaba
  que la URL devuelta perteneciera al dominio pedido: se etiquetaba
  source=site / country=PA / language=es de forma incondicional para
  CUALQUIER resultado.
  Impacto medido: de 23 artículos jamás revisados etiquetados
  "prensa.com", el 100% resultaron ser falsos positivos (Malasia, Utah,
  España, Brasil, Arabia Saudita, catálogos de archive.org/IEEE/UNESCO).
  Ninguno llegó a generar contenido real de wiki — el gate de ingesta
  manual del LLM los detuvo a todos — pero contaminaron sources/,
  processed.json y las métricas de "artículos descargados".

Fix aplicado 2026-08-07 : fetch_ddg_search() ahora valida que el netloc de
  la URL devuelta coincida con `site` (o sea subdominio de `site`) antes de
  aceptarla; descarta el resto en vez de mal-etiquetarla. También se
  corrigió mark_ingested() en scripts/ingest.py, que crasheaba con
  AttributeError al iterar la clave interna `_gdelt_windows` (lista) sin
  filtrarla vía article_entries().
Estado post-fix         : Pendiente validación en próxima corrida Actions.
  fetch_gdelt_historical() no se ve afectado (usa sourcecountry:PA nativo
  de GDELT).

--- Diagnóstico GDELT (previo, 2026-06-22, aún vigente) ---
Causa identificada      : GDELT ventanas 2026-2027 = fechas futuras → timeout/403
                           RSS IICA y La Prensa devolvieron 0 entradas ese día
Fix aplicado             : fetch_gdelt_historical() ahora limita end a datetime.utcnow()-1d
                           Ventanas GDELT reseteadas a [] para backfill real
Estado 2026-08-07        : 63 ventanas GDELT completadas (> 45-46 estimadas)
                           → el rango histórico 2015-hoy está efectivamente
                           agotado; expandir `coverage.end_year` en
                           config/sources.yaml o aceptar que el backfill
                           histórico llegó a su límite y el avance futuro
                           depende de RSS/DDG diario.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | ? | Pendiente |
| 2016 Q1-Q4 | 0/4 | ? | Pendiente |
| 2017 Q1-Q4 | 0/4 | ? | Pendiente |
| 2018 Q1-Q4 | 0/4 | ? | Pendiente |
| 2019 Q1-Q4 | 0/4 | ? | Pendiente |
| 2020 Q1-Q4 | 0/4 | ? | Pendiente |
| 2021 Q1-Q4 | 0/4 | ? | Pendiente |
| 2022 Q1-Q4 | 0/4 | ? | Pendiente |
| 2023 Q1-Q4 | 4/4 | ? | Completado |
| 2024 Q1-Q4 | 4/4 | ? | Completado |
| 2025 Q1-Q4 | 4/4 | ? | Completado |
| 2026 (parcial, hoy) | 27 ventanas | ? | En progreso (ventanas de cola móvil, normal) |
| **TOTAL (2026-08-07)** | **63 ventanas, tally por año abajo** | **?** | **2015-2016 en 0 — ver alerta** |

**Tally real por año de inicio de ventana** (de `sources/processed.json → _gdelt_windows`):
2015: **0** · 2016: **0** · 2017: 4 · 2018: 4 · 2019: 4 · 2020: 4 · 2021: 4 · 2022: 4 · 2023: 4 · 2024: 4 · 2025: 4 · 2026: 27

⚠️ **ALERTA — 2015 y 2016 tienen 0 ventanas completadas**, pese a que
`fetch_gdelt_historical()` empieza el walk en `date_range.start = 2015-01-01`
en cada corrida. Como el walk solo marca una ventana completa tras una
respuesta HTTP exitosa (aunque tenga 0 resultados) y en error de red la
salta SIN marcarla, la hipótesis más probable es que las ventanas de
2015-2016 fallan sistemáticamente (network/HTTP error) en cada corrida de
Actions y por eso nunca se marcan `completed`, mientras el walk logra
avanzar y completar 2017 en adelante. No se pudo confirmar en vivo desde
este sandbox: `api.gdeltproject.org` está bloqueado por el proxy saliente
de este entorno (403 en el CONNECT), así que la prueba debe hacerse desde
el runner real de GitHub Actions (revisar logs del step de fetch para
2015-01-01→2015-04-01). Si se confirma, GDELT podría no tener cobertura
fiable tan atrás, o requerir parámetros distintos (`sourcelang`,
`sourcecountry`) para esas fechas.
2026 acumula 27 ventanas porque `end = min(config_end, utcnow()-1d)` avanza
un día por corrida, generando una ventana de "cola" ligeramente distinta
cada vez — comportamiento esperado, no es un bug.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-07 | 0 reales (16/16 revisados = 100% falsos positivos) | 0 | Bug crítico encontrado: fetch_ddg_search() no validaba dominio de resultados DDG → 23 artículos "prensa.com" nunca eran de Panamá. Fix aplicado (validación de netloc). Bug adicional en mark_ingested() (crash por `_gdelt_windows`) corregido. Ventanas GDELT: 2015-2016 en 0/8, rango efectivamente agotado para 2017-2025. |

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
