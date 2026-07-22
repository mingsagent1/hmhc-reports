#!/usr/bin/env python3
"""Build-Benchmarks — deterministic peer benchmarking for sg-banks (Frame Q5/Q6).

Reads the reconciled ledger (SG banks) plus, when present, data/peers.csv
(Fetch-Peers output) and data/flows.csv (Fetch-Flows output), and generates
data/benchmarks.md: monetization indices, four valuation indexes vs the
index bank = 100, required 5-yr outperformance, and the wealth-hub flows
table. Until the fetch outputs exist it emits an SG-only preview and marks
the indexed sections pending. Same inputs in -> same output out.

Usage:  python3 pipeline/sg-banks/method/code/build_benchmarks.py [--check]
Spec:   pipeline/sg-banks/method/code/build-benchmarks.md
"""
import csv, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "data" / "ledger.csv"
PEERS = ROOT / "data" / "peers.csv"
FLOWS = ROOT / "data" / "flows.csv"
OUT = ROOT / "data" / "benchmarks.md"
INDEX_BANK = "HSBC"
SG = ["DBS", "OCBC", "UOB"]

L = {(r["bank"], r["metric"], r["period"]): (r["reconciled_value"] or "").strip()
     for r in csv.DictReader(open(LEDGER, newline="", encoding="utf-8"))}

def lv(bank, metric, period):
    try:
        return float(L[(bank, metric, period)])
    except (KeyError, ValueError):
        return None

def sg_fundamentals(bank):
    """SG-bank fundamentals from the ledger (FY2025 + current price)."""
    shares = lv(bank, "SharesOut", "2025")
    return {
        "CustomerDeposits": lv(bank, "CustomerDeposits", "2025"),
        "WealthAUM": lv(bank, "WealthAUM", "2025"),
        "TotalRevenue": lv(bank, "TotalIncome", "2025"),
        "NetProfit": lv(bank, "NetProfit", "2025"),
        "BookEquity": (lv(bank, "BVPS", "2025") or 0) * (shares or 0) or None,
        "MarketCap": (lv(bank, "PriceCurrent", "2026-latest") or 0) * (shares or 0) or None,
    }

def peer_fundamentals():
    """Peer fundamentals from data/peers.csv, if present."""
    if not PEERS.exists():
        return {}
    out = {}
    for r in csv.DictReader(open(PEERS, newline="", encoding="utf-8")):
        try:
            out.setdefault(r["bank"], {})[r["metric"]] = float(r["value"])
        except (KeyError, ValueError):
            continue
    return out

def ratios(f):
    dep, aum = f.get("CustomerDeposits"), f.get("WealthAUM")
    rev, prof = f.get("TotalRevenue"), f.get("NetProfit")
    book, mcap = f.get("BookEquity"), f.get("MarketCap")
    cap = dep + aum if dep is not None and aum is not None else None
    def d(a, b):
        return a / b if a is not None and b not in (None, 0) else None
    return {
        "Monetization_vDeposits": d(rev, dep),
        "Monetization_vCapitalBase": d(rev, cap),
        "P/CapitalBase": d(mcap, cap),
        "P/Rev": d(mcap, rev),
        "P/E": d(mcap, prof),
        "P/B": d(mcap, book),
    }

def pct(x, dp=2):
    return "n/r" if x is None else f"{x * 100:.{dp}f}%"

def build():
    banks = {b: ratios(sg_fundamentals(b)) for b in SG}
    peers = {b: ratios(f) for b, f in peer_fundamentals().items()}
    have_peers = INDEX_BANK in peers
    e = ["# SG Banks — Benchmarks (generated artifact)", "",
         "*Artifact: `pipeline/sg-banks/data/benchmarks.md` — sole output of `pipeline/sg-banks/method/code/build_benchmarks.py`. "
         "Inputs: reconciled `data/ledger.csv` (SG banks)" +
         (", `data/peers.csv`" if PEERS.exists() else "") + (", `data/flows.csv`" if FLOWS.exists() else "") +
         ". Rerun the script to regenerate; same inputs in, same output out.*", ""]
    # Q5 — monetization
    e += ["## Monetization (Frame Q5)", ""]
    if have_peers:
        base = peers[INDEX_BANK]
        e += [f"Indexed to {INDEX_BANK} = 100 (latest FY per bank; ratios are within-bank, so currencies cancel).", "",
              "| Bank | Monetization_vDeposits (index) | Monetization_vCapitalBase (index) |", "|---|---:|---:|"]
        for b in SG + [p for p in peers if p not in SG]:
            r = banks.get(b) or peers.get(b)
            m1 = r["Monetization_vDeposits"]; m2 = r["Monetization_vCapitalBase"]
            i1 = "n/r" if None in (m1, base["Monetization_vDeposits"]) else f"{m1 / base['Monetization_vDeposits'] * 100:.0f}"
            i2 = "n/r" if None in (m2, base["Monetization_vCapitalBase"]) else f"{m2 / base['Monetization_vCapitalBase'] * 100:.0f}"
            e.append(f"| {b} | {i1} | {i2} |")
    else:
        e += ["**Peer index pending** — `data/peers.csv` not yet fetched (module `ai/fetch-peers.md` is written; run is cost-gated). "
              "SG-only raw values meanwhile:", "",
              "| Bank | Monetization_vDeposits | Monetization_vCapitalBase |", "|---|---:|---:|"]
        for b in SG:
            e.append(f"| {b} | {pct(banks[b]['Monetization_vDeposits'])} | {pct(banks[b]['Monetization_vCapitalBase'])} |")
    e += ["", "*Monetization_vDeposits = total revenue ÷ customer deposits. Monetization_vCapitalBase = total revenue ÷ (customer deposits + wealth AUM) — "
          "AUM definitions differ per bank; read the two indices together.*", ""]
    # Q6 — valuation
    e += ["## Relative valuation (Frame Q6)", ""]
    if have_peers:
        base = peers[INDEX_BANK]
        e += [f"Four indexes vs {INDEX_BANK} = 100; required outperformance = (premium ratio)^(1/5) − 1 per year (5-yr convergence).", "",
              "| Bank | P/CapitalBase | req %/yr | P/Rev | req %/yr | P/E | req %/yr | P/B | req %/yr |",
              "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for b in SG + [p for p in peers if p not in SG]:
            r = banks.get(b) or peers.get(b)
            cells = []
            for k in ("P/CapitalBase", "P/Rev", "P/E", "P/B"):
                v, bv = r[k], base[k]
                if None in (v, bv) or bv == 0:
                    cells += ["n/r", ""]
                else:
                    idx = v / bv * 100
                    req = ((idx / 100) ** 0.2 - 1) * 100
                    cells += [f"{idx:.0f}", f"{req:+.1f}%"]
            e.append(f"| {b} | " + " | ".join(cells) + " |")
    else:
        e += ["**Pending** — needs `data/peers.csv` (module `ai/fetch-peers.md` is written; run is cost-gated). "
              "SG-only raw multiples meanwhile (market cap at the ledger's dated current price):", "",
              "| Bank | P/CapitalBase | P/Rev | P/E | P/B |", "|---|---:|---:|---:|---:|"]
        for b in SG:
            r = banks[b]
            e.append(f"| {b} | " + " | ".join(
                "n/r" if r[k] is None else f"{r[k]:.2f}" for k in ("P/CapitalBase", "P/Rev", "P/E", "P/B")) + " |")
    e += ["", "*P/CapitalBase = market cap ÷ (deposits + AUM) · P/Rev = market cap ÷ total revenue · P/E = market cap ÷ net profit · "
          "P/B = market cap ÷ book equity. SG market cap = current dated price × FY25 shares outstanding, from the ledger.*", ""]
    # Q2 — flows
    e += ["## Wealth-hub capital flows (Frame Q2)", ""]
    if FLOWS.exists():
        rows = list(csv.DictReader(open(FLOWS, newline="", encoding="utf-8")))
        hubs = {}
        for r in rows:
            if r.get("measure") == "CrossBorderWealth":
                try:
                    hubs.setdefault(r["hub"], {})[r["year"]] = float(r["value"])
                except ValueError:
                    continue
        e += ["| WealthHub | US$tn | 5y-CAGR | FY25 % | FY24 % | FY23 % | FY22 % |", "|---|---:|---:|---:|---:|---:|---:|"]
        for hub, ys in sorted(hubs.items()):
            def g(y):
                a, b = ys.get(str(y)), ys.get(str(y - 1))
                return "n/r" if None in (a, b) else f"{(a / b - 1) * 100:+.1f}"
            lvl = ys.get("2025")
            c5 = ("n/r" if None in (ys.get("2025"), ys.get("2020")) or not ys.get("2020")
                  else f"{((ys['2025'] / ys['2020']) ** 0.2 - 1) * 100:.1f}%")
            e.append(f"| {hub} | {'n/r' if lvl is None else f'{lvl:.1f}'} | {c5} | {g(2025)} | {g(2024)} | {g(2023)} | {g(2022)} |")
    else:
        e += ["**Pending** — `data/flows.csv` not yet fetched (module `ai/fetch-flows.md` is written; run is cost-gated)."]
    e += [""]
    return "\n".join(e).rstrip() + "\n"

if __name__ == "__main__":
    content = build()
    if "--check" in sys.argv:
        if OUT.exists() and OUT.read_text(encoding="utf-8") == content:
            print("CHECK OK: benchmarks.md reproducible from inputs")
        elif not OUT.exists():
            sys.exit("CHECK FAIL: data/benchmarks.md missing — run build_benchmarks.py")
        else:
            sys.exit("CHECK FAIL: committed benchmarks.md differs from generated output")
    else:
        OUT.write_text(content, encoding="utf-8")
        print(f"wrote {OUT}")
