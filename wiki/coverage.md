# Coverage and limitations

The seed was reviewed on **7 November 2026**. It demonstrates the architecture and all fourteen topic groups; it is not a full census of organizations, datasets, countries or questions.

Included examples cover UNdata, UN System Data Commons, the SDG database, World Bank catalogs and indicators, ILOSTAT, WHO GHO, FAOSTAT, UNODC, UNHCR, MICS, IPUMS MICS, LSMS, Global Findex, WVS, ESS, ISSP, Afrobarometer and MTUS. Not every represented organization is a UN agency: source cards explain the relationship.

Current limits:

- Broad statistical databases coexist with specific survey releases, and are explicitly labeled. Search counts are **metadata records**, never counts of independent underlying studies.
- Country tags cover only checked examples. Most portals' country inventories have not been enumerated. Filter results should not be interpreted as exhaustive availability.
- Defense, alliance membership, diplomatic relations, noise pollution, light pollution and several other subtopics remain thin or absent. The treaty collection is useful primary material for A5, not a harmonized alliance panel.
- No full indicator/question dictionary, cross-country comparability scoring, complete wave inventory, or download authentication test has been performed.
- Some landing pages require JavaScript or use dynamic links. Cards favor stable official landing/documentation URLs; APIs are labeled documentation or examples, not promises of tested uptime.
- The site performs local metadata search. It does not query provider APIs in the background, update itself, collect analytics or send search terms to a data provider.
- A successful static build and functional checks do not replace a full browser and screen-reader accessibility audit. Visual browser QA was unavailable during the initial build.

The initial implementation has **no workflows, schedules, crawlers, imports or background synchronization**. Local rendering commands are run manually, only against the already-authored YAML.
