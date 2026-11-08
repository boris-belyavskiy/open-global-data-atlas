# Access guide

Access describes the **route to data**, not the file format or reuse license.

| Code | Meaning | In available free data? |
| --- | --- | --- |
| OPEN | No-fee data without an account; terms may still apply | Yes |
| REGISTER | Free registration or user form; no substantive research review | Yes |
| APPLY | No-fee research application or authorization; approval not guaranteed | Yes, conditionally |
| REQUEST | Individually supplied data with a confirmed no-fee policy | Yes, conditionally |
| METADATA_ONLY | Only discovery/documentation is established by this card | No; reference directory only |
| PAID | Purchase, subscription or paid license required | No |

The initial records do not need to contain an example of every code. In particular, we do not invent a REQUEST or PAID example to fill a category. PAID remains in the schema so future reviews can explicitly reject or track out-of-scope leads without exposing them as available free data.

Methods (`api`, `bulk_download`, `web_download`, `web_interface`, `research_application`, `email_request`) and formats (`CSV`, `JSON`, `SDMX`, `Stata`, `SPSS`, etc.) are separate. An API can require registration. A catalogue may expose DDI metadata while withholding the respondent file.

Read the scope of the access claim. Afrobarometer public survey files are distinct from any special geocoded products. Global Findex public records do not provide the full Gallup World Poll. UNHCR aggregate statistics do not establish access to its microdata library. National restricted MTUS files may have additional conditions.

`license_url` points to the provider's documented access/terms evidence. Where a uniform license was not established, `license_name` says so instead of inventing an open license. Cite the selected release and follow its attribution, research-only and non-redistribution conditions. The repository license covers only our original code and metadata prose.
