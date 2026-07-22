# Reconcile — Module SOP: ledger reconciliation (SG Banks)

> **Module:** Reconcile · **Cost:** cheap (no retrieval) · **Run on:** human + Claude (judgment step; no search, no memory-fills).
> **History:** promoted to a standalone module 2026-07-21; rules previously lived as a "reference" aside in `build-tables.md`.

## Module contract

| | |
|---|---|
| **Inputs** | `pipeline/sg-banks/data/ledger.csv` with the retriever columns filled (`px_*` from the external pass, `cl_*` from the Claude pass) and the pre-set `checksum_expected` values. |
| **Sole output** | The `reconciled_value` / `reconciliation_status` / `reconciliation_note` columns of the **same** `data/ledger.csv`. This module is the controlled exception to one-file-per-output: it writes columns in place rather than a separate artifact. |
| **Idempotence** | A rerun re-fills the reconciled columns from the current `px_*`/`cl_*` values. Git retains history. |
| **Position** | `Frame → (Fetch-Ledger ‖ Fetch-Signals) → Reconcile → Build-Tables → …`. Build-Tables consumes only reconciled rows; it never re-opens retrieval. |

## Reconciliation rules

For every row compare `px_value`, `cl_value`, and `checksum_expected`, then fill the three reconciled columns:

- **`match`** — agents agree (and agree with the checksum if present) → take the value. Use `match` **only** when `px_value`, `cl_value`, and any `checksum_expected` are all equal (pure rounding aside); if the taken value differs from the checksum, or `px≠cl`, it is `resolved`, not `match`.
- **`single-px` / `single-cl`** — only one agent filled it → take it; the status names which. Cross-model confidence rules: same-model agreement can share a blind spot — see the provenance-stamp rationale in `fetch-ledger.md` §1.
- **`resolved`** — agents disagree, or the taken value disagrees with the checksum. **Do not average or silently pick.** Take the value that (a) reproduces the checksum and (b) ties out (NII + Non-NII = Total income), and record the loser + likely cause (rounding / basis / restatement / price-date) in `reconciliation_note`. If neither ties, mark the cell `n/r` for the report and log it.
- **`n/r` / `n/d` / `text/other`** — carry through (`text/other` = guidance/verbatim text rows).

Prefer **restated** figures (trap B6 in `fetch-ledger.md`) and record the original in the note. Every `resolved` row becomes a line in the report's Validation Report (Appendix A), lifted downstream via `tables.md`.

## Self-checks before returning the ledger (all must pass)

1. Every row consumed by Tables carries a `reconciliation_status`.
2. **NII + Non-NII = Total income** holds for every reconciled bank-year.
3. **DBS NIM canary:** `DBS_NIMgroup_2025` = 2.01 (group series, not 2.80 commercial-book).
4. No checksum mismatch is left unexplained — each has a cause in `reconciliation_note`.
5. No averaged or silently-picked values.

## Hand-off

The reconciled `data/ledger.csv` feeds **Build-Tables** (`method/code/build-tables.md`). Reconcile publishes nothing to `reports/`.
