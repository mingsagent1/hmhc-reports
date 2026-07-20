# HMHC Reports

Source of record for the analyst reports published at **[reports.hmhc.ai](https://reports.hmhc.ai)**.

Each report is a self-contained, source-graded business analysis produced with a disciplined, AI-assisted **modular pipeline** (Frame → Retrieve + Scan → Tables → Assemble → Exec Summary → Publish, with Style consumed by Tables and Assemble). Reports are **sticky** (a stable URL always shows the latest version) and **versioned** (full history in git commits, tags, and releases).

## Layout

```
reports/      Published, web-facing reports. The website reads only this.
  <slug>/     One folder per report series; the folder name is the URL slug.
    report.md       The current report (always the latest).
    execsummary.md  Executive summary (top-10 insights), linked from meta.json.
    meta.json       Title, summary, status, dates, version, tags, pipeline lineage.
    assets/         Charts and images for this report.

pipeline/     How each report is made. Not published.
  <slug>/
    index.md        Living registry: dependency graph, module registry, decisions, open questions.
    frame.md        Framing artifact: thesis, key questions, good-vs-bad rubric.
    data/           Structured data.
      ledger.csv    Reconciliation master (Retrieve output).
      signals.md    Qualitative signals (Scan output).
      tables.md     Generated table blocks (Build-Tables output).
    method/         One instruction file per module (see the pipeline below).
    sources/        Raw source material, download scripts, guidance notes.

reports.json  Master index of all series (the site's landing-page feed).
```

## Pipeline

Every module has one instruction file in `method/`, explicit inputs, exactly one output artifact, and is **idempotent** (rerunning overwrites its output; git retains history).

| Module | Instruction file | Sole output |
|---|---|---|
| **Frame** — thesis, key questions, good-vs-bad rubric (living doc) | `method/frame.md` | `frame.md` |
| **Retrieve** — fill the raw-data ledger from Tier-1 sources | `method/retrieval.md` | `data/ledger.csv` |
| **Scan** — dated, sourced qualitative signals (recency-biased) | `method/scan.md` | `data/signals.md` |
| **Tables** — deterministic table generation from the reconciled ledger | `method/build-tables.md` | `data/tables.md` |
| **Assemble** — compose the published report from all inputs | `method/build.md` | `report.md` |
| **Exec Summary** — closed-book top-10 insights from the report only | `method/execsummary.md` | `execsummary.md` |
| **Style** — marking/format/tone spec (a *consumed spec*, no output) | `method/style.md` | *(consumed by Tables & Assemble)* |
| **Publish / Lineage** — metadata + lineage map | `method/publish.md` | `meta.json` |

**Reconciliation** — comparing the retrievers' ledger columns against each other and the embedded checksums into `reconciled_value` — is the human/Claude step **between** Retrieve/Scan and Tables. It fills the ledger's `reconciled_*` columns and has no separate output artifact.

**Style** is the one deliberate exception to the one-output-per-module rule: it is a static specification consumed by Tables and Assemble rather than an executable step, so it emits no artifact of its own.

## Reports

| Series | Slug | Status |
|---|---|---|
| Singapore Banks — Core Tables (DBS · OCBC · UOB) | `sg-banks` | Published |

## Adding a new report

1. Create `reports/<slug>/` with `report.md`, `execsummary.md`, `meta.json`, and an `assets/` folder.
2. Create `pipeline/<slug>/` with `index.md`, `frame.md`, `data/`, `method/` (the module instruction files above), and `sources/`.
3. Add the series to `reports.json`.
4. Commit, then tag the version: `git tag <slug>-v<YYYY.MM>`.

## Versioning

`report.md` is overwritten in place, so its URL never changes. History lives in git: `git log`, `git blame`, tags (`<slug>-v<YYYY.MM>`), and GitHub Releases for public, dated milestones.

## Conventions

Slugs and filenames are lowercase-hyphenated and permanent — never rename a published slug, it breaks links and bookmarks. Files are named for what they contain, not their format. Figures stay in the report's stated currency; sources are Tier-1 filings; no estimates or memory-fills.
