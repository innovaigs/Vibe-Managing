---
name: variance-diagnosis
domain: growth
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [finance, metrics, goals, strategy, risks, customers, offerings, operations, decisions]
writes: [decisions, metrics]
related_skills: [monthly-business-review, executive-dashboard-builder, kpi-design, initiative-prioritization, financial-forecast-builder]
owned_by_agents: [growth-agent, business-analyst-agent]
---

# Skill: Variance Diagnosis

## Purpose
Take a single metric that missed its target and explain WHY: attribute the miss to the specific line-item drivers behind it, interpret it against co-moving related metrics so a misleading "good" number is caught, and recommend the one lever most likely to correct it. This is attribution before action — the difference between knowing the total missed and knowing the root cause well enough to fix it.

## When to Use
- A metric missed forecast (or moved sharply vs prior period) and the founder asks "why?", "what drove this?", "what's behind the revenue drop?", or "is this actually a problem?"
- The monthly review flagged a material variance and needs root-cause on that specific metric.
- A dashboard tile turned amber/red and the founder wants the driver before acting.
- A "favorable" variance appears and the founder wants to confirm it is real, not an artifact.

## When NOT to Use
- The founder wants the full monthly loop across all headline metrics → use `monthly-business-review` (it calls this skill per flagged metric).
- The forecast or actual for the metric is missing → the data-completeness gate blocks diagnosis; fix the data first.
- The founder wants to choose which initiative to fund next → use `initiative-prioritization`.
- The variance is within the tolerance band ("about the same") → no diagnosis needed; it is noise.

## Required Context
- `finance` / `metrics` — the metric's actual and forecast values, and its line-item breakdown (the attribution requires component-level data).
- `metrics` — related/co-moving metric values for the same period (e.g., revenue when diagnosing expenses; utilization when diagnosing margin).
- `strategy` — the forecast assumption(s) underlying the metric (to test whether the miss is an assumption error).
- `risks` — the metric's warning-signal threshold, if it is a risk-linked metric.
- `decisions` — prior diagnoses of the same metric (to detect a recurring/systematic cause).

## Inputs
```yaml
input:
  metric: str                      # the metric that missed
  actual: number                   # REQUIRED
  forecast: number                 # REQUIRED (target/baseline being missed)
  period: {month, year}
  line_items: list                 # [{line, actual, forecast}] — the components of the metric (for attribution)
  related_metrics: list|null       # [{metric, actual, forecast, expected_relationship}] for co-movement check
  underlying_assumptions: list|null # forecast assumptions behind this metric
  risk_threshold: object|null       # {threshold, direction} if metric is risk-linked
  prior_diagnoses: list|null        # previous root-cause findings for this metric
  tolerance_band_pct: number        # below which the variance is noise, not diagnosed
```

## Missing Information Protocol
1. **Gate:** both actual and forecast for the metric are required; if either is missing, block with an incompleteness notice (do not diagnose a half-known variance).
2. If `line_items` are absent, attribution cannot be performed — request the breakdown or pull it from the accounting/source system; do not guess which line drove the miss.
3. If related metrics for the co-movement check are unavailable, perform the attribution but flag that the "real vs artifact" judgment is unconfirmed.
4. Never attribute a miss to a driver without line-item evidence, and never assume the cause from the metric name alone.

## Diagnostic Questions
- Is the variance outside the tolerance band (worth diagnosing) at all?
- Which line items contributed most to the variance, and in what direction (Top Movers)?
- Does the miss concentrate in one driver or spread across many?
- Do co-moving metrics confirm the variance is real, or reveal it as an artifact (e.g., low expenses because activity stalled)?
- Is the root cause an execution failure, a wrong assumption, an external/environment shift, or a data error?
- Has this metric missed for the same reason before (systematic, not one-off)?
- Which single lever best addresses the identified root cause?

## Analysis Framework
1. **Gate + materiality.** Confirm actual and forecast exist; confirm |variance %| exceeds tolerance (else return "within tolerance — no action").
2. **Attribute (Top Movers).** Decompose the metric into its line items; rank each by contribution to the total variance (line actual − line forecast). Report drivers until they explain the bulk of the miss. Note whether the miss is concentrated or diffuse.
3. **Interpret via co-movement.** Test the variance against related metrics and their expected relationship:
   - A favorable cost variance alongside a revenue shortfall → stalled activity, not efficiency.
   - A revenue miss alongside a healthy pipeline → conversion/delivery problem, not demand.
   - A margin miss alongside stable pricing → cost-side driver (input costs, utilization).
   - Confirm sign and magnitude line up with a genuine performance story before accepting the surface reading.
4. **Classify the root cause** into one of: execution failure, wrong assumption, external/environment shift, or data/recording error.
5. **Check for recurrence.** Compare to prior diagnoses; a repeat cause is systematic and escalates the recommended lever (e.g., re-forecast rather than one-off correction).
6. **Recommend the lever.** Map the root-cause class to the corrective lever (see Decision Rules), stating expected effect, effort, and whether it needs approval.

## Calculations
- **Total variance** = Actual − Forecast; **Variance %** = (Actual − Forecast)/Forecast × 100 (Forecast = 0 → "no comparison").
- **Line-item contribution** = (line Actual − line Forecast); **contribution share** = line contribution / total variance.
- **Concentration** = share of total variance explained by the single largest driver (high share → concentrated cause; low → diffuse).
- **Co-movement expectation:** for related metric R with expected relationship to M, compare observed direction/magnitude vs expected; a divergence flags an artifact or a broken assumption.
- **Recurrence count** = number of prior periods with the same root-cause class for this metric.

## Decision Rules
- IF actual OR forecast missing THEN block diagnosis and surface the data gap.
- IF |variance %| within tolerance THEN return "within tolerance — noise, no action."
- IF line_items are unavailable THEN return attribution as "cannot attribute — breakdown required" rather than guessing.
- IF one driver explains the majority of the variance THEN name it as the concentrated root cause and target the lever there.
- IF the variance is diffuse across many lines THEN treat as a systemic/assumption issue rather than a single line fix.
- IF a favorable variance co-moves adversely with a related activity metric (e.g., expenses down AND revenue down) THEN classify as an artifact of reduced activity, NOT a genuine gain, and recommend investigating activity.
- IF root cause = wrong assumption AND it has recurred (2+ periods) THEN recommend re-forecast (systematic), not execution correction.
- IF root cause = execution failure THEN recommend a targeted corrective action with owner and deadline.
- IF root cause = external/environment shift THEN recommend re-forecast + strategy review (not blaming execution).
- IF root cause = data/recording error THEN recommend correcting the source data and re-running, not acting on the false variance.
- IF the metric is risk-linked and crossed its threshold THEN flag the risk trip alongside the diagnosis and route to the risk owner.
- IF the recommended lever involves spend, pricing, or a public commitment THEN hold it for founder approval.

## Procedure
1. Run the gate and materiality check; exit early if within tolerance.
2. Decompose the metric into line items; compute contributions and rank Top Movers.
3. Run the co-movement check against related metrics; test each surface reading.
4. Classify the root cause; check recurrence against prior diagnoses.
5. Map root cause → corrective lever; estimate expected effect and effort; set approval flag.
6. Emit the diagnosis (L1) with attribution, co-movement interpretation, root-cause class, and the recommended lever.
7. On approval (if the lever needs it), write the diagnosis to `decisions` and any corrective task/metric note; otherwise return to `monthly-business-review` for loop integration.

## Output
```yaml
output:
  metric: str
  period: {month, year}
  variance: {amount, pct}
  materiality: enum(within_tolerance, material)
  attribution:
    top_movers: [ {line, actual, forecast, contribution, contribution_share} ]
    concentration: enum(concentrated, diffuse)
    largest_driver: str
  co_movement:
    checks: [ {related_metric, expected, observed, verdict: enum(confirms, contradicts)} ]
    interpretation: str            # e.g. "favorable cost variance is an activity artifact"
  root_cause:
    class: enum(execution_failure, wrong_assumption, external_shift, data_error)
    statement: str
    recurring: bool
  recommended_lever:
    lever: enum(correct_execution, reforecast, reprioritize, fix_data, strategy_review)
    action: str
    owner: str|null
    deadline: date|null
    expected_effect: str
    needs_approval: bool
  risk_trip: {risk, threshold, tripped: bool} | null
```

## Recommendations
The single recommended lever is chosen by root-cause class, not by which number moved: execution failures get targeted corrections; recurring wrong assumptions get re-forecasts; external shifts get strategy reviews; data errors get corrected and re-run before any action. The recommendation always leads with the evidence (Top Movers + co-movement verdict) so the founder sees why this lever and not another. A "favorable" variance never yields a celebratory recommendation until the co-movement check confirms it is real.

## Execution Opportunities
- Produce the attribution, co-movement interpretation, and root-cause diagnosis (reversible, LOW) — L1.
- Draft the corrective action / task with owner and deadline (reversible, LOW).
- Flag a data-recording error and open a correction task for the accounting source (reversible, LOW).
- Route a risk trip to its owner (reversible, LOW — internal notice).
- Draft a re-forecast note for a systematically-wrong assumption (reversible, LOW — draft only).

## Human Approval Requirements
- Any recommended lever involving budget/experiment spend, a pricing change, or a public commitment requires founder approval before execution.
- Committing a re-forecast as authoritative requires founder (+ CFO agent / accountant) approval.
- Correcting source accounting records requires approval (business-record change).
- Analysis, attribution, and drafting proceed at L1. Complies with AUTONOMY_AND_APPROVAL_MODEL.md.

## Escalation Conditions
- Line-item data is unavailable and cannot be obtained → founder/accounting (attribution impossible without it).
- Root cause is a tax/regulatory, contractual, or employee-specific issue → accountant / attorney / HR.
- A risk-linked metric tripped its threshold → the risk's contingency owner + founder.
- Root cause is genuinely ambiguous (evidence supports multiple causes) → surface the uncertainty with confidence levels; do not force a single cause.

## KPIs
- Attribution accuracy: does the corrective lever, once applied, move the metric as predicted next period?
- % of favorable variances correctly re-classified as artifacts by the co-movement check.
- % of diagnoses that named a concentrated driver vs "unknown."
- Recurrence detection rate (systematic causes caught before a third miss).

## Monitoring
After a corrective lever is applied, watch the metric and its co-moving related metrics next period to confirm the diagnosis was right and the fix worked. If the metric misses again for the same reason, escalate the root-cause class (one-off correction → systematic re-forecast or strategy review).

## Follow-Up
- Runs on demand and as a callee of `monthly-business-review` whenever a metric is flagged material.
- Re-run next period on the same metric to verify the corrective lever's effect.

## Related Skills
Called by `monthly-business-review` per flagged metric; consumes `executive-dashboard-builder` Top Movers and `kpi-design` thresholds; feeds `initiative-prioritization` (when the lever is re-sequencing) and `financial-forecast-builder` (when the lever is re-forecast); shares risk trips with the risk register.

## Guardrails
- Never attribute a miss to a driver without line-item evidence.
- Never accept a favorable surface reading before the co-movement check — the classic trap is reading lower expenses as savings when activity has stalled.
- Never diagnose a within-tolerance variance; that manufactures signal from noise.
- Handle Forecast = 0 as "no comparison," never as an infinite or 100% variance to be explained.
- Distinguish a data error from a real variance before recommending any operational action.
- A recommended lever that spends, re-prices, or commits externally is a proposal held for approval.

## Example
**Founder input:** "My gross margin came in at 48% against a 56% forecast this month — why, and what do I do?"

**Skill reasoning:**
- Gate: actual 48%, forecast 56% present. Variance −8 pts, well outside tolerance → material.
- Attribution (line items by service line): Line A margin held at 57%; Line B collapsed to 31% (its direct-cost line ran far over forecast). Line B contributes ~90% of the total margin miss → concentrated.
- Co-movement: pricing on Line B unchanged (revenue/unit stable) and revenue volume on plan → so this is not a pricing or demand problem; the driver is cost-side (a subcontractor/input cost on Line B ran over). Co-movement verdict: contradicts a "demand/pricing" story, confirms a cost driver.
- Root cause class = execution_failure (uncontrolled input cost on Line B), not wrong_assumption; check recurrence — first occurrence.
- Recommended lever = correct_execution: renegotiate/cap Line B input cost or re-price Line B; owner = founder; expected effect = restore Line B margin toward 55%. Because it may involve a pricing change, needs_approval = true.

**Output (abridged):** variance −8 pts (material); largest_driver = Line B direct cost, concentration = concentrated; co_movement interpretation = "cost-side driver, not pricing/demand"; root_cause = execution_failure (not recurring); recommended_lever = correct_execution (renegotiate input cost / re-price Line B), needs_approval = true.

**Executed vs. approval:** Attribution, co-movement analysis, and root-cause diagnosis produced at L1; a draft corrective task created. The pricing-change option and any renegotiation commitment held for founder approval.

## Provenance
SOURCE — derived from the Growth Execution domain knowledge (`09-growth-execution.md`): the DIAGNOSE-with-Top-Movers attribution step ("attribution before action"), the cost-variance co-movement interpretation nuance (favorable cost variance alongside a revenue shortfall = stalled activity, not savings), the variance formulas and divide-by-zero handling, and the adapt-lever decision rules. De-branded (generic service lines, no named vendors or company). See internal/PROVENANCE_MAP.md.
