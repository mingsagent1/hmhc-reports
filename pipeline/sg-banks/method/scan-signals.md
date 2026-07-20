# sg-banks — Scan-Signals SOP (earnings + media, recency-biased)

> ## ⚠ Cost gate — opt-in only (read first)
> This module runs **live web retrieval** across many sources and is **token/time-intensive**. **Do NOT run it unless the user has explicitly requested it AND confirmed in chat** (the UPDATE controller's Step 2b cost gate). If you have reached this file without that explicit confirmation, **stop and ask for it first** — do not begin scanning.

**Module:** Scan · **Input:** `guides/frame.md` · **Output:** `data/signals.md` · **Depends on:** Frame
**Run on:** Orchestrator or **GPT-5.6** (search-heavy — **must** use live web/search; the opposite of the closed-book Exec Summary). Non-Claude keeps it independent of the Claude-built numeric work.

## Purpose

Gather **qualitative signals** about DBS, OCBC, and UOB from earnings and media — the narrative counterpart to the numeric ledger. Like `update-ledger`, this step **gathers raw, sourced, dated signals only**. It does **not** draw cross-bank conclusions, rank, or write prose — that is Assemble's job. One signal = one sourced statement.

## Step 0 — Read the Frame first

Open `guides/frame.md`. The human's big questions define what matters. Ensure every Frame question has at least one signal per bank addressing it (or an explicit "no recent disclosure"). You may gather beyond the Frame, but the Frame themes are mandatory coverage.

## Recency policy (the point of this module)

Stamp an **as-of date** (run date, SGT) at the top of the output. Classify every signal into a recency band and **weight accordingly**:

- **Primary** — the most recently reported quarter/half **plus** any management guidance issued since. The "current view" the report rests on. Cover thoroughly.
- **Context** — the immediately prior quarter and the year-ago comparable. For direction/change only.
- **Trend** — older. Include **only** if it establishes a multi-period trend a Frame question asks about; mark `Trend`.

Rules:
- **Never present a Context/Trend statement as the current stance.** On conflict, prefer the newest, most authoritative source and **note the change** ("NIM guidance revised from ~2.0% to ~1.9%, Q1'26 call").
- **Latest guidance supersedes** older guidance on the same metric.
- If one bank's newest results predate a peer's, say so — don't let uneven reporting dates read as a real gap.

## Source hierarchy

- **Tier 1 (preferred):** earnings-call transcripts, quarterly/FY results presentations & press releases, SGX announcements/filings, annual reports, official guidance.
- **Tier 2 (allowed, always marked):** reputable financial media — The Business Times, Reuters, Bloomberg, CNBC, Financial Times, Straits Times (business).
- **Avoid / flag:** forums, social, unattributed blogs, rumor. A lead from these is `unverified` and needs Tier-1 confirmation before it counts.
- **Every signal needs ≥1 dated source.** A Tier-2-only signal is flagged `needs-T1`.

## Themes to cover (per bank)

NIM & rate outlook · deposits & CASA · wealth / AUM flows · credit quality & provisions (NPL, GP/SP) · capital, dividends & buybacks · cost/efficiency (CIR) · **changes in management guidance** · notable strategy/events (M&A, regulatory, leadership). Cover the Frame themes at minimum.

## Signal record — schema for `data/signals.md`

One row per distinct statement. Group by bank; within a bank order Primary → Context → Trend.

| Field | Meaning |
|---|---|
| `id` | `SCN-<bank>-###` |
| `bank` | DBS / OCBC / UOB |
| `date` | date of the **source** (YYYY-MM-DD) |
| `period` | period the statement is about (Q1'26, FY2025, guidance-FY26) |
| `theme` | NIM / CASA / WealthAUM / Credit / Capital / Cost / Guidance / Strategy |
| `band` | Primary / Context / Trend |
| `polarity` | `+` / `–` / `±` / `context` |
| `type` | fact / guidance / commentary / media |
| `signal` | the statement, 1–2 factual sentences (no spin, no editorializing) |
| `tier` | T1 / T2 (add `needs-T1` if T2-only) |
| `src` | superscript ref → numbered source in the appendix |
| `conf` | high / med / low |

Distinguish **fact** (reported outcome), **guidance** (forward management statement), **commentary** (management framing/spin — tag it, don't launder as fact), **media** (third-party). Keep figures **as stated, in SGD**; don't convert or compute.

## Conflict & dedupe

- One record per distinct statement; cite the most authoritative Tier-1, note others only if additive.
- Disagreement ⇒ keep the newest/most-authoritative as the signal, add a one-line `conflict:` note.
- **No fabrication.** If a theme has **no recent disclosure**, record exactly that — an honest gap beats an invented signal.

## Output file layout (`data/signals.md`)

```
# sg-banks — Signals (Scan output)
As-of: <YYYY-MM-DD SGT> · Provenance: <YYMMDD-NNN> <Harness><Model>  (e.g. 20260720-001 PxGPT5.6)
Latest period covered: DBS <…> · OCBC <…> · UOB <…>

## DBS
<signal table>
### Sources (DBS)
1. <publisher, title, date, URL>
…

## OCBC
…

## UOB
…

## Coverage gaps / no-recent-disclosure
- <bank/theme>: no recent disclosure as of <date>.
```

Provenance stamp matches the ledger: `YYMMDD-NNN <Harness><Model>` (Perplexity + GPT-5.6 ⇒ `PxGPT5.6`).

## Self-check before writing the file (all must pass)

1. As-of date and latest-period-per-bank are stated.
2. Every Frame question has ≥1 signal per bank, or an explicit "no recent disclosure".
3. Every signal is dated, sourced, and tagged (`band`, `polarity`, `type`, `tier`).
4. Every bank has a populated **Primary** band (or a stated reason it can't).
5. No cross-bank synthesis, ranking, or conclusions.
6. Tier-2-only signals flagged `needs-T1`.
7. Figures as-stated in SGD; nothing computed.

If any check fails, fix and re-verify before saving `data/signals.md`.

## Hand-off
`data/signals.md` feeds **Assemble** (`method/build-report.md`) and **ExecSummary** downstream. Scan itself publishes nothing to `reports/`.
