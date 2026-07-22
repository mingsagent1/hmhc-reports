# Build-Benchmarks — Module SOP: peer benchmarking computation (SG Banks)

> **Artifact:** `pipeline/sg-banks/method/code/build-benchmarks.md` — the specification for `build_benchmarks.py`; keep the two in sync.
> **Status:** Active — executed by the script, not by a model. Runs in **SG-only preview mode** until the fetch outputs exist.

## Module contract

| | |
|---|---|
| **Inputs** | Reconciled `data/ledger.csv` (SG banks) · `data/peers.csv` (Fetch-Peers output, when present) · `data/flows.csv` (Fetch-Flows output, when present). |
| **Sole output** | `data/benchmarks.md` — monetization indices and four valuation indexes vs the index bank = 100 (Frame Q5/Q6), required 5-yr outperformance = (premium)^(1/5) − 1, and the wealth-hub flows table (Frame Q2). Sections needing unfetched inputs are marked pending, with SG-only raw values shown meanwhile. |
| **Executor** | **No model — a deterministic script:** `python3 pipeline/sg-banks/method/code/build_benchmarks.py`; `--check` verifies reproducibility (CI runs it on every PR). |
| **Position** | `Fetch-Peers ‖ Fetch-Flows → Build-Benchmarks → Write-Conclusions`. Index bank, peer set, metric definitions all come from `guides/frame.md`. |

## Rules

- All indices are **within-bank ratios** (currency cancels); never convert FX.
- Index bank = 100 per `guides/frame.md` (currently HSBC). SG market cap = the ledger's dated current price × FY25 shares outstanding.
- Missing inputs are shown as `n/r` — never estimated. Output is pure markdown (no raw HTML).
