#!/usr/bin/env python3
"""Build-Gaps — the smart-update worklist for sg-banks.

Reads the reconciled ledger and module outputs and generates
  meta/gaps.md    prioritized fetch worklist (human-readable)
  meta/gaps.json  machine-readable mirror (feed for a future UI / job cards)

Purpose: enable SURGICAL fetch jobs (delta updates) instead of expensive
full refreshes — each gap names exactly which rows need work, the SOP that
covers it, and a job-size estimate. Deterministic: file contents only.

Usage:  python3 pipeline/sg-banks/method/code/build_gaps.py [--check]
Spec:   pipeline/sg-banks/method/code/build-gaps.md
"""
import csv, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
METADIR = ROOT / "meta"

rows = list(csv.DictReader(open(DATA / "ledger.csv", newline="", encoding="utf-8")))

def st(r):
    return (r["reconciliation_status"] or "").strip()

# Expected next results dates (approximate, from each bank's historical cadence;
# update when banks announce). Static by design — determinism over precision.
CALENDAR = [
    ("DBS", "1H26 results", "early Aug 2026 (historically ~first week of Aug)"),
    ("OCBC", "1H26 results", "early Aug 2026 (historically ~first week of Aug)"),
    ("UOB", "1H26 results", "early Aug 2026 (historically ~first week of Aug)"),
]

# P1 — retrievable but never retrieved
p1 = [r["data_point_id"] for r in rows if st(r) == "n/r"]

# P2 — single-retriever rows needing a cross-check pass, in job-sized batches
q126 = [r["data_point_id"] for r in rows if st(r) == "single-cl" and r["period"] == "Q1-2026"]
other_cl = Counter(r["metric"] for r in rows if st(r) == "single-cl" and r["period"] != "Q1-2026")
px_fam = Counter(r["metric"] for r in rows if st(r) == "single-px")

# P4 — pending module outputs
pending_outputs = [name for name, f in (("fetch-flows → data/flows.csv", DATA / "flows.csv"),
                                        ("fetch-peers → data/peers.csv", DATA / "peers.csv")) if not f.exists()]

gaps = {
    "p1_never_retrieved": {
        "priority": 1, "sop": "method/ai/fetch-ledger.md",
        "rows": p1, "count": len(p1),
        "note": "n/r cells — retrievable from Tier-1 but never fetched; smallest possible job",
    },
    "p2a_q1_2026_single_claude": {
        "priority": 2, "sop": "method/ai/fetch-ledger.md (verification pass, non-Claude)",
        "rows": q126, "count": len(q126),
        "note": "the whole 1Q2026 interim block is one Claude pass — a non-Claude re-fetch upgrades it to dual-verified; "
                "consider bundling with the 2Q26 refresh (see calendar)",
    },
    "p2b_single_px_history": {
        "priority": 2, "sop": "method/ai/fetch-ledger.md (verification pass, Claude or non-Perplexity)",
        "families": dict(sorted(px_fam.items(), key=lambda kv: -kv[1])), "count": sum(px_fam.values()),
        "note": "FY-history cells filled by one retriever only (px) — grouped by metric family for batch-sized jobs",
    },
    "p2c_single_cl_other": {
        "priority": 3, "sop": "method/ai/fetch-ledger.md (verification pass, non-Claude)",
        "families": dict(sorted(other_cl.items(), key=lambda kv: -kv[1])), "count": sum(other_cl.values()),
        "note": "non-1Q26 cells filled by the Claude retriever only",
    },
    "p3_reporting_calendar": {
        "priority": 2,
        "events": [{"bank": b, "event": ev, "expected": when} for b, ev, when in CALENDAR],
        "note": "when 1H26/2Q26 results land, the 1Q2026 interim block (~%d rows) is superseded — "
                "the natural moment for one bundled fetch job (new quarter + P2a verification)" % len(q126),
    },
    "p4_pending_module_outputs": {
        "priority": 1, "items": pending_outputs, "count": len(pending_outputs),
        "note": "modules written and cost-gated; queue via PERPLEXITY.md",
    },
}

def md():
    e = ["# SG Banks — Fetch Gaps (smart-update worklist)", "",
         "*Artifact: `pipeline/sg-banks/meta/gaps.md` (+ `gaps.json`) — sole output of `pipeline/sg-banks/method/code/build_gaps.py`. "
         "Each gap is a surgical fetch job: exact rows, the SOP that covers it, and a size estimate — so updates are deltas, "
         "not full refreshes. Queue jobs for the external runner via `PERPLEXITY.md`.*", "",
         "| # | Gap | Size | SOP | Priority |", "|---|---|---:|---|---|",
         f"| P1 | Never-retrieved cells (`n/r`) | {gaps['p1_never_retrieved']['count']} rows | fetch-ledger (delta) | high |",
         f"| P2a | 1Q2026 block single-Claude → needs non-Claude verification | {gaps['p2a_q1_2026_single_claude']['count']} rows | fetch-ledger (verify) | high (bundle with 2Q26) |",
         f"| P2b | FY-history single-px cells | {gaps['p2b_single_px_history']['count']} rows | fetch-ledger (verify) | medium |",
         f"| P2c | Other single-cl cells | {gaps['p2c_single_cl_other']['count']} rows | fetch-ledger (verify) | low |",
         f"| P3 | Reporting calendar — next results supersede the interim block | ~{gaps['p2a_q1_2026_single_claude']['count']} rows | fetch-ledger + fetch-signals | dated |",
         f"| P4 | Pending module outputs | {gaps['p4_pending_module_outputs']['count']} datasets | fetch-flows · fetch-peers | high |", "",
         "## P1 — never retrieved (`n/r`)", "",
         "`" + "`, `".join(gaps["p1_never_retrieved"]["rows"]) + "`" if gaps["p1_never_retrieved"]["rows"] else "none", "",
         "## P2a — 1Q2026 single-Claude block", "",
         f"{gaps['p2a_q1_2026_single_claude']['count']} rows, all stamped `20260720-001 CwClOpus4.8`. "
         "A non-Claude verification pass upgrades the whole block to dual-verified. " + gaps['p2a_q1_2026_single_claude']['note'].split('; ')[-1] + ".", "",
         "## P2b — single-px FY-history families", ""]
    e += ["| Metric family | Rows |", "|---|---:|"]
    for fam, n in gaps["p2b_single_px_history"]["families"].items():
        e.append(f"| {fam} | {n} |")
    e += ["", "## P2c — other single-cl families", "", "| Metric family | Rows |", "|---|---:|"]
    for fam, n in gaps["p2c_single_cl_other"]["families"].items():
        e.append(f"| {fam} | {n} |")
    e += ["", "## P3 — reporting calendar (approximate, from historical cadence)", ""]
    for ev in gaps["p3_reporting_calendar"]["events"]:
        e.append(f"- **{ev['bank']}** — {ev['event']}: expected {ev['expected']}")
    e += ["", gaps["p3_reporting_calendar"]["note"], "",
          "## P4 — pending module outputs", ""]
    for item in gaps["p4_pending_module_outputs"]["items"]:
        e.append(f"- {item}")
    if not gaps["p4_pending_module_outputs"]["items"]:
        e.append("none — all module outputs present")
    return "\n".join(e).rstrip() + "\n"

if __name__ == "__main__":
    METADIR.mkdir(exist_ok=True)
    md_out, js_out = METADIR / "gaps.md", METADIR / "gaps.json"
    md_c = md()
    js_c = json.dumps(gaps, indent=2) + "\n"
    if "--check" in sys.argv:
        ok = (md_out.exists() and md_out.read_text(encoding="utf-8") == md_c
              and js_out.exists() and js_out.read_text(encoding="utf-8") == js_c)
        if ok:
            print("CHECK OK: gaps.md/json reproducible from inputs")
        else:
            sys.exit("CHECK FAIL: committed gaps files differ from generated output")
    else:
        md_out.write_text(md_c, encoding="utf-8")
        js_out.write_text(js_c, encoding="utf-8")
        print(f"wrote {md_out} and {js_out}")
