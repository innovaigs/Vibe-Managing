---
name: pipeline-and-forecast-review
domain: sales
version: 0.1.0
autonomy_ceiling: L1
provenance: SYNTH
reads: [sales, pipeline, deals, offerings, metrics, goals, customers, team]
writes: [metrics, forecasts, decisions, tasks]
related_skills: [sales-process-design, proposal-builder, negotiation-preparation, business-health-diagnostic, cash-flow-diagnostic, build-marketing-funnel-plan]
owned_by_agents: [orchestrator, sales-agent]
---

# Skill: Pipeline & Forecast Review

## Purpose
Give the founder an honest read on whether they will hit their number: diagnose pipeline coverage and stage-by-stage conversion, produce a weighted bookings forecast, and name the specific gaps (too little pipeline, a leaking stage, stalled deals, over-optimistic dates) with the actions that close them. It converts a list of open deals into a defensible number and a to-do list.

## When to Use
- Recurring cadence: weekly/monthly pipeline review, month-end or quarter-end forecast.
- The founder asks "Will I hit my target?", "How's my pipeline looking?", "What's my forecast?", "Which deals are real?"
- Before a cash decision that depends on incoming bookings (hiring, spend, runway calls).
- After a period of missed or lumpy revenue, to find where the pipeline leaks.
- Example founder phrasings: "Review my pipeline," "Am I going to make quota?", "Build me a forecast," "Why do my deals keep slipping?"

## When NOT to Use
- No defined pipeline/stages exist yet → run `sales-process-design` first; there is nothing to review without stages and exit criteria.
- The founder wants to design or redesign the process (stages, exit criteria) → `sales-process-design`.
- The question is a single deal's proposal or negotiation → `proposal-builder` / `negotiation-preparation`.
- The founder wants a whole-company scan (cash, ops, people, not just sales) → `business-health-diagnostic`.

## Required Context
Reads Business Memory: `sales` (the process definition: stages, exit criteria, target conversion rates, SLAs from `sales-process-design`), `pipeline`/`deals` (each open deal with stage, value, expected close date, age-in-stage, owner, last activity), `offerings` (deal value / margin context), `metrics` (historical win rate, cycle time, and prior forecast accuracy), `goals` (the revenue/bookings target and horizon), `customers` (for concentration risk), `team` (seller capacity). Every deal and metric carries `source`, `confidence`, `as_of`; stale `last_activity` and unmoved `expected_close_date` are themselves diagnostic signals.

## Inputs
```yaml
input:
  as_of_date: date
  period:
    target_bookings: number           # the number to hit
    period_start: date
    period_end: date
  process:                            # from sales-process-design
    stages: [ {name: str, order: int, target_conversion_to_next_pct: number, sla_days: int} ]
    overall_win_rate_pct: number      # observed if available, else target
    avg_cycle_days: int
  open_deals:
    - id: str
      account: str                    # generalized ("the counterparty" if sensitive)
      stage: str
      value: number
      gross_margin_pct: number
      expected_close_date: date
      age_in_stage_days: int
      last_activity_date: date
      owner: str
      decision_maker_engaged: bool
      commit_category: enum(commit, best_case, pipeline, omitted)  # rep's call, optional
  closed_history:                     # trailing window, to compute observed rates
    - id: str
      stage_reached: str
      outcome: enum(won, lost, disqualified)
      value: number
      cycle_days: int
      close_date: date
  forecast_history:                   # optional, to score forecast accuracy
    - period_end: date
      forecasted: number
      actual: number
```

## Missing Information Protocol
1. Compute observed conversion and win rate from `closed_history` before using target rates; prefer real data.
2. If `closed_history` is too thin (< ~10 closed deals) for stable rates, fall back to the process's target rates and label the forecast `low-confidence / assumed rates`.
3. If a deal lacks `expected_close_date` or `stage`, it cannot be forecast — list it under data gaps, do not silently drop or guess it.
4. Batch at most one concise question set for the highest-leverage gaps (typically: target number, period dates, missing close dates on large deals).
5. Never fabricate a deal's value, stage, or close date, and never upgrade a deal's likelihood beyond what its stage/evidence supports. A padded forecast is worse than an honest low one.

## Diagnostic Questions
Answered internally:
- **Coverage:** Is there enough open pipeline value to hit the target given the win rate? (Coverage ratio.)
- **Conversion:** Which stage transition converts worst vs. its target? Where does the pipeline leak?
- **Weighted forecast:** Applying stage probabilities, how much is realistically expected to close this period?
- **Aging/stall:** Which deals have exceeded their stage SLA or gone quiet (no recent activity)? Stalled deals are the #1 source of forecast error.
- **Date realism:** Are expected close dates inside the period credible given cycle time, or are they optimistic pull-ins?
- **Concentration:** Does one deal or one account dominate the forecast (single-deal risk)?
- **Qualification integrity:** Are advanced-stage deals actually qualified (decision-maker engaged, budget confirmed), or is the pipeline inflated?
- **Accuracy:** How did prior forecasts compare to actuals (bias — do we over- or under-forecast)?

## Analysis Framework
Five-lens review, then a single forecast with a confidence band:

1. **Coverage lens** — total open pipeline ÷ target vs. the coverage multiple the win rate demands.
2. **Conversion lens** — observed stage conversion vs. target; rank leaks by lost-value.
3. **Weighted forecast lens** — probability-weight each deal by stage, then reconcile against a category (commit/best-case) view.
4. **Hygiene lens** — flag stalled (age > SLA), quiet (no recent activity), date-slipping, and unqualified-but-advanced deals.
5. **Risk lens** — concentration (single deal/account share of forecast), and forecast bias from history.

Findings are ranked by impact on hitting the number (gap-to-target closed) × confidence.

## Calculations
Let target `T`, open pipeline value `P`, observed win rate `w`.

- **Pipeline coverage ratio** = `P ÷ T`. Health depends on win rate: needed coverage ≈ `1 ÷ w`. Healthy if coverage ≥ needed (e.g., w=25% → need 4×; w=33% → need 3×). Needs-Attention within 20% below; At-Risk below that; Critical < 2×. [SYNTH]
- **Stage conversion (observed)** = deals advancing past stage ÷ deals that entered stage, from `closed_history`. [CLAUDE-DERIVED]
- **Overall win rate (observed)** = won ÷ (won + lost) over the window (exclude disqualified from the denominator so loose qualification doesn't distort it). [SYNTH]
- **Weighted (expected-value) forecast** = Σ over open deals of `value × stage_probability`, counting only deals with `expected_close_date` in the period. Stage probability = observed historical conversion from that stage to Won. [SYNTH]
- **Default stage probabilities (fallback bands, replace with observed):** Discovery/Qualify 10–20%; Solution/Demo 25–40%; Proposal 40–60%; Negotiation 65–85%; Verbal/Commit 90%; Won 100%; Lost 0%. [CLAUDE-DERIVED]
- **Category forecast** = `Σ commit + (factor × Σ best_case)`, factor ~0.5 (tunable from history). Reconcile against the weighted forecast; large divergence = a rep-optimism or staging problem. [SYNTH]
- **Gap to target** = `T − forecast`. **Coverage to close the gap** = `gap ÷ w` = additional qualified pipeline needed. [SYNTH]
- **Deals needed** = `gap ÷ (avg_deal_value × w)`. [CLAUDE-DERIVED]
- **Stall flag:** `age_in_stage_days > stage_sla_days` OR `days_since_last_activity > (cycle_days ÷ n_stages)`. [SYNTH]
- **Slip risk:** `expected_close_date − as_of_date < (remaining stages × avg_days_per_stage)` → date is likely too soon; discount or push. [SYNTH]
- **Concentration** = largest single deal ÷ weighted forecast. Flag if > 25% (single-deal dependency). [CLAUDE-DERIVED]
- **Forecast accuracy / bias** = `mean(forecasted − actual)` over `forecast_history`; positive = chronic over-forecasting → apply a haircut. [SYNTH]
- **Weighted margin forecast** = Σ `value × margin% × stage_probability` (bookings vs. gross profit for cash-planning handoff). [CLAUDE-DERIVED]

## Decision Rules
- **IF** coverage ratio < needed (1÷w) **THEN** Coverage = At-Risk/Critical; primary action is top-of-funnel (route to `build-marketing-funnel-plan` / `select-channels`) — more leads, not more optimism.
- **IF** a stage's observed conversion is materially below its target **THEN** that is the leak; route to `sales-process-design` (tighten exit criteria) or enablement, and quantify lost value.
- **IF** a deal's `age_in_stage_days` > SLA OR no activity within the stall window **THEN** flag stalled; either re-engage with a next step or move to Lost/Disqualified — do NOT keep it inflating the forecast.
- **IF** `expected_close_date` is sooner than remaining-stage cycle time allows **THEN** discount the deal or push its date; flag as slip risk.
- **IF** an advanced-stage deal has `decision_maker_engaged = false` **THEN** downgrade its stage/probability — it is not truly qualified regardless of category.
- **IF** category forecast ≫ weighted forecast **THEN** rep optimism or mis-staging; trust the weighted view and flag the divergence.
- **IF** one deal/account > 25% of the forecast **THEN** flag concentration risk; do not treat the number as safe.
- **IF** forecast_history shows chronic over-forecasting **THEN** apply the historical bias haircut to the committed number.
- **IF** closed_history < ~10 deals **THEN** use target rates, label forecast low-confidence, and prioritize collecting data.
- **IF** gap to target cannot be closed within the period by existing pipeline (cycle time > remaining days) **THEN** it is a NEXT-period problem; tell the founder the current period is largely locked and shift focus to pipeline creation.
- **IF** forecast shorts a cash need **THEN** hand the weighted margin forecast to `cash-flow-diagnostic` and flag runway impact.

## Procedure
1. Load process definition, open deals, closed history, target, and prior forecast accuracy from memory.
2. Compute observed stage conversion and win rate from `closed_history`; if too thin, fall back to target rates and set low-confidence.
3. Coverage lens: total open pipeline ÷ target vs. needed multiple.
4. Conversion lens: compare observed vs. target per stage; rank leaks by lost value.
5. Hygiene lens: flag stalled, quiet, slip-risk, and unqualified-but-advanced deals; recommend re-engage or remove.
6. Build the weighted forecast (deals closing in-period × stage probability); build the category forecast; reconcile; apply historical bias haircut.
7. Risk lens: concentration and bias.
8. Compute gap to target, additional pipeline/deals needed, and whether the gap is a this-period or next-period problem.
9. Rank findings by gap-closed × confidence; map each to a next action/skill.
10. Assemble output; write the forecast + snapshot to `forecasts`/`metrics`, a decision record to `decisions`, and draft follow-up tasks (re-engage stalled deals, chase missing close dates) at L1 for founder approval. Never send anything to a customer.

## Output
```yaml
output:
  as_of_date: date
  period: {start: date, end: date, target_bookings: number}
  coverage:
    open_pipeline_value: number
    coverage_ratio: number
    needed_ratio: number
    status: enum(Healthy, Needs-Attention, At-Risk, Critical)
  conversion:
    - transition: str
      observed_pct: number
      target_pct: number
      leak_value: number              # value lost to below-target conversion
      status: enum(Healthy, Needs-Attention, At-Risk, Critical)
    overall_win_rate_pct: number
    basis: enum(observed, target_assumed)
  forecast:
    weighted_forecast: number
    category_forecast: number
    reconciliation_note: str
    bias_haircut_applied_pct: number
    committed_number: number          # the honest call
    weighted_margin_forecast: number  # gross profit, for cash handoff
    confidence: enum(high, medium, low)
  gap:
    gap_to_target: number
    additional_pipeline_needed: number
    additional_deals_needed: number
    closable_this_period: bool
  hygiene_flags:
    - deal_id: str
      flag: enum(stalled, quiet, slip_risk, unqualified_advanced)
      detail: str
      recommended_action: enum(re_engage, push_date, downgrade, disqualify)
  risk:
    concentration_pct: number
    concentration_note: str
    forecast_bias_note: str
  ranked_findings:
    - rank: int
      finding: str
      gap_closed_if_fixed: number
      recommended_skill_or_action: str
  data_gaps: [ {deal_id: str, missing: str} ]
```

## Recommendations
Findings are ranked by how much of the gap-to-target they close, weighted by confidence. The order is deliberate: first fix pipeline HYGIENE (stalled/unqualified deals distort everything downstream), then address the worst-converting STAGE (leak), then COVERAGE (feed the top of funnel) if the math shows a structural shortfall. Each recommendation names the exact action or next skill and its quantified impact. This skill diagnoses and forecasts; it proposes actions but does not execute customer-facing moves.

## Execution Opportunities
- Write the forecast and pipeline snapshot to `forecasts`/`metrics` — reversible, LOW (prepared at L1 ceiling).
- Draft internal follow-up tasks: re-engage each stalled deal (with a suggested internal next step), chase missing close dates, review mis-staged deals — reversible, LOW.
- Draft an internal forecast briefing for the founder — reversible, LOW.
- Draft (never send) re-engagement outreach for stalled deals for the founder to review — the draft is LOW/reversible; SENDING is external and gated.
- Schedule the next review as an internal reminder — reversible, LOW.

## Human Approval Requirements
- No customer-facing action is executed. Any re-engagement message drafted for a stalled deal is an EXTERNAL communication and must be founder-approved before sending — per `AUTONOMY_AND_APPROVAL_MODEL.md`, external customer communications ALWAYS require founder approval.
- Committing pricing/terms, sending proposals/quotes, or signing contracts implied by a deal in the pipeline are gated to the founder in their own skills; this review only reports on them.
- Moving a deal to Closed-Won/Lost in a live CRM (a business record change) is prepared, not auto-executed, and shown to the founder.

## Escalation Conditions
- **Forecast materially below target with the period largely locked** (cycle time > remaining days) → escalate to founder now; current period cannot be saved by selling harder, only by pipeline creation for next period.
- **Weighted forecast shorts a known cash need** → founder + `cash-flow-diagnostic` (runway impact).
- **Coverage Critical (< 2×)** → founder + route to demand-gen skills.
- **Concentration risk** (one deal > 25% of forecast) → surface explicitly; do not present the number as safe.
- **Pervasive low-confidence data** (thin history, missing close dates) → present ranges, not a single false-precise number; prioritize data collection.

## KPIs
This skill's success:
- Forecast accuracy: |forecast − actual| ÷ actual, trending down over successive reviews.
- Forecast bias: mean(forecast − actual) trending toward zero.
- Stall reduction: % of deals within SLA improving cycle over cycle.
- Coverage discipline: coverage ratio held at or above the needed multiple.
- Action follow-through: % of recommended follow-ups the founder completes before the next review.

## Monitoring
After the review: track whether flagged stalled deals were re-engaged or removed, whether the committed number holds as deals close, and whether the identified stage leak improves. Compare this forecast to actuals at period end and feed the bias back into the next run. Watch for repeated slipping of the same deal (a sign it should be Lost/Disqualified).

## Follow-Up
- Time-triggered: weekly for fast/short-cycle sales, monthly for longer cycles; a fuller forecast at each period-end.
- Event-triggered: a large deal changing stage, a deal closing (update rates), a target reset, or a cash decision that depends on bookings.

## Related Skills
Depends on `sales-process-design` (stages, exit criteria, rates). Routes to `build-marketing-funnel-plan`/`select-channels` (coverage gaps), `proposal-builder` and `negotiation-preparation` (specific advancing deals), `cash-flow-diagnostic` (forecast → runway), and feeds `business-health-diagnostic` (sales dimension).

## Guardrails
- Never pad the forecast; the honest committed number, with its confidence band, is the deliverable — an inflated number destroys cash planning.
- Prefer observed conversion over target rates; when using target rates, label the forecast low-confidence explicitly.
- Never fabricate a deal's value, stage, or close date; unknowns go to data gaps.
- Do not silently promote a deal's probability beyond its stage evidence (especially with no decision-maker engaged).
- Any re-engagement drafted is internal until founder-approved; this skill never contacts customers.
- Generalize sensitive account names in shared artifacts ("the counterparty") unless the founder consents to naming.

## Example
**Founder input (month-end):** "Target is $150k in bookings this quarter, one month left. Here's my pipeline — will I make it?"
**Data:** Open pipeline = $520k across 14 deals. Observed win rate (last 30 closed) = 25% → needed coverage 4×; $520k / $150k = 3.5× → slightly under. Weighted forecast (deals with close date in-period × stage prob) = $96k. Category view: commit $70k + 0.5×best_case $60k = $100k — roughly reconciles. Two Proposal-stage deals ($40k, $28k) have no activity in 21 days (SLA 7) → stalled. One Negotiation deal ($55k) has expected close in 5 days but decision-maker never engaged → downgrade. Largest deal = $55k = 57% of weighted forecast → concentration risk. Forecast history shows +12% chronic over-forecasting → apply haircut.
**Reasoning:** Committed number after haircut ≈ $96k × 0.88 ≈ $85k, band $70k–$100k. Gap to target = ~$54–65k. Cycle time ~45 days > 30 days remaining → the gap is largely a NEXT-quarter problem; this quarter is mostly locked. Biggest recoverable value is the two stalled Proposal deals ($68k) if re-engaged.
**Output (abridged):** Coverage At-Risk (3.5× vs. 4× needed). Committed forecast $85k (medium-low confidence), vs. $150k target → gap ~$65k, NOT fully closable this quarter. Findings ranked: (1) Re-engage two stalled Proposal deals ($68k at stake) — draft internal follow-ups; (2) Downgrade the unqualified Negotiation deal (no decision-maker) — remove $55k of false comfort; (3) Concentration risk on the $55k deal — don't bank on it; (4) Coverage gap → route to `select-channels` for next-quarter pipeline. Handed weighted margin forecast to `cash-flow-diagnostic`.
**Executed vs. approval:** Wrote forecast + snapshot to `forecasts`/`metrics`, drafted internal re-engagement notes and CRM re-stage tasks at L1. No customer contacted; any outreach held for founder approval.

## Provenance
SYNTH. Restructures the SOURCE-DERIVED buyer's-journey / marketing-funnel stages (Awareness→Retention; B2B/B2G Product-Spec + RFP) and the funnel-leak diagnostics from the Marketing & Customer domain into a runnable coverage-and-conversion review, combined with CLAUDE-DERIVED sales-forecasting mechanics (weighted expected-value forecast, coverage ratio 1÷win-rate, stage probabilities, bias haircut, concentration flag). Numeric probability bands and coverage multiples are CLAUDE-DERIVED planning defaults to be replaced by the business's observed data. See `internal/PROVENANCE_MAP.md`.
