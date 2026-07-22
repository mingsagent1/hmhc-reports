# SG Banks — Benchmarks (generated artifact)

*Artifact: `pipeline/sg-banks/data/benchmarks.md` — sole output of `pipeline/sg-banks/method/code/build_benchmarks.py`. Inputs: reconciled `data/ledger.csv` (SG banks). Rerun the script to regenerate; same inputs in, same output out.*

## Monetization (Frame Q5)

**Peer index pending** — `data/peers.csv` not yet fetched (module `ai/fetch-peers.md` is written; run is cost-gated). SG-only raw values meanwhile:

| Bank | Monetization_vDeposits | Monetization_vCapitalBase |
|---|---:|---:|
| DBS | 3.75% | 2.09% |
| OCBC | 3.41% | 1.89% |
| UOB | 3.24% | 2.20% |

*Monetization_vDeposits = total revenue ÷ customer deposits. Monetization_vCapitalBase = total revenue ÷ (customer deposits + wealth AUM) — AUM definitions differ per bank; read the two indices together.*

## Relative valuation (Frame Q6)

**Pending** — needs `data/peers.csv` (module `ai/fetch-peers.md` is written; run is cost-gated). SG-only raw multiples meanwhile (market cap at the ledger's dated current price):

| Bank | P/CapitalBase | P/Rev | P/E | P/B |
|---|---:|---:|---:|---:|
| DBS | 0.19 | 8.92 | 18.51 | 2.96 |
| OCBC | 0.17 | 8.79 | 17.30 | 2.14 |
| UOB | 0.11 | 5.10 | 15.03 | 1.45 |

*P/CapitalBase = market cap ÷ (deposits + AUM) · P/Rev = market cap ÷ total revenue · P/E = market cap ÷ net profit · P/B = market cap ÷ book equity. SG market cap = current dated price × FY25 shares outstanding, from the ledger.*

## Wealth-hub capital flows (Frame Q2)

**Pending** — `data/flows.csv` not yet fetched (module `ai/fetch-flows.md` is written; run is cost-gated).
