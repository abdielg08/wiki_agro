---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-17
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 (7 previos + 16 esta sesión) | **0 nuevos reales colados** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal real (GDELT) | 2017-2026 | 2015 → hoy (faltan 2015-2016) |
| Ventanas GDELT completadas | 69 / ~46 estimadas | 2015→hoy sin huecos |
| Días sin artículos nuevos | 18 (desde 2026-07-30) | máx 3 antes de diagnosticar — **⚠ ALARMA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-16 (corre a diario, 6:00 AM Panamá)
Resultado               : 0 artículos nuevos (racha de 18 días desde 2026-07-30)
Causa identificada       : Dos problemas distintos, ver diagnóstico completo en wiki/log.md 2026-08-17:
  1. Faltan 8 ventanas GDELT de 2015-2016 (Q1-Q4 cada año) — nunca se completan,
     se reintentan cada corrida sin avanzar. Backfill real cubre solo 2017-2026.
  2. Cuando SÍ llegan artículos "nuevos", son en su mayoría falsos positivos:
     score_article() en prioritize.py puntúa alto cualquier mención de "MIDA"
     sin verificar que sea la agencia panameña (colisión con Utah Military
     Installation Development Authority, agencia de inversión de Malasia, etc.)
     — 16/16 artículos pendientes esta sesión eran ruido global sin relación
     con Panamá (España, Brasil, EE.UU., Arabia Saudita, Irán, Malasia, Utah).
Bug de código corregido : mark_all_ingested() en scripts/ingest.py marcaba un lote
                          DISTINTO al mostrado para revisión (find_pending() por
                          orden de archivo vs. prioritize() por score) — podía
                          marcar artículos reales como "ingestados" sin que el LLM
                          los viera nunca. Ahora lee las URLs exactas de
                          pending_ingest.md. Ver wiki/log.md 2026-08-17 para detalle.
Estado post-diagnóstico  : Pendiente: (1) investigar por qué 2015-2016 nunca completan
                          (no se pudo probar GDELT desde este sandbox, proxy bloqueado),
                          (2) acotar el filtro de relevancia para exigir mención
                          explícita de Panamá, no solo términos agro genéricos.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | ? | **⚠ Nunca completa — reintenta cada corrida sin avanzar** |
| 2016 Q1-Q4 | 0/4 | ? | **⚠ Nunca completa — reintenta cada corrida sin avanzar** |
| 2017 Q1-Q4 | 4/4 | ver processed.json | Completo |
| 2018 Q1-Q4 | 4/4 | ver processed.json | Completo |
| 2019 Q1-Q4 | 4/4 | ver processed.json | Completo |
| 2020 Q1-Q4 | 4/4 | ver processed.json | Completo |
| 2021 Q1-Q4 | 4/4 | ver processed.json | Completo |
| 2022 Q1-Q4 | 4/4 | ver processed.json | Completo |
| 2023 Q1-Q4 | 4/4 | ver processed.json | Completo |
| 2024 Q1-Q4 | 4/4 | ver processed.json | Completo |
| 2025 Q1-Q4 | 4/4 | ver processed.json | Completo |
| 2026 (cola móvil) | 33 ventanas de 1 día | ver processed.json | Avanza 1 ventana/día, sin huecos |
| **TOTAL** | **69/46 estimadas** | ver sources/ | **2017-2026 completo; 2015-2016 bloqueado (8 ventanas)** |

> 2015-2016 son las únicas ventanas que faltan del backfill trimestral. Investigar en la
> próxima sesión por qué fallan sistemáticamente (ver diagnóstico 2026-08-17 en log.md) —
> no se pudo probar el endpoint de GDELT desde este sandbox (proxy bloquea el dominio).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-17 | 0 (16 falsos positivos, 0 reales) | 0 | Fix de bug en mark_all_ingested (marcaba lote sin revisar) + diagnóstico completo de la contaminación de la cola y del bloqueo GDELT 2015-2016 — ver log.md |

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
