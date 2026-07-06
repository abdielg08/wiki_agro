---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-06
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 19 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 13 | **0 nuevos** (filtro DDG corregido hoy) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 45 / ~46 estimadas | 46 (2015→hoy) |
| Días sin artículos nuevos | **3 (07-03, 07-04, 07-05)** | máx 3 antes de diagnosticar → **LÍMITE ALCANZADO** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-05 (run #40, success, 0 artículos nuevos)
Resultado              : 3 días consecutivos sin artículos nuevos (07-03, 07-04, 07-05)
Causa identificada     : Bloqueo/rate-limit de servicios externos gratuitos, no bug de código:
                         - GDELT devuelve 403/429 en casi todas las ventanas (incl. las 8
                           pendientes de 2015-2016 y la ventana más reciente)
                         - ddgs (DuckDuckGo) devuelve "No results found" en las 8 búsquedas
                           web configuradas — rate-limit conocido del paquete sin API oficial
                         - RSS IICA y LaPrensaGeneral devolvieron 0 entradas ese día
Fix aplicado hoy       : fetch_ddg_search() ahora aplica _is_blocked_domain()/_is_panama_related()
                         (mismo filtro que RSS y GDELT) — cierra el hueco que causó 13 falsos
                         positivos acumulados (7 del 2026-06-22 + 6 hoy, todos de la búsqueda
                         DDG site:prensa.com que DDG no filtraba de forma confiable)
Estado post-fix        : Pendiente validación en próxima corrida Actions. El bloqueo de GDELT/DDG
                         es externo — monitorear próximas 2-3 corridas antes de intervenir más
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
| **TOTAL** | **45/46** | **0 reales** | **Ventanas casi agotadas, 0 artículos reales guardados** |

> 45/46 ventanas GDELT ya se marcaron completas (2017-2026), pero GDELT no ha devuelto
> NINGÚN artículo real aprovechable — o las ventanas devolvieron 0 resultados o fueron
> filtrados. Las 8 ventanas restantes de 2015-2016 llevan varios días reintentándose sin
> éxito por bloqueo 403/429 de la API (ver "Estado del Fetch" arriba). Pendiente: una vez
> resuelto el bloqueo, revisar si el backfill 2017-2026 realmente no tiene contenido
> aprovechable o si el filtro `_is_panama_related()` está siendo demasiado estricto para
> resultados de GDELT (que ya exige Panamá en el query booleano vía sourcecountry:PA).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-06 | 0 (6 revisados, 6 falsos positivos) | 0 | Fix causa raíz: filtro Panama-relevance faltante en fetch_ddg_search(). Diagnóstico: GDELT bloqueado (403/429) + ddgs rate-limited → 3 días consecutivos sin artículos nuevos |

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
