# Exec Summary — Module SOP: closed-book Top-10 insights (SG Banks)

> **Project:** Singapore Bank Stock Accumulation Strategy
> **Artifact:** `pipeline/sg-banks/method/execsummary.md` — version history in git (`git log --oneline pipeline/sg-banks/method/execsummary.md`).
> **Status:** Draft — encodes the contract already used to produce the current `reports/sg-banks/execsummary.md`.

## Module contract

| | |
|---|---|
| **Inputs** | **Only** the finished report: `reports/sg-banks/report.md` (body + footnotes + appendices). Nothing else — no ledger, no tables.md, no signals, no web. This is a **closed-book** read of the published report. |
| **Sole output** | `reports/sg-banks/execsummary.md` — exactly 10 ranked insights with a tally line and scope line. |
| **Idempotence** | A rerun overwrites `reports/sg-banks/execsummary.md` in place from the current report. Git retains history. |
| **Recommended model** | **GPT-5.6 primary; Claude 4.8 alternative.** **Never** an Orchestrator/search-enabled configuration — this step must be closed-book (no browsing, no retrieval); search access would violate the contract. |
| **Position** | `… → Assemble → Exec Summary → Publish`. Runs after the report is finished; its output is linked from `meta.json` (`executive_summary`) by the Publish step. |

## The closed-book contract (exact — this is what produced the current exec summary)

1. **Source scope: the finished report only.** Derive every insight solely from `reports/sg-banks/report.md` — its body, footnotes, and appendices. Do **not** consult the ledger, `tables.md`, `signals.md`, external sources, or memory. If it is not in the report, it cannot be in the summary.
2. **Exactly 10 insights, ranked.** A numbered list, 1–10, ordered by decision-relevance (most important first).
3. **Balance: ≥3 positive and ≥3 negative.** At least three clearly positive and at least three clearly negative insights; the remainder may be mixed. Tag each insight `[+]`, `[–]`, or `[±]`.
4. **Accurate tally.** Open with a tally line counting the tags exactly, e.g. `Positive: 4 · Negative: 3 · Mixed: 3`. The counts must match the tags in the list (they must also satisfy the ≥3/≥3 floor).
5. **Every item traceable to a real report location.** Each insight ends with a parenthetical pointer to the actual table/section/footnote/appendix it comes from (e.g. `(Table 4 — Current P/B / Current vs 10-yr avg rows)`, `(Appendix C)`). The pointer must reference a location that genuinely exists in the report and genuinely supports the claim.
6. **No outside facts, no forecasts, no investment advice.** State what the report shows. Do not add data the report does not contain, do not predict, do not recommend buying/selling/holding.
7. **Heading and scope conventions (exact):**
   - Title: `## Executive Summary — Top 10 Insights`.
   - Immediately below the title: the tally line (`Positive: N · Negative: N · Mixed: N`).
   - Then the numbered 1–10 list; each item leads with a bold one-line claim, tagged `[+]/[–]/[±]`, followed by the supporting figures and the source pointer.
   - Final line: a scope line naming the sole source and the report version, and stating it is not investment advice — e.g. `Scope: derived solely from reports/sg-banks/report.md (v<version>). Not investment advice.`
8. **Self-check before overwrite.** Before writing the file, verify: exactly 10 items; ≥3 `[+]` and ≥3 `[–]`; tally matches tags; every figure quoted appears in the report; every source pointer resolves to a real, supporting location; no outside facts / forecast / advice; headings and scope line exactly as above. Only then overwrite `reports/sg-banks/execsummary.md`.

## How to run this module

1. Read `reports/sg-banks/report.md` end to end (closed-book — no other inputs).
2. Draft candidate insights, each tied to a specific report location; pick the 10 most decision-relevant, ensuring the positive/negative floor.
3. Rank them, tag them, write the tally line, and add the scope line with the current report version (from `reports/sg-banks/meta.json` `current_version`).
4. Run the self-check in §8.
5. Overwrite `reports/sg-banks/execsummary.md`. Commit.

## Acceptance criteria (stop when all true)
- Exactly 10 ranked insights; ≥3 positive and ≥3 negative; tally line accurate.
- Every insight traces to a real, supporting location in `report.md`; every quoted figure appears there.
- No outside facts, no forecasts, no investment advice.
- Headings, tally line, and scope line follow the exact conventions above.
- Produced closed-book (report-only); no Orchestrator/search used.
