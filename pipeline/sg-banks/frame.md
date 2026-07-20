# SG Banks — Frame (thesis · key questions · good-vs-bad rubric)

> **Project:** Singapore Bank Stock Accumulation Strategy
> **Artifact:** `pipeline/sg-banks/frame.md` — the framing artifact. Produced by `pipeline/sg-banks/method/frame.md`; version history in git.
> **Status:** Living document — revisited at the start of each report version.
> **Scope:** DBS (D05) · OCBC (O39) · UOB (U11). FY2016–FY2025 + latest 2026 interim. **SGD only.** Descriptive analysis, **not investment advice.**

---

## Thesis

Singapore's three major banks are the listed proxy for Singapore's standing as a **regional wealth and deposit hub**. The project's working hypothesis is that the franchise worth measuring is a bank's **structural ability to attract assets** — sticky customer deposits, low-cost CASA funding, and capital-light wealth AUM — and to convert those attracted assets into durable income across a full rate cycle. Balance-sheet *size* (total assets, wholesale-funded leverage) is explicitly **not** the thesis; assets *attracted* are.

The reconciled `Tables` component is the evidentiary spine of this thesis: it lays out each bank's income engine, deposit/CASA/AUM attraction base, net interest margin against the rate cycle, and valuation/returns — all on Tier-1 sourced, dual-checked numbers, so the thesis is argued from data rather than narrative.

## Key questions

1. **Who attracts assets best?** How have customer deposits, CASA quality, and wealth AUM grown per bank over FY2016–2025, and what does that say about franchise strength? *(→ Table 2; deposits+CASA benchmark note.)*
2. **How durable is the income engine?** How do NII, non-NII, total revenue, and net profit compound per bank, and how efficiently is each pool of attracted assets converted to revenue and profit? *(→ Table 1 per bank + Rev/Dep, Profit/Dep, Profit/Rev.)*
3. **How rate-cycle-dependent are margins?** How did group NIM move with 3M SORA and Fed funds through the 2022–23 peak and the subsequent reversal, and what is guidance for FY2026? *(→ Tables 3 and 5.)*
4. **What are investors paying for it?** Where do current P/B and P/TB sit versus each bank's own 10-yr and 5-yr history, and how do ROE/RoTE compare? *(→ Table 4 + P/TB block.)*
5. **How much can we trust the numbers?** Which cells are Tier-1 dual-verified vs single-retriever or model-correlated, and what should be spot-checked before high-stakes use? *(→ Appendix A provenance caveat; ledger stamps.)*

## Good-vs-bad rubric

A **good** answer to this brief:
- Uses **Tier-1 company disclosures** (annual-report financial summaries, full-year results releases, SGX filings) for every fundamental; market data only for prices/shares/rates.
- Marks honestly: `n/r` (not retrieved from Tier-1) and `n/d` (bank does not disclose) are correct answers; a suspiciously complete table is a failure mode.
- Reads **within-bank trends over a full cycle**, and never makes false cross-bank comparisons on definitionally non-comparable lines (wealth income, AUM definitions).
- Ties out mechanically (NII + non-NII = total income; DBS group-NIM canary 2.01%) and explains every >30% YoY move and every checksum mismatch by a definitional cause.
- Separates the **quality overlay** (CASA, cheap sticky money) from raw deposit size, and never sums deposits + AUM (double-count risk).
- Stays **descriptive** — data and factual footnotes only, no buy/sell view.

A **bad** answer:
- Pulls fundamentals or ratios from aggregators/screeners/brokers (Yahoo, GuruFocus, Investing.com, Simply Wall St, etc.) when the bank publishes them.
- Estimates, interpolates, or fills from memory instead of marking `n/r`.
- Treats total-asset size as asset-attraction, or compares AUM levels across banks as if the definitions matched.
- Hides a failed tie-out or an unexplained discontinuity.
- Presents an investment recommendation or price target.

## Open framing questions (carry forward)

- **`TotalAssets` "net"** — currently defined as consolidated total assets; confirm whether a narrower definition is intended (see `index.md` open decisions).
- **Model correlation** — several un-checksummed cells were retrieved by two Claude Opus 4.8 passes; the thesis' confidence rubric wants a non-Claude retriever pass before those cells are relied on. *(→ handled by Retrieve/Scan modules.)*
- **Scan not yet integrated** — the qualitative signal layer (`data/signals.md`) is scaffolded but not yet run, so the current report is built from Tables alone; a future version should fold dated Tier-1 signals into the narrative.
