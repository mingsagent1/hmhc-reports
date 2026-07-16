# SGBanks — Project Index & Artifact Registry

> **Project:** Singapore Bank Stock Accumulation Strategy · **Index updated:** 2026-07-16 SGT
> This is the **single, living registry** — always current, overwritten in place. Start here to find the latest of anything. **Version history lives in git** (commits, tags, blame); there are no timestamped filenames or `archive/` folder.

The project is built as **components** (self-contained analyses). Each component runs a **two-stage pipeline**: retrieve raw data into a shared ledger → reconcile + build the report.

---

## Naming convention

```
SGBanks_<Component>_<Type>.<ext>
```

- **`<Component>`** — the analysis unit. Current: `Tables` (income engines · attracted assets · NIM · valuation/returns · rate cycle). Future: `Capital`, `CreditQuality`, `Dividend`, `Peers`, …
- **`<Type>`** — `SOPRetrieval` · `Ledger` · `SOPReport` · `Report`.
- **No timestamps in filenames.** Git is the version-control system: use commits/tags to find or restore any prior state (`git log`, `git blame`, `git show <sha>:<file>`). Files are overwritten in place; git keeps the history.
- **`SGBanks_Index.md`** (this file) is the living registry — the human-readable pointer to the current artifacts.

## Versioning & history (git-native)

- **Every change is a commit.** No `v0.x` suffixes, no timestamped copies, no `archive/` folder — superseded content is recoverable from git history.
- To see what changed: `git log --oneline <file>` and `git show <sha>`. To restore: `git checkout <sha> -- <file>`.
- Tag milestone states (e.g. `git tag coretables-reconciled-260716`) when a component reaches a clean reconciled state.
- **Provenance still lives inside the files** (ledger `px_version`/`cl_version` stamps, SOP changelogs) as a second, in-band record.

---

## Registry — current

### Component: `Tables` (income engines · attracted assets · NIM · valuation/returns · rate cycle)

| Artifact | File | Status |
|---|---|---|
| Retrieval SOP | `SGBanks_Tables_SOPRetrieval.md` | Draft |
| Ledger (schema v0.2) | `SGBanks_Tables_Ledger.csv` | Reconciled — px (Perplexity) + cl (Claude) + CASA pass; 536 rows |
| Report-build SOP | `SGBanks_Tables_SOPReport.md` | Draft |
| Report (output) | `SGBanks_Tables_Report.md` | Built — all Phase-1 gates pass (tie-out, canary, poison-pills, continuity) |

---

## Pipeline (how a component is produced)
1. **Retrieve** — each agent fills its columns in the `Ledger` per the `SOPRetrieval` (raw numbers only, no calcs).
2. **Reconcile** — Claude compares agents' values vs each other and the embedded checksums, resolving mismatches (never averaging) into `reconciled_value`.
3. **Build** — Claude builds the `Report` from reconciled values per the `SOPReport`.
4. **Version** — commit the change to git with a descriptive message; update this Index; tag milestone states as needed.

## Ledger schema (v0.2)
`data_point_id · bank · metric · period · unit · checksum_expected · checksum_note · px_value/source/comment/version · cl_value/source/comment/version · reconciled_value/status/note`. Provenance stamp format: `YYMMDD-NNN <Harness><Model>` (e.g. `20260716-001 PxClOpus4.8`, `20260716-002 CwClOpus4.8`).

## Standing analytical decisions
- **Asset-attraction proxy:** customer **deposits = primary** · **CASA % = quality overlay** · **wealth AUM = FY2019+ overlay** · **total assets = leverage only**.
- **UOB profit:** reported (attributable) headline, core in footnote.
- **Marking:** report tables carry numbers / `n/r` / `n/d` only; derived cells unmarked (per-table formula footnote); citations as superscripts.

## Open decisions (carry forward)
- **`TotalAssets` "net"** — defined as consolidated total assets; confirm if narrower.
- **Un-cross-checked cells** — `CustomerDeposits` (30), `TotalAssets` (30), `WealthAUM` (26) are currently **`single-px`** (Perplexity-only, no `cl` confirmation); other un-checksummed cells (SORA/current prices) are model-correlated (both runs Claude Opus 4.8) or single-source. Spot-verify vs Tier-1 or run a **non-Claude** retriever before the Report stage consumes them.
- **OCBC 2016–2018 CASA** — filled 2026-07-16 from OCBC FY-results presentations (Tier-1, GPT-5.5 non-Claude pass, computer-verified): 51.1 / 49.2 / 46.4. Currently `single-px` pending a second retriever pass. **OCBC AUM 2016–2017** — still `n/d` (not disclosed in that vintage of results decks).

## Changelog
- **2026-07-16 (casa-fill)** — Filled OCBC CASA 2016 / 2017 / 2018 (51.1% / 49.2% / 46.4%) from OCBC FY-results presentations via a **GPT-5.5 non-Claude retrieval pass** (Perplexity `research` subagent), then computer-verified each figure against the source PDF. Rows re-classified `n/r` → `single-px` and tagged `2026-07-16-run003 (GPT-5.5 non-Claude cross-check)` in `px_version`. Ledger status now (re-audited from CSV): **261 match · 120 single-px · 67 single-cl · 61 resolved · 16 n/d · 8 n/r · 3 text/other = 536 rows.** (Prior registry line "307 match" was carrying a stale pre-audit count and is corrected here.)
- **2026-07-16 (report)** — Built `SGBanks_Tables_Report.md` from the reconciled ledger per SOPReport: Tables 1 (income engines + CAGRs), 1b (deposits & CASA), 1c (wealth AUM), 2 (NIM & NII), 3 (valuation/returns + P/TB block), 4 (NIM vs rate cycle), the Other-income breakdown, the deposits+CASA benchmark note, and Appendices A–C (validation, definitions, restatements). Phase-1 gates all pass: NII+NonII=TotalIncome exact for all 30 bank-years, DBS NIM canary 2.01, no poison pills, all >30% YoY moves explained.
- **2026-07-16 (later)** — **Went git-native:** dropped timestamped filenames, the `v0.x` scheme, and the `claude/`+`archive/` retention process — git commits/tags now carry version history. Registry uses the plain `SGBanks_Tables_*` filenames as committed. **Reconciliation audit fix:** 46 rows mislabeled `match` (where `px≠cl` or `reconciled≠checksum`) re-classified to `resolved` with a cause note each (rounding / SFRS(I) 17 restatement B6 / Citi uplift B4 / UOB FY2025 provisioning artefact B5 / price-date). **Metric-name fix:** 2026-latest rate rows re-keyed `EFFR→EFFRavg`, `SORA→SORA_YE` for series consistency.
- **2026-07-16 (earlier)** — Tables component built: split monolithic brief into SOPRetrieval + Ledger + SOPReport; Perplexity retrieval + Claude reconciliation. Ledger status after this run: **307 match · 117 single-px · 67 single-cl · 15 resolved · 16 n/d · 11 n/r · 3 text/other** (536 rows). Added version/provenance columns; added Attracted-assets (deposits & CASA) + Wealth-AUM overlay + "why deposits+CASA" rationale.
