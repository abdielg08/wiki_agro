---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-23
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 30 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 16 | **0 nuevos** (revisados y documentados, no en wiki/) |
| Pendientes de ingesta | 8 | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 73 (37 trimestrales 2017–2026 + 36 diarias jun–ago 2026) | cobertura 2015–hoy |
| Días sin artículos nuevos en sources/ | 4 (último: 2026-08-19) | máx 3 antes de diagnosticar ⚠️ **SUPERADO** |

---

## ⚠️ Alerta activa: 4 días sin artículos nuevos en sources/

Supera el umbral de 3 días definido en CLAUDE.md. Último commit con artículos
nuevos: `e9d45e6` (2026-08-19, 1 artículo). Los commits del 08-20 al 08-22
reportan "0 artículos nuevos" cada uno. GitHub Actions (`wiki_daily.yml`) sí
está corriendo diariamente — el problema no es que el workflow falle, sino que
casi no encuentra artículos nuevos relevantes. Ver diagnóstico completo abajo
y en `wiki/log.md` (entrada 2026-08-23).

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con contenido nuevo : 2026-08-19 (1 artículo)
Últimas 3 corridas (08-20 a 08-22) : 0 artículos nuevos cada una
Causa identificada (esta sesión)   : fetch_ddg_search() etiquetaba resultados como
                                      "prensa.com" sin validar que el dominio real
                                      del resultado fuera prensa.com — el operador
                                      site: de DDG no se respeta de forma confiable.
                                      Esto inflaba processed.json con "pendientes"
                                      que en realidad eran ruido internacional
                                      (Malasia, Utah, España, Brasil, Arabia
                                      Saudita...), no artículos panameños perdidos.
Fix aplicado (2026-08-23)          : fetch_ddg_search() ahora valida el dominio real
                                      del resultado contra el `site` configurado, y
                                      aplica _is_panama_related() cuando no hay site.
Estado post-fix                    : Pendiente validación en próxima corrida Actions
```

---

## Progreso del Backfill GDELT (2015 → hoy)

Basado en `sources/processed.json:_gdelt_windows` (73 ventanas registradas: 37
con patrón trimestral real 2017–2026, 36 con patrón diario deslizante
jun–ago 2026 que no aportan al backfill histórico).

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 Q1-Q4 | 0/4 | **Pendiente — gap sin explicar** |
| 2016 Q1-Q4 | 0/4 | **Pendiente — gap sin explicar** |
| 2017 Q1-Q4 | 4/4 | Completo |
| 2018 Q1-Q4 | 4/4 | Completo |
| 2019 Q1-Q4 | 4/4 | Completo |
| 2020 Q1-Q4 | 4/4 | Completo |
| 2021 Q1-Q4 | 4/4 | Completo |
| 2022 Q1-Q4 | 4/4 | Completo |
| 2023 Q1-Q4 | 4/4 | Completo |
| 2024 Q1-Q4 | 4/4 | Completo |
| 2025 Q1-Q4 | 4/4 | Completo |
| 2026 Q1-Q2 | ~1/2 | Parcial |
| **TOTAL** | **37/46 trimestres** | **2015–2016 sin cubrir; resto completo** |

> `wiki_historical.yml` (crawl histórico dedicado) es de ejecución manual y no
> hay evidencia en el log de git de haberse disparado — las 37 ventanas
> trimestrales probablemente vinieron del job diario (`wiki_daily.yml`, modo
> `all`). Investigar en próxima sesión por qué 2015–2016 nunca se completaron:
> candidatos son rate-limit/bloqueo de GDELT para ventanas muy antiguas, o que
> el job diario nunca alcanza esas ventanas por límite de artículos/tiempo
> antes de llegar a ellas en el barrido secuencial desde 2015-01-01.

---

## Historial de Sesiones de Routine

| Fecha | Artículos reales | Falsos positivos revisados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 7 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-23 | 0 | 9 | 8 | Fix bug DDG `site:` (fetch_news.py) + fix desincronización ingest/mark-all-ingested + fix crash de mark_ingested (ingest.py) + alerta: 4 días sin artículos nuevos |

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
