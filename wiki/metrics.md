---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-06
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 19 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 13 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 45 / ~45 estimadas | 45 (2015→hoy) |
| Días sin artículos nuevos (reales) | ~43 (desde 2026-05-24) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-04 (sin corrida detectada el 2026-07-05)
Resultado              : 0 artículos nuevos válidos desde 2026-05-24 (6 semanas)
Causa identificada     : fetch_ddg_search() en scripts/fetch_news.py NO aplicaba los
                         filtros _is_blocked_domain()/_is_panama_related() que sí usan
                         fetch_rss() y fetch_gdelt_historical(). ddgs.news() no respeta
                         de forma confiable "site:prensa.com", así que devolvió noticias
                         de sltrib.com (Utah, EE.UU.) y spa.gov.sa (Arabia Saudita) que
                         solo coincidían con keywords genéricos ("MIDA", "agricultura"),
                         etiquetadas ciegamente como source=prensa.com, country=PA.
                         Resultado: 6/6 artículos "nuevos" de las últimas 3 corridas
                         (2026-06-26 a 2026-07-02) eran falsos positivos — 100% de la
                         ruta DDG search contaminado.
Fix aplicado (hoy)     : se agregaron los mismos 2 filtros a fetch_ddg_search()
                         (scripts/fetch_news.py). Las 3 rutas de fetch (RSS, GDELT,
                         DDG) ahora aplican el mismo criterio de relevancia geográfica.
GDELT windows          : 45/45 completadas → backfill GDELT agotado, necesita expansión
                         de rango de fechas o queries adicionales (ver Progreso Backfill).
Estado post-fix        : Pendiente validación en próxima corrida Actions (2026-07-07+)
```

---

## Progreso del Backfill GDELT (2015 → hoy)

Calculado a partir de `sources/processed.json` → `_gdelt_windows` (45 ventanas registradas):

| Período | Ventanas completas | Estado |
|---------|---------------------|--------|
| 2015 | 0/4 | **Nunca completa — revisar** |
| 2016 | 0/4 | **Nunca completa — revisar** |
| 2017 | 4/4 | Completo |
| 2018 | 4/4 | Completo |
| 2019 | 4/4 | Completo |
| 2020 | 4/4 | Completo |
| 2021 | 4/4 | Completo |
| 2022 | 4/4 | Completo |
| 2023 | 4/4 | Completo |
| 2024 | 4/4 | Completo |
| 2025 | 4/4 | Completo |
| 2026 | 9 (solapadas) | En curso — la ventana final se regenera cada corrida porque su fecha de fin (`utcnow()-1d`) avanza a diario, produciendo un `window_key` nuevo en vez de reutilizar el anterior |
| **TOTAL** | **45** | Ver notas |

**Notas de diagnóstico** (no confirmado en vivo — este entorno no tiene acceso de red a
`api.gdeltproject.org`, bloqueado por el proxy sandbox; falta validar contra una corrida
real de GitHub Actions):
- Ninguna ventana de 2015-2016 aparece jamás como completada, pese a 45+ ventanas totales
  acumuladas. `fetch_gdelt_historical()` reintenta desde el inicio (`2015-01-01`) en cada
  corrida y solo marca una ventana como completa si la respuesta HTTP es exitosa — si las
  ventanas 2015-2016 fallan sistemáticamente (posible rate-limit, rango de fechas no
  soportado, o timeout), se reintentan cada día sin nunca avanzar, pero el resto de años sí
  progresa porque el bucle no se detiene en un fallo.
- La ventana final (año actual) genera una clave nueva cada día en vez de reusar/expandir
  la anterior, inflando el conteo de "ventanas completadas" sin aportar cobertura nueva real.
- Recomendación: agregar logging del código de error HTTP específico para 2015-2016 en la
  próxima corrida de Actions, y considerar anclar la ventana del año en curso a fin de mes
  en vez de a `utcnow()-1d` para evitar duplicados.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-06 | 0 (6 descartados) | 0 | 6/6 pendientes eran falsos positivos (colisión "MIDA" Utah + agro Arabia Saudita). Causa raíz encontrada y corregida en `fetch_ddg_search()`. Bugfix adicional en `mark_ingested()` (crash con `_gdelt_windows`). |

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
