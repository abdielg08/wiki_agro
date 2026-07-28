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

## 2026-07-28 00:07
ROUTINE: 9 artículos revisados — 9 falsos positivos (0 ingestados al wiki)
  Ningún artículo mencionaba "Panamá" ni una sola vez (verificado con grep).
  Falsos positivos documentados (NO ingestados, marcados como procesados para
  vaciar la cola de pendientes):
    1. paultan.org — "MITI working on simplified NCM..." → MITI/MIDA de Malasia
       (Ministry of Investment, Trade and Industry; MIDA = Malaysian Investment
       Development Authority), no Panamá.
    2. sltrib.com — "Box Elder data center opponents..." → MIDA = Military
       Installation Development Authority de Utah, EE.UU.
    3. sltrib.com — "Utah Gov. Cox issues order to protect Great Salt Lake..."
       → mismo MIDA de Utah.
    4. sltrib.com — "Utah wants to process uranium..." → mismo MIDA de Utah.
    5. nyfb.org — "New York Farm Bureau" → agricultura de Nueva York, EE.UU.
    6. spa.gov.sa — "'Reef Saudi'..." → programa agrícola de Arabia Saudita.
    7. whc.unesco.org — "The Persian Qanat" → sistema de riego histórico de Irán.
    8. ieeexplore.ieee.org — "Ambient IoT: ... Precision Agriculture" → paper
       técnico 6G/IoT sin referencia geográfica a Panamá.
    9. archive.org — "Catalogue of the diptera of the Americas South of United
       States" → catálogo entomológico brasileño de 1966/1967.

  DIAGNÓSTICO DE CAUSA RAÍZ: los 9 quedaron mal etiquetados con
  source="prensa.com", country="PA", trust_level=3 e ingresaron a la cola de
  ingesta porque:
  (a) `config/sources.yaml` → `web_searches: prensa_agro` usa una búsqueda
      DuckDuckGo `site:prensa.com` cuyo operador `site:` DDG no siempre
      respeta — los resultados de dominios no relacionados se cuelan y
      `scripts/fetch_news.py::fetch_ddg_search` los guardaba igual con los
      metadatos de la fuente configurada (bug real, no solo config).
  (b) "MIDA" está en `search_terms.primary` como acrónimo suelto — coincide
      con cualquier "MIDA" del mundo (Malasia, Utah) sin exigir contexto de
      Panamá, y `is_agro_relevant()` solo hace substring-match sin
      contexto geográfico.

  FIX APLICADO (scripts/fetch_news.py): `fetch_ddg_search()` ahora valida que
  el dominio real de la URL devuelta coincida con el `site` configurado (o un
  subdominio) antes de aceptar el resultado — descarta la fuga del operador
  `site:` de DDG en la raíz. Aplica a los 8 `web_searches` configurados.

  BUG ADICIONAL encontrado y corregido en `scripts/ingest.py`:
  - `mark_ingested()` (singular) crasheaba con AttributeError porque
    `sources/processed.json` tiene la clave interna `_gdelt_windows` (una
    lista, no un dict) y el loop llamaba `.get()` sobre ella sin chequear
    tipo. Fix: se agregó `isinstance(meta, dict)` antes de acceder.
  - `mark_all_ingested()` (`mark-all-ingested --limit N`) recalculaba de
    forma independiente los N artículos pendientes usando orden de archivo
    (glob por path), mientras que `ingest --limit N` selecciona por SCORE de
    relevancia (`prioritize.py`) — dos criterios de orden distintos. Esto
    causó que la primera corrida de esta sesión marcara como "ingestados"
    3 artículos que NUNCA fueron mostrados ni revisados (uranio en Utah,
    paper IEEE de agricultura de precisión, catálogo de dípteros de 1966),
    dejándolos permanentemente fuera de la cola sin haber sido procesados
    — una violación directa de la regla de "sin backlog sin procesar".
    Detectado, revertido (`ingested: false` restaurado) y corregido: ahora
    `mark_all_ingested()` lee las URLs exactas del bloque de comandos al
    final de `pending_ingest.md` (el que sí refleja lo que Claude Code
    revisó) en lugar de recalcular la selección desde cero.

  Acción: cola de pendientes vaciada a 0 sin ingestar ningún falso positivo
  al wiki. Recomendado a el usuario: revisar y fusionar el fix de
  `fetch_ddg_search`/`ingest.py` para reducir falsos positivos futuros.
  Fuentes con cobertura: MIDA (2), TVNNoticias (1), LaPrensaEco (1), BDA (1), IICA (1)

## 2026-07-28 00:04
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-28 00:07
INGEST: 9 artículos marcados como ingestados por sesión Claude Code
