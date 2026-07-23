# SG Banks — Fetch Gaps (smart-update worklist)

*Artifact: `pipeline/sg-banks/meta/gaps.md` (+ `gaps.json`) — sole output of `pipeline/sg-banks/method/code/build_gaps.py`. Each gap is a surgical fetch job: exact rows, the SOP that covers it, and a size estimate — so updates are deltas, not full refreshes. Queue jobs for the external runner via `PERPLEXITY.md`.*

| # | Gap | Size | SOP | Priority |
|---|---|---:|---|---|
| P1 | Never-retrieved cells (`n/r`) | 8 rows | fetch-ledger (delta) | high |
| P2a | 1Q2026 block single-Claude → needs non-Claude verification | 46 rows | fetch-ledger (verify) | high (bundle with 2Q26) |
| P2b | FY-history single-px cells | 119 rows | fetch-ledger (verify) | medium |
| P2c | Other single-cl cells | 70 rows | fetch-ledger (verify) | low |
| P3 | Reporting calendar — next results supersede the interim block | ~46 rows | fetch-ledger + fetch-signals | dated |
| P4 | Pending module outputs | 2 datasets | fetch-flows · fetch-peers | high |

## P1 — never retrieved (`n/r`)

`RATE_SORA_YE_2016`, `RATE_SORA_AVG_2016`, `RATE_SORA_YE_2017`, `RATE_SORA_AVG_2017`, `RATE_SORA_YE_2018`, `RATE_SORA_AVG_2018`, `RATE_SORA_YE_2019`, `RATE_SORA_AVG_2019`

## P2a — 1Q2026 single-Claude block

46 rows, all stamped `20260720-001 CwClOpus4.8`. A non-Claude verification pass upgrades the whole block to dual-verified. consider bundling with the 2Q26 refresh (see calendar).

## P2b — single-px FY-history families

| Metric family | Rows |
|---|---:|
| CustomerDeposits | 30 |
| TotalAssets | 30 |
| WealthAUM | 26 |
| Wealth | 14 |
| SORA_YE | 6 |
| SORA_avg | 6 |
| RoTE | 3 |
| CASAratio | 3 |
| ROE | 1 |

## P2c — other single-cl families

| Metric family | Rows |
|---|---:|
| CASAratio | 27 |
| CurrentAccts | 20 |
| SavingsDep | 20 |
| PriceCurrent | 3 |

## P3 — reporting calendar (approximate, from historical cadence)

- **DBS** — 1H26 results: expected early Aug 2026 (historically ~first week of Aug)
- **OCBC** — 1H26 results: expected early Aug 2026 (historically ~first week of Aug)
- **UOB** — 1H26 results: expected early Aug 2026 (historically ~first week of Aug)

when 1H26/2Q26 results land, the 1Q2026 interim block (~46 rows) is superseded — the natural moment for one bundled fetch job (new quarter + P2a verification)

## P4 — pending module outputs

- fetch-flows → data/flows.csv
- fetch-peers → data/peers.csv
