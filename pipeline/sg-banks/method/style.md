# Style — Marking & presentation spec (SG Banks)

> **Project:** Singapore Bank Stock Accumulation Strategy
> **Artifact:** `pipeline/sg-banks/method/style.md` — version history in git (`git log --oneline pipeline/sg-banks/method/style.md`).
> **Status:** Draft.

## Module contract — a *consumed spec*, not an executable module (controlled exception)

Every other module in this pipeline produces exactly one output artifact. **Style is the deliberate exception.** It is a **static specification**, not a step that runs and emits a file. It has **no output artifact of its own**; instead it is *consumed by* the Build-Tables and Assemble modules, which apply its conventions when they generate their outputs.

| | |
|---|---|
| **Inputs** | None to run — this is a written specification maintained by hand as conventions evolve. |
| **Output** | **None** (controlled exception to the one-output rule — documented here explicitly). Style is not executed and produces no artifact. |
| **Consumed by** | `pipeline/sg-banks/method/build-tables.md` (Tables) and `pipeline/sg-banks/method/build.md` (Assemble). |
| **Idempotence** | N/A — a spec, not a transform. Edits are ordinary commits; git retains history. |
| **Position** | Sits to the side of the main flow: `Frame → (Retrieve ‖ Scan) → Tables → Assemble → …`, with Style feeding Tables and Assemble. |

Why the exception is safe: Style carries no data and derives nothing, so it cannot drift from the ledger or the report. It is version-controlled prose that Tables and Assemble read, exactly like a house style guide. This is called out so the one-output invariant is not silently broken.

---

## 1. Marking: `n/r` vs `n/d`

- **`n/r`** = **not retrieved** from a Tier-1 source (the datum may exist but was not captured/verified). A correct answer where verification is incomplete.
- **`n/d`** = **not disclosed** — the bank does not publish the figure at all (e.g. OCBC wealth AUM pre-2018, UOB AUM 2018–19, OCBC/UOB RoTE).
- These are the **only** non-numeric tokens allowed in a data cell. Never guess, interpolate, or fill from memory to avoid an `n/r`. A suspiciously complete table is the failure mode.
- Give the `n/r`/`n/d` legend **once** at the top of the report; do not repeat it per table.

## 2. Number formats

| Quantity | Format |
|---|---|
| Deposits, Total assets, Wealth AUM | S$bn, **0 dp** (e.g. `610`) |
| NII, Other, TotalRev, Profit (Table 1) | S$bn, **1 dp** (e.g. `14.5`) |
| NII in the NIM table (Table 3) | S$bn, **2 dp** (e.g. `14.50`) — one extra dp because this is where NII precision matters |
| NIM | **%, 2 dp, with `%` symbol** (e.g. `2.01%`) |
| CASA | **%, 1 dp, with `%` symbol** (e.g. `58.4%`) |
| Rev/Dep, Profit/Dep | **3 dp**, dimensionless |
| Profit/Rev | **2 dp**, dimensionless |
| P/B, P/TB, TBVPS, Price, BVPS | 2 dp |
| ROE / RoTE | 1 dp (as reported) |
| Rates (SORA, Fed) | 2 dp |
| CAGR / growth | %, 1 dp |

- Ratio, NIM, and CASA cells are **intentionally blank on CAGR rows** — a point-in-time ratio does not compound.
- Right-align numeric columns; keep tables as narrow as the data allows.
- **Currency: SGD only, always.** Never convert, never USD, never ADR-derived figures. State the currency once in the header.

## 3. Superscript citations & trap-notes

- **Citations and trap-notes are superscript numbers/letters only** inside tables (`<sup>5</sup>`, `<sup>c1</sup>`, `<sup>u1</sup>`). The note text goes in a small-font footnote block **under** the table using `<sub>…</sub>`.
- **No sentence-long text inside any table cell.** Cells hold a number, `n/r`, or `n/d` — nothing else.
- Standing superscript keys: `<sup>5</sup>` = UOB FY2025 provisioning artefact; `<sup>6</sup>` = OCBC FY2022 SFRS(I) 17 restatement; `<sup>c1</sup>` = OCBC 2016–2018 CASA single-source note; `<sup>u1</sup>` = UOB CASA 2023–25 remix note.

## 4. Derived-cell marking

- **No inline `calc` marker.** Derived cells (Other, TotalRev, CAGR, Rev/Dep, Profit/Dep, Profit/Rev, P/B, P/TB, TBVPS) appear as plain numbers, **unmarked**.
- Under each table, add **one** small-font derived-line naming the derived columns and their formulas, e.g. `Other = TotalRev − NII; CAGR = (end/start)^(1/n) − 1`.
- Both inputs to any derived ratio are shown in the table so the derivation is auditable (e.g. Price and BVPS both shown for P/B). Never use a vendor-computed ratio.

## 5. Table formatting

- Markdown pipe tables; header row + right-aligned numeric columns.
- Each table is followed by: (a) the one-line `<sub>` derived-line + footnote block, then (b) any standard-size narrative that belongs to it (per-bank commentary, guidance bullets) — narrative is Assemble's, not part of the table.
- No instructional text in the published output — no "amounts only", no "retrieval notes", no restating the SOP.

## 6. Tone & scope

- **Neutral, descriptive tone.** Report data and factual footnotes only.
- **No investment advice** — no buy/sell/hold view, no price targets, no forecasts of the author's own. Management guidance is reported as attributed commentary, not as the report's prediction.
- Read **within-bank trends over a cycle**; do not make false cross-bank comparisons on definitionally non-comparable lines (wealth income, AUM definitions) — flag non-comparability where relevant.

## Changelog
- **2026-07-20** — Created in the modular-pipeline refactor by formalizing the marking/format/tone conventions previously embedded in `build.md` (rev 2026-07-16c) and the report legend. No convention changed; this is an extraction into a single consumed spec.
