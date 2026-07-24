# Fetch-Peers — Module SOP: benchmark peer financials (SG Banks · Frame Q5/Q6)

> ## ⚠ EXPENSIVE — opt-in only
> Runs only via `UPDATE.md`'s ask-gate + Step 2b cost gate (explicit user confirmation — full rule there). Reached this file without that confirmation? **Stop and ask first.**

**Module:** Fetch-Peers · **Input:** `guides/frame.md` (peer set + Q5/Q6 definitions) · **Output:** `data/peers.csv` · **Depends on:** Frame
**Run on:** a **non-Claude, search-grounded** model (Perplexity Computer / GPT-class with live web) — by design, for independence from the Claude-built pipeline.

## Purpose

Fill the inputs for Frame **Q5** (monetization indices) and **Q6** (four valuation indexes + 5-yr required outperformance): one row of fundamentals per peer bank, latest full FY, plus current market cap.

## Banks

The **7 approved peers** in `guides/frame.md` (HSBC — the index bank — UBS, JPMorgan Chase, Bank of America, Standard Chartered, China Merchants Bank, RBC) **and the 3 SG banks** (DBS, OCBC, UOB — fetched again here deliberately, as an external cross-check against the ledger; the reconcile step compares them). *(Commonwealth Bank was replaced by RBC on 2026-07-24 — Australia's majors all divested wealth, see the frame's peer-table note; remove any CBA rows when updating `peers.csv`.)*

## Metrics per bank (latest full FY; state the FY used)

| metric | Definition | Notes |
|---|---|---|
| `CustomerDeposits` | total customer deposits (group, balance sheet) | not interbank |
| `WealthAUM` | wealth-management / private-bank client assets (invested assets, client balances) | state each bank's label + definition in `comment` — definitions vary hugely; this is expected and flagged downstream |
| `TotalRevenue` | total operating income / total revenue net of interest expense | state basis |
| `NII` | net interest income (group, same FY and basis as `TotalRevenue`) | feeds the Q5 NII/OR split — OR is derived downstream as TotalRevenue − NII, never fetched |
| `NIM` | net interest margin, as stated by the bank (group where available) | context only, not indexed — state the bank's own basis in `comment`; `n/d` honestly (e.g. UBS discloses no group NIM) |
| `NetProfit` | net profit attributable to shareholders | |
| `BookEquity` | total shareholders' equity attributable (ex-minorities) | |
| `MarketCap` | current market capitalisation, with date | |
| `SharePrice` | current local per-share price, with date (`period` = the as-of date) | Tier-2 market data; same venue/date as `MarketCap` where possible — feeds the Q6 table's staleness column |
| `TopOtherRevenue` | top-3 non-NII revenue categories with % of total revenue (text) | e.g. "insurance 23%" |

**Currency rule:** report each bank in its **reporting currency** and name it in `unit`. The downstream indices are ratios (market cap ÷ deposits, revenue ÷ deposits, …) computed **within one bank**, so currency cancels — never convert, never mix currencies within a row's numerator/denominator.

## Source hierarchy

Tier 1 — the bank's own annual report / FY results release / regulatory filing for every fundamental. Tier 2 — market data only for `MarketCap` (state date + venue). Aggregators/screeners forbidden for fundamentals, per the ledger rules.

## Output — `data/peers.csv`

`bank, metric, period, unit, value, source, comment, version` — provenance stamp `YYYYMMDD-NNN <Harness><Model>` per the ledger convention. `n/r` / `n/d` honestly (several peers may not disclose comparable wealth AUM — that's a finding, not a failure).

## Self-checks (all must pass)

1. Every fundamental is Tier-1 sourced; MarketCap dated.
2. Currency named per row; no conversions.
3. WealthAUM definition captured verbatim per bank in `comment`.
4. SG-bank rows present (cross-check set).
5. Enough to compute, per bank: the Q5 monetization set (`NII_vDep`, `OR_vDep`, `OR_vCap`, `total_vCap` — needs `NII` alongside `TotalRevenue`) and the Q6 valuation set (`P/CapitalBase`, `P/Rev`, `P/E`, `P/B`). Computation happens downstream in `code/build_benchmarks.py`, not here.

## Hand-off

`data/peers.csv` feeds **Build-Benchmarks** (`method/code/build_benchmarks.py`), which produces the indexed scores consumed by **Write-Conclusions** (Q5/Q6). Fetch-Peers publishes nothing to `reports/`.
