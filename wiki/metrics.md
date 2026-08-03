---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-03
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 12 | **0 nuevos** |
| Pendientes de ingesta | 11 | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 61 / ~46 estimadas | 45+ (2015→hoy) — rango agotado |
| Días sin artículos nuevos | 2 corridas consecutivas (07-31, 08-02) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-02 (chore(sources): 0 artículos nuevos)
Resultado              : 0 artículos nuevos — 2ª corrida consecutiva en 0
                         (07-30 y 07-29 sí trajeron 3 y 2 artículos, así que
                         no es una falla sostenida, solo días secos normales)
Ventanas GDELT          : 61 completadas — por encima del umbral de 45,
                         el rango 2015→hoy ya fue cubierto por el backfill;
                         los "0 nuevos" ahora reflejan que no hay noticias
                         agro-PA nuevas ese día, no un fallo de fetch
Causa de los 5 falsos positivos de esta sesión (ver wiki/log.md 2026-08-03):
                         fetch_ddg_search() en scripts/fetch_news.py no exigía
                         mención de Panamá (a diferencia de fetch_rss/fetch_gdelt),
                         dejando pasar colisiones del acrónimo "MIDA" con
                         Malaysia (paultan.org, thestar.com.my) y Utah, EE.UU.
                         (sltrib.com — "Military Installation Development Authority")
Fix aplicado esta sesión: se agregaron _is_blocked_domain() + _is_panama_related()
                         a fetch_ddg_search(), igualando el estándar de los
                         otros dos fetchers. Pendiente validar en próxima
                         corrida de Actions que no reaparezcan falsos positivos
                         de las búsquedas prensa_agro/oirsa_alertas/mida_noticias/
                         idiap_investigacion.
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
| 2026-08-03 | 0 (5 revisados, 5 falsos positivos) | 11 | Fix de raíz en fetch_ddg_search() (faltaba `_is_panama_related`) |

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
