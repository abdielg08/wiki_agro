---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-05
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 19 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 13 (¡13/13 de fuente `prensa.com` DDG!) | **0 nuevos tras fix** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 45 / ~45 estimadas | 45 (2015→hoy) — rango alcanzado |
| Días sin artículos nuevos | 2 (2026-07-03, 07-04) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-04 (corrió correctamente, 0 artículos nuevos)
Resultado               : 0 artículos nuevos 2026-07-03 y 2026-07-04 (2 días,
                          bajo el umbral de falla de 3 días)
Causa identificada      : (1) GDELT: 45 ventanas completadas → backfill ya
                          alcanzó la fecha actual, no es bloqueo/timeout.
                          (2) BUG en web_searches (DDG): fetch_ddg_search()
                          buscaba "MIDA" sin filtro de término panameño ni
                          validación de dominio real del resultado — trajo
                          13/13 artículos "prensa.com" que eran en realidad
                          de Malasia, Utah/EEUU, Arabia Saudita, IEEE y
                          World Bank genérico (0% relación con Panamá).
                          Ver wiki/log.md 2026-07-05 00:20 para detalle.
Fix aplicado            : scripts/fetch_news.py::fetch_ddg_search() ahora
                          valida que el dominio del resultado contenga el
                          `site` configurado y exige _is_panama_related()
                          (o "panam" en el cuerpo) antes de aceptar el
                          artículo — igual que el path RSS.
Estado post-fix         : Pendiente validación en próxima corrida Actions
                          (debería reducir "prensa.com" a 0 nuevos falsos
                          positivos; noticias reales de La Prensa Panamá
                          seguirán pasando el filtro de dominio + término PA)
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
| 2026-07-05 | 0 | 0 | 6 falsos positivos detectados y descartados (0 ingestados) + fix de `fetch_ddg_search()` (dominio real + término PA obligatorio) |

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
