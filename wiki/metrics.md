---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-07
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 (7 previos + 16 esta sesión) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2017-03-30 → 2026-06-17 (backfill GDELT) + semilla 2015-2024 | 2015-02-19 → hoy real |
| Ventanas GDELT completadas | 37 / ~46 estimadas (limpiado de 62 aparentes, ver diagnóstico) | 46 (2015→hoy) |
| Días sin artículos nuevos | 2 (2026-08-05, 2026-08-06) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions  : 2026-08-06 (completed/success, verificado vía API de GitHub)
Resultado               : 0 artículos nuevos por 2 días consecutivos (08-05, 08-06)
Último commit con datos : 2026-08-04 (chore(sources): 0 artículos nuevos)
Causa identificada      : (1) RSS (IICA/La Prensa) sin entradas nuevas esas fechas.
                          (2) Bug en fetch_gdelt_historical(): la ventana trimestral
                              final quedaba acotada por "ayer" y se marcaba completa
                              con una clave nueva cada día — 25 entradas basura en
                              processed.json sin avanzar cobertura real (solo 37/62
                              ventanas eran trimestres genuinos de 90 días).
                          (3) fetch_ddg_search() no exigía mención de Panamá ni
                              descartaba dominios bloqueados — causa raíz de 16
                              falsos positivos ingresados a la cola esta sesión
                              (MIDA Malasia/Utah, agro España/Brasil/Arabia Saudita).
Fix aplicado            : (1) fetch_ddg_search() ahora aplica _is_panama_related() y
                              _is_blocked_domain(), y usa el dominio real de la URL
                              como "source" en vez del sitio configurado.
                          (2) fetch_gdelt_historical() solo marca una ventana
                              completa si alcanzó 90 días reales o el end
                              configurado; la ventana de cola ya no se persiste
                              prematuramente. Se podaron las 25 entradas basura
                              de _gdelt_windows (62 → 37).
                          (3) mark_all_ingested() ahora usa el mismo orden por
                              score que ingest() — antes marcaba artículos
                              distintos a los que Claude había revisado.
Pendiente de investigar : ~9 trimestres sin completar entre 2015-01-01 y
                           2017-03-29 (gap real de cobertura — ver wiki/log.md
                           entrada 2026-08-07 08:30).
Estado post-fix         : Pendiente validación en próxima corrida Actions (2026-08-07 11:00 UTC)
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | 0 | **Pendiente — gap real, ver diagnóstico 2026-08-07** |
| 2016 Q1-Q4 | 0/4 | 0 | **Pendiente — gap real, ver diagnóstico 2026-08-07** |
| 2017 Q1 (parcial) | 0/1 | 0 | **Pendiente — gap real, ver diagnóstico 2026-08-07** |
| 2017 Q2-Q4 | 3/3 | ? | Completo |
| 2018 Q1-Q4 | 4/4 | ? | Completo |
| 2019 Q1-Q4 | 4/4 | ? | Completo |
| 2020 Q1-Q4 | 4/4 | ? | Completo |
| 2021 Q1-Q4 | 4/4 | ? | Completo |
| 2022 Q1-Q4 | 4/4 | ? | Completo |
| 2023 Q1-Q4 | 4/4 | ? | Completo |
| 2024 Q1-Q4 | 4/4 | ? | Completo |
| 2025 Q1-Q4 | 4/4 | ? | Completo |
| 2026 Q1-Q2 (hasta 06-17) | 2/2 | ? | Completo |
| 2026 Q3 (en curso) | 0/1 | ? | En progreso (ventana de cola, se re-consulta a diario) |
| **TOTAL** | **37/46** | **?** | **Gap 2015-01 → 2017-03 sin cubrir; resto completo hasta 2026-06-17** |

> Conteo de artículos por trimestre no disponible (GDELT no lo registra por ventana en
> `processed.json`). Prioridad siguiente sesión: investigar el gap 2015-2017 (ver
> wiki/log.md 2026-08-07 08:30) — probar `fetch_historical.py --years 2015-2017` y/o una
> fuente alterna (Wayback CDX / sitemaps) si GDELT no cubre ese rango en español.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-07 | 0 (16 revisados, 16 falsos positivos) | 0 | Fix de 3 bugs: fetch_ddg_search sin filtro Panamá, ventana GDELT de cola duplicada (62→37 ventanas reales), mark_all_ingested con orden inconsistente. Ver wiki/log.md. |

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
