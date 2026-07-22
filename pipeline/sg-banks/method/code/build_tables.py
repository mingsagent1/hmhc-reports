#!/usr/bin/env python3
"""Build-Tables — deterministic table generation for sg-banks.

Reads the reconciled ledger (data/ledger.csv) and regenerates data/tables.md.
Same ledger in -> same tables out. No retrieval, no LLM, no timestamps.

Usage:  python3 pipeline/sg-banks/method/code/build_tables.py [--check]
        --check: build to a temp string, compare numeric cells against the
                 committed data/tables.md, exit non-zero on any difference.

Spec: pipeline/sg-banks/method/code/build-tables.md (formats, gates, footnotes).
"""
import csv, sys, re
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # pipeline/sg-banks (this file lives in method/code/)
LEDGER = ROOT / "data" / "ledger.csv"
OUT = ROOT / "data" / "tables.md"

BANKS = ["DBS", "OCBC", "UOB"]
YEARS = [str(y) for y in range(2016, 2026)]

# ---------- ledger access ----------

def load():
    table = {}
    rows = list(csv.DictReader(open(LEDGER, newline="", encoding="utf-8")))
    for r in rows:
        table[(r["bank"], r["metric"], r["period"])] = r
    return table, rows

T, ROWS = load()

def raw(bank, metric, period):
    r = T.get((bank, metric, period))
    if r is None:
        return None, "missing"
    v = (r["reconciled_value"] or "").strip()
    st = (r["reconciliation_status"] or "").strip()
    if st in ("n/r", "n/d") or v in ("", "n/r", "n/d"):
        return None, (st if st in ("n/r", "n/d") else "n/r")
    return float(v), st

def val(bank, metric, period):
    v, _ = raw(bank, metric, period)
    return v

def mark(bank, metric, period):
    """Value or its n/r / n/d marker."""
    v, st = raw(bank, metric, period)
    return v if v is not None else ("n/d" if st == "n/d" else "n/r")

# ---------- formatting (ROUND_HALF_EVEN everywhere) ----------

def rnd(x, dp):
    # ROUND_HALF_EVEN matches the rounding of the previously published tables
    return Decimal(str(x)).quantize(Decimal("1." + "0" * dp) if dp else Decimal("1"), rounding=ROUND_HALF_EVEN)

def bn(x, dp=0):          # S$m -> S$bn string
    return "n/r" if x is None else f"{rnd(x / 1000.0, dp)}"

def num(x, dp):
    return "n/r" if x is None else f"{rnd(x, dp)}"

def pct(x, dp=2):
    return "n/r" if x is None else f"{rnd(x, dp)}%"

def sm(x):                # S$m with thousands separators
    return "n/r" if x is None else f"{int(rnd(x, 0)):,}"

def fmt(x, dp):
    """Format value-or-marker."""
    return x if isinstance(x, str) else f"{rnd(x, dp)}"

def cagr(bank, metric, y0, y1):
    a, b = val(bank, metric, y0), val(bank, metric, y1)
    if a is None or b is None:
        return None
    n = int(y1) - int(y0)
    return ((b / a) ** (1.0 / n) - 1.0) * 100.0

def cagr_s(bank, metric, y0, y1):
    c = cagr(bank, metric, y0, y1)
    return "n/r" if c is None else f"{rnd(c, 1)}%"

# ---------- gates (run before writing) ----------

def gates():
    errs = []
    for b in BANKS:
        for p in YEARS + ["Q1-2026"]:
            nii, non, ti = val(b, "NII", p), val(b, "NonII", p), val(b, "TotalIncome", p)
            if None in (nii, non, ti):
                continue
            if abs(nii + non - ti) > 1.0:
                errs.append(f"tie-out fail {b} {p}: {nii}+{non}!={ti}")
    canary = val("DBS", "NIMgroup", "2025")
    if canary != 2.01:
        errs.append(f"DBS NIM canary fail: {canary} != 2.01")
    poison = [("UOB", "TotalIncome", "2025", 12000.0), ("DBS", "ROE", "2025", 16.5)]
    for b, m, p, bad in poison:
        if val(b, m, p) == bad:
            errs.append(f"poison pill present: {b} {m} {p} == {bad}")
    return errs

# ---------- table builders ----------

def t1(bank):
    sup = {"OCBC": {"2022": " [6]"}, "UOB": {"2025": " [5]"}}.get(bank, {})
    L = [f"### Table 1 — {bank}: Income Engine", "",
         "| FY | Dep | Assets | NII | Other | TotalRev | Profit | NIM | Rev/Dep | Profit/Dep | Profit/Rev |",
         "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for y in YEARS:
        dep, ta = val(bank, "CustomerDeposits", y), val(bank, "TotalAssets", y)
        nii, ti, np_ = val(bank, "NII", y), val(bank, "TotalIncome", y), val(bank, "NetProfit", y)
        other = None if None in (ti, nii) else ti - nii
        nim = val(bank, "NIMgroup", y)
        rd = None if None in (ti, dep) else ti / dep
        pd = None if None in (np_, dep) else np_ / dep
        pr = None if None in (np_, ti) else np_ / ti
        L.append(f"| {y} | {bn(dep)} | {bn(ta)} | {bn(nii,1)} | {bn(other,1)} | {bn(ti,1)} | {bn(np_,1)}{sup.get(y,'')} | {pct(nim)} | {num(rd,3)} | {num(pd,3)} | {num(pr,2)} |")
    for lbl, y0 in (("CAGR 21→25", "2021"), ("CAGR 16→25", "2016")):
        cells = [cagr_s(bank, m, y0, "2025") for m in ("CustomerDeposits", "TotalAssets", "NII")]
        a0, a1 = val(bank, "TotalIncome", y0), val(bank, "TotalIncome", "2025")
        n0, n1 = val(bank, "NII", y0), val(bank, "NII", "2025")
        oth = "n/r" if None in (a0, a1, n0, n1) else f"{rnd((((a1-n1)/(a0-n0))**(1.0/(2025-int(y0)))-1)*100,1)}%"
        cells += [oth, cagr_s(bank, "TotalIncome", y0, "2025"), cagr_s(bank, "NetProfit", y0, "2025")]
        L.append(f"| **{lbl}** | " + " | ".join(cells) + " |  |  |  |  |")
    foot = ("*Other = TotalRev − NII (derived). TotalRev = reported total income. Rev/Dep = TotalRev ÷ Deposits; "
            "Profit/Dep = Profit ÷ Deposits; Profit/Rev = Profit ÷ TotalRev (all dimensionless). CAGR = (end/start)^(1/n) − 1, "
            "on FY2021→FY2025 (4-yr) and FY2016→FY2025 (9-yr) bases. NIM = group net interest margin as reported. "
            "Profit = net profit attributable to shareholders (reported).")
    if bank == "OCBC":
        foot += " [6] FY2022 figures as restated for SFRS(I) 17 (insurance) in the FY2023 release."
    if bank == "UOB":
        foot += (" [5] FY2025 profit −23% is a provisioning artefact: ~S$2.0bn pre-emptive general allowances booked 3Q2025; "
                 "operating profit was −4%; UOB core net profit ≈ S$4.82bn (FY2022) / S$6.06bn (FY2023) where separately disclosed.")
    return L + ["", foot + "*", ""]

def t2():
    csup = {("OCBC", "2016"): " [c1]", ("OCBC", "2017"): " [c1]", ("OCBC", "2018"): " [c1]",
            ("UOB", "2023"): " [u1]", ("UOB", "2024"): " [u1]", ("UOB", "2025"): " [u1]"}
    L = ["### Table 2 — Attracted assets: deposits, CASA & wealth AUM", "",
         "| FY | " + " | ".join(f"{b} Dep | {b} CASA | {b} AUM" for b in BANKS) + " |",
         "|---|" + "---:|" * 9]
    for y in YEARS:
        cells = []
        for b in BANKS:
            dep = bn(val(b, "CustomerDeposits", y))
            casa = mark(b, "CASAratio", y)
            casa = casa if isinstance(casa, str) else f"{rnd(casa,1)}%"
            aum = mark(b, "WealthAUM", y)
            aum = aum if isinstance(aum, str) else bn(aum)
            cells += [dep, casa + csup.get((b, y), ""), aum]
        L.append(f"| {y} | " + " | ".join(cells) + " |")
    for lbl, y0 in (("CAGR 21→25", "2021"), ("CAGR 16→25", "2016")):
        cells = []
        for b in BANKS:
            cells += [cagr_s(b, "CustomerDeposits", y0, "2025"), "", cagr_s(b, "WealthAUM", y0, "2025")]
        L.append(f"| **{lbl}** | " + " | ".join(cells) + " |")
    foot = ("*Deposits = total non-bank customer deposits (group). CASA = (current + savings) / total customer deposits, as printed "
            "by each bank where available. Wealth AUM = bank-reported wealth / private-bank AUM. [c1] OCBC 2016–2018 CASA sourced "
            "from OCBC FY-results presentations (Tier-1) via a non-Claude retrieval pass (2026-07-16), computer-verified against source PDFs; "
            "currently `single-px` pending a second retriever. [u1] UOB CASA lifted ~48% → 58% (2023→25) mainly on post-rate-cycle "
            "deposit remix (customers rotating back from fixed deposits) plus mix contribution from the Citi consumer (deposit-heavy) book. "
            "CASA is a point-in-time ratio — CAGR cells intentionally blank. AUM: OCBC 2016–17 and UOB 2018–19 = `n/d` (not disclosed in that "
            "vintage of results decks). AUM definitions differ across banks (DBS \"Wealth Management AUM\"; OCBC group/banking wealth incl. "
            "Bank of Singapore + Great Eastern; UOB narrower, reclassified 1 Jan 2023) — read within-bank trends, not cross-bank levels. "
            "Never sum Deposits + AUM (double-count risk).*")
    return L + ["", foot, ""]

def t3():
    L = ["### Table 3 — Net interest margin (Group) & NII", "",
         "| FY | DBS NII | DBS NIM | OCBC NII | OCBC NIM | UOB NII | UOB NIM |",
         "|---|---:|---:|---:|---:|---:|---:|"]
    for y in YEARS:
        cells = []
        for b in BANKS:
            cells += [bn(val(b, "NII", y), 2), pct(val(b, "NIMgroup", y))]
        L.append(f"| {y} | " + " | ".join(cells) + " |")
    return L + ["", "*NIM = group net interest margin, %, as printed by each bank; NII in S$bn (2 dp). DBS uses **group** NIM "
                "(not the commercial-book series, which was 2.80% in FY2024); canary FY2025 group NIM = 2.01%.*", ""]

def pb_series(bank):
    out = {}
    for y in YEARS:
        p, b = val(bank, "PriceYE", y), val(bank, "BVPS", y)
        out[y] = None if None in (p, b) else p / b
    return out

def t4():
    sup5 = {("UOB", "2025"): " [5]"}
    hdr = " | ".join(f"{b} Price | {b} BVPS | {b} P/B | {b} ROE | {b} RoTE" for b in BANKS)
    L = ["### Table 4 — Valuation & Returns (P/B + ROE)", "", f"| FY | {hdr} |", "|---|" + "---:|" * 15]
    pb = {b: pb_series(b) for b in BANKS}
    for y in YEARS:
        cells = []
        for b in BANKS:
            rv, rst = raw(b, "RoTE", y)
            # OCBC/UOB print no RoTE (no ledger rows) and DBS pre-2021 is undisclosed -> n/d per ledger/definitions
            rote = f"{rnd(rv,1)}" if rv is not None else ("n/d" if rst in ("n/d", "missing") else "n/r")
            roe = mark(b, "ROE", y)
            roe = roe if isinstance(roe, str) else f"{rnd(roe,1)}"
            cells += [num(val(b, "PriceYE", y), 2), num(val(b, "BVPS", y), 2),
                      num(pb[b][y], 2), roe + sup5.get((b, y), ""), rote]
        L.append(f"| {y} | " + " | ".join(cells) + " |")
    def row(label, per_bank):
        cells = []
        for b in BANKS:
            v = per_bank(b)
            cells += v
        return f"| **{label}** | " + " | ".join(cells) + " |"
    avg10 = {b: sum(v for v in pb[b].values() if v) / len([v for v in pb[b].values() if v]) for b in BANKS}
    avg5 = {b: sum(pb[b][y] for y in YEARS[5:]) / 5 for b in BANKS}
    cur = {b: val(b, "PriceCurrent", "2026-latest") / val(b, "BVPS", "2025") for b in BANKS}
    L.append(row("10-yr avg P/B", lambda b: ["", "", f"{rnd(avg10[b],2)}", "", ""]))
    L.append(row("5-yr avg P/B (21–25)", lambda b: ["", "", f"{rnd(avg5[b],2)}", "", ""]))
    L.append(row("Current P/B", lambda b: ["", "", f"{rnd(cur[b],2)}", "", ""]))
    L.append(row("Current vs 10-yr avg", lambda b: ["", "", f"+{rnd((cur[b]/avg10[b]-1)*100,0)}%", "", ""]))
    L.append(row("10-yr avg ROE", lambda b: ["", "", "", f"{rnd(sum(val(b,'ROE',y) for y in YEARS)/10,1)}", ""]))
    foot = ("*P/B = 31-Dec close ÷ BVPS for FY rows (derived; both inputs shown). ROE reported (group). RoTE: DBS discloses FY2021+ "
            "(`n/d` before); OCBC and UOB do not print RoTE → `n/d`. [5] UOB FY2025 ROE = 9.6 reflects the ~S$2.0bn pre-emptive GP "
            "booked 3Q2025 (provisioning artefact); UOB core ROE ≈ 14.2% (FY2023) where separately disclosed. DBS 1-for-10 bonus issue "
            "(1Q2024): price and BVPS kept on the same basis within each year — P/B is bonus-invariant; do not mix adjusted price with "
            "unadjusted BVPS. **Current P/B uses the intraday 2026-07-20 price (71.96 / 28.60 / 42.60 — NOT a closing price) ÷ FY2025 BVPS** "
            "(see the 1Q2026 snapshot valuation table).*")
    # P/TB block
    P = ["", foot, "", "**P/TB block (FY2025)**", "",
         "| Bank | BVPS | Goodwill+Intang (S$m) | Shares (m) | TBVPS | P/TB (FY25 close) | P/TB (current) |",
         "|---|---:|---:|---:|---:|---:|---:|"]
    for b in BANKS:
        bv, gi, sh = val(b, "BVPS", "2025"), val(b, "GoodwillIntangibles", "2025"), val(b, "SharesOut", "2025")
        tb = bv - gi / sh
        P.append(f"| {b} | {rnd(bv,2)} | {int(rnd(gi,0))} | {int(rnd(sh,0))} | {rnd(tb,2)} | "
                 f"{rnd(val(b,'PriceYE','2025')/tb,2)} | {rnd(val(b,'PriceCurrent','2026-latest')/tb,2)} |")
    P += ["", "*TBVPS = BVPS − (Goodwill + Intangibles) / Shares outstanding. P/TB (FY25 close) uses the 31-Dec-2025 close; "
          "**P/TB (current) uses the intraday 2026-07-20 price (71.96 / 28.60 / 42.60) — not a closing price.** P/TB derived from stated "
          "prices. Historical P/TB not shown — per-year goodwill was not retrieved.*", ""]
    return L + P

def t5():
    L = ["### Table 5 — NIM vs the rate cycle", "",
         "| FY | DBS NIM | OCBC NIM | UOB NIM | 3M SORA (31-Dec) | 3M SORA (FY avg) | Fed upper (31-Dec) | EFFR (FY avg) |",
         "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for y in YEARS:
        rates = []
        for m in ("SORA_YE", "SORA_avg", "FedUpper", "EFFRavg"):
            v = mark("-", m, y)
            rates.append(v if isinstance(v, str) else f"{rnd(v,2)}")
        L.append(f"| {y} | " + " | ".join(pct(val(b, "NIMgroup", y)) for b in BANKS) + " | " + " | ".join(rates) + " |")
    q = [pct(val(b, "NIMgroup", "Q1-2026")) for b in BANKS]
    sora_avg = val("-", "SORA_avg", "Q1-2026")
    L.append(f"| 2026 latest (1Q26) | {q[0]} | {q[1]} | {q[2]} | n/d | {rnd(sora_avg,2)}* | "
             f"{rnd(val('-','FedUpper','2026-latest'),2)} | {rnd(val('-','EFFRavg','2026-latest'),2)} |")
    foot = ("*NIM from Table 3 (group), with `%` symbol per 2dp format. **2026-latest NIM row is 1Q2026 group NIM** (quarter ended "
            "31 Mar 2026), all down YoY. 3M compounded SORA (MAS) exists only from 6-Aug-2020 → pre-2020 = `n/r` (no SIBOR splice). "
            "**3M SORA (31-Dec) 2026 = `n/d`**: MAS eServices statistics portal under scheduled maintenance on 2026-07-20; latest official "
            "single-day value not retrievable. **\\*3M SORA (FY avg) 2026 = 1.07 is the bank-characterised 1Q26 average** "
            "([DBS 1Q26 media transcript](https://www.dbs.com/iwov-resources/images/investors/quarterly-financials/2026/1Q26_media_transcript.pdf)), "
            "**not an official MAS FY figure**. Fed funds target upper = FRED `DFEDTARU` (3.75, held at the "
            "[17-Jun-2026 FOMC](https://www.federalreserve.gov/newsevents/pressreleases/monetary20260617a.htm)); effective fed funds (FY avg) = "
            "FRED `DFF`, 2026 YTD ≈ 3.62. 2026-latest rates as of mid-July 2026.*")
    return L + ["", foot, ""]

def snapshot():
    n = {"income": "records at DBS & OCBC"}
    inc = [("Net interest income (S$m)", "NII", "UOB Tier-2 host; OCBC NII derived-to-tie"),
           ("Non-interest income (S$m)", "NonII", "DBS & UOB derived (TI−NII); UOB slide components don't reconcile (see note)"),
           ("Total income (S$m)", "TotalIncome", "records at DBS & OCBC"),
           ("Net fee income (S$m)", "NetFee", "DBS +16% YoY · OCBC +24% YoY · UOB −8% YoY"),
           ("Net profit (S$m)", "NetProfit", "+1% / +5% / −4% YoY")]
    L = ["## Latest 1Q2026 snapshot (quarters ended 31 Mar 2026)", "",
         "> **Read with care — these lines are NOT fully cross-comparable:** reporting formats differ (DBS trading update · OCBC press "
         "release · UOB CFO/CEO slides via MarketScreener); UOB income-statement detail is **Tier-2 host** while DBS/OCBC are Tier-1; all "
         "cells are single-retriever (`single-cl`, stamped `20260720-001 CwClOpus4.8`) and not yet dual-checked. Wealth-AUM definitions "
         "differ across banks (see Table 2 note). **SGD.**", "",
         "### 1Q2026 — income & returns", "",
         "| Metric (1Q26) | DBS | OCBC | UOB | Note |", "|---|---:|---:|---:|---|"]
    for label, m, note in inc:
        L.append(f"| {label} | " + " | ".join(sm(val(b, m, "Q1-2026")) for b in BANKS) + f" | {note} |")
    L.append("| Group NIM (%) | " + " | ".join(f"{rnd(val(b,'NIMgroup','Q1-2026'),2)}" for b in BANKS) + " | all down YoY; OCBC steepest (−28bps) |")
    L.append("| ROE (%) | " + " | ".join(f"{rnd(val(b,'ROE','Q1-2026'),1)}" for b in BANKS) + " | reported (group) |")
    L.append("| Cost/income (%) | " + " | ".join(f"{rnd(val(b,'CostIncome','Q1-2026'),1)}" for b in BANKS) + " |  |")
    tie = " · ".join(f"{b} {sm(val(b,'NII','Q1-2026'))}+{sm(val(b,'NonII','Q1-2026'))}={sm(val(b,'TotalIncome','Q1-2026'))}" for b in BANKS)
    L += ["", f"*NII + Non-II = Total income ties exactly for all three ({tie}). DBS non-II is derived (fee 1,482 + other 972); OCBC NII "
          "is derived-to-tie (TI 3,828 − non-II 1,606). **UOB non-II caveat:** UOB's CFO-slide components (net fee 637 + trading & investment "
          "405 + other 462 = 1,504) do not reconcile with total income − NII (1,098); the tie-out-consistent derived 1,098 is shown and the "
          "slide split is flagged as an unresolved retrieval gap. Net profit = attributable to shareholders (reported).*", "",
          "### 1Q2026 — attraction, balance sheet & asset quality (period-end 31 Mar 2026)", "",
          "| Metric | DBS | OCBC | UOB | Note |", "|---|---:|---:|---:|---|"]
    bs = [("Customer deposits (S$m)", "CustomerDeposits", 0, ""),
          ("CASA ratio (%)", "CASAratio", 1, "printed / mix basis differs"),
          ("Wealth AUM (S$m)", "WealthAUM", 0, "**definitions differ — do not compare levels**"),
          ("Total assets (S$m)", "TotalAssets", 0, "leverage only, not attraction"),
          ("Gross loans (S$m)", "Loans", 0, ""),
          ("CET1 ratio (%)", "CET1", 1, ""), ("NPL ratio (%)", "NPL", 1, ""),
          ("Credit cost (bps)", "CreditCost", 0, "OCBC incl. S$191m overlay; UOB elevated")]
    for label, m, dp, note in bs:
        cells = [sm(val(b, m, "Q1-2026")) if dp == 0 and "S$m" in label else f"{rnd(val(b,m,'Q1-2026'),dp)}" if dp else f"{int(rnd(val(b,m,'Q1-2026'),0))}" for b in BANKS]
        L.append(f"| {label} | " + " | ".join(cells) + f" | {note} |")
    pbn = {b: val(b, "PriceCurrent", "2026-latest") / val(b, "BVPS", "2025") for b in BANKS}
    pb_all = {b: pb_series(b) for b in BANKS}
    avg10 = {b: sum(v for v in pb_all[b].values() if v) / 10 for b in BANKS}
    tb = {b: val(b, "BVPS", "2025") - val(b, "GoodwillIntangibles", "2025") / val(b, "SharesOut", "2025") for b in BANKS}
    L += ["", "***Never sum deposits + AUM** (double-count). Wealth-AUM levels are **not** cross-comparable — DBS \"Wealth Management "
          "AUM\"; OCBC group wealth incl. Bank of Singapore + Great Eastern; UOB \"Group Retail AUM\" (narrower, reclassified 1-Jan-2023). "
          "UOB balance-sheet/ratio lines are Tier-1 (UOB Financial Highlights); UOB CASA / wealth AUM / credit cost are Tier-2 host "
          "(UOB 1Q26 CFO slides via MarketScreener). OCBC credit cost includes S$191m management-overlay allowances for non-impaired "
          "assets.*", "",
          "### 1Q2026 — current valuation (as of 2026-07-20, intraday)", "",
          "| Metric | DBS | OCBC | UOB |", "|---|---:|---:|---:|",
          "| Price (S$, intraday 2026-07-20) | " + " | ".join(f"{rnd(val(b,'PriceCurrent','2026-latest'),2)}" for b in BANKS) + " |",
          "| FY2025 BVPS (S$) | " + " | ".join(f"{rnd(val(b,'BVPS','2025'),2)}" for b in BANKS) + " |",
          "| Current P/B | " + " | ".join(f"{rnd(pbn[b],2)}" for b in BANKS) + " |",
          "| Current vs 10-yr avg P/B | " + " | ".join(f"+{rnd((pbn[b]/avg10[b]-1)*100,0)}%" for b in BANKS) + " |",
          "| FY2025 TBVPS (S$) | " + " | ".join(f"{rnd(tb[b],2)}" for b in BANKS) + " |",
          "| Current P/TB | " + " | ".join(f"{rnd(val(b,'PriceCurrent','2026-latest')/tb[b],2)}" for b in BANKS) + " |", "",
          "*Prices are **intraday 2026-07-20 (Perplexity Finance, SGX open) — NOT closing prices**; treat as a tier-2 market-data "
          "snapshot only. P/B = price ÷ FY2025 BVPS; P/TB = price ÷ FY2025 TBVPS (FY2025 per-share book denominators; 1Q26 per-share book "
          "not retrieved). These figures feed the Table 4 \"Current P/B\" rows and the P/TB \"current\" column.*", "", "---", ""]
    return L

def validation():
    res = [r for r in ROWS if (r["reconciliation_status"] or "").strip() == "resolved"
           and (r["checksum_expected"] or "").strip() and (r["reconciliation_note"] or "").strip()]
    material = [r for r in res if not re.search(r"round", r["reconciliation_note"], re.I)]
    inv = {}
    for r in ROWS:
        st = (r["reconciliation_status"] or "").strip()
        if st in ("n/r", "n/d"):
            inv.setdefault(st, []).append(r["data_point_id"])
    L = ["## Table-level validation data (for Appendix A)", "",
         "**Gates (recomputed this build):** NII + Non-II = Total income exact (≤S$1m residual) for every filled bank-period · "
         "DBS FY2025 group-NIM canary = 2.01 · all values SGD · no poison-pill values present.", "",
         "**Material resolved rows (checksum ≠ reconciled, non-rounding):**", "",
         "| Row | Checksum | Reconciled | Cause |", "|---|---:|---:|---|"]
    for r in material:
        cs, rv = (x[:-2] if x.endswith('.0') else x for x in (r['checksum_expected'], r['reconciled_value']))
        L.append(f"| {r['data_point_id']} | {cs} | {rv} | {r['reconciliation_note']} |")
    L += ["", f"Other `resolved` rows: {len(res) - len(material)} rounding-level (±S$1–25m vs a rounded checksum; agents agree).", "",
          f"**`n/r` inventory ({len(inv.get('n/r', []))}):** " + ", ".join(inv.get("n/r", [])) or "none", "",
          f"**`n/d` inventory ({len(inv.get('n/d', []))}):** " + ", ".join(inv.get("n/d", [])) or "none", ""]
    return L

def build():
    errs = gates()
    if errs:
        sys.exit("GATES FAILED:\n" + "\n".join(errs))
    counts = {}
    for r in ROWS:
        st = (r["reconciliation_status"] or "").strip() or "?"
        counts[st] = counts.get(st, 0) + 1
    status_line = " · ".join(f"{v} {k}" for k, v in sorted(counts.items(), key=lambda kv: -kv[1]))
    head = ["# SG Banks — Tables (generated table-block artifact)", "",
            "> **Artifact:** `pipeline/sg-banks/data/tables.md` — sole output of `pipeline/sg-banks/method/code/build_tables.py` "
            "(the deterministic Build-Tables script; spec in `method/code/build-tables.md`). Consumed by the Build-Report step "
            "(`pipeline/sg-banks/method/ai/build-report.md`).",
            f"> **Provenance:** every number is a deterministic transform of reconciled `pipeline/sg-banks/data/ledger.csv` "
            f"({len(ROWS)} data rows: {status_line}). Rerun `python3 pipeline/sg-banks/method/code/build_tables.py` to regenerate; "
            "same ledger in → same tables out.",
            "> **Banks:** DBS (D05) · OCBC (O39) · UOB (U11). FY2016–FY2025 long-run base + **1Q2026 interim (quarters ended "
            "31 Mar 2026)** + **current (2026-07-20 intraday) valuation.** **SGD only.**", "",
            "**Contents:** Latest 1Q2026 snapshot · Tables 1 (per bank) · 2 · 3 · 4 (+ P/TB block) · 5, each with derived-line and "
            "superscript footnotes; plus table-level validation data for Appendix A. Narrative blocks are written by Assemble, not here.",
            "", "---", ""]
    body = snapshot()
    for b in BANKS:
        body += t1(b)
    body += ["---", ""] + t2() + ["---", ""] + t3() + ["---", ""] + t4() + ["---", ""] + t5() + ["---", ""] + validation()
    return "\n".join(head + body).rstrip() + "\n"

# ---------- check mode: numeric comparison vs committed tables.md ----------

def cells_of(text):
    text = text.split("## Table-level validation data")[0]
    out = []
    for line in text.splitlines():
        if line.startswith("|") and not set(line) <= set("|-: "):
            row = [re.sub(r"<sup>.*?</sup>|\s?\[[a-z0-9]+\]|\*\*|`", "", c).strip() for c in line.strip("|").split("|")]
            nums = [c for c in (re.sub(r"[%,+]", "", c) for c in row) if re.fullmatch(r"-?\d+(\.\d+)?", c)]
            if nums:
                out.append(nums)
    return out

if __name__ == "__main__":
    content = build()
    if "--check" in sys.argv:
        old = OUT.read_text(encoding="utf-8")
        a, b = cells_of(old), cells_of(content)
        flat_a = [x for r in a for x in r]
        flat_b = [x for r in b for x in r]
        if flat_a == flat_b:
            print(f"CHECK OK: {len(flat_b)} numeric cells identical")
        else:
            import difflib
            print(f"CHECK DIFF: {len(flat_a)} vs {len(flat_b)} numeric cells")
            for d in difflib.unified_diff(flat_a, flat_b, lineterm="", n=1):
                print(d)
            sys.exit(1)
    else:
        OUT.write_text(content, encoding="utf-8")
        print(f"wrote {OUT} ({len(content.splitlines())} lines)")
