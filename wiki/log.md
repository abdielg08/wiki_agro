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

## 2026-09-21 00:00
ROUTINE (sesión programada): git pull origin main OK. `python wiki_agro.py stats` → 57 descargados,
13 ingestados, 44 pendientes. Se instalaron dependencias faltantes (click, requirements.txt) en el
entorno antes de poder ejecutar el script.

INGEST: 5 artículos procesados (todos verificados 100% sobre agro de Panamá — 0 falsos positivos)
  Artículos:
    - 20250724_prensacom_arroz-crisis-importaciones-cosecha → summaries/ + topics/arroz.md, credito_financiamiento.md, politicas_agropecuarias.md actualizados + entities/mida.md actualizado
    - 20241107_prensacom_inundaciones-perdidas-arroz-maiz-ganaderia → summaries/ + topics/arroz.md, maiz.md, cambio_climatico.md actualizados
    - 20220524_prensacom_siembra-90mil-hectareas-arroz-2022-2023 → summaries/ + topics/arroz.md actualizado + entities/mida.md actualizado
    - 20240607_prensacom_roberto-linares-revision-subsidios-mida → summaries/ + topics/politicas_agropecuarias.md actualizado + entities/mida.md actualizado
    - 20240613_prensacom_productores-arroz-panama-este-darien-compensaciones → summaries/ + topics/arroz.md, credito_financiamiento.md actualizados + entities/mida.md actualizado
  Páginas actualizadas: arroz.md, maiz.md, cambio_climatico.md, credito_financiamiento.md, politicas_agropecuarias.md, mida.md
  Summaries: 5 nuevos archivos en wiki/summaries/
  Nota de calidad de datos: los artículos de origen prensa.com en `sources/articles/` solo contienen
  `summary_raw` truncado (~280 caracteres); `full_text` es `null`. Los resúmenes y hechos clave
  ingestados reflejan únicamente lo disponible en ese extracto — no se inventaron cifras ni datos
  adicionales. Se marcó explícitamente en cada summary cuando el texto fuente está truncado.

`python wiki_agro.py mark-all-ingested --limit 5` → 5 artículos marcados como ingestados.
Post-ingesta: 18 ingestados, 39 pendientes, 25 páginas wiki (8 topics, 3 entidades, 11 resúmenes).

DIAGNÓSTICO: Pendientes de ingesta > 0 (39) al cierre de la sesión — dentro de lo esperado dado el
límite de 5 artículos/sesión; no se activa el diagnóstico avanzado del Paso 4. Ver wiki/metrics.md
para el estado del fetch GitHub Actions / GDELT.

## 2026-09-21 00:13
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-09-21 00:20
DIAGNÓSTICO: Contaminación de falsos positivos detectada en la cola de pendientes (sources/articles/)

Al inspeccionar los 39 artículos pendientes en `sources/processed.json` / `sources/articles/` para
esta sesión, se encontró que un subconjunto significativo **no trata sobre agro panameño**, pese a
estar etiquetados con `"source": "prensa.com"`. Ejemplos concretos identificados (URLs reales en
`sources/articles/`, ninguno fue ingestado al wiki):

- `ieeexplore.ieee.org/document/10945742` — paper IEEE sobre IoT y agricultura de precisión (genérico, sin relación con Panamá)
- `www.sltrib.com/...utah-nuclear...` y otras 2 notas de Salt Lake Tribune sobre data centers en Utah — coinciden por la sigla **"MIDA"** (en Utah, "Military Installation Development Authority"), no el Mida panameño
- `www.thestar.com.my/...` (3 artículos) y `paultan.org/...` — MIDA = **Malaysian Investment Development Authority**, agencia de inversión de Malasia, no relacionada con Panamá
- `www.heraldo.es/...` (3 artículos) — agricultura en **Aragón, España**
- `clubofmozambique.com/...` — vacunación ganadera en **Mozambique**
- `agenciabrasil.ebc.com.br/...` — financiamiento agrícola en **Brasil**
- `www.spa.gov.sa/...` — programa de agricultura de secano en **Arabia Saudita**
- `www.nyfb.org/` — New York Farm Bureau (EE.UU.)
- `whc.unesco.org/...persian-qanat` — patrimonio UNESCO de Irán, sin relación agrícola panameña
- `www.maine.gov/dacf/ard/...` — división de desarrollo agrícola del estado de **Maine**, EE.UU.
- `www.msn.com/...cultural-rules-for-staying-with-locals-abroad` — artículo de viajes, sin relación con agro

Estimado: **~17 de 39 pendientes (≈44%)** son falsos positivos claros por esta causa. Todos
comparten el campo `"source": "prensa.com"` en su JSON pese a que la URL real apunta a otros
dominios — indica que el pipeline de fetch (GDELT y/o agregador RSS) está mal etiquetando el
`source` y/o capturando resultados por colisión de palabras clave (la sigla "MIDA" en particular
coincide con al menos 3 instituciones no panameñas: Malasia, Utah y posiblemente otras).

**Ningún falso positivo fue ingestado al wiki** — el ingest de esta sesión (5 artículos, ver entrada
anterior) fue verificado individualmente y confirmado 100% sobre agro de Panamá antes de escribir
cualquier página. Este hallazgo es sobre la **cola de pendientes**, no sobre contenido ya en wiki/.

**Acción recomendada para el usuario / próximas sesiones**:
1. Revisar y endurecer el filtro de relevancia geográfica en el pipeline de fetch (GDELT/RSS) antes
   de guardar en `sources/articles/` — no confiar en coincidencias de palabras clave como "MIDA",
   "agro" o "farm" sin verificar país/dominio.
2. En cada sesión de `ingest`, verificar la URL real de cada artículo (no solo el campo `source`)
   antes de decidir si es sobre agro panameño, tal como exige CLAUDE.md regla 9.
3. No se modificó `sources/` ni se marcaron estos artículos como ingestados/falsos positivos en
   `processed.json`, ya que el script no expone un comando dedicado para ello (solo
   `mark-ingested`/`mark-all-ingested`) y `sources/` es inmutable por regla del proyecto.

## 2026-09-21 00:16
LINT: 25 páginas revisadas, 54 issues encontrados
  frontmatter:0, huérfanas:1, broken_links:41, stale:11, no_index:1

## 2026-09-21 00:17
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-09-21 00:25
BUGFIX: `mark-all-ingested` marcaba artículos incorrectos en `processed.json`

Al verificar `sources/processed.json` tras el primer `mark-all-ingested --limit 5` de esta sesión,
se detectó que **ninguno de los 5 artículos realmente procesados** en este ingest (los de
`pending_ingest.md`: crisis arrocera 2025, inundaciones Veraguas 2024, proyección siembra
2022-2023, transición Linares 2024, compensaciones Panamá Este/Darién 2024) quedó marcado como
`ingested: true`. En su lugar, el comando marcó 5 artículos completamente distintos y no
relacionados con el trabajo de esta sesión (p. ej. "Catalogue of the diptera of the Americas South
of United States", "Las seis plagas de la agricultura", "Horizonte agropecuario").

**Causa raíz** (en `scripts/ingest.py`): `mark_all_ingested()` llamaba a `find_pending()`, que
ordena los artículos pendientes alfabéticamente por nombre de archivo. Pero `ingest`/`run_prepare()`
selecciona y ordena los artículos mostrados en `pending_ingest.md` usando `prioritize(strategy=
"score")` (orden por relevancia). Ambos órdenes son distintos, así que "los primeros N pendientes"
según `find_pending()` casi nunca coinciden con "los N artículos que Claude acaba de procesar".
Este bug existía desde la sesión semilla (2026-05-24) y probablemente afectó marcas anteriores
también (no verificado retroactivamente en esta sesión).

**Fix aplicado**: `mark_all_ingested()` ahora parsea las URLs exactas de los comandos
`mark-ingested '<url>'` que `run_prepare()` ya escribe al final de `pending_ingest.md` — es decir,
usa la fuente de verdad de qué se le mostró realmente a Claude, en vez de recalcular una lista
pendiente con un orden distinto. Con fallback al comportamiento anterior si `pending_ingest.md` no
existe. Ver `scripts/ingest.py`.

**Corrección de datos**: se revirtieron manualmente los 5 marcados incorrectos
(`ingested: false`, se eliminó `ingested_at`) y se volvió a ejecutar `mark-all-ingested --limit 5`
con el fix, que marcó correctamente los 5 artículos de esta sesión. Verificado: `python wiki_agro.py
stats` reporta 18 ingestados / 39 pendientes, consistente antes y después de la corrección (el
número total no cambió, solo qué URLs específicas están marcadas).

**Impacto**: ninguna página del wiki se vio afectada — el contenido escrito en `wiki/` siempre
correspondió a los 5 artículos correctos, verificados individualmente. El bug solo corrompía el
libro de contabilidad en `processed.json`, con el riesgo de que artículos reales pendientes quedaran
permanentemente ocultos de futuras sesiones de `ingest` (al aparecer falsamente como ya ingestados)
mientras el trabajo real quedaba sin registrar.
