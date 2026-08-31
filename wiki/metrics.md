---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-31
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 51 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Falsos positivos acumulados | 8 (7 previos + 1 hoy: paultan.org/MITI Malasia) | **0 nuevos** ⚠️ meta incumplida hoy |
| Páginas en wiki/ | 24 | ↑ continuo |
| Cobertura temporal | 2015-2026 (parcial, dominado por 2022-2024) | 2015 → hoy real |
| Ventanas GDELT completadas | no expuesto en processed.json actual | 45 (2015→hoy) |
| Días sin artículos nuevos en sources/ | **3-4 días** (último commit de fetch: 2026-08-27) | máx 3 antes de diagnosticar ⚠️ **UMBRAL SUPERADO** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions      : 2026-08-30 15:06 UTC (run #96) — CONCLUSIÓN: failure
Corridas previas             : #95 (2026-08-29) failure | #94 (2026-08-28) failure
                                #93 (2026-08-27) success — 0 artículos nuevos
Último commit con artículos  : 2e30165 "1 artículos nuevos descargados" — 2026-08-27
Causa identificada            : Las 3 corridas más recientes (#94, #95, #96) fallaron en
                                ~3-6 segundos — tiempo insuficiente para completar
                                checkout + setup-python + pip install + fetch. Apunta a un
                                fallo temprano (runner/quota/permisos), NO a un error dentro
                                de wiki_agro.py fetch. Logs no disponibles vía API (HTTP 404
                                al descargarlos) — no se pudo confirmar la causa exacta.
Acción recomendada            : Revisar manualmente los logs en GitHub:
                                https://github.com/abdielg08/wiki_agro/actions/runs/33318722494
                                https://github.com/abdielg08/wiki_agro/actions/runs/33260107823
                                https://github.com/abdielg08/wiki_agro/actions/runs/33211853678
                                Posibles causas: cuota de Actions agotada, permisos de
                                GITHUB_TOKEN cambiados, o incidente de GitHub Actions.
Estado                         : SEÑAL DE ALARMA — 3 días consecutivos sin artículos nuevos
                                en sources/articles/ (umbral del CLAUDE.md alcanzado)
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
| 2026-08-31 | 4 (de 5 pendientes; 1 falso positivo) | 33 | Fetch de GitHub Actions falla 3 días consecutivos (#94-#96); ver Estado del Fetch |

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
