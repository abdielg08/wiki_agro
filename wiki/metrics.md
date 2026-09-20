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
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 39 | 0 |
| Falsos positivos acumulados | 7 | **0 nuevos** |
| Páginas en wiki/ | 26 (9 topics, 3 entidades, 11 resúmenes, ~3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + prensa.com histórico) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 | ≥45 (rango ya agotado, ver abajo) |
| Días sin artículos nuevos en sources/ | **14** (último commit exitoso: 2026-09-06) | máx 3 antes de diagnosticar — 🔴 **EXCEDIDO** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions          : 2026-09-19 (run #116) — el workflow SÍ está corriendo a diario (cron 11:00 UTC)
Último commit exitoso a sources/: 2026-09-06 (run #103) → 14 días sin artículos nuevos
Resultado runs #104–#116        : "failure" en TODAS (09-07 a 09-19), cada una en ~4 segundos
Causa identificada               : El job falla casi instantáneamente (~4s), lo cual es demasiado rápido
                                    para un timeout de fetch/GDELT — es consistente con un fallo temprano
                                    en el job (checkout o instalación de dependencias), probablemente un
                                    problema de permisos/token de GITHUB_TOKEN o config del runner.
                                    NO se pudo confirmar la causa exacta: los logs del job ya no son
                                    descargables desde esta sesión (HTTP 404 en blob storage / URL firmada
                                    expirada, y el dominio de blob storage está bloqueado por el proxy
                                    de red de este entorno).
Runs previos también fallidos    : #94–#97 y #104 en adelante (patrón intermitente desde 2026-08-28,
                                    persistente desde 2026-09-07)
Acción recomendada (requiere humano): revisar el run en
  https://github.com/abdielg08/wiki_agro/actions/runs/35447538976
  y Settings → Actions → General → Workflow permissions (debe ser "Read and write permissions").
Estado post-diagnóstico          : PENDIENTE — no corregido en esta sesión (requiere acceso a Settings
                                    del repo y a los logs completos, fuera del alcance de esta sesión)
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| **TOTAL** | **79 ventanas completadas** (`_gdelt_windows` en processed.json) | 57 descargados (multi-fuente: prensa.com 51, MIDA 2, TVN 1, LaPrensaEco 1, BDA 1, IICA 1) | Ventanas GDELT ≥ 45 estimadas — el rango de fechas probablemente ya está agotado |

> No se recalculó el desglose trimestral 2015–2026 en esta sesión (no hay timestamps por ventana en
> `_gdelt_windows`, solo la lista de rangos completados). Dado que 79 ≥ 45 ventanas, per CLAUDE.md
> Paso 4.2 esto indica "rango de fechas agotado (necesita expansión)" — evaluar en próxima sesión si
> corresponde expandir el rango histórico o si el foco debe pasar a fuentes RSS (IICA, La Prensa).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-20 | 5 (arroz/MIDA, todos prensa.com) | 39 | 0% falsos positivos. Diagnóstico: fetch diario de GitHub Actions lleva 14 días fallando (último commit exitoso 2026-09-06); requiere revisión humana de permisos/config del workflow |

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
