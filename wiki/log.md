---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2025-05-24
---

# Log de Actividad

> Registro cronológico append-only de ingestas, consultas y operaciones de mantenimiento.

---

## 2025-05-24 00:00
INIT: Wiki Agropecuario de Panamá inicializado
  Estructura: topics/, entities/, summaries/, index.md, log.md
  Metodología: Karpathy LLM Wiki (3 capas: sources → wiki → schema)
  Cobertura objetivo: noticias agropecuarias de Panamá 2015–2025
  Fuentes configuradas: MIDA, IDIAP, BDA, IICA, FAO, La Prensa, Panamá América, TVN, La Estrella
  Método histórico: GDELT API (gratuito, sin clave, cobertura 2015–2025)

## 2026-05-24 13:38
LINT: 8 páginas revisadas, 39 issues encontrados
  frontmatter:0, huérfanas:0, broken_links:39, stale:0, no_index:0

## 2026-05-24 15:04
LINT: 8 páginas revisadas, 39 issues encontrados
  frontmatter:0, huérfanas:0, broken_links:39, stale:0, no_index:0

## 2026-05-24 16:00
INGEST: 6 artículos semilla procesados (sesión Claude Code — metodología Karpathy)
  Artículos:
    - 20230915_mida_produccion-arroz-panama-2023 → summaries/ + topics/arroz.md actualizado
    - 20180620_laprensaeco_gusano-cogollero-crisis-maiz-2018 → summaries/ + topics/maiz.md creado + topics/plagas_enfermedades.md actualizado
    - 20160301_tvnnoticias_sequia-azuero-nino-2015-2016 → summaries/ + topics/cambio_climatico.md actualizado
    - 20220410_iica_platano-banano-exportaciones-fusarium → summaries/ + topics/platano_banano.md actualizado + topics/plagas_enfermedades.md actualizado
    - 20210815_bda_credito-agropecuario-pandemia-2020-2021 → summaries/ + topics/credito_financiamiento.md creado + entities/bda.md actualizado
    - 20240305_mida_politica-agropecuaria-mulino-2024 → summaries/ + topics/politicas_agropecuarias.md creado + entities/mida.md actualizado
  Páginas creadas: maiz.md, credito_financiamiento.md, politicas_agropecuarias.md
  Páginas actualizadas: arroz.md, plagas_enfermedades.md, cambio_climatico.md, platano_banano.md, mida.md, bda.md
  Summaries: 6 nuevos archivos en wiki/summaries/

## 2026-05-24 22:58
INGEST: 6 artículos marcados como ingestados por sesión Claude Code

## 2026-05-27 00:00
MAINTENANCE: Verificación automática de artículos pendientes
  Sin artículos pendientes — 6/6 artículos ya ingestados
  Total páginas wiki: 19 (8 topics, 3 entities, 6 summaries, 2 overview)
  Fuentes con cobertura: MIDA (2), TVNNoticias (1), LaPrensaEco (1), BDA (1), IICA (1)

## 2026-08-17 08:32
ROUTINE: Sesión de ingesta — 16 pendientes revisados, 0 ingestados (16 falsos positivos, 0% tolerado)

  **Falsos positivos detectados (16/16 — todo lo pendiente esta sesión)**:
  Ninguno de los 16 artículos pendientes trataba sobre agro panameño. El patrón dominante:
  coincidencia de la palabra clave "MIDA" con otras entidades homónimas (Utah Military
  Installation Development Authority, Malaysian Investment Development Authority) más
  ruido genérico de agricultura mundial sin ningún vínculo con Panamá.

  1. "MITI working on simplified NCM..." (paultan.org) — MIDA = agencia de inversión de Malasia
  2. "Timeline: Kevin O'Leary data center..." (sltrib.com) — MIDA = autoridad de Utah (data centers)
  3. "Box Elder data center opponents..." (sltrib.com) — ídem, MIDA de Utah
  4. "Utah Gov. Cox issues order..." (sltrib.com) — ídem, MIDA de Utah
  5. "Cultural Rules For Staying With Locals Abroad" (msn.com) — mención lateral de demanda contra MIDA (Utah)
  6. "Utah wants to process uranium..." (sltrib.com) — MIDA de Utah, energía nuclear
  7. "Ambient IoT: Communications Enabling Precision Agriculture" (ieeexplore.ieee.org) — paper genérico 6G/IoT, sin mención de Panamá
  8. "Catalogue of the diptera of the Americas South of United States" (archive.org) — catálogo entomológico histórico, sin relación agro-Panamá
  9. "Aragón celebra sentencia del Supremo... espacio cerdo granjas" (heraldo.es) — porcicultura en Aragón, España
  10. "'Reef Saudi', a Successful Program Based on Rain-Fed Agriculture" (spa.gov.sa) — programa agrícola de Arabia Saudita
  11. "Finep vai pagar R$ 220 milhões para inovações em agricultura familiar" (agenciabrasil.ebc.com.br) — Brasil
  12. "The Persian Qanat" (whc.unesco.org) — sitio Patrimonio UNESCO, Irán
  13. "AEGA pide elecciones al campo en Aragón..." (heraldo.es) — España
  14. "New York Farm Bureau" (nyfb.org) — EE.UU.
  15. "Arvensis Agro amplía sus instalaciones..." (heraldo.es) — Aragón, España
  16. "Luis Biendicho asume la consejería de Medio Ambiente..." (heraldo.es) — Aragón, España

  Los 16 se marcaron `ingested: true` en `processed.json` (sin crear páginas de wiki) para
  que no vuelvan a aparecer en la cola. Cero páginas de wiki creadas o modificadas esta sesión.

  **BUG DE SOFTWARE ENCONTRADO Y CORREGIDO** — `mark-all-ingested` marcaba el lote equivocado:
  `mark_all_ingested()` en `scripts/ingest.py` recalculaba "los siguientes N pendientes" con
  `find_pending()` (orden alfabético por nombre de archivo), mientras que `ingest` selecciona
  el lote a revisar con `prioritize()` (orden por score de relevancia). Con más de una página
  de pendientes, ambos órdenes difieren, así que el primer `mark-all-ingested --limit 5` de
  esta sesión marcó como ingestados 5 artículos que el LLM **nunca revisó** (distintos a los
  5 mostrados en `pending_ingest.md`): uranio en Utah, un paper IEEE de IoT, un catálogo de
  dípteros de 1916, una nota de porcicultura en Aragón y (por coincidencia) el mismo artículo
  de "Cultural Rules" ya revisado. Los 5 resultaron ser falsos positivos también al revisarlos
  retroactivamente (documentados arriba, items 6–9), pero el bug es serio: en cualquier otra
  sesión pudo haber marcado como "ingestado" un artículo real sobre agro panameño sin que
  el LLM lo viera nunca, causando pérdida silenciosa de datos y violando la garantía de
  0% falsos positivos (que depende de que TODO pendiente sea revisado antes de marcarse).
  **Fix aplicado**: `mark_all_ingested()` ahora lee las URLs exactas del bloque
  `mark-ingested` al final de `pending_ingest.md` (el lote que realmente se mostró para
  revisión) en vez de recalcular una selección nueva. Archivo: `scripts/ingest.py`.

  **Diagnóstico de causa raíz (por qué la cola está contaminada)**:
  `scripts/prioritize.py::score_article()` incluye "MIDA" en `HIGH_PRIORITY_TERMS` como
  substring sin verificar que el artículo sea sobre Panamá — cualquier "MIDA" (Utah,
  Malasia, etc.) sube el score. Además, los artículos guardados vía GDELT/DDG llevan
  `country: "PA"` y `language: "es"` fijos en el código de guardado (`fetch_news.py`),
  independientemente del contenido real (varios de estos 16 están en inglés o portugués).
  Esto sugiere que el filtro `is_panama_related`/`is_agro_relevant` no se está aplicando
  de forma efectiva para el modo de búsqueda que originó estos artículos. No se modificó
  este código en esta sesión (requiere revisión más profunda del pipeline de fetch) —
  se deja documentado para una sesión dedicada a fetch/filtrado.

  **Diagnóstico avanzado (Pendientes = 0 tras esta sesión)**:
  - Últimos 3 commits en `sources/` (2026-08-14, 15, 16): "0 artículos nuevos descargados"
    cada día — GitHub Actions corre (cron diario 6am Panamá) pero no trae nada nuevo.
  - Racha real: 0 artículos nuevos desde 2026-07-31 (18 días), con la excepción de
    2026-08-... revisar el historial completo de commits para confirmar.
  - `_gdelt_windows` en `processed.json`: 69 ventanas completadas. Cubren 2017–2026
    completo (4/año) MÁS 33 ventanas de un solo día en 2026 (un patrón de "cola móvil":
    cada corrida diaria agrega una ventana nueva porque el fin de rango es
    `ayer`, que avanza un día por corrida).
  - **Faltan las 8 ventanas de 2015 y 2016** (2015 Q1–Q4, 2016 Q1–Q4) — nunca aparecen
    como completadas pese a ser las primeras en el orden de iteración. El código
    (`fetch_gdelt_historical` en `fetch_news.py`) solo marca una ventana como completa
    tras una respuesta HTTP exitosa; en error de red la reintenta en la próxima corrida
    SIN marcarla. El patrón observado (siempre faltan las mismas 8, nunca avanzan) es
    consistente con que esas 8 ventanas fallan sistemáticamente en cada corrida.
    No se pudo probar el endpoint de GDELT directamente desde este sandbox (el proxy
    de salida bloquea `api.gdeltproject.org` con 403 — ver `.github/workflows/*.yml`,
    que indica que GDELT sí funciona desde IPs de GitHub Actions), así que esto queda
    como hipótesis a confirmar revisando el log de la próxima corrida de Actions.
  - Cobertura real actual: 2017–2026, NO 2015–hoy como indica la meta de `CLAUDE.md`.
  - Conclusión: `Pendientes > 0` no es el problema ahora mismo (quedó en 0), pero el
    *flujo de entrada* está efectivamente detenido — 18 días sin artículos nuevos
    reales, y cuando llegan, son en su mayoría ruido global sin relación con Panamá
    (ver bug de scoring arriba). Se recomienda una sesión dedicada a: (1) revisar por
    qué las ventanas 2015–2016 nunca completan, (2) acotar el filtro de relevancia
    para exigir mención explícita de Panamá/región panameña, no solo términos genéricos
    de agricultura o el acrónimo "MIDA".

## 2026-08-17 08:29
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-17 08:31
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-17 08:32
INGEST: 6 artículos marcados como ingestados por sesión Claude Code
