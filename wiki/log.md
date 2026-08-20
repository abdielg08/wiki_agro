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

## 2026-08-20 — DIAGNÓSTICO: causa raíz del backfill detenido

**Resultado de la sesión**: 0 artículos ingestados. Los 17 pendientes eran
falsos positivos al 100%. Ninguno se ingestó al wiki.

### Falsos positivos rechazados (24 en total)

Los 17 pendientes más 7 que sesiones previas habían marcado como "ingestados"
sin llegar a crear página. Todos entraron por la ruta de búsqueda web (DDG) y
figuraban erróneamente con fuente `prensa.com`:

- **9 por la sigla MIDA**: Malaysian Investment Development Authority
  (thestar.com.my, paultan.org) y Military Installation Development Authority
  de Utah (sltrib.com, fox13now.com, msn.com). Nada que ver con el Ministerio
  de Desarrollo Agropecuario de Panamá.
- **9 de agro extranjero**: Aragón/España (heraldo.es), Brasil
  (agenciabrasil.ebc.com.br), Arabia Saudita (spa.gov.sa), Maine y Nueva York.
- **6 sin relación con agro**: paper de robótica IEEE, catálogo entomológico de
  1966, ficha UNESCO sobre qanats persas, uranio en Utah, página genérica del
  Banco Mundial.

El wiki mantiene **0% de falsos positivos**: ninguno generó página. La
contaminación estaba solo en `processed.json`, ahora saneada con un estado
`rejected` explícito y su motivo.

### Cuatro bugs que explican el estancamiento

1. **`sourcecountry:PA` consultaba Paraguay.** GDELT usa códigos FIPS 10-4,
   donde `PA` = Paraguay y Panamá = `PM`. Las 71 ventanas crawleadas entre
   junio y agosto (2017-03-30 → 2026-08-19, contiguas) devolvieron **cero**
   artículos porque preguntaban por el país equivocado. Esta es la causa
   principal de que el backfill lleve ~3 meses sin avanzar.
2. **Filtro de titular redundante en GDELT.** Sobre `sourcecountry` ya
   restringido, se exigía además un término "Panamá" en el título. La prensa
   panameña no nombra al país en sus titulares ("Productores de arroz piden
   apoyo"), así que el filtro descartaba precisamente la cobertura doméstica
   que buscamos.
3. **DDG ignora `site:`.** El endpoint de noticias de `ddgs` (backends Bing/
   Yahoo) no respeta el operador, y el código no verificaba el dominio
   resultante ni aplicaba los guardas `_is_blocked_domain` /
   `_is_panama_related` que sí usan RSS y GDELT. De ahí los 24 falsos
   positivos, todos etiquetados con el `site` pedido en vez del dominio real.
4. **Match por subcadena.** `is_agro_relevant` buscaba términos como
   subcadenas, de modo que "MIDA" disparaba dentro de "comida", "medida" o
   "temida" — una fuente silenciosa de ruido en texto español.

### Correcciones aplicadas

- `sourcecountry:PM` en `fetch_news.py`, `fetch_historical.py` y `config/sources.yaml`.
- GDELT: el filtro de titular se sustituye por relevancia agro; la geografía
  queda a cargo de `sourcecountry`.
- DDG: se verifica que el dominio devuelto coincida con el `site` pedido, se
  aplican ambos guardas y la fuente se etiqueta con el dominio real. Los
  dominios panameños conocidos quedan exentos del requisito de nombrar al país.
- `is_agro_relevant` pasa a match por palabra completa.
- Ventanas GDELT reseteadas de 71 a 0: su estado reflejaba un crawl de Paraguay.
- Nuevo estado `rejected` + comando `mark-rejected`, para que un falso positivo
  salga de la cola sin contarse como ingestado. `stats` ahora lo reporta aparte.

### Validación

Los filtros se probaron contra los 30 artículos almacenados: rechazan los 24
falsos positivos y conservan los 6 legítimos. El fetch en vivo **no pudo
validarse** desde la routine: el egress del sandbox bloquea GDELT, los RSS y
DDG. La verificación real ocurrirá en la próxima corrida de GitHub Actions;
si el backfill sigue en cero tras el cambio a `PM`, revisar ahí los logs.
