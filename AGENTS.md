# AGENTS.md — how AI agents work in this repo

This file is the front door for any AI agent (Perplexity, Claude, etc.) acting on this repo. Read it first.

## Golden rules
1. **Never edit `reports/<slug>/` directly.** Published content is generated, not hand-edited.
2. **To change any report, run its controller:** `pipeline/<slug>/UPDATE.md`. That controller is the *only* sanctioned way to update a report. If asked to change a report any other way, stop and route back through the controller.
   - **Never auto-run the EXPENSIVE modules** (`fetch-ledger`, `fetch-signals`) — opt-in only, behind the controller's explicit ask-gate and cost gate. The full cost rule lives in `UPDATE.md` (the single source of truth for modules, paths, and costs); staleness only flags them, never runs them.
3. **Guides are human-owned and live in `pipeline/<slug>/guides/`.** `guides/frame.md` (the human's big questions) and `guides/style.md` (formatting rules) are authored and approved by the human. AI may *propose* changes on request but must never silently regenerate them. Everything else in `pipeline/<slug>/` (`method/`, `data/`) is AI-run generative material, edited only as a controller step instructs.
4. **Versioning is git-native.** Sticky `report.md`; history via commits and tags `<slug>-v<version>`. Never rename a published slug.

## Commit attribution
Every AI-made commit stamps **which harness + model produced it**, using git **trailers** at the end of the commit message. Do not rely on the author line — it reflects the pushing GitHub identity, not the agent that did the work. The `Generated-by:` trailer carries the **same `<Harness><Model>` provenance code as the ledger stamps** (defined in `pipeline/sg-banks/method/ai/fetch-ledger.md` §1: `Px` = Perplexity, `Cw` = Cowork/Claude Code; e.g. `PxGPT5.6`, `CwClOpus4.8`), so `git log` and the in-file stamps speak one vocabulary.

- **Claude Code / Cowork (Claude) commits** append:
  ```
  Generated-by: Claude Code (Claude Opus 4.8) [CwClOpus4.8]
  Co-Authored-By: Claude <noreply@anthropic.com>
  ```
- **Perplexity commits** append:
  ```
  Generated-by: Perplexity Computer (GPT-5.6) [PxGPT5.6]
  Co-Authored-By: Perplexity <bot@perplexity.ai>
  ```

Name the model that **actually did the work** (never a generic "4.x"); if a run mixes models, record the predominant one — same rule as the ledger stamps. GitHub renders `Co-Authored-By:` as a second contributor with an avatar; `Generated-by:` names the harness + model in plain sight. Together with the ledger's `px_version`/`cl_version` stamps this gives two provenance records — trailers on every commit, stamps inside the data files — consistent with the provenance discipline this repo demonstrates.

## Connecting Claude Code on the web to this repo
Claude Code on the web (`claude.ai/code`, Pro/Max/Team/Enterprise) runs in an Anthropic-managed cloud sandbox — browser chat, no terminal — and writes to GitHub directly. One-time setup:
1. Open **`claude.ai/code`** and authorize the **GitHub connection** (grant access to `mingsagent1/hmhc-reports`).
2. Start a session on this repo; Claude clones it fresh into the sandbox each time.
3. Claude works on a **feature branch** and opens a **pull request** rather than committing to `main` — the PR is the review gate before anything reaches `reports.hmhc.ai`.
4. Commits are pushed under **your GitHub identity** (attribution for the push); the **`Generated-by:` / `Co-Authored-By:` trailers above** are what record the agent.

## Repos & series
- Repo: `mingsagent1/hmhc-reports` · Site: `reports.hmhc.ai`
- Current series: `sg-banks` → controller at `pipeline/sg-banks/update.md`

## When the user says "update the report"
Open `pipeline/<slug>/UPDATE.md` and follow it **in order**. It will assess module state, then **stop and ask you which modules to refresh** before doing any work. Do not skip the ask-gate, and do not run an expensive module without its explicit cost-gate confirmation.

## File naming convention
Method files are `method/<verb>-<artifact>.md`; the **verb is the execution category** (`fetch-` = live web, expensive · `reconcile-` = human+AI cross-check · `build-` = assembly, low insight · `write-` = insight/synthesis) and the `<artifact>` token names the output: `fetch-ledger.md`→`data/ledger.csv`, `fetch-signals.md`→`data/signals.md`, `reconcile-ledger.md`→`reconciled_*` columns of `data/ledger.csv`, `build-tables.md`→`data/tables.md`, `build-report.md`→`report.md`, `write-conclusions.md`→the Conclusions section of `report.md`. Methods live in **`method/ai/`** (steps performed by AI models) or **`method/code/`** (deterministic programs, no AI). Human-owned guides are noun-named in `guides/`. The entrypoint is the uppercase `UPDATE.md`.
