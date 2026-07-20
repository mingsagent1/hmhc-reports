# Scan — Module SOP: Qualitative Signal Sweep (SG Banks)

> **Project:** Singapore Bank Stock Accumulation Strategy
> **Artifact:** `pipeline/sg-banks/method/scan.md` — version history in git (`git log --oneline pipeline/sg-banks/method/scan.md`).
> **Status:** Draft — module defined; not yet run (its output `data/signals.md` is a scaffold).

## Module contract

| | |
|---|---|
| **Inputs** | `pipeline/sg-banks/frame.md` (thesis + key questions — tells Scan what to look for) and current Tier-1 / Tier-2 public sources (earnings calls, guidance, filings, reputable media). |
| **Sole output** | `pipeline/sg-banks/data/signals.md` — a dated, sourced list of qualitative signals. It writes **no** numeric ledger cells and **no** report. |
| **Idempotence** | A rerun overwrites `data/signals.md` in place. Git retains history; no timestamped copies. Each rerun should re-establish the recency window from scratch rather than appending stale items. |
| **Recommended model** | A **search-grounded** model — **GPT-5.6** (or the nearest available non-Claude search-grounded model). Scan is a live-web reading task and requires current search access. |
| **Position** | `Frame → (Retrieve ‖ Scan) → [human/Claude Reconcile] → Tables → Assemble → …`. Scan runs in parallel with Retrieve. Its output feeds the **Assemble** step (narrative colour), not the deterministic Tables step. |

## What Scan is for

Retrieve captures the hard numbers into the ledger. **Scan captures the qualitative narrative around them** — management commentary, strategy shifts, guidance changes, one-off events, and credible market reporting — so the Assemble step can add sourced context to the tables without inventing anything. Scan is the pipeline's answer to "what is management actually saying, and what just happened this quarter?"

## Recency bias

Scan is deliberately **recency-weighted**. Prioritise the **latest 1–2 quarters** and the most recent full-year guidance. Older context is included only when it is needed to make a recent signal legible (e.g. a prior-year restatement that a current call references). The goal is a current-state snapshot, not a history — the tables already carry the multi-year series.

## Tiering — keep the two tiers visibly separate

Every signal is filed under exactly one tier, and the two tiers are kept in separate sections of the output so a reader can weight them differently:

- **Tier 1 — primary company disclosure.** Earnings-call transcripts and remarks, management guidance, results media releases, and SGX/annual-report filings. These are the bank speaking for itself. Highest trust.
- **Tier 2 — reputable media.** Established financial press and wire coverage (e.g. major newswires and business dailies) reporting on the banks. Usable for context and for events not yet in a filing, but always attributed and never promoted to Tier-1 status.

Anything that would be Tier-3 under the retrieval hierarchy (aggregators, screeners, forums, social) is **out of scope** — do not record it.

## Rules

1. **Every signal is dated and sourced.** A signal with no date or no attributable source is not recorded. Format each as: a one-line factual statement, the date it refers to (or was published), and the source (document type + issuer + period, or outlet + headline + date).
2. **No unsourced synthesis.** Scan records what sources say; it does not editorialise, forecast, or connect dots into a conclusion. Interpretation is the Assemble step's job, and only from sourced inputs.
3. **No numbers that belong in the ledger.** If a signal is fundamentally a hard financial figure, its home is Retrieve/the ledger, not here. Scan may quote a figure a source states, but only as attributed context (e.g. "CEO said FY26 NIM guidance 1.75–1.80%"), never as a reconciled data point.
4. **No investment advice.** Descriptive only.
5. **Tie back to the frame.** Prefer signals that bear on the thesis and key questions in `frame.md` (asset attraction, income durability, rate-cycle sensitivity, valuation, data confidence).

## How to run this module

1. Read `frame.md` for the thesis and key questions.
2. Sweep Tier-1 sources first (latest earnings calls, guidance, filings for DBS/OCBC/UOB), then Tier-2 media for the same recent window.
3. Record each signal under its tier with date + source, using the schema in the current `data/signals.md` scaffold.
4. Keep the recency window tight (latest 1–2 quarters + current guidance).
5. **Overwrite** `pipeline/sg-banks/data/signals.md`. Commit with a descriptive message and set its status header to "run" with the run date.

## Acceptance criteria (stop when all true)
- `data/signals.md` contains only dated, sourced signals, each filed under Tier-1 or Tier-2.
- No unsourced synthesis, no forecasts, no investment view.
- Recency window is the latest 1–2 quarters + current guidance (older items only as needed for legibility).
- No hard financial figures that belong in the ledger are presented as data points here.
