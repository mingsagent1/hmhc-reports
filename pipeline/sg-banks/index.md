# SGBanks — Project Index & Artifact Registry

> **Project:** Singapore Bank Stock Accumulation Strategy · **Index updated:** 2026-07-20 SGT
> This is the **single, living registry** — always current, overwritten in place. Start here to find the latest of anything. **Version history lives in git** (commits, tags, blame); there are no timestamped filenames or `archive/` folder.

The project is built as a **modular pipeline**: each module has one instruction file in `method/`, explicit inputs, exactly one output artifact, and is **idempotent** (rerun overwrites its output; git retains history). The one deliberate exception is **Style**, a static spec consumed by other modules (see registry).

---

## Pipeline dependency graph

```
                 ┌─────────────┐
                 │    Frame     │  method/frame.md → frame.md
                 └──────┬───────┘
            ┌───────────┴───────────┐
            ▼                       ▼
   ┌────────────────┐      ┌────────────────┐
   │    Retrieve    │      │      Scan      │        (run in parallel)
   │ method/        │      │ method/scan.md │
   │  retrieval.md  │      │ → data/        │
   │ → data/        │      │   signals.md   │
   │   ledger.csv   │      └───────┬────────┘
   └───────┬────────┘              │
           └──────────┬───────────┘
                      ▼
        [ Reconcile — human/Claude step ]     fills reconciled_* in ledger.csv
                      │                        (no separate output artifact)
                      ▼
              ┌───────────────┐        ┌───────────────┐
              │    Tables     │◀──────│     Style      │  method/style.md
              │ method/        │  spec  │ (consumed spec │
              │  build-tables. │        │  — no output)  │
              │  md → data/    │        └──────┬────────┘
              │  tables.md     │               │ spec
              └───────┬────────┘               │
                      ▼                         ▼
              ┌───────────────────────────────────────┐
              │              Assemble                   │  method/build.md
              │ consumes frame + tables + signals+style │  → reports/sg-banks/report.md
              └───────────────────┬─────────────────────┘
                                  ▼
                        ┌──────────────────┐
                        │   Exec Summary    │  method/execsummary.md
                        │ (closed-book,     │  → reports/sg-banks/execsummary.md
                        │  report only)     │
                        └────────┬──────────┘
                                 ▼
                        ┌──────────────────┐
                        │ Publish / Lineage │  method/publish.md
                        └──────────────────┘  → reports/sg-banks/meta.json
```

Flow: **Frame → (Retrieve ‖ Scan) → [Reconcile] → Tables → Assemble → Exec Summary → Publish**, with **Style** feeding Tables and Assemble.

---

## Repo layout

The repo separates **published, web-facing** output from **working pipeline** files. Each report series has its own slug folder.

```
reports/sg-banks/
  report.md       Published report (Assemble output).
  execsummary.md  Executive summary (Exec Summary output).
  meta.json       Metadata + pipeline lineage (Publish output).
  assets/         Charts and images for this report.

pipeline/sg-banks/
  index.md        This registry.
  frame.md        Framing artifact (Frame output): thesis, questions, rubric.
  data/
    ledger.csv    Reconciliation master (schema v0.2) — Retrieve output.
    signals.md    Qualitative signals (Scan output) — currently a scaffold.
    tables.md     Generated table blocks (Build-Tables output).
  method/
    frame.md        SOP — Frame.
    retrieval.md    SOP — Retrieve.
    scan.md         SOP — Scan.
    build-tables.md SOP — Build-Tables (deterministic table generation).
    build.md        SOP — Assemble (report composition).
    execsummary.md  SOP — Exec Summary (closed-book Top-10).
    style.md        Spec — Style (consumed by Tables & Assemble; no output).
    publish.md      SOP — Publish / Lineage.
  sources/        Raw source material, download scripts, guidance notes.
```

- **File names are permanent and describe content, not format.** No timestamps in filenames — git is the version-control system (`git log`, `git blame`, `git show <sha>:<file>`). Files are overwritten in place; git keeps the history.
- **`pipeline/sg-banks/index.md`** (this file) is the living registry — the human-readable pointer to the current artifacts.

## Versioning & history (git-native)

- **Every change is a commit.** No `v0.x` suffixes, no timestamped copies, no `archive/` folder — superseded content is recoverable from git history.
- To see what changed: `git log --oneline <file>` and `git show <sha>`. To restore: `git checkout <sha> -- <file>`.
- Tag milestone states (e.g. `git tag coretables-reconciled-260716`) when a component reaches a clean reconciled state.
- **Provenance still lives inside the files** (ledger `px_version`/`cl_version` stamps, SOP changelogs) as a second, in-band record.

---

## Module registry — current

| Module | Method file | Inputs | Sole output | Status / model |
|---|---|---|---|---|
| **Frame** | `method/frame.md` | registry + project brief | `frame.md` | **Materialized** 2026-07-20 · reasoning model (no search) |
| **Retrieve** | `method/retrieval.md` | ledger skeleton + Tier-1/2 sources | `data/ledger.csv` | **Reconciled** — 536 rows; px+cl+CASA passes · GPT-5.6 / non-Claude search-grounded |
| **Scan** | `method/scan.md` | `frame.md` + live Tier-1/2 sources | `data/signals.md` | **Scaffold — NOT run** · GPT-5.6 / search-grounded |
| **Reconcile** | *(human/Claude step; see `build-tables.md`)* | filled `ledger.csv` | *(fills `reconciled_*` in ledger — no separate artifact)* | **Done** for current ledger |
| **Tables** | `method/build-tables.md` | reconciled `ledger.csv` + `style.md` | `data/tables.md` | **Materialized** 2026-07-20 from current report · deterministic (code) |
| **Assemble** | `method/build.md` | `frame.md` + `tables.md` + `signals.md` + `style.md` | `reports/sg-banks/report.md` | **Built** — all Phase-1 gates pass · writing model (no search) |
| **Exec Summary** | `method/execsummary.md` | `report.md` only (closed-book) | `reports/sg-banks/execsummary.md` | **Built** — 10 insights · GPT-5.6 primary / Claude 4.8 alt; never search |
| **Style** | `method/style.md` | *(none — static spec)* | *(none — consumed by Tables & Assemble)* | **Spec** — controlled one-output exception |
| **Publish** | `method/publish.md` | published artifacts + method paths + version | `reports/sg-banks/meta.json` | **Current** — lineage object added 2026-07-20 |

### Artifact statuses
- `frame.md` — materialized (living doc, revisited each version).
- `data/ledger.csv` — reconciled; 536 rows (261 match · 120 single-px · 67 single-cl · 61 resolved · 16 n/d · 8 n/r · 3 text/other).
- `data/signals.md` — **scaffold only; Scan has not been run.** The current report is assembled from Tables alone; Assemble marks (does not invent) signal-dependent narrative.
- `data/tables.md` — **materialized 2026-07-20 from the current published report** (values copied verbatim, not altered). A future clean Build-Tables run will overwrite it from the ledger and should reproduce these values.
- `reports/sg-banks/report.md` — built; all Phase-1 gates pass (tie-out, canary, poison-pills, continuity). **Unchanged by this refactor.**
- `reports/sg-banks/execsummary.md` — built (Top-10). **Unchanged by this refactor.**
- `reports/sg-banks/meta.json` — lineage `pipeline` object added; published report version preserved (`2026.07`).

## Ledger schema (v0.2)
`data_point_id · bank · metric · period · unit · checksum_expected · checksum_note · px_value/source/comment/version · cl_value/source/comment/version · reconciled_value/status/note`. Provenance stamp format: `YYMMDD-NNN <Harness><Model>` (e.g. `20260716-001 PxClOpus4.8`, `20260716-002 CwClOpus4.8`).

## Standing analytical decisions
- **Asset-attraction proxy:** customer **deposits = primary** · **CASA % = quality overlay** · **wealth AUM = FY2019+ overlay** · **total assets = leverage only**.
- **UOB profit:** reported (attributable) headline, core in footnote.
- **Marking:** report tables carry numbers / `n/r` / `n/d` only; derived cells unmarked (per-table formula footnote); citations as superscripts. (Formalized in `method/style.md`.)

## Open questions (carry forward)
- **Scan not yet run** — the qualitative signal layer (`data/signals.md`) is scaffolded but empty; a future version should run Scan (search-grounded) and fold dated Tier-1/2 signals into Assemble.
- **Tables snapshot provenance** — `data/tables.md` was materialized from the current report, not from a fresh Build-Tables run against the ledger. Reconcile the two on the next full rebuild.
- **`TotalAssets` "net"** — defined as consolidated total assets; confirm if narrower.
- **Un-cross-checked cells** — `CustomerDeposits` (30), `TotalAssets` (30), `WealthAUM` (26) are currently **`single-px`** (Perplexity-only, no `cl` confirmation); other un-checksummed cells (SORA/current prices) are model-correlated (both runs Claude Opus 4.8) or single-source. Spot-verify vs Tier-1 or run a **non-Claude** retriever before the Assemble stage consumes them.
- **OCBC 2016–2018 CASA** — filled 2026-07-16 from OCBC FY-results presentations (Tier-1, GPT-5.5 non-Claude pass, computer-verified): 51.1 / 49.2 / 46.4. Currently `single-px` pending a second retriever pass. **OCBC AUM 2016–2017** — still `n/d` (not disclosed in that vintage of results decks).

## Changelog
- **2026-07-20 (modular pipeline)** — Refactored the two-stage (retrieve → reconcile+build) process into an **8-module pipeline**: Frame · Retrieve · Scan · Tables · Assemble · Exec Summary · Style · Publish. Added `method/frame.md`+`frame.md`, `method/scan.md`+`data/signals.md` (scaffold), `method/style.md`, `method/publish.md`, `method/execsummary.md`; split table generation out of `build.md` into `method/build-tables.md` → `data/tables.md` (snapshot materialized from the current report); refactored `build.md` into Assemble-only; normalized the module contract in `retrieval.md`; added the `pipeline` lineage object to `meta.json`. **No report/ledger/execsummary values changed.** Scan is scaffolded (not run); `data/tables.md` is a verbatim snapshot of the current report's tables.
- **2026-07-16 (casa-fill)** — Filled OCBC CASA 2016 / 2017 / 2018 (51.1% / 49.2% / 46.4%) from OCBC FY-results presentations via a **GPT-5.5 non-Claude retrieval pass** (Perplexity `research` subagent), then computer-verified each figure against the source PDF. Rows re-classified `n/r` → `single-px` and tagged `2026-07-16-run003 (GPT-5.5 non-Claude cross-check)` in `px_version`. Ledger status now (re-audited from CSV): **261 match · 120 single-px · 67 single-cl · 61 resolved · 16 n/d · 8 n/r · 3 text/other = 536 rows.** (Prior registry line "307 match" was carrying a stale pre-audit count and is corrected here.)
- **2026-07-16 (report)** — Built `reports/sg-banks/report.md` from the reconciled ledger per `pipeline/sg-banks/method/build.md`: Tables 1 (income engines + CAGRs), 1b (deposits & CASA), 1c (wealth AUM), 2 (NIM & NII), 3 (valuation/returns + P/TB block), 4 (NIM vs rate cycle), the Other-income breakdown, the deposits+CASA benchmark note, and Appendices A–C (validation, definitions, restatements). Phase-1 gates all pass: NII+NonII=TotalIncome exact for all 30 bank-years, DBS NIM canary 2.01, no poison pills, all >30% YoY moves explained.
- **2026-07-16 (later)** — **Went git-native:** dropped timestamped filenames, the `v0.x` scheme, and the `claude/`+`archive/` retention process — git commits/tags now carry version history. Registry uses the plain filenames as committed. **Reconciliation audit fix:** 46 rows mislabeled `match` (where `px≠cl` or `reconciled≠checksum`) re-classified to `resolved` with a cause note each (rounding / SFRS(I) 17 restatement B6 / Citi uplift B4 / UOB FY2025 provisioning artefact B5 / price-date). **Metric-name fix:** 2026-latest rate rows re-keyed `EFFR→EFFRavg`, `SORA→SORA_YE` for series consistency.
- **2026-07-16 (earlier)** — Tables component built: split monolithic brief into SOPRetrieval + Ledger + SOPReport; Perplexity retrieval + Claude reconciliation. Ledger status after this run: **307 match · 117 single-px · 67 single-cl · 15 resolved · 16 n/d · 11 n/r · 3 text/other** (536 rows). Added version/provenance columns; added Attracted-assets (deposits & CASA) + Wealth-AUM overlay + "why deposits+CASA" rationale.
