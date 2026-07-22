---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-22
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados | 13 | = total sin falsos positivos |
| Falsos positivos acumulados | 18 (7 previos + 11 nuevos hoy) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 37 trimestrales + 15 incrementales diarias | Faltan ~9 ventanas: 2015-01 → 2017-03 (ver detalle abajo) |
| Días sin artículos nuevos | 0 (Actions de hoy aún no corre, programado 11:00 UTC) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-21 12:26 UTC — 0 artículos nuevos
Historial reciente     : 07-21:0, 07-20:2, 07-19:0, 07-18:0 (sin racha de 3+ días en 0)
Ventanas GDELT          : 37 trimestrales (2017-03-30 → 2026-06-17) + 15 incrementales
                         diarias recientes = 52 en total. GAP REAL: 2015-01-01 →
                         2017-03-29 (~9 ventanas) nunca se completaron — el backfill
                         NO cubre aún el rango objetivo completo (2015-02-19 → hoy).
                         Sin red en este entorno sandbox (proxy 403 al probar
                         api.gdeltproject.org) no se pudo re-ejecutar esas ventanas
                         aquí; validar en próxima corrida real de GitHub Actions.
Falsos positivos hoy    : 11/11 pendientes de esta sesión NO eran sobre agro panameño
                         (ver wiki/log.md 2026-07-22 para el detalle de cada URL)
Causa raíz              : web_searches.prensa_agro usa site:prensa.com, pero ddgs.news()
                         no respeta el operador site: de forma confiable → devolvía
                         resultados de dominios ajenos (sltrib.com, paultan.org, msn.com,
                         archive.org, ieeexplore.ieee.org) etiquetados como prensa.com.
                         is_agro_relevant() aceptaba acrónimos ambiguos como "MIDA"
                         (existe en Malasia y Utah) sin exigir contexto Panamá.
Fix aplicado hoy        : scripts/fetch_news.py::fetch_ddg_search() ahora descarta resultados
                         cuyo dominio real no coincide con el `site` configurado, antes
                         del filtro de keywords.
Estado post-fix         : Pendiente de validación en próximas corridas de Actions
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 Q1-Q4 | 0/4 | **Pendiente — gap real** |
| 2016 Q1-Q4 | 0/4 | **Pendiente — gap real** |
| 2017 Q1 | 0/1 | **Pendiente — gap real** |
| 2017 Q2-Q4 | 3/3 | Completo |
| 2018 Q1-Q4 | 4/4 | Completo |
| 2019 Q1-Q4 | 4/4 | Completo |
| 2020 Q1-Q4 | 4/4 | Completo |
| 2021 Q1-Q4 | 4/4 | Completo |
| 2022 Q1-Q4 | 4/4 | Completo |
| 2023 Q1-Q4 | 4/4 | Completo |
| 2024 Q1-Q4 | 4/4 | Completo |
| 2025 Q1-Q4 | 4/4 | Completo |
| 2026 (hasta 06-17) | 2/2 | Completo |
| **TOTAL trimestral** | **37/46** | Faltan 9 ventanas (2015-01 → 2017-03) |

> Datos extraídos de `_gdelt_windows` en sources/processed.json (2026-07-22).
> No se pudo reintentar las 9 ventanas faltantes en este entorno (sin acceso de red).
> Próxima sesión con red disponible: priorizar 2015 Q1 → 2017 Q1 para cerrar el gap.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-22 | 0 (11/11 falsos positivos) | 0 | Fix de causa raíz en fetch_ddg_search (dominio no verificado) + diagnóstico de gap real GDELT 2015–2017Q1 |

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
