---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-16
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 39 (⚠️ 17 identificados como falsos positivos, ver abajo) | 0 |
| Falsos positivos acumulados (detectados, no ingestados) | 7 (previos) + 17 (nuevos, 2026-09-16) = 24 | **0 nuevos ingestados** |
| Páginas en wiki/ | 28 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 / ~45 estimadas | 45 (2015→hoy) — **umbral superado, rango agotado** |
| Días sin artículos nuevos en sources/ | **10 días** (última corrida exitosa: 2026-09-06) | máx 3 antes de diagnosticar — **UMBRAL EXCEDIDO** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions (histórico) : 2026-06-21 — 0 artículos, fix de ventanas GDELT aplicado
Última corrida EXITOSA             : 2026-09-06 (run #103, "0 artículos nuevos")
Corridas fallidas consecutivas     : 9 (run #104 → #112, 2026-09-07 → 2026-09-15)
Resultado                          : 0 artículos nuevos desde hace 10 días — FALLA CRÍTICA
Causa identificada                 : NO CONFIRMADA — logs de Actions bloqueados por el proxy
                                      de red de este entorno de ejecución (no se pudieron bajar)
Evidencia                          : runs #104-#111 fallan en 4-7s (fallo temprano: checkout,
                                      permisos o cuota Actions); run #112 falla en ~33s (posible
                                      fallo en `pip install -r requirements.txt`, deps sin pin
                                      de versión exacta — todas usan `>=`)
                                      Mismo head_sha (24cfc3c) en runs #104-#111 → ningún commit
                                      nuevo llegó a sources/ en 9 corridas
                                      Sin cambios recientes en .github/workflows/,
                                      requirements.txt ni scripts/fetch_*.py que expliquen
                                      el inicio de la falla el 2026-09-07
Acción requerida                   : revisar logs en
                                      https://github.com/abdielg08/wiki_agro/actions/runs/34987787411
                                      y re-disparar workflow_dispatch tras corregir la causa
Estado post-diagnóstico            : Pendiente de corrección manual (fuera del alcance de
                                      esta sesión — sin acceso a logs de Actions)
```

## Falsos Positivos Detectados en Cola de Pendientes (2026-09-16)

```
17 de 39 artículos pendientes (44%) provienen de dominios sin relación con Panamá,
mal etiquetados como source=prensa.com / country=PA:
  - sltrib.com (Utah, EE.UU.)                                        — 4 artículos
  - heraldo.es (Aragón, España)                                      — 3 artículos
  - thestar.com.my / paultan.org (Malasia, "MIDA" ≠ MIDA panameño)   — 3 artículos
  - fox13now.com (Utah, "MIDA" ≠ MIDA panameño)                      — 1 artículo
  - ieeexplore.ieee.org, spa.gov.sa, agenciabrasil.ebc.com.br,
    whc.unesco.org, maine.gov, clubofmozambique.com, nyfb.org, msn.com — 6 artículos
Ninguno fue ingestado. Ver wiki/log.md (2026-09-16 00:05) para el detalle completo.
Causa probable: búsqueda por palabra clave sin filtro de dominio (allowlist) en el fetch.
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
| 2026-09-16 | 5 | 39 (17 sospechosos de falso positivo, no ingestados) | Fetch diario roto 9 corridas seguidas (#104-#112); 17 falsos positivos detectados en cola |

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
