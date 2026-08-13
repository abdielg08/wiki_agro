---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-13
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 | **0 nuevos desde el fix del 2026-08-13** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 65 (ver nota) | cobertura 2015→hoy |
| Días sin artículos nuevos (fetch diario) | ≥13 (último: 2026-07-30) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con commit : 2026-08-12 (0 artículos nuevos)
Últimos artículos nuevos  : 2026-07-30 (3) y 2026-07-29 (2) — luego 6 corridas
                             consecutivas (07-31, 08-02, 08-04, 08-07, 08-10, 08-12)
                             con 0 artículos nuevos → señal de alarma (>3 días).

DIAGNÓSTICO 2026-08-13 — falsos positivos (RESUELTO):
  Los 16 artículos pendientes al inicio de la sesión de hoy eran 100% falsos
  positivos (Arabia Saudita, Brasil, Irán, España/Aragón, EE.UU./Utah,
  Malasia) — ninguno sobre Panamá. Causa raíz: fetch_ddg_search() en
  scripts/fetch_news.py no validaba dominio/relevancia geográfica (a
  diferencia de fetch_rss(), que sí lo hace). El operador `site:` de DDGS no
  se aplica estrictamente, así que devolvía resultados de cualquier país y el
  código los guardaba con source="prensa.com"/country="PA" hardcodeados.
  FIX: se agregaron los mismos filtros (_is_blocked_domain, verificación de
  dominio real, _is_panama_related) a fetch_ddg_search(). Ver wiki/log.md
  2026-08-13 para el detalle completo. Pendiente: confirmar en la próxima
  corrida de Actions que ya no aparecen falsos positivos de este tipo.

DIAGNÓSTICO 2026-08-13 — 0 artículos nuevos en 6 corridas (ABIERTO, no
resuelto en esta sesión — requiere revisión adicional del pipeline RSS/DDG):
  Con fetch_ddg_search() ahora filtrando correctamente por Panamá, es
  esperable que el volumen de resultados baje mucho (la mayoría de lo que
  traía no era de Panamá). Hay que confirmar que las fuentes RSS (IICA, La
  Prensa) sigan activas y que las búsquedas DDG configuradas realmente
  apunten a dominios panameños — si tras el fix el fetch sigue en 0/día,
  el problema es la escasez de cobertura real de noticias agro-PA en RSS/DDG,
  no un bug de filtrado.

NOTA — ventanas GDELT (65 registradas, no 45): la cola de `_gdelt_windows`
mezcla ventanas trimestrales históricas completas (2017-03 → 2026-06, ~37
ventanas) con ~28 ventanas de "cola" cerca del presente (todas con inicio
2026-06-18 pero fin distinto cada día: .._20260623, .._20260624, ...,
.._20260811). Causa: en fetch_gdelt_historical(), `end = min(config_end,
utcnow()-1d)` avanza un día cada corrida, así que la ventana final nunca
tiene una clave estable y se re-registra como "nueva" cada día en vez de
cerrarse — infla el contador de ventanas sin reflejar cobertura real
adicional. Además faltan ventanas 2015-01 → 2017-03 (no aparecen en la lista;
posible pérdida de progreso o tracking duplicado con
scripts/fetch_historical.py::fetch_gdelt_years, que usa un archivo de
progreso distinto). No corregido en esta sesión — requiere revisar el
diseño de la ventana de cola antes de tocarlo, ya que corre en producción
vía GitHub Actions sin supervisión directa.
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
| 2026-08-13 | 0 reales / 16 falsos positivos descartados | 0 | 16/16 pendientes eran falsos positivos (agro global, no PA). Root cause encontrado y corregido en `fetch_ddg_search()`. Bug de doble-batch en `mark_all_ingested()` también corregido. Ver wiki/log.md. |

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
