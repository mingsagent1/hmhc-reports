# sg-banks — Frame

> This document contains the thesis and key questions the report seeks to answer. The HUMAN authors and approves the file; the AGENT proposes wording. The key questions should be answered in the Conclusions section of the report, and be supported by the various Data.

## Thesis
Over a **10–15 year** horizon, Singapore keeps attracting and growing the wealth — deposits and AUM — that the world parks and moves through it, and DBS, OCBC and UOB monetize that growing capital base into income and are valued accordingly. The fundamental driver is **capital attraction**: as long as deposits and wealth AUM keep growing (capital continuing to move into Singapore), the banks will find a way to monetize it — rates and spreads move up and down, and new products get created — much as far larger global banks already earn on, and are valued on, multi-trillion deposit bases. The question for a **core asset allocation** is whether that capital attraction continues, and if so, to what extent it is already in the price.

## Key Questions

**A. Capital attraction — the primary driver**

1. What is the trend for Deposits and Wealth AUM?
   *(Format: `Bank_Metric: S$bn, CASA %, 5y-CAGR %, FY25 %, FY24 %, FY23 %, FY22 %` — metrics per bank: **Deposits**, **Wealth AUM**, and **Capital Base** = customer deposits + wealth AUM (internal note: included to see how consistent the various AUM/deposit/capital-base definitions are). Each `FYxx %` = that FY's YoY growth; CASA % applies to the Deposits rows as the deposit-quality marker; "5y" = latest FY vs FY five years prior; latest-quarter YoY as a dated secondary where available.)*

2. What is the trend in wealth-hub capital flows over the last 5 years?
   *(Format: `WealthHub: US$tn, 5y-CAGR %, FY25 %, FY24 %, FY23 %, FY22 %` — Singapore versus Hong Kong, Switzerland, and other relevant hubs. Cross-hub macro is reported in USD as sourced — a deliberate exception to the SGD-only rule, which applies to bank financials.)*

**B. Monetization — secondary (expected to follow attraction)**

3. What is the trend in NII and Other Revenue?
   *(Format: `Bank_Metric: S$bn, 5y-CAGR %, FY25 %, FY24 %, FY23 %, FY22 %` — metrics per bank: NII and OR. Each `FYxx %` = that FY's YoY growth. OR = total income − NII.)*

4. How volatile and cyclical is NIM?
   *(Format: **line chart** — group NIM per bank vs **3M SORA (FY avg)** and **effective Fed funds (FY avg)** (theoretical Fed → SORA → NIM transmission), FY2016–25 + latest, generated deterministically from the ledger (`method/code/build_charts.py` → `reports/sg-banks/assets/nim-vs-sora.svg`); plus one or two sentences on the swing — trough → peak → latest — and the group pattern.)*

5. What is the monetization score of the SG banks versus benchmark peers?
   *(Format: **one table**, SG banks + all peers, latest available FY, index bank = 100:
   `Bank | Monetization_vDeposits (index) | Monetization_vCapitalBase (index) | Top Other-Revenue categories (% of total revenue)`
   **`Monetization_vDeposits`** = total revenue ÷ customer deposits — monetization of the sticky on-balance-sheet base.
   **`Monetization_vCapitalBase`** = total revenue ÷ (customer deposits + wealth AUM) — monetization of the full attracted-capital base.
   The second deliberately sums deposits + AUM as a service-base denominator — a noted exception to the never-sum-for-attraction rule — and AUM definitions differ across banks and overlap deposits, so the two indices are always read together. The last column is compact per bank — the top-3 non-NII categories of any significance, e.g. "insurance 23% · fees 19%"; `n/d` where a bank does not disclose the split. Benchmarks: the peer set below.)*

**C. Relative valuations**

6. What is the relative valuation premium of the SG banks versus benchmark peers, and what annual growth outperformance over the next 5 years would justify it?
   *(Format: same peers and index bank as Q5; **four valuation indexes**, each indexed to the index bank = 100, using market cap and latest-FY denominators:
   **`P/CapitalBase`** = market cap ÷ (customer deposits + wealth AUM) — valuation per unit of attracted capital, the primary-driver lens.
   **`P/Rev`** = market cap ÷ total revenue — valuation of monetization ability.
   **`P/E`** = market cap ÷ net profit — the standard earnings lens.
   **`P/B`** = market cap ÷ book equity — included as the banking convention, relevance viewed with skepticism.
   Required outperformance per index = (premium ratio)^(1/5) − 1 per year — the extra annual growth in that index's denominator (capital base / revenue / earnings / book) needed for multiples to converge to the index bank's within 5 years. Present as **one table**, SG banks + all peers:
   `Bank | Price (local ccy/share, as-of date) | P/CapitalBase | req %/yr | P/Rev | req %/yr | P/E | req %/yr | P/B | req %/yr`
   The Price column is the staleness/relevance marker: each bank's local per-share price with the date it was taken (the same dated market data behind its market cap). Comment on whether the spread between DBS, OCBC and UOB is justified by fundamentals.)*

## Benchmark peer set (used by Q5 & Q6)

**Selection criteria:** universal/commercial banks in the same category as the SG banks — large retail deposit bases **and** substantive wealth-management arms (wealth AUM ≳ US$500bn where disclosed) — drawn from distinct wealth-hub or major-banking jurisdictions. Pure investment banks and pure asset/wealth managers are excluded.

| Peer | Jurisdiction | Note |
|---|---|---|
| **HSBC** | Hong Kong / UK | **index bank = 100** — closest business model, competing wealth hub |
| UBS | Switzerland | Swiss-hub wealth giant |
| JPMorgan Chase | US | universal; caveat: large investment-banking share |
| Bank of America | US | commercial + Merrill wealth |
| Standard Chartered | UK / Asia hubs | Asia-footprint universal bank |
| China Merchants Bank | China | China's retail/wealth leader |
| Commonwealth Bank | Australia | deposit-rich; wealth arm small post-divestments — read `Monetization_vDeposits` primarily |

## Decision rule
The decisive signal is capital-attraction momentum: if deposit and wealth-AUM growth stalls or reverses — capital no longer moving into Singapore — the narrative and the premium die with it, and the asset is not allocated regardless of the other answers.
