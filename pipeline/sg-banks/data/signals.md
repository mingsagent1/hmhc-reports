# SG Banks — Signals (qualitative scan output)

> **Project:** Singapore Bank Stock Accumulation Strategy
> **Artifact:** `pipeline/sg-banks/data/signals.md` — sole output of `pipeline/sg-banks/method/scan.md`.
> **Status:** ⚠️ **SCAFFOLD — SCAN HAS NOT YET BEEN RUN.** This file is an empty template. It contains **no signals**. The schema below is exactly what the Scan module will overwrite when it runs.
> **Banks:** DBS (D05) · OCBC (O39) · UOB (U11). **Recency window (when run):** latest 1–2 quarters + current guidance. **Descriptive only — not investment advice.**

---

## Run status

- **Last run:** _never_ — this is a pre-run scaffold.
- **Model:** _n/a_ (Scan requires a search-grounded model; see `method/scan.md`).
- When Scan runs, replace this block with: last-run date, model/harness used, and the recency window actually covered.

**Because Scan has not run, the current `reports/sg-banks/report.md` is assembled from Tables alone.** The Assemble step (`method/build.md`) is instructed to treat this file as empty and to mark, rather than invent, any narrative that signals would have supplied.

---

## Schema (what Scan writes — do not fabricate)

Each signal is one row under its tier, in this shape:

- **Signal** — a one-line factual statement of what was said or what happened.
- **Date** — the date the signal refers to, or its publication date (`YYYY-MM-DD`).
- **Source** — Tier-1: document type + issuer + period (e.g. "DBS FY2026 results call, 4Q26"). Tier-2: outlet + headline + date.
- **Bearing** — which `frame.md` key question it touches (attraction / income durability / rate cycle / valuation / data confidence).

### Tier 1 — primary company disclosure (earnings calls · guidance · filings)

_(empty — no signals recorded; populate on first Scan run)_

| Signal | Date | Source | Bearing |
|---|---|---|---|
| _n/r_ | _n/r_ | _n/r_ | _n/r_ |

### Tier 2 — reputable media

_(empty — no signals recorded; populate on first Scan run)_

| Signal | Date | Source | Bearing |
|---|---|---|---|
| _n/r_ | _n/r_ | _n/r_ | _n/r_ |

---

<sub>`n/r` here means the scan has not been run, not that nothing exists to find. Do not fill these tables from memory, aggregators, or unsourced synthesis — run `method/scan.md` with a search-grounded model, which will overwrite this file.</sub>
