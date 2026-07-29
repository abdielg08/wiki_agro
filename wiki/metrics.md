---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-29
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 18 (+11 hoy) | **0 nuevos** (causa raíz corregida hoy) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 57 (≥ 46 estimadas) | backfill histórico agotado |
| Días sin artículos nuevos válidos | ≥9 (último real: 2026-07-20) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-28 (0 artículos nuevos)
Resultado sesión hoy    : 11 pendientes procesados, 11/11 falsos positivos — 0 ingestados al wiki
Causa identificada      : web_search "prensa_agro" (config/sources.yaml) usa site:prensa.com +
                          términos genéricos (incl. "MIDA" suelto). El operador site: de
                          DuckDuckGo no se respeta de forma confiable — llegaron resultados de
                          dominios ajenos (paultan.org, sltrib.com, nyfb.org, spa.gov.sa,
                          whc.unesco.org, ieeexplore.ieee.org, archive.org, thestar.com.my)
                          etiquetados incorrectamente como "prensa.com". Además
                          is_agro_relevant() no exigía mención de "Panamá", solo un término
                          agro genérico → falsos positivos por colisión de sigla MIDA (Utah
                          Military Installation Development Authority, MITI/MARii Malasia) y
                          contenido agro global sin relación con Panamá.
Fix aplicado hoy         : scripts/fetch_news.py — fetch_ddg_search() ahora valida el dominio
                          real (urlparse) contra el `site` solicitado antes de aceptar un
                          resultado; is_agro_relevant() acepta require_panama=True, usado en
                          la ruta de búsqueda web para exigir mención explícita de Panamá.
                          Ver wiki/log.md 2026-07-29 08:20 para el detalle completo.
Estado post-fix          : Pendiente validación en próxima corrida Actions
Backfill GDELT           : 57 ventanas completadas — supera la estimación de 46 (2015→2027 Q2).
                          El backfill histórico por trimestres parece agotado; el avance
                          futuro depende de RSS (IICA, La Prensa) y de la búsqueda web ya
                          corregida.
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
| **TOTAL** | **57 ventanas registradas** | **ver sources/processed.json** | **Backfill avanzado, desglose trimestral desactualizado** |

> NOTA 2026-07-29: `_gdelt_windows` en sources/processed.json registra 57 ventanas
> completadas (formato `YYYYMMDD_YYYYMMDD`, ~90 días cada una, no necesariamente
> alineadas a trimestres calendario), superando la estimación original de 46 ventanas
> trimestrales. La tabla de arriba quedó desactualizada porque nunca se rellenó tras el
> reset de 2026-06-22. Pendiente: recalcular el desglose por año a partir de
> `_gdelt_windows` en una próxima sesión de mantenimiento (LINT), no crítico para el
> flujo diario de ingesta.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-29 | 0 | 0 | 11/11 pendientes = falsos positivos (colisión sigla MIDA + site: no aplicado) — fix de causa raíz en fetch_ddg_search()/is_agro_relevant() |

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
