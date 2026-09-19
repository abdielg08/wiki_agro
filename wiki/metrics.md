---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-19
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 39 | 0 |
| Falsos positivos acumulados | 7 | **0 nuevos** |
| Páginas en wiki/ | 28 (11 topics, 3 entities, 11 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + ingestas manuales) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 / ~45 estimadas | 45 (2015→hoy) — **rango agotado, necesita expansión** |
| Días sin artículos nuevos en sources/ | **13** (último commit sources/: 2026-09-06) | máx 3 antes de diagnosticar — **⚠ UMBRAL SUPERADO** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida wiki_daily.yml     : 2026-09-18 14:42 UTC — conclusion: FAILURE
Historial reciente (2026-09-09 → 2026-09-18): 10/10 corridas FALLARON consecutivamente
Duración de cada corrida fallida  : ~3-7 segundos (demasiado rápido para un fetch real de red)
Último commit exitoso en sources/ : 2026-09-06 (13 días sin artículos nuevos al 2026-09-19)
wiki_historical.yml               : 0 corridas registradas — NUNCA se ha ejecutado (ni manual ni programada)

Causa identificada  : Falla estructural, no rate-limit de GDELT. El job muere en segundos, lo
                      que apunta a un error temprano de script/config (ej. excepción sin
                      capturar, dependencia rota, o argumento inválido a wiki_agro.py fetch)
                      en lugar de un timeout de red — el paso "Fetch artículos nuevos" tiene
                      continue-on-error:true, así que la falla del job debe originarse en el
                      paso "Commit artículos nuevos" (git add/commit/push) u otro paso previo
                      sin continue-on-error.
                      Logs de las corridas fallidas ya expiraron (404 al intentar leerlos),
                      por lo que no se pudo confirmar el stack trace exacto desde esta sesión.
Ventanas GDELT      : 79/45 completadas — el rango histórico ya está "agotado" según la
                      heurística de CLAUDE.md, pero esto es irrelevante mientras el job falle
                      antes de llegar a ejecutar el fetch.
Acción recomendada  : Un mantenedor humano debe disparar wiki_daily.yml manualmente
                      (workflow_dispatch) y revisar el log del job "Fetch artículos → Commit a
                      sources/" mientras esté fresco, para identificar el error exacto. No se
                      aplicó ningún cambio al workflow desde esta sesión: no hay evidencia
                      suficiente para diagnosticar la causa raíz exacta sin ver un log en vivo,
                      y modificar el YAML a ciegas podría empeorar el problema.
Estado post-fix     : Sin resolver — pendiente de intervención manual
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
| **TOTAL** | **0/46** | **0** | **Backfill no iniciado** |

> Una vez que Actions corra con el código corregido, actualizar esta tabla con los datos reales.
> El rendimiento real de GDELT (artículos/trimestre) determinará la duración del backfill.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-19 | 5 (0 falsos positivos) | 39 | wiki_daily.yml lleva 10/10 corridas fallidas (2026-09-09→18); sin artículos nuevos en sources/ desde 2026-09-06 (13 días, umbral de 3 superado) |

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
