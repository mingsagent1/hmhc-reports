# SG Banks — Frame (thesis · key questions · good-vs-bad rubric)

> **Project:** Singapore Bank Stock Accumulation Strategy
> **Artifact:** `pipeline/sg-banks/frame.md` — the framing artifact. Produced by `pipeline/sg-banks/method/frame.md`; version history in git.
> **Status:** Living document — revisited at the start of each report version. **Refreshed 2026-07-20 for the 1Q2026 update.**
> **Scope:** DBS (D05) · OCBC (O39) · UOB (U11). FY2016–FY2025 long-run base + **1Q2026 interim (quarters ended 31 Mar 2026) + current (as-of 2026-07-20) valuation.** **SGD only.** Descriptive analysis, **not investment advice.**

---

## Thesis

Singapore's three major banks are the listed proxy for Singapore's standing as a **regional wealth and deposit hub**. The project's working hypothesis is that the franchise worth measuring is a bank's **structural ability to attract assets** — sticky customer deposits, low-cost CASA funding, and capital-light wealth AUM — and to convert those attracted assets into durable income across a full rate cycle. Balance-sheet *size* (total assets, wholesale-funded leverage) is explicitly **not** the thesis; assets *attracted* are.

The reconciled `Tables` component is the evidentiary spine of this thesis: it lays out each bank's income engine, deposit/CASA/AUM attraction base, net interest margin against the rate cycle, and valuation/returns — all on Tier-1 sourced, dual-checked numbers, so the thesis is argued from data rather than narrative.

### 1Q2026 refresh lens (what changed since the FY2025 build)

The FY2025 base was built at the top of a normalising-but-still-elevated rate regime. The material development in 1Q2026 is a **regime shift in Singapore rates**: 3M SORA averaged ~1.07% in 1Q26 versus ~2.54% in 1Q25, compressing group NIM and net interest income at all three banks. This refresh therefore re-centres the thesis on a live stress test:

- **Rate-regime test.** With NII falling YoY across the group, is the deposit/CASA franchise still the durable earnings anchor, or does the earnings mix now depend on the fee/wealth cycle? *(NIM 1Q26: DBS 1.89% · OCBC 1.76% · UOB 1.82%; all down YoY.)*
- **Wealth / non-interest-income offset.** Record wealth-management and non-interest income are the stated offset to NII compression (DBS wealth fees +25% YoY, OCBC non-II +23% YoY with wealth fees +34%). The test is whether the capital-light fee engine can hold total income "at or around 2025 levels" as management guides — and which bank monetises attracted assets best when rates fall.
- **Credit / provision risk.** Falling rates arrive alongside macro/tariff uncertainty. OCBC booked S$191m of management-overlay allowances; UOB credit costs are elevated at 26bps with Greater-China NPAs rising; UOB's FY2025 pre-emptive general provision still distorts YoY comparisons. Asset quality and provisioning are now a first-order lens, not a footnote.
- **Valuation.** The re-rating documented at FY2025 is re-checked against **as-of 2026-07-20 intraday prices** and FY2025 book/tangible-book denominators, versus each bank's own long-run P/B and P/TB history.
- **Latest guidance.** FY2026 guidance is captured per bank at its stated vintage (DBS qualitative, updated 30 Apr 2026; OCBC and UOB quantitative, set at FY2025 results Feb 2026) — never blended across banks.

## Key questions

1. **Who attracts assets best?** How have customer deposits, CASA quality, and wealth AUM grown per bank over FY2016–2025, and what does that say about franchise strength? *(→ Table 2; deposits+CASA benchmark note.)*
2. **How durable is the income engine?** How do NII, non-NII, total revenue, and net profit compound per bank, and how efficiently is each pool of attracted assets converted to revenue and profit? *(→ Table 1 per bank + Rev/Dep, Profit/Dep, Profit/Rev.)*
3. **How rate-cycle-dependent are margins?** How did group NIM move with 3M SORA and Fed funds through the 2022–23 peak and the subsequent reversal — and now into the 1Q2026 downshift (SORA ~1.07%) — and what is FY2026 guidance? *(→ Tables 3 and 5; 1Q2026 snapshot.)*
4. **Does the fee/wealth engine offset NII compression?** As NII falls YoY in 1Q26, can record non-interest / wealth income hold total income and profit near 2025 levels, and which bank converts attracted assets to fees best? *(→ 1Q2026 snapshot; Table 1 mix.)*
5. **What are investors paying for it?** Where do current P/B and P/TB sit versus each bank's own 10-yr and 5-yr history, and how do ROE/RoTE compare? *(→ Table 4 + P/TB block; as-of 2026-07-20 valuation.)*
6. **Is asset quality holding as rates fall?** How do CET1, NPL, credit costs and provisioning overlays look in 1Q26, and how much of the YoY change is the UOB FY2025 pre-emptive-provision base effect vs genuine deterioration? *(→ 1Q2026 snapshot; Appendix C.)*
7. **How much can we trust the numbers?** Which cells are Tier-1 dual-verified vs single-retriever or model-correlated, and what should be spot-checked before high-stakes use? *(→ Appendix A provenance caveat; ledger stamps.)*

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
- **Scan integrated this refresh** — `data/signals.md` is now populated with a dated 1Q2026 Tier-1/Tier-2 signal register (evidence-grounded), folded into the Assemble narrative. Signals remain descriptive.
- **1Q2026 rows are single-retriever (`single-cl`)** — the 1Q26 interim block was retrieved in one Claude pass from the evidence set; it is not yet dual-checked. UOB income-statement detail is Tier-2-host (bank CFO/CEO slides via MarketScreener) because UOB's own PDFs were not directly retrievable in-session. Spot-verify against UOB's own release before high-stakes use.
- **UOB 1Q26 non-II components don't reconcile** — the CFO-slide breakdown (fee 637 + T&I 405 + other 462 = 1,504) does not equal total income − NII (3,422 − 2,324 = 1,098); the tie-out-consistent derived non-II (1,098) is used and the slide breakdown is flagged as an unresolved retrieval gap.
- **Official 3M SORA temporarily `n/d`** — the MAS statistics portal was under maintenance on 2026-07-20; the bank-characterised 1Q26 average (~1.07%, DBS transcript) is used as interim context and re-fetch is required before publishing a hard SORA number.
