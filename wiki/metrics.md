---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-27
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados | 13 | = total sin falsos positivos |
| Falsos positivos acumulados | 12 (7 previos + 5 nuevos 2026-07-27) | **0 nuevos** ⚠️ ver diagnóstico |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 56 / ~45 estimadas | 45 (2015→hoy) — **rango agotado** |
| Días sin artículos reales nuevos | 7 (desde 2026-07-20) | máx 3 antes de diagnosticar — **🔴 excedido** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-26 (corre diariamente, commits "chore(sources)")
Resultado              : 0-2 artículos "nuevos" por día, pero los últimos 2
                         (2026-07-20) eran falsos positivos (Utah MIDA)
Causa identificada     : (1) GDELT: 56 ventanas completadas (> 45 estimadas)
                             → el rango histórico 2015→hoy ya fue recorrido,
                             GDELT ya no aporta artículos nuevos genuinos.
                         (2) Fuente "prensa.com" del fetcher: NO está trayendo
                             La Prensa (Panamá) real — trae resultados de una
                             búsqueda genérica por "MIDA" que colisiona con
                             Malaysian Investment Development Authority y
                             Utah Military Installation Development Authority,
                             además de contenido aleatorio (archive.org,
                             IEEE, UNESCO, World Bank, Saudi Press Agency).
                         (3) RSS activas (IICA, La Prensa) no están aportando
                             volumen suficiente por sí solas.
Fix aplicado esta sesión: bug en scripts/ingest.py::mark_ingested() corregido
                         (crasheaba con la clave interna _gdelt_windows).
Fix pendiente (requiere código, fuera del alcance de la routine de wiki):
                         acotar la query de la fuente "prensa.com" a
                         `"MIDA" AND "Panamá"` o restringir dominio real de
                         prensa.com, para dejar de traer ruido de Malasia/Utah.
                         Ya se había "arreglado" un episodio similar el
                         2026-06-22 (7 falsos positivos) — el problema es
                         recurrente porque no se corrigió la fuente en sí.
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
| 2026-07-27 | 0 (5 falsos positivos rechazados) | 6 (también sospechosos de FP) | Colisión de keyword "MIDA" (Malasia/Utah) — ver log.md y diagnóstico arriba |

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
