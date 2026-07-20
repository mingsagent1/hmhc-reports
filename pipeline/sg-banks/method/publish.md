# Publish / Lineage — Module SOP (SG Banks)

> **Project:** Singapore Bank Stock Accumulation Strategy
> **Artifact:** `pipeline/sg-banks/method/publish.md` — version history in git (`git log --oneline pipeline/sg-banks/method/publish.md`).
> **Status:** Draft.

## Module contract

| | |
|---|---|
| **Inputs** | All published artifacts (`reports/sg-banks/report.md`, `reports/sg-banks/execsummary.md`), the pipeline method/artifact paths (every file under `pipeline/sg-banks/`), and the intended version string. |
| **Sole output** | `reports/sg-banks/meta.json` — the published metadata + pipeline lineage. |
| **Idempotence** | A rerun overwrites `reports/sg-banks/meta.json` in place. Git retains history. |
| **Recommended model** | Any capable model; this is a bookkeeping/serialization step. Deterministic — no search, no memory-fills. |
| **Position** | Final module: `… → Exec Summary → Publish`. Publish runs last, after the report and exec summary are finished. |

## What Publish is for

Publish is the **lineage keeper**. It records, in `meta.json`, the published metadata (title/summary/status/dates/version/tags), the link to the executive summary, and a machine-readable map of **which method file produced which artifact** for every module in the pipeline. It is how a reader (or the website) can answer "what version is this, and how was each piece made?" without reading every SOP.

**Publish never alters report content.** It touches only `meta.json`. If the report body needs to change, that is Assemble's job, not Publish's.

## How to run this module

1. **Read the published artifacts** to confirm they exist and are current: `reports/sg-banks/report.md`, `reports/sg-banks/execsummary.md`.
2. **Preserve all existing `meta.json` fields** — `slug`, `title`, `subtitle`, `summary`, `status`, `first_published`, `last_updated`, `current_version`, `tags`, and **`executive_summary`** (the link to the exec summary). Do not drop or rename any of these.
3. **Update / maintain the `pipeline` lineage object** (top-level). It maps each module to its method file and sole output, using **repo-root-relative paths** consistently. Cover: `frame`, `retrieve`, `scan`, `tables`, `assemble`, `exec_summary`, `style`, `publish`.
   - For each **executable** module include its `method` path and its `output` path.
   - For **`style`** (the consumed spec with no output — see `method/style.md`) include its `method` path and a `consumed_by` list, **not** an `output`.
4. **Set dates/version deliberately.** Update `last_updated` and `current_version` **only when the published report content actually changed**. Do **not** bump the report version or `last_updated` solely because architecture/lineage docs changed — prefer preserving the published report version. Record an `architecture_updated` date under `pipeline` if you want to stamp a docs-only change.
5. **Validate the JSON** (`python -m json.tool reports/sg-banks/meta.json` or equivalent) before committing. It must remain valid JSON.
6. **Verify paths.** Every `method` / `output` / `consumed_by` path in the lineage must point to a file that exists in the repo.
7. Overwrite `reports/sg-banks/meta.json`. Commit.

## Acceptance criteria (stop when all true)
- All pre-existing `meta.json` fields preserved, including `executive_summary`.
- Top-level `pipeline` lineage covers all eight modules; executable modules have `method` + `output`; Style has `method` + `consumed_by`.
- All paths are repo-root-relative and resolve to real files.
- JSON is valid.
- Report version / `last_updated` unchanged unless the report content itself changed.
