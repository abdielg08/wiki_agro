---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-17
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos descargados (sources/) | 57 | ↑ continuo |
| Artículos ingestados | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 39 | 0 |
| Falsos positivos acumulados | 7 | **0 nuevos** |
| Páginas en wiki/ | 25 (8 topics, 3 entities, 11 summaries, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2025 (artículos con fecha) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 | 45+ → rango agotado, necesita expansión |
| Días sin artículos nuevos en sources/ | **11** (último: 2026-09-06) | máx 3 antes de diagnosticar — **⚠️ ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions (completada)   : 2026-09-16 15:12 UTC (run #113)
Resultado                             : FAILURE — sin commit a sources/ (ni "0 artículos")
Último commit real en sources/        : 2026-09-06 ("6 artículos nuevos descargados", sha 24cfc3c)
Corridas fallidas consecutivas        : al menos 11 (runs #103–#113, 2026-09-07 → 2026-09-16),
                                         todas con conclusion="failure" y duración de ~4-5s
                                         (demasiado corta para instalar deps y correr el fetch;
                                         sugiere fallo temprano en el job, no timeout de red)
Logs del job                          : no recuperables vía API (HTTP 404 al pedir el contenido) —
                                         revisar manualmente en la pestaña Actions del repo:
                                         https://github.com/abdielg08/wiki_agro/actions/runs/35113787193
Ventanas GDELT completadas            : 79 (por encima del umbral de 45 → el rango histórico
                                         2015-hoy ya fue cubierto; esto NO explica el fallo actual,
                                         que ocurre antes de llegar a la lógica de fetch)
Hipótesis a revisar manualmente       : 1) límite de gasto/minutos de GitHub Actions agotado
                                         2) permiso de escritura del GITHUB_TOKEN revocado/cambiado
                                         3) cambio en requirements.txt o en el runner que rompe
                                            "pip install -r requirements.txt"
                                         4) el repo requiere aprobación manual para workflows
                                            programados (configuración de Actions)
Impacto en el sistema                 : CRÍTICO — supera el umbral de 3 días sin artículos nuevos
                                         definido como condición de falla en CLAUDE.md
```

---

## Progreso del Backfill GDELT (2015 → hoy)

- Ventanas GDELT completadas: **79**, por encima del estimado original de 45 ventanas para cubrir
  2015-02-19 → hoy. Esto indica que el rango histórico ya fue recorrido al menos una vez; el
  déficit de artículos nuevos actual se debe al fallo del workflow (ver arriba), no a falta de
  ventanas por procesar.
- Próximo paso una vez resuelto el fallo del workflow: evaluar si se requiere expandir el rango
  (ventanas más finas, o repetir ventanas con pocos resultados) para seguir encontrando artículos
  no descubiertos aún.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-17 | 5 | 39 | Diagnóstico: fetch de GitHub Actions falla desde 2026-09-07 (11 corridas fallidas seguidas, 0 commits nuevos a sources/) |

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

**Estado 2026-09-17**: la señal de alarma está ACTIVA (11 días sin artículos nuevos). El workflow
`.github/workflows/wiki_daily.yml` corre diariamente según el cron pero termina en `failure` en
~4-5 segundos, antes de que pueda producirse un commit (ni siquiera "0 artículos nuevos"). Los
logs no son accesibles vía la API de GitHub usada en esta sesión (HTTP 404). **Se requiere
revisión manual de la pestaña Actions del repositorio por el propietario** para identificar la
causa raíz (ver hipótesis en la sección "Estado del Fetch" arriba).
