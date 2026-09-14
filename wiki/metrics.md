---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-14
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos ingestados (total) | 18 | = descargados |
| Artículos reales ingestados | 11 | = total sin falsos positivos |
| Falsos positivos acumulados | 7 | **0 nuevos** |
| Pendientes de ingesta | 39 | 0 |
| Páginas en wiki/ | 27 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + prensa.com) | 2015 → hoy real |
| Ventanas GDELT completadas | 0 / ~45 estimadas | 45 (2015→hoy) |
| Días sin commits nuevos en sources/ | **8** (último: 2026-09-06) | máx 3 antes de diagnosticar |

**⚠️ ALERTA — umbral de falla superado**: han pasado 8 días sin artículos nuevos en
`sources/articles/` (último commit de fetch exitoso: `bcc74c2`, 2026-09-06). Esto
supera el límite de 3 días definido como criterio de falla en CLAUDE.md.

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con commit nuevo : 2026-09-06 (0 artículos — la anterior con
                                   contenido real fue 2026-09-07, 6 artículos,
                                   pero ese mismo run terminó en FAILURE)
Corridas 2026-09-07 → 2026-09-13 : 7 corridas consecutivas, TODAS con
                                    conclusion=FAILURE
Causa identificada (vía GitHub Actions API): en las 7 corridas fallidas, el
  job "Fetch artículos → Commit a sources/" nunca llegó a asignarse un runner
  (runner_id=0, runner_name vacío) y terminó en ~3 segundos — un tiempo
  demasiado corto incluso para completar el `actions/checkout`. Este patrón
  (fallo instantáneo sin runner asignado, repetido en cada corrida programada)
  es característico de:
    (a) minutos de GitHub Actions agotados para el plan/cuenta, o
    (b) un límite de gasto ("spending limit") en $0 alcanzado, o
    (c) Actions deshabilitado/restringido a nivel de organización o repo.
  No se pudo confirmar la causa exacta porque los logs de esas corridas ya
  expiraron (retención de GitHub); el patrón runner_id=0 + duración ~3s es la
  evidencia disponible.
Acción recomendada     : el usuario debe revisar
                          https://github.com/settings/billing (minutos/spending
                          limit de Actions) y Settings → Actions → General del
                          repo abdielg08/wiki_agro, y re-disparar el workflow
                          "Wiki Agropecuario — Fetch Diario" manualmente
                          (workflow_dispatch) tras corregir la causa.
Fix histórico previo    : fetch_gdelt_historical() limita end a datetime.utcnow()-1d
                          (aplicado ~2026-06-22, no relacionado con esta falla actual)
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
| 2026-09-14 | 5 (arroz/MIDA, prensa.com) | 39 | Diagnóstico: fetch de Actions falla 7 días seguidos (runner_id=0) |

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
