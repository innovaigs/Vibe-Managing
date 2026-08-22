---
name: monthly-business-review
domain: growth
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [company, finance, metrics, goals, strategy, risks, decisions, integrations]
writes: [metrics, decisions, goals, strategy]
related_skills: [variance-diagnosis, executive-dashboard-builder, kpi-design, growth-plan-builder, initiative-prioritization, financial-forecast-builder]
owned_by_agents: [growth-agent, business-analyst-agent]
---

# Skill: Monthly Business Review

## Purpose
Run the company's core learning loop: each month, compare actuals to forecast (and to prior month and prior year), classify each variance in plain language, diagnose the drivers, decide what to adapt, and feed the decision back into the plan. This is the mechanism that turns a static forecast into a system that learns — closing the loop between what the founder planned and what actually happened, so the plan gets more accurate and the next actions get sharper every month.

## When to Use
- The month's books are closed and the founder asks "how did we do vs plan?", "run my monthly review," "close out the month," or "what did we learn this month?"
- The monthly growth-review cadence fires (the recurring learning loop).
- After any period where actuals are available and a forecast exists to compare against.

## When NOT to Use
- Only one metric missed and the founder wants deep root-cause on it → use `variance-diagnosis` (this skill calls it per metric, but a single-metric deep dive can be run directly).
- The forecast or the actuals do not exist yet → the data-completeness gate blocks the review; fix the data first (accounting close, forecast build).
- The founder wants to arrange the monitoring tiles → use `executive-dashboard-builder`.
- The founder wants to rebuild the whole plan → use `growth-plan-builder`.

## Required Context
- `finance` — the forecast for the month (P&L, cash flow) AND the actuals for the month (from the accounting integration). Both are mandatory (gate).
- `metrics` — the KPI definitions, thresholds, and prior-period values (for prior-month / prior-year baselines).
- `risks` — the risk warning-signal metrics and thresholds (to check whether any tripped).
- `goals` / `strategy` — the Success Factors, Progress Metrics, Next Steps, and forecast assumptions (the adaptation targets).
- `decisions` — the prior-month review record (to detect assumptions missing the same direction repeatedly).

## Inputs
```yaml
input:
  period: {month, year}
  headline_metrics: list           # default: Revenue, Expenses & Costs, Net Profit, Cash Balance/Net Cash Flow
  forecast: object                 # per-metric forecast values for the period  (REQUIRED)
  actuals: object                  # per-metric actual values for the period    (REQUIRED)
  previous_month: object|null      # per-metric prior-month actuals
  previous_year: object|null       # per-metric same-month-last-year actuals
  line_items: object|null          # per-metric line-item breakdown (for Top Movers)
  tolerance_band_pct: number       # e.g. 5 → within +/-5% classifies "about the same"; configurable
  assumptions: list|null            # forecast key assumptions with direction/confidence
  risk_signals: list|null           # [{risk, metric, threshold, owner}]
  prior_review: object|null         # last month's classifications & adaptation decisions
```

## Missing Information Protocol
1. **Data-completeness gate runs first.** For each headline metric, BOTH a forecast value and an actual value are required. If either is missing for the month, the review is BLOCKED for that metric (or entirely, if the whole month is unpopulated) with an explicit incompleteness notice — never present variance analysis on half-populated data.
2. If actuals are missing, point to the accounting close; if forecast is missing, point to `financial-forecast-builder`. Surface the specific gap, not a partial result.
3. Prior-month / prior-year baselines are optional enrichments — if absent, run the forecast comparison and note the missing baselines rather than blocking.
4. Never assume a value to fill a gap, never impute an actual, and never treat "no data" as "zero."

## Diagnostic Questions
- Do we have BOTH a forecast and an actual for every headline metric this month? (gate)
- For each metric: higher / lower / about the same vs forecast, prior month, and prior year — and by how much (amount and %)?
- What are the Top Movers driving each variance, and what caused each?
- Is any favorable variance real, or an artifact of reduced activity? (check co-movement of related metrics)
- Did any risk warning-signal threshold trip this month?
- Which assumption, if any, has now missed direction two-plus months in a row and must be re-forecast?
- What concrete change to the Next-Steps list results from this month's learning?

## Analysis Framework — the learning loop
**COMPARE → CLASSIFY → DIAGNOSE → ADAPT → NEXT ACTION**, preceded by the data-completeness gate.

**0. GATE — data integrity.** Confirm forecast AND actual exist for each metric. Block and surface any gap before proceeding.

**1. COMPARE.** For each headline metric (Revenue, Expenses & Costs, Net Profit, Cash Balance / Net Cash Flow), compute actual vs three baselines — Forecast, Previous Month, Previous Year — reporting both delta amount and delta %.

**2. CLASSIFY.** Convert each raw variance to a plain-language band, not a bare number: "Higher than / Lower than / About the same as" each baseline. Apply the tolerance band so small variances collapse to "about the same" and the founder does not over-react to noise.

**3. DIAGNOSE with Top Movers.** For each material variance, rank line items by contribution to the variance and name the specific drivers (each with Actual, Forecast, Change). Attribution before action — isolate *where* the miss came from, not just *that* the total missed. For any single flagged metric, hand off to `variance-diagnosis` for full root-cause and co-movement interpretation.

**4. ADAPT.** Based on the diagnosis, choose the lever: (a) correct execution, (b) re-forecast the assumption that was wrong, (c) re-prioritize/re-sequence initiatives, or (d) trip a risk warning-signal and activate its contingency. Apply the co-movement rule (see Decision Rules) so a favorable cost variance alongside a revenue shortfall is read as stalled activity, not savings.

**5. NEXT ACTION.** Translate each adaptation into a concrete change to the Next-Steps list and the assumption set, with an owner and a deadline — closing the loop for next month.

## Calculations
- **Variance amount** = Actual − Forecast (and Actual − Prior Month; Actual − Prior Year).
- **Variance %** = (Actual − Forecast) / Forecast × 100. Undefined when Forecast = 0 → report "no comparison" (never 0% or ∞).
- **Classification band:** |Variance %| ≤ tolerance_band_pct → "about the same"; > tolerance and positive → "higher than"; > tolerance and negative → "lower than." Same logic for each baseline.
- **Top Movers contribution** = line-item (Actual − Forecast); rank by |contribution| descending; report top drivers until they explain the bulk of the total variance.
- **Co-movement check:** compare the sign/magnitude of related metrics (e.g., expenses vs revenue) to test whether a variance is genuine performance or an activity artifact.
- **Assumption-miss streak** = count of consecutive months an assumption missed the same direction; ≥ 2 → systematic, re-forecast.

## Decision Rules
- IF forecast OR actual is missing for the month THEN block the review and surface the data gap instead of reporting variance.
- IF |variance %| within the tolerance band THEN classify "about the same" and take no action (avoid noise-chasing).
- IF revenue is below forecast beyond tolerance THEN run Top-Movers attribution and flag the responsible line/segment for a corrective Next Step.
- IF expenses are below forecast AND revenue is also below forecast THEN treat as stalled activity (NOT savings) and investigate execution — do not celebrate the "cost saving."
- IF the same assumption misses the same direction for 2+ consecutive months THEN re-forecast that assumption (systematic error, not noise) and update `strategy`.
- IF cash runway < 6 months THEN trigger a funding / cash-preservation initiative as top priority.
- IF burn rate exceeds plan by > 15% THEN escalate a cost review and re-sequence spend.
- IF win rate on proposals < 40% OR average deal size declines > 10% THEN trigger a competitive-differentiation / pricing review.
- IF gross-margin compression > 3% (or margin outside its target band) THEN review pricing and cost structure by service line.
- IF a top risk's warning-signal crosses its threshold THEN activate that risk's contingency and notify its accountable owner.
- IF a Next-Step passed its deadline incomplete THEN re-prioritize/re-scope and reset the deadline; surface repeated slippage as an execution-risk signal.
- IF a proposed adaptation involves spend, a pricing change, or a public commitment THEN hold it for founder approval (analysis and the recommendation proceed; execution does not).

## Procedure
1. Run the data-completeness gate; block and surface gaps for any metric lacking forecast or actual.
2. COMPARE each headline metric to Forecast, Previous Month, Previous Year (amount + %).
3. CLASSIFY each variance into higher / lower / about the same using the tolerance band.
4. DIAGNOSE each material variance with Top Movers; hand flagged metrics to `variance-diagnosis`.
5. Apply the co-movement rule to every "favorable" variance to confirm it is real.
6. Check every risk warning-signal against its threshold; check assumption-miss streaks against prior reviews.
7. ADAPT: choose the lever per metric and write proposed adaptations.
8. NEXT ACTION: convert adaptations into dated, owned Next-Step changes.
9. Emit the review (L1) with classifications, Top Movers, adaptation decisions, and Next-Step changes; hold any spend/pricing/commitment for approval.
10. On approval, write the review record to `decisions`, update `metrics` (prior-period values), re-forecast assumptions in `strategy`, and update `goals` (Next Steps).

## Output
```yaml
output:
  period: {month, year}
  gate: {status: enum(passed, blocked), missing: [ {metric, missing: enum(forecast, actual, both)} ]}
  comparisons:                     # only if gate passed
    - metric: str
      actual: number
      vs_forecast: {amount, pct, class: enum(higher, lower, about_same)}
      vs_previous_month: {amount, pct, class} | null
      vs_previous_year: {amount, pct, class} | null
      top_movers: [ {line, actual, forecast, change} ]
      co_movement_note: str|null   # e.g. "favorable cost variance is an artifact of stalled revenue"
  risk_signals_tripped: [ {risk, metric, value, threshold, owner} ]
  assumptions_to_reforecast: [ {assumption, miss_streak, direction} ]
  adaptations: [ {metric, lever: enum(correct_execution, reforecast, reprioritize, trip_risk), rationale, needs_approval: bool} ]
  next_step_changes: [ {change, owner, deadline} ]
  headline_summary: text           # plain-language "here is what happened and what we're doing about it"
```

## Recommendations
Adaptation decisions are prioritized by threat to the business, then by leverage: (1) cash/runway and tripped-risk items first (existential); (2) systematic assumption errors (they corrupt every future forecast until fixed); (3) margin/pricing/win-rate deteriorations; (4) execution corrections. Each recommendation states the lever, the evidence (Top Movers + co-movement), the expected effect, and whether it needs founder approval. A favorable variance is never recommended as a win until the co-movement check confirms it is real.

## Execution Opportunities
- Produce the full review, classifications, Top Movers, and adaptation recommendations (reversible, LOW) — L1.
- Update prior-period metric values and the dashboard after the review (reversible, LOW).
- Create/adjust internal Next-Step tasks with owners and deadlines (reversible, LOW).
- Route tripped risk signals to their contingency owners (reversible, LOW — internal notice).
- Draft a re-forecast of a systematically-wrong assumption for CFO/founder review (reversible, LOW — draft only).

## Human Approval Requirements
- Any adaptation involving budget/experiment spend, a pricing change, or a public/external commitment requires founder approval before execution.
- Committing a re-forecast as the new authoritative forecast requires founder (and CFO agent / accountant) approval.
- Activating a risk contingency that spends money, contacts external parties, or changes staffing requires approval per that contingency.
- Analysis, classification, diagnosis, drafting, and internal task creation proceed at L1. Complies with AUTONOMY_AND_APPROVAL_MODEL.md.

## Escalation Conditions
- Data-completeness gate cannot be satisfied (persistent missing actuals/forecast) → founder + accounting (fix the source data).
- Cash runway < 6 months or burn > 15% over plan → founder + (recommend) accountant.
- A tripped risk signal implicates tax/regulatory, contracts, or a specific employee → accountant / attorney / HR respectively.
- An assumption is systematically wrong but the correct value is genuinely uncertain → surface the uncertainty; do not silently pick a number.
- Two-plus consecutive months of the same Next-Step slippage → founder (execution-risk / possible key-person constraint).

## KPIs
- Gate pass rate (months with complete data) — a measure of the whole system's data hygiene.
- Forecast accuracy trend (variance % shrinking over months as re-forecasting corrects assumptions).
- % of adaptations that produced the expected effect next month (the loop actually learning).
- Time from month-close to completed review.
- Number of favorable-variance misreads caught by the co-movement rule.

## Monitoring
Track whether each adaptation moved its metric in the intended direction next month (the loop's own feedback), whether re-forecast assumptions now hold, and whether Next-Step changes were completed. Watch for recurring gate failures (data hygiene problem) and for assumptions that keep needing re-forecasting (a deeper model error).

## Follow-Up
- Runs every month on the growth-review cadence (time-triggered), immediately after the accounting close.
- Event-triggered off-cycle when a risk signal trips mid-month or a major variance is detected in the dashboard.
- Feeds the quarterly growth-plan refresh with accumulated learnings.

## Related Skills
Calls `variance-diagnosis` per flagged metric; consumes `executive-dashboard-builder` headline tiles and Top Movers; uses `kpi-design` thresholds; feeds `initiative-prioritization` (re-sequencing) and `financial-forecast-builder` (re-forecast); updates `growth-plan-builder` (Next Steps / assumptions) at the quarterly refresh.

## Guardrails
- Never present variance analysis on incomplete data — the gate is absolute.
- Never treat a favorable single-metric variance as good without the co-movement check (lower expenses with lower revenue = stalled activity, not efficiency).
- Never impute or assume an actual; "no data" is never "zero."
- Handle divide-by-zero (Forecast = 0) as "no comparison."
- A recommendation to spend, re-price, or commit externally is a proposal held for approval, not an auto-action.
- Distinguish noise from signal via the tolerance band; do not trigger action on within-band variance.

## Example
**Founder input:** "Close out July for me — how did we do vs plan?"

**Skill reasoning:**
- GATE: Revenue actual = $0, forecast = $22,400 (present); Expenses actual = $0, forecast = $15,836 (present); Net Profit and Cash present. Gate passes for all headline metrics.
- COMPARE: Revenue $0 vs $22,400 → −$22,400, −100%. Expenses $0 vs $15,836 → −$15,836, −100%. Net Profit ≈ flat vs a small forecast profit.
- CLASSIFY: Revenue "lower than forecast"; Expenses "lower than forecast."
- DIAGNOSE (Top Movers): no revenue line posted; no cost lines posted.
- CO-MOVEMENT rule fires: expenses "lower than forecast" is NOT a saving — it co-moves with revenue at $0, meaning the business was inactive that month, not efficient. Flagged as stalled activity.
- Risk signals: cash runway checked — still > 6 months, no trip. Assumption check: "monthly project revenue starts in July" missed; first month of this direction, not yet a 2-month streak (watch next month).
- ADAPT: lever = correct_execution (why was there no activity/billing in July?), plus watch the revenue-start assumption for a second miss.
- NEXT ACTION: Next Step — "confirm July inactivity cause and restart billing," owner = founder, deadline set; monitor the revenue-start assumption in August.

**Output (abridged):** gate passed; Revenue & Expenses both "lower than forecast"; co_movement_note = "favorable cost variance is an artifact of zero activity, not savings"; no risk trips; assumptions_to_reforecast = [] (streak = 1, flagged to watch); adaptation = correct_execution; one dated Next Step.

**Executed vs. approval:** Review, classification, co-movement flag, and the internal Next-Step task executed at L1. No spend/pricing/commitment proposed this month, so nothing was held for approval; had a re-forecast or spend been triggered, it would have been held.

## Provenance
SOURCE — derived from the Growth Execution domain knowledge (`09-growth-execution.md`): the forecast-vs-actual monthly review method (the COMPARE→CLASSIFY→DIAGNOSE→ADAPT→NEXT-ACTION loop), the data-integrity precondition gate, the three-baseline comparison (Forecast / Previous Month / Previous Year), the plain-language variance bands with a tolerance collapse, Top Movers attribution, and the cost-variance co-movement interpretation nuance ($0 expenses vs forecast because the business was inactive, not efficient). De-branded (generic "accounting tool," no named products or company). See internal/PROVENANCE_MAP.md.
