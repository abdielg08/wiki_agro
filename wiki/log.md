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

## 2026-08-01 00:00
FALSOS POSITIVOS: 16/16 artículos pendientes descartados — 0 ingestados

Se ejecutó `ingest --limit 5` sobre la cola de 16 pendientes. Los 5 artículos
devueltos NO eran sobre agro panameño (ninguno mencionaba "Panamá"/"Panamá"
en su texto, pese a estar todos etiquetados `country: "PA"`):

  1. "MITI working on simplified NCM..." → paultan.org — incentivos
     industriales de Malasia (MITI/MIDA malayo = Malaysian Industrial
     Development Authority, colisión de siglas con MIDA-Panamá).
  2. "Timeline: Kevin O'Leary data center..." → sltrib.com — centro de
     datos en Utah (MIDA = Military Installation Development Authority
     de Utah, no Ministerio de Desarrollo Agropecuario).
  3. "Box Elder data center opponents..." → sltrib.com — mismo caso Utah.
  4. "Utah Gov. Cox issues order..." → sltrib.com — mismo caso Utah.
  5. "Cultural Rules For Staying With Locals Abroad" → msn.com — artículo
     de viajes que menciona de paso la demanda contra MIDA-Utah.

Ninguno se ingestó al wiki. Se marcaron como `ingested: true` en
`processed.json` vía `mark-all-ingested` (documentados aquí, no omitidos).

**Diagnóstico ampliado**: se inspeccionaron los 16 pendientes en la cola
completa (no solo los 5 servidos) y los 16 resultaron ser falsos positivos
del mismo origen — ninguno menciona "Panamá" en su texto:
  - 4 sobre MIDA-Utah/MIDA-Malasia (colisión de siglas, ver arriba)
  - "Reef Saudi" (agricultura de secano en Arabia Saudita)
  - "New York Farm Bureau" (EE.UU.)
  - "Utah wants to process uranium..." (energía nuclear, Utah)
  - "The Persian Qanat" (patrimonio UNESCO, Irán)
  - "Ambient IoT: Communications Enabling Precision Agriculture" (paper
    IEEE genérico, sin mención geográfica)
  - "Catalogue of the diptera of the Americas..." (catálogo entomológico
    histórico, Brasil/Sudamérica en general)
  - 3 artículos de heraldo.es sobre agricultura/política en Aragón, España
  - "Finep vai pagar R$ 220 milhões..." (agricultura familiar, Brasil)
  - "Arvensis Agro amplía sus instalaciones..." (España)

Los 16 se marcaron `ingested: true` para vaciar la cola (todos documentados
arriba, ninguno omitido silenciosamente). No se ingestó ni una sola página
de wiki en esta sesión: tasa de falsos positivos de la cola = 100%,
ingesta real = 0/16, manteniendo la tasa de falsos positivos **del wiki**
en 0% (regla innegociable).

**Causa raíz identificada y corregida**: los 16 provenían todos de la
fuente `ddg_search: prensa.com` (búsqueda DuckDuckGo News en
`config/sources.yaml`, query `"agropecuario OR agricultura OR ganadería
OR MIDA OR cosecha Panamá"`). A diferencia de `fetch_rss()` y
`fetch_gdelt_batch()` (que ya aplican `_is_blocked_domain()` y
`_is_panama_related()` antes de aceptar un artículo — ver comentario
existente en el código: "MIDA matches Malaysia too"), la función
`fetch_ddg_search()` en `scripts/fetch_news.py` carecía de ambos filtros:
solo llamaba a `is_agro_relevant()`, que acepta cualquier texto que
contenga términos genéricos como "agricultura" o "MIDA" sin exigir
mención de Panamá. Además, el operador `site:prensa.com` de DDGS no
está siendo respetado por el backend de búsqueda, devolviendo resultados
de dominios arbitrarios (sltrib.com, heraldo.es, paultan.org, etc.) que
luego se etiquetan igual con `country: "PA"` de forma ciega.

**Fix aplicado**: se agregaron las mismas dos verificaciones que ya usan
`fetch_rss()`/`fetch_gdelt_batch()` a `fetch_ddg_search()` en
`scripts/fetch_news.py` (rechazar dominios bloqueados vía
`_is_blocked_domain()`, exigir término panameño en título/URL vía
`_is_panama_related()`). Cambio puramente restrictivo — no puede
introducir falsos positivos nuevos, solo elimina los que ya colaban.
Commit incluido en esta sesión.

**Nota para el usuario**: la fuente de búsqueda `prensa.com` (DDG search)
ha estado produciendo 100% de basura no relacionada con Panamá al menos
en este último lote de 16 artículos. Con el fix, se espera que deje de
traer estos casos, pero conviene revisar el rendimiento de esta fuente en
las próximas 2-3 sesiones de routine para confirmar.

## 2026-08-01 00:05
INGEST: 16 artículos marcados como ingestados por sesión Claude Code
