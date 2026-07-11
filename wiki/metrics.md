---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-11
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 20 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 14 | **0 nuevos** (ver fix de causa raíz abajo) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 48 / ~45 estimadas | 45 (2015→hoy) — rango agotado, evaluar expansión |
| Días sin artículos nuevos | 1 | máx 3 antes de diagnosticar |
| Pendientes de ingesta | 0 | 0 |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con artículos nuevos : 2026-07-10 (commit 88389fe, +1 artículo)
Resultado sesión 2026-07-11         : 0 pendientes al iniciar; 8 pendientes procesados
                                       durante la sesión (5 + 2 + 1 recuperado de bug)
Causa identificada     : GDELT ventanas 2026-2027 = fechas futuras → timeout/403 (fix previo)
                         RSS IICA y La Prensa devolvieron 0 entradas ese día (fix previo)
Fix aplicado           : fetch_gdelt_historical() ahora limita end a datetime.utcnow()-1d
Estado post-fix        : validado — hay commits diarios de sources/ desde entonces

BUG NUEVO ENCONTRADO Y CORREGIDO (2026-07-11):
  El fetcher DDG `prensa_agro` (site:prensa.com, query incluye "MIDA") no aplicaba los
  filtros _is_blocked_domain()/_is_panama_related() que sí usan fetch_rss() y GDELT.
  El operador `site:` de DDGS tampoco se respeta de forma confiable. Resultado: 14/20
  artículos descargados hasta hoy (70%) resultaron ser falsos positivos por colisión de
  la sigla "MIDA" (Malaysian Investment Development Authority, Military Installation
  Development Authority de Utah) o coincidencias genéricas de "agricultura" sin relación
  con Panamá (Arabia Saudita, Irán/UNESCO, World Bank, IEEE).
  Fix: se agregaron ambos filtros a fetch_ddg_search() en scripts/fetch_news.py.
  También se corrigió mark_all_ingested() (usaba orden distinto a ingest(), ver log.md
  00:10) y mark_ingested() (crasheaba con la clave _gdelt_windows).
  Validación pendiente: confirmar que la próxima corrida de GitHub Actions ya no
  produce falsos positivos de prensa_agro.
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
| **TOTAL** | **48/46** | **?** | **Ventanas agotadas — desglose por trimestre pendiente de auditoría** |

> `sources/processed.json._gdelt_windows` reporta 48 ventanas completadas (más que las
> ~45 estimadas para 2015→hoy), pero esta tabla no se ha actualizado con el desglose real
> por trimestre desde que se inició el backfill. Pendiente para una sesión futura: auditar
> `_gdelt_windows` y volcar el desglose real aquí, y evaluar si el rango de fechas
> necesita expandirse más allá de "hoy".

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-11 | 0 (7 falsos positivos rechazados) | 0 | Fix causa raíz: filtro Panamá faltante en fetch_ddg_search() (14/20 artículos históricos = falsos positivos); fix bug de orden en mark_all_ingested(); fix crash en mark_ingested() por clave _gdelt_windows |

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
