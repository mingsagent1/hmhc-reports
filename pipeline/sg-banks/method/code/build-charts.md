# Build-Charts — Module SOP: deterministic chart generation (SG Banks)

> **Artifact:** `pipeline/sg-banks/method/code/build-charts.md` — the specification for `build_charts.py`; keep the two in sync.
> **Status:** Active — executed by the script, not by a model.

## Module contract

| | |
|---|---|
| **Inputs** | Reconciled `pipeline/sg-banks/data/ledger.csv` (Reconcile must be complete for every consumed row). |
| **Sole output** | SVG chart assets in `reports/sg-banks/assets/` (currently `nim-vs-sora.svg`). |
| **Executor** | **No model — a deterministic script:** `pipeline/sg-banks/method/code/build_charts.py`. Run `python3 pipeline/sg-banks/method/code/build_charts.py` to regenerate; `--check` verifies the committed SVGs byte-for-byte against the ledger (CI runs this on every PR). Hand-written SVG — no plotting libraries, no timestamps, no AI. |
| **Idempotence** | Rerun regenerates the assets in place; same ledger in → same SVG out. Git retains history. |
| **Position** | `… → Reconcile → Build-Charts → Build-Report → …` (parallel to Build-Tables). Build-Report embeds the assets by relative path. |

## Chart inventory

| Asset | Serves | Content |
|---|---|---|
| `nim-vs-sora.svg` | Frame Q4 (NIM cyclicality) | Group NIM per bank (solid lines) vs 3M SORA FY-avg and effective Fed funds FY-avg (dashed), FY2016–FY2025 + 2026 latest (1Q26 NIM · 1Q26 avg SORA · YTD Fed). Single % y-axis 0–5.5. SORA starts 2020 (series began Aug-2020; no splice). |

## Rules

- Values come **only** from `reconciled_value` in the ledger; missing/`n/r`/`n/d` points are omitted from the line, never interpolated.
- Colors: DBS `#d62728` · OCBC `#ff7f0e` · UOB `#1f77b4`; benchmark rates in muted dashed (`#7f7f7f` SORA, `#9467bd` Fed). NIM lines solid and heavier than rate lines.
- Every chart carries: title, unit in the title, legend, and a footnote stating any partial-period or definitional caveat.
- Adding a chart = add a builder to `build_charts.py`, a row to the inventory above, and embed it from the report — one PR.

## Acceptance criteria

- `--check` passes (committed SVG byte-identical to a fresh generation from the ledger).
- The chart renders as a plain `<img>`/markdown image — no external resources, fonts declared with safe fallbacks, self-contained SVG.
