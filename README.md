# HMHC Reports

Source of record for the analyst reports published at **[reports.hmhc.ai](https://reports.hmhc.ai)**.

Each report is a self-contained, source-graded business analysis produced with a disciplined, AI-assisted two-stage pipeline (retrieve → reconcile & build). Reports are **sticky** (a stable URL always shows the latest version) and **versioned** (full history in git commits, tags, and releases).

## Layout

```
reports/      Published, web-facing reports. The website reads only this.
  <slug>/     One folder per report series; the folder name is the URL slug.
    report.md     The current report (always the latest).
    meta.json     Title, summary, status, dates, version, tags.
    assets/       Charts and images for this report.

pipeline/     How each report is made. Not published.
  <slug>/
    index.md      Living registry: artifacts, decisions, open questions.
    data/         Structured data. ledger.csv is the reconciliation master.
    method/       Repeatable procedures: retrieval.md, build.md.
    sources/      Raw source material, download scripts, guidance notes.

reports.json  Master index of all series (the site's landing-page feed).
```

## Reports

| Series | Slug | Status |
|---|---|---|
| Singapore Banks — Core Tables (DBS · OCBC · UOB) | `sg-banks` | Published |

## Adding a new report

1. Create `reports/<slug>/` with `report.md`, `meta.json`, and an `assets/` folder.
2. Create `pipeline/<slug>/` with `index.md`, `data/`, `method/`, and `sources/`.
3. Add the series to `reports.json`.
4. Commit, then tag the version: `git tag <slug>-v<YYYY.MM>`.

## Versioning

`report.md` is overwritten in place, so its URL never changes. History lives in git: `git log`, `git blame`, tags (`<slug>-v<YYYY.MM>`), and GitHub Releases for public, dated milestones.

## Conventions

Slugs and filenames are lowercase-hyphenated and permanent — never rename a published slug, it breaks links and bookmarks. Files are named for what they contain, not their format. Figures stay in the report's stated currency; sources are Tier-1 filings; no estimates or memory-fills.
