# Wiki Agropecuario de Panamá — Schema y Guía del LLM

## Propósito
Este wiki documenta noticias, tendencias, retos y oportunidades del sector
agropecuario panameño de los últimos 10 años (2015–2025), construido y
mantenido por un LLM siguiendo la metodología Karpathy.

---

## Estructura de Directorios

```
wiki_agro/
├── CLAUDE.md               ← Este archivo (schema e instrucciones)
├── sources/                ← Artículos crudos (INMUTABLES, LLM no modifica)
│   ├── articles/           ← JSON+texto de cada artículo
│   └── processed.json      ← Registro de artículos procesados
├── wiki/                   ← DOMINIO DEL LLM (crea y mantiene)
│   ├── index.md            ← Catálogo maestro de todas las páginas
│   ├── log.md              ← Log cronológico de actividad (append-only)
│   ├── topics/             ← Páginas de temas/conceptos
│   ├── entities/           ← Páginas de entidades (orgs, lugares, cultivos)
│   └── summaries/          ← Resúmenes individuales de artículos
└── scripts/                ← Automatización Python
```

---

## Taxonomía de Temas (topics/)

### Cultivos Principales
- `arroz.md` — producción, variedades, mercado
- `maiz.md` — producción, usos, subsidios
- `platano_banano.md` — exportaciones, plagas (Sigatoka, Fusarium)
- `cafe_cacao.md` — Chiriquí, mercados especiales
- `cana_azucar.md` — ingenios, producción de azúcar
- `hortalizas.md` — tomate, cebolla, tubérculos
- `frutas.md` — mangos, piñas, melones, sandías

### Ganadería y Proteína Animal
- `ganaderia_bovina.md` — cría, doble propósito, carne, leche
- `porcicultura.md` — producción porcina
- `avicultura.md` — pollos, huevos, mercado
- `acuicultura_pesca.md` — camarones, tilapia, pesca artesanal

### Retos Sectoriales
- `cambio_climatico.md` — sequías, El Niño, inundaciones, adaptación
- `seguridad_alimentaria.md` — autoabastecimiento, pobreza rural
- `plagas_enfermedades.md` — gusano cogollero, roya, enfermedades
- `precios_mercados.md` — volatilidad, importaciones, exportaciones
- `credito_financiamiento.md` — BDA, préstamos, seguros agrícolas
- `tecnologia_innovacion.md` — agricultura de precisión, drones, semillas
- `agua_riego.md` — sistemas de riego, sequías, gestión hídrica
- `tierras_tenencia.md` — reforma agraria, titulación, conflictos
- `comercio_exterior.md` — TLC, exportaciones, acceso a mercados

### Políticas y Gobernanza
- `politicas_agropecuarias.md` — leyes, decretos, planes de gobierno
- `subsidios_programas.md` — Plan de Semillas, Agroalimentos, crédito subsidiado
- `mida_institucional.md` — MIDA, IDIAP, BDA, políticas

### Regiones Agrícolas
- `chirique.md` — principal zona agrícola, hortalizas, ganadería, café
- `azuero.md` — ganadería, cultivos, sequía
- `veraguas.md` — diversidad productiva, palma africana
- `cocle.md` — caña de azúcar, piña, ganadería
- `bocas_del_toro.md` — banano, cacao, Chiquita/Fyffes
- `darien_comarca.md` — frontera, agricultura indígena, palma africana

---

## Tipos de Entidades (entities/)

### Organizaciones Gubernamentales
- `mida.md` — Ministerio de Desarrollo Agropecuario
- `idiap.md` — Instituto de Investigación Agropecuaria de Panamá
- `bda.md` — Banco de Desarrollo Agropecuario
- `anamb.md` — Autoridad Nacional del Ambiente (y sus sucesores)
- `mef_agricola.md` — MEF y política fiscal agrícola

### Organizaciones Internacionales
- `iica_panama.md` — IICA oficina Panamá
- `fao_panama.md` — FAO Panamá
- `bid_panama.md` — BID proyectos agrícolas
- `banco_mundial_panama.md` — Banco Mundial proyectos

### Sector Privado y Gremios
- `anagan.md` — Asociación Nacional de Ganaderos
- `arap.md` — Autoridad de Recursos Acuáticos
- `cna_panama.md` — Consejo Nacional Agropecuario

---

## Formato de Páginas Wiki

Cada página usa este frontmatter YAML:

```yaml
---
title: "Título de la Página"
type: topic|entity|summary|overview
tags: [tag1, tag2, tag3]
last_updated: YYYY-MM-DD
article_count: N
sources: [url1, url2]
related: [page1.md, page2.md]
---
```

Luego secciones en markdown:
- **Resumen** (1-2 párrafos)
- **Hechos Clave** (bullets con fechas y fuentes)
- **Tendencias** (evolución en los 10 años)
- **Retos** (problemas identificados)
- **Referencias** (artículos fuente)
- **Ver también** (links a páginas relacionadas)

---

## Operaciones del LLM

### INGEST (al procesar un artículo nuevo)
1. Leer el artículo crudo de `sources/articles/`
2. Extraer: resumen, entidades, temas, hechos clave con fechas
3. Crear `wiki/summaries/{slug}.md` con el resumen del artículo
4. Actualizar páginas de topics relevantes (máx 5 páginas por artículo)
5. Actualizar páginas de entities mencionadas (máx 3 por artículo)
6. Actualizar `wiki/index.md` con nuevas páginas creadas
7. Agregar entrada a `wiki/log.md`

### QUERY (al responder una pregunta)
1. Leer `wiki/index.md` para orientarse
2. Leer páginas relevantes del wiki
3. Formular respuesta con citas
4. Si la respuesta es valiosa y nueva, crear página en `wiki/topics/` o `wiki/summaries/`
5. Actualizar index y log

### LINT (mantenimiento periódico)
1. Verificar consistencia de frontmatter en todas las páginas
2. Identificar páginas huérfanas (sin links entrantes)
3. Detectar contradicciones entre páginas
4. Marcar afirmaciones potencialmente desactualizadas
5. Sugerir cross-references faltantes

---

## Convenciones de Naming

- Archivos: `snake_case.md` (minúsculas, guiones bajos)
- Slugs de artículos: `YYYYMMDD_{fuente}_{titulo-corto}.md`
- Topics: nombre descriptivo en español
- Entidades: nombre oficial abreviado

---

## Fuentes Confiables (niveles de confianza)

### Nivel 1 — Oficial/Gubernamental
- MIDA (mida.gob.pa)
- IDIAP (idiap.gob.pa)
- Contraloría General (contraloria.gob.pa)
- ARAP (arap.gob.pa)

### Nivel 2 — Internacional
- FAO (fao.org)
- IICA (iica.int)
- BID/IADB (iadb.org)
- Banco Mundial (worldbank.org)
- CEPAL (cepal.org)

### Nivel 3 — Medios Nacionales Verificados
- La Prensa (prensa.com)
- Panama América (panamaamerica.com.pa)
- TVN Noticias (tvn-2.com)
- El Siglo (elsiglo.com.pa)
- La Estrella de Panamá (laestrella.com.pa)

### Nivel 4 — Medios Internacionales con cobertura de Panamá
- Reuters
- AFP
- El País

---

## Citas en el Wiki

Formato: `[Fuente, Fecha](URL)` o `[Fuente, Año]` si no hay URL directa.
Ejemplo: `La producción de arroz cayó un 15% [MIDA, 2023](https://mida.gob.pa/...)`

---

## Reglas Críticas

1. **NUNCA modificar archivos en `sources/`** — son la fuente de verdad inmutable
2. **SIEMPRE actualizar `wiki/log.md`** al hacer cualquier cambio al wiki
3. **SIEMPRE actualizar `wiki/index.md`** al crear una página nueva
4. **Usar fechas precisas** cuando estén disponibles (YYYY-MM-DD)
5. **Cross-referenciar agresivamente** — si mencionas "MIDA" en un topic, agrega link a `entities/mida.md`
6. **Conflictos de información**: registrar ambas versiones con sus fuentes, no omitir
7. **Máximo 800 palabras** por página de wiki (excepto overviews que pueden tener 1500)
