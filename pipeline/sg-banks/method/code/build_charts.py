#!/usr/bin/env python3
"""Build-Charts — deterministic chart generation for sg-banks.

Reads the reconciled ledger (data/ledger.csv) and generates hand-written
SVG charts into reports/sg-banks/assets/. Same ledger in -> same SVG out.
No AI, no plotting libraries, no timestamps.

Charts:
  nim-vs-sora.svg — group NIM per bank vs 3M SORA (FY avg) and effective
                    Fed funds (FY avg), FY2016-2025 + 2026 latest.

Usage:  python3 pipeline/sg-banks/method/code/build_charts.py [--check]
        --check: regenerate to memory and compare byte-for-byte against
                 the committed SVG; exit non-zero on any difference.

Spec: pipeline/sg-banks/method/code/build-charts.md.
"""
import csv, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]              # pipeline/sg-banks
LEDGER = ROOT / "data" / "ledger.csv"
ASSETS = ROOT.parents[1] / "reports" / "sg-banks" / "assets"

T = {(r["bank"], r["metric"], r["period"]): (r["reconciled_value"] or "").strip()
     for r in csv.DictReader(open(LEDGER, newline="", encoding="utf-8"))}

def val(bank, metric, period):
    v = T.get((bank, metric, period), "")
    try:
        return float(v)
    except ValueError:
        return None

YEARS = [str(y) for y in range(2016, 2026)]
X_LABELS = ["FY16", "FY17", "FY18", "FY19", "FY20", "FY21", "FY22", "FY23", "FY24", "FY25", "2026*"]

def series(bank, metric, periods):
    return [val(bank, metric, p) for p in periods]

SERIES = [
    # (label, color, dash, values over FY2016..FY2025 + 2026-latest)
    ("DBS NIM",  "#d62728", None,  series("DBS",  "NIMgroup", YEARS) + [val("DBS",  "NIMgroup", "Q1-2026")]),
    ("OCBC NIM", "#ff7f0e", None,  series("OCBC", "NIMgroup", YEARS) + [val("OCBC", "NIMgroup", "Q1-2026")]),
    ("UOB NIM",  "#1f77b4", None,  series("UOB",  "NIMgroup", YEARS) + [val("UOB",  "NIMgroup", "Q1-2026")]),
    ("3M SORA (FY avg)", "#7f7f7f", "6,4", series("-", "SORA_avg", YEARS) + [val("-", "SORA_avg", "Q1-2026")]),
    ("Fed funds effective (FY avg)", "#9467bd", "6,4", series("-", "EFFRavg", YEARS) + [val("-", "EFFRavg", "2026-latest")]),
]

# ---- geometry ----
W, H = 880, 460
PL, PR, PT, PB = 64, 24, 46, 78          # plot margins
Y_MAX = 5.5
PW, PH = W - PL - PR, H - PT - PB

def xp(i):
    return PL + i * (PW / (len(X_LABELS) - 1))

def yp(v):
    return PT + PH - (v / Y_MAX) * PH

def f(x):
    return f"{x:.1f}"

def build_svg():
    e = []
    e.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">')
    e.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
    e.append(f'<text x="{PL}" y="22" font-size="16" font-weight="bold" fill="#222222">Group NIM vs 3M SORA and Fed funds (%)</text>')
    e.append(f'<text x="{PL}" y="38" font-size="11" fill="#666666">FY2016–FY2025 + 2026 latest · NIM solid, policy/benchmark rates dashed · generated from data/ledger.csv</text>')
    # gridlines + y labels
    for g in range(0, 6):
        y = f(yp(g))
        e.append(f'<line x1="{PL}" y1="{y}" x2="{W - PR}" y2="{y}" stroke="#e0e0e0" stroke-width="1"/>')
        e.append(f'<text x="{PL - 8}" y="{f(yp(g) + 4)}" font-size="11" fill="#666666" text-anchor="end">{g}%</text>')
    # x labels
    for i, lab in enumerate(X_LABELS):
        e.append(f'<text x="{f(xp(i))}" y="{H - PB + 18}" font-size="11" fill="#666666" text-anchor="middle">{lab}</text>')
    # series
    for label, color, dash, vals in SERIES:
        pts = [(xp(i), yp(v)) for i, v in enumerate(vals) if v is not None]
        path = " ".join(f"{f(x)},{f(y)}" for x, y in pts)
        dashattr = f' stroke-dasharray="{dash}"' if dash else ""
        e.append(f'<polyline points="{path}" fill="none" stroke="{color}" stroke-width="{2 if dash else 2.5}"{dashattr}/>')
        for x, y in pts:
            e.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="2.4" fill="{color}"/>')
    # legend (two rows)
    lx, ly = PL + 6, PT + 10
    for idx, (label, color, dash, _) in enumerate(SERIES):
        row, col = divmod(idx, 3)
        x = lx + col * 150
        y = ly + row * 18
        dashattr = f' stroke-dasharray="{dash}"' if dash else ""
        e.append(f'<line x1="{x}" y1="{y}" x2="{x + 22}" y2="{y}" stroke="{color}" stroke-width="3"{dashattr}/>')
        e.append(f'<text x="{x + 28}" y="{y + 4}" font-size="11" fill="#333333">{label}</text>')
    # footnote
    e.append(f'<text x="{PL}" y="{H - 12}" font-size="10" fill="#888888">*2026 = 1Q26 group NIM (quarter ended 31 Mar 2026) · 1Q26 average 3M SORA (bank-characterised, ~1.07%) · Fed funds effective 2026 YTD. 3M compounded SORA exists only from Aug-2020.</text>')
    e.append('</svg>')
    return "\n".join(e) + "\n"

if __name__ == "__main__":
    out = ASSETS / "nim-vs-sora.svg"
    content = build_svg()
    if "--check" in sys.argv:
        if out.read_text(encoding="utf-8") == content:
            print("CHECK OK: nim-vs-sora.svg reproducible from ledger")
        else:
            sys.exit("CHECK FAIL: committed nim-vs-sora.svg differs from ledger-generated output")
    else:
        ASSETS.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
        print(f"wrote {out}")
