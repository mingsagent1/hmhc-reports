# Build-Health — Module SOP: pipeline completeness & confidence metrics (SG Banks)

> **Artifact:** `pipeline/sg-banks/method/code/build-health.md` — the specification for `build_health.py`; keep the two in sync.
> **Status:** Active — executed by the script, not by a model.

## Module contract

| | |
|---|---|
| **Inputs** | `data/ledger.csv` · `data/signals.md` (as-of line) · `reports/sg-banks/meta.json` · presence of `data/peers.csv` / `data/flows.csv`. |
| **Sole output** | `data/health.md` (human-readable status print) **+** `data/health.json` (machine-readable mirror — the data feed for a future UI). The controlled two-file exception: same content, two consumers. |
| **Executor** | **No model — a deterministic script:** `python3 pipeline/sg-banks/method/code/build_health.py`; `--check` verifies reproducibility (CI runs it on every PR). Derived only from file contents — no clocks, no git calls. |
| **Position** | Runs after any module changes `data/` or the report; cheap, rerun freely. |

## What it measures

- **Completeness** — how much of the frame is answered: per-question status (answered / partial / pending, with the module each depends on) and ledger fill rate (`filled` vs `n/d` vs `n/r`).
- **Confidence** — how trustworthy the filled cells are: dual-verified share (match + resolved), single-retriever exposure (incl. the 1Q2026 block), checksum agreement.
- **Gates** — live recomputation of the arithmetic tie-outs and the DBS NIM canary.
- **Freshness** — latest retrieval stamp in the ledger, signals as-of date, whether peer/flows data exists.
