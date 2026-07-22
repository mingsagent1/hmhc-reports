# sg-banks — Write-Conclusions SOP (answers to the Key Questions + thesis score)

**Module:** Write-Conclusions · **Inputs:** `guides/frame.md` (thesis + key questions) **+** `reports/sg-banks/report.md` (excluding its own Conclusions section) **+** `pipeline/sg-banks/data/signals.md` (if present) · **Output:** the **Conclusions** section of `reports/sg-banks/report.md` (between markers) · **Depends on:** Build-Report, Frame
**Run on:** **GPT-5.6** — **grounded, NO web search.** Independent of the Claude-built body.
**Changelog:** 2026-07-21 (later) — module renamed Write-Conclusions; the report section is now titled "Conclusions". · 2026-07-21 — reformatted from "top-10 insights" to "answers to the Frame's key questions + thesis score" per the author's decision. · 2026-07-20 — first closed-book run (top-10 format).

## Grounding rule (hard wall)
Use **only three sources**:
1. **`guides/frame.md`** — the thesis and key questions being answered (structure only; never a source of facts),
2. the **report body** — Interpretation, Key Data tables, footnotes, and Appendices — **excluding the existing Conclusions section** (never summarize your own prior conclusions), and
3. **`data/signals.md`** if present (the recency-biased earnings/media signals from the Scan module).

No web search, no outside knowledge, no number/name/date that isn't in sources 2–3.

## Task

1. **Answer each key question in `guides/frame.md`, in order** (currently 7). Each answer: 2–4 sentences, grounded in the report/signals, **cited to a real location** — a report table/section/appendix (e.g. "Table 2", "Appendix C") and/or a signal id (e.g. "SCN-DBS-003"). Open each answer with a polarity marker: `+` (supports the thesis), `–` (against), `±` (mixed).
2. **Honesty rule — pending questions.** Where the report and signals cannot support an answer (currently **Q2** — cross-hub wealth flows, **Q4** — larger-bank / other-hub precedent, and **Q6** — pricing vs other wealth-hub banks; check `index.md` open questions for the current list), write exactly: *"Pending new research module — not answerable from current data."* Do not synthesize an answer from outside knowledge, and cite nothing.
3. **Thesis score.** Score the Frame's thesis **0–100** on current evidence (100 = the evidence fully supports it). Give the score, a 2–3 sentence rationale naming the strongest supporting and opposing evidence (cited), and one sentence on the **decision rule** (current capital-attraction momentum vs the kill signal). *Note: a multi-model "AI council" scoring mechanism may later replace the single-model score (design pending, Perplexity-led); until then one closed-book model scores.*

No forecasts beyond what the sources state. Neutral tone. Not investment advice.

## Output — write into `report.md` between markers
Replace everything between these markers:
```
<!-- conclusions:start -->
## Conclusions — Answers to the Key Questions

1. **[±] <short label of Q1>** — <answer>. (source)
2. **[–] <short label of Q2>** — Pending new research module — not answerable from current data.
…
7. **[+] <short label of Q7>** — <answer>. (source)

**Thesis score: NN/100.** <rationale with cited strongest evidence for and against>. Decision rule: <capital-attraction momentum status>.

Scope: questions from guides/frame.md; grounded in report.md + data/signals.md (v<version>). Not investment advice.
<!-- conclusions:end -->
```
Question numbering and order must match `guides/frame.md` exactly. This module **only** (re)writes this section — it never edits tables or appendices, so it is independently rerunnable on the lite path.

## Self-check before saving (all must pass)
1. Every Frame key question is answered **or** carries the exact pending-research line — none skipped, none invented.
2. Every non-pending answer cites a report location and/or signal id **that actually exists** in the sources.
3. No fact/number appears that isn't in `report.md` or `data/signals.md`.
4. The thesis score is present, 0–100, with a cited rationale and the decision-rule sentence.
5. You did **not** use the prior Conclusions section as a source.
6. Numbering/order matches `guides/frame.md`.

If any check fails, fix and re-verify before writing.
