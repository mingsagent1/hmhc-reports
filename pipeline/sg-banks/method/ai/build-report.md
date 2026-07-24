# Assemble — Module SOP: Report assembly (SG Banks · Tables)

> **Artifact:** `pipeline/sg-banks/method/ai/build-report.md` (`build-` = assembly, low insight) — version history in git (`git log --oneline pipeline/sg-banks/method/ai/build-report.md`).
> **Status:** Draft.
> **History:** Until 2026-07-20 this file was the monolithic "reconcile + build" SOP. In the modular-pipeline refactor its **reconciliation** guidance moved to the upstream human/Claude step (documented in `build-tables.md`) and all **table specifications, formulas, tie-outs, canaries, and number formats** moved to `pipeline/sg-banks/method/code/build-tables.md`. This file is now **Assemble-only**: it turns finished inputs into the published report. **Table arithmetic is NOT specified here — it lives only in `build-tables.md`.**

## Module contract

| | |
|---|---|
| **Inputs** | `pipeline/sg-banks/guides/frame.md` (human-owned: thesis, key questions, decision rule) · `pipeline/sg-banks/data/tables.md` (finished table blocks + footnotes + validation data) · `pipeline/sg-banks/data/benchmarks.md` (peer benchmark index tables, when populated) · `pipeline/sg-banks/data/signals.md` (dated/sourced qualitative signals) · `pipeline/sg-banks/guides/style.md` (marking/format/tone spec). |
| **Sole output** | `reports/sg-banks/report.md` — the published report: legend/header, the table blocks (lifted from `tables.md`), per-bank narrative, methodology note, FY2026 guidance, and Appendices A–C. |
| **Idempotence** | A rerun overwrites `reports/sg-banks/report.md` in place from the current inputs. Git retains history. Assemble does **not** recompute table arithmetic or re-retrieve data. |
| **Recommended model** | Any capable writing/synthesis model. No search grounding — Assemble may only use its four inputs; it must not fetch outside facts. |
| **Position** | `… → Build-Tables → Build-Report → Write-Conclusions → Publish`. Build-Report consumes `tables.md`, `signals.md`, `frame.md`, `style.md`; the Write-Conclusions and Publish modules run after. |

**Banks:** DBS (D05), OCBC (O39), UOB (U11). Period FY2016–FY2025 + latest 2026 interim. **SGD only.**

---

## Role of this SOP

Assemble is the **composition** stage. Everything numeric is already decided: `tables.md` carries the finished tables and their footnotes; `signals.md` carries the qualitative colour; `frame.md` says what the report is arguing; `style.md` says how to mark and word it. Assemble's job is to weave these into one clean, readable report — **without introducing a single number or fact that is not already in its inputs.**

## Handling an unpopulated or stale Scan

If `pipeline/sg-banks/data/signals.md` is unpopulated or stale (check its as-of date against the report period):

- **Never invent signals.** Do not add management-commentary or market-context narrative that is not present in `signals.md` or already in `tables.md`.
- **Assemble from what is available** and **mark omissions** — where a section would be enriched by scan signals, say the qualitative layer is stale/absent rather than filling the gap.

*(Scan was first run 2026-07-20; `signals.md` is currently populated.)*

## Formatting, marking, and tone

**All marking and formatting conventions come from `pipeline/sg-banks/guides/style.md`** (`n/r` vs `n/d`, number formats, superscript citations and trap-notes, derived-cell marking, table formatting, currency/scope, neutral descriptive tone, no investment advice). Assemble applies that spec. It does **not** restate per-column number formats or re-derive any cell — those belong to `build-tables.md`.

The report's top legend and formats block is copied from `style.md`'s report-level conventions; keep it to one short legend + one short formats line.

## What Assemble writes

1. **Header + legend + formats block.** Project/component line, banks/period/currency, the one-line `n/r`/`n/d` legend, and the one-line formats summary (per `style.md`).
2. **Table blocks.** Lift Tables 1 (per bank), 2, 3, 4 (+ P/TB block), and 5 — with their derived-line and superscript footnotes — verbatim from `pipeline/sg-banks/data/tables.md`; **Table 6 (peer benchmarks: monetization + valuation indices)** is lifted verbatim from `pipeline/sg-banks/data/benchmarks.md` once its peer inputs are populated (until then Key Data has no Table 6 and the Conclusions mark Q5/Q6 pending). **Do not recompute or reformat cells.** If a cell looks wrong, fix it upstream (ledger → Build-Tables · peers.csv → Build-Benchmarks), not here.
3. **Per-bank "Other (non-NII) revenue" commentary** under each Table 1 — 2–3 standard-size dot points per bank covering: (1) **composition** (what non-NII is made of, latest-FY figure, biggest slices), (2) **growth engine** (structural driver + CAGR/growth number where available), (3) **risks** (one line on cyclicality / mark-to-market / bank-specific vulnerability, only where material). Factual only — sourced from the tables/ledger figures and, once Scan runs, from dated signals. **No investment view.**
4. **"Why deposits + CASA is the attraction benchmark" methodology note** under Table 2 — ≈1 short paragraph carrying only the 2–4 most decision-relevant lines (see the rationale in prior frame revisions — git history): deposits = the only consistently-disclosed on-balance-sheet attraction measure; CASA = the quality overlay; wealth AUM = the truest but secondary flywheel; never sum deposits + AUM.
5. **FY2026 management guidance** under Table 3 — three standard-size bullets, one per bank, prefixed by bank name (verbatim management commentary; keep UOB's numeric target inline). These are disclosed-guidance narrative; once Scan runs, refresh them from dated Tier-1 signals.
6. **Appendices A–C** (see below).

## Phase — Appendices (after the tables)

1. **Validation report (Appendix A):** lift the tie-out gates, the resolved-checksum line-list, and the `n/r`/`n/d` inventory from the "Table-level validation data" section of `tables.md`; add the **narrative continuity** notes (every >30% YoY move explained by restatement / acquisition / one-off / rate cycle) and the **provenance caveat** (model-correlation status of un-checksummed cells). The prose framing of validation lives here; the raw gate results come from `tables.md`.
2. **Definitions appendix (Appendix B):** each bank's stated definition of NIM, wealth-management income, net-fee basis, ROE/RoTE, and the deposits/assets/AUM definitions used.
3. **Restatement log (Appendix C):** every restated year used, what changed, which standard, how treated (incl. DBS bonus issue and its effect on the per-share series).

Keep all three as prose / compact tables — this is where explanation lives, so it stays **out** of the data tables.

## Narrative & citation rules
- **Neutral, descriptive tone; no investment view** (per `style.md`).
- **Citations and trap-notes are bracketed `[n]` markers** pointing into italic footnote paragraphs (no raw HTML — the site renders pure markdown only); no sentence-long text inside table cells (the tables arrive pre-formatted from `tables.md` — preserve that).
- **Every narrative claim must trace to an input** — a table cell, a ledger-grounded figure already in `tables.md`, a dated signal in `signals.md`, or the framing in `frame.md`. No outside facts, no forecasts of your own, no memory-fills.
- Read **within-bank trends**, never false cross-bank comparisons on non-comparable lines (wealth income, AUM definitions) — always flag non-comparability.

## Canonical report structure

The published `reports/sg-banks/report.md` is titled **"Analysis of Singapore Banks — DBS · OCBC · UOB"** and has a **fixed five-section order**, top to bottom. Every rebuild must reproduce it exactly:

1. **Purpose** — opens the document. Contains: the **Thesis** (a succinct rendering of `guides/frame.md`'s thesis — condense wording, never change substance) · the **key questions verbatim from `guides/frame.md`** — exact question wording, grouped under the frame's A/B/C category headings, numbering preserved, **internal-note format comments omitted** — with a note that each is answered in the Conclusions · a one-line **Scope** (banks/tickers · period · currency · Appendix D pointer) · and the fixed disclaimer blockquote: *"**This is not financial advice.** It is a demonstration of the use of AI in business analysis."* There is no separate Interpretation section — Purpose replaced it (2026-07-22).
2. **How this report was made** — a **static provenance section** for non-technical readers, **kept to ~15 lines (half a page) max**: one short paragraph (documented AI-run workflow + repo link; instruction files as SOPs; data files as CSV/markdown; then exactly "The general structure of the workflow is as follows:"), the simplified workflow tree, and a one-sentence closing line on the instruction files as living documents the AI reviews and refines run over run (a continuous self-improvement cycle, version-controlled and traceable in git). Tree rules: **indented list lines with inline-code paths, not a fenced code block** (bold/links don't render in fenced blocks); link-outs are inline on the tree lines with absolute GitHub URLs (the report is served off-repo) — no separate "More:" line; no "Human + AI" phrasing — human ownership shows only via the `guides/` HUMAN-OWNED comment; `frame.md` = "the key questions we are trying to answer from the analysis"; `style.md` on its own line; the module block is headed "`method/` and outputs" and opens with two hyperlinked entries: [`AGENTS.md`] ("the ground rules every AI agent reads before working in this repo") then [`UPDATE.md`] ("intelligent instruction routing of user prompts"); `fetch-ledger.md` links its `data/ledger.csv` output; no separate `reports/` block — `build-report.md` sits **last**, pointing at a **bolded `report.md`** hyperlinked to the report's commit history, with the comment "assembling this publicized report". **Not data-dependent:** rebuilds reproduce it verbatim; its content changes only when the workflow itself changes (new module, moved artifact).
3. **Conclusions** — sits in the top-third, **wrapped in the `<!-- conclusions:start -->` / `<!-- conclusions:end -->` markers** so the Write-Conclusions module (`write-conclusions.md`) can regenerate it in place. Format: **answers to the Frame's key questions, in order, plus a 0–100 thesis score** (see `write-conclusions.md`). There is no separate Key Questions section — the Conclusions section *is* where the Frame's questions are answered.
4. **Key Data (tables)** — the five tables (Table 1 ×3, Tables 2–5), the latest-quarter interim tables, and **Table 6 — peer benchmarks** (from `data/benchmarks.md`, when populated), numbers unchanged. **No signal commentary in the body:** no "Risks:" blocks, no "FY2026 management guidance" block, no forward/interpretive "Growth engine:" passages — that content lives only in `data/signals.md` and feeds the Conclusions section only. Factual composition breakdowns and the deposits/CASA methodology are relocated to Appendix B, never dropped; any hard datum (e.g. a CAGR) must survive in a table or an appendix.
5. **Appendix** — **A — Validation report**, **B — Definitions** (also holding the relocated composition/benchmark methodology), **C — Restatement log**, and **D — Notation & Formats** (the Legend/Formats moved out of the top). Appendices are top-level `## Appendix A/B/C/D` headings — no bare `## Appendix` wrapper heading.

**Rules that keep rebuilds consistent:**
- The "How this report was made" section is **workflow-descriptive only** — it never carries report data, findings, or signal content, and is not touched by data refreshes.
- Signal commentary never appears in the report body; signals feed **only** the Conclusions section (via `data/signals.md`).
- Legend and number-format notation live in **Appendix D**, not at the top.
- The Conclusions section is always wrapped in the `conclusions` markers and is the canonical copy (there is no separate conclusions artifact file).
- Never change a table's numbers during assembly; fix upstream (ledger → Build-Tables) if a cell looks wrong.

## Acceptance criteria (stop when all true)
- `reports/sg-banks/report.md` contains the header/legend, all table blocks (lifted unchanged from `tables.md`), the per-bank commentary, the benchmark note, FY2026 guidance, and Appendices A–C.
- No table cell value differs from `tables.md`; no number or fact appears that is not traceable to an input.
- Scan-not-run state is handled honestly — no invented signals; omissions marked.
- Data tables contain only numbers / `n/r` / `n/d` + superscripts; all prose is in footnotes, the per-bank commentary blocks, the guidance bullets, or the appendices.
- Neutral tone throughout; no investment view.

**Deliver as a single markdown file.** No commentary outside the report, no investment view.
