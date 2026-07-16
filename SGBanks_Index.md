# SGBanks — Project Index & Artifact Registry

> **Project:** Singapore Bank Stock Accumulation Strategy · **Index updated:** 2026-07-16 16:12 SGT
> This is the **single, living registry** — always current, no timestamp, overwritten in place. Everything else is timestamped. Start here to find the latest of anything.

The project is built as **components** (self-contained analyses). Each component runs a **two-stage pipeline**: retrieve raw data into a shared ledger → reconcile + build the report.

---

## Naming convention

```
SGBanks_<Component>_<Type>_<YYMMDD-HHMMSS>.<ext>
```

- **`<YYMMDD-HHMMSS>`** — creation timestamp, **Asia/Singapore**. This is the version id: the largest timestamp is the newest. (We use timestamps, not `v0.1/v0.2` — easier to see at a glance what's new.)
- **`<Component>`** — the analysis unit. Current: `CoreTables`. Future: `Capital`, `CreditQuality`, `Dividend`, `Peers`, …
- **`<Type>`** — `SOP-Retrieval` · `Ledger` · `SOP-Report` · `Report`.
- **`SGBanks_Index.md`** (this file) is the **only** un-timestamped file — the living pointer to the current timestamps.

## Retention & archiving process (important)

- **`claude/` = your "Outputs" panel.** Only the **current** version of each artifact + this Index + source files live in `claude/`.
- **On every new version:** the new timestamped file is written to `claude/`, and the **previous** version is **moved to the top-level `archive/` folder (outside `claude/`)**, so it disappears from Outputs but is not lost.
- **No trash exists.** A hard delete is effectively permanent, so superseded files are **archived, not deleted**. Permanent removal of an archived file is left to you via the claude.ai project UI.
- **Provenance still lives inside the files** (ledger `px_version`/`cl_version` stamps, SOP changelogs), so history survives archiving.

---

## Registry — current (in `claude/`)

### Component: `CoreTables` (income engines · attracted assets · NIM · valuation/returns · rate cycle)

| Artifact | Current file | Status |
|---|---|---|
| Retrieval SOP | `SGBanks_CoreTables_SOP-Retrieval_260716-161218.md` | Draft |
| Ledger (schema v0.2) | `SGBanks_CoreTables_Ledger_260716-161218.csv` | Reconciled — px (Perplexity) + cl (Claude) + CASA pass; 536 rows |
| Report-build SOP | `SGBanks_CoreTables_SOP-Report_260716-161218.md` | Draft |
| Report (output) | *(not yet built)* | Pending |

### Source material (in `claude/`, keep)
- `download_sg_bank_reports.sh` · `sg-bank-reports-index.html` · `sg-banks-q1-2026-results-guidance.md`

### Archived (in top-level `archive/`, outside Outputs)
- `archive/SGBanks_CoreTables_Ledger_v0.1.csv` — blank schema-v0.1 template (superseded; kept as a fresh-start template).
- `archive/sg-banks-six-tables-FY2016-FY2025.md` — legacy report, old six-table layout (superseded; pending the CoreTables report).

> Note: files delivered into the chat earlier (via file attachments) may still linger in the Outputs history as a delivery log — those are separate from the project folder and can be dismissed in the UI. Going forward, timestamped names make the newest obvious, and files are delivered sparingly.

---

## Pipeline (how a component is produced)
1. **Retrieve** — each agent fills its columns in the `Ledger` per the `SOP-Retrieval` (raw numbers only, no calcs).
2. **Reconcile** — Claude compares agents' values vs each other and the embedded checksums, resolving mismatches (never averaging) into `reconciled_value`.
3. **Build** — Claude builds the `Report` from reconciled values per the `SOP-Report`.
4. **Version** — new timestamped output to `claude/`; prior version moved to `archive/`; this Index updated.

## Ledger schema (v0.2)
`data_point_id · bank · metric · period · unit · checksum_expected · checksum_note · px_value/source/comment/version · cl_value/source/comment/version · reconciled_value/status/note`. Provenance stamp format: `YYMMDD-NNN <Harness><Model>` (e.g. `20260716-001 PxClOpus4.8`, `20260716-002 CwClOpus4.8`).

## Standing analytical decisions
- **Asset-attraction proxy:** customer **deposits = primary** · **CASA % = quality overlay** · **wealth AUM = FY2019+ overlay** · **total assets = leverage only**.
- **UOB profit:** reported (attributable) headline, core in footnote.
- **Marking:** report tables carry numbers / `n/r` / `n/d` only; derived cells unmarked (per-table formula footnote); citations as superscripts.

## Open decisions (carry forward)
- **`TotalAssets` "net"** — defined as consolidated total assets; confirm if narrower.
- **Un-checksummed cells** (deposits/assets/AUM/SORA/current prices) are model-correlated (both runs Claude Opus 4.8) or single-source — spot-verify vs Tier-1 or run a non-Claude retriever before trusting.
- **OCBC 2016–2018 CASA / OCBC AUM** — `n/r` / low-confidence; complete from OCBC deposit notes if wanted.

## Changelog
- **2026-07-16 16:12 SGT** — Switched to **timestamped filenames** (dropped `v0.x`). Established **archive-on-new-version** process; moved `archive/` to **top-level (outside `claude/`)** so superseded files leave the Outputs panel. Current CoreTables set re-stamped `260716-161218`. Index is now the sole living, un-timestamped registry.
- **2026-07-16 (earlier)** — CoreTables built: split monolithic brief into SOP-Retrieval + Ledger + SOP-Report; Perplexity retrieval + Claude reconciliation (307 match / 118 holes filled / 14 mismatches resolved); added version/provenance columns; added Attracted-assets (deposits & CASA) + Wealth-AUM overlay + "why deposits+CASA" rationale.
