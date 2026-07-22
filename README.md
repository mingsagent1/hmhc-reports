# HMHC Reports

Source of record for the analyst reports published at **[reports.hmhc.ai](https://reports.hmhc.ai)**.

Each report is a self-contained, source-graded business analysis produced with a disciplined, AI-assisted **modular pipeline**. Reports are **sticky** (a stable URL always shows the latest version) and **versioned** (full history in git commits, tags, and releases).

## Layout

```
reports/      Published, web-facing reports. The website reads only this.
  <slug>/     One folder per report series; the folder name is the URL slug.
    report.md       The current report (always the latest); its Conclusions section
                    lives inside it, between regeneration markers.
    meta.json       Title, summary, status, dates, version, pipeline lineage.
    assets/         Charts and images for this report.

pipeline/     How each report is made. Not published.
  <slug>/
    UPDATE.md       Controller — the single entrypoint for any change, and the
                    single source of truth for modules, method files, and costs.
    index.md        Living registry of state: artifact statuses, standing
                    decisions, open questions, changelog.
    guides/         Human-owned: frame.md (thesis + key questions the report
                    must answer) and style.md (formatting & marking rules).
    method/         One instruction file per module, named <verb>-<artifact>.md;
      ai/           steps performed by AI models (fetch-, reconcile-, write-, build-).
      code/         steps performed by deterministic programs (build_tables.py) — no AI.
    data/           Working data: ledger.csv (reconciliation master),
                    signals.md (qualitative signals), tables.md (generated tables).

reports.json  Master index of all series (the site's landing-page feed).
```

## Pipeline

The flow is linear: **Frame (human guide) → Fetch-Ledger ‖ Fetch-Signals → Reconcile → Build-Tables → Build-Report → Write-Conclusions → Publish**, with the human-owned **Style** guide consumed by Build-Tables and Build-Report. The method **verb is the execution category**: `fetch-` = live web (expensive, opt-in) · `reconcile-` = human+AI cross-check · `build-` = assembly · `write-` = insight/synthesis; `method/ai/` steps run on AI models, `method/code/` steps are deterministic programs. Every module has one SOP in `method/`, explicit inputs, one output, and is **idempotent** (rerunning overwrites its output; git retains history).

The module table — method files, outputs, costs, dependencies, and the cost gates for the two **expensive** `fetch-` modules (live web retrieval, opt-in only) — lives in **`pipeline/<slug>/UPDATE.md`**, the controller every change must route through. Do not duplicate it here.

## Reports

| Series | Slug | Status |
|---|---|---|
| Singapore Banks — Core Tables (DBS · OCBC · UOB) | `sg-banks` | Published |

## Adding a new report

1. Create `reports/<slug>/` with `report.md`, `meta.json`, and an `assets/` folder.
2. Create `pipeline/<slug>/` with `UPDATE.md`, `index.md`, `guides/` (`frame.md`, `style.md`), `method/` (the module SOPs), and `data/`.
3. Add the series to `reports.json`.
4. Commit, then tag the version: `git tag <slug>-v<version>`.

## Versioning

`report.md` is overwritten in place, so its URL never changes. History lives in git: `git log`, `git blame`, tags, and GitHub Releases for public, dated milestones. Versions are `YYYY.MM.DD` of the publish date; a same-day re-release appends `-r2`, `-r3`, … (e.g. `sg-banks-v2026.07.20-r2`).

## Conventions

Slugs and filenames are lowercase-hyphenated and permanent — never rename a published slug, it breaks links and bookmarks. Files are named for what they contain, not their format. Figures stay in the report's stated currency; sources are Tier-1 filings; no estimates or memory-fills. AI agents start at `AGENTS.md`; every AI commit carries the attribution trailers defined there.
