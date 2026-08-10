---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-10
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Artículos marcados "ingested" (incl. falsos positivos descartados) | 18 | — |
| Pendientes de ingesta | 11 | 0 |
| Falsos positivos acumulados | 12 (7 previos + 5 de hoy) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal real | 2015-2026 (solo 6 artículos semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 63 | rango 2015→hoy prácticamente agotado |
| Días sin artículos nuevos genuinos | 11 (último: 2026-07-30) | máx 3 antes de diagnosticar → **ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions       : 2026-08-09 (runs #66-75, TODAS "success" — verificado vía API)
Resultado últimas corridas   : 0 artículos nuevos desde 2026-07-30 (11 días)
Causa identificada           : Actions SÍ corre diariamente y SÍ tiene éxito, pero el fetch
                                no encuentra contenido nuevo:
                                1. GDELT: 63 ventanas ya completadas (más que el rango
                                   histórico estimado) → backfill 2015-2025 esencialmente
                                   agotado, quedan pocas/ninguna ventana nueva por explorar.
                                2. RSS: solo IICA y La Prensa activos, publican con poca
                                   frecuencia — no alcanza para cubrir el hueco de GDELT.
                                3. Búsqueda web DDG ("prensa_agro"): SÍ trae resultados,
                                   pero son 100% falsos positivos (ver debajo) — no
                                   contribuyen artículos reales de Panamá.
Bug adicional descubierto    : fuente "prensa.com" (búsqueda DDG site:prensa.com + query con
  hoy (2026-08-10)             "MIDA" como término suelto) no filtra por dominio real ni por
                                contexto de Panamá. Resultado: siempre trae noticias sobre
                                MIDA de Malasia (Malaysian Investment Development Authority) o
                                MIDA de Utah (Military Installation Development Authority),
                                NUNCA sobre Panamá. Confirmado en 5/5 del lote de hoy y en
                                muestra del resto de la cola (16 pendientes). Detalle completo
                                en wiki/log.md (entrada 2026-08-10).
Recomendación                : (a) quitar "MIDA" de search_terms.primary o exigir
                                coocurrencia con "Panamá", (b) validar dominio real de la URL
                                contra el `site` esperado en fetch_ddg_search(), (c) usar el
                                dominio real como `source` en vez del `site` configurado,
                                (d) considerar agregar más fuentes RSS o expandir GDELT con
                                nuevas queries ya que el backfill actual está cerca de agotarse.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | **0/4** | 0 | **NUNCA EJECUTADO — ver diagnóstico abajo** |
| 2016 Q1-Q4 | **0/4** | 0 | **NUNCA EJECUTADO — ver diagnóstico abajo** |
| 2017 Q1-Q4 | 4/4 | ? | Completo (artículos reales sin contar aparte — la mayoría 0 resultados PA) |
| 2018 Q1-Q4 | 4/4 | ? | Completo |
| 2019 Q1-Q4 | 4/4 | ? | Completo |
| 2020 Q1-Q4 | 4/4 | ? | Completo |
| 2021 Q1-Q4 | 4/4 | ? | Completo |
| 2022 Q1-Q4 | 4/4 | ? | Completo |
| 2023 Q1-Q4 | 4/4 | ? | Completo |
| 2024 Q1-Q4 | 4/4 | ? | Completo |
| 2025 Q1-Q4 | 4/4 | ? | Completo |
| 2026 (parcial, hasta hoy) | 27 ventanas registradas (solapadas/variables, ver diagnóstico) | ? | En progreso, con reintentos por timeout de Actions |
| **TOTAL** | **63 ventanas en processed.json** | — | **2015-2016 son el hueco real; 2017-2026 ya cubiertos por GDELT** |

> Diagnóstico 2026-08-10: 2015 y 2016 nunca se han descargado a pesar de ser el
> inicio de la cobertura objetivo (CLAUDE.md: "2015-02-19 → hoy"). Causa probable:
> `fetch_gdelt_historical()` solo persiste `_gdelt_windows` a disco cada 50
> artículos guardados o al finalizar `run_fetch()`; el timeout de 30 min del
> workflow de Actions corta la corrida antes de que el progreso en años
> recientes (2026) se guarde, así que el loop parece "reintentar" en 2026 en
> vez de nunca llegar a completar y avanzar más allá. Ver wiki/log.md
> (2026-08-10) para el detalle completo y la recomendación de correr
> `fetch-historical --years 2015-2016 --mode gdelt` manualmente sin límite de
> 30 min.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-10 | 0 (5 falsos positivos descartados) | 11 | Bug sistémico en fuente "prensa.com" (colisión MIDA Malasia/Utah); Actions corre OK pero sin contenido nuevo desde 2026-07-30 |

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
