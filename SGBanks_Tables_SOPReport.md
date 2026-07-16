# SOP 2 — Report Component Build (SG Banks · Tables: revenue-engine / valuation view)

> **Project:** Singapore Bank Stock Accumulation Strategy
> **Artifact:** `SGBanks_Tables_SOPReport.md` — version history in git (`git log --oneline SGBanks_Tables_SOPReport.md`).
> **Status:** Draft.
> **Consumes:** `SGBanks_Tables_Ledger.csv` → **Produces:** `SGBanks_Tables_Report.md`.
> **Changelog:** v0.1 — New table order (Income Engines first); deposits/assets/Other/Profit engine view; removed standalone Wealth & Net-Fee tables; added Other-income breakdown block; combined P/B + ROE; NIM table gains an NII column; no inline `calc` marker; citations as superscript footnotes.
> · **rev 2026-07-16:** added **Table 1b — Attracted assets (deposits & CASA)** as the asset-attraction spine.
> · **rev 2026-07-16b:** added **Table 1c — Wealth AUM (overlay)** and a **"why deposits + CASA is the benchmark"** methodology note.
> · **rev 2026-07-16c:** **Table 1 split per bank** (three tables — one each for DBS/OCBC/UOB) with new columns (TotalRev, NIM, Rev/Dep, Profit/Dep, Profit/Rev), per-column formatting, and 2–3 dot-point "Other revenue" commentary under each bank's table (replaces the standalone Other-income breakdown block). **Table 1b + 1c merged into a single Table 2** carrying Deposits + CASA + Wealth AUM. **Downstream tables renumbered** (old Table 2 NIM/NII → **Table 3**; old Table 3 valuation → **Table 4**; old Table 4 NIM-vs-rates → **Table 5**). Table 3 (NIM/NII) column order changed to **NII first, then NIM**; NIM values carry a **`%`** suffix; FY2026 guidance moves out of the table into three standard-size bullet footnotes (one per bank).

**Role of this SOP.** This is the *reconcile + build* stage. Input = the filled `SGBanks_Tables_Ledger.csv` (from SOP 1, with one or more agents' columns). Output = one clean markdown report component.

**Banks:** DBS (D05), OCBC (O39), UOB (U11). Period FY2016–FY2025 + latest 2026 interim. **SGD only.** Amounts and ratios per per-column formatting rules below.

---

## Phase 1 — Reconcile the ledger (do this first, in code)

For every row, compare `px_value`, `cl_value`, and `checksum_expected`, then fill `reconciled_value` / `reconciliation_status` / `reconciliation_note`:

- **`match`** — agents agree (and agree with checksum if present) → take the value. Use `match` **only** when `px_value`, `cl_value`, and any `checksum_expected` are all equal (pure rounding aside); if the value you take differs from the checksum, or `px≠cl`, it is a `resolved`, not a `match`.
- **`single-px` / `single-cl`** — only one agent filled it → take it; the status names which (`single-px` = Perplexity-only, `single-cl` = Claude-only).
- **`resolved`** — agents disagree, or the taken value disagrees with the checksum. **Do not average or silently pick.** Take the value that (a) reproduces the checksum and (b) ties out (NII+Non-NII=Total income), and record the loser + the likely cause (rounding / basis / restatement / price-date) in `reconciliation_note`. If neither ties, mark the cell `n/r` for the report and log it.
- **`n/r` / `n/d` / `text/other`** — carry through (`text/other` = guidance/verbatim text rows).

Prefer **restated** figures (B6) and record the original in the note. Every `resolved` row becomes a line in the Validation Report.

---

## Phase 2 — Build the report

### Global formatting rules (apply to every table)
1. **No inline `calc` marker.** Derived cells appear as plain numbers. Under each table add ONE small-font line naming the derived columns and the formula, e.g. `Other = Total income − NII; CAGR = (end/start)^(1/n) − 1`.
2. **Citations & trap-notes = superscript numbers only.** Put the note text in a small-font footnote block under the table using `<sub>…</sub>`. **No sentence-long text inside any table cell.**
3. **Cell contents are only:** a number, `n/r`, or `n/d`. Nothing else.
4. **No instructional text in the output** — no "amounts only", no "retrieval notes", no restating the SOP. The reader sees data + footnotes + the validation/appendix sections only.
5. Right-align numeric columns. Keep tables as narrow as the data allows.

### Per-column number formats (Tables 1, 2, 3)

| Column | Format | Notes |
|---|---|---|
| Dep | S$bn, no decimals | e.g. `610` |
| Assets | S$bn, no decimals | e.g. `897` |
| NII | S$bn, 1 decimal | e.g. `14.5` |
| Other | S$bn, 1 decimal | derived: `TotalIncome − NII` |
| TotalRev | S$bn, 1 decimal | = `TotalIncome` (reported) |
| Profit | S$bn, 1 decimal | net profit attributable |
| NIM | %, 2 decimals, with `%` symbol | e.g. `2.01%` |
| Rev/Dep | 3 decimals | derived: TotalRev ÷ Dep (unitless) |
| Profit/Dep | 3 decimals | derived: Profit ÷ Dep (unitless) |
| Profit/Rev | 2 decimals | derived: Profit ÷ TotalRev (unitless) |
| CASA | %, 1 decimal, with `%` symbol | bank-printed where given |
| Wealth AUM | S$bn, no decimals | overlay only; definitions differ |
| CAGR rows | %, 1 decimal | non-meaningful cells (ratios, NIM, CASA) left **blank** |

### Marking (report-level)
`n/r` = not retrieved from Tier-1; `n/d` = bank does not disclose. Derived values are unmarked (covered by the per-table derived-line). Give the tiny legend once at the top.

---

### Table 1 — Income Engine, per bank (THREE tables: one each for DBS, OCBC, UOB)  ⟵ FIRST tables

**Why split.** The prior single-table layout ran to 16 columns wide and was hard to scan. Splitting per bank lets each bank's engine and ratios be read at a glance and lets us add a small "Other revenue" commentary block right beneath its own numbers.

For **each of DBS, OCBC, UOB**, build a standalone table with the same schema:

`FY | Dep | Assets | NII | Other | TotalRev | Profit | NIM | Rev/Dep | Profit/Dep | Profit/Rev`

- **Other** = TotalIncome − NII (derived; footnote the formula).
- **TotalRev** = TotalIncome (reported).
- **Profit** = net profit attributable to shareholders (reported). For UOB, footnote the **core** figure alongside (B4).
- **Rev/Dep, Profit/Dep, Profit/Rev** are derived (compute from S$m-denominated reconciled values so ratios are dimensionless; per-column formats above).
- **NIM** = group NIM (canary DBS FY2025 = 2.01 per B1). Include `%` symbol per format.
- Final rows per table: **4-yr CAGR (FY2021→FY2025)** and **9-yr CAGR (FY2016→FY2025)** on Dep, Assets, NII, Other, TotalRev, Profit (derived; formula in footnote). **Ratio and NIM cells left blank on CAGR rows** — a point-in-time ratio does not compound.
- Superscript footnotes: `<sup>5</sup>` UOB FY2025 provisioning artefact; `<sup>6</sup>` OCBC FY2022 restatement (SFRS(I) 17).

**Under each bank's Table 1, add a "Other (non-NII) revenue" commentary block** — 2–3 dot points in **standard-size text** (not `<sub>`) covering:
1. **Composition** — what the bank's non-NII is actually made of, latest FY figure, and the biggest slice(s).
2. **Growth engine** — the structural driver (e.g. wealth AUM CAGR, insurance profit, Citi consumer uplift) with the CAGR / growth number if we have it.
3. **Risks** — one line on cyclicality, mark-to-market sensitivity, or a bank-specific vulnerability (only where material).

Bullets are factual only — no investment view. This block replaces the prior standalone "Below Table 1 — Other (non-NII) income breakdown" section.

### Table 2 — Attracted assets: deposits, CASA & wealth AUM (single combined table)

The primary **asset-attraction** view (deposits) with the **CASA quality overlay** and the **wealth-AUM flywheel** — merged into one table.

Layout: `FY | DBS Dep | DBS CASA | DBS AUM | OCBC Dep | OCBC CASA | OCBC AUM | UOB Dep | UOB CASA | UOB AUM`.

- **Dep** = total customer deposits (S$bn, no decimals).
- **CASA** = bank-printed CASA ratio (%, 1 decimal, `%` symbol). Where the bank did not print it and it could not be computed from the deposit note, use `n/r`.
- **Wealth AUM** = the bank's disclosed wealth / private-bank AUM (S$bn, no decimals). Mark `n/d` where the bank did not disclose (OCBC pre-2018, UOB 2018–19).
- Final rows: **CAGR 21→25** and **CAGR 16→25** on Dep and AUM only. **CASA cells blank** on CAGR rows (CASA is a point-in-time ratio, not compounded).
- Footnotes: (a) OCBC 2016–2018 CASA is single-source (Tier-1 OCBC results decks, filled 2026-07-16 via non-Claude retriever) — `single-px` pending second pass. (b) UOB CASA lift 2023→25 reflects post-rate-cycle deposit remix + Citi consumer-book mix contribution. (c) Each bank's AUM definition differs (DBS "Wealth Management AUM"; OCBC group/banking wealth incl. Bank of Singapore + Great Eastern; UOB narrower, reclassified 1 Jan 2023) — read within-bank trend, **not** cross-bank level. (d) Deposits + AUM must never be summed (double-count risk).

### Why deposits + CASA is the attraction benchmark (methodology note — surface only the most relevant lines)

*The final report should carry a short "why this benchmark" note (≈1 paragraph, the 2–4 most decision-relevant points below), not this whole rationale.*

- **Goal.** Measure the franchise's structural ability to **attract assets** — the fundamental driver behind the Singapore wealth-hub thesis — in a way that is comparable **across banks** and **over a full cycle**.
- **Primary = customer deposits.** The only asset-attraction measure disclosed by all three banks every year FY2016–2025, on a standardized line, dual-verified (Perplexity + Tier-1 deposit notes), and on-balance-sheet — excludes leverage.
- **Total assets rejected** as the attraction base: it is inflated by wholesale-funded **leverage**, so it measures balance-sheet *size*, not assets *attracted*. It belongs only in the leverage column (Total assets ÷ deposits) which Table 1 carries via Rev/Dep and Profit/Dep.
- **Deposits + AUM sum rejected**: double-count risk (some banks' AUM includes wealth deposits). Pair each pool with its own income instead (NII/deposits, fees/AUM); never sum.
- **CASA = the quality overlay.** Deposit *size* can be flattered by *buying* deposits with high fixed-deposit rates. CASA isolates the cheap, sticky, relationship-driven money — the genuine "attraction". CASA is rate-cycle sensitive (COVID surge 2020–21, reversal 2022–23) — compare within-year and over a cycle, not point-to-point.
- **Wealth AUM = the truest flywheel but a secondary overlay**: off-balance-sheet, fee-generating, capital-light — but patchy pre-2019 and inconsistently defined.
- **Sharpest single signal:** **CASA balance** (deposits × CASA%) growth — the low-cost, sticky money, with rate-bought deposits stripped out.

### Table 3 — Net interest margin (Group) & NII

Column order: **NII first, then NIM**, per bank.

`FY | DBS NII | DBS NIM | OCBC NII | OCBC NIM | UOB NII | UOB NIM`

- DBS = **group** NIM (B1; canary FY2025 = 2.01%). NII in S$bn (2 decimals here for the NIM table — one more decimal than the S$bn columns in Table 1, because this table is where NII precision matters). NIM as % with **`%` symbol** and 2 decimals (e.g. `2.01%`).
- **No FY2026 guidance row inside the table.** Instead, place the guidance as **three standard-size bullet footnotes below the table, one per bank on its own line**, prefixed by the bank name (verbatim management commentary; keep numeric target for UOB inline).
- Superscript footnote: DBS group-vs-commercial-book distinction (B1).

### Table 4 — Valuation & Returns (P/B + ROE combined)  ⟵ was Table 3

Per bank: **Price · BVPS · P/B · ROE · RoTE**. Layout `FY | DBS Price | DBS BVPS | DBS P/B | DBS ROE | DBS RoTE | OCBC … | UOB …`.
- **P/B** = 31-Dec close ÷ BVPS (derived; both inputs shown so it's auditable). Never use a vendor P/B.
- ROE reported; for **UOB add a core-ROE footnote** (B4) and the FY2025 provisioning footnote (B5). **OCBC/UOB RoTE = `n/d`.**
- **B7 (DBS bonus issue):** keep DBS price and BVPS on the **same basis within each year** so P/B is bonus-invariant; footnote the treatment.
- Summary rows: **10-yr avg P/B**, **5-yr avg P/B (FY2021–25)**, **current P/B** (latest close ÷ FY2025 BVPS — use the *dated* current price from the ledger), **premium/discount of current vs 10-yr avg**, and **10-yr avg ROE** per bank.
- Then a compact **P/TB block (FY2025)**: BVPS, goodwill+intangibles used, shares, TBVPS (= BVPS − (gw+intang)/shares), P/TB at FY2025 close and at current close. State the goodwill/intangibles figure. Historical P/TB = `n/r` unless per-year goodwill was retrieved.

### Table 5 — NIM vs the rate cycle  ⟵ was Table 4

`FY | DBS NIM | OCBC NIM | UOB NIM | 3M comp. SORA (31-Dec) | 3M comp. SORA (FY avg) | Fed funds target upper (31-Dec) | Effective fed funds (FY avg)`
- NIM from Table 3. Rates from the ledger (MAS/FRED). Compounded SORA pre-Aug-2020 = `n/r` (footnote: no splice). Final row = **latest 2026** (Q1 NIM + latest rates, dated).
- NIM values with `%` symbol per Table 3 format; rates displayed with 2 decimals for consistency.

---

## Phase 3 — Appendices (after the tables)

1. **Validation report:** tie-out gates (NII+Non-NII=Total income; DBS NIM canary; currency; continuity >30% moves explained; poison-pill hits); every checksum mismatch resolved in Phase 1 (your value, checksum value, both sources, cause); `n/r` count per table with the reason each could not be retrieved.
2. **Definitions appendix:** each bank's stated definition of NIM, wealth-management income, net-fee basis, ROE/RoTE, and the deposits/assets/AUM definitions used.
3. **Restatement log:** every restated year used, what changed, which standard, how treated (incl. DBS bonus issue and its effect on the per-share series).

Keep all three as prose/compact tables — this is where explanation lives, so it stays **out** of the data tables.

---

## Acceptance criteria (stop when all true)
- Every tie-out gate passes (or each failure is reported, not hidden).
- Every `checksum_expected` is reproduced **or** its mismatch is explained and traced to a definitional cause.
- No poison-pill value present unflagged.
- Data tables contain only numbers / `n/r` / `n/d` + superscripts; all prose is in footnotes or appendices (except the per-bank "Other revenue" commentary blocks under Table 1, which are standard-size dot points per the v0.1c revision).
- `n/r` count is honest (a suspiciously complete table is the failure mode).

**Deliver as a single markdown file.** No commentary, no investment view.
