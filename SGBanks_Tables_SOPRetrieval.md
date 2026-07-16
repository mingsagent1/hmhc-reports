# SOP 1 — Raw Data Retrieval (SG Banks · CoreTables)

> **Project:** Singapore Bank Stock Accumulation Strategy
> **Artifact:** `SGBanks · CoreTables · SOP-Retrieval` — **260716-161218** (timestamp id — see filename)
> **Status:** Draft — not yet validated by a full two-agent run.
> **Pairs with:** `SGBanks_CoreTables_Ledger_260716-161218.csv` (its output) → `SGBanks_CoreTables_SOP-Report_260716-161218.md` (next stage).
> **Supersedes:** ad-hoc brief `SOP_BankDataAndTables.md`.
> **Ledger schema:** v0.2 (adds `px_version` / `cl_version` run-stamp columns, format `YYYYMMDD-NNN <Harness><Model>`).
> **Changelog:** v0.1 — Split retrieval from report-build (was one monolithic brief); output is now a shared reconciliation ledger, not a report; added customer-deposits, total-assets and wealth-AUM rows; checksums embedded per row.
> · **rev 2026-07-16:** added deposit-mix / CASA to retrieval scope (`CurrentAccts`, `SavingsDep`, `CASAratio`).

**Role of this SOP.** This is the *retrieval* stage. Your only job is to fill a shared raw-data ledger (CSV) with atomic, sourced numbers. You do **not** build tables, compute CAGRs/P/B, or write a report — that happens in SOP 2. One row = one number.

**Who runs this.** Any retrieval agent (Perplexity Computer, Claude Cowork, etc.). Each agent fills *its own three columns*. The ledger already contains a prior Claude pass in the `cl_*` columns; a Perplexity run fills the `px_*` columns; add more triplets for more agents.

**Banks & period.** DBS (SGX: D05), OCBC (SGX: O39), UOB (SGX: U11). FY2016–FY2025 (all 31-Dec year-ends) + latest 2026 interim. **SGD only — never convert, never USD, never ADRs (DBSDY/OVCHY/UOVEY etc.).**

---

## 1. The ledger you are filling

File: `SGBanks_CoreTables_Ledger_260716-161218.csv` (schema v0.2). One row per data point. Columns:

| Column | Who fills | Meaning |
|---|---|---|
| `data_point_id` | pre-set | Stable key, e.g. `OCBC_NIMgroup_2022`. Do not rename. |
| `bank` / `metric` / `period` / `unit` | pre-set | What the number is and its unit (`%`, `S$m`, `S$`, `m`, `text`). Report in the stated unit. |
| `checksum_expected` / `checksum_note` | pre-set | A known-verified value (from §E) where one exists. **If your number disagrees, do NOT overwrite — report the disagreement in your comment.** |
| `px_value` / `px_source` / `px_comment` | **you (Perplexity)** | Your value, its citation, and any note. |
| `px_version` | **you** | Run stamp for your fill (see **Provenance stamp** below). Stamp every cell you fill; leave blank if unfilled. Lets a later partial refresh, and the *model correlation* between agents, be traced. |
| `cl_value` / `cl_source` / `cl_comment` / `cl_version` | Claude | Prior Claude run (already filled for most rows), with its own run stamp. Leave as-is. |

**Provenance stamp format** — `YYYYMMDD-NNN <Harness><Model>`:
- `YYYYMMDD-NNN` — run date + sequence (e.g. `20260716-001`; bump `NNN` for re-runs the same day).
- `<Harness>` — the tool orchestrating retrieval: `Px` = Perplexity, `Cw` = Cowork/Claude Code, etc.
- `<Model>` — the model actually doing the extraction: `ClOpus4.8` = Claude Opus 4.8, `GPT…`, `Gemini…`. If a run mixes models, record the **predominant** one and note "mixed" in the comment.
- Examples: `20260716-001 PxClOpus4.8` (Perplexity harness, Claude Opus 4.8) · `20260716-001 CwClOpus4.8` (Cowork, Claude Opus 4.8).
- **Why it matters:** when two agents *agree* on a cell that has no checksum, that agreement is only strong evidence if the stamps show **different models**. Same-model agreement (both `…ClOpus4.8`) can share a blind spot — lean on the checksum / Tier-1 citation there instead. For maximum independence, run the external retriever on a **non-Claude model** where the harness allows it.
| `reconciled_value` / `reconciliation_status` / `reconciliation_note` | SOP 2 | Leave blank. The report stage fills these. |

**Rules for your columns**
- `px_value`: the raw number only, in the row's `unit`. No "%", no "S$", no commas inside the CSV field beyond what's quoted. For `text` rows (guidance) write the verbatim phrase.
- `px_source`: **document type + fiscal period + page/table/section**. A value with no usable citation is worthless — leave `px_value` blank and mark `n/r` in the comment instead of guessing.
- `px_comment`: basis notes, restatement flags, "does not tie", checksum disagreements, or why it's `n/r`/`n/d`.
- Fill **every** row you can. Where you cannot retrieve from a Tier-1 source, put `n/r` in `px_value` (not a guess). Where the bank does not disclose it at all, put `n/d`.
- **Do not compute derived quantities** (Non-NII by subtraction, CAGRs, P/B, tangible book). Report only what the source prints. (Exception: if a bank prints total income and NII but not the non-II line, you may report non-II and tag `px_comment` = "derived = TI−NII".)

**Priority holes** (rows currently blank in `cl_*` — these are where you add the most value): `CustomerDeposits`, `TotalAssets`, `WealthAUM`, DBS & UOB `Wealth`, DBS `RoTE` 2021–2023, all `SORA_*`, and the OCBC current price.

---

## 2. Source hierarchy — mandatory, in this order

**Tier 1 — Company reports. Use for EVERY fundamental (NIM, NII, non-II, net fee, wealth income, total income, ROE, RoTE, BVPS, net profit, CET1, NPL, deposits, total assets, AUM).**
1. The **Ten-Year / Five-Year Financial Summary** or **Financial Highlights** page in each Annual Report — one page fills most of this. *OCBC publishes a "Download Historical Financials" file on Investor Relations → Financial Results — get it first.*
2. The bank's **full-year results media release / performance summary** for each FY.
3. **Condensed / audited financial statements** (SGX filings).

**Tier 2 — Market data ONLY** (Perplexity Finance / FactSet / LSEG): year-end (31 Dec) closing price, shares outstanding, market cap, 3-month **compounded** SORA, Fed funds target range + effective rate. **MAS (SORA) and FRED (`DFEDTARU`, `DFF`) are preferable to any vendor for rates.**

**Tier 3 — Yahoo Finance: price cross-check ONLY.** Forbidden for any fundamental, ratio, NIM, ROE, P/B, or book value.

### Hard prohibitions
1. **Never** take a fundamental or ratio from an aggregator/screener/broker/news source when the bank publishes it (Yahoo, GuruFocus, Investing.com, StockAnalysis, Simply Wall St, IG, Morningstar, TradingView, WSJ, Bloomberg summaries).
2. **Never** compute a ratio the bank prints (use the bank's printed NIM/ROE; note its definition).
3. **Never** estimate, interpolate, infer, or fill from memory. `n/r` is a correct answer; a plausible wrong number is a failure.
4. **Never** use SEC/EDGAR — these banks file with **SGX**.
5. **Never** use ADRs — SGX tickers only.

---

## 3. Definitional traps — read before extracting

- **B1 — DBS publishes THREE NIMs.** Use **Group NIM** for every `NIMgroup` row (the `NIMcommbook` rows are reference only). *Canary:* DBS FY2025 group NIM = **2.01%**; FY2024 commercial-book NIM = 2.80%. If a `DBS_NIMgroup` cell comes back ~2.80% or ~3.23%, it's the wrong series — re-extract.
- **B2 — DBS net fee is on a commercial-book basis** (recent years); OCBC/UOB report group. Note the basis in `px_comment` for DBS `NetFee` rows.
- **B3 — "Wealth management income" is not comparable across banks and overlaps NII** (OCBC/DBS include NII on wealth deposits; UOB is narrower, restated 1 Jan 2023). Report each bank's number as printed; never treat wealth as a slice of non-II. **Distinguish `Wealth` (income line) from `WealthAUM` (assets under management)** — they are different rows.
- **B4 — UOB "core" vs "reported" differ** (one-off Citi integration + stamp duty). Separate rows exist (`NetProfitCore`, `NetProfitReported`, `ROEcore`). Fill both; never substitute one for the other.
- **B5 — UOB FY2025 profit −23% is a provisioning artefact** (~S$2.0bn pre-emptive general allowances, 3Q2025; operating profit −4%). Note it on FY2025 UOB profit/ROE rows.
- **B6 — Restatements: use the restated figure, flag it.** OCBC FY2022 comparatives restated for **SFRS(I) 17** (insurance); OCBC 2017 (SFRS(I) + Great Eastern policy); OCBC 2016–2019 reclassified; UOB wealth reclassified 1 Jan 2023. When your source is a later report showing a restated prior year, say so in `px_comment` (e.g. "FY2022 as restated in FY2023 release").
- **B7 — DBS 1-for-10 bonus issue** (bonus shares from 1Q2024). For DBS `PriceYE` and `BVPS`, state in `px_comment` whether the figure is **as-traded/as-reported** or **bonus-adjusted**, and give the **exact date** for prices. Do not mix an adjusted price with an unadjusted BVPS.
- **B8 — MAS 2020 dividend cap** (60% of 2019; lifted 2021) — note on FY2020 DPS if retrieved.
- **B9 — FY2021 is the deliberate CAGR base** (trough NIM, peak wealth fees). Just retrieve FY2016/FY2021/FY2025 accurately; the report stage handles CAGR bases.

---

## 4. Definitions to capture (put in `px_comment` where relevant)
- **CustomerDeposits** = group **non-bank customer deposits** (balance-sheet liability).
- **TotalAssets** = consolidated **total assets** (balance-sheet total). *[Definition of "net" to be confirmed by owner; default = total assets as printed.]*
- **WealthAUM** = the bank's reported wealth / private-bank AUM (off-balance-sheet client assets). Note each bank's label (DBS "Wealth Management AUM"; OCBC "group/banking wealth AUM"; UOB "wealth AUM") — definitions differ; expect patchy pre-2019.
- **Deposit mix / CASA** — fill `CurrentAccts`, `SavingsDep`, and `CASAratio` per bank per year. CASA ratio = (current + savings) ÷ total customer deposits. **Prefer the bank's directly-printed CASA ratio** where it gives one (DBS/UOB/OCBC state it in results decks); otherwise report the current-account and savings balances (S$m) from the customer-deposits note so the ratio can be computed, and flag it computed. CASA is the deposit-*quality* lens on the attracted-asset base (cheap sticky money vs bought fixed deposits); it is rate-cycle sensitive (2020–21 COVID surge, 2022–23 reversal). OCBC pre-2019 is often `n/r` from the readily-available decks — mark it so rather than reaching for an aggregator.
- **Price dates:** `PriceYE` = last trading day of December (give the exact date). `PriceCurrent` = today's close (give the date).
- **Rates:** `SORA_YE` = 31-Dec value of **3M compounded SORA**; `SORA_avg` = calendar-year average. Compounded SORA exists only from **6 Aug 2020** → pre-2020 = `n/r` (do NOT splice SIBOR). `FedUpper` = `DFEDTARU` year-end; `EFFRavg` = `DFF`/`FEDFUNDS` annual average.

---

## 5. Poison pills — known-wrong values in circulation
If any of these appears in your extraction, the source is contaminated — discard it for the whole task and re-extract from Tier 1. Flag any hit in `px_comment`.

| If you return… | …truth is | Contaminated source |
|---|---|---|
| UOB FY2025 total income **S$12.0bn** | **S$13.8bn** (9.36+2.57+1.88=13.81) | IG |
| DBS FY2025 ROE **16.5%** | **16.2%** (RoTE 17.8%) | IG |
| DBS FY2025 group NIM **~2.80%** | **2.01%** (2.80 is FY2024 commercial book) | definitional |
| DBS NIM **~3.23%** | not a DBS-published figure | GuruFocus |

---

## 6. Self-checks before you return the ledger
Run these; note failures in `px_comment` on the affected rows (do **not** hide them):
1. **NII + Non-NII = Total income**, every bank/year you filled.
2. **DBS NIM canary:** `DBS_NIMgroup_2025` = 2.01.
3. **Currency:** every value SGD; no ADR/USD ratios.
4. **Checksum agreement:** for every row with a `checksum_expected`, does your `px_value` match? If not — comment with your value, the expected value, and your source. Expect the known-hard disagreements to land on restatement/basis (OCBC FY2022 original-vs-restated; UOB FY2025 ROE 9.6 vs 10.1; UOB FY2022 P/B basis).
5. **Continuity:** any year-on-year move >30% — note the cause (restatement / acquisition / one-off / rate cycle).

**Return:** the filled CSV only. No prose report at this stage.
