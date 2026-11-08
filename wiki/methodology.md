# Methodology

## Scope and unit of cataloging

The atlas covers freely accessible UN-system data, documented collaborations and independent international survey datasets. It is a metadata directory; it does not host statistical observations or respondent data. “Open” in the project title includes documented no-fee registration and application routes; it does not mean every source has an open license.

Four record kinds form a graph:

1. **Organization / source**: institutional identity and relationship to the UN.
2. **Catalog**: portal or meta-catalog indexing resources. Some also distribute data.
3. **Programme**: recurring survey or harmonization programme.
4. **Dataset**: a statistical database family or a specific survey release. The title and release field say which.

A parent relationship expresses the main catalog/programme context. `catalog_ids` expresses additional discovery locations. The same study is not duplicated just because it appears in IHSN and the World Bank. A harmonized derivative such as IPUMS MICS gets its own record linked to the original programme; it is not a new independent survey. A variable/indicator entity is intentionally deferred.

## Institutions and provenance

`organization_id` links to the responsible source card. `original_producer`, `collector` and `publisher` describe distinct roles. National statistical agencies frequently produce data that international organizations harmonize and publish. Broad database cards name the producer class; precise producer identifiers belong in future series-level records.

`UN_SYSTEM` includes UN entities and autonomous specialized institutions. `UN_RELATED` is reserved for documented formal related-organization status. `UN_PARTNER` requires evidence of a particular collaboration and does not imply UN ownership. `INDEPENDENT` prevents research networks from being mislabeled as UN bodies merely because UN publications use their data. Membership context comes from the [CEB](https://unsceb.org/faq/); individual partner claims have card-specific evidence.

## Two dimensions, not two competing copies

The source directory and the topic directory are rendered from the same curated YAML records. Topics can overlap. Country and microdata topics are discovery routes; they are not a claim that every linked item has the same unit of observation. For example, a treaty has a treaty/event unit, and Findex has separate individual and aggregate products.

`data_levels` describes publication form. `observation_units` describes what one observation refers to. A household sampling frame does not automatically make the public file household-level. MTUS diary-day records require additional care. Neither topic nor programme membership substitutes for these fields.

## Verification

Each card records a check date, evidence URLs, supported claims and verification scope. `verified` in this seed means official public documentation was reviewed; it does **not** mean we created an account, received research approval, downloaded every data file or audited every variable. `discovered` is for unverified leads; `indexed` is reserved for deeper release/series indexing. Neither status guarantees freshness.

Provider documentation can conflict or lag an interface. The WVS access note explains a discrepancy between older no-registration publicity and current registration documentation. The Ethiopia LSMS seed is marked reference-only because its current public access page did not establish data availability. Failures to fetch JavaScript pages are not interpreted as proof that data are unavailable.

## Geography and time

Country tags are confirmed **examples**, not the full coverage. Their completeness is explicit. No country match is inferred from a worldwide programme label. This conservative filter has false negatives until the inventory expands. A record can be globally scoped yet contain no country codes in this release.

Time coverage is descriptive at this stage. A programme's starting date must not be mistaken for a balanced panel. Dataset release, fieldwork year and publication date are different. Geography, variable availability, sampling and weights should be verified at the original source before analysis.
