# Schema reference · version 1.0

The canonical records are UTF-8 YAML files under `catalog/{organizations,catalogs,programs,datasets}/`. The [JSON Schema](downloads/catalog.schema.json) uses Draft 2020-12, rejects unknown fields and is enforced by the manually run validator. IDs are globally unique lowercase kebab-case strings. Relationships use IDs, not names.

## Shared fields

| Field | Type | Contract |
| --- | --- | --- |
| schema_version | string | Exactly `1.0` |
| id | string | Stable globally unique ID; filename matches |
| kind | enum | `organization`, `catalog`, `program`, `dataset` |
| name, description | string | English human-readable label and summary |
| topics | string array | Zero or more of A1–A6 and B1–B8; organizations may have an empty list |
| keywords | string array | English discovery terms and common aliases |
| verification | object | Status, date, method, scope, nonempty evidence list |

## Organization fields

| Field | Type | Contract |
| --- | --- | --- |
| website | URL | Official home or programme-specific organization page |
| un_relation | enum | `UN_SYSTEM`, `UN_RELATED`, `UN_PARTNER`, `INDEPENDENT` |
| relation_note | string | Explain legal independence or the particular collaboration; evidence required |

Organizations have no implicit dataset access status. Source cards list their linked resources.

## Resource fields (catalogs, programmes and datasets)

| Field | Type | Contract |
| --- | --- | --- |
| organization_id | ID | Must resolve to an organization |
| parent_id | ID or null | Primary parent catalog or programme; no cycles |
| catalog_ids | ID array | Additional indexing catalogs; no duplicate dataset records |
| original_producer | string | Who creates or harmonizes data; national agencies may differ by series |
| collector | string | Who collected responses or administrative records |
| publisher | string | Who distributes this representation; may differ from the responsible organization |
| data_levels | enum array | `aggregate`, `microdata`, `geospatial`, `text_event` |
| observation_units | enum array | `country`, `region`, `person`, `household`, `diary_day`, `treaty`, `event`, `organization`, `firm`, `grid_cell` |
| geography | object | Scope, regions, country codes, completeness and explanatory notes |
| time_coverage | string | Descriptive fieldwork/series coverage, without implying a balanced panel |
| release | string or null | Exact release identifier where verified; null if not pinned |
| access | object | Data access status, fee availability flag, methods, formats, notes and terms reference |
| links | object array | Each has `rel` and exact `url`; first is the original landing URL |
| survey | object or null | Method, weights, representativeness, comparability; required non-null for survey programme/dataset microdata |

### Geography

`scope` is `single_country`, `multi_country` or `global`. `regions` uses the discovery regions in `taxonomy/geography.yml`, not a claimed official UN M49 hierarchy. `country_codes` uses the curated ISO 3166-1 alpha-3 examples in that file. Territories and non-ISO provider geographies require an explicit future schema extension; never silently rewrite a provider code as ISO. `coverage_completeness` is `complete`, `partial` or `not_enumerated`. `notes` explains what was checked. Empty codes mean unknown/not enumerated, never “no coverage.”

### Access

`status` is `OPEN`, `REGISTER`, `APPLY`, `REQUEST`, `METADATA_ONLY` or `PAID`. `free_data_available` must be true for the first four and false for the last two. For APPLY/REQUEST, true describes a documented no-fee route, not approval for a particular user. The UI starts with available free routes only.

`methods` and `formats` use `taxonomy/methods.yml`. `notes` limits the claim to the actual product. `license_name` is a provider license name when established, otherwise an explicit provider-specific/unknown statement. `license_url` links to the provider terms or access documentation; it is not a blanket relicensing claim.

### Verification

`status`: `discovered`, `verified`, `indexed`. `checked_on`: ISO date. `method`: `public_documentation` or `download_test`. `scope`: what was and was not checked. `evidence`: nonempty array of `{url, claim}` objects. Official provider documentation supports access claims, but public-documentation verification does not imply successful authenticated download.

## SDG crosswalk

`crosswalks/sdg-indicators.csv` has `record_id`, `topic_id`, `goal`, `target`, `indicator`, `mapping_type`, `note`, `evidence_url`. Goal/target/indicator identifiers are strings. `mapping_type` is `official_series`, `related_measure` or `potential_input`. Relationships are many-to-many. SDG codes are not valid topic IDs. Crosswalk edits require checking the current official metadata, because indicator frameworks are revised.

## Export and search contract

JSONL exports complete canonical records, one JSON object per line. CSV uses the union of top-level fields as columns; nested arrays/objects are compact JSON strings in properly quoted CSV cells. Blank means the field is absent for that entity kind; literal `null` means an explicitly null canonical value. For lossless processing prefer JSONL.

The browser index adds `organization_name`, `un_relation`, `topic_labels`, `country_labels` and `card_url` as derived display fields. These do not belong in canonical YAML. It excludes organization rows because they have a separate source directory. The search count is a count of heterogeneous metadata records.

Validation checks structural types, known topics/countries, foreign keys, parent cycles, free-data rules and SDG references. Site checks also verify export equivalence, generated record consistency and local links. These are manually invoked checks, not scheduled automation.
