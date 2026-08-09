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

## 2026-08-09 00:00
FALSOS POSITIVOS: 5/5 artículos del batch descartados — NO ingestados
  Causa raíz: colisión de sigla "MIDA" — el scraper/GDELT capturó noticias
  de otras entidades llamadas MIDA que no son el Ministerio de Desarrollo
  Agropecuario de Panamá:
    - 20260708_prensacom_...miti-working-on-simplified-ncm... → MIDA =
      Malaysian Investment Development Authority (Malasia, incentivos
      industriales). No relacionado con Panamá ni agro.
    - 20260519_prensacom_...kevin-oleary-data-center-timeline... → MIDA =
      Military Installation Development Authority (Utah, EE.UU.), plan de
      centro de datos de Kevin O'Leary. No agro, no Panamá.
    - 20260527_prensacom_...box-elder-data-center-opponents... → mismo caso,
      oposición al centro de datos de MIDA en Box Elder, Utah.
    - 20260529_prensacom_...utah-governor-issues-order-prote... → mismo caso,
      orden del gobernador de Utah sobre centros de datos y MIDA.
    - 20260307_prensacom_...cultural-rules-for-staying-with-locals-abro... →
      artículo de estilo de vida/viajes que menciona de pasada la demanda
      contra MIDA (Utah). Sin relación con agro panameño.
  Acción: NO se crearon páginas de wiki. Los 5 artículos se marcarán como
  ingestados (mark-all-ingested) para no reprocesarlos, pero quedan
  registrados aquí como falsos positivos, no como contenido del wiki.
  Nota para el pipeline de fetch: el filtro de keywords/GDELT debería
  excluir resultados donde "MIDA" no coincide con contexto panameño
  (country != PA en metadata real, o ausencia de términos agro) — ver
  diagnóstico en próxima sesión si el patrón se repite.

## 2026-08-09 16:03
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-09 16:20
BUG ENCONTRADO Y CORREGIDO: `mark-all-ingested` no marcaba los mismos
artículos que `ingest` había mostrado.
  Causa: `ingest`/`run_prepare` ordena los pendientes por score de
  relevancia (`prioritize()`), pero `mark_all_ingested` tomaba los
  primeros N pendientes por orden de archivo — listas distintas. Resultado:
  4 de 5 artículos ya procesados (o descartados como falso positivo)
  reaparecían en el siguiente batch.
  Fix: `scripts/ingest.py::mark_all_ingested` ahora usa `prioritize()` con
  la misma estrategia ("score") que `run_prepare`, garantizando que marca
  exactamente los artículos que se mostraron.
  Bug adicional: `mark_ingested()` iteraba `processed.items()` sin excluir
  la clave interna `_gdelt_windows` (una lista), causando `AttributeError`
  al llamar `meta.get()`. Fix: usa `article_entries(processed)` (ya
  disponible en `core.py`) para filtrar claves internas.

## 2026-08-09 16:20
FALSOS POSITIVOS: 7/7 artículos restantes del backlog descartados — NO
ingestados. Ninguno es sobre agro/Panamá:
  - heraldo.es (x3): noticias de Aragón, España — política ambiental
    (Inaga/Forestalia), elecciones al campo aragonés, y Arvensis Agro
    (empresa española de nutrición vegetal). Nada relacionado con Panamá.
  - nyfb.org: New York Farm Bureau (EE.UU.)
  - spa.gov.sa: programa "Reef Saudi" de agricultura de secano (Arabia
    Saudita)
  - agenciabrasil.ebc.com.br: financiamiento Finep para agricultura
    familiar (Brasil)
  - whc.unesco.org: sitio Patrimonio Mundial del Qanat persa (Irán)
  Acción: NO se crearon páginas de wiki. Se marcan como ingestados para
  vaciar la cola, quedando registrados aquí como falsos positivos.

## 2026-08-09 16:20
DIAGNÓSTICO — CAUSA RAÍZ DE LOS FALSOS POSITIVOS (12/12 en esta sesión):
  `scripts/fetch_news.py::fetch_ddg_search()` arma la consulta DDG como
  `site:prensa.com agropecuario OR agricultura OR ganadería OR MIDA OR
  cosecha Panamá`, pero el backend de noticias de DDG (`ddgs`) no respeta
  de forma confiable el operador `site:` — devuelve resultados de
  dominios completamente distintos (heraldo.es, nyfb.org, spa.gov.sa,
  sltrib.com, paultan.org, ebc.com.br, whc.unesco.org, msn.com) que
  simplemente contienen alguno de los términos OR (p. ej. "MIDA" o
  "agriculture"). Además, el código etiquetaba cada resultado con
  `source: "prensa.com"` y `country: "PA"` de forma incondicional, sin
  verificar el dominio real ni el contenido — por eso los falsos
  positivos parecían fuentes panameñas confiables en `stats`.
  FIX APLICADO: `fetch_ddg_search()` ahora descarta cualquier resultado
  cuyo dominio (`urlparse(url).netloc`) no contenga el `site` configurado,
  antes de aceptarlo como artículo. Esto debería eliminar la fuga de
  contenido global en el próximo fetch de GitHub Actions.
  Pendiente de verificar: confirmar en la próxima sesión que el fetch
  automático post-fix ya no produce falsos positivos de dominios ajenos.

## 2026-08-09 16:30
DIAGNÓSTICO — BUG EN GDELT BACKFILL (`_gdelt_windows` en processed.json):
  `sources/processed.json` tenía 63 "ventanas GDELT completadas", pero solo
  37 eran ventanas trimestrales reales (90 días). Las otras 26 eran
  variantes casi duplicadas de la MISMA ventana ("20260618_20260623",
  "20260618_20260624", ... hasta "20260618_20260806") — una nueva por
  cada corrida de GitHub Actions desde 2026-06-18.
  Causa raíz en `fetch_news.py::fetch_gdelt_historical()`: el límite
  superior `end` se calcula como `utcnow() - 1 día` (ayer), un valor que
  avanza cada día. Mientras la ventana de cola (la más reciente, aún sin
  llegar a 90 días) se recorta con `min(current+90, end)`, cada corrida
  genera una `window_key` distinta (porque `end` cambió), así que nunca
  coincide con ninguna entrada ya marcada como completa. Resultado: la
  ventana de cola se re-descarga y se marca "completa" de nuevo cada día,
  sin avanzar nunca al siguiente trimestre, desperdiciando llamadas a la
  API de GDELT en rangos de fecha casi idénticos.
  Efecto colateral: esto infla artificialmente el conteo de "ventanas
  completadas" en `wiki/metrics.md`, activando por error el umbral de
  "45+ ventanas ⇒ backfill agotado" del diagnóstico avanzado (Paso 4,
  punto 2 de CLAUDE.md) cuando en realidad el backfill real (37/~46
  trimestres) no había terminado.
  FIX APLICADO en `fetch_news.py::fetch_gdelt_historical()`: una ventana
  solo se marca como completa si alcanza los 90 días completos
  (`current + 90 días <= end`). La ventana de cola (parcial, limitada por
  `end` móvil) se consulta pero NUNCA se persiste como completa — el loop
  simplemente termina (`break`) tras procesarla, y se reintentará (más
  barato, con datos mayormente superpuestos) en la próxima corrida hasta
  que alcance los 90 días reales y cierre para siempre.
  LIMPIEZA: se eliminaron las 26 entradas basura de
  `sources/processed.json["_gdelt_windows"]`, dejando solo las 37
  ventanas trimestrales reales y verificadas (2017-03-30 → 2026-06-17).
  HALLAZGO ADICIONAL (sin confirmar — requiere acceso de red real de
  GitHub Actions, no disponible en esta sesión sandboxed): las primeras
  ~8 ventanas trimestrales (2015-01-01 → 2017-03-29, ~2 años) NUNCA
  aparecen como completadas, ni siquiera antes de la limpieza. Como el
  código solo marca una ventana completa tras una respuesta HTTP exitosa
  (nunca tras error de red), esto sugiere que esas ventanas llevan mucho
  tiempo fallando silenciosamente en cada corrida (error de red/HTTP) sin
  que nadie lo note, O que la API GDELT DOC 2.0 simplemente no tiene
  cobertura indexada para `sourcecountry:PA` en ese rango (el límite real
  de cobertura del GDELT DOC API documentado públicamente es ~2017, pese
  a que `CLAUDE.md` asume 2015-02-19 como "límite real de GDELT API v2").
  Acción para la próxima sesión con red real: correr manualmente
  `fetch_gdelt_batch` para la ventana `2015-01-01_2015-04-01` y revisar el
  código de respuesta/error exacto para confirmar la causa.
