# wealth_assetanalysis_banks

Data pipeline and analysis for the **Singapore Bank Stock Accumulation Strategy** — a fundamentals-driven look at DBS (SGX: D05), OCBC (SGX: O39), and UOB (SGX: U11) over FY2016–FY2025 plus the latest 2026 interim, built around the Singapore wealth-hub / asset-attraction thesis.

## Start here

**[`SGBanks_Index.md`](SGBanks_Index.md) is the living registry** — the single source of truth for what each artifact is, its current status, the ledger schema, standing analytical decisions, and open questions. Read it first.

## How it works

The project is built as **components** (self-contained analyses; current component: `Tables`). Each component runs a **two-stage pipeline**:

1. **Retrieve** — one or more agents fill a shared raw-data ledger with atomic, sourced numbers (no calculations). Each agent fills its own columns; values are cross-checked against embedded checksums. Governed by the retrieval SOP.
2. **Reconcile + build** — agents' values are compared against each other and the checksums, disagreements are resolved (never averaged) into a `reconciled_value`, and the clean report is built from those. Governed by the report SOP.

## Files

| File | What it is |
|---|---|
| [`SGBanks_Index.md`](SGBanks_Index.md) | Living project registry — start here |
| [`SGBanks_Tables_SOPRetrieval.md`](SGBanks_Tables_SOPRetrieval.md) | SOP 1 — raw-data retrieval rules (source hierarchy, definitional traps, poison pills, self-checks) |
| [`SGBanks_Tables_Ledger.csv`](SGBanks_Tables_Ledger.csv) | The shared reconciliation ledger — 536 data points, one number per row, with per-agent provenance and reconciliation status |
| [`SGBanks_Tables_SOPReport.md`](SGBanks_Tables_SOPReport.md) | SOP 2 — reconcile + report-build rules (table specs, formatting, validation, appendices) |
| `LICENSE` | MIT |

The report output (`SGBanks_Tables_Report.md`) is not yet built.

## Versioning

**Git-native.** Version history lives in git commits and tags — there are no timestamped filenames and no `archive/` folder. To inspect or restore prior states:

```bash
git log --oneline SGBanks_Tables_Ledger.csv   # what changed, when
git show <sha>:SGBanks_Tables_Ledger.csv        # view a past version
git checkout <sha> -- SGBanks_Tables_Ledger.csv # restore a past version
```

Provenance is also recorded *inside* the files (ledger `px_version` / `cl_version` run stamps, SOP changelogs) as a second, in-band record.

## Scope guardrails (see the SOPs for the full list)

- **SGD only** — never convert, never USD, never ADRs.
- **Tier-1 sources** (company reports) for every fundamental; market data (prices, rates) only from Tier-2 vendors / MAS / FRED; Yahoo for price cross-check only.
- **Never estimate, interpolate, or fill from memory** — `n/r` (not retrieved) and `n/d` (not disclosed) are correct answers; a plausible wrong number is a failure.
