#!/usr/bin/env python3
"""Build-Health — pipeline completeness & confidence metrics for sg-banks.

Reads the ledger, data files, meta.json and the frame, and generates
  meta/health.md    human-readable status print (GitHub-friendly)
  meta/health.json  machine-readable mirror (feed for a future UI)

Completeness = how much of the frame is answered / how many cells are filled.
Confidence   = how trustworthy the filled cells are (dual-verified share,
               checksum agreement, single-retriever exposure, tier flags).
Deterministic: derived only from file contents — no clocks, no git calls.

Usage:  python3 pipeline/sg-banks/method/code/build_health.py [--check]
Spec:   pipeline/sg-banks/method/code/build-health.md
"""
import csv, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
METADIR = ROOT / "meta"
META = ROOT.parents[1] / "reports" / "sg-banks" / "meta.json"

rows = list(csv.DictReader(open(DATA / "ledger.csv", newline="", encoding="utf-8")))
meta = json.loads(META.read_text(encoding="utf-8"))

# ---- completeness ----
status_counts = {}
for r in rows:
    st = (r["reconciliation_status"] or "").strip() or "?"
    status_counts[st] = status_counts.get(st, 0) + 1
total = len(rows)
filled = sum(v for k, v in status_counts.items() if k in ("match", "single-px", "single-cl", "resolved", "text/other"))
unavailable = status_counts.get("n/d", 0)          # bank does not disclose
unretrieved = status_counts.get("n/r", 0)          # retrievable but not retrieved

QUESTIONS = [
    ("Q1", "Deposits & Wealth AUM trend", "answered", "ledger"),
    ("Q2", "Wealth-hub capital flows", "answered" if (DATA / "flows.csv").exists() else "pending", "fetch-flows"),
    ("Q3", "NII & Other Revenue trend", "answered", "ledger"),
    ("Q4", "NIM volatility & cyclicality", "answered", "ledger + chart"),
    ("Q5", "Monetization score vs peers", "answered" if (DATA / "peers.csv").exists() else "partial (SG-only)", "fetch-peers + build-benchmarks"),
    ("Q6", "Relative valuation vs peers", "answered" if (DATA / "peers.csv").exists() else "pending", "fetch-peers + build-benchmarks"),
]
answered = sum(1 for q in QUESTIONS if q[2] == "answered")

# ---- confidence ----
dual = status_counts.get("match", 0) + status_counts.get("resolved", 0)
single = status_counts.get("single-px", 0) + status_counts.get("single-cl", 0)
q126_single = sum(1 for r in rows if r["period"] == "Q1-2026"
                  and (r["reconciliation_status"] or "").strip() == "single-cl")
checksum_rows = [r for r in rows if (r["checksum_expected"] or "").strip()]
checksum_agree = sum(1 for r in checksum_rows if (r["reconciliation_status"] or "").strip() == "match")

# retriever scorecard: where BOTH retrievers filled a numeric cell, do they agree?
both = agree = 0
for r in rows:
    try:
        pv, cv = float(r["px_value"]), float(r["cl_value"])
    except (ValueError, TypeError, KeyError):
        continue
    both += 1
    if pv == cv or (cv != 0 and abs(pv / cv - 1) <= 0.005):
        agree += 1

def tie_outs():
    fails = 0
    L = {(r["bank"], r["metric"], r["period"]): (r["reconciled_value"] or "").strip() for r in rows}
    def f(k):
        try:
            return float(L[k])
        except (KeyError, ValueError):
            return None
    for b in ("DBS", "OCBC", "UOB"):
        for p in [str(y) for y in range(2016, 2026)] + ["Q1-2026"]:
            nii, non, ti = f((b, "NII", p)), f((b, "NonII", p)), f((b, "TotalIncome", p))
            if None not in (nii, non, ti) and abs(nii + non - ti) > 1.0:
                fails += 1
    return fails

tie_fail = tie_outs()
canary_ok = any(r["data_point_id"] == "DBS_NIMgroup_2025" and r["reconciled_value"].strip() == "2.01" for r in rows)

# ---- freshness (from file contents only) ----
stamp_dates = sorted({m.group(1) for r in rows for m in
                      [re.match(r"(\d{8})-", (r.get("cl_version") or "") + " ")] if m} |
                     {m.group(1) for r in rows for m in
                      [re.match(r"(\d{8})-", (r.get("px_version") or "") + " ")] if m})
signals_asof = ""
sig = (DATA / "signals.md")
if sig.exists():
    m = re.search(r"\*\*Last run:\*\* ([0-9-]+)", sig.read_text(encoding="utf-8"))
    signals_asof = m.group(1) if m else "unknown"

health = {
    "version": meta.get("current_version"),
    "last_updated": meta.get("last_updated"),
    "completeness": {
        "questions_total": len(QUESTIONS),
        "questions_answered": answered,
        "questions": [{"id": q[0], "topic": q[1], "status": q[2], "depends_on": q[3]} for q in QUESTIONS],
        "ledger_rows": total,
        "ledger_filled": filled,
        "ledger_filled_pct": round(filled / total * 100, 1),
        "not_disclosed": unavailable,
        "not_retrieved": unretrieved,
    },
    "confidence": {
        "dual_verified_rows": dual,
        "dual_verified_pct_of_filled": round(dual / filled * 100, 1),
        "single_retriever_rows": single,
        "single_retriever_pct_of_filled": round(single / filled * 100, 1),
        "q1_2026_single_retriever_rows": q126_single,
        "checksum_rows": len(checksum_rows),
        "checksum_exact_match": checksum_agree,
        "retriever_scorecard": {
            "both_filled_numeric": both,
            "agree_within_half_pct": agree,
            "agreement_pct": round(agree / both * 100, 1) if both else None,
        },
        "status_breakdown": status_counts,
    },
    "gates": {
        "tie_out_failures": tie_fail,
        "dbs_nim_canary_ok": canary_ok,
    },
    "freshness": {
        "ledger_latest_stamp": stamp_dates[-1] if stamp_dates else None,
        "signals_last_run": signals_asof,
        "peers_fetched": (DATA / "peers.csv").exists(),
        "flows_fetched": (DATA / "flows.csv").exists(),
    },
}

def md():
    c, f, g, fr = health["completeness"], health["confidence"], health["gates"], health["freshness"]
    e = ["# SG Banks — Pipeline Health (generated artifact)", "",
         f"*Artifact: `pipeline/sg-banks/meta/health.md` (+ `health.json`, the machine-readable mirror) — sole output of "
         f"`pipeline/sg-banks/method/code/build_health.py`. Report version {health['version']}, last updated {health['last_updated']}.*", "",
         "## Completeness — how much of the frame is answered", "",
         f"- Key questions: **{c['questions_answered']} of {c['questions_total']} fully answered**",
         ""]
    e += ["| Q | Topic | Status | Depends on |", "|---|---|---|---|"]
    for q in c["questions"]:
        e.append(f"| {q['id']} | {q['topic']} | {q['status']} | {q['depends_on']} |")
    e += ["",
          f"- Ledger: **{c['ledger_filled']} of {c['ledger_rows']} rows filled ({c['ledger_filled_pct']}%)** · "
          f"{c['not_disclosed']} not disclosed by the banks (`n/d`) · {c['not_retrieved']} not yet retrieved (`n/r`)", "",
          "## Confidence — how trustworthy the filled cells are", "",
          f"- **Dual-verified: {f['dual_verified_rows']} rows ({f['dual_verified_pct_of_filled']}% of filled)** — two independent "
          f"retrievers agree or the disagreement is resolved with a documented cause",
          f"- **Single-retriever exposure: {f['single_retriever_rows']} rows ({f['single_retriever_pct_of_filled']}% of filled)** — "
          f"one source only; of these, {f['q1_2026_single_retriever_rows']} are the whole 1Q2026 block (one Claude pass, "
          f"non-Claude cross-check advisable)",
          f"- Checksums: {f['checksum_exact_match']} of {f['checksum_rows']} embedded checksums matched exactly; the rest are "
          f"`resolved` with documented causes (restatements, basis, rounding)",
          f"- Retriever scorecard: where both retrievers filled a numeric cell, they agree (within 0.5%) on "
          f"**{f['retriever_scorecard']['agree_within_half_pct']} of {f['retriever_scorecard']['both_filled_numeric']} cells "
          f"({f['retriever_scorecard']['agreement_pct']}%)** — the cross-model error-rate baseline to improve on", "",
          "## Gates", "",
          f"- Arithmetic tie-outs (NII + Non-II = Total income): **{'all pass' if g['tie_out_failures'] == 0 else str(g['tie_out_failures']) + ' FAILURES'}**",
          f"- DBS group-NIM canary (FY25 = 2.01): **{'pass' if g['dbs_nim_canary_ok'] else 'FAIL'}**", "",
          "## Freshness", "",
          f"- Ledger latest retrieval stamp: {fr['ledger_latest_stamp']}",
          f"- Signals last run: {fr['signals_last_run']}",
          f"- Peer data fetched: {'yes' if fr['peers_fetched'] else 'no (fetch-peers pending)'} · "
          f"Flows data fetched: {'yes' if fr['flows_fetched'] else 'no (fetch-flows pending)'}", ""]
    return "\n".join(e)

if __name__ == "__main__":
    METADIR.mkdir(exist_ok=True)
    md_out, js_out = METADIR / "health.md", METADIR / "health.json"
    md_c = md()
    js_c = json.dumps(health, indent=2) + "\n"
    if "--check" in sys.argv:
        ok = (md_out.exists() and md_out.read_text(encoding="utf-8") == md_c
              and js_out.exists() and js_out.read_text(encoding="utf-8") == js_c)
        if ok:
            print("CHECK OK: health.md/json reproducible from inputs")
        else:
            sys.exit("CHECK FAIL: committed health files differ from generated output")
    else:
        md_out.write_text(md_c, encoding="utf-8")
        js_out.write_text(js_c, encoding="utf-8")
        print(f"wrote {md_out} and {js_out}")
