# Fetch-Flows — Module SOP: wealth-hub capital flows (SG Banks · Frame Q2)

> ## ⚠ EXPENSIVE — opt-in only
> Runs only via `UPDATE.md`'s ask-gate + Step 2b cost gate (explicit user confirmation — full rule there). Reached this file without that confirmation? **Stop and ask first.**

**Module:** Fetch-Flows · **Input:** `guides/frame.md` Q2 · **Output:** `data/flows.csv` · **Depends on:** Frame
**Run on:** a **non-Claude, search-grounded** model (Perplexity Computer / GPT-class with live web) — by design, for independence from the Claude-built pipeline.

## Purpose

Answer Frame **Q2**: the trend in wealth-hub capital flows over the last 5 years — is Singapore gaining, holding, or losing share versus other hubs? Gather **assets-under-management / cross-border wealth stocks per hub, in USD**, for FY2020–FY2025 (or the latest available year per source; state the vintage).

## Hubs to cover (minimum)

Singapore · Hong Kong · Switzerland · United States (international/booking-centre wealth) · UAE/Gulf (include as a flow *competitor* even though excluded from the bank peer set) · United Kingdom. Add others only if a Tier-1/2 source ranks them among top cross-border booking centres.

## Source hierarchy

- **Tier 1 (preferred):** official statistics — MAS asset-management survey (Singapore AUM), HK SFC asset & wealth management survey, Swiss Bankers Association / SNB, national regulators.
- **Tier 2 (allowed, marked):** BCG Global Wealth Report, Deloitte International Wealth Management Centre Ranking, McKinsey, Capgemini WWR — name report + year + page.
- **Consistency rule:** cross-hub *share* comparisons must come from a **single source family** (e.g. BCG cross-border booking-centre series) — never mix one hub's regulator number with another hub's consultant number in the same comparison row. Per-hub deep figures may additionally cite the local regulator.

## Output — `data/flows.csv`

One row per hub-year-measure: `hub, measure, year, unit, value, source, comment, version`.
- `measure`: e.g. `CrossBorderWealth` (booking-centre stock, the share basis) · `TotalAUM` (regulator series). Keep measures separate; never blend.
- `unit`: `US$tn` (as sourced; note original currency if converted by the source).
- `version`: provenance stamp `YYYYMMDD-NNN <Harness><Model>` (e.g. `PxGPT5.6`), per the ledger convention.
- Mark `n/r` / `n/d` honestly; a complete-looking grid from mixed sources is the failure mode.

## Self-checks (all must pass)

1. Every value has a dated, named source; share comparisons single-source-family.
2. Singapore, Hong Kong, Switzerland present for ≥4 of the last 5 years (or gaps explained).
3. Units USD as sourced; no self-computed FX conversions.
4. No forecasts — historical/actuals only.
5. Enough to fill the frame Q2 format: `WealthHub: US$tn, 5y-CAGR %, FY25 %, FY24 %, FY23 %, FY22 %` (derivations happen downstream in `code/build_benchmarks.py`, not here).

## Hand-off

`data/flows.csv` feeds **Build-Benchmarks** (`method/code/build_benchmarks.py`) and **Write-Conclusions** (Q2). Fetch-Flows publishes nothing to `reports/`.
