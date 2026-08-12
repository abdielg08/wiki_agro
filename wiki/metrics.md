---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-12
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados (con contenido en wiki/) | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 (7 previos + 16 esta sesión) | **0 nuevos** |
| Pendientes de ingesta | 0 | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla, sin backfill real aún) | 2015 → hoy real |
| Ventanas GDELT completadas | 64 / ~48 estimadas (ver nota abajo) | cobertura 2015→hoy sin huecos |
| Última fecha con artículos nuevos en sources/ | 2026-07-30 (3 nuevos) | — |
| Días sin artículos nuevos (al 2026-08-12) | 13 días | máx 3 antes de diagnosticar — ⚠ FALLO ACTIVO |

---

## ⚠️ Diagnóstico de esta sesión (2026-08-12)

**1. Los 11 pendientes de la cola eran 100% falsos positivos (0/11 válidos).**
De hecho, desde la inicialización del wiki (2026-05-24) no ha entrado ningún artículo real
adicional: los 23 artículos descargados por la fuente `prensa.com` (búsqueda DDG `prensa_agro`)
son todos ruido global (Aragón/España, Utah/EE.UU., Arabia Saudita, Brasil, IEEE, UNESCO,
archive.org) mal etiquetado con `country: PA`. Causa raíz: la búsqueda `site:prensa.com` vía
`ddgs.news()` no respeta el operador `site:` de forma confiable, y el filtro `is_agro_relevant()`
solo exige keywords agro genéricos (incluyendo el acrónimo ambiguo "MIDA") sin exigir mención de
Panamá.

**Fix aplicado** en `scripts/fetch_news.py::fetch_ddg_search`: ahora se descarta cualquier
resultado cuyo dominio no coincida exactamente con el `site` configurado. Efecto esperado en la
próxima corrida de Actions: la fuente `prensa_agro` debería devolver 0 o muy pocos artículos (los
que realmente sean de prensa.com), en vez de ruido constante.

Dos bugs adicionales corregidos en `scripts/ingest.py`:
- `mark_ingested()` individual crasheaba por no filtrar la clave interna `_gdelt_windows`.
- `mark_all_ingested()` marcaba artículos en orden alfabético de archivo, distinto al orden por
  score que usa `ingest`/`run_prepare` — podía marcar como ingestados artículos que nunca se
  habían revisado. Ahora usa el mismo orden por score.

Ver `wiki/log.md` (entradas del 2026-08-12) para el detalle completo y la lista de URLs rechazadas.

**2. Sistema en estado de fallo por artículos estancados**: 13 días sin artículos nuevos en
`sources/articles/` (última vez con contenido nuevo: 2026-07-30). Supera el umbral de 3 días de
CLAUDE.md — ver diagnóstico de causa en "Estado del Fetch" abajo.

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con contenido nuevo : 2026-07-30 (3 artículos, todos prensa.com → falsos positivos)
Corridas recientes (2026-08-02 → 2026-08-10) : 0 artículos nuevos, 5 corridas consecutivas
Ventanas GDELT completadas : 64 (esperadas ~48 para 2015→hoy en pasos de 90 días)
Causa del sobreconteo de ventanas :
  fetch_gdelt_historical() recalcula end=ayer en cada corrida; la ventana final de cada corrida
  es parcial (current→ayer) y queda distinta a la siguiente corrida 2-3 días después, generando
  ventanas nuevas pequeñas en vez de reutilizar/extender la ventana anterior. No es un "rango
  agotado" real — el backfill 2015→hoy probablemente ya está sustancialmente cubierto sin huecos,
  pero no se ha verificado artículo por año todavía.
Por qué "0 artículos nuevos" en las últimas 5 corridas :
  a) GDELT: backfill 2015→~2026-07 ya recorrido, quedan pocas ventanas nuevas por explorar
     (solo el tramo más reciente cada vez) y puede no indexar mucho contenido agro-PA.
  b) RSS (IICA, La Prensa): únicas fuentes activas confiables — puede que simplemente no
     publiquen artículos agro-PA todos los días.
  c) prensa_agro (DDG): fuente rota desde el inicio (ver diagnóstico arriba) — nunca aportó
     artículos válidos, solo ruido.
Fix aplicado esta sesión : filtro de dominio en fetch_ddg_search() (ver diagnóstico arriba)
Estado post-fix          : pendiente validar en la próxima corrida de GitHub Actions — si
                            prensa_agro cae a 0 resultados de forma consistente, evaluar
                            reemplazarla por scraping directo de la sección agropecuaria de
                            prensa.com en vez de búsqueda DDG.
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
| 2023 Q1-Q4 | 0/4 | ? | Pendiente |
| 2024 Q1-Q4 | 0/4 | ? | Pendiente |
| 2025 Q1-Q4 | 0/4 | ? | Pendiente |
| 2026 Q1-Q2 | 0/2 | ? | Pendiente |
| **TOTAL** | **64 ventanas completadas (ver nota)** | **0 confirmados como agro-PA real** | **Tabla desactualizada — ver nota** |

> ⚠️ Esta tabla por trimestre está desactualizada: `_gdelt_windows` en processed.json ya tiene 64
> ventanas marcadas completas (no 0), pero no están alineadas a trimestres fijos por el problema
> de ventana final móvil descrito en "Estado del Fetch" arriba, y ninguno de los artículos
> descargados hasta ahora vía GDELT ha sido confirmado como contenido agro-Panamá real (los 6
> artículos reales en el wiki son semilla manual, no de GDELT). Pendiente: escribir un script que
> reconcilie `_gdelt_windows` contra rangos de trimestre reales para poblar esta tabla con datos
> verídicos, y confirmar si GDELT está aportando algún artículo válido en absoluto.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-12 | 0 (0 reales, 16 falsos positivos rechazados) | 0 | Cola de 11 (+5 previos) 100% falsos positivos — bug de fetch corregido, ver diagnóstico arriba |

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
