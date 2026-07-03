---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-03
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 19 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 13 | **0 nuevos** (bug de origen corregido hoy) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 43 / ~46 estimadas | 46 (2015→hoy) |
| Días sin artículos nuevos | 0 (fetch corrió 2026-07-02) | máx 3 antes de diagnosticar |
| Días sin artículos **reales** de Panamá | ~40 (desde semilla 2026-05-24) | 1 día hábil |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-02 (trajo 1 artículo — falso positivo)
Resultado              : Actions SÍ corre a diario y SÍ trae artículos,
                          pero 13/13 de los últimos artículos fetchados
                          automáticamente resultaron falsos positivos (0% útiles).
Causa raíz identificada: fetch_ddg_search() en scripts/fetch_news.py NO aplicaba
                          los filtros _is_blocked_domain()/_is_panama_related() que
                          sí tienen fetch_rss() y fetch_gdelt_batch() desde el fix
                          del 2026-06-22 (c032e62). Además etiquetaba el campo
                          "source" con el nombre de config (ej. "prensa.com") en
                          vez del dominio real del resultado — esto ocultaba que
                          DDG estaba devolviendo resultados de sltrib.com,
                          thestar.com.my, fox13now.com, nyfb.org y spa.gov.sa
                          pese al calificador site:prensa.com (DDG no lo impone
                          estrictamente en su API de noticias). La keyword "MIDA"
                          en la query de búsqueda colisiona con "Military
                          Installation Development Authority" (Utah) y "Malaysian
                          Investment Development Authority" (Malasia).
Fix aplicado (hoy)     : fetch_ddg_search() ahora aplica _is_blocked_domain() y
                          _is_panama_related() igual que fetch_rss()/GDELT, y usa
                          el dominio real de la URL para el campo "source".
                          Ver scripts/fetch_news.py y wiki/log.md 2026-07-03.
Estado post-fix        : Pendiente validación en próxima corrida Actions
                          (esperado: 0 falsos positivos vía DDG a partir de ahora)
```

---

## Progreso del Backfill GDELT (2015 → hoy)

Ventanas GDELT rolling reales (no calendario fijo): 43 completadas, cubriendo
**2017-03-30 → 2026-07-01** de forma continua (37 ventanas trimestrales +
6 ventanas incrementales diarias de catch-up de esta última semana).

| Período | Estado | Nota |
|---------|--------|------|
| 2015-02-19 → 2017-03-29 | **NO cubierto** | Gap real de ~8 ventanas al inicio del rango — prioridad #1 del backfill |
| 2017-03-30 → 2026-07-01 | 43/43 ventanas completadas | Cobertura continua, 0 huecos detectados |
| **TOTAL** | **43/~46 estimadas** | Falta el tramo 2015–2017 para completar cobertura objetivo |

> Resultado real de artículos por las 43 ventanas GDELT: **0 artículos de agro
> panameño incorporados al wiki** (todo lo fetchado vía GDELT/DDG hasta hoy que
> no era falso positivo = 0; los 6 artículos reales del wiki son semilla manual
> del 2026-05-24). Con el fix de `fetch_ddg_search()` de hoy, monitorear si las
> próximas corridas empiezan a producir artículos reales de Panamá.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-03 | 0 | 0 | 6 artículos revisados, 6 falsos positivos (0 al wiki). Root cause: `fetch_ddg_search()` sin filtro geográfico → corregido hoy. Ver wiki/log.md |

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
