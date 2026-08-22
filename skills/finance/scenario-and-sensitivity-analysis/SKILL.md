---
name: scenario-and-sensitivity-analysis
domain: finance
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [finance.forecasts, finance.income_statement, finance.balance_sheet, finance.position, company]
writes: [finance.forecasts, finance.sensitivity, decisions]
related_skills: [financial-forecast-builder, cash-runway-monitor, break-even-and-pricing-analysis, debt-service-and-covenant-analysis]
owned_by_agents: [cfo-agent, business-analyst-agent]
---

# Skill: Scenario & Sensitivity Analysis

## Purpose
Stress-test a financial forecast by (1) building coherent Base / Upside / Downside scenarios that flex bundles of interrelated assumptions together, and (2) running single-variable sensitivities to find the assumption the plan is most fragile to. Tells the founder how much room for error the plan has and where to watch hardest.

## When to Use
- "What if revenue growth doesn't materialize / a recession hits / costs spike?"
- "Which assumption breaks my plan if I'm wrong?"
- "Show me best case, worst case, and expected case."
- After `financial-forecast-builder` produces a base case, before committing to fundraising, budget, or a major bet.

## When NOT to Use
- No base forecast exists yet → build one with `financial-forecast-builder` first.
- The question is purely unit economics (break-even, contribution, price change) → `break-even-and-pricing-analysis`.
- Near-term cash-out risk specifically → `cash-runway-monitor`.
- Deciding whether to actually take the downside-mitigating financing → founder decision; this skill quantifies exposure, it does not execute financing.

## Required Context
- A complete base-case forecast (the model to flex). Read from `finance.forecasts`.
- The forecast's assumption set with each driver's source and plausibility range. Read from `finance.forecasts` assumptions log.
- Which outputs matter to the founder (revenue, net income, operating cash flow, funding needed, runway, covenant status). Read from `company` goals.

## Inputs
```yaml
input:
  base_forecast_ref: string               # pointer to the base model in finance.forecasts
  scenarios:                              # coherent assumption bundles
    - name: enum[base, upside, downside] | string
      assumption_overrides:               # each interrelated driver moved together
        revenue_growth_pct: number
        cogs_pct: number
        price_change_pct: number
        dso_days: number
        dio_days: number
        opex_change_pct: number
        churn_or_volume_pct: number
  sensitivities:                          # single-variable sweeps (all else held)
    - variable: string                    # e.g. "revenue_growth_pct"
      range: {low: number, high: number, step: number}
  output_metrics: list                    # e.g. [revenue, net_income, operating_cash_flow, funding_needed, runway_months, covenant_status]
  assumption_uncertainty:                 # optional, to rank fragility
    - {variable: string, plausible_range: {low, high}, confidence: enum[high, medium, low]}
  covenants: {current_ratio_min, tie_min, dscr_min}   # optional, to find breach points
```

## Missing Information Protocol
- If scenario bundles aren't specified, propose Base/Upside/Downside defaults derived from the assumption ranges (e.g., downside = revenue growth halved + prices pressured + COGS up + collections slower) and present them for founder confirmation before relying on results.
- If plausibility ranges are missing, ask the founder for realistic high/low bounds per key driver in ONE batch; do not invent ranges that drive a conclusion.
- Keep scenario bundles internally coherent — do not combine assumptions that cannot occur together (e.g., high volume with rising prices in a price-competitive downside). Flag any incoherent bundle the founder requests.
- If the base forecast is stale, re-run `financial-forecast-builder` first.

## Diagnostic Questions
1. What are the plausible interrelated futures (base/upside/downside), and how do the key outputs differ across them?
2. Which single assumption, if wrong, moves the outcome most (the fragile one)?
3. At what value of each variable does the plan break — hit a funding gap, breach a covenant, or run out of cash?
4. How much margin of safety does the base plan have before it turns unfinanceable?
5. Which fragile assumptions are also the most uncertain (highest risk = high impact × low confidence)?
6. What early indicator would tell us a downside is materializing?

## Analysis Framework
Two complementary methods, per source guidance that scenarios (coherent bundles) are preferred over single-variable sensitivity because real assumptions move together — but sensitivities isolate fragility.

- **Scenario analysis:** define Base/Upside/Downside as bundles of interrelated assumptions moved together; re-run the full three-statement model for each; compare Revenue, Net Income, Operating Cash Flow, and Funding Needed (plus runway and covenant status). The documented downside pattern to always test: forecast revenue growth fails because competition intensifies and prices are pressured.
- **Single-variable sensitivity:** hold all else fixed, sweep one variable across its range, and record the output response and any breakpoint (funding gap, covenant breach, out-of-cash). Rank variables by output elasticity (Δoutput / Δinput).
- **Fragility ranking:** combine sensitivity magnitude with assumption uncertainty (impact × (1 − confidence)) to surface the most-critical-and-most-uncertain assumptions — the ones to monitor and de-risk.
- **Breakpoint search:** for each critical variable, solve for the value at which the plan crosses a failure threshold (funding gap > 0, covenant < min, cash < 0).

## Calculations
- **Scenario output** = re-run `financial-forecast-builder` with each bundle's overrides; capture the output_metrics per scenario.
- **Sensitivity response** = output at each swept value of the variable, all else equal.
- **Elasticity (fragility magnitude)** = (%Δ output) / (%Δ input) for each variable, evaluated near the base point; higher |elasticity| = more fragile.
- **Fragility score** = |elasticity| × (1 − confidence_weight), where confidence_weight ∈ {high=0.9, medium=0.6, low=0.3}; rank descending.
- **Breakpoint** = the input value where a target output crosses its threshold (e.g., revenue growth% at which funding_needed first exceeds available financing, or current ratio first falls below covenant min).
- **Margin of safety on a variable** = (base value − breakpoint value) / base value × 100 (how far the assumption can move before the plan breaks).
- **Range of outcomes** = downside vs. upside spread for each key metric (a measure of plan risk).

## Decision Rules
- IF a downside scenario produces a funding gap the founder cannot cover → THEN flag it as a plan-breaking risk; recommend building the mitigation (extra financing runway, cost flex) BEFORE committing — financing itself needs approval.
- IF a single variable has high elasticity AND low confidence → THEN it is the plan's most fragile point; prioritize monitoring and de-risking it.
- IF a covenant is breached in the downside or at a plausible breakpoint → THEN hand to `debt-service-and-covenant-analysis` and warn the founder of the trigger value.
- IF the downside runs the business out of cash → THEN hand to `cash-runway-monitor` and surface the timing.
- IF the margin of safety on a critical variable is thin (small % move breaks the plan) → THEN recommend hedging (fixed-to-variable cost shifts, pre-arranged financing, diversifying the driver).
- IF a requested scenario bundle is internally incoherent → THEN flag it and propose a coherent version rather than reporting a misleading result.
- IF upside is large but requires assumptions well above history/benchmark → THEN label it aspirational, not a plan.

## Procedure
1. Load and validate the base forecast; confirm which output metrics matter.
2. Define/confirm Base/Upside/Downside bundles (coherent, interrelated moves), including the competition-pressures-price downside.
3. Re-run the full model per scenario; capture Revenue, Net Income, Operating CF, Funding Needed, runway, covenant status.
4. Run single-variable sensitivities across each variable's range; record responses and breakpoints.
5. Compute elasticity and fragility scores; rank the most-critical-and-most-uncertain assumptions.
6. Search breakpoints for each critical variable (funding gap, covenant, cash-out) and margins of safety.
7. Emit the scenario matrix, sensitivity/tornado ranking, fragile assumptions, breakpoints, and monitoring indicators; write to `finance.forecasts`/`finance.sensitivity` (L1); record in `decisions`.

## Output
```yaml
output:
  scenario_matrix:                        # per scenario
    - {scenario: string, revenue: number, net_income: number, operating_cash_flow: number, funding_needed: number, runway_months: number, covenant_status: string}
  sensitivity_ranking:                    # tornado order, most fragile first
    - {variable: string, elasticity: number, output_low: number, output_high: number}
  fragile_assumptions:                    # impact × uncertainty
    - {variable: string, fragility_score: number, confidence: enum[high, medium, low], why: string}
  breakpoints:
    - {variable: string, threshold: string, break_value: number, margin_of_safety_pct: number}
  outcome_range: {revenue: {low, high}, net_income: {low, high}, funding_needed: {low, high}}
  most_fragile_assumption: string
  monitoring_indicators: list             # early signals a downside is materializing
  recommendations: list
  handoffs: list
```

## Recommendations
Lead with the single most fragile assumption and how to de-risk it (monitor a leading indicator, pre-arrange contingency financing, shift fixed costs to variable, diversify the driver). Prioritize mitigations by the exposure they remove per unit of cost/effort and by reversibility. Present the downside funding need explicitly with lead time. Separate operational hedges (proceed as tasks) from financing contingencies (founder approval). Frame upside as opportunity, not plan.

## Execution Opportunities
- Write scenarios and sensitivity results to `finance.forecasts`/`finance.sensitivity` (reversible, LOW; L1; sensitivity kept confidential).
- Create monitoring tasks/alerts on the leading indicators of the fragile assumptions (reversible, LOW).
- Draft a risk-and-scenario summary for the founder / board (reversible, LOW; external sharing needs approval).
- Trigger `cash-runway-monitor` or `debt-service-and-covenant-analysis` when a downside breaches cash or covenants (reversible, LOW).

## Human Approval Requirements
- Building scenarios, running sensitivities, and interpreting them: always allowed.
- Arranging contingency financing, drawing debt, or any money movement to mitigate a downside: ALWAYS requires founder approval.
- Committing to budget changes or cost restructuring from a scenario: requires founder approval (budget commitment).
- Sharing scenario/sensitivity output externally: requires founder approval (sensitivity data is confidential).

## Escalation Conditions
- Downside produces an uncoverable funding gap or cash-out → founder + recommend accountant.
- Plausible breakpoint breaches a covenant → founder + `debt-service-and-covenant-analysis`.
- Assumption ranges depend on tax/entity/regulatory factors → accountant/CPA.
- Wide, low-confidence outcome range (plan is highly uncertain) → surface uncertainty to founder; recommend narrowing key assumptions before committing.

## KPIs
- Correct identification of the most fragile assumption (validated as actuals unfold).
- Breakpoints and downside funding needs surfaced with actionable lead time.
- Founder establishes monitoring/mitigation on flagged fragile assumptions.
- Actual outcomes fall within the modeled scenario range.

## Monitoring
- Track the leading indicators of fragile assumptions each period; alert on drift toward a breakpoint.
- Re-run scenarios as actuals update the base case.
- Watch whether the realized path is tracking base, upside, or downside.

## Follow-Up
- Re-run whenever the base forecast changes materially, and at each planning/fundraising cycle.
- Re-run if a monitored indicator crosses a warning level.

## Related Skills
- `financial-forecast-builder` (base model to flex).
- `cash-runway-monitor` (downside cash timing).
- `debt-service-and-covenant-analysis` (covenant breakpoints).
- `break-even-and-pricing-analysis` (price/volume fragility).

## Guardrails
- Scenario bundles must be internally coherent; never combine mutually exclusive assumptions.
- Sensitivity ranges must be plausible and founder-confirmed; do not manufacture ranges that force a conclusion.
- Label aspirational upside as such; the downside, not the upside, sizes the safety margin.
- Financing and budget mitigations require founder approval; tax/entity factors escalate to an accountant.
- Sensitivity output is confidential; audited writes to permitted namespaces only.

## Example
**Founder input:** "Stress-test my 3-year plan. Base is 20% revenue growth. What if growth is slower and prices get squeezed by competitors?"

**Skill reasoning:** Defines Downside = growth 8% + price −5% + COGS +2 pts + DSO +10 days; Base = 20%; Upside = 28% + prices flat. Re-runs the model: Base year-2 net income $210k, operating CF $150k, funding needed $140k (within revolver); Downside net income $60k, operating CF −$30k, funding needed $310k (exceeds the $200k revolver cap → $110k external gap); Upside net income $310k, no external gap. Single-variable sweep: revenue growth elasticity on funding needed is highest; the breakpoint where funding needed exceeds available financing is ~12% growth → margin of safety = (20 − 12)/20 = 40%. Fragility ranking: revenue growth (high impact, medium confidence) > price (high impact, low confidence — most fragile) > COGS%. Downside also pushes current ratio to 1.42 → covenant breach.

**Output:** scenario matrix, tornado ranking with price as most fragile, breakpoint at 12% growth (40% safety margin), downside $110k external funding gap and a covenant breach, monitoring indicators = weekly bookings growth and average selling price. Handoffs: `debt-service-and-covenant-analysis`, `cash-runway-monitor`.

**Executed vs. approval:** scenarios written (sensitivity confidential), monitoring alerts on bookings/ASP created, board-risk summary drafted (L1); any contingency financing or cost restructuring held for founder approval.

## Provenance
SOURCE. Derives from the Statements & Ratios knowledge (scenario analysis of interrelated assumption bundles; base/downside/upside comparison of Revenue/NI/OCF/Funding-Needed; identifying most-critical and most-uncertain assumptions) and the Forecasting/Cash knowledge (sensitivity analysis, the competition-pressures-price downside, scenario diagnostics). Branding stripped and generalized per PROVENANCE_MAP.
