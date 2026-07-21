# SG Banks — Signals (qualitative scan output)

> **Project:** Singapore Bank Stock Accumulation Strategy
> **Artifact:** `pipeline/sg-banks/data/signals.md` — sole output of `pipeline/sg-banks/method/scan-signals.md`.
> **Status:** **POPULATED — 1Q2026 scan run 2026-07-20.** Grounded strictly in the supplied evidence set (`sg_banks_evidence_report_2026-07-20.md`); every signal carries its dated Tier-1/Tier-2 source URL. **Descriptive only — not investment advice.**
> **Banks:** DBS (D05) · OCBC (O39) · UOB (U11). **Recency window:** 1Q2026 results (quarters ended 31 Mar 2026, announced 30 Apr–8 May 2026) + FY2026 guidance + latest macro (to mid-Jul 2026).

---

## Run status

- **Last run:** 2026-07-20 (1Q2026 refresh).
- **Model / harness:** Claude Opus 4.8 (Cowork), closed to live search — signals transcribed and tiered from the pre-fetched evidence set only, not independently re-searched.
- **Recency window covered:** latest 1–2 quarters (1Q2026) + current FY2026 guidance + macro rates to mid-July 2026.
- **Tiering:** Tier 1 = bank IR / MAS / Fed primary disclosure. Tier 2 = reputable media, or the bank's own slides redistributed via an aggregator ("Tier-2 host"). DBS and OCBC 1Q26 signals are Tier 1; **all UOB 1Q26 income-statement signals are Tier 2** (UOB's own CFO/CEO slides via MarketScreener + Bloomberg/Business Times) because UOB's own PDFs were not directly retrievable in-session.

**Polarity:** (+) positive · (−) negative/risk. Per-bank balance below satisfies ≥3 positive and ≥3 negative each.

- **DBS:** 3 (+) · 3 (−)  · **OCBC:** 3 (+) · 3 (−)  · **UOB:** 3 (+) · 4 (−)

**Bearing** maps to `frame.md` key questions: `attraction` · `income-durability` · `rate-cycle` · `fee-offset` · `valuation` · `credit-quality` · `data-confidence`.

---

## Tier 1 — primary company disclosure (bank IR / MAS / Fed)

### DBS
| Pol | Signal | Date | Source | Bearing |
|---|---|---|---|---|
| + | Record 1Q26 total income S$5.95bn and net profit S$2.93bn (+1% YoY, +24% QoQ), beating consensus; ROE 17.0% | 2026-04-30 | [DBS 1Q26 Trading Update](https://www.dbs.com/iwov-resources/images/investors/quarterly-financials/2026/1Q26_trading_update.pdf) | income-durability |
| + | Wealth AUM record S$492bn (+17% YoY cc); net new money +S$10bn; wealth fees +25% YoY — structural franchise offset to NIM | 2026-04-30 | [DBS 1Q26 CFO presentation](https://www.dbs.com/iwov-resources/images/investors/quarterly-financials/2026/1Q26_CFO_presentation.pdf); [DBS 1Q26 media transcript](https://www.dbs.com/iwov-resources/images/investors/quarterly-financials/2026/1Q26_media_transcript.pdf) | attraction / fee-offset |
| + | Guidance upgraded: FY26 net profit "good shot at coming close to 2025 levels," better than prior "below 2025" | 2026-04-30 | [DBS 1Q26 media transcript](https://www.dbs.com/iwov-resources/images/investors/quarterly-financials/2026/1Q26_media_transcript.pdf) | income-durability |
| − | NII −5% YoY to S$3.49bn; group NIM 1.89% (−23bps YoY) as 3M SORA fell from ~2.54% to ~1.07% | 2026-04-30 | [DBS 1Q26 Trading Update](https://www.dbs.com/iwov-resources/images/investors/quarterly-financials/2026/1Q26_trading_update.pdf) | rate-cycle |
| − | Expenses +4% YoY (higher staff costs); profit before allowances −1% | 2026-04-30 | [DBS 1Q26 Trading Update](https://www.dbs.com/iwov-resources/images/investors/quarterly-financials/2026/1Q26_trading_update.pdf) | income-durability |
| − | Iran/Middle East war raises macro uncertainty; general-provision release deferred pending outcome | 2026-04-30 | [DBS 1Q26 media transcript](https://www.dbs.com/iwov-resources/images/investors/quarterly-financials/2026/1Q26_media_transcript.pdf) | credit-quality |

### OCBC
| Pol | Signal | Date | Source | Bearing |
|---|---|---|---|---|
| + | 1Q26 net profit S$1.97bn (+5% YoY, +13% QoQ), a beat; record total income S$3.83bn and record non-interest income S$1.61bn (+23% YoY) | 2026-05-08 | [OCBC 1Q26 Press Release](https://www.ocbc.com/group/media/release/2026/ocbc-group-first-quarter-2026-net-profit-up-5percent.page) | fee-offset / income-durability |
| + | Wealth fees +34% YoY (S$422m); wealth AUM S$342bn (+12% YoY); wealth income ~39% of total | 2026-05-08 | [OCBC 1Q26 Press Release](https://www.ocbc.com/group/media/release/2026/ocbc-group-first-quarter-2026-net-profit-up-5percent.page) | attraction / fee-offset |
| + | Asset quality clean: NPL 0.9% steady for 8 quarters; new corporate NPA formation fell to S$123m (from S$399m in 4Q25); NPA coverage 163% | 2026-05-08 | [OCBC 1Q26 Press Release](https://www.ocbc.com/group/media/release/2026/ocbc-group-first-quarter-2026-net-profit-up-5percent.page) | credit-quality |
| − | NII −5% YoY; group NIM 1.76% (−28bps YoY, −10bps QoQ) — steepest NIM compression among the three | 2026-05-08 | [OCBC 1Q26 Press Release](https://www.ocbc.com/group/media/release/2026/ocbc-group-first-quarter-2026-net-profit-up-5percent.page) | rate-cycle |
| − | Set aside S$191m allowances for non-impaired assets (management overlays) citing "elevated uncertainties" — comparability distortion & caution signal | 2026-05-08 | [OCBC 1Q26 Press Release](https://www.ocbc.com/group/media/release/2026/ocbc-group-first-quarter-2026-net-profit-up-5percent.page) | credit-quality |
| − | ROE 13.0% remains below DBS; total NPAs +7% YoY to S$3.12bn | 2026-05-08 | [OCBC 1Q26 Press Release](https://www.ocbc.com/group/media/release/2026/ocbc-group-first-quarter-2026-net-profit-up-5percent.page) | valuation / credit-quality |

### Macro (Tier 1 — Fed / MAS)
| Pol | Signal | Date | Source | Bearing |
|---|---|---|---|---|
| − | Fed held funds target at 3.50–3.75% (17 Jun 2026 FOMC, first under Chair Warsh); dot plot turned hawkish (median 2026 ~3.8%) — banks now assume zero 2026 Fed cuts | 2026-06-17 | [Federal Reserve FOMC statement, 17 Jun 2026](https://www.federalreserve.gov/newsevents/pressreleases/monetary20260617a.htm); [FOMC minutes, 16–17 Jun 2026](https://www.federalreserve.gov/monetarypolicy/fomcminutes20260617.htm) | rate-cycle |
| − | 3M SORA averaged ~1.07% in 1Q26 vs ~2.54% in 1Q25 ("less than half of a year ago"), driving group-wide NIM compression | 2026-04-30 | [DBS 1Q26 media transcript](https://www.dbs.com/iwov-resources/images/investors/quarterly-financials/2026/1Q26_media_transcript.pdf) | rate-cycle |
| n/d | Latest official single-day 3M compounded SORA not retrievable — MAS eServices statistics portal under scheduled maintenance during this session | 2026-07-20 | [MAS domestic interest rates eServices](https://eservices.mas.gov.sg/statistics/dir/domesticinterestrates.aspx) (portal under maintenance); [MAS SORA page](https://www.mas.gov.sg/monetary-policy/sora) (methodology) | data-confidence / rate-cycle |

---

## Tier 2 — reputable media & bank slides via aggregator (Tier-2 host)

### UOB
| Pol | Signal | Date | Source | Bearing |
|---|---|---|---|---|
| + | 1Q26 net profit S$1.44bn beat consensus (~S$1.39bn) by ~3% on tight cost control; NIM held QoQ at 1.82% (+2bps) as funding-cost management offset asset repricing | 2026-05-07 | [UOB 1Q26 CFO Slides (via MarketScreener)](https://www.marketscreener.com/news/united-overseas-bank-uob-group-1q26-trading-update-cfo-slides-ce7f58d2d18df127); [Business Times, 7 May 2026](https://www.businesstimes.com.sg/companies-markets/uob-aims-double-wealth-income-least-s2-5-billion-2030-q1-profit-slips-4) | income-durability / rate-cycle |
| + | Global Markets / trading & investment income rebounded to S$405m (+88% QoQ); CET1 strengthened to 15.3% | 2026-05-07 | [UOB 1Q26 CFO Slides (via MarketScreener)](https://www.marketscreener.com/news/united-overseas-bank-uob-group-1q26-trading-update-cfo-slides-ce7f58d2d18df127) | income-durability |
| + | Strategic pivot: targets wealth income of at least S$2.5bn by 2030; +S$1bn net new money in 1Q26 | 2026-05-07 | [Business Times, 7 May 2026](https://www.businesstimes.com.sg/companies-markets/uob-aims-double-wealth-income-least-s2-5-billion-2030-q1-profit-slips-4) | attraction / fee-offset |
| − | Net profit −4% YoY; third consecutive quarter of YoY declines in both total income and net profit | 2026-05-07 | [UOB 1Q26 CFO Slides (via MarketScreener)](https://www.marketscreener.com/news/united-overseas-bank-uob-group-1q26-trading-update-cfo-slides-ce7f58d2d18df127) | income-durability |
| − | Greater China NPAs rose (China NPL ratio ~3.5% from 3.3%, CRE stress); credit costs elevated at 26bps on higher specific provisions | 2026-05-06 | [Bloomberg, 6 May 2026](https://www.bloomberg.com/news/articles/2026-05-06/uob-profit-dips-on-lending-income-ceo-says-uncertainty-elevated) | credit-quality |
| − | Net fee income −8% YoY to S$637m (off record 1Q25 base) as IB/loan-related and card fees softened; non-II only ~32.1% of income vs ~37% target | 2026-05-07 | [UOB 1Q26 CFO Slides (via MarketScreener)](https://www.marketscreener.com/news/united-overseas-bank-uob-group-1q26-trading-update-cfo-slides-ce7f58d2d18df127); [Business Times, 7 May 2026](https://www.businesstimes.com.sg/companies-markets/uob-aims-double-wealth-income-least-s2-5-billion-2030-q1-profit-slips-4) | fee-offset |
| − | CEO: "global uncertainty remains elevated"; FY2026 guidance only maintained (fee guidance already trimmed to high single-digit at FY25) | 2026-05-06 | [Bloomberg, 6 May 2026](https://www.bloomberg.com/news/articles/2026-05-06/uob-profit-dips-on-lending-income-ceo-says-uncertainty-elevated) | income-durability |

---

## Retrieval gaps recorded during this scan

- **UOB income-statement detail is Tier-2 host.** UOB.com direct PDF links were not retrievable in-session; NII, NIM, total income, fees, allowances, CASA and wealth AUM come from UOB's own CFO/CEO slides redistributed via MarketScreener. Values are UOB's own numbers but should be re-pulled from uobgroup.com IR before final publication. ([UOB 1Q26 CFO Slides](https://www.marketscreener.com/news/united-overseas-bank-uob-group-1q26-trading-update-cfo-slides-ce7f58d2d18df127))
- **UOB non-II components do not reconcile.** Slide breakdown (net fee 637 + T&I 405 + other 462 = 1,504) ≠ total income − NII (3,422 − 2,324 = 1,098). The tie-out-consistent derived non-II (1,098) is used downstream; the component split is unresolved.
- **Official 3M compounded SORA single-day value = `n/d`** — MAS statistics portal under maintenance 2026-07-20; interim context uses the bank-characterised 1Q26 average ~1.07% (DBS transcript). Re-fetch before publishing a hard number.
- **DBS FY2026 numeric guidance = `n/r`** — DBS gives qualitative guidance only; no numeric NIM/fee/credit-cost target.
- **OCBC/UOB official full earnings-call transcripts** not retrieved — only DBS's official transcript is Tier 1; OCBC/UOB call content is via press releases (Tier 1) or media/analyst notes (Tier 2).

<sub>Signals are descriptive statements of what was disclosed or reported, each dated and source-linked. No investment recommendation is expressed or implied. Tier-2 signals are used only where Tier-1 primary disclosure was not directly retrievable in-session.</sub>
