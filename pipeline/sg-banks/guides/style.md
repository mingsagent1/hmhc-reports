# sg-banks — Style (human-owned)

> Formatting & marking rules the build must follow. **I own these rules; AI applies them.** Seeded from the report's existing conventions — refine as you like.

- **Currency:** every series in its reporting currency, never FX-converted. SG-bank series are SGD (no conversion, no ADRs); cross-hub macro in USD as sourced; peer financials in each bank's local reporting currency.
- **Number formats:** deposits & assets in billions (no decimals); revenue & profit in billions (1 decimal); margins and ratios as percentages.
- **Marking:** table cells carry a number, `n/r` (not retrieved), or `n/d` (not disclosed) only. Derived cells (ratios, CAGRs, valuations) are unmarked; each table gets a formula footnote.
- **Citations:** bracketed `[n]` markers (superscript substitute), keyed to a per-table or per-section source list. **No raw HTML** (`<sub>`, `<sup>`, …) in published files — the site renders pure markdown only; notes/footnotes are italic paragraphs under their table or answer.
- **Restatements / adjustments:** flagged in a footnote, never silently baked into a figure.
- **Tone:** neutral and descriptive — report the finding, don't sell it. Every report ends with "Not investment advice."
