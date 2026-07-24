# SG Banks — Benchmarks (generated artifact)

*Artifact: `pipeline/sg-banks/data/benchmarks.md` — sole output of `pipeline/sg-banks/method/code/build_benchmarks.py`. Inputs: reconciled `data/ledger.csv` (SG banks), `data/peers.csv`. Rerun the script to regenerate; same inputs in, same output out.*

## Monetization (Frame Q5)

Indexed to HSBC = 100 (latest FY per bank; ratios are within-bank, so currencies cancel). vDep = Monetization_vDeposits · vCap = Monetization_vCapitalBase (definitions below).

| Bank | vDep (idx) | vCap (idx) | Top Other-Revenue (% of total revenue) |
|---|---:|---:|---|
| DBS | 98 | 100 | net fee & commission 21.4% · net trading income 14.7% · net income from investment securities 0.4% |
| OCBC | 89 | 91 | fees & commissions 16.5% · trading income 11.5% · life & general insurance income 7.3% |
| UOB | 85 | 106 | net fee & commission 18.6% · other non-interest income 13.6% · 3rd n/d |
| HSBC | 100 | 100 | trading/FV income 28.8% · net fee income 19.5% · insurance service revenue 4.7% |
| UBS | 165 | 43 | net fee & commission income 56.3% · other net income from FI at FVTPL (trading) 28.3% · 3rd n/d |
| JPMorgan Chase | 187 | 119 | asset management fees 11.1% · investment banking fees ~5.6% · card income 2.6% |
| Bank of America | 147 | 80 | asset management fees 13.8% · investment banking fees 5.9% · service charges 5.7% |
| Standard Chartered | 103 | 103 | net trading & other income 51.3% · net fees & commission 20.3% (reported basis) |
| China Merchants Bank | 90 | 60 | net fee & commission income 22.3% · other net non-interest income ~13.8% |
| Commonwealth Bank | 79 | n/r | net other operating income 15.1% · 2nd/3rd n/d |

*Monetization_vDeposits = total revenue ÷ customer deposits. Monetization_vCapitalBase = total revenue ÷ (customer deposits + wealth AUM) — AUM definitions differ per bank; read the two indices together.*

## Relative valuation (Frame Q6)

Four indexes vs HSBC = 100; req %/yr = required outperformance, (premium ratio)^(1/5) − 1 per year (5-yr convergence). Px = local per-share price with its as-of date — the staleness marker (P/Cap = P/CapitalBase).

| Bank | Px (as-of) | P/Cap | req %/yr | P/Rev | req %/yr | P/E | req %/yr | P/B | req %/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| DBS | S$71.96 (2026-07-20) | 175 | +11.9% | 175 | +11.8% | 112 | +2.3% | 169 | +11.0% |
| OCBC | S$28.60 (2026-07-20) | 157 | +9.4% | 172 | +11.5% | 105 | +0.9% | 122 | +4.0% |
| UOB | S$42.60 (2026-07-20) | 106 | +1.1% | 100 | -0.0% | 91 | -1.9% | 83 | -3.8% |
| HSBC | n/r (mcap 2026-07-23) | 100 | +0.0% | 100 | +0.0% | 100 | +0.0% | 100 | +0.0% |
| UBS | n/r (mcap 2026-07-23) | 27 | -22.9% | 63 | -8.7% | 125 | +4.6% | 101 | +0.2% |
| JPMorgan Chase | n/r (mcap 2026-07-22) | 119 | +3.5% | 99 | -0.1% | 98 | -0.3% | 145 | +7.8% |
| Bank of America | n/r (mcap 2026-07-20) | 59 | -10.1% | 73 | -6.0% | 84 | -3.4% | 80 | -4.5% |
| Standard Chartered | n/r (mcap 2026-07-03) | 56 | -11.0% | 54 | -11.5% | 69 | -7.1% | 71 | -6.7% |
| China Merchants Bank | n/r (mcap 2026-07-06) | 33 | -19.7% | 55 | -11.2% | 38 | -17.4% | 43 | -15.7% |
| Commonwealth Bank | n/r (mcap 2026-07) | n/r |  | 202 | +15.0% | 174 | +11.7% | 210 | +16.0% |

*P/CapitalBase = market cap ÷ (deposits + AUM) · P/Rev = market cap ÷ total revenue · P/E = market cap ÷ net profit · P/B = market cap ÷ book equity. SG market cap = current dated price × FY25 shares outstanding, from the ledger.*

## Wealth-hub capital flows (Frame Q2)

**Pending** — `data/flows.csv` not yet fetched (module `ai/fetch-flows.md` is written; run is cost-gated).
