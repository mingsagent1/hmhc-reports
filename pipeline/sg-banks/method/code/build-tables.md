# Build-Tables — Module SOP: deterministic table generation (SG Banks)

> **Artifact:** `pipeline/sg-banks/method/code/build-tables.md` — version history in git (`git log --oneline pipeline/sg-banks/method/code/build-tables.md`).
> **Status:** Draft.
> **History:** Split out of `pipeline/sg-banks/method/build.md` on 2026-07-20 (modular-pipeline refactor). All table specs, formulas, tie-outs, canaries, and validation gates below were moved here verbatim from `build.md` rev 2026-07-16c; `build.md` is now the Assemble-only SOP. **Formulas live here only — do not duplicate them in `build.md`.**

## Module contract

| | |
|---|---|
| **Inputs** | Reconciled `pipeline/sg-banks/data/ledger.csv` (the Reconcile module — `method/ai/reconcile-ledger.md` — must be complete: every consumed row carries a `reconciled_value` / `reconciliation_status`) **and** `pipeline/sg-banks/guides/style.md` (the marking/number-format spec). |
| **Sole output** | `pipeline/sg-banks/data/tables.md` — the generated table blocks (Tables 1–5, the P/TB block, per-table derived-line and superscript footnotes, and the table-level validation gates). It writes **no** narrative body and **no** report. |
| **Idempotence** | A rerun regenerates `data/tables.md` in place from the current reconciled ledger. Git retains history. Rerunning must not change report or ledger values — it is a **deterministic transform** of the ledger, not a re-retrieval. |
| **Executor** | **No model — a deterministic script:** `pipeline/sg-banks/method/code/build_tables.py`. Run `python3 pipeline/sg-banks/method/code/build_tables.py` to regenerate `data/tables.md`; `--check` verifies the committed tables still match the ledger without writing (CI runs this on every PR). Same ledger in → same tables out; no search, no memory-fills, no LLM arithmetic. This SOP is the script's specification — keep the two in sync. |
| **Position** | `… → [human/Claude Reconcile] → Build-Tables → Assemble → …`. Build-Tables consumes the reconciled ledger; Assemble consumes this module's `tables.md` output. |

**Why this module exists (resolving the proposal gap).** The proposal's module list named a Tables step but did not give the table blocks their own explicit artifact. This SOP resolves that: the deterministic table blocks are materialised as the single artifact `pipeline/sg-banks/data/tables.md`, so Assemble consumes a finished table block rather than recomputing arithmetic.

---

## Reconciliation is an input, not a step here

Reconciling the ledger is the **Reconcile module** (`method/ai/reconcile-ledger.md`), which runs between Retrieve/Scan and this module and fills the `reconciled_*` columns in place. Build-Tables assumes it is complete and does not re-open source retrieval; every consumed row must carry a `reconciliation_status`, and each `resolved` row becomes a line in the Validation Report (below).

---

## Formatting and marking

**Marking conventions (`n/r` vs `n/d`, derived-cell marking, superscript citations, currency/scope) are specified in `pipeline/sg-banks/guides/style.md`.** This SOP applies that spec; it does not restate it. The number-format table below is reproduced here because it is table-specific and load-bearing for the arithmetic.

### Global formatting rules (apply to every table)
1. **No inline `calc` marker.** Derived cells appear as plain numbers. Under each table add ONE small-font line naming the derived columns and the formula, e.g. `Other = Total income − NII; CAGR = (end/start)^(1/n) − 1`.
2. **Citations & trap-notes = superscript numbers only.** Put the note text in a small-font footnote block under the table using `<sub>…</sub>`. **No sentence-long text inside any table cell.**
3. **Cell contents are only:** a number, `n/r`, or `n/d`. Nothing else.
4. **No instructional text in the output** — no "amounts only", no "retrieval notes", no restating the SOP. The table block carries data + footnotes only.
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

---

## Table specifications

### Table 1 — Income Engine, per bank (THREE tables: one each for DBS, OCBC, UOB)  ⟵ FIRST tables

**Why split.** The prior single-table layout ran to 16 columns wide and was hard to scan. Splitting per bank lets each bank's engine and ratios be read at a glance and lets a small "Other revenue" commentary block sit right beneath its own numbers.

For **each of DBS, OCBC, UOB**, build a standalone table with the same schema:

`FY | Dep | Assets | NII | Other | TotalRev | Profit | NIM | Rev/Dep | Profit/Dep | Profit/Rev`

- **Other** = TotalIncome − NII (derived; footnote the formula).
- **TotalRev** = TotalIncome (reported).
- **Profit** = net profit attributable to shareholders (reported). For UOB, footnote the **core** figure alongside (B4).
- **Rev/Dep, Profit/Dep, Profit/Rev** are derived (compute from S$m-denominated reconciled values so ratios are dimensionless; per-column formats above).
- **NIM** = group NIM (canary DBS FY2025 = 2.01 per B1). Include `%` symbol per format.
- Final rows per table: **4-yr CAGR (FY2021→FY2025)** and **9-yr CAGR (FY2016→FY2025)** on Dep, Assets, NII, Other, TotalRev, Profit (derived; formula in footnote). **Ratio and NIM cells left blank on CAGR rows** — a point-in-time ratio does not compound.
- Superscript footnotes: `<sup>5</sup>` UOB FY2025 provisioning artefact; `<sup>6</sup>` OCBC FY2022 restatement (SFRS(I) 17).

The 2–3 dot-point "Other (non-NII) revenue" commentary block that sits under each bank's Table 1 is **narrative, not arithmetic** — it is written by the **Assemble** step (`build.md`), not here. Build-Tables emits the numeric table plus its derived-line and superscript footnotes only.

### Table 2 — Attracted assets: deposits, CASA & wealth AUM (single combined table)

The primary **asset-attraction** view (deposits) with the **CASA quality overlay** and the **wealth-AUM flywheel** — merged into one table.

Layout: `FY | DBS Dep | DBS CASA | DBS AUM | OCBC Dep | OCBC CASA | OCBC AUM | UOB Dep | UOB CASA | UOB AUM`.

- **Dep** = total customer deposits (S$bn, no decimals).
- **CASA** = bank-printed CASA ratio (%, 1 decimal, `%` symbol). Where the bank did not print it and it could not be computed from the deposit note, use `n/r`.
- **Wealth AUM** = the bank's disclosed wealth / private-bank AUM (S$bn, no decimals). Mark `n/d` where the bank did not disclose (OCBC pre-2018, UOB 2018–19).
- Final rows: **CAGR 21→25** and **CAGR 16→25** on Dep and AUM only. **CASA cells blank** on CAGR rows (CASA is a point-in-time ratio, not compounded).
- Footnotes: (a) OCBC 2016–2018 CASA is single-source (Tier-1 OCBC results decks, filled 2026-07-16 via non-Claude retriever) — `single-px` pending second pass. (b) UOB CASA lift 2023→25 reflects post-rate-cycle deposit remix + Citi consumer-book mix contribution. (c) Each bank's AUM definition differs (DBS "Wealth Management AUM"; OCBC group/banking wealth incl. Bank of Singapore + Great Eastern; UOB narrower, reclassified 1 Jan 2023) — read within-bank trend, **not** cross-bank level. (d) Deposits + AUM must never be summed (double-count risk).

### Table 3 — Net interest margin (Group) & NII

Column order: **NII first, then NIM**, per bank.

`FY | DBS NII | DBS NIM | OCBC NII | OCBC NIM | UOB NII | UOB NIM`

- DBS = **group** NIM (B1; canary FY2025 = 2.01%). NII in S$bn (2 decimals here for the NIM table — one more decimal than the S$bn columns in Table 1, because this table is where NII precision matters). NIM as % with **`%` symbol** and 2 decimals (e.g. `2.01%`).
- **No FY2026 guidance row inside the table.** The FY2026 guidance bullets below the table are **management-commentary narrative** and are written by the **Assemble** step, not here.
- Superscript footnote: DBS group-vs-commercial-book distinction (B1).

### Table 4 — Valuation & Returns (P/B + ROE combined)

Per bank: **Price · BVPS · P/B · ROE · RoTE**. Layout `FY | DBS Price | DBS BVPS | DBS P/B | DBS ROE | DBS RoTE | OCBC … | UOB …`.
- **P/B** = 31-Dec close ÷ BVPS (derived; both inputs shown so it's auditable). Never use a vendor P/B.
- ROE reported; for **UOB add a core-ROE footnote** (B4) and the FY2025 provisioning footnote (B5). **OCBC/UOB RoTE = `n/d`.**
- **B7 (DBS bonus issue):** keep DBS price and BVPS on the **same basis within each year** so P/B is bonus-invariant; footnote the treatment.
- Summary rows: **10-yr avg P/B**, **5-yr avg P/B (FY2021–25)**, **current P/B** (latest close ÷ FY2025 BVPS — use the *dated* current price from the ledger), **premium/discount of current vs 10-yr avg**, and **10-yr avg ROE** per bank.
- Then a compact **P/TB block (FY2025)**: BVPS, goodwill+intangibles used, shares, TBVPS (= BVPS − (gw+intang)/shares), P/TB at FY2025 close and at current close. State the goodwill/intangibles figure. Historical P/TB = `n/r` unless per-year goodwill was retrieved.

### Table 5 — NIM vs the rate cycle

`FY | DBS NIM | OCBC NIM | UOB NIM | 3M comp. SORA (31-Dec) | 3M comp. SORA (FY avg) | Fed funds target upper (31-Dec) | Effective fed funds (FY avg)`
- NIM from Table 3. Rates from the ledger (MAS/FRED). Compounded SORA pre-Aug-2020 = `n/r` (footnote: no splice). Final row = **latest 2026** (Q1 NIM + latest rates, dated).
- NIM values with `%` symbol per Table 3 format; rates displayed with 2 decimals for consistency.

---

## Table-level validation gates (run before writing `tables.md`)

These are the deterministic gates on the numbers themselves. (The narrative continuity checks and the prose Validation Report live in the Assemble SOP / the report's Appendix A.)

1. **NII + Non-NII = Total income** — must hold for every bank-year filled (exact to S$1m rounding; every residual 0).
2. **DBS NIM canary** — `DBS_NIMgroup_2025` = **2.01%** (group series, not the 2.80% commercial book). If a DBS NIM cell comes back ~2.80% or ~3.23%, the wrong series was consumed — stop and re-check the ledger.
3. **Currency** — every value SGD; no ADR/USD ratios.
4. **Poison-pill scan** — none of the known-wrong values present unflagged: UOB FY2025 total income ≠ 12.0 (truth 13.81) · DBS FY2025 ROE ≠ 16.5 (truth 16.2) · DBS FY2025 group NIM ≠ 2.80/3.23 (truth 2.01).
5. **Checksum reproduction** — every `checksum_expected` is reproduced, or its mismatch is traced to a definitional cause and carried into the Validation Report line-list (OCBC SFRS(I) 17 restatements, UOB Citi uplift, UOB FY2025 provisioning, price-date, rounding).
6. **`n/r` honesty** — the `n/r`/`n/d` count is accurate per table; a suspiciously complete table is the failure mode.

Emit the resolved-row line-list and the `n/r`/`n/d` inventory into `tables.md` so Assemble can lift them straight into Appendix A.

## Acceptance criteria (stop when all true)
- `data/tables.md` contains Tables 1–5, the P/TB block, and each table's derived-line + superscript footnotes — numbers / `n/r` / `n/d` only in cells.
- Every table-level validation gate above passes (or each failure is reported, not hidden).
- The output is a pure deterministic transform of the reconciled ledger — no report/ledger values changed, no narrative, no investment view.
