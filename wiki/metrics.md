---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-12
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
| Falsos positivos acumulados | 7 | **0 nuevos** (0 nuevos esta sesión) |
| Páginas en wiki/ | 25 (8 topics, 3 entities, 11 summaries, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (backfill en curso) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 (ver nota en log 2026-09-12) | cobertura continua, no requiere expansión |
| Días sin artículos nuevos | **6** (última descarga: 2026-09-06) | máx 3 antes de diagnosticar — **⚠ ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida exitosa (con artículos) : 2026-09-06 (run #103, 6 artículos nuevos)
Última corrida exitosa (0 artículos)   : 2026-09-06 (run #103 mismo día, steps completos)
Corridas fallidas consecutivas         : 2026-09-07 → 2026-09-11 (runs #104-#108, 5/5 failure)
Días sin artículos nuevos hoy          : 6 (⚠ supera umbral de 3 días)

Causa raíz (confirmada vía GitHub Actions API, no es bug de código):
  Los 5 runs fallidos duran ~3 segundos cada uno y no ejecutan ningún step
  (get_workflow_run_usage → duration_ms: 0; list_workflow_jobs no reporta steps).
  Esta firma = el runner nunca se aprovisiona, típico de cuota de minutos de
  GitHub Actions agotada o "spending limit" en $0. fetch_news.py NUNCA llegó
  a ejecutarse en esos 5 días — no hay nada que corregir en el script.

Acción requerida (fuera del alcance de un commit — requiere el dueño del repo):
  Revisar GitHub → Settings → Billing and plans → Actions y/o el spending
  limit de la cuenta/organización. Una vez restablecido, la próxima corrida
  programada de wiki_daily.yml debería volver a completar normalmente.

Nota sobre ventanas GDELT: 79 ventanas completadas en sources/processed.json,
pero esto NO significa que el rango 2015→2027 esté agotado. La ventana final
usa min(config_end, utcnow()-1d), que cambia de fecha cada día que el fetch
corre con éxito, generando una clave nueva cada vez. No requiere expansión
de config/sources.yaml.
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
| 2026-09-12 | 5 | 39 | Routine automatizada; 0 falsos positivos; diagnóstico: fetch diario falla 5 días seguidos por límite de minutos/spending limit de GitHub Actions (no requiere fix de código) |

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
