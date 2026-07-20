# AGENTS.md — how AI agents work in this repo

This file is the front door for any AI agent (Perplexity, Claude, etc.) acting on this repo. Read it first.

## Golden rules
1. **Never edit `reports/<slug>/` directly.** Published content is generated, not hand-edited.
2. **To change any report, run its controller:** `pipeline/<slug>/UPDATE.md`. That controller is the *only* sanctioned way to update a report. If asked to change a report any other way, stop and route back through the controller.
   - **Never auto-run the EXPENSIVE modules** (`update-ledger`, `scan-signals`): they do live web retrieval and are token/time-intensive, so they run **only** when the user explicitly names them **and** reconfirms at the controller's cost gate. Staleness only flags them; it never runs them.
3. **Guides are human-owned and live in `pipeline/<slug>/guides/`.** `guides/frame.md` (the human's big questions) and `guides/style.md` (formatting rules) are authored and approved by the human. AI may *propose* changes on request but must never silently regenerate them. Everything else in `pipeline/<slug>/` (`method/`, `data/`) is AI-run generative material, edited only as a controller step instructs.
4. **Versioning is git-native.** Sticky `report.md`; history via commits and tags `<slug>-v<version>`. Never rename a published slug.

## Repos & series
- Repo: `mingsagent1/hmhc-reports` · Site: `reports.hmhc.ai`
- Current series: `sg-banks` → controller at `pipeline/sg-banks/update.md`

## When the user says "update the report"
Open `pipeline/<slug>/UPDATE.md` and follow it **in order**. It will assess module state, then **stop and ask you which modules to refresh** before doing any work. Do not skip the ask-gate, and do not run an expensive module without its explicit cost-gate confirmation.

## File naming convention
Method files are `method/<verb>-<artifact>.md` and produce an output that shares the `<artifact>` token, so the pair is obvious: `update-ledger.md`→`data/ledger.csv`, `scan-signals.md`→`data/signals.md`, `build-tables.md`→tables, `build-report.md`→`report.md`, `write-execsummary.md`→`execsummary.md`. Human-owned guides are noun-named in `guides/`. The entrypoint is the uppercase `UPDATE.md`.
