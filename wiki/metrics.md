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
| Artículos en sources/ | 26 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 20 (7 previos + 13 nuevos hoy) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 58 / ~46 estimadas | 45 (2015→hoy) |
| Días sin artículos nuevos | 0 (2 nuevos el 2026-07-29) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-29 (2 artículos nuevos)
Resultado               : Actions SÍ está corriendo — commits diarios/casi diarios
                          en sources/ con "[skip ci]" (26 artículos totales)
Ventanas GDELT          : 58/46 completadas → rango 2015→hoy ya agotado por GDELT
                          (backfill histórico vía GDELT esencialmente cubierto;
                          nuevas ventanas ya no aportan volumen significativo)
Problema identificado   : 13/13 artículos pendientes de esta sesión eran falsos
                          positivos (0% reales) — ver wiki/log.md 2026-07-29.
                          Causa: la búsqueda web DDG (`prensa_agro` en
                          config/sources.yaml) no validaba dominio ni exigía
                          mención de Panamá, a diferencia del RSS y GDELT que sí
                          lo hacían. Coincidencias espurias de "MIDA" con
                          Malasia (MITI/MARii) y Utah (Military Installation
                          Development Authority) contaminaron 13 artículos.
Fix aplicado            : scripts/fetch_news.py → fetch_ddg_search() ahora exige
                          coincidencia real de dominio (_url_domain) y al menos
                          un término panameño (_is_panama_related), igual que
                          fetch_rss() y fetch_gdelt_batch(). Commit en esta sesión.
Estado post-fix         : Pendiente validar en próxima corrida de Actions que la
                          búsqueda DDG deje de producir falsos positivos.
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
| 2026-07-29 | 0 | 0 | 13/13 pendientes eran falsos positivos (0 reales) — fix de raíz en fetch_ddg_search() (validación de dominio + término panameño obligatorio) |

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
