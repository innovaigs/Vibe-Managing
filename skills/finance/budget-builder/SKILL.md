---
name: budget-builder
domain: finance
version: 0.1.0
autonomy_ceiling: L1
provenance: SYNTH
reads: [finance.forecasts, finance.income_statement, finance.position, finance.budgets, company, offerings]
writes: [finance.budgets, decisions]
related_skills: [financial-forecast-builder, scenario-and-sensitivity-analysis, cash-runway-monitor, financial-ratio-analysis]
owned_by_agents: [cfo-agent, business-analyst-agent]
---

# Skill: Budget Builder

## Purpose
Turn the founder's goals and the driver-based forecast into a concrete operating budget by line and period, then track actuals against it with variance analysis — so spending stays aligned with the plan and cash, and drift is caught early. Bridges the forecast (what should happen financially) to operational commitments (what each area is allowed to spend).

## When to Use
- "Build me an operating budget for next year / quarter."
- "How much can each area spend and stay on plan?"
- "Track my actuals vs. budget and tell me where I'm off."
- Start of a fiscal period, after a forecast is built, or when spend needs a control framework.

## When NOT to Use
- No forecast/goals exist yet → build the forecast with `financial-forecast-builder` first.
- Stress-testing the plan → `scenario-and-sensitivity-analysis`.
- Near-term cash-out risk → `cash-runway-monitor`.
- Approving or committing the budget / authorizing spend → founder decision; this skill drafts and tracks, it does not commit funds.

## Required Context
- The base forecast (revenue and cost drivers by period). Read from `finance.forecasts`.
- Founder goals/priorities for the period (growth targets, hiring plans, investments). Read from `company`.
- Prior-period actuals for baselining and variance. Read from `finance.income_statement`, `finance.budgets`.
- Cash position and minimum-cash cushion (budget must respect runway). Read from `finance.position`.

## Inputs
```yaml
input:
  mode: enum[build_budget, track_variance, reforecast]
  period_type: enum[monthly, quarterly, annual]
  horizon: string                          # e.g. "FY2027" or "2027-Q1..Q4"
  forecast_ref: string                     # base forecast from finance.forecasts
  goals: list                              # founder priorities the budget must fund
  budget_lines:                            # target lines (from forecast + goals)
    - {line: string, category: enum[revenue, cogs, opex, capex], method: enum[fixed, pct_of_revenue, growth, per_headcount], value: number}
  cash_constraint: {min_cash_balance: number, available_cash: number}
  actuals:                                 # for track_variance mode
    - {period: string, line: string, budget: number, actual: number}
  variance_thresholds: {favorable_pct: number, warning_pct: number, critical_pct: number}  # e.g. 5/10/20
```

## Missing Information Protocol
- If `budget_lines` are not provided, derive them from the forecast's assumption set and the founder's goals, and present the draft for confirmation before treating it as the budget.
- If goals conflict with the cash constraint (the plan spends below minimum cash), do not silently trim — surface the conflict and the trade-offs for the founder.
- If prior actuals are missing for a line, baseline off the forecast and note it.
- If variance thresholds are unset, default to favorable/warning/critical at 5%/10%/20% and state the default.
- Never commit or authorize any spend; the budget is a plan until the founder approves it.

## Diagnostic Questions
1. What must the budget fund to hit the founder's goals, and does the forecast support it?
2. Does the budget respect the minimum-cash cushion and runway in every period?
3. Which lines are fixed, which scale with revenue, and which scale with headcount?
4. Where are actuals diverging from budget, and is the variance favorable, warning, or critical?
5. Is a variance a timing difference (will reverse) or a run-rate change (needs reforecast)?
6. Does cumulative variance threaten the annual plan or the cash position?

## Analysis Framework
Build top-down from the forecast and goals, reconcile to cash, then run variance analysis on actuals.

- **Budget construction:** for each line, apply its method — fixed $, % of revenue, growth series, or per-headcount — tied to the forecast's revenue and driver path. Sum to a budgeted P&L by period; roll capex separately.
- **Cash reconciliation:** confirm the budget keeps projected cash above the minimum-cash balance every period (pull from the forecast's cash plug); if not, flag and iterate.
- **Goal alignment:** each founder goal maps to the line(s) that fund it; unfunded goals are surfaced explicitly.
- **Variance analysis:** for each line and period, compute budget-vs-actual variance ($ and %), classify favorable/warning/critical, and label each as timing vs. run-rate.
- **Reforecast trigger:** persistent run-rate variances flow back to `financial-forecast-builder` to update the plan.

## Calculations
- **Line budget (fixed)** = value. **(% of revenue)** = pct × budgeted revenue. **(growth)** = prior × (1 + g). **(per headcount)** = per-head cost × planned headcount.
- **Budgeted operating profit** = Budgeted revenue − budgeted COGS − budgeted opex.
- **Variance ($)** = Actual − Budget. For costs, positive = over budget (unfavorable); for revenue, positive = above budget (favorable). Report favorability by category, not just sign.
- **Variance (%)** = (Actual − Budget) / Budget × 100.
- **Cumulative (YTD) variance** = Σ(Actual − Budget) across elapsed periods.
- **Run-rate projection** = annualized actual run-rate vs. annual budget (to test whether the year is on track).
- **Cash-headroom check** = projected cash each period − minimum cash balance (must stay ≥ 0).

**Variance classification (default thresholds):** |variance%| ≤ 5% on-plan · 5–10% (unfavorable direction) warning · 10–20% investigate · > 20% critical. Favorable variances beyond threshold are also flagged (may signal an unrealistic budget or a missed opportunity).

## Decision Rules
- IF a proposed budget drives projected cash below the minimum-cash balance in any period → THEN it is infeasible; surface the shortfall and required trims/financing (financing needs approval).
- IF a founder goal is unfunded by the forecast-supported budget → THEN flag it and present the trade-off (cut elsewhere, extend runway, or drop the goal).
- IF a cost line's variance is unfavorable and > warning threshold → THEN investigate; create a task and ask whether it is timing or a run-rate change.
- IF a variance is a run-rate change (not timing) → THEN trigger a reforecast (`financial-forecast-builder`) and reassess cash/runway.
- IF revenue is materially below budget → THEN check cash impact and hand to `cash-runway-monitor`; consider scaling variable costs down.
- IF a large favorable variance persists → THEN the budget may be unrealistic or an opportunity is being missed; recommend rebasing.
- IF cumulative YTD variance threatens the annual plan or cash → THEN escalate to the founder with corrective options.

## Procedure
1. Load the forecast, goals, prior actuals, and cash constraint.
2. Build each budget line by its method; sum to a budgeted P&L by period; roll capex.
3. Reconcile to cash: confirm every period stays above minimum cash; iterate or flag if not.
4. Map goals to funding lines; surface any unfunded goals.
5. Present the draft budget for founder confirmation (it is a plan, not a commitment).
6. **track_variance:** ingest actuals, compute line/period and YTD variances, classify, label timing vs. run-rate.
7. **reforecast:** feed run-rate variances back to `financial-forecast-builder`.
8. Emit the budget and/or variance report; write to `finance.budgets` (L1 staged, approved_by set on founder confirmation); record in `decisions`.

## Output
```yaml
output:
  mode: enum[build_budget, track_variance, reforecast]
  horizon: string
  budget:
    - {period: string, line: string, category: string, amount: number, method: string, funds_goal: string}
  budgeted_pnl: list                       # per period: revenue, cogs, opex, operating_profit
  cash_headroom: list                      # per period: projected_cash minus min_cash (must be >= 0)
  unfunded_goals: list
  variance_report:                         # track_variance mode
    - {period: string, line: string, budget: number, actual: number, variance_abs: number, variance_pct: number, status: enum[on_plan, favorable, warning, critical], type: enum[timing, run_rate]}
  ytd_variance: list
  reforecast_triggered: boolean
  narrative: string
  handoffs: list
```

## Recommendations
Prioritize by cash impact and plan risk: fund the highest-priority goals first within the cash constraint; where the budget is infeasible, recommend the lowest-pain trims (defer discretionary spend, scale variable costs) before proposing financing (founder-approved). In variance mode, rank investigations by variance size and run-rate persistence; recommend reforecast when run-rate changes are confirmed. Always distinguish planning (proceed as draft) from committing spend (founder approval).

## Execution Opportunities
- Write the draft budget to `finance.budgets` (reversible, LOW; L1 staged, approved_by empty until founder confirms).
- Build a budget-vs-actual dashboard and variance report (reversible, LOW).
- Create investigation tasks for warning/critical variances (reversible, LOW).
- Trigger `financial-forecast-builder` reforecast on confirmed run-rate variances (reversible, LOW).
- Alert `cash-runway-monitor` when revenue shortfall threatens runway (reversible, LOW).

## Human Approval Requirements
- Building the draft budget and running variance analysis: always allowed.
- Committing/approving the budget as binding spend authority: ALWAYS requires founder approval (budget commitment) — sets `approved_by`.
- Authorizing any specific spend, capex, or hire within the budget: requires founder approval (routes to the owning agent).
- Any financing to make the budget feasible: ALWAYS requires founder approval.

## Escalation Conditions
- Budget infeasible within cash/runway and goals cannot all be funded → founder (prioritization decision).
- Confirmed run-rate overspend threatening the annual plan or cash → founder + `cash-runway-monitor`.
- Variance rooted in a tax/accounting classification question → accountant/CPA.
- Goal-vs-cash conflict the founder must resolve → founder.

## KPIs
- Budget adherence: % of lines within on-plan threshold.
- Variance detection lead time (caught before cumulative impact is material).
- Cash headroom maintained ≥ 0 every period.
- Reforecast triggered promptly on confirmed run-rate changes.
- Founder goals funded vs. planned.

## Monitoring
- Track line and YTD variances each period; watch for cumulative drift.
- Monitor cash headroom against the minimum-cash cushion.
- Watch for recurring warning variances that indicate a stale budget.

## Follow-Up
- Build at the start of each fiscal period; variance-track every close.
- Reforecast when run-rate variances persist or the base forecast changes.

## Related Skills
- `financial-forecast-builder` (source of the budget and the reforecast target).
- `scenario-and-sensitivity-analysis` (budget under downside).
- `cash-runway-monitor` (cash impact of variances).
- `financial-ratio-analysis` (budgeted vs. actual margins).

## Guardrails
- A budget is a plan until the founder approves it; never treat a draft as spend authority or authorize spend autonomously.
- Never trim goals silently to fit cash — surface the trade-off for founder decision.
- Distinguish timing from run-rate variances before triggering a reforecast or corrective action.
- Financing and specific spend commitments require founder approval; classification questions escalate to an accountant.
- Confidential financial data; audited writes to `finance.budgets` (approved_by recorded on confirmation).

## Example
**Founder input:** "Build my FY2027 quarterly budget from the forecast. Goals: hire one salesperson in Q2 and spend $40k on a marketing push in Q3. Keep at least $50k cash at all times." Forecast: revenue $2.4M (20% growth), COGS 59%, G&A $220k, base S&M $240k + 5% of revenue.

**Skill reasoning:** Builds lines: COGS 59% of quarterly revenue; S&M = $60k/qtr + 5% of revenue; G&A $55k/qtr; adds the salesperson (~$25k/qtr fully loaded) from Q2 and the $40k marketing in Q3. Sums to a budgeted quarterly P&L. Cash reconciliation from the forecast's plug: Q3 dips to $46k projected cash — below the $50k minimum → flag. Trade-off surfaced: move the marketing push to Q4, or trim it to $30k, or accept a small revolver draw. The salesperson goal and marketing goal are both mapped to funding lines; no goal is unfunded, but Q3 timing breaches the cushion.

**Output:** draft quarterly budget, budgeted P&L, cash headroom by quarter (Q3 headroom −$4k flagged), recommendation to shift $10k of the Q3 push to Q4 to preserve the cushion. Handoff: `cash-runway-monitor` (confirm Q3 cash), `financial-forecast-builder` if timing changes.

**Executed vs. approval:** draft budget written to `finance.budgets` (approved_by empty), dashboard and the Q3-cushion flag created (L1); approving the budget, the Q2 hire, and the marketing spend held for founder approval.

## Provenance
SYNTH. Synthesized from the Statements & Ratios knowledge (dashboard/metric goal-setting, funding-shortfall levers) and the Forecasting/Cash knowledge (driver-based forecast lines, minimum-cash cushion, working-capital and cost drivers), extended with standard operating-budget and budget-vs-actual variance practice. No single source defines a budgeting method verbatim; the variance thresholds and construction methods are synthesized and should be tuned per business. Branding stripped and generalized per PROVENANCE_MAP.
