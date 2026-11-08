# Open Global Data Atlas

**[Open the searchable atlas →](https://boris-belyavskiy.github.io/open-global-data-atlas/)**

A metadata-first directory of freely accessible UN-system and partner data, plus independent international surveys. All authored content is English. Find sources by organization or topic, understand how to obtain data, and follow links to the original publisher.

[Browse by source](wiki/sources.md) · [Browse by topic](wiki/topics/index.md) · [Survey programmes](wiki/programs.md) · [Catalogs](wiki/catalogs.md) · [Datasets](wiki/datasets.md) · [Schema reference](wiki/schema-reference.md) · [JSONL](exports/catalog.jsonl) · [CSV](exports/catalog.csv)

## What is here

- A GitHub Pages-ready **MkDocs Material** site with a prominent keyword finder, combined topic/country-or-region/data-level/access/type filters, shareable filtered URLs, and full-documentation search.
- Source, catalog, programme and dataset cards derived from a single curated YAML registry. Each card records provenance, access conditions, exact original URLs and verification evidence.
- Six country/regional groups: economy and resources; demography and population health; environment and climate; defence and security; international relations and affiliations; social development and institutions.
- Eight individual/household groups: time use; financial/economic behaviour; health and subjective well-being; family/reproductive relations; social relations; political participation and the state; values/norms/beliefs; risk/safety/migration.
- A separate, evidence-linked **SDG crosswalk**, with explicit distinctions between official series, related measures and potential inputs.
- YAML, CSV and JSONL metadata, a JSON Schema, research guides and manual publishing instructions. No original statistical data or respondent records are stored here.

This is a curated seed, checked against public provider documentation on **2026-11-07**. It is not exhaustive. “Verified” does not mean every download was tested. Country filters cover **checked examples only**, not complete source coverage. Data level and unit of observation are distinct. Read [coverage and limitations](wiki/coverage.md).

## Data schema at a glance

Canonical files live in `catalog/`, one entity per YAML file. The complete contract is in [schemas/catalog.schema.json](schemas/catalog.schema.json) and the [schema reference](wiki/schema-reference.md).

| Field group | Key fields | Purpose |
| --- | --- | --- |
| Identity | `schema_version`, `id`, `kind`, `name`, `description` | Stable IDs; organization/catalog/program/dataset entities |
| Organization | `website`, `un_relation`, `relation_note` | UN-system, related, documented partner, or independent identity |
| Relationships | `organization_id`, `parent_id`, `catalog_ids` | Source/programme/catalog graph without duplicating studies |
| Provenance | `original_producer`, `collector`, `publisher` | Distinguish who made, collected and published data |
| Discovery | `topics`, `keywords`, `data_levels`, `observation_units` | Separate thematic subject from publication form and record unit |
| Coverage | `geography`, `time_coverage`, `release` | Countries/regions, completeness caveat, fieldwork/series period and release |
| Access | `access.status`, `free_data_available`, `methods`, `formats`, `notes`, `license_name`, `license_url` | No-fee route, technical access and reuse evidence |
| Original material | `links` | Exact landing, documentation, codebook and API URLs |
| Survey design | `survey` | Method, weights, representativeness and comparability caveats |
| Evidence | `verification` | Status, check date, method, scope and supporting URLs |

`access.status`: **OPEN**, **REGISTER**, **APPLY**, **REQUEST**, **METADATA_ONLY**, **PAID**. Only the first four can be marked available free data. APPLY/REQUEST are conditional on approval. Reference-only entries remain discoverable but are excluded by the finder's default free-data filter. PAID is supported by the schema but excluded from available data. Free download does not imply permission to redistribute.

YAML is the source of truth. JSONL contains complete records. CSV has one entity per row, with nested arrays/objects encoded as JSON cells. The browser index is derived and adds display labels. SDGs belong in `crosswalks/`, not the topic field.

## Repository layout

```text
catalog/         Curated YAML: organizations, catalogs, programmes, datasets
taxonomy/        Six country topics, eight microdata topics, access/method/geography vocabularies
crosswalks/      Selected SDG mappings
schemas/         JSON Schema
exports/         Complete JSONL and CSV metadata
wiki/            MkDocs source: editorial pages and rendered cards/directories
docs/            Committed static HTML for GitHub Pages (main /docs)
scripts/         Manually invoked offline rendering and checks
mkdocs.yml       Material theme, navigation and full-text search
```

## Run and publish manually

```bash
python -m pip install -r requirements.txt
python scripts/render_catalog.py
python -m mkdocs build --strict
python scripts/check_site.py
node scripts/test_search.cjs
```

Use an isolated Python environment, then review and commit source, exports and rendered `docs/` together. For local preview, use `python -m mkdocs serve`. The renderer reads local YAML only; it never imports provider data.

If Pages is not already enabled, open **Settings → Pages**, select **Deploy from a branch → main → /docs**, and save. [Detailed instructions](wiki/publishing.md). GitHub's built-in static hosting deployment is the only publication mechanism; this repository contains **no Actions workflows, scheduled CI, crawlers, automated imports or background jobs**.

## Contribute and extend

Read [CONTRIBUTING.md](CONTRIBUTING.md). Preserve stable IDs, cite official evidence and distinguish dataset access from metadata visibility. No registration, research request or automated extraction is performed on behalf of a visitor.

Recommended order: expand and review the registry → approve change-validation checks → pilot a single metadata importer → add release/variable indexing → consider opt-in scheduled refreshes. The [roadmap](wiki/roadmap.md) describes these future stages; none is enabled.

Original atlas code and metadata prose are under [MIT](LICENSE). External source data, documents, names and third-party MkDocs/Material assets retain their own rights and licenses. This atlas is an independent directory and is not an official UN publication.

