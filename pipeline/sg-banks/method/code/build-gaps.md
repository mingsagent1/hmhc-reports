# Build-Gaps — Module SOP: smart-update worklist (SG Banks)

> **Artifact:** `pipeline/sg-banks/method/code/build-gaps.md` — the specification for `build_gaps.py`; keep the two in sync.
> **Status:** Active — executed by the script, not by a model.

## Module contract

| | |
|---|---|
| **Inputs** | `data/ledger.csv` · presence of `data/flows.csv` / `data/peers.csv` · the static reporting-calendar table inside the script (update it when banks announce dates). |
| **Sole output** | `meta/gaps.md` + `meta/gaps.json` (machine-readable mirror). |
| **Executor** | **No model — a deterministic script:** `python3 pipeline/sg-banks/method/code/build_gaps.py`; `--check` verifies reproducibility (CI runs it on every PR). |
| **Position** | Regenerate after any ledger/data change (alongside Build-Health). Its output is the source for **job cards in `PERPLEXITY.md`** — each gap is a ready-made, surgical fetch job. |

## Why it exists

Full fetch runs are expensive. This module turns the ledger's own quality flags into **delta jobs**: exactly which rows are missing (`n/r`), which need a second retriever (single-px / single-cl, incl. the 1Q2026 block), when the reporting calendar will supersede data (bundle opportunities), and which module outputs are still pending. Continuous improvement = these numbers trending toward zero, visible run over run in `meta/health.json`.
