# Frame — Module SOP (SG Banks)

> **Project:** Singapore Bank Stock Accumulation Strategy
> **Artifact:** `pipeline/sg-banks/method/frame.md` — version history in git (`git log --oneline pipeline/sg-banks/method/frame.md`).
> **Status:** Draft.
> **Module role:** the first module in the pipeline. It sets the thesis, the key questions, and the good-vs-bad rubric that every downstream module is judged against.

## Module contract

| | |
|---|---|
| **Inputs** | The current project registry (`pipeline/sg-banks/index.md`) and the project brief / prior framing embedded there. No external facts. |
| **Sole output** | `pipeline/sg-banks/frame.md` (the framing artifact — thesis, key questions, good-vs-bad rubric). |
| **Idempotence** | Rerunning overwrites `pipeline/sg-banks/frame.md` in place. Git retains the history; do not create timestamped copies or an `archive/` folder. |
| **Recommended model** | Any capable reasoning model. This is a thinking/synthesis step, not a search step — no search grounding required. Claude 4.8 or GPT-5.6 are both fine. |
| **Position** | `Frame → (Retrieve ‖ Scan) → Tables → Assemble → Exec Summary → Publish`. Frame runs first and is **revisited each version**. |

## What Frame is for

Frame is the pipeline's north star. Before any data is retrieved or any table is built, Frame answers: *what are we actually trying to learn, and how will we know a good answer from a bad one?* Everything downstream (which rows to retrieve, which signals to scan for, which tables to build, what the report emphasises) should trace back to the thesis and questions written here.

Frame is a **living document**. It is deliberately re-opened at the start of each report version: the thesis may sharpen, questions get answered or retired, and the rubric tightens as the analysis matures. Do not treat it as write-once.

## How to run this module

1. **Read the inputs.** Read `pipeline/sg-banks/index.md` (the registry, standing analytical decisions, open decisions) and the current `pipeline/sg-banks/frame.md` if one exists. Understand what the project already believes and what is still open.
2. **State the thesis.** One or two paragraphs: what is the central hypothesis this report exists to test? Ground it only in what the repo already asserts — do not import outside market views or investment advice.
3. **List the key questions.** The specific, answerable questions the report must address for the thesis to be evaluated. Each should be traceable to a table or section downstream (or flagged as not-yet-covered).
4. **Write the good-vs-bad rubric.** Explicit criteria for what makes a *good* answer to this brief versus a *bad* one — e.g. sourced Tier-1 numbers vs aggregator fills, within-bank trends vs false cross-bank comparisons, honest `n/r` vs plausible guesses. This rubric is what reviewers and downstream modules check against.
5. **Note open framing questions.** Anything unresolved about scope or definitions that a future version should settle.
6. **Overwrite** `pipeline/sg-banks/frame.md`. Commit with a descriptive message.

## Guardrails

- **No external facts.** Frame synthesises the project's own stated position; it does not introduce new market data, forecasts, or investment recommendations.
- **No investment advice.** The rubric and thesis describe *what the analysis should establish*, never *what to buy or sell*.
- **One output only.** The sole artifact is `pipeline/sg-banks/frame.md`. Do not emit side files.

## Acceptance criteria (stop when all true)
- `pipeline/sg-banks/frame.md` contains a thesis, a numbered set of key questions, and a good-vs-bad rubric.
- Every claim is grounded in existing repo content — no outside facts, no investment view.
- The document reads as a usable brief a downstream module could actually be steered by.
