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
| Falsos positivos acumulados | 23 | **0 nuevos** ⚠️ ver diagnóstico |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 37 reales + 27 recicladas / 64 reportadas | 45-47 (2015→hoy) |
| Días sin artículos nuevos | 11 (desde 2026-07-30) | máx 3 antes de diagnosticar |

**⚠️ Sistema en estado de fallo**: 11 días sin ingesta real, supera el
umbral de 3 días de CLAUDE.md. Causa raíz identificada y corregida esta
sesión (ver abajo) — pendiente de validar en la próxima corrida de Actions.

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions   : 2026-08-10 (corre a diario, según git log de sources/)
Último commit con
  artículos nuevos       : 2026-07-30 (3 artículos)
Resultado reciente       : 0 artículos nuevos por 11 días consecutivos

Causa identificada (2026-08-10):
  1. web_searches.prensa_agro (DDG) es la fuente de TODOS los falsos
     positivos acumulados (23/23, fuente "prensa.com"). fetch_ddg_search()
     no aplicaba _is_panama_related() como sí hacen RSS y GDELT, y la
     query "site:prensa.com X OR Y OR MIDA OR ..." sin paréntesis anulaba
     la restricción site: para DDG. Resultado: artículos de Malasia, Utah,
     España (Aragón), Arabia Saudita, Irán y Brasil colándose por
     coincidir con "MIDA" u otro término agro genérico.
  2. GDELT: la ventana final parcial (arranca en 2026-06-18) se re-fetchea
     cada día con una fecha de fin distinta y se cuenta como ventana
     "nueva" cada vez (27 de las 64 completadas son esta misma ventana
     reciclada). El backfill real de 2015-01-01 a 2017-03-29 (~9
     trimestres) nunca se ha ejecutado.

Fix aplicado (2026-08-10):
  - scripts/fetch_news.py: fetch_ddg_search() ahora aplica
    _is_blocked_domain() + _is_panama_related() antes de aceptar un
    resultado, igual que RSS y GDELT.
  - config/sources.yaml: query de prensa_agro reescrita con paréntesis
    alrededor de los términos OR para que site:prensa.com aplique a toda
    la búsqueda.
  - GDELT (ventana final reciclada): NO corregido esta sesión — requiere
    cambiar la lógica de qué ventana se marca "completa" en
    fetch_gdelt_historical(). Pendiente para una sesión dedicada.

Estado post-fix: Pendiente validación en próxima corrida de Actions — si
  prensa_agro sigue devolviendo 0 o vuelve a traer falsos positivos,
  considerar desactivarla o acotar aún más la query.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | 0 | **Pendiente — nunca fetcheado** |
| 2016 Q1-Q4 | 0/4 | 0 | **Pendiente — nunca fetcheado** |
| 2017 Q1 (parcial) | 0/1 | 0 | **Pendiente — nunca fetcheado** |
| 2017 Q2-Q4 | 3/3 | ver sources/ | Completo |
| 2018 Q1-Q4 | 4/4 | ver sources/ | Completo |
| 2019 Q1-Q4 | 4/4 | ver sources/ | Completo |
| 2020 Q1-Q4 | 4/4 | ver sources/ | Completo |
| 2021 Q1-Q4 | 4/4 | ver sources/ | Completo |
| 2022 Q1-Q4 | 4/4 | ver sources/ | Completo |
| 2023 Q1-Q4 | 4/4 | ver sources/ | Completo |
| 2024 Q1-Q4 | 4/4 | ver sources/ | Completo |
| 2025 Q1-Q4 | 4/4 | ver sources/ | Completo |
| 2026 (hasta 2026-06-17) | 1/1 | ver sources/ | Completo |
| 2026-06-18 → hoy | reciclada diariamente, no cuenta como avance real | — | **Bug — ver diagnóstico arriba** |
| **TOTAL real** | **37/~46** | 29 artículos en sources/ (todas las fuentes) | **Faltan 2015-01-01 → 2017-03-29 (~9 ventanas)** |

> Conteo recalculado el 2026-08-10 a partir de `sources/processed.json._gdelt_windows`.
> 27 ventanas adicionales reportadas como "completadas" son en realidad la misma
> ventana final (`20260618_*`) recontada cada día — no representan progreso de
> backfill real (ver diagnóstico en "Estado del Fetch" arriba).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-10 | 0 | 0 | 16 falsos positivos revisados (0 ingestados) — fix de causa raíz en fetch_ddg_search() y query de prensa_agro; ventana GDELT final reciclada identificada, backfill 2015-2017 aún pendiente |

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
