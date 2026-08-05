---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-05
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 12 | **0 nuevos** (0% preservado — 5 detectados y rechazados hoy) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 62 | 45+ (2015→hoy) |
| Días sin artículos nuevos | 6 (desde 2026-07-30) | máx 3 antes de diagnosticar — **SUPERADO** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-04 (corre ~diario, ver git log -- sources/)
Resultado               : 0 artículos nuevos últimos 2 días; última carga real fue 2026-07-30 (3 art.)
Causa identificada (2026-08-05): el fetch SÍ está corriendo, pero la fuente "laprensa_agro"
                          (DDG search "site:prensa.com ... MIDA ...") no está restringiendo
                          resultados al dominio prensa.com. ddgs.news() ignora el operador
                          site: y devuelve noticias globales que matchean "MIDA" por colisión
                          de acrónimo (Malaysian Investment Development Authority, Utah
                          Military Installation Development Authority, etc.), guardadas todas
                          como source="prensa.com" sin validar el dominio real.
                          Se confirmó inspeccionando processed.json: los 16 artículos pendientes
                          al inicio de esta sesión provenían TODOS de dominios ajenos a Panamá
                          (sltrib.com, paultan.org, spa.gov.sa, nyfb.org, whc.unesco.org,
                          ieeexplore.ieee.org, archive.org, msn.com, heraldo.es, agenciabrasil.ebc.com.br).
                          5 de esos 16 se triagearon hoy (todos falsos positivos, ver wiki/log.md);
                          quedan 11 pendientes con el mismo patrón, pendientes de triage.
Fix previo (2026-06-22) : fetch_gdelt_historical() limita end a datetime.utcnow()-1d — vigente,
                          ventanas GDELT avanzando (62 completadas), pero GDELT no está aportando
                          contenido nuevo real de Panamá en las corridas recientes; casi todo el
                          volumen entrante viene del canal DDG contaminado.
Recomendación pendiente : validar dominio de cada resultado ddgs.news() contra site_cfg["site"]
                          antes de guardar, y/o quitar el término ambiguo "MIDA" de la query o
                          forzar "Panamá" en el query string (fuera de alcance de esta routine —
                          requiere editar scripts/fetch_news.py).
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
| 2026-08-05 | 0 | 11 | 5 falsos positivos rechazados (bug DDG site: filter, ver Estado del Fetch); 11 pendientes con el mismo patrón sin triagear |

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
