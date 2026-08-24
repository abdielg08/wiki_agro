---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-24
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 30 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 24 (7 previos + 17 esta sesión) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 73 / ~45-46 estimadas | rango agotado — ver diagnóstico |
| Días sin artículos nuevos | 5 (último real: 2026-08-19) | máx 3 antes de diagnosticar — **⚠ ALARMA ACTIVA** |

---

## ⚠ Alarma activa: 5 días sin artículos nuevos (supera el máximo de 3)

El último artículo nuevo llegó el 2026-08-19. Desde entonces (08-20, 08-21, 08-22) el workflow de
GitHub Actions corrió y descargó 0 artículos nuevos cada vez; no hay commits de `sources/` para
08-23 ni 08-24 al momento de esta sesión (posible que Actions aún no haya corrido hoy, o que esté
fallando silenciosamente). Diagnóstico de causa (ver `wiki/log.md` 2026-08-24 para el detalle
completo):

1. **GDELT agotado**: 73 ventanas completadas ≥ 45-46 estimadas para cubrir 2015→hoy → el rango de
   fechas de GDELT ya se recorrió por completo. GDELT ya no es una fuente productiva de artículos
   nuevos hasta que se expanda el rango (o se re-procesen ventanas con criterios distintos).
2. **DDG (DuckDuckGo search) era la fuente activa pero sin filtro de país**: `fetch_ddg_search()`
   en `scripts/fetch_news.py` no aplicaba `_is_blocked_domain()` ni `_is_panama_related()` (los
   mismos filtros que sí usan `fetch_rss()` y `fetch_gdelt_window()`), y el operador `site:` de DDG
   no se respeta de forma confiable. Resultado: los 17 artículos pendientes de esta sesión eran
   100% falsos positivos de dominios ajenos a Panamá (España, EE.UU., Arabia Saudita, Brasil, Irán,
   Malasia), todos mal-etiquetados como fuente "prensa.com". **Fix aplicado esta sesión** (ver log)
   — pendiente validar en la próxima corrida real de Actions si esto reduce el volumen de falsos
   positivos y si quedan artículos genuinamente panameños por descubrir vía DDG.
3. **RSS**: IICA y La Prensa siguen siendo las únicas fuentes RSS activas — no se diagnosticó su
   estado esta sesión; revisar en la próxima routine si siguen sin producir entradas.

**Próxima acción recomendada**: expandir el rango de fechas de GDELT (o probar `fetch --mode cdx`
para dominios de medios panameños) y verificar que el fix de `fetch_ddg_search` produzca resultados
relevantes reales en la próxima corrida de Actions.

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con datos en sources/ : 2026-08-22 (0 artículos nuevos)
Último artículo nuevo real           : 2026-08-19 (1 artículo)
Resultado corridas recientes          : 0 artículos nuevos desde 2026-08-20
Causa identificada (esta sesión)      : GDELT con 73/~45-46 ventanas completadas → rango agotado.
                                         fetch_ddg_search() sin filtro de país → solo producía
                                         falsos positivos, no aportaba artículos reales nuevos.
Fix aplicado                          : fetch_ddg_search() ahora aplica _is_blocked_domain() y
                                         _is_panama_related() antes de aceptar un resultado.
Estado post-fix                       : Pendiente validación en próxima corrida Actions.
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
| 2026-08-24 | 0 | 0 | 17/17 falsos positivos descartados (0 reales); fix de bugs mark-ingested/mark-all-ingested; fix de fetch_ddg_search sin filtro de país (causa raíz de los falsos positivos); alarma: 5 días sin artículos nuevos |

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
