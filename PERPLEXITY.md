# PERPLEXITY.md — job card for Perplexity Computer

> **How to use this file (for the human):** tell Perplexity — *"Read `PERPLEXITY.md` in `hmhc-ai/hmhc-reports` and execute it."* Nothing else needed. Claude maintains this file: it queues one job at a time from the gap list (`pipeline/sg-banks/meta/gaps.md`) and rotates it when done.
> **Authorization note:** a job being queued here **is** the author's cost-gate confirmation (UPDATE.md Step 2b) for that one run — the author queues jobs by asking Claude to update this card.

## Status: **NO JOB QUEUED — do nothing**

There is currently no authorized job. If you were sent here, stop and report back that the job card is empty.

---

## Completed jobs

- **Job #2 — fetch-peers delta** (NII · NIM · SharePrice · RBC in, CBA out) — **done 2026-07-24**, delivered in PR #30 (`perplexity/fetch-peers-delta`, peers.csv now 100 rows, 10 banks × 10 metrics, stamps `20260724-002 PxClOpus4.8`). Reviewed against independent search anchors (JPM/BofA/UBS/HSBC NII exact) and the ledger's SG rows (NII/NIM exact); merged by Claude; Q5 NII/OR split + Q6 price column live in `build_benchmarks.py`.

- **Job #1 — fetch-peers** (benchmark peer financials, Frame Q5/Q6) — **done 2026-07-24**, delivered in PR #26 (`perplexity/fetch-peers`, 70 rows, 10 banks × 7 metrics, stamp `20260724-001 PxClOpus4.8`). Reviewed, cross-checked against the ledger's SG rows (10/12 exact matches; 2 small deltas flagged), and merged by Claude; `build_benchmarks.py` now computes the full Q5/Q6 indices.

---

## Job queue (next up, not yet authorized — do NOT execute)

- fetch-flows (`pipeline/sg-banks/method/ai/fetch-flows.md`) — wealth-hub capital flows, Frame Q2.
- fetch-ledger delta P1 — the 8 never-retrieved `n/r` cells (see `pipeline/sg-banks/meta/gaps.md`).
- fetch-ledger verify P2a — non-Claude verification of the 46-row 1Q2026 block (bundle with the 2Q26 refresh, expected early Aug 2026).
