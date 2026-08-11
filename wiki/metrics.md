---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-11
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 (7 previos + 16 esta sesión) | **0 nuevos** desde el fix de `fetch_news.py` (2026-06-22) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 64 / ~45 estimadas | 45 (2015→hoy) — pero con hueco real, ver abajo |
| Días sin artículos nuevos | 3+ (commits 08-04, 08-07, 08-10 con 0 artículos) | máx 3 antes de diagnosticar → **umbral alcanzado, ver diagnóstico** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con cambios en sources/ : 2026-08-10 (0 artículos nuevos, [skip ci])
Commits de sources/ en 7 días          : 08-04, 08-07, 08-10 (no diario pese a cron "0 11 * * *")
Resultado                              : 0 artículos nuevos en las últimas 3 corridas registradas
Causa identificada (esta sesión)       : (1) el filtro de relevancia Panamá (_is_panama_related /
                                          _is_blocked_domain), ya presente en fetch_news.py desde
                                          el fix de 2026-06-22, está funcionando — ya no entran
                                          falsos positivos nuevos a sources/articles/.
                                          (2) La cobertura GDELT quarter-a-quarter desde 2017-03-30
                                          ya es densa (64 ventanas); queda poco contenido nuevo por
                                          descubrir en el rango ya escaneado.
                                          (3) HUECO REAL: 2015-01-01 → 2017-03-29 (rango configurado
                                          en config/sources.yaml) nunca se ha escaneado con GDELT.
Fix aplicado esta sesión               : scripts/fetch_historical.py (crawler manual histórico) no
                                          tenía el filtro Panamá — se agregó, para cuando se dispare
                                          el workflow "Crawl Histórico 15 Años".
Acción recomendada (pendiente)         : disparar manualmente "Crawl Histórico 15 Años" acotado a
                                          2015-2017 para cerrar el hueco — no ejecutado esta sesión
                                          por ser potencialmente una corrida larga en CI; requiere
                                          decisión explícita del usuario.
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
| 2026-08-11 | 0 (16 revisados, todos falsos positivos) | 0 | Backlog pre-fix limpiado; 3 bugs corregidos en scripts/ingest.py y fetch_historical.py; hueco 2015-2017 identificado |

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
