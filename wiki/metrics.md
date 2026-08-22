---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-22
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 30 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 24 | **0 nuevos** ⚠️ ver diagnóstico |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 72 / ~45 estimadas | 45 (2015→hoy) |
| Días sin artículos nuevos | 1 | máx 3 antes de diagnosticar |
| Pendientes de ingesta | 0 | 0 |

---

## ⚠️ Diagnóstico crítico (2026-08-22) — Fetch trae 100% ruido

**Los 24 falsos positivos acumulados representan el 100% de los artículos**
**bajo fuente "prensa.com"** (24/24). El fetch etiqueta como "prensa.com"
resultados que en realidad vienen de dominios sin relación con Panamá ni con
La Prensa: sltrib.com, heraldo.es (España), spa.gov.sa, maine.gov,
agenciabrasil.com.br, whc.unesco.org, ieeexplore.ieee.org, archive.org,
paultan.org, msn.com, nyfb.org. Parece un fetch por palabra clave genérica
("MIDA", "agriculture") sin filtro geográfico de Panamá ni verificación del
dominio real de origen. Ver `wiki/log.md` (entrada 2026-08-22 00:45) para el
detalle artículo por artículo y la recomendación de fix (restringir a
dominios .pa / medios de CLAUDE.md, exigir co-ocurrencia con "Panamá",
corregir la atribución de "source").

Las 6 fuentes no-"prensa.com" (MIDA, TVNNoticias, LaPrensaEco, BDA, IICA) son
el 100% del contenido real ingestado hasta ahora — siguen siendo confiables.

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-21 11:24 UTC
Resultado               : 0 artículos nuevos (pero SÍ corrió — no está caído)
Ventanas GDELT          : 72 completadas, por encima del estimado de 45 →
                          el backfill temporal ya cubrió gran parte del rango,
                          pero sin filtro geográfico sigue trayendo ruido global
Causa identificada       : el fetch por palabra clave no distingue MIDA Panamá
                          de MIDA Malasia/Utah, ni exige que el artículo
                          mencione Panamá — ver diagnóstico arriba
Estado post-fix anterior : el fix de rango de fechas (2026-06-22) funcionó (ya
                          no hay ventanas futuras/timeout), pero no resolvió
                          el problema de precisión geográfica
Próximo paso             : corregir el filtro de relevancia geográfica en el
                          fetcher antes de seguir expandiendo el backfill
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos reales | Estado |
|---------|----------|-----------|--------|
| 2015 | 0/4 | 0 | **Pendiente — hueco de cobertura** |
| 2016 | 0/4 | 0 | **Pendiente — hueco de cobertura** |
| 2017 | 4/4 | 0 | Cubierto, sin artículos reales |
| 2018 | 4/4 | 0 | Cubierto, sin artículos reales |
| 2019 | 4/4 | 0 | Cubierto, sin artículos reales |
| 2020 | 4/4 | 0 | Cubierto, sin artículos reales |
| 2021 | 4/4 | 0 | Cubierto, sin artículos reales |
| 2022 | 4/4 | 0 | Cubierto, sin artículos reales |
| 2023 | 4/4 | 0 | Cubierto, sin artículos reales |
| 2024 | 4/4 | 0 | Cubierto, sin artículos reales |
| 2025 | 4/4 | 0 | Cubierto, sin artículos reales |
| 2026 | 36 (rolling) | 0 | Cubierto, sin artículos reales |
| **TOTAL** | **72** | **0** | **Backfill cubre 2017-2026; faltan 2015-2016; 0 artículos reales via GDELT** |

> Conteo real derivado de `sources/processed.json._gdelt_windows` (2026-08-22).
> Los 6 artículos reales del wiki vienen todos del lote semilla manual
> (2026-05-24), no del fetch GDELT/RSS automático — el fetch automático aún
> no ha producido ni un solo artículo real de agro panameño. Prioridad:
> arreglar precisión antes de cerrar el hueco 2015-2016.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-22 | 0 reales / 17 revisados | 0 | 17/17 falsos positivos (100%) — ver diagnóstico arriba. Fix de bug en `mark-ingested`/`mark-all-ingested`. |

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
