---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-20
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ (descargados) | 57 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Artículos pendientes de ingesta | 39 | 0 |
| Falsos positivos acumulados (sesión) | 0 nuevos (5/5 verificados 100% agro-Panamá) | **0 nuevos** |
| Páginas en wiki/ | 27 (10 topics, 3 entities, 11 summaries, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 | 2015 → hoy real |
| Ventanas GDELT completadas | 79 | 45 (2015→hoy) — **umbral superado, rango agotado** |
| Días sin artículos nuevos en sources/ | **14** (último commit: 2026-09-06) | máx 3 antes de diagnosticar — **🚨 ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions           : 2026-09-19 14:02 UTC (run #116) — CORRIÓ pero FALLÓ
Resultado                        : 0 artículos nuevos (falla antes de ejecutar el fetch)
Último commit real en sources/   : 2026-09-06 (run #103, exitoso) → 14 días sin artículos nuevos

Diagnóstico (2026-09-20):
  - Runs #104-#116 (2026-09-07 → 2026-09-19): 13 corridas CONSECUTIVAS con
    conclusion=failure, cada una completada en ~3-4 segundos.
  - Ese tiempo de ejecución es demasiado corto para llegar siquiera al paso
    "pip install" (mucho menos a fetch/stats/commit), lo que descarta un bug
    en wiki_agro.py o en la lógica de fetch — el job falla antes de correr
    ningún step real.
  - No hubo cambios recientes en .github/workflows/wiki_daily.yml (verificado
    con git log) que expliquen la ruptura.
  - Los runs #94-#97 (2026-08-28 → 2026-08-31) ya mostraban fallas
    intermitentes con la misma firma (~3-4s), antes de volverse 100%
    consistentes desde el run #104 en adelante.
  - No fue posible descargar los logs del job (`get_job_logs` → HTTP 404;
    descarga directa del ZIP de logs bloqueada por la política de red del
    proxy de este entorno) para confirmar la causa exacta.
  - Hipótesis más probable dado el patrón (fallo uniforme e inmediato, sin
    relación con el código): límite de minutos/gasto de GitHub Actions
    alcanzado en la cuenta, o un cambio en permisos/configuración de Actions
    a nivel de repositorio u organización.
  - Ventanas GDELT ya en 79 (≥45): el rango de fechas GDELT también está
    agotado y requeriría expansión una vez que el fetch vuelva a correr.

Acción recomendada (requiere acceso humano al dashboard de GitHub):
  1. Revisar Settings → Actions → General del repo (¿Actions deshabilitado
     o restringido?)
  2. Revisar Billing → Plans and usage → Actions minutes (¿se agotó la
     cuota incluida o el spending limit configurado?)
  3. Una vez resuelto, disparar manualmente el workflow (workflow_dispatch)
     para confirmar que vuelve a completar el fetch real
  4. Expandir el rango de ventanas GDELT más allá de lo ya cubierto (79
     ventanas completadas)
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
| 2026-09-20 | 5 (0 falsos positivos) | 39 | Routine automática; diagnosticado GitHub Actions fallando 13 corridas consecutivas desde 2026-09-07 |

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
