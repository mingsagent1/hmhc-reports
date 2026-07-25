# SG Banks — Pipeline Health (generated artifact)

*Artifact: `pipeline/sg-banks/meta/health.md` (+ `health.json`, the machine-readable mirror) — sole output of `pipeline/sg-banks/method/code/build_health.py`. Report version 2026.07.25, last updated 2026-07-25.*

## Completeness — how much of the frame is answered

- Key questions: **5 of 6 fully answered**

| Q | Topic | Status | Depends on |
|---|---|---|---|
| Q1 | Deposits & Wealth AUM trend | answered | ledger |
| Q2 | Wealth-hub capital flows | pending | fetch-flows |
| Q3 | NII & Other Revenue trend | answered | ledger |
| Q4 | NIM volatility & cyclicality | answered | ledger + chart |
| Q5 | Monetization score vs peers | answered | fetch-peers + build-benchmarks |
| Q6 | Relative valuation vs peers | answered | fetch-peers + build-benchmarks |

- Ledger: **557 of 582 rows filled (95.7%)** · 17 not disclosed by the banks (`n/d`) · 8 not yet retrieved (`n/r`)

## Confidence — how trustworthy the filled cells are

- **Dual-verified: 319 rows (57.3% of filled)** — two independent retrievers agree or the disagreement is resolved with a documented cause
- **Single-retriever exposure: 235 rows (42.2% of filled)** — one source only; of these, 46 are the whole 1Q2026 block (one Claude pass, non-Claude cross-check advisable)
- Checksums: 34 of 72 embedded checksums matched exactly; the rest are `resolved` with documented causes (restatements, basis, rounding)
- Retriever scorecard: where both retrievers filled a numeric cell, they agree (within 0.5%) on **300 of 322 cells (93.2%)** — the cross-model error-rate baseline to improve on

## Gates

- Arithmetic tie-outs (NII + Non-II = Total income): **all pass**
- DBS group-NIM canary (FY25 = 2.01): **pass**

## Freshness

- Ledger latest retrieval stamp: 20260720
- Signals last run: 2026-07-20
- Peer data fetched: yes · Flows data fetched: no (fetch-flows pending)
