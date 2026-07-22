# SG Banks — Tables (generated table-block artifact)

> **Artifact:** `pipeline/sg-banks/data/tables.md` — sole output of `pipeline/sg-banks/method/code/build_tables.py` (the deterministic Build-Tables script; spec in `method/code/build-tables.md`). Consumed by the Build-Report step (`pipeline/sg-banks/method/ai/build-report.md`).
> **Provenance:** every number is a deterministic transform of reconciled `pipeline/sg-banks/data/ledger.csv` (582 data rows: 261 match · 119 single-px · 116 single-cl · 58 resolved · 17 n/d · 8 n/r · 3 text/other). Rerun `python3 pipeline/sg-banks/method/code/build_tables.py` to regenerate; same ledger in → same tables out.
> **Banks:** DBS (D05) · OCBC (O39) · UOB (U11). FY2016–FY2025 long-run base + **1Q2026 interim (quarters ended 31 Mar 2026)** + **current (2026-07-20 intraday) valuation.** **SGD only.**

**Contents:** Latest 1Q2026 snapshot · Tables 1 (per bank) · 2 · 3 · 4 (+ P/TB block) · 5, each with derived-line and superscript footnotes; plus table-level validation data for Appendix A. Narrative blocks are written by Assemble, not here.

---

## Latest 1Q2026 snapshot (quarters ended 31 Mar 2026)

> **Read with care — these lines are NOT fully cross-comparable:** reporting formats differ (DBS trading update · OCBC press release · UOB CFO/CEO slides via MarketScreener); UOB income-statement detail is **Tier-2 host** while DBS/OCBC are Tier-1; all cells are single-retriever (`single-cl`, stamped `20260720-001 CwClOpus4.8`) and not yet dual-checked. Wealth-AUM definitions differ across banks (see Table 2 note). **SGD.**

### 1Q2026 — income & returns

| Metric (1Q26) | DBS | OCBC | UOB | Note |
|---|---:|---:|---:|---|
| Net interest income (S$m) | 3,494 | 2,222 | 2,324 | UOB Tier-2 host; OCBC NII derived-to-tie |
| Non-interest income (S$m) | 2,454 | 1,606 | 1,098 | DBS & UOB derived (TI−NII); UOB slide components don't reconcile (see note) |
| Total income (S$m) | 5,948 | 3,828 | 3,422 | records at DBS & OCBC |
| Net fee income (S$m) | 1,482 | 675 | 637 | DBS +16% YoY · OCBC +24% YoY · UOB −8% YoY |
| Net profit (S$m) | 2,930 | 1,974 | 1,437 | +1% / +5% / −4% YoY |
| Group NIM (%) | 1.89 | 1.76 | 1.82 | all down YoY; OCBC steepest (−28bps) |
| ROE (%) | 17.0 | 13.0 | 11.5 | reported (group) |
| Cost/income (%) | 38.7 | 39.3 | 44.5 |  |

*NII + Non-II = Total income ties exactly for all three (DBS 3,494+2,454=5,948 · OCBC 2,222+1,606=3,828 · UOB 2,324+1,098=3,422). DBS non-II is derived (fee 1,482 + other 972); OCBC NII is derived-to-tie (TI 3,828 − non-II 1,606). **UOB non-II caveat:** UOB's CFO-slide components (net fee 637 + trading & investment 405 + other 462 = 1,504) do not reconcile with total income − NII (1,098); the tie-out-consistent derived 1,098 is shown and the slide split is flagged as an unresolved retrieval gap. Net profit = attributable to shareholders (reported).*

### 1Q2026 — attraction, balance sheet & asset quality (period-end 31 Mar 2026)

| Metric | DBS | OCBC | UOB | Note |
|---|---:|---:|---:|---|
| Customer deposits (S$m) | 629,868 | 444,000 | 427,000 |  |
| CASA ratio (%) | 55.0 | 50.2 | 57.0 | printed / mix basis differs |
| Wealth AUM (S$m) | 492,000 | 342,000 | 198,000 | **definitions differ — do not compare levels** |
| Total assets (S$m) | 935,365 | 703,124 | 574,000 | leverage only, not attraction |
| Gross loans (S$m) | 453,180 | 347,000 | 354,000 |  |
| CET1 ratio (%) | 16.9 | 17.0 | 15.3 |  |
| NPL ratio (%) | 1.0 | 0.9 | 1.5 |  |
| Credit cost (bps) | 14 | 23 | 26 | OCBC incl. S$191m overlay; UOB elevated |

***Never sum deposits + AUM** (double-count). Wealth-AUM levels are **not** cross-comparable — DBS "Wealth Management AUM"; OCBC group wealth incl. Bank of Singapore + Great Eastern; UOB "Group Retail AUM" (narrower, reclassified 1-Jan-2023). UOB balance-sheet/ratio lines are Tier-1 (UOB Financial Highlights); UOB CASA / wealth AUM / credit cost are Tier-2 host (UOB 1Q26 CFO slides via MarketScreener). OCBC credit cost includes S$191m management-overlay allowances for non-impaired assets.*

### 1Q2026 — current valuation (as of 2026-07-20, intraday)

| Metric | DBS | OCBC | UOB |
|---|---:|---:|---:|
| Price (S$, intraday 2026-07-20) | 71.96 | 28.60 | 42.60 |
| FY2025 BVPS (S$) | 24.29 | 13.38 | 29.36 |
| Current P/B | 2.96 | 2.14 | 1.45 |
| Current vs 10-yr avg P/B | +96% | +84% | +24% |
| FY2025 TBVPS (S$) | 22.07 | 12.41 | 26.36 |
| Current P/TB | 3.26 | 2.30 | 1.62 |

*Prices are **intraday 2026-07-20 (Perplexity Finance, SGX open) — NOT closing prices**; treat as a tier-2 market-data snapshot only. P/B = price ÷ FY2025 BVPS; P/TB = price ÷ FY2025 TBVPS (FY2025 per-share book denominators; 1Q26 per-share book not retrieved). These figures feed the Table 4 "Current P/B" rows and the P/TB "current" column.*

---

### Table 1 — DBS: Income Engine

| FY | Dep | Assets | NII | Other | TotalRev | Profit | NIM | Rev/Dep | Profit/Dep | Profit/Rev |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2016 | 347 | 482 | 7.3 | 4.2 | 11.5 | 4.2 | 1.80% | 0.033 | 0.012 | 0.37 |
| 2017 | 374 | 518 | 7.8 | 4.1 | 11.9 | 4.4 | 1.75% | 0.032 | 0.012 | 0.37 |
| 2018 | 394 | 551 | 9.0 | 4.2 | 13.2 | 5.6 | 1.85% | 0.033 | 0.014 | 0.43 |
| 2019 | 404 | 579 | 9.6 | 4.9 | 14.5 | 6.4 | 1.89% | 0.036 | 0.016 | 0.44 |
| 2020 | 465 | 650 | 9.1 | 5.5 | 14.6 | 4.7 | 1.62% | 0.031 | 0.010 | 0.32 |
| 2021 | 502 | 686 | 8.4 | 5.9 | 14.3 | 6.8 | 1.45% | 0.028 | 0.014 | 0.48 |
| 2022 | 527 | 743 | 10.9 | 5.6 | 16.5 | 8.2 | 1.75% | 0.031 | 0.016 | 0.50 |
| 2023 | 535 | 739 | 13.6 | 6.5 | 20.2 | 10.3 | 2.15% | 0.038 | 0.019 | 0.51 |
| 2024 | 562 | 827 | 14.4 | 7.9 | 22.3 | 11.4 | 2.13% | 0.040 | 0.020 | 0.51 |
| 2025 | 610 | 897 | 14.5 | 8.4 | 22.9 | 11.0 | 2.01% | 0.038 | 0.018 | 0.48 |
| **CAGR 21→25** | 5.0% | 6.9% | 14.5% | 9.4% | 12.5% | 12.9% |  |  |  |  |
| **CAGR 16→25** | 6.5% | 7.2% | 7.9% | 8.1% | 8.0% | 11.2% |  |  |  |  |

*Other = TotalRev − NII (derived). TotalRev = reported total income. Rev/Dep = TotalRev ÷ Deposits; Profit/Dep = Profit ÷ Deposits; Profit/Rev = Profit ÷ TotalRev (all dimensionless). CAGR = (end/start)^(1/n) − 1, on FY2021→FY2025 (4-yr) and FY2016→FY2025 (9-yr) bases. NIM = group net interest margin as reported. Profit = net profit attributable to shareholders (reported).*

### Table 1 — OCBC: Income Engine

| FY | Dep | Assets | NII | Other | TotalRev | Profit | NIM | Rev/Dep | Profit/Dep | Profit/Rev |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2016 | 261 | 410 | 5.1 | 3.4 | 8.5 | 3.5 | 1.67% | 0.032 | 0.013 | 0.41 |
| 2017 | 284 | 453 | 5.4 | 4.2 | 9.6 | 4.1 | 1.65% | 0.034 | 0.015 | 0.43 |
| 2018 | 295 | 468 | 5.9 | 3.8 | 9.7 | 4.5 | 1.70% | 0.033 | 0.015 | 0.46 |
| 2019 | 303 | 492 | 6.3 | 4.5 | 10.9 | 4.9 | 1.77% | 0.036 | 0.016 | 0.45 |
| 2020 | 315 | 521 | 6.0 | 4.2 | 10.1 | 3.6 | 1.61% | 0.032 | 0.011 | 0.35 |
| 2021 | 342 | 542 | 5.9 | 4.7 | 10.6 | 4.9 | 1.54% | 0.031 | 0.014 | 0.46 |
| 2022 | 350 | 557 | 7.7 | 3.6 | 11.3 | 5.5 [6] | 1.91% | 0.032 | 0.016 | 0.49 |
| 2023 | 364 | 581 | 9.6 | 3.9 | 13.5 | 7.0 | 2.28% | 0.037 | 0.019 | 0.52 |
| 2024 | 391 | 625 | 9.8 | 4.7 | 14.5 | 7.6 | 2.20% | 0.037 | 0.019 | 0.52 |
| 2025 | 428 | 676 | 9.2 | 5.5 | 14.6 | 7.4 | 1.91% | 0.034 | 0.017 | 0.51 |
| **CAGR 21→25** | 5.8% | 5.7% | 11.8% | 3.6% | 8.4% | 11.2% |  |  |  |  |
| **CAGR 16→25** | 5.6% | 5.7% | 6.8% | 5.3% | 6.2% | 8.8% |  |  |  |  |

*Other = TotalRev − NII (derived). TotalRev = reported total income. Rev/Dep = TotalRev ÷ Deposits; Profit/Dep = Profit ÷ Deposits; Profit/Rev = Profit ÷ TotalRev (all dimensionless). CAGR = (end/start)^(1/n) − 1, on FY2021→FY2025 (4-yr) and FY2016→FY2025 (9-yr) bases. NIM = group net interest margin as reported. Profit = net profit attributable to shareholders (reported). [6] FY2022 figures as restated for SFRS(I) 17 (insurance) in the FY2023 release.*

### Table 1 — UOB: Income Engine

| FY | Dep | Assets | NII | Other | TotalRev | Profit | NIM | Rev/Dep | Profit/Dep | Profit/Rev |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2016 | 255 | 340 | 5.0 | 3.1 | 8.1 | 3.1 | 1.71% | 0.032 | 0.012 | 0.38 |
| 2017 | 273 | 359 | 5.5 | 3.3 | 8.9 | 3.4 | 1.77% | 0.032 | 0.012 | 0.38 |
| 2018 | 293 | 388 | 6.2 | 2.9 | 9.1 | 4.0 | 1.82% | 0.031 | 0.014 | 0.44 |
| 2019 | 311 | 387 | 6.6 | 3.5 | 10.0 | 4.3 | 1.78% | 0.032 | 0.014 | 0.43 |
| 2020 | 325 | 424 | 6.0 | 3.1 | 9.2 | 2.9 | 1.57% | 0.028 | 0.009 | 0.32 |
| 2021 | 353 | 459 | 6.4 | 3.4 | 9.8 | 4.1 | 1.56% | 0.028 | 0.012 | 0.42 |
| 2022 | 369 | 504 | 8.3 | 3.2 | 11.6 | 4.6 | 1.86% | 0.031 | 0.012 | 0.40 |
| 2023 | 385 | 524 | 9.7 | 4.3 | 13.9 | 5.7 | 2.09% | 0.036 | 0.015 | 0.41 |
| 2024 | 404 | 538 | 9.7 | 4.6 | 14.3 | 6.0 | 2.03% | 0.035 | 0.015 | 0.42 |
| 2025 | 426 | 572 | 9.4 | 4.5 | 13.8 | 4.7 [5] | 1.89% | 0.032 | 0.011 | 0.34 |
| **CAGR 21→25** | 4.8% | 5.6% | 10.0% | 7.0% | 9.0% | 3.5% |  |  |  |  |
| **CAGR 16→25** | 5.9% | 5.9% | 7.2% | 4.2% | 6.2% | 4.7% |  |  |  |  |

*Other = TotalRev − NII (derived). TotalRev = reported total income. Rev/Dep = TotalRev ÷ Deposits; Profit/Dep = Profit ÷ Deposits; Profit/Rev = Profit ÷ TotalRev (all dimensionless). CAGR = (end/start)^(1/n) − 1, on FY2021→FY2025 (4-yr) and FY2016→FY2025 (9-yr) bases. NIM = group net interest margin as reported. Profit = net profit attributable to shareholders (reported). [5] FY2025 profit −23% is a provisioning artefact: ~S$2.0bn pre-emptive general allowances booked 3Q2025; operating profit was −4%; UOB core net profit ≈ S$4.82bn (FY2022) / S$6.06bn (FY2023) where separately disclosed.*

---

### Table 2 — Attracted assets: deposits, CASA & wealth AUM

| FY | DBS Dep | DBS CASA | DBS AUM | OCBC Dep | OCBC CASA | OCBC AUM | UOB Dep | UOB CASA | UOB AUM |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2016 | 347 | 61.8% | 166 | 261 | 51.1% [c1] | n/d | 255 | 44.5% | 93 |
| 2017 | 374 | 62.3% | 206 | 284 | 49.2% [c1] | n/d | 273 | 45.5% | 104 |
| 2018 | 394 | 58.6% | 220 | 295 | 46.4% [c1] | 258 | 293 | 44.5% | n/d |
| 2019 | 404 | 59.0% | 246 | 303 | 48.4% | 265 | 311 | 45.4% | n/d |
| 2020 | 465 | 72.7% | 264 | 315 | 60.3% | 241 | 325 | 53.5% | 134 |
| 2021 | 502 | 76.0% | 291 | 342 | 63.3% | 258 | 353 | 56.2% | 139 |
| 2022 | 527 | 60.3% | 297 | 350 | 51.8% | 258 | 369 | 47.5% | 154 |
| 2023 | 535 | 53.4% | 365 | 364 | 48.7% | 263 | 385 | 48.9% [u1] | 176 |
| 2024 | 562 | 51.8% | 426 | 391 | 48.8% | 299 | 404 | 54.7% [u1] | 190 |
| 2025 | 610 | 54.5% | 488 | 428 | 50.7% | 343 | 426 | 58.4% [u1] | 201 |
| **CAGR 21→25** | 5.0% |  | 13.8% | 5.8% |  | 7.4% | 4.8% |  | 9.7% |
| **CAGR 16→25** | 6.5% |  | 12.7% | 5.6% |  | n/r | 5.9% |  | 8.9% |

*Deposits = total non-bank customer deposits (group). CASA = (current + savings) / total customer deposits, as printed by each bank where available. Wealth AUM = bank-reported wealth / private-bank AUM. [c1] OCBC 2016–2018 CASA sourced from OCBC FY-results presentations (Tier-1) via a non-Claude retrieval pass (2026-07-16), computer-verified against source PDFs; currently `single-px` pending a second retriever. [u1] UOB CASA lifted ~48% → 58% (2023→25) mainly on post-rate-cycle deposit remix (customers rotating back from fixed deposits) plus mix contribution from the Citi consumer (deposit-heavy) book. CASA is a point-in-time ratio — CAGR cells intentionally blank. AUM: OCBC 2016–17 and UOB 2018–19 = `n/d` (not disclosed in that vintage of results decks). AUM definitions differ across banks (DBS "Wealth Management AUM"; OCBC group/banking wealth incl. Bank of Singapore + Great Eastern; UOB narrower, reclassified 1 Jan 2023) — read within-bank trends, not cross-bank levels. Never sum Deposits + AUM (double-count risk).*

---

### Table 3 — Net interest margin (Group) & NII

| FY | DBS NII | DBS NIM | OCBC NII | OCBC NIM | UOB NII | UOB NIM |
|---|---:|---:|---:|---:|---:|---:|
| 2016 | 7.30 | 1.80% | 5.05 | 1.67% | 4.99 | 1.71% |
| 2017 | 7.79 | 1.75% | 5.42 | 1.65% | 5.53 | 1.77% |
| 2018 | 8.96 | 1.85% | 5.89 | 1.70% | 6.22 | 1.82% |
| 2019 | 9.62 | 1.89% | 6.33 | 1.77% | 6.56 | 1.78% |
| 2020 | 9.08 | 1.62% | 5.97 | 1.61% | 6.04 | 1.57% |
| 2021 | 8.44 | 1.45% | 5.86 | 1.54% | 6.39 | 1.56% |
| 2022 | 10.94 | 1.75% | 7.69 | 1.91% | 8.34 | 1.86% |
| 2023 | 13.64 | 2.15% | 9.64 | 2.28% | 9.68 | 2.09% |
| 2024 | 14.42 | 2.13% | 9.76 | 2.20% | 9.67 | 2.03% |
| 2025 | 14.50 | 2.01% | 9.15 | 1.91% | 9.36 | 1.89% |

*NIM = group net interest margin, %, as printed by each bank; NII in S$bn (2 dp). DBS uses **group** NIM (not the commercial-book series, which was 2.80% in FY2024); canary FY2025 group NIM = 2.01%.*

---

### Table 4 — Valuation & Returns (P/B + ROE)

| FY | DBS Price | DBS BVPS | DBS P/B | DBS ROE | DBS RoTE | OCBC Price | OCBC BVPS | OCBC P/B | OCBC ROE | OCBC RoTE | UOB Price | UOB BVPS | UOB P/B | UOB ROE | UOB RoTE |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2016 | 17.34 | 16.87 | 1.03 | 10.1 | n/d | 8.92 | 8.49 | 1.05 | 10.0 | n/d | 20.40 | 18.82 | 1.08 | 10.2 | n/d |
| 2017 | 24.85 | 17.85 | 1.39 | 9.7 | n/d | 12.39 | 8.96 | 1.38 | 11.2 | n/d | 26.45 | 20.37 | 1.30 | 10.2 | n/d |
| 2018 | 23.69 | 18.12 | 1.31 | 12.1 | n/d | 11.26 | 9.56 | 1.18 | 11.5 | n/d | 24.57 | 21.31 | 1.15 | 11.3 | n/d |
| 2019 | 25.88 | 19.17 | 1.35 | 13.2 | n/d | 10.98 | 10.38 | 1.06 | 11.4 | n/d | 26.41 | 22.33 | 1.18 | 11.6 | n/d |
| 2020 | 25.04 | 20.08 | 1.25 | 9.1 | n/d | 10.21 | 10.82 | 0.94 | 7.6 | n/d | 22.75 | 23.03 | 0.99 | 7.4 | n/d |
| 2021 | 32.66 | 21.47 | 1.52 | 12.5 | 13.8 | 11.40 | 11.46 | 0.99 | 9.6 | n/d | 26.90 | 24.08 | 1.12 | 10.2 | n/d |
| 2022 | 33.92 | 21.17 | 1.60 | 15.0 | 16.7 | 12.18 | 10.99 | 1.11 | 11.1 | n/d | 30.70 | 24.24 | 1.27 | 11.9 | n/d |
| 2023 | 33.41 | 23.14 | 1.44 | 18.0 | 20.0 | 13.00 | 11.77 | 1.10 | 13.7 | n/d | 28.45 | 26.00 | 1.09 | 13.4 | n/d |
| 2024 | 43.72 | 23.38 | 1.87 | 18.0 | 20.0 | 16.69 | 12.80 | 1.30 | 13.7 | n/d | 36.33 | 28.11 | 1.29 | 13.3 | n/d |
| 2025 | 56.36 | 24.29 | 2.32 | 16.2 | 17.8 | 19.76 | 13.38 | 1.48 | 12.6 | n/d | 35.06 | 29.36 | 1.19 | 9.6 [5] | n/d |
| **10-yr avg P/B** |  |  | 1.51 |  |  |  |  | 1.16 |  |  |  |  | 1.17 |  |  |
| **5-yr avg P/B (21–25)** |  |  | 1.75 |  |  |  |  | 1.20 |  |  |  |  | 1.19 |  |  |
| **Current P/B** |  |  | 2.96 |  |  |  |  | 2.14 |  |  |  |  | 1.45 |  |  |
| **Current vs 10-yr avg** |  |  | +96% |  |  |  |  | +84% |  |  |  |  | +24% |  |  |
| **10-yr avg ROE** |  |  |  | 13.4 |  |  |  |  | 11.2 |  |  |  |  | 10.9 |  |

*P/B = 31-Dec close ÷ BVPS for FY rows (derived; both inputs shown). ROE reported (group). RoTE: DBS discloses FY2021+ (`n/d` before); OCBC and UOB do not print RoTE → `n/d`. [5] UOB FY2025 ROE = 9.6 reflects the ~S$2.0bn pre-emptive GP booked 3Q2025 (provisioning artefact); UOB core ROE ≈ 14.2% (FY2023) where separately disclosed. DBS 1-for-10 bonus issue (1Q2024): price and BVPS kept on the same basis within each year — P/B is bonus-invariant; do not mix adjusted price with unadjusted BVPS. **Current P/B uses the intraday 2026-07-20 price (71.96 / 28.60 / 42.60 — NOT a closing price) ÷ FY2025 BVPS** (see the 1Q2026 snapshot valuation table).*

**P/TB block (FY2025)**

| Bank | BVPS | Goodwill+Intang (S$m) | Shares (m) | TBVPS | P/TB (FY25 close) | P/TB (current) |
|---|---:|---:|---:|---:|---:|---:|
| DBS | 24.29 | 6314 | 2838 | 22.07 | 2.55 | 3.26 |
| OCBC | 13.38 | 4360 | 4490 | 12.41 | 1.59 | 2.30 |
| UOB | 29.36 | 4953 | 1652 | 26.36 | 1.33 | 1.62 |

*TBVPS = BVPS − (Goodwill + Intangibles) / Shares outstanding. P/TB (FY25 close) uses the 31-Dec-2025 close; **P/TB (current) uses the intraday 2026-07-20 price (71.96 / 28.60 / 42.60) — not a closing price.** P/TB derived from stated prices. Historical P/TB not shown — per-year goodwill was not retrieved.*

---

### Table 5 — NIM vs the rate cycle

| FY | DBS NIM | OCBC NIM | UOB NIM | 3M SORA (31-Dec) | 3M SORA (FY avg) | Fed upper (31-Dec) | EFFR (FY avg) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2016 | 1.80% | 1.67% | 1.71% | n/r | n/r | 0.75 | 0.40 |
| 2017 | 1.75% | 1.65% | 1.77% | n/r | n/r | 1.50 | 1.00 |
| 2018 | 1.85% | 1.70% | 1.82% | n/r | n/r | 2.50 | 1.83 |
| 2019 | 1.89% | 1.77% | 1.78% | n/r | n/r | 1.75 | 2.16 |
| 2020 | 1.62% | 1.61% | 1.57% | 0.12 | 0.10 | 0.25 | 0.38 |
| 2021 | 1.45% | 1.54% | 1.56% | 0.19 | 0.17 | 0.25 | 0.08 |
| 2022 | 1.75% | 1.91% | 1.86% | 2.94 | 1.08 | 4.50 | 1.68 |
| 2023 | 2.15% | 2.28% | 2.09% | 3.74 | 3.54 | 5.50 | 5.02 |
| 2024 | 2.13% | 2.20% | 2.03% | 3.14 | 3.58 | 4.50 | 5.14 |
| 2025 | 2.01% | 1.91% | 1.89% | 1.26 | 2.06 | 3.75 | 4.21 |
| 2026 latest (1Q26) | 1.89% | 1.76% | 1.82% | n/d | 1.07* | 3.75 | 3.62 |

*NIM from Table 3 (group), with `%` symbol per 2dp format. **2026-latest NIM row is 1Q2026 group NIM** (quarter ended 31 Mar 2026), all down YoY. 3M compounded SORA (MAS) exists only from 6-Aug-2020 → pre-2020 = `n/r` (no SIBOR splice). **3M SORA (31-Dec) 2026 = `n/d`**: MAS eServices statistics portal under scheduled maintenance on 2026-07-20; latest official single-day value not retrievable. **\*3M SORA (FY avg) 2026 = 1.07 is the bank-characterised 1Q26 average** ([DBS 1Q26 media transcript](https://www.dbs.com/iwov-resources/images/investors/quarterly-financials/2026/1Q26_media_transcript.pdf)), **not an official MAS FY figure**. Fed funds target upper = FRED `DFEDTARU` (3.75, held at the [17-Jun-2026 FOMC](https://www.federalreserve.gov/newsevents/pressreleases/monetary20260617a.htm)); effective fed funds (FY avg) = FRED `DFF`, 2026 YTD ≈ 3.62. 2026-latest rates as of mid-July 2026.*

---

## Table-level validation data (for Appendix A)

**Gates (recomputed this build):** NII + Non-II = Total income exact (≤S$1m residual) for every filled bank-period · DBS FY2025 group-NIM canary = 2.01 · all values SGD · no poison-pill values present.

**Material resolved rows (checksum ≠ reconciled, non-rounding):**

| Row | Checksum | Reconciled | Cause |
|---|---:|---:|---|
| UOB_NII_2022 | 8300 | 8343 | reconciled 8343 vs checksum 8300; NII basis — checksum stale, agents agree |
| DBS_TotalIncome_2018 | 13200 | 13183 | auto: px/cl/checksum disagreement resolved to reconciled_value |
| DBS_TotalIncome_2021 | 14300 | 14297 | px 14188 vs cl 14297; cl closer to checksum 14300 — took cl |
| OCBC_NonII_2022 | 3990 | 3598 | reconciled 3598 vs checksum 3990; SFRS(I) 17 insurance restatement (B6) — restated figure taken |
| DBS_NetProfit_2018 | 5630 | 5625 | px 5577 vs cl 5625; cl closer to checksum 5630 — took cl |
| DBS_NetProfit_2024 | 11400 | 11408 | auto: px/cl/checksum disagreement resolved to reconciled_value |
| DBS_NetProfit_2025 | 11000 | 11033 | auto: px/cl/checksum disagreement resolved to reconciled_value |
| OCBC_NetProfit_2021 | 4860 | 4858 | auto: px/cl/checksum disagreement resolved to reconciled_value |
| OCBC_NetProfit_2022 | 5750 | 5526 | reconciled 5526 vs checksum 5750; SFRS(I) 17 insurance restatement (B6) — restated figure taken |
| OCBC_NetProfit_2025 | 7420 | 7422 | auto: px/cl/checksum disagreement resolved to reconciled_value |
| UOB_NetProfit_2023 | 5710 | 5711 | auto: px/cl/checksum disagreement resolved to reconciled_value |
| UOB_NetProfit_2025 | 4680 | 4682 | auto: px/cl/checksum disagreement resolved to reconciled_value |
| UOB_ROE_2025 | 10.1 | 9.6 | reconciled 9.6 vs checksum 10.1; FY2025 provisioning artefact (B5, ~S$2.0bn pre-emptive GP 3Q2025) — agents agree on 9.6 reported |
| DBS_NetFee_2022 | 3090 | 3091 | auto: px/cl/checksum disagreement resolved to reconciled_value |
| DBS_NetFee_2024 | 4170 | 4168 | auto: px/cl/checksum disagreement resolved to reconciled_value |
| DBS_NetFee_2025 | 4900 | 4898 | auto: px/cl/checksum disagreement resolved to reconciled_value |
| OCBC_NetFee_2021 | 2250 | 2245 | auto: px/cl/checksum disagreement resolved to reconciled_value |
| OCBC_NetFee_2022 | 1850 | 1851 | auto: px/cl/checksum disagreement resolved to reconciled_value |
| UOB_NetFee_2021 | 2400 | 2412 | auto: px/cl/checksum disagreement resolved to reconciled_value |
| UOB_NetFee_2022 | 2100 | 2143 | reconciled 2143 vs checksum 2100; Citi consumer integration uplift (B4/B6) — agents agree |
| UOB_NetFee_2023 | 2200 | 2235 | reconciled 2235 vs checksum 2200; Citi consumer integration uplift (B4/B6) — agents agree |
| OCBC_Wealth_2022 | 3890 | 3420 | reconciled 3420 vs checksum 3890; wealth-income basis (B3) — agents agree |

Other `resolved` rows: 15 rounding-level (±S$1–25m vs a rounded checksum; agents agree).

**`n/r` inventory (8):** RATE_SORA_YE_2016, RATE_SORA_AVG_2016, RATE_SORA_YE_2017, RATE_SORA_AVG_2017, RATE_SORA_YE_2018, RATE_SORA_AVG_2018, RATE_SORA_YE_2019, RATE_SORA_AVG_2019

**`n/d` inventory (17):** UOB_Wealth_2016, UOB_Wealth_2017, UOB_Wealth_2018, UOB_Wealth_2019, UOB_Wealth_2020, UOB_Wealth_2021, UOB_Wealth_2022, OCBC_WealthAUM_2016, OCBC_WealthAUM_2017, UOB_WealthAUM_2018, UOB_WealthAUM_2019, DBS_RoTE_2016, DBS_RoTE_2017, DBS_RoTE_2018, DBS_RoTE_2019, DBS_RoTE_2020, RATE_SORA_YE_2026
