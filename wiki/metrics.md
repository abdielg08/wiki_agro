---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-04
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 | **0 nuevos** |
| Pendientes de ingesta | 0 | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal (contenido real) | 2015-2024 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 61 (ver nota de bug abajo) | ~48 (2015→hoy, trimestral) |
| Días sin artículos nuevos | 5 (último: 2026-07-30) | máx 3 antes de diagnosticar — **UMBRAL SUPERADO** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con artículos nuevos : 2026-07-30 (3 artículos)
Última corrida registrada           : 2026-08-02 (0 artículos nuevos)
Hoy                                 : 2026-08-04 → 5 días sin artículos nuevos
Sin commit de sources/ registrado   : 2026-08-01 y 2026-08-03 (posible falla del
                                       workflow o "0 artículos" no genera commit)
```

**DIAGNÓSTICO — dos problemas encontrados esta sesión (2026-08-04):**

1. **Umbral de "3 días sin nuevos" superado.** Van 5 días (07-31 a 08-04) sin
   artículos nuevos reales en `sources/articles/`. Revisar el historial de runs de
   `wiki_daily.yml` en GitHub Actions directamente (no accesible desde esta sesión)
   para confirmar si el workflow está fallando, fue deshabilitado, o simplemente
   GDELT/RSS no tienen contenido nuevo sobre Panamá esos días.

2. **Bug de estancamiento en el backfill GDELT.** `fetch_gdelt_historical()`
   (`scripts/fetch_news.py`) construye la clave de ventana como
   `f"{current}_{next_q}"` donde `next_q = min(current + 90d, end)` y `end` es
   siempre "ayer" (se recalcula cada corrida). El cursor `current` **no se persiste**
   entre corridas — solo se persiste la lista de `window_key` ya completadas. Como
   resultado, desde el **2026-06-18** el `current` quedó fijo en esa fecha: cada día
   `end` avanza 1 día, se genera una `window_key` nueva (mismo inicio, fin distinto),
   se descarga esa ventana (0-3 artículos), se marca como "completa", pero el cursor
   **nunca avanza** a la siguiente ventana trimestral porque nunca acumula los 90 días
   completos antes de que `end` la alcance. Efecto: 25 de las 61 "ventanas
   completadas" registradas son en realidad la misma ventana `20260618_*` repetida
   con fin creciente día a día — el backfill histórico real (2015→2026, trimestral)
   sigue esencialmente detenido desde 2026-06-18, no avanza a periodos anteriores no
   cubiertos ni cierra el periodo actual.
   Fix sugerido para próxima sesión con acceso de escritura a `scripts/`: persistir
   `current` explícitamente (no derivarlo de `end`), o cerrar la ventana en curso una
   vez transcurridos los 90 días desde su inicio en vez de cuando `next_q` alcanza `end`.

**Nota**: ninguno de los 2 problemas anteriores es causado por la sesión de ingesta de
hoy — son preexistentes en el pipeline de `fetch`, fuera del alcance de la rutina de
ingesta (que solo lee `sources/` y escribe en `wiki/` + `sources/processed.json`).

---

## Progreso del Backfill GDELT (2015 → hoy)

> Recalculado el 2026-08-04 leyendo directamente `sources/processed.json["_gdelt_windows"]`
> (61 entradas). La tabla anterior ("0/46, no iniciado") estaba desactualizada.

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015-01-01 → 2017-03-29 | 0/9 | **Sin cubrir — hueco real de ~2.25 años** |
| 2017 (desde 30-mar) | 4/4 | Completo desde Q2 |
| 2018 | 4/4 | Completo |
| 2019 | 4/4 | Completo |
| 2020 | 4/4 | Completo |
| 2021 | 4/4 | Completo |
| 2022 | 4/4 | Completo |
| 2023 | 4/4 | Completo |
| 2024 | 4/4 | Completo |
| 2025 | 4/4 | Completo |
| 2026 (hasta 2026-06-17) | 1/1 | Completo |
| 2026-06-18 → hoy | 24 entradas repetidas | **Estancado — ver bug en "Estado del Fetch"** |
| **TOTAL** | **61** | **Backfill 2017-03→2026-06 completo; falta 2015-2017 y el tramo actual está estancado** |

**Artículos por ventana**: no se puede derivar de `processed.json` (no se registra por
ventana); ver `sources/articles/*.json` individuales para conteo real por fecha.

> Próximo paso recomendado: forzar un rango explícito `2015-01-01 → 2017-03-29` en una
> corrida manual (`fetch --mode gdelt`) para cerrar el hueco inicial, y corregir el bug
> de estancamiento del cursor antes de que el backfill pueda avanzar más allá de
> 2026-06-18.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-04 | 0 (16 revisados, 16 falsos positivos) | 0 | Routine automática. 0% falsos positivos ingestados al wiki (correcto). Encontrados y documentados: (1) bug de desajuste de orden entre `ingest` y `mark-all-ingested`, (2) bug de estancamiento del cursor GDELT desde 2026-06-18, (3) umbral de 3 días sin artículos nuevos superado (van 5). Ver wiki/log.md 08:20-08:25 para detalle. |

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
