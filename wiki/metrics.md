---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-12
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 12 | **0 nuevos** ⚠️ 5 nuevos esta sesión |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 64 (huecos 2015-01→2017-03 sin cubrir) | cobertura continua 2015→hoy |
| Días sin artículos nuevos | 13 (último real: 2026-07-30) | máx 3 antes de diagnosticar ⚠️ SISTEMA EN FALLA |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions        : 2026-08-10 (corre diario 6:00 AM Panamá, mode=all)
Resultado últimas 5 corridas  : 0 artículos nuevos (2026-07-31, 08-02, 08-04, 08-07, 08-10)
Último artículo real nuevo    : 2026-07-30 → 13 días sin avance (supera el límite de 3)

Causa raíz A — GDELT (confirmada por datos en processed.json):
  La ventana GDELT final (inicio fijo 2026-06-18, fin = ayer) aparece en
  _gdelt_windows con 5 claves distintas (20260618_20260730, _20260801, _20260803,
  _20260806, _20260809) — una por cada corrida — porque fetch_gdelt_historical()
  nunca logra marcarla completa: falla con error de red en cada intento y el bucle
  termina justo después (es la última ventana del rango). Reproducido en esta
  sesión: la llamada directa a fetch_gdelt_batch() para ese rango devuelve
  "ProxyError / Tunnel connection failed: 403 Forbidden" al conectar a
  api.gdeltproject.org (bloqueo de red saliente en este entorno; no se pudo
  confirmar si el runner de GitHub Actions ve el mismo 403 o un timeout/rate-limit
  distinto de GDELT, pero el patrón de reintentos fallidos en processed.json es
  evidencia directa de producción, no de este sandbox).
  Adicionalmente: faltan por completo las ventanas 2015-01-01 → 2017-03-29
  (~9 trimestres) — nunca se marcaron "done", probablemente fallaron de forma
  persistente en corridas anteriores al reset de 2026-06-22 y quedaron huérfanas.

Causa raíz B — Falsos positivos por sigla "MIDA" (confirmada y corregida hoy):
  config/sources.yaml → search_terms.primary incluía el término suelto "MIDA".
  is_agro_relevant() hace match por substring sin contexto de país, y la búsqueda
  DDG "site:prensa.com" no siempre respeta el filtro de dominio, dejando pasar
  artículos de MIDA (Malasia) y MIDA (Utah, EE.UU. — data centers) marcados como
  fuente "prensa.com". Esto produjo 5 falsos positivos esta sesión (ver log.md
  2026-08-12). FIX APLICADO: se eliminó "MIDA" de search_terms.primary — la
  cobertura real de MIDA Panamá se mantiene vía RSS/DDG específicos de
  mida.gob.pa (ver web_searches.mida_noticias en config/sources.yaml).

Recomendaciones pendientes (no aplicadas esta sesión, requieren validar en
Actions con acceso de red real):
  1. Limitar reintentos de una ventana GDELT que falla N veces seguidas (ej. 3)
     y saltar al siguiente rango en vez de bloquear el avance indefinidamente.
  2. Rellenar manualmente (o con fetch-historical) las ventanas huérfanas
     2015-01-01 → 2017-03-29.
  3. Confirmar en los logs de GitHub Actions si el 403/timeout de GDELT es
     recurrente en el runner real (no solo en este sandbox).
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas completadas | Estado |
|---------|----------------------|--------|
| 2015 Q1-Q4 | 0/4 | ⚠️ Nunca cubierto — huérfano desde antes del reset 2026-06-22 |
| 2016 Q1-Q4 | 0/4 | ⚠️ Nunca cubierto — huérfano desde antes del reset 2026-06-22 |
| 2017 Q1-Q4 | 4/4 | Completo (arranca 2017-03-30) |
| 2018 Q1-Q4 | 4/4 | Completo |
| 2019 Q1-Q4 | 4/4 | Completo |
| 2020 Q1-Q4 | 4/4 | Completo |
| 2021 Q1-Q4 | 4/4 | Completo |
| 2022 Q1-Q4 | 4/4 | Completo |
| 2023 Q1-Q4 | 4/4 | Completo |
| 2024 Q1-Q4 | 4/4 | Completo |
| 2025 Q1-Q4 | 4/4 | Completo |
| 2026 (parcial) | 28 claves registradas | ⚠️ No son 28 ventanas reales — la ventana final (inicio fijo 2026-06-18) se reintenta y falla cada corrida, generando una clave nueva por día (fin=ayer cambia) en vez de reintentar la misma. Ver "Causa raíz A" arriba. |
| **TOTAL** | **64 claves / cobertura real ≈ 2017-03-30 → 2026-06-17** | **Huecos: 2015-01-01→2017-03-29 (nunca iniciado) y 2026-06-18→hoy (reintentos fallidos sin avanzar)** |

> Corrección 2026-08-12: la tabla anterior decía "0/46, backfill no iniciado", pero
> processed.json muestra 64 ventanas ya completadas 2017-2025. La tabla estaba
> desactualizada, no reflejaba las corridas de Actions entre 2026-06-22 y hoy.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-12 | 0 reales (5 falsos positivos descartados) | 11 | Sesión de routine: 5/5 artículos pendientes eran falsos positivos por sigla "MIDA" (Malasia/Utah) — no ingestados, marcados procesados. Fix aplicado: se quitó "MIDA" de search_terms.primary. Diagnóstico: sistema en falla — 13 días sin artículos nuevos reales (último: 2026-07-30), causa raíz = ventana GDELT final atascada en error de red desde ~2026-07-30 (ver "Estado del Fetch"). |

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
