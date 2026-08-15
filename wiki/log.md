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

## 2026-08-15 09:00
ROUTINE: 16 artículos revisados — 16 falsos positivos, 0 ingestados (0% tasa de aceptación)
  Se procesó TODA la cola de pendientes (3 lotes de `ingest --limit`), no solo 5, porque
  se detectó que el 100% del backlog restante compartía la misma causa raíz (ver abajo)
  y dejarlo pendiente habría bloqueado las próximas 3 routines/día indefinidamente.

  Ninguno de los 16 trata sobre agro panameño:
    - paultan.org/.../miti-working-on-simplified-ncm-... → MITI/MIDA de Malasia (incentivos industriales)
    - sltrib.com/.../kevin-oleary-data-center-timeline → MIDA = Military Installation Development Authority (Utah)
    - sltrib.com/.../box-elder-data-center-opponents → ídem, oposición a centro de datos en Utah
    - sltrib.com/.../utah-governor-issues-order-protect → ídem, orden del gobernador de Utah
    - sltrib.com/.../utah-nuclear-energy-state → ídem, MIDA de Utah y energía nuclear
    - msn.com/.../cultural-rules-for-staying-with-locals-abroad → viajes, menciona de pasada demanda contra MIDA de Utah
    - heraldo.es/.../aragon-celebra-sentencia-supremo... → política agraria de Aragón, España
    - heraldo.es/.../aega-pide-elecciones-campo-aragon... → ídem, Aragón, España
    - heraldo.es/.../luis-biendicho-vox-asume-consejeria... → ídem, Aragón, España (caso Forestalia)
    - heraldo.es/.../arvensis-agro-amplia-sus-instalaciones... → empresa agro aragonesa, España
    - spa.gov.sa/en/N2096157 → programa "Reef Saudi", Arabia Saudita
    - agenciabrasil.ebc.com.br/.../finep-vai-pagar... → financiamiento agrícola en Brasil
    - whc.unesco.org/en/list/1506 → sitio Patrimonio Mundial "The Persian Qanat" (Irán)
    - nyfb.org → New York Farm Bureau, EE.UU.
    - ieeexplore.ieee.org/document/10945742 → paper IEEE sobre IoT y agricultura de precisión (genérico)
    - archive.org/.../Cataloguedipter2SaoP → catálogo entomológico, sin relación con Panamá
  No se creó contenido en wiki/ para ninguno (regla: falso positivo → NO ingestar).

  CAUSA RAÍZ identificada: `fetch_ddg_search()` en scripts/fetch_news.py NO aplicaba
    `_is_blocked_domain()` ni verificaba que el dominio del resultado coincidiera con el
    `site:` solicitado (a diferencia de `fetch_rss()`, que sí lo hace). El operador `site:`
    de DDGS no se respeta de forma confiable, así que la búsqueda `prensa_agro`
    (query genérica "agropecuario OR agricultura OR ganadería OR MIDA OR cosecha")
    devolvió noticias globales de agricultura de cualquier país, etiquetadas
    incorrectamente como `source: prensa.com, country: PA` por defecto (23/29 artículos
    descargados en total tenían esta etiqueta falsa). Este es el mismo patrón de falso
    positivo ya documentado el 2026-06-22 (7 falsos positivos) — la causa no se había
    corregido en el código entonces, solo se habían marcado manualmente los artículos.
  BUG adicional encontrado y corregido: `mark_ingested()` en scripts/ingest.py iteraba
    `processed.items()` crudo en lugar de `article_entries(processed)`, lo que causaba
    un `AttributeError` al toparse con la clave interna `_gdelt_windows` (una lista).
  FIX aplicado:
    1. `fetch_ddg_search()` ahora rechaza resultados cuyo dominio real no contenga el
       `site` configurado, y aplica `_is_blocked_domain()` como en `fetch_rss()`.
       Archivo: scripts/fetch_news.py.
    2. `mark_ingested()` ahora usa `article_entries()` para excluir claves internas.
       Archivo: scripts/ingest.py.
  Artículos marcados como revisados (ingested=true) para vaciar la cola de pendientes:
    ver processed.json — las 16 URLs anteriores.
  Resultado: Pendientes de ingesta = 0 (antes: 16). Artículos reales ingestados
    sin cambio (6). Falsos positivos acumulados: 7 → 23.
