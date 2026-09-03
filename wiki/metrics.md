---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-03
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 51 | ↑ continuo |
| Artículos ingestados (total, incl. falsos positivos) | 18 | = total sin pendientes |
| Artículos reales ingestados al wiki | 10 | = total sin falsos positivos |
| Falsos positivos acumulados | 8 | **0 nuevos** (1 detectado esta sesión, ver log 2026-09-03) |
| Pendientes de ingesta | 33 | 0 |
| Páginas en wiki/ | 26 (10 topics, 3 entities, 10 summaries) | ↑ continuo |
| Cobertura temporal | 2015-2026 (backfill en curso) | 2015 → hoy real |
| Ventanas GDELT completadas | 78 / ~45 estimadas | 45 (2015→hoy) — **rango agotado, requiere expansión** |
| Días sin artículos nuevos | 7 (último real: 2026-08-27) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-09-03 (SÍ corrió — commit "0 artículos nuevos descargados")
Resultado               : 0 artículos nuevos (igual que 2026-09-01; último real fue 2026-08-27)
Causa identificada      : Ventanas GDELT completadas = 78, por encima de las ~45 estimadas
                          para cubrir 2015→hoy → el rango histórico ya fue barrido por GDELT.
                          Los 0 nuevos ya no son timeout/bloqueo sino agotamiento del rango.
                          RSS IICA y La Prensa siguen activos, aportan artículos ocasionales.
Recomendación           : expandir backfill — sub-particionar ventanas ya cubiertas (semanal
                          en vez de trimestral) o sumar nuevas fuentes RSS/GDELT.
Bug encontrado          : `wiki_agro.py mark-ingested '<url>'` falla (AttributeError) porque
                          scripts/ingest.py:145 no filtra la clave interna `_gdelt_windows`
                          (lista) al iterar processed.items(). Usar `mark-all-ingested --limit N`
                          mientras no se corrija.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| **TOTAL** | **78/~45 estimadas** | **51 (sources/)** | **Rango 2015→hoy cubierto por GDELT; requiere expansión (ver Estado del Fetch)** |

> `sources/processed.json._gdelt_windows` registra 78 ventanas completadas, superando la
> estimación inicial de ~45 para cubrir 2015→hoy. El desglose por trimestre no se guarda en
> processed.json (solo la lista plana de ventanas), por lo que la tabla trimestral anterior no
> se puede reconstruir sin instrumentar `fetch_gdelt_historical()` para registrar período+conteo
> por ventana. Próxima mejora sugerida: loggear (ventana, artículos_encontrados) por corrida.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-03 | 5 (4 reales + 1 falso positivo) | 33 | Routine: git pull + ingest --limit 5; falso positivo MITI/Malasia detectado y documentado en log.md |

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
