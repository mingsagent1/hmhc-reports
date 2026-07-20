# sg-banks — Write-ExecSummary SOP (Top-10 insights)

**Module:** ExecSummary · **Inputs:** `reports/sg-banks/report.md` (excluding its own Executive Summary section) **+** `pipeline/sg-banks/data/signals.md` (if it exists) · **Output:** the **Executive Summary** section of `reports/sg-banks/report.md` (between markers) · **Depends on:** Assemble, Scan (optional), Frame
**Run on:** **GPT-5.6** — **grounded, NO web search.** Independent of the Claude-built body.

## Grounding rule (hard wall)
Use **only two sources**:
1. the **report body** — Interpretation, Key Data tables, footnotes, and Appendices — **excluding the existing Executive Summary section** (never summarize your own prior summary), and
2. **`data/signals.md`** if present (the recency-biased earnings/media signals from the Scan module).

No web search, no outside knowledge, no number/name/date that isn't in one of those two files.

## Task
Produce the **Top 10 insights**, ranked by materiality.
- **≥3 clearly positive** and **≥3 clearly negative**; the rest may be mixed/neutral. Exactly 10.
- **Every insight cited to a real location:** a report table/section/appendix (e.g. "Table 2 (NIM)", "Appendix B") **and/or** a signal id from signals.md (e.g. "SCN-DBS-003"). Insights that rest on signals should prefer the most recent **Primary-band** signals and may tag "(latest: Q_'26)".
- No forecasts beyond what the sources state. Neutral tone. Not investment advice.

## Output — write into `report.md` between markers
Replace everything between these markers (add them around the Executive Summary section if absent):
```
<!-- execsummary:start -->
## Executive Summary — Top 10 Insights

Positive: X · Negative: Y · Mixed: Z

1. **[+] <one-sentence insight>** <one sentence of specifics>. (source)
2. **[–] <one-sentence insight>** <one sentence of specifics>. (source)
…
10. **[±] <one-sentence insight>** <one sentence of specifics>. (source)

Scope: grounded in report.md + data/signals.md (v<version>). Not investment advice.
<!-- execsummary:end -->
```
Markers: `+` positive, `–` negative, `±` mixed. Tally must hold (X≥3, Y≥3, X+Y+Z=10). Order by materiality, not polarity. This module **only** (re)writes this section — it never edits tables or appendices, so it is independently rerunnable on the lite path.

## Self-check before saving (all must pass)
1. Exactly 10 insights.
2. ≥3 marked `+` and ≥3 marked `–`.
3. Every insight cites a report location and/or a signal id **that actually exists** in the sources.
4. No fact/number appears that isn't in `report.md` or `data/signals.md`.
5. You did **not** use the prior Executive Summary as a source.
6. The tally line matches the markers used.

If any check fails, fix and re-verify before writing.
