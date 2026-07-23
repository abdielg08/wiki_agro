---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-23
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados | 13 | = total sin falsos positivos |
| Falsos positivos acumulados | 18 (7 previos + 11 hoy) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 53 / ~45-64 estimadas | rango agotado, necesita expansión |
| Días sin artículos nuevos | 3 (2026-07-21 a 2026-07-23) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-23 12:25 UTC (commit 51e7fed)
Resultado              : 0 artículos nuevos (igual 2026-07-21; sin corrida 07-22)
                         Última vez con contenido nuevo: 2026-07-20 (2 artículos)
Causa identificada      : (1) Ventanas GDELT completadas = 53, por encima del
                         umbral de 45 → rango histórico configurado agotado,
                         necesita expandirse (nuevo --years en fetch-historical
                         o ajustar rango por defecto para cubrir 2026+).
                         (2) RSS IICA/La Prensa sin entradas nuevas en 3 días
                         — consistente con baja frecuencia de publicación,
                         no necesariamente una falla.
Bug encontrado hoy      : fetch_ddg_search() (mode=all, usado por el workflow
                         diario) no aplicaba _is_blocked_domain() ni
                         _is_panama_related() como sí hace fetch_rss(). El
                         operador site: de DDG no se respeta de forma
                         confiable, y la búsqueda "MIDA" hacía match con
                         Malaysia/Utah. Produjo 11 falsos positivos en la
                         cola de ingesta (ver wiki/log.md 2026-07-23).
Fix aplicado hoy        : scripts/fetch_news.py — mismos filtros de
                         fetch_rss() agregados a fetch_ddg_search().
                         scripts/ingest.py — mark_ingested() ya no crashea
                         con _gdelt_windows; mark_all_ingested() ahora usa
                         el mismo orden (strategy=score) que `ingest`.
Estado post-fix         : Pendiente validación en próxima corrida Actions
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
| 2026-07-23 | 0 | 0 | 11 falsos positivos rechazados (0 reales) + fix bug DDG search (fetch_ddg_search sin filtro Panamá) + fix mark_ingested/mark_all_ingested |

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
