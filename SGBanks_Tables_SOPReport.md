# SOP 2 — Report Component Build (SG Banks · Tables: revenue-engine / valuation view)

> **Project:** Singapore Bank Stock Accumulation Strategy
> **Artifact:** `SGBanks_Tables_SOPReport.md` — version history in git (`git log --oneline SGBanks_Tables_SOPReport.md`).
> **Status:** Draft.
> **Consumes:** `SGBanks_Tables_Ledger.csv` → **Produces:** `SGBanks_Tables_Report.md`.
> **Changelog:** v0.1 — New table order (Income Engines first); deposits/assets/Other/Profit engine view; removed standalone Wealth & Net-Fee tables; added Other-income breakdown block; combined P/B + ROE; NIM table gains an NII column; no inline `calc` marker; citations as superscript footnotes.
> · **rev 2026-07-16:** added **Table 1b — Attracted assets (deposits & CASA)** as the asset-attraction spine.
> · **rev 2026-07-16b:** added **Table 1c — Wealth AUM (overlay)** and a **"why deposits + CASA is the benchmark"** methodology note (report surfaces only the most relevant lines).

**Role of this SOP.** This is the *reconcile + build* stage. Input = the filled `SGBanks_Tables_Ledger.csv` (from SOP 1, with one or more agents' columns). Output = one clean markdown report component. Best run by Claude Cowork (it can reconcile in code and build the file).

**Banks:** DBS (D05), OCBC (O39), UOB (U11). Period FY2016–FY2025 + latest 2026 interim. **SGD only.** All amounts **S$bn to 2dp**, ratios to 2dp.

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

### Marking (report-level)
`n/r` = not retrieved from Tier-1; `n/d` = bank does not disclose. Derived values are unmarked (covered by the per-table derived-line). Give the tiny legend once at the top.

---

### Table 1 — Income Engines (S$bn)  ⟵ FIRST table

Per bank, five columns: **Customer Deposits · Total Assets · NII · Other · Profit**. (Wealth is intentionally excluded — overlaps NII and is inconsistently available; the wealth story sits in the breakdown block below.)

Layout: `FY | DBS Dep | DBS Assets | DBS NII | DBS Other | DBS Profit | OCBC … | UOB …`
- **Other** = Total income − NII (derived; footnote the formula).
- **Profit** = net profit attributable to shareholders (reported). For UOB, footnote the **core** figure alongside (B4).
- Final rows: **4-yr CAGR (FY2021→FY2025)** and **9-yr CAGR (FY2016→FY2025)** for Deposits, Assets, NII, Other, Profit per bank (derived; formula in footnote). Use FY2021 and FY2016 bases exactly (B9).
- Memo row: **FY2025 total income** per bank.
- Superscript footnotes for: UOB FY2025 profit provisioning artefact (B5); OCBC FY2022 restatement (B6); any `n/r` (deposits/assets if a year is missing).

### Table 1b — Attracted assets: deposits & CASA

The primary **asset-attraction** proxy for the franchise (deposits are the one attraction measure disclosed by all three banks, every year, on a consistent basis; total assets includes leverage; wealth AUM is patchy pre-2019).

Layout: `FY | DBS dep | DBS CASA | OCBC dep | OCBC CASA | UOB dep | UOB CASA`.
- **Deposits** = total customer deposits (S$B). **CASA ratio (%)** = (current + savings) ÷ total; use the bank's printed ratio where given, else compute from the deposit note (footnote which cells are computed; mark OCBC pre-2019 `n/r`).
- Final rows: **9-yr deposit CAGR (FY2016→25)**, **4-yr deposit CAGR (FY2021→25)**, **average CASA** (over available years).
- Superscript footnote: CASA is rate-cycle sensitive — the 2020–21 spike is the COVID zero-rate liquidity surge, the 2022–23 fall is the shift into fixed deposits — so read CASA **within-year across banks** and over a **full cycle**, not point-to-point.
- Optional overlay: **CASA balance** (deposits × CASA%) — the low-cost, sticky money; the sharpest single "attraction" signal because it strips out deposits bought with rate.
- Positioning: treat **deposits + CASA** as the attracted-asset spine; **total assets** belongs in the leverage column (Table 1 / monetization), and **wealth AUM** is a FY2019+ overlay, not a primary series.

### Table 1c — Wealth AUM (thesis overlay, S$B)

The off-balance-sheet client-asset flywheel — the *purest* expression of the wealth-hub thesis (AUM → fees, capital-light). Kept as an **overlay**, not a primary series, because the history is incomplete and the definition is bank-specific.

Layout: `FY | DBS AUM | OCBC AUM | UOB AUM`.
- Mark `n/d` where the bank did not disclose it (OCBC pre-2018, UOB 2018–19).
- Final rows: **AUM CAGR** (longest clean window per bank) shown **side-by-side with deposit CAGR** — AUM compounding faster than deposits signals the franchise tilting toward capital-light fee assets (e.g. DBS AUM ~12.7% vs deposits ~6.5%).
- Footnotes (required): (a) **single-source / low-confidence** until a second retriever or Tier-1 confirms; (b) **each bank's AUM definition differs** — state DBS "Wealth Management AUM", OCBC group/banking wealth AUM (incl. Bank of Singapore + Great Eastern), UOB wealth AUM — so levels are **not** strictly comparable across banks; read the *trend within a bank*, not the cross-bank level. Do not compute a ratio that treats the three AUM figures as like-for-like without this caveat.

### Why deposits + CASA is the attraction benchmark (methodology — surface only the most relevant lines in the report)

*The final report should carry a short "why this benchmark" note (≈1 paragraph, the 2–4 most decision-relevant points below), not this whole rationale.*

- **Goal.** Measure the franchise's structural ability to **attract assets** — the fundamental driver behind the Singapore wealth-hub thesis — in a way that is comparable **across banks** and **over a full cycle**.
- **Primary = customer deposits.** Chosen on three axes: (i) *availability* — the only asset-attraction measure disclosed by all three banks every year FY2016–2025; (ii) *consistency* — a standardized line, and here dual-verified (Perplexity + Tier-1 deposit notes agree); (iii) *purity* — on-balance-sheet client money the franchise pulls in, and it **excludes leverage**.
- **Total assets rejected** as the attraction base: it is inflated by wholesale-funded **leverage**, so it measures balance-sheet *size*, not assets *attracted*. It belongs only in the leverage column (Total assets ÷ deposits).
- **Deposits + AUM sum rejected**: double-count risk (some banks' AUM includes wealth deposits) — the same overlap lesson as wealth-vs-NII. Pair each pool with its own income instead (NII/deposits, fees/AUM); never sum.
- **CASA = the quality overlay.** Deposit *size* can be flattered by *buying* deposits with high fixed-deposit rates. CASA isolates the cheap, sticky, relationship-driven money — the genuine "attraction." A bank whose deposits grow while CASA falls is paying up, not attracting. Caveat: CASA is rate-cycle sensitive (COVID surge 2020–21, reversal 2022–23) — compare within-year and over a cycle, not point-to-point.
- **Wealth AUM = the truest flywheel but a secondary overlay** (Table 1c): off-balance-sheet, fee-generating, capital-light — but patchy pre-2019 and inconsistently defined, so it can't carry a clean cross-bank time series.
- **Sharpest single signal:** **CASA balance** (deposits × CASA%) growth — the low-cost, sticky money, with rate-bought deposits stripped out.

### Below Table 1 — "Other (non-NII) income" breakdown, per bank

Purpose: show what each bank's non-NII engine is made of and how scalable it looks against the Singapore wealth-hub / AUM hypothesis. **Categories are bank-specific — do not force a common schema.** For each bank give a small table of its disclosed non-NII components with, where disclosed, the latest figure, the growth, and (only where the bank prints it) the segment profit/margin; mark undisclosed sub-items `n/r`/`n/d`.
- **DBS:** net fee & commission (split wealth-management fees, cards, transaction services, loan-related, investment banking where disclosed) · net trading / markets income · other. Note wealth-fee growth vs AUM.
- **OCBC:** net fees & commissions · **insurance (Great Eastern) profit/income** · net trading · other. Note GEH contribution and wealth AUM.
- **UOB:** net fees & commissions (flag the Citigroup consumer-cards/wealth uplift, 2022–24) · net trading · other.
- One small-font line per bank on the AUM/scalability read (factual only — e.g. "wealth fees +X% vs AUM +Y%"), no investment view.

### Table 2 — Net interest margin (Group) & NII

`FY | DBS NIM | DBS NII | OCBC NIM | OCBC NII | UOB NIM | UOB NII`
- DBS = **group** NIM (B1; canary FY2025 = 2.01). NIM in %, NII in S$bn.
- Final row: **FY2026 management guidance** (verbatim NIM guidance per bank, via footnote if long).
- Superscript footnote: DBS group-vs-commercial-book distinction.

### Table 3 — Valuation & Returns (P/B + ROE combined)

Per bank: **Price · BVPS · P/B · ROE · RoTE**. Layout `FY | DBS Price | DBS BVPS | DBS P/B | DBS ROE | DBS RoTE | OCBC … | UOB …`.
- **P/B** = 31-Dec close ÷ BVPS (derived; both inputs shown so it's auditable). Never use a vendor P/B.
- ROE reported; for **UOB add a core-ROE footnote** (B4) and the FY2025 provisioning footnote (B5). **OCBC/UOB RoTE = `n/d`.**
- **B7 (DBS bonus issue):** keep DBS price and BVPS on the **same basis within each year** so P/B is bonus-invariant; footnote the treatment (do not repeat the Perplexity error of adjusted price ÷ unadjusted BVPS).
- Summary rows: **10-yr avg P/B**, **5-yr avg P/B (FY2021–25)**, **current P/B** (latest close ÷ FY2025 BVPS — use the *dated* current price from the ledger), **premium/discount of current vs 10-yr avg**, and **10-yr avg ROE** per bank.
- Then a compact **P/TB block (FY2025)**: BVPS, goodwill+intangibles used, shares, TBVPS (= BVPS − (gw+intang)/shares), P/TB at FY2025 close and at current close. State the goodwill/intangibles figure. Historical P/TB = `n/r` unless per-year goodwill was retrieved.

### Table 4 — NIM vs the rate cycle

`FY | DBS NIM | OCBC NIM | UOB NIM | 3M comp. SORA (31-Dec) | 3M comp. SORA (FY avg) | Fed funds target upper (31-Dec) | Effective fed funds (FY avg)`
- NIM from Table 2. Rates from the ledger (MAS/FRED). Compounded SORA pre-Aug-2020 = `n/r` (footnote: no splice). Final row = **latest 2026** (Q1 NIM + latest rates, dated).

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
- Data tables contain only numbers / `n/r` / `n/d` + superscripts; all prose is in footnotes or appendices.
- `n/r` count is honest (a suspiciously complete table is the failure mode).

**Deliver as a single markdown file.** No commentary, no investment view.
