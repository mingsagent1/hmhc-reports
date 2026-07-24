# PERPLEXITY.md — job card for Perplexity Computer

> **How to use this file (for the human):** tell Perplexity — *"Read `PERPLEXITY.md` in `hmhc-ai/hmhc-reports` and execute it."* Nothing else needed. Claude maintains this file: it queues one job at a time from the gap list (`pipeline/sg-banks/meta/gaps.md`) and rotates it when done.
> **Authorization note:** a job being queued here **is** the author's cost-gate confirmation (UPDATE.md Step 2b) for that one run — the author queues jobs by asking Claude to update this card.

## Status: **JOB QUEUED — Job #2: fetch-peers delta (NII · NIM · SharePrice · RBC in, CBA out)**

---

## Job #2 — fetch-peers delta (Frame Q5 NII/OR split + Q6 price column + peer swap)

**Objective.** Update `pipeline/sg-banks/data/peers.csv` for the amended frame (2026-07-24): add the new metrics to every bank, add the new peer RBC in full, remove Commonwealth Bank.

**Instructions — read and follow, in order:**
1. `AGENTS.md` § Perplexity working agreement (the rules you operate under).
2. `pipeline/sg-banks/guides/frame.md` — the amended peer set (RBC replaces CBA; Australia-exclusion note) and the Q5/Q6 formats the data feeds.
3. **`pipeline/sg-banks/method/ai/fetch-peers.md` — the SOP.** Note the three metrics added to its table: `NII`, `NIM` (as-stated, `n/d` honestly), `SharePrice` (dated, same venue/date as `MarketCap` where possible).

**The delta, precisely — edit `data/peers.csv` in place:**
- **Add** `NII`, `NIM`, `SharePrice` rows for all 10 banks (7 peers incl. RBC + DBS/OCBC/UOB), same FY basis as each bank's existing rows.
- **Add** the full metric set for **RBC** (all metrics in the SOP; FY ends 31 Oct 2025; CAD).
- **Remove** all Commonwealth Bank rows.
- **Do not modify** any other existing row (they are already reviewed and reconciled).

**Deliverable.** One file only: `pipeline/sg-banks/data/peers.csv`. Provenance stamp per new row: `YYYYMMDD-NNN Px<Model>` — name the model you actually run on (prefer a **non-Claude** model for cross-model independence).

**Git workflow.**
- Branch: `perplexity/fetch-peers-delta` (branched from `main`).
- Commit trailers per `AGENTS.md` § Commit attribution.
- Open a pull request titled **"Perplexity: fetch-peers delta — NII/NIM/SharePrice + RBC"**. In the description: FY used per bank, every `n/d` and why, and any questions.
- **Do not merge.** Claude reviews, reconciles, runs the build modules, and merges.

**Do not touch anything else** — no edits to `method/`, `guides/`, `reports/`, `UPDATE.md`, the registry, workflows, or this file.

---

## Completed jobs

- **Job #1 — fetch-peers** (benchmark peer financials, Frame Q5/Q6) — **done 2026-07-24**, delivered in PR #26 (`perplexity/fetch-peers`, 70 rows, 10 banks × 7 metrics, stamp `20260724-001 PxClOpus4.8`). Reviewed, cross-checked against the ledger's SG rows (10/12 exact matches; 2 small deltas flagged), and merged by Claude; `build_benchmarks.py` now computes the full Q5/Q6 indices.

---

## Job queue (next up, not yet authorized — do NOT execute)

- fetch-flows (`pipeline/sg-banks/method/ai/fetch-flows.md`) — wealth-hub capital flows, Frame Q2.
- fetch-ledger delta P1 — the 8 never-retrieved `n/r` cells (see `pipeline/sg-banks/meta/gaps.md`).
- fetch-ledger verify P2a — non-Claude verification of the 46-row 1Q2026 block (bundle with the 2Q26 refresh, expected early Aug 2026).
