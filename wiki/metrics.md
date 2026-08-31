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
| Artículos ingestados | 17 | = total sin falsos positivos |
| Pendientes de ingesta | 34 | 0 |
| Falsos positivos acumulados | 8 | **0 nuevos** |
| Páginas en wiki/ | 24 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + backfill parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 76 / ~45 estimadas | 45 (2015→hoy) — **rango agotado, necesita expansión** |
| Días sin commit nuevo en sources/ | 4 (último: 2026-08-27) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida EXITOSA  : 2026-08-27 20:51 UTC (run #93) → 0 artículos nuevos
Última corrida (any)    : 2026-08-30 15:06 UTC (run #96) → FALLÓ
Corridas recientes      : #94 (2026-08-28), #95 (2026-08-29), #96 (2026-08-30)
                           las 3 con conclusion=failure, duración ~3-4 segundos cada una
Diagnóstico             : Un fallo en ~3s es demasiado rápido para llegar siquiera al paso
                           `pip install -r requirements.txt` (que toma minutos en corridas
                           exitosas). Esto apunta a un fallo a nivel de arranque del job
                           (runner no asignado, cuota de minutos de Actions agotada, o
                           permisos del repo para Actions/GITHUB_TOKEN), NO a un error en
                           el código de scripts/fetch*.py.
Logs                    : No disponibles vía API (HTTP 404 — expirados/purgados)
Ventanas GDELT          : 76 completadas, muy por encima de las ~45 estimadas para
                           cubrir 2015→hoy → el rango histórico configurado está agotado
                           y necesita expansión (ver fetch-historical / rango de fechas)
Acción recomendada       : Revisar en GitHub → Settings → Actions si hay restricciones de
                           permisos o cuota, y revisar el log completo de la corrida #96
                           directamente en la UI de Actions (la API ya no lo sirve)
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
| 2026-08-31 | 4 | 34 | Routine automatizada. 1 falso positivo detectado y rechazado (artículo de MITI/Malasia mal etiquetado como prensa.com/PA). Fix aplicado a bug de `mark-ingested` en scripts/ingest.py. GitHub Actions falla las últimas 3 corridas (#94-#96) — ver Estado del Fetch. |

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
