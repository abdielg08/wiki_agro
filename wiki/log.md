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

## 2026-08-05 00:00
INGEST (routine): lote de 5 pendientes revisado — 0 ingestados, 5 falsos positivos
  Causa raíz: colisión de la sigla "MIDA" — el filtro de GDELT capturó artículos
  que mencionan otras entidades llamadas "MIDA" que NO son el Ministerio de
  Desarrollo Agropecuario de Panamá:
    - "MIDA" = Malaysian Investment Development Authority (Malasia)
    - "MIDA" = Military Installation Development Authority (Utah, EE.UU.)
  Nota: los 5 artículos vienen etiquetados country=PA, language=es en su JSON
  fuente pese a ser en inglés y sobre Malasia/Utah — el filtro de país/idioma
  de la fuente no es confiable para estos casos; el chequeo de contenido caza
  el falso positivo antes de ingestar.
  Falsos positivos descartados (NO ingestados, NO se crea página wiki):
    1. "MITI working on simplified NCM customised incentive mechanism..." (paultan.org, 2026-07-08)
       → MIDA = Malaysian Investment Development Authority
    2. "Timeline: How the Kevin O'Leary data center plan came to be..." (sltrib.com, 2026-05-19)
       → MIDA = Military Installation Development Authority (Utah)
    3. "Box Elder data center opponents hope for a vote..." (sltrib.com, 2026-05-27)
       → MIDA = Military Installation Development Authority (Utah)
    4. "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com, 2026-05-29)
       → MIDA = Military Installation Development Authority (Utah)
    5. "Cultural Rules For Staying With Locals Abroad" (msn.com, 2026-03-07)
       → menciona la Military Installation Development Authority (Utah) de pasada
  Acción: los 5 se marcan `ingested: true` en processed.json (individualmente,
  ver nota de bug abajo) para sacarlos de la cola de pendientes (no se
  reintentan), pero no generan contenido de wiki. Tasa de falsos positivos de
  esta sesión: 5/5 (100% del lote), 0 páginas nuevas — cumple la regla de 0%
  falsos positivos ingestados al wiki.

  ⚠️ BUG DE HERRAMIENTAS ENCONTRADO Y CORREGIDO EN ESTA SESIÓN:
  1. `python wiki_agro.py mark-all-ingested --limit 5` NO usa el mismo orden
     que `ingest --limit 5`: `ingest` selecciona por score de relevancia
     (ver `prioritize.py`/`run_prepare`), mientras que `mark-all-ingested`
     usa `find_pending()` (orden alfabético de archivo). Al ejecutar
     mark-all-ingested tras revisar el lote de `ingest`, marcó como
     `ingested: true` 5 artículos DISTINTOS a los 5 revisados — ninguno de
     ellos había sido leído ni documentado (incluían un documento de IEEE,
     un catálogo de dípteros de archive.org y una nota económica de Aragón,
     España — claramente no agro-Panamá, pero sin revisión no debieron
     marcarse). Se detectó por `ingested_at` con timestamp de esta sesión
     no coincidiendo con las URLs reales revisadas.
     CORRECCIÓN: se revirtió `ingested: false` en los 4 artículos no
     revisados que quedaban mal marcados (el 5to coincidió por azar con el
     msn.com sí revisado) y se marcaron correctamente, uno por uno, los 4
     artículos realmente documentados como falsos positivos arriba.
     Los 4 artículos restaurados a `pending` (doc IEEE, catálogo archive.org
     dípteros São Paulo, nota Heraldo.es Aragón, sltrib.com nuclear-energy-state
     Utah) sí se revisaron más tarde en esta misma sesión — ver entradas
     siguientes.
  2. `python wiki_agro.py mark-ingested '<url>'` también falla con
     `AttributeError: 'list' object has no attribute 'get'` porque itera
     `processed.items()` sin filtrar la clave interna `_gdelt_windows`
     (que es una lista, no un dict). Se evitó el comando y se actualizó
     `processed.json` directamente con el mismo efecto (ingested=true +
     ingested_at) para los 4 artículos revisados.
  RECOMENDACIÓN: revisar/arreglar `scripts/ingest.py::mark_ingested` (usar
  `article_entries()` como ya hace `mark_all_ingested`) y decidir si
  `mark_all_ingested` debe usar la misma priorización que `ingest` en vez
  de `find_pending()` alfabético, para que ambos comandos operen siempre
  sobre el mismo lote.

## 2026-08-05 16:04
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-05 00:00 (continuación)
INGEST (routine): lote 2/3 revisado — 0 ingestados, 5 falsos positivos
  Falsos positivos descartados (NO ingestados, NO se crea página wiki):
    1. "Aragón celebra la sentencia del Supremo que tumba ampliación obligatoria
       del espacio por cerdo en las granjas" (heraldo.es, 2025-11-25) → Aragón, España
    2. "Utah wants to process uranium on the Wasatch Front..." (sltrib.com, 2025-06-13)
       → MIDA = Military Installation Development Authority (Utah), nada agro
    3. "New York Farm Bureau" (nyfb.org, 2026-06-17) → gremio agrícola de EE.UU.
    4. "Arvensis Agro amplía sus instalaciones..." (heraldo.es, 2026-06-23) → empresa aragonesa, España
    5. "'Reef Saudi', a Successful Program Based on Rain-Fed Agriculture" (spa.gov.sa, 2026-06-24)
       → programa agrícola de Arabia Saudita
  Los 5 vienen etiquetados country=PA, language=es en su JSON fuente pese a
  ser de España/EE.UU./Arabia Saudita — confirma el patrón sistémico (ver
  diagnóstico avanzado abajo).

## 2026-08-05 00:00 (continuación)
INGEST (routine): lote 3/3 revisado — 0 ingestados, 6 falsos positivos
  Falsos positivos descartados (NO ingestados, NO se crea página wiki):
    1. "Finep vai pagar R$ 220 milhões para inovações em agricultura familiar"
       (agenciabrasil.ebc.com.br, 2026-07-02) → Brasil
    2. "The Persian Qanat" (whc.unesco.org, 2026-07-07) → sitio UNESCO, Irán
    3. "AEGA pide elecciones al campo en Aragón..." (heraldo.es, 2026-06-08) → Aragón, España
    4. "Luis Biendicho asume la consejería de Medio Ambiente..." (heraldo.es, 2026-05-03) → Aragón, España
    5. "Ambient IoT: Communications Enabling Precision Agriculture" (ieeexplore.ieee.org,
       2025-03-31) → paper académico 6G, sin país específico
    6. "Catalogue of the diptera of the Americas South of United States" (archive.org,
       2016-05-13) → catálogo zoológico, Secretaria da Agricultura de São Paulo, Brasil
  Con este lote, los 16 pendientes originales de la sesión quedaron 100%
  revisados: 16/16 falsos positivos, 0 páginas nuevas de wiki. Todos marcados
  `ingested: true` en processed.json (uno por uno, evitando el bug de
  mark-all-ingested/mark-ingested documentado arriba) para sacarlos de la cola.
  `python wiki_agro.py stats` → Pendientes de ingesta: 0.

## 2026-08-05 00:00 (diagnóstico avanzado)
DIAGNÓSTICO: causa raíz sistémica de la tasa de falsos positivos 100% (16/16) de esta sesión
  Los 16 artículos pendientes revisados hoy eran, sin excepción, de fuentes
  internacionales sin relación con Panamá: España (Aragón, 4×), EE.UU./Utah
  (5×, colisión de sigla "MIDA"), Malasia (1×), Brasil (2×), Arabia Saudita
  (1×), Irán/UNESCO (1×), un paper académico IEEE sin país (1×), y un
  artículo genérico de EE.UU. (New York Farm Bureau, 1×).
  Causa raíz identificada en `scripts/fetch_historical.py`:
    - La query GDELT combina keywords genéricos de agro
      ("agropecuario OR agricultura OR ganaderia OR MIDA OR IDIAP OR cosecha
      OR cultivo OR arroz OR maiz OR platano OR ganadero") con el filtro
      `sourcecountry:PA` (línea ~73), pero el filtro NO está restringiendo
      los resultados a fuentes panameñas — GDELT está devolviendo artículos
      de medios españoles, saudíes, brasileños y estadounidenses.
    - Además, el código etiqueta cada resultado con `"language": "es",
      "country": "PA"` de forma FIJA (línea ~103), sin verificar el
      contenido real — por eso todos estos falsos positivos aparecen en
      `sources/articles/*.json` marcados como country=PA/language=es aunque
      sean en inglés/portugués y de otros países.
    - La palabra "MIDA" en la query es especialmente problemática: colisiona
      con "Malaysian Investment Development Authority" y con la "Military
      Installation Development Authority" de Utah, generando falsos
      positivos recurrentes.
  Impacto: el chequeo de contenido de esta sesión evitó que estos 16
  artículos contaminaran el wiki (0% falsos positivos ingestados — regla
  cumplida), pero cada sesión de rutina futura seguirá gastando ciclos
  revisando y descartando el mismo tipo de ruido mientras no se corrija el
  fetcher.
  RECOMENDACIÓN (no aplicada en esta sesión — cambio de código fuera del
  alcance de la rutina de ingesta): en `fetch_gdelt_window()`
  (scripts/fetch_historical.py) validar `sourcecountry` real del artículo
  devuelto por GDELT en vez de asumir PA, y/o retirar "MIDA" de la query
  genérica y usarlo solo combinado con términos agro-específicos, y/o subir
  el `trust_level`/país real solo tras confirmar el dominio contra una
  lista de medios panameños conocidos.
