# PERPLEXITY.md — job card for Perplexity Computer

> **How to use this file (for the human):** tell Perplexity — *"Read `PERPLEXITY.md` in `mingsagent1/hmhc-reports` and execute it."* Nothing else needed. Claude maintains this file: it queues one job at a time from the gap list (`pipeline/sg-banks/meta/gaps.md`) and rotates it when done.
> **Authorization note:** a job being queued here **is** the author's cost-gate confirmation (UPDATE.md Step 2b) for that one run — the author queues jobs by asking Claude to update this card.

## Status: **JOB QUEUED — Job #1: fetch-peers**

---

## Job #1 — fetch-peers (benchmark peer financials, Frame Q5/Q6)

**Objective.** Fill `pipeline/sg-banks/data/peers.csv` with Tier-1 fundamentals for the 7 benchmark banks + the 3 SG banks (external cross-check), so the monetization and valuation indices can be computed.

**Instructions — read and follow, in order:**
1. `AGENTS.md` § Perplexity working agreement (the rules you operate under).
2. `pipeline/sg-banks/guides/frame.md` — the peer set, metric definitions, and index design (Q5/Q6).
3. **`pipeline/sg-banks/method/ai/fetch-peers.md` — the SOP for this job.** Banks, metrics, source hierarchy, currency rule, CSV schema, self-checks. Follow it exactly.

**Deliverable.** One file only: `pipeline/sg-banks/data/peers.csv` — schema `bank, metric, period, unit, value, source, comment, version`. Provenance stamp per row: `YYYYMMDD-NNN PxGPT5.6` (adjust the model token to what you actually run on).

**Git workflow.**
- Branch: `perplexity/fetch-peers` (branched from `main`).
- Commit message trailers per `AGENTS.md` § Commit attribution.
- Open a pull request titled **"Perplexity: fetch-peers — benchmark peer financials (Q5/Q6)"**. In the PR description: your per-bank FY used, any `n/r`/`n/d` cells and why, and any questions.
- **Do not merge.** Claude reviews, reconciles against the ledger's SG rows, runs the build modules, and merges.

**Do not touch anything else** — no edits to `method/`, `guides/`, `reports/`, `UPDATE.md`, the registry, workflows, or this file.

---

## Job queue (next up, not yet authorized — do NOT execute)

- fetch-flows (`pipeline/sg-banks/method/ai/fetch-flows.md`) — wealth-hub capital flows, Frame Q2.
- fetch-ledger delta P1 — the 8 never-retrieved `n/r` cells (see `pipeline/sg-banks/meta/gaps.md`).
- fetch-ledger verify P2a — non-Claude verification of the 46-row 1Q2026 block (bundle with the 2Q26 refresh, expected early Aug 2026).
