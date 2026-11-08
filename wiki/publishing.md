# Manual editing and publishing

There are no GitHub Actions workflows, imports, scheduled checks or deploy bots in this repository. The rendered HTML is committed in `docs/`, so GitHub Pages can serve it without installing Python or MkDocs.

## Enable GitHub Pages

Open repository **Settings → Pages → Build and deployment**. Choose **Deploy from a branch**, then **main** and **/docs**, and save. GitHub's built-in Pages publication service may show a deployment run; that is the hosting mechanism, not a repository-defined data pipeline. The `.nojekyll` file preserves MkDocs output.

Expected address: [Open Global Data Atlas](https://boris-belyavskiy.github.io/open-global-data-atlas/). The root [README](https://github.com/boris-belyavskiy/open-global-data-atlas) and source Markdown remain usable if Pages is not enabled.

Reference: [GitHub publishing-source documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Edit locally

Use Python 3.10 or later. Install the pinned build dependencies in an isolated environment:

```bash
python -m venv .venv
# Activate .venv for your operating system.
python -m pip install -r requirements.txt
```

Edit `catalog/`, `taxonomy/`, `crosswalks/` or the editorial pages under `wiki/`. Then explicitly run:

```bash
python scripts/validate.py
python scripts/render_catalog.py
python -m mkdocs build --strict
python scripts/check_site.py
node scripts/test_search.cjs
```

Review the changed metadata, generated pages, exports and compiled `docs/`, then commit and push them together. Site rebuilding is manual. These local helpers do not access the network or harvest data. If deleting a record, also remove its old generated page from `wiki/records/` before building; validation checks for stale pages at the site-check stage.

For an optional local preview, run `python -m mkdocs serve`. Plainly opening HTML using `file://` can prevent the browser from loading the local JSON search index; use HTTP or GitHub Pages.

Public URLs in `mkdocs.yml` need adjustment if the repository is forked to another owner. Authored content is English. Prefer stable official links, preserve IDs, explain access discrepancies and attach evidence before calling an entry verified.
