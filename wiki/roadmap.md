# Staged next steps

Nothing on this page is enabled or scheduled.

Before adding long-lived build automation, review the theme lifecycle. The requested Material for MkDocs implementation is pinned and working, but its maintainers announce [end of life on May 5, 2027](https://squidfunk.github.io/mkdocs-material/). Evaluate a supported migration while retaining the portable YAML/Markdown catalog; no framework migration is included in this release.

1. **Expand and review the registry manually.** Fill source gaps, add complete country/wave coverage, verify download routes and nominate maintainers. Prioritize diplomacy/defense, time use, household budgets, environmental exposures and missing UN agencies. Add reproducible issue templates for access corrections.
2. **Add validation on proposed changes, if approved.** Run schema, relationship, export consistency and internal-link checks on pull requests. Keep external link checks rate-limited and distinguish temporary blocking from dead resources. This stage does not import data.
3. **Pilot one metadata-only importer.** Start with a well-documented catalog such as the World Bank Indicators API or ILOSTAT table of contents. Cache metadata, retain provenance and revisions, use stable IDs, and submit changes for human review. Do not download respondent files or bypass registration. Review each provider's automation terms first; UNHCR's current API guidance specifically limits continuous/high-volume extraction and production backend use.
4. **Index studies, indicators and questions.** Model release-specific countries, years, units, question wording, response scales and file relationships. Build conservative duplicate links and distinguish harmonized derivatives. Extend the schema before ingesting variable-level metadata.
5. **Introduce opt-in scheduled refreshes only after pilots work.** Set a modest cadence, failure budget, rate limits, change summaries and human approval thresholds. Preserve historic metadata snapshots and an audit trail. Schedule publishing separately from metadata discovery, and keep licensing changes visible.

Provider APIs and catalogs have different terms and structures; a universal crawler is not the recommended first step. Success should be measured by accurate access routes and useful study discovery before expanding record counts.
