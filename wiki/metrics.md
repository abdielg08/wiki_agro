---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-05
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 (7 previos + 16 hoy) | **0 nuevos en wiki/** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 62 / ~45 estimadas | 45+ (2015→hoy) — estimación superada |
| Días sin artículos nuevos | 6 (desde 2026-07-30) | máx 3 antes de diagnosticar → **⚠️ EXCEDIDO** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con artículos nuevos : 2026-07-30 (3 artículos)
Última corrida registrada           : 2026-08-04 (0 artículos nuevos)
Días consecutivos sin artículos     : 6 (07-31, 08-02, 08-04 con 0; 08-01/08-03/08-05
                                       sin commit en sources/ — corridas faltantes o sin
                                       resultado) → SUPERA el umbral de 3 días de CLAUDE.md

Causa identificada (sesión 2026-08-05):
  1. Ventanas GDELT completadas = 62, ya por encima de la estimación original de
     ~45 → el rango de fechas 2015→hoy está prácticamente agotado con la
     ventana de consulta actual; cada corrida nueva encuentra cada vez menos
     ventanas sin procesar, lo cual reduce el volumen de artículos nuevos
     genuinos con el tiempo (backfill se acerca a su límite natural).
  2. TASA DE FALSOS POSITIVOS 100% EN ESTA SESIÓN (16/16 revisados): la query
     GDELT de scripts/fetch_historical.py combina keywords genéricos de agro
     ("agricultura", "cosecha", "cultivo", "MIDA", etc.) con `sourcecountry:PA`,
     pero ese filtro NO está restringiendo correctamente — los 16 artículos
     pendientes de hoy eran de España, EE.UU./Utah, Malasia, Brasil, Arabia
     Saudita e Irán, todos etiquetados (incorrectamente) `country: PA,
     language: es` porque el fetcher fija esos valores sin verificar contenido
     (ver wiki/log.md, entrada de diagnóstico 2026-08-05 para el detalle
     completo y la recomendación de fix).
  3. RSS: única fuentes activas configuradas son IICA
     (https://www.iica.int/es/rss/noticias) y La Prensa
     (https://www.prensa.com/feed/, feed general — no hay feed de sección
     agropecuaria). El resto de fuentes en config/sources.yaml tienen
     `rss: null` (URLs desactualizadas, sin feed público, o bloqueo por bots).
     No se validó en vivo si estos 2 feeds están devolviendo entradas — pendiente
     de revisión en la próxima corrida de GitHub Actions o sesión con acceso de red.

Estado  : ⚠️ Requiere atención — el ritmo real de artículos NUEVOS Y VÁLIDOS
          (no falsos positivos) se está desacelerando. Recomendado: corregir
          el filtro de país en fetch_historical.py (ver recomendación en log.md)
          y/o ampliar la query más allá del rango 2015-2026 ya cubierto.
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
| **TOTAL** | **62/46 (estimación superada)** | **29 descargados / 6 reales** | **Backfill en curso, ritmo desacelerando** |

> Nota 2026-08-05: `processed.json._gdelt_windows` reporta 62 ventanas trimestrales
> completadas, por encima de la estimación original de 46 para 2015→hoy. El
> desglose por año/trimestre de esta tabla no se ha recalculado ventana por
> ventana en esta sesión — pendiente de un script que cruce `_gdelt_windows`
> contra el calendario real. La mayoría de artículos nuevos descargados
> últimamente resultan ser falsos positivos (ver Estado del Fetch arriba),
> no backfill histórico genuino de Panamá.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-05 | 0 (16 revisados, 16 falsos positivos) | 0 | Rutina automática: 100% falsos positivos por colisión de "MIDA" y filtro `sourcecountry:PA` roto en fetch_historical.py; además corregido bug de `mark-all-ingested`/`mark-ingested` (ver log.md) |

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
