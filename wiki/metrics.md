---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-18
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 13 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 (7 previos + 16 hoy) | **0 nuevos** |
| Páginas en wiki/ | 20 (8 topics, 3 entities, 6 summaries) | ↑ continuo |
| Cobertura temporal real | 2017-03-30 → 2026-06-17 (GDELT) | 2015-02-19 → hoy |
| Ventanas GDELT completadas | 70 (ninguna en 2015-02→2017-03) | cubrir el rango completo |
| Días sin artículos nuevos reales | 19 (último: 2026-07-30) | máx 3 antes de diagnosticar |

**⚠️ Alarma activa**: 19 días sin artículos nuevos reales — muy por encima del umbral de 3 días.

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions      : 2026-08-18 (run 32130922392) — "completed success" pero 0 artículos
Último artículo genuino     : 2026-07-30 (3 artículos)
Causa identificada (hoy)    : Fallo simultáneo de las 4 fuentes de fetch:
  1. RSS IICA y LaPrensaGeneral → 0 entradas en el feed (feeds vacíos o URL obsoleta)
  2. DDG por dominio oficial (oirsa/mida.gob.pa/idiap.gob.pa/bda.gob.pa/fao.org/
     bancomundial.org/iica.int) → "No results found" en las 7 búsquedas
  3. DDG "prensa_agro" (única que rendía resultados) → site: no respetado por
     DDGS, devolvía artículos globales sin relación a Panamá (falsos positivos)
  4. GDELT histórico → bloqueado 403/429 en el 100% de ventanas intentadas hoy
     (tanto 2015-2017 sin cubrir como la ventana incremental reciente)
Fix aplicado hoy            : fetch_ddg_search() ahora exige dominio configurado +
                               _is_blocked_domain() + _is_panama_related(), igual
                               que fetch_rss(). Bug de mark-ingested corregido
                               (crasheaba en clave interna _gdelt_windows).
Pendiente de investigar     : URLs de RSS IICA/La Prensa; rate-limit de GDELT
                               (IP compartida de Actions); si ddgs indexa dominios
                               .gob.pa en absoluto.
Estado post-fix             : Pendiente validación en próxima corrida Actions
```

---

## Progreso del Backfill GDELT (2015 → hoy)

> Datos reales tomados de `sources/processed.json:_gdelt_windows` (70 ventanas) el 2026-08-18.
> El fetch diario reintenta 2015-2017 cada corrida y falla por bloqueo 403/429 de GDELT
> (ver "Estado del Fetch" arriba) — **el rango 2015-02-19 → 2017-03-29 sigue sin cubrirse**.

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015-02-19 → 2015-12-31 | 0/4 | **Pendiente — bloqueado por GDELT 403/429** |
| 2016 Q1-Q4 | 0/4 | **Pendiente — bloqueado por GDELT 403/429** |
| 2017-01-01 → 2017-03-29 | 0/1 | **Pendiente — bloqueado por GDELT 403/429** |
| 2017-03-30 → 2017-12-27 | 3/3 | Completo |
| 2018 Q1-Q4 | 4/4 | Completo |
| 2019 Q1-Q4 | 4/4 | Completo |
| 2020 Q1-Q4 | 4/4 | Completo |
| 2021 Q1-Q4 | 4/4 | Completo |
| 2022 Q1-Q4 | 4/4 | Completo |
| 2023 Q1-Q4 | 4/4 | Completo |
| 2024 Q1-Q4 | 4/4 | Completo |
| 2025 Q1-Q4 | 4/4 | Completo |
| 2026-01-01 → 2026-06-17 | 2/2 | Completo |
| 2026-06-18 → hoy | 34 ventanas solapadas (fetch incremental diario) | Ver nota abajo |
| **TOTAL** | **70 ventanas** | **2017-03-30 → 2026-06-17 cubierto; 2015-02-19 → 2017-03-29 pendiente** |

> Nota: las 34 ventanas de 2026-06-18→hoy comparten el mismo inicio (`20260618_*`)
> con fecha de fin creciente cada día — es el mecanismo de fetch incremental, no
> backfill real. Esto infla el conteo de "ventanas completadas" sin representar
> cobertura nueva. Considerar consolidar a una sola ventana por corrida.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-18 | 0 (16/16 falsos positivos rechazados) | 0 | Fix de raíz en fetch_ddg_search() (faltaban guards de dominio/Panamá) + fix de bug en mark-ingested. Diagnóstico: 19 días sin artículos reales — RSS vacíos, DDG oficial sin resultados, GDELT bloqueado 403/429 en 2015-2017 |

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
