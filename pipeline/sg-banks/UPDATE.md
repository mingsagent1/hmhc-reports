# sg-banks — UPDATE (ENTRYPOINT controller)

> **This is the single entrypoint for any change to the sg-banks report.**
> Do not edit `reports/sg-banks/*` directly. Follow Steps 1–6 **in order**, **stop at the Step 2 gate to ask the user**, and **never auto-run an EXPENSIVE module** (see the cost rule below). Never assume which modules to run.

## ⚠ Cost rule (read first)
Two modules are **EXPENSIVE** (live web retrieval, token/time-intensive): **`update-ledger`** and **`scan-signals`**. They are **opt-in only**:
- They are **never run by default** and **never triggered automatically by staleness** — staleness only *flags* them, it never *runs* them.
- They run **only** when BOTH are true: (1) the user **explicitly names** the module, and (2) the user **reconfirms at the cost gate** (Step 2b) in chat.
- No explicit confirmation ⇒ skip that module and continue with the rest.

## Guides (human-owned) vs Modules (AI-run)

**Guides — the human owns these; AI only advises.** Constrain the modules; never auto-generated.

| Guide | File | Purpose |
|---|---|---|
| **Frame** | `guides/frame.md` | Your big questions the report must answer. AI may propose candidates on request; you author/approve. |
| **Style** | `guides/style.md` | Formatting & marking rules. You own them; AI applies them. |

**Modules — AI-run generative steps.**

| Module | Method file | Output artifact | Cost | Depends on |
|---|---|---|---|---|
| Retrieve | `method/update-ledger.md` | `data/ledger.csv` (retriever columns) | **EXPENSIVE — opt-in** | Frame |
| Scan | `method/scan-signals.md` | `data/signals.md` | **EXPENSIVE — opt-in** | Frame |
| Reconcile | `method/reconcile-ledger.md` | `reconciled_*` columns of `data/ledger.csv` | cheap | Retrieve |
| Tables | `method/build-tables.md` | `data/tables.md` | cheap | Reconcile |
| Assemble | `method/build-report.md` | `reports/sg-banks/report.md` | cheap | Tables, Frame, Scan, Style |
| ExecSummary | `method/write-execsummary.md` | Executive Summary section of `report.md` (in place, between markers) | cheap | Assemble, Frame |
| Publish | (this controller) | `reports/sg-banks/meta.json` | cheap | ExecSummary |

Model per module: Retrieve/Scan → GPT-5.6/Orchestrator (search); Reconcile → human + Claude; Tables/Assemble → Claude 4.8; ExecSummary → GPT-5.6 (closed-book).

---

## Step 1 — Assess state (always print; never skip)

For each **module** classify: **MISSING** (method file or output absent) · **STALE** (an upstream output committed more recently than this output — `git log -1 --format=%cI -- <path>`) · **DATA-AGE** (Retrieve/Scan only — last retrieval date vs today; new quarter closed ⇒ "possibly outdated") · **OK**.
For **guides** (Frame, Style): report as *human-owned*; never mark STALE or auto-refresh.

Output a table: `item | type (guide/module) | cost | status | reason`. **Flagging an EXPENSIVE module as STALE/DATA-AGE does not authorize running it** — it only informs the user.

## Step 2 — GATE: ask the user (mandatory stop)

Present the table, then ask:
> "Which modules would you like to refresh? Cheap/suggested: [list]. **Expensive (needs explicit confirm): update-ledger, scan-signals.** Or reply **none** to just refresh the report (lite). Also: revise your **Frame** or **Style**? I can propose, you approve."

**Do not proceed until the user answers.**

## Step 2b — COST GATE (only if an EXPENSIVE module was named)

For each expensive module the user selected, ask a **second, explicit confirmation**:
> "Running **<module>** does live web retrieval and is token/time-intensive. Confirm you want to run it now? (yes / no)"

Run it **only** on an explicit "yes". On "no" or anything ambiguous, **skip that module** and continue. Do not batch-assume a single "yes" covers both — confirm each expensive module.

## Step 3 — Run the selected path

- **Guide revised (Frame/Style):** human edit — AI may propose wording, human approves; write to `guides/frame.md` / `guides/style.md`; then rerun downstream (Frame ⇒ Assemble ⇒ ExecSummary; Style ⇒ Assemble/ExecSummary presentation).
- **Modules named (and confirmed where expensive):** run in dependency order (Retrieve ‖ Scan → Reconcile → Tables → Assemble), honoring current Frame & Style. Refreshing any module forces rerun of everything downstream of it.
- **"none":** run the **LITE path** only — rerun **ExecSummary** (`method/write-execsummary.md`, closed-book; rewrites the Executive Summary section of `report.md` in place) and apply **Style** (`guides/style.md`). Never touches `data/`. **The lite path is the default and never invokes an expensive module.**

Always finish with **Publish** (Step 5).

## Step 4 — Gates before publishing (all must pass)
- **Assemble:** arithmetic tie-outs pass; every **Frame** question is addressed in the report.
- **ExecSummary:** every Frame key question answered (or explicitly marked "pending new research module" where the data does not exist — currently Q2 and Q4), each answer cited; thesis score 0–100 with rationale; closed-book (its self-checks).
- Every refreshed module's output exists and is committed.

## Step 5 — Publish (version, meta, commit, tag)
- **Version scheme:** `YYYY.MM.DD` of the publish date; a same-day re-release appends `-r2`, `-r3`, … (e.g. `2026.07.20-r2`). The tag `sg-banks-v<version>` is created on `main` **after the PR merges** (tag automation via GitHub Actions is planned; until then create it manually from the merge commit).
- **Bump:** data/scan/tables changed ⇒ **minor**; only ExecSummary/Style/presentation ⇒ **patch**; a Frame change that alters the report ⇒ minor.
- Update `reports/sg-banks/meta.json` (`last_updated`, `current_version`, `pipeline.ref` = new tag). Commit; `git tag sg-banks-v<version>`; push.
- **Commit trailers:** every commit carries the `Generated-by:` / `Co-Authored-By:` attribution trailers per `AGENTS.md` § Commit attribution (harness+model code matching the ledger stamps).

## Step 6 — Report back
State: the assessment, which guides/modules changed, whether any expensive module was run (and that it was explicitly confirmed), gates passed, new version + tag.

---

## Enforcement note
Convention-enforced: works only if every change starts here (via `AGENTS.md`). It cannot physically stop a rogue edit or an unconfirmed expensive run — for hard enforcement move Steps 1–5 into code (GitHub Actions `workflow_dispatch`), where the cost gate becomes a required input parameter.
