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
        "NII": lv(bank, "NII", "2025"),
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

def peer_meta():
    """Per-bank text columns from data/peers.csv: top Other-Revenue text,
    market-cap as-of date, unit, and (when fetched) dated share price."""
    if not PEERS.exists():
        return {}
    out = {}
    for r in csv.DictReader(open(PEERS, newline="", encoding="utf-8")):
        m = out.setdefault(r["bank"], {})
        if r["metric"] == "TopOtherRevenue":
            m["top_or"] = r["value"].replace("; ", " · ")
        elif r["metric"] == "MarketCap":
            m["mcap_asof"] = r["period"]
        elif r["metric"] == "SharePrice":
            m["px"] = r["value"]
            m["px_asof"] = r["period"]
            m["px_unit"] = r["unit"].replace("/share", "")
        elif r["metric"] == "NII":
            m["ccy"] = r["unit"].split()[0]
        elif r["metric"] == "NIM":
            m["nim"] = r["value"]
    return out

def sg_price(bank):
    """SG per-share price + as-of date from the ledger's PriceCurrent row."""
    import re
    for r in csv.DictReader(open(LEDGER, newline="", encoding="utf-8")):
        if r["bank"] == bank and r["metric"] == "PriceCurrent" and r["period"] == "2026-latest":
            try:
                px = float(r["reconciled_value"])
            except ValueError:
                return None
            m = re.search(r"(\d{4}-\d{2}-\d{2})", r["cl_comment"] + " " + r["cl_source"])
            return (px, m.group(1) if m else "2026-latest")
    return None

def px_cell(bank, meta):
    """Price column: local per-share price with as-of date (the staleness
    marker). Peers without a fetched SharePrice show n/r plus the
    market-cap as-of date, so the row's staleness is still visible."""
    if bank in SG:
        p = sg_price(bank)
        return f"S${p[0]:.2f} ({p[1]})" if p else "n/r"
    m = meta.get(bank, {})
    if "px" in m:
        unit = CCY.get(m.get("px_unit", ""), m.get("px_unit", ""))
        return f"{unit} {m['px']} ({m.get('px_asof', '?')})".strip()
    return f"n/r (mcap {m['mcap_asof']})" if "mcap_asof" in m else "n/r"

def ratios(f):
    dep, aum = f.get("CustomerDeposits"), f.get("WealthAUM")
    rev, prof = f.get("TotalRevenue"), f.get("NetProfit")
    book, mcap = f.get("BookEquity"), f.get("MarketCap")
    nii = f.get("NII")
    orv = rev - nii if None not in (rev, nii) else None   # Other Revenue = TotalRevenue − NII
    cap = dep + aum if dep is not None and aum is not None else None
    def d(a, b):
        return a / b if a is not None and b not in (None, 0) else None
    return {
        "NII": nii, "OR": orv,
        "NII_vDep": d(nii, dep),
        "OR_vDep": d(orv, dep),
        "OR_vCA": d(orv, cap),
        "total_vCA": d(rev, cap),
        "Monetization_vDeposits": d(rev, dep),
        "P/CA": d(mcap, cap),
        "P/Rev": d(mcap, rev),
        "P/E": d(mcap, prof),
        "P/B": d(mcap, book),
    }

CCY = {"SGD": "S$", "USD": "US$", "CNY": "RMB", "CAD": "C$", "GBP": "£", "CHF": "CHF"}

def lc_bn(val, ccy_code):
    """Level in local-currency billions, e.g. 'S$14.5' (bn implied by header)."""
    if val is None:
        return "n/r"
    return f"{CCY.get(ccy_code, ccy_code)}{val / 1000:.1f}"

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
        meta = peer_meta()
        order = SG + [p for p in peers if p not in SG]
        e += [f"Levels in each bank's local reporting currency (bn, never FX-converted); the four ratio columns are within-bank, "
              f"indexed to {INDEX_BANK} = 100, so currencies cancel. OR = Other Revenue = total revenue − NII.", "",
              "| Bank | NII (lc bn) | OR (lc bn) | NII_vDep | OR_vDep | OR_vCA | total_vCA | Top Other-Revenue (% of total revenue) |",
              "|---|---:|---:|---:|---:|---:|---:|---|"]
        for b in order:
            r = banks.get(b) or peers.get(b)
            ccy = "SGD" if b in SG else meta.get(b, {}).get("ccy", "")
            idx = lambda k: ("n/r" if None in (r[k], base[k]) or base[k] == 0
                             else f"{r[k] / base[k] * 100:.0f}")
            e.append(f"| {b} | {lc_bn(r['NII'], ccy)} | {lc_bn(r['OR'], ccy)} | {idx('NII_vDep')} | {idx('OR_vDep')} | "
                     f"{idx('OR_vCA')} | {idx('total_vCA')} | {meta.get(b, {}).get('top_or', 'n/d')} |")
        nims = " · ".join(f"{b} {meta.get(b, {}).get('nim', 'n/d')}" for b in order)
        e += ["", f"*As-stated NIM (context only — denominator conventions differ per bank, not comparable as an index): {nims}.*"]
        up = []
        b0 = base["OR_vDep"]
        for b in SG:
            r = banks[b]
            if None in (r["OR_vDep"], b0) or r["OR_vDep"] >= b0:
                continue
            dep = sg_fundamentals(b)["CustomerDeposits"]
            rev = sg_fundamentals(b)["TotalRevenue"]
            add = (b0 - r["OR_vDep"]) * dep
            up.append(f"{b} +S${add / 1000:.1f}bn (+{add / rev * 100:.0f}% of revenue)")
        if up:
            e += ["", "*Implied SG Other-Revenue uplift at index-bank parity (OR_vDep gap × deposits — under the thesis, "
                  "under-monetization of an already-attracted base is optionality): " + " · ".join(up) + ".*"]
    else:
        e += ["**Peer index pending** — `data/peers.csv` not yet fetched (module `ai/fetch-peers.md` is written; run is cost-gated). "
              "SG-only raw values meanwhile:", "",
              "| Bank | NII_vDep | OR_vDep | total_vCA |", "|---|---:|---:|---:|"]
        for b in SG:
            e.append(f"| {b} | {pct(banks[b]['NII_vDep'])} | {pct(banks[b]['OR_vDep'])} | {pct(banks[b]['total_vCA'])} |")
    e += ["", "*NII_vDep = NII ÷ customer deposits · OR_vDep = OR ÷ customer deposits · OR_vCA = OR ÷ client assets · "
          "total_vCA = total revenue ÷ client assets (CA = customer deposits + wealth AUM) — AUM definitions differ per bank; read the vDep and vCA lenses together.*", ""]
    # Q6 — valuation
    e += ["## Relative valuation (Frame Q6)", ""]
    if have_peers:
        base = peers[INDEX_BANK]
        meta = peer_meta()
        e += [f"Four indexes vs {INDEX_BANK} = 100; req %/yr = required outperformance, (premium ratio)^(1/5) − 1 per year (5-yr convergence). "
              "Px = local per-share price with its as-of date — the staleness marker. P/CA = price ÷ client assets.", "",
              "| Bank | Px (as-of) | P/CA | req %/yr | P/Rev | req %/yr | P/E | req %/yr | P/B | req %/yr |",
              "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for b in SG + [p for p in peers if p not in SG]:
            r = banks.get(b) or peers.get(b)
            cells = []
            for k in ("P/CA", "P/Rev", "P/E", "P/B"):
                v, bv = r[k], base[k]
                if None in (v, bv) or bv == 0:
                    cells += ["n/r", ""]
                else:
                    idx = v / bv * 100
                    req = ((idx / 100) ** 0.2 - 1) * 100
                    cells += [f"{idx:.0f}", f"{req:+.1f}%"]
            e.append(f"| {b} | {px_cell(b, meta)} | " + " | ".join(cells) + " |")
    else:
        e += ["**Pending** — needs `data/peers.csv` (module `ai/fetch-peers.md` is written; run is cost-gated). "
              "SG-only raw multiples meanwhile (market cap at the ledger's dated current price):", "",
              "| Bank | P/CapitalBase | P/Rev | P/E | P/B |", "|---|---:|---:|---:|---:|"]
        for b in SG:
            r = banks[b]
            e.append(f"| {b} | " + " | ".join(
                "n/r" if r[k] is None else f"{r[k]:.2f}" for k in ("P/CapitalBase", "P/Rev", "P/E", "P/B")) + " |")
    e += ["", "*P/CA = market cap ÷ client assets (customer deposits + wealth AUM) · P/Rev = market cap ÷ total revenue · P/E = market cap ÷ net profit · "
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
