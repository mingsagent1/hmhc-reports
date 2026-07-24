# SG Banks — Benchmarks (generated artifact)

*Artifact: `pipeline/sg-banks/data/benchmarks.md` — sole output of `pipeline/sg-banks/method/code/build_benchmarks.py`. Inputs: reconciled `data/ledger.csv` (SG banks), `data/peers.csv`. Rerun the script to regenerate; same inputs in, same output out.*

## Monetization (Frame Q5)

Indexed to HSBC = 100 (latest FY per bank; ratios are within-bank, so currencies cancel).

| Bank | Monetization_vDeposits (index) | Monetization_vCapitalBase (index) |
|---|---:|---:|
| DBS | 98 | 100 |
| OCBC | 89 | 91 |
| UOB | 85 | 106 |
| HSBC | 100 | 100 |
| UBS | 165 | 43 |
| JPMorgan Chase | 187 | 119 |
| Bank of America | 147 | 80 |
| Standard Chartered | 103 | 103 |
| China Merchants Bank | 90 | 60 |
| Commonwealth Bank | 79 | n/r |

*Monetization_vDeposits = total revenue ÷ customer deposits. Monetization_vCapitalBase = total revenue ÷ (customer deposits + wealth AUM) — AUM definitions differ per bank; read the two indices together.*

## Relative valuation (Frame Q6)

Four indexes vs HSBC = 100; required outperformance = (premium ratio)^(1/5) − 1 per year (5-yr convergence).

| Bank | P/CapitalBase | req %/yr | P/Rev | req %/yr | P/E | req %/yr | P/B | req %/yr |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| DBS | 175 | +11.9% | 175 | +11.8% | 112 | +2.3% | 169 | +11.0% |
| OCBC | 157 | +9.4% | 172 | +11.5% | 105 | +0.9% | 122 | +4.0% |
| UOB | 106 | +1.1% | 100 | -0.0% | 91 | -1.9% | 83 | -3.8% |
| HSBC | 100 | +0.0% | 100 | +0.0% | 100 | +0.0% | 100 | +0.0% |
| UBS | 27 | -22.9% | 63 | -8.7% | 125 | +4.6% | 101 | +0.2% |
| JPMorgan Chase | 119 | +3.5% | 99 | -0.1% | 98 | -0.3% | 145 | +7.8% |
| Bank of America | 59 | -10.1% | 73 | -6.0% | 84 | -3.4% | 80 | -4.5% |
| Standard Chartered | 56 | -11.0% | 54 | -11.5% | 69 | -7.1% | 71 | -6.7% |
| China Merchants Bank | 33 | -19.7% | 55 | -11.2% | 38 | -17.4% | 43 | -15.7% |
| Commonwealth Bank | n/r |  | 202 | +15.0% | 174 | +11.7% | 210 | +16.0% |

*P/CapitalBase = market cap ÷ (deposits + AUM) · P/Rev = market cap ÷ total revenue · P/E = market cap ÷ net profit · P/B = market cap ÷ book equity. SG market cap = current dated price × FY25 shares outstanding, from the ledger.*

## Wealth-hub capital flows (Frame Q2)

**Pending** — `data/flows.csv` not yet fetched (module `ai/fetch-flows.md` is written; run is cost-gated).
