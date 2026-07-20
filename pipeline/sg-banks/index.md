# SGBanks — Project Index & Artifact Registry

> **Project:** Singapore Bank Stock Accumulation Strategy · **Index updated:** 2026-07-20 SGT (1Q2026 refresh)
> This is the **single, living registry** — always current, overwritten in place. Start here to find the latest of anything. **Version history lives in git** (commits, tags, blame); there are no timestamped filenames or `archive/` folder.
> **Current content version:** `2026.07.20` (1Q2026 update). **Executive summary regenerated** via a closed-book GPT-5.5 pass on the refreshed `report.md`.

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
| **Frame** | `method/frame.md` | registry + project brief | `frame.md` | **Refreshed** 2026-07-20 for 1Q2026 (rate-regime/fee-offset/credit lenses added) · reasoning model (no search) |
| **Retrieve** | `method/retrieval.md` | ledger skeleton + Tier-1/2 sources | `data/ledger.csv` | **Extended** 2026-07-20 — 582 rows incl. 49 Q1-2026 (single-cl); history unchanged |
| **Scan** | `method/scan.md` | `frame.md` + live Tier-1/2 sources | `data/signals.md` | **Run 2026-07-20** — 1Q2026 dated signal register (Tier-1/2 separated); transcribed from evidence set (Claude Opus 4.8, not live-searched) |
| **Reconcile** | *(human/Claude step; see `build-tables.md`)* | filled `ledger.csv` | *(fills `reconciled_*` in ledger — no separate artifact)* | **Done** for current ledger (incl. Q1-2026 tie-outs) |
| **Tables** | `method/build-tables.md` | reconciled `ledger.csv` + `style.md` | `data/tables.md` | **Refreshed** 2026-07-20 — added 1Q2026 snapshot + updated current valuation; history verbatim |
| **Assemble** | `method/build.md` | `frame.md` + `tables.md` + `signals.md` + `style.md` | `reports/sg-banks/report.md` | **Rebuilt** 2026-07-20 — added 1Q2026 Update section; Phase-1 gates + 1Q26 tie-outs pass |
| **Exec Summary** | `method/execsummary.md` | `report.md` only (closed-book) | `reports/sg-banks/execsummary.md` | **Regenerated** 2026-07-20 — closed-book GPT-5.5 pass on refreshed `report.md`; 10 ranked insights (3 pos / 4 neg / 3 mixed) |
| **Style** | `method/style.md` | *(none — static spec)* | *(none — consumed by Tables & Assemble)* | **Spec** — controlled one-output exception |
| **Publish** | `method/publish.md` | published artifacts + method paths + version | `reports/sg-banks/meta.json` | **Updated** 2026-07-20 — version `2026.07.20`, refresh note + exec-summary-pending flag |

### Artifact statuses
- `frame.md` — **refreshed 2026-07-20** for the 1Q2026 update (added the rate-regime test, fee/wealth offset, credit/provision risk, valuation and latest-guidance lenses; two new key questions). Living doc.
- `data/ledger.csv` — **extended 2026-07-20**; 582 data rows (261 match · 119 single-px · 116 single-cl · 58 resolved · 17 n/d · 8 n/r · 3 text/other). 49 rows are Q1-2026 (46 new metrics + 3 pre-existing NIMgroup). FY2016–FY2025 values unchanged; 1Q2026 rows are `single-cl` (stamp `20260720-001 CwClOpus4.8`).
- `data/signals.md` — **Scan run 2026-07-20**; populated with a dated 1Q2026 Tier-1/Tier-2 signal register (≥3 positive / ≥3 negative per bank), grounded in the evidence set and folded into Assemble.
- `data/tables.md` — **refreshed 2026-07-20**: prepended a *Latest 1Q2026 snapshot* section; updated Table 4 Current-P/B rows, the P/TB current column, and the Table 5 2026-latest row (1Q26 NIM + rates); historical blocks verbatim.
- `reports/sg-banks/report.md` — **rebuilt 2026-07-20** with a prominent *1Q2026 Update* section (income/attraction/valuation tables, guidance, signal synthesis, comparability + retrieval-limitation notes, inline evidence URLs). FY2016–FY2025 tables unchanged. Phase-1 gates and 1Q26 tie-outs pass.
- `reports/sg-banks/execsummary.md` — **Regenerated 2026-07-20** via a closed-book GPT-5.5 pass on the refreshed `report.md`; 10 ranked insights (tally: 3 positive · 4 negative · 3 mixed), scope line `v2026.07.20`.
- `reports/sg-banks/meta.json` — `last_updated` `2026-07-20`, `current_version` `2026.07.20`; `first_published` (2026-07-16) and pipeline lineage preserved; `executive_summary_status` cleared to reflect the regenerated closed-book summary.

## Ledger schema (v0.2)
`data_point_id · bank · metric · period · unit · checksum_expected · checksum_note · px_value/source/comment/version · cl_value/source/comment/version · reconciled_value/status/note`. Provenance stamp format: `YYMMDD-NNN <Harness><Model>` (e.g. `20260716-001 PxClOpus4.8`, `20260716-002 CwClOpus4.8`).

## Standing analytical decisions
- **Asset-attraction proxy:** customer **deposits = primary** · **CASA % = quality overlay** · **wealth AUM = FY2019+ overlay** · **total assets = leverage only**.
- **UOB profit:** reported (attributable) headline, core in footnote.
- **Marking:** report tables carry numbers / `n/r` / `n/d` only; derived cells unmarked (per-table formula footnote); citations as superscripts. (Formalized in `method/style.md`.)

## Open questions (carry forward)
- **1Q2026 block is single-retriever** — all 49 Q1-2026 ledger rows are `single-cl` (one Claude pass from the evidence set, stamp `20260720-001 CwClOpus4.8`); not yet dual-checked. **UOB 1Q26 income-statement detail is Tier-2 host** (CFO/CEO slides via MarketScreener); re-pull UOB's own PDFs and run a non-Claude confirmation before high-stakes use.
- **UOB 1Q26 non-II components don't reconcile** — slide split (637+405+462=1,504) ≠ TI−NII (1,098); derived 1,098 used, split flagged. Resolve when UOB's own release is retrievable.
- **Official 3M SORA `n/d`** — MAS eServices statistics portal under maintenance 2026-07-20; interim ~1.07% is the bank-characterised 1Q26 average (DBS transcript). Re-fetch MAS before publishing a hard SORA number.
- **Tables snapshot provenance** — historical `data/tables.md` blocks are still a verbatim snapshot of the report, not a fresh Build-Tables run against the ledger. Reconcile on the next full rebuild.
- **`TotalAssets` "net"** — defined as consolidated total assets; confirm if narrower.
- **Un-cross-checked historical cells** — `CustomerDeposits`, `TotalAssets`, `WealthAUM` (FY history) remain `single-px` (Perplexity-only); other un-checksummed cells (SORA/current prices) are model-correlated or single-source. Spot-verify vs Tier-1 or run a **non-Claude** retriever.
- **OCBC 2016–2018 CASA** — filled 2026-07-16 from OCBC FY-results presentations (Tier-1, GPT-5.5 non-Claude pass, computer-verified): 51.1 / 49.2 / 46.4. Currently `single-px` pending a second retriever pass. **OCBC AUM 2016–2017** — still `n/d` (not disclosed in that vintage of results decks).

## Changelog
- **2026-07-20 (exec-summary refresh)** — Regenerated `reports/sg-banks/execsummary.md` via a **closed-book GPT-5.5 pass** on the refreshed `report.md` (v2026.07.20), per `method/execsummary.md`. 10 ranked insights, tally **3 positive · 4 negative · 3 mixed**, every item traced to a real report location and scope line naming `v2026.07.20`. Cleared the exec-summary pending flag/status in this registry and `meta.json`. **No Retrieve/Scan content, statuses, or data changed — `ledger.csv`, `signals.md`, `report.md`, and `tables.md` remain frozen from the 1Q2026 refresh commit.**
- **2026-07-20 (1Q2026 refresh)** — Refreshed the report for **1Q2026** (quarters ended 31 Mar 2026) + current (2026-07-20 intraday) valuation. **Frame** updated with rate-regime / fee-offset / credit-provision / valuation / guidance lenses and two new key questions. **Scan run for the first time** — `data/signals.md` populated with a dated Tier-1/Tier-2 1Q26 signal register (≥3 pos / ≥3 neg per bank), grounded in the fetched-URL evidence set. **Ledger** extended by 46 new Q1-2026 metric rows + 1 macro row (49 Q1-2026 rows total incl. 3 pre-existing NIMgroup), all `single-cl` (stamp `20260720-001 CwClOpus4.8`); PriceCurrent×3 updated to intraday 2026-07-20 (71.96/28.60/42.60), SORA_YE_2026 → `n/d` (MAS portal maintenance), NIMguidance×3 refreshed to primary FY26 guidance; **FY2016–FY2025 values unchanged**; row count 536 → 582. **Tables** gained a *Latest 1Q2026 snapshot* section and updated current-valuation cells (Current P/B DBS 2.96 / OCBC 2.14 / UOB 1.45; P/TB current 3.26 / 2.30 / 1.62) + 1Q26 NIM in the Table 5 latest row. **Report** rebuilt with a prominent *1Q2026 Update* section (income/attraction/valuation tables, dated guidance, signal synthesis, comparability + retrieval-limitation notes, inline evidence URLs). **meta.json** → version `2026.07.20`, `last_updated` 2026-07-20, refresh note + `executive_summary_status: pending`. Tie-outs: 1Q26 NII+NonII=TotalIncome exact for all three (DBS 5,948 · OCBC 3,828 · UOB 3,422); UOB non-II slide components (1,504) don't reconcile with derived 1,098 → flagged. **Executive summary was intentionally deferred in this refresh commit and regenerated in the follow-up closed-book pass** (see the exec-summary-refresh entry above).
- **2026-07-20 (modular pipeline)** — Refactored the two-stage (retrieve → reconcile+build) process into an **8-module pipeline**: Frame · Retrieve · Scan · Tables · Assemble · Exec Summary · Style · Publish. Added `method/frame.md`+`frame.md`, `method/scan.md`+`data/signals.md` (scaffold), `method/style.md`, `method/publish.md`, `method/execsummary.md`; split table generation out of `build.md` into `method/build-tables.md` → `data/tables.md` (snapshot materialized from the current report); refactored `build.md` into Assemble-only; normalized the module contract in `retrieval.md`; added the `pipeline` lineage object to `meta.json`. **No report/ledger/execsummary values changed.** Scan is scaffolded (not run); `data/tables.md` is a verbatim snapshot of the current report's tables.
- **2026-07-16 (casa-fill)** — Filled OCBC CASA 2016 / 2017 / 2018 (51.1% / 49.2% / 46.4%) from OCBC FY-results presentations via a **GPT-5.5 non-Claude retrieval pass** (Perplexity `research` subagent), then computer-verified each figure against the source PDF. Rows re-classified `n/r` → `single-px` and tagged `2026-07-16-run003 (GPT-5.5 non-Claude cross-check)` in `px_version`. Ledger status now (re-audited from CSV): **261 match · 120 single-px · 67 single-cl · 61 resolved · 16 n/d · 8 n/r · 3 text/other = 536 rows.** (Prior registry line "307 match" was carrying a stale pre-audit count and is corrected here.)
- **2026-07-16 (report)** — Built `reports/sg-banks/report.md` from the reconciled ledger per `pipeline/sg-banks/method/build.md`: Tables 1 (income engines + CAGRs), 1b (deposits & CASA), 1c (wealth AUM), 2 (NIM & NII), 3 (valuation/returns + P/TB block), 4 (NIM vs rate cycle), the Other-income breakdown, the deposits+CASA benchmark note, and Appendices A–C (validation, definitions, restatements). Phase-1 gates all pass: NII+NonII=TotalIncome exact for all 30 bank-years, DBS NIM canary 2.01, no poison pills, all >30% YoY moves explained.
- **2026-07-16 (later)** — **Went git-native:** dropped timestamped filenames, the `v0.x` scheme, and the `claude/`+`archive/` retention process — git commits/tags now carry version history. Registry uses the plain filenames as committed. **Reconciliation audit fix:** 46 rows mislabeled `match` (where `px≠cl` or `reconciled≠checksum`) re-classified to `resolved` with a cause note each (rounding / SFRS(I) 17 restatement B6 / Citi uplift B4 / UOB FY2025 provisioning artefact B5 / price-date). **Metric-name fix:** 2026-latest rate rows re-keyed `EFFR→EFFRavg`, `SORA→SORA_YE` for series consistency.
- **2026-07-16 (earlier)** — Tables component built: split monolithic brief into SOPRetrieval + Ledger + SOPReport; Perplexity retrieval + Claude reconciliation. Ledger status after this run: **307 match · 117 single-px · 67 single-cl · 15 resolved · 16 n/d · 11 n/r · 3 text/other** (536 rows). Added version/provenance columns; added Attracted-assets (deposits & CASA) + Wealth-AUM overlay + "why deposits+CASA" rationale.
