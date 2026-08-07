---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-07
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 (7 previos + 16 hoy) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 62 (rango real: 2017-03-30 → 2026-08-03) | cubrir desde 2015-02-19 |
| Días sin artículos nuevos | **8 días** (último `saved_at`: 2026-07-30) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con artículos nuevos : 2026-07-30 (8 días sin nuevos artículos — supera
                                       el umbral de falla de 3 días de CLAUDE.md)
Resultado hoy (2026-08-07)          : 0 artículos nuevos en sources/articles/

PROBLEMA #1 (identificado y corregido hoy):
  fetch_ddg_search() en scripts/fetch_news.py no filtraba por relevancia
  geográfica → 16/16 artículos pendientes eran falsos positivos globales
  (Malasia, Utah, España, Brasil) que coincidían con términos ambiguos
  como "MIDA" o "agricultura". Fix: se agregó _is_panama_related() a
  fetch_ddg_search(), igual que ya tenían fetch_rss() y el fetcher GDELT.
  Ver wiki/log.md 2026-08-07 para el detalle completo.

PROBLEMA #2 (pendiente de diagnóstico — requiere revisar corridas de Actions):
  A pesar de 62 ventanas GDELT "completadas", el rango real cubierto es
  2017-03-30 → 2026-08-03 — el período 2015-02-19 a 2017-03-29 (objetivo
  de cobertura) AÚN NO se ha procesado. Varias ventanas registradas
  comparten la misma fecha de inicio (ej. tres ventanas distintas que
  empiezan en 2026-06-18), lo que sugiere que la selección de ventanas en
  fetch_historical.py puede estar re-visitando periodos recientes en vez
  de avanzar sistemáticamente hacia atrás desde 2015. No se modificó ese
  código esta sesión — se documenta para revisión en la próxima sesión.
  Esto es probablemente también la causa de los 8 días sin artículos
  nuevos: si GDELT sigue re-consultando ventanas ya vistas (2026), no
  hay contenido nuevo que descubrir, y las fuentes RSS activas
  (IICA, La Prensa) no producen suficiente volumen por sí solas.

Estado post-fix : Fix de falsos positivos aplicado. Pendiente validar en
                   la próxima corrida de Actions si vuelven a aparecer
                   artículos nuevos reales; si no, investigar
                   fetch_historical.py (selección de ventanas GDELT).
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
| 2026-08-07 | 0 reales (16 falsos positivos detectados y excluidos) | 0 | Fix de bug en fetch_ddg_search() (faltaba filtro Panamá); 8 días sin artículos nuevos — ver diagnóstico arriba |

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
