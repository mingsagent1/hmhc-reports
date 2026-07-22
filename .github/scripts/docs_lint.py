#!/usr/bin/env python3
"""Docs consistency lint: referenced paths must exist.

Checks three reference classes that have historically drifted:
  1. meta.json pipeline lineage — every pipeline/... or reports/... path
     mentioned in a string value must exist.
  2. pipeline/<slug>/UPDATE.md — every method/*, guides/*, data/* token
     must exist relative to pipeline/<slug>/.
  3. All *.md files — relative markdown link targets [text](path) must
     exist (http(s), mailto and #anchors are skipped).

Historical mentions in registries/changelogs are exempt via class 2/3 scoping
(backticked prose paths are deliberately NOT checked).
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
errors = []

# Declared future outputs of modules that are written but not yet run
# (fetch runs are cost-gated). Remove entries here once the data lands.
PENDING_OUTPUTS = {
    "pipeline/sg-banks/data/flows.csv",     # fetch-flows
    "pipeline/sg-banks/data/peers.csv",     # fetch-peers
}

def check(path_str, where):
    if path_str in PENDING_OUTPUTS:
        return
    p = (ROOT / path_str)
    if not p.exists():
        errors.append(f"{where}: missing path '{path_str}'")

# 1. meta.json lineage paths
for meta in ROOT.glob("reports/*/meta.json"):
    def walk(x):
        if isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
        elif isinstance(x, str):
            for m in re.findall(r"(?:pipeline|reports)/[A-Za-z0-9_./-]+", x):
                check(m.rstrip("./"), str(meta.relative_to(ROOT)))
    walk(json.loads(meta.read_text()))

# 2. UPDATE.md module/guide/data tokens
for upd in ROOT.glob("pipeline/*/UPDATE.md"):
    base = upd.parent
    text = upd.read_text()
    for m in re.findall(r"`((?:method(?:/(?:ai|code))?|guides|data)/[A-Za-z0-9_.-]+\.(?:md|py|csv))`", text):
        if f"{base.relative_to(ROOT)}/{m}" in PENDING_OUTPUTS:
            continue
        if not (base / m).exists():
            errors.append(f"{upd.relative_to(ROOT)}: missing path '{m}'")

# 3. relative markdown links in all .md files
for md in ROOT.rglob("*.md"):
    if ".git" in md.parts:
        continue
    for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)\s]*)?\)", md.read_text(encoding="utf-8")):
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        cand = (md.parent / target)
        if not cand.exists() and not (ROOT / target).exists():
            errors.append(f"{md.relative_to(ROOT)}: broken relative link '{target}'")

if errors:
    print("DOCS LINT FAILED:")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("docs lint OK")
