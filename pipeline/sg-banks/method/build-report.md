# Assemble — Module SOP: Report assembly (SG Banks · Tables)

> **Project:** Singapore Bank Stock Accumulation Strategy
> **Artifact:** `pipeline/sg-banks/method/build.md` — version history in git (`git log --oneline pipeline/sg-banks/method/build.md`).
> **Status:** Draft.
> **History:** Until 2026-07-20 this file was the monolithic "reconcile + build" SOP. In the modular-pipeline refactor its **reconciliation** guidance moved to the upstream human/Claude step (documented in `build-tables.md`) and all **table specifications, formulas, tie-outs, canaries, and number formats** moved to `pipeline/sg-banks/method/build-tables.md`. This file is now **Assemble-only**: it turns finished inputs into the published report. **Table arithmetic is NOT specified here — it lives only in `build-tables.md`.**

## Module contract

| | |
|---|---|
| **Inputs** | `pipeline/sg-banks/frame.md` (thesis, questions, rubric) · `pipeline/sg-banks/data/tables.md` (finished table blocks + footnotes + validation data) · `pipeline/sg-banks/data/signals.md` (dated/sourced qualitative signals) · `pipeline/sg-banks/method/style.md` (marking/format/tone spec). |
| **Sole output** | `reports/sg-banks/report.md` — the published report: legend/header, the table blocks (lifted from `tables.md`), per-bank narrative, methodology note, FY2026 guidance, and Appendices A–C. |
| **Idempotence** | A rerun overwrites `reports/sg-banks/report.md` in place from the current inputs. Git retains history. Assemble does **not** recompute table arithmetic or re-retrieve data. |
| **Recommended model** | Any capable writing/synthesis model. No search grounding — Assemble may only use its four inputs; it must not fetch outside facts. |
| **Position** | `… → Build-Tables → Assemble → Exec Summary → Publish`. Assemble consumes `tables.md`, `signals.md`, `frame.md`, `style.md`; the Exec Summary and Publish modules run after. |

**Banks:** DBS (D05), OCBC (O39), UOB (U11). Period FY2016–FY2025 + latest 2026 interim. **SGD only.**

---

## Role of this SOP

Assemble is the **composition** stage. Everything numeric is already decided: `tables.md` carries the finished tables and their footnotes; `signals.md` carries the qualitative colour; `frame.md` says what the report is arguing; `style.md` says how to mark and word it. Assemble's job is to weave these into one clean, readable report — **without introducing a single number or fact that is not already in its inputs.**

## Handling the current state (Scan not yet run)

`pipeline/sg-banks/data/signals.md` is currently a **scaffold — Scan has not been run**, so it contains no signals. Assemble must:

- **Not invent signals.** Do not add management-commentary or market-context narrative that a signal would have supplied but which is not present in `signals.md` or already in `tables.md`.
- **Assemble from what is available.** Build the report from `tables.md` + `frame.md` + `style.md`. The per-bank "Other (non-NII) revenue" commentary and the FY2026 guidance bullets in the current report are grounded in ledger/report content (composition figures, disclosed guidance) — these are retained because they trace to the tables/ledger, not to an unrun scan.
- **Mark omissions.** Where a section would be enriched by scan signals, note that the qualitative scan layer is not yet integrated rather than filling the gap. (See `frame.md` open framing questions.)

When Scan is later run, a rerun of Assemble folds its dated, sourced signals into the narrative.

## Formatting, marking, and tone

**All marking and formatting conventions come from `pipeline/sg-banks/method/style.md`** (`n/r` vs `n/d`, number formats, superscript citations and trap-notes, derived-cell marking, table formatting, currency/scope, neutral descriptive tone, no investment advice). Assemble applies that spec. It does **not** restate per-column number formats or re-derive any cell — those belong to `build-tables.md`.

The report's top legend and formats block is copied from `style.md`'s report-level conventions; keep it to one short legend + one short formats line.

## What Assemble writes

1. **Header + legend + formats block.** Project/component line, banks/period/currency, the one-line `n/r`/`n/d` legend, and the one-line formats summary (per `style.md`).
2. **Table blocks.** Lift Tables 1 (per bank), 2, 3, 4 (+ P/TB block), and 5 — with their derived-line and superscript footnotes — verbatim from `pipeline/sg-banks/data/tables.md`. **Do not recompute or reformat cells.** If a cell looks wrong, fix it upstream (ledger → Build-Tables), not here.
3. **Per-bank "Other (non-NII) revenue" commentary** under each Table 1 — 2–3 standard-size dot points per bank covering: (1) **composition** (what non-NII is made of, latest-FY figure, biggest slices), (2) **growth engine** (structural driver + CAGR/growth number where available), (3) **risks** (one line on cyclicality / mark-to-market / bank-specific vulnerability, only where material). Factual only — sourced from the tables/ledger figures and, once Scan runs, from dated signals. **No investment view.**
4. **"Why deposits + CASA is the attraction benchmark" methodology note** under Table 2 — ≈1 short paragraph carrying only the 2–4 most decision-relevant lines (see the rationale in `frame.md` / prior revisions): deposits = the only consistently-disclosed on-balance-sheet attraction measure; CASA = the quality overlay; wealth AUM = the truest but secondary flywheel; never sum deposits + AUM.
5. **FY2026 management guidance** under Table 3 — three standard-size bullets, one per bank, prefixed by bank name (verbatim management commentary; keep UOB's numeric target inline). These are disclosed-guidance narrative; once Scan runs, refresh them from dated Tier-1 signals.
6. **Appendices A–C** (see below).

## Phase — Appendices (after the tables)

1. **Validation report (Appendix A):** lift the tie-out gates, the resolved-checksum line-list, and the `n/r`/`n/d` inventory from the "Table-level validation data" section of `tables.md`; add the **narrative continuity** notes (every >30% YoY move explained by restatement / acquisition / one-off / rate cycle) and the **provenance caveat** (model-correlation status of un-checksummed cells). The prose framing of validation lives here; the raw gate results come from `tables.md`.
2. **Definitions appendix (Appendix B):** each bank's stated definition of NIM, wealth-management income, net-fee basis, ROE/RoTE, and the deposits/assets/AUM definitions used.
3. **Restatement log (Appendix C):** every restated year used, what changed, which standard, how treated (incl. DBS bonus issue and its effect on the per-share series).

Keep all three as prose / compact tables — this is where explanation lives, so it stays **out** of the data tables.

## Narrative & citation rules
- **Neutral, descriptive tone; no investment view** (per `style.md`).
- **Citations and trap-notes are superscripts** into small-font footnote blocks; no sentence-long text inside table cells (the tables arrive pre-formatted from `tables.md` — preserve that).
- **Every narrative claim must trace to an input** — a table cell, a ledger-grounded figure already in `tables.md`, a dated signal in `signals.md`, or the framing in `frame.md`. No outside facts, no forecasts of your own, no memory-fills.
- Read **within-bank trends**, never false cross-bank comparisons on non-comparable lines (wealth income, AUM definitions) — flag non-comparability per `frame.md`'s rubric.

## Canonical report structure

The published `reports/sg-banks/report.md` has a **fixed six-section order**, top to bottom. Every rebuild must reproduce it exactly:

1. **How this report was made** — a **static provenance section** for non-technical readers, **kept to ~15 lines (half a page) max**: one short paragraph (documented AI-run workflow + repo link; instruction files as SOPs; data files as CSV/markdown; then exactly "The general structure of the workflow is as follows:"), the simplified workflow tree, and one **More:** line of GitHub link-outs (repo, `AGENTS.md`, `UPDATE.md`, `ledger.csv`, version history — absolute URLs, since the report is served off-repo). Tree rules: **indented list lines with inline-code paths, not a fenced code block** (bold/links don't render in fenced blocks); no "Human + AI" phrasing — human ownership shows only via the `guides/` HUMAN-OWNED comment; `frame.md` = "the key questions we are trying to answer from the analysis"; `style.md` on its own line; the module block is headed "`method/` and outputs"; no separate `reports/` block — `build-report.md` sits **last**, pointing at a **bolded `report.md`** with the comment "assembling this publicized report". **Not data-dependent:** rebuilds reproduce it verbatim; its content changes only when the workflow itself changes (new module, moved artifact).
2. **Interpretation (short)** — the one-line thesis (Singapore as a regional wealth hub; DBS/OCBC/UOB the vehicles), the banks/period/currency line, and a compact "How this was built" flex line. No Legend/Formats here.
3. **Key Questions & AI Recommendations** — the big questions from `pipeline/sg-banks/guides/frame.md` as dot points, each with a concise AI recommendation answered from the report's findings. **If `guides/frame.md` still holds placeholder `<your question>` lines, do not invent questions** — insert *"Key Questions pending — to be set in guides/frame.md by the author."* and leave recommendations blank.
4. **Executive Summary** — sits in the top-third, **wrapped in the `<!-- execsummary:start -->` / `<!-- execsummary:end -->` markers** so the Exec-Summary module (`write-execsummary.md`) can regenerate it in place. Exactly 10 ranked insights, ≥3 positive and ≥3 negative.
5. **Key Data (tables)** — the five tables (Table 1 ×3, Tables 2–5) plus the latest-quarter interim tables, numbers unchanged. **No signal commentary in the body:** no "Risks:" blocks, no "FY2026 management guidance" block, no forward/interpretive "Growth engine:" passages — that content lives only in `data/signals.md` and feeds the Executive Summary only. Factual composition breakdowns and the deposits/CASA methodology are relocated to Appendix B, never dropped; any hard datum (e.g. a CAGR) must survive in a table or an appendix.
6. **Appendix** — **A — Validation report**, **B — Definitions** (also holding the relocated composition/benchmark methodology), **C — Restatement log**, and **D — Notation & Formats** (the Legend/Formats moved out of the top).

**Rules that keep rebuilds consistent:**
- The "How this report was made" section is **workflow-descriptive only** — it never carries report data, findings, or signal content, and is not touched by data refreshes.
- Signal commentary never appears in the report body; signals feed **only** the Executive Summary (via `data/signals.md`).
- Legend and number-format notation live in **Appendix D**, not at the top.
- The Executive Summary is always wrapped in the `execsummary` markers and is the canonical copy (there is no separate `execsummary.md` artifact).
- Never change a table's numbers during assembly; fix upstream (ledger → Build-Tables) if a cell looks wrong.

## Acceptance criteria (stop when all true)
- `reports/sg-banks/report.md` contains the header/legend, all table blocks (lifted unchanged from `tables.md`), the per-bank commentary, the benchmark note, FY2026 guidance, and Appendices A–C.
- No table cell value differs from `tables.md`; no number or fact appears that is not traceable to an input.
- Scan-not-run state is handled honestly — no invented signals; omissions marked.
- Data tables contain only numbers / `n/r` / `n/d` + superscripts; all prose is in footnotes, the per-bank commentary blocks, the guidance bullets, or the appendices.
- Neutral tone throughout; no investment view.

**Deliver as a single markdown file.** No commentary outside the report, no investment view.
