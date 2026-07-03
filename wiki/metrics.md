---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-03
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 19 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 13 (7 previos + 6 el 2026-07-03) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 37 reales / ~45 estimadas (+7 parciales del período actual) | 45 (2015→hoy) |
| Días sin artículos nuevos | 1 (hoy, 2026-07-03) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-03 (run 28661759040) — SUCCESS
Resultado               : 0 artículos nuevos guardados hoy
Backfill GDELT          : ESTANCADO en 2017-03-30. Las 9 ventanas del rango
                          2015-01-01 → 2017-03-29 fallan TODAS, cada corrida,
                          con "error de red" (timeout) o "GET blocked (403/429)"
                          en api.gdeltproject.org. Como nunca se marcan completas,
                          se reintentan desde cero cada día y vuelven a fallar —
                          el backfill de 2015-2017 no avanza.
RSS                     : IICA y LaPrensaGeneral → 0 entradas hoy
Búsqueda DDG            : 7/8 queries devuelven "No results found" (mida.gob.pa,
                          idiap.gob.pa, bda.gob.pa, fao.org, bancomundial.org,
                          iica.int, oirsa.org) — solo prensa_agro devuelve resultados
Falsos positivos        : los 6 detectados hoy (Utah "MIDA"/data centers, NY Farm
                          Bureau, "Reef Saudi") vienen de la query GDELT genérica
                          de agricultura sin filtro geográfico Panamá — el JSON
                          fuente los etiqueta `country: PA` incorrectamente
Diagnóstico completo    : ver wiki/log.md, entrada 2026-07-03 16:10
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 Q1-Q4 | 0/4 | **Bloqueado — GDELT 403/429 cada corrida** |
| 2016 Q1-Q4 | 0/4 | **Bloqueado — GDELT 403/429 cada corrida** |
| 2017 Q1 (parcial, hasta 03-29) | 0/1 | **Bloqueado — GDELT 403/429 cada corrida** |
| 2017 Q2-Q4 → 2026 Q2 (2017-03-30 → 2026-06-17) | 37/37 | ✓ Completo |
| 2026-06-18 → hoy | ventana viva (se re-abre cada día) | En curso |
| **TOTAL histórico (2015-02 → 2017-03-29)** | **0/9** | **Estancado — ver diagnóstico 2026-07-03** |
| **TOTAL resto (2017-03-30 → hoy)** | **37/37 + ventana viva** | **Completo / al día** |

> Diagnóstico 2026-07-03: el tramo 2015-01-01 → 2017-03-29 (9 ventanas) falla en
> el 100% de las corridas de GitHub Actions con timeout o "GET blocked (403/429)"
> de api.gdeltproject.org. No se marcan como completas nunca, por lo que se
> reintentan (y fallan) todos los días sin progreso. Requiere intervención en
> `scripts/fetch_news.py` (backoff/estrategia distinta para ese rango) — fuera del
> alcance de esta sesión de routine. Ver wiki/log.md 2026-07-03 16:10.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-03 | 0 (6 revisados, 6/6 falsos positivos) | 0 | Diagnóstico: backfill GDELT 2015-2017 estancado por bloqueo 403/429 (ver log) |

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
