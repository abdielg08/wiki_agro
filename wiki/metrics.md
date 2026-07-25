---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-25
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 18 | **0 nuevos reales** (todos documentados, no evitables desde el fetch) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 54 / ~46 estimadas | 46 (2015→hoy, ver anomalía abajo) |
| Días sin artículos nuevos (reales) | 5 (desde 2026-07-20) | máx 3 antes de diagnosticar → **ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions       : 2026-07-24 (workflow SÍ está corriendo diariamente)
Último artículo real nuevo   : 2026-07-20 (2 artículos)
Días consecutivos en 0       : 07-21, 07-23, 07-24 (07-22 sin commit) → ALARMA (≥3 días, umbral CLAUDE.md)
Artículos ingestados hoy     : 0 reales — los 11 pendientes al inicio de sesión eran
                                11/11 falsos positivos (ver wiki/log.md 2026-07-25)

DIAGNÓSTICO — anomalía en _gdelt_windows (54 completadas):
  2015: 0/4   2016: 0/4   2017-2025: 4/4 cada año (36 total)   2026: 18 (!)

  Causa probable A (2015-2016 = 0 completadas):
    fetch_gdelt_historical() en scripts/fetch_news.py itera secuencialmente desde
    date_range.start (2015-01-01) en cada corrida. Si fetch_gdelt_batch() devuelve
    None (error de red/API) para una ventana, el código hace `continue` SIN marcar
    la ventana como completada — pero además NO usa `break`, así que sigue avanzando
    en memoria hacia ventanas posteriores dentro de la misma corrida. Si GDELT
    responde con error consistentemente para 2015-2016 (posible límite real de la
    API v2 pese a que el rango teórico es 2015-02-19+), esas 8 ventanas se reintentan
    ÍNTEGRAMENTE cada día sin nunca persistir éxito, mientras 2017+ sí progresa.
    → Backfill real de 2015-2016 nunca ha avanzado pese a 54 "ventanas completadas".

  Causa probable B (2026 = 18 ventanas, debería ser ~2-3):
    El límite superior `end = min(config_end, utcnow() - 1 día)` es un blanco móvil:
    avanza cada día. La última ventana (parcial, aún no llega a 90 días) genera una
    `window_key` distinta cada corrida porque su fecha final cambia día a día, y cada
    una se marca completada por separado sin fusionarse con la anterior. Esto infla
    el conteo de "ventanas completadas" sin reflejar cobertura real nueva.

  Impacto: el conteo de 54/46 ventanas es engañoso — no indica que el rango 2015→hoy
  esté cubierto. La cobertura real de 2015-2016 sigue en 0.

Recomendación (no aplicada aún — requiere prueba contra la API real, fuera del
  alcance de esta sesión de rutina):
  1. Anclar las ventanas a límites de trimestre calendario fijos (no "hoy - N días")
     para que la última ventana del año en curso no cambie de key cada día.
  2. Si fetch_gdelt_batch() falla repetidamente para 2015-2016, verificar manualmente
     si la GDELT DOC 2.0 API realmente tiene cobertura ahí (probar la URL directo)
     y documentar si el límite real es distinto al declarado en CLAUDE.md.
  3. Considerar separar "ventanas intentadas sin éxito" de "ventanas completadas"
     para no ocultar fallas persistentes en el conteo agregado.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 Q1-Q4 | 0/4 | **Nunca completado — ver diagnóstico "Causa probable A"** |
| 2016 Q1-Q4 | 0/4 | **Nunca completado — ver diagnóstico "Causa probable A"** |
| 2017-2025 (9 años) | 36/36 (4/año) | Completo |
| 2026 (parcial) | 18 (ventanas duplicadas/solapadas, ver "Causa probable B") | Inflado — no confiar en el conteo |
| **TOTAL** | **54 (no comparable con la meta de 46)** | **2015-2016 sin cubrir en absoluto** |

> Rendimiento real de GDELT en este proyecto: de los 24 artículos en `sources/`, 18 llegaron
> vía GDELT/`prensa.com` y los 18/18 resultaron ser falsos positivos (0% de precisión hasta
> ahora). Los 6 artículos reales del wiki son semilla manual, no de GDELT. Esto sugiere que
> el query/filtro GDELT configurado es demasiado laxo — ver recomendaciones arriba.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-25 | 0 reales (11 falsos positivos revisados y descartados) | 0 | 11/11 pendientes eran falsos positivos por colisión de la palabra "MIDA" (Malasia/Utah). Fix de bug en `mark_ingested()` (crash con `_gdelt_windows`). Detectado y corregido mismatch entre `ingest` y `mark-all-ingested` (ordenan pendientes distinto). Diagnóstico de fetch: 5 días consecutivos sin artículos reales nuevos (alarma activa), anomalía en ventanas GDELT documentada arriba. |

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
