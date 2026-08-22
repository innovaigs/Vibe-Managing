---
name: break-even-and-pricing-analysis
domain: finance
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [finance.income_statement, finance.position, offerings, company, customers]
writes: [finance.position, decisions]
related_skills: [financial-forecast-builder, scenario-and-sensitivity-analysis, working-capital-optimizer, financial-ratio-analysis]
owned_by_agents: [cfo-agent, business-analyst-agent]
---

# Skill: Break-Even & Pricing Analysis

## Purpose
Compute contribution margin, break-even volume and revenue, and the margin of safety, and test how sensitive break-even and profit are to price and cost changes — so the founder knows the minimum volume to survive, how much cushion exists, and what a price or cost move does to the bottom line. Also sizes the go/no-go economics of a new line or expansion (with ROI and payback).

## When to Use
- "How many units/orders do I need to sell to break even?"
- "Can I afford to cut/raise prices — what does it do to break-even and profit?"
- "What's my contribution margin / margin of safety?"
- "Is this new product line/expansion worth it (ROI, payback)?"
- Pricing decisions, launch decisions, and cost-structure changes.

## When NOT to Use
- Full multi-year linked forecast → `financial-forecast-builder`.
- Stress-testing a whole plan across scenarios → `scenario-and-sensitivity-analysis`.
- Freeing cash from the working-capital cycle → `working-capital-optimizer`.
- Setting a final price to customers (external commitment) → founder approval; this skill informs the price, it does not publish it.

## Required Context
- Price per unit (or average bill/order) and variable cost per unit (or COGS%). Read from `offerings`.
- Fixed costs for the period (rent, salaries, other overhead). Read from `finance.income_statement`.
- For an opportunity: capex and incremental working capital, and a volume ramp. Read from `offerings`, `finance.working_capital`.
- Current/forecast volume for margin-of-safety context. Read from `finance.position`, `offerings`.

## Inputs
```yaml
input:
  mode: enum[break_even, price_sensitivity, cost_sensitivity, opportunity_go_no_go]
  price_per_unit: number                  # or average bill/order
  variable_cost_per_unit: number          # OR provide cogs_pct
  cogs_pct: number                        # alternative to variable_cost_per_unit
  fixed_costs_period: number              # fixed costs for the relevant period
  period_label: string                    # e.g. "quarter", "year"
  current_or_forecast_volume: number      # units for margin of safety
  price_change_scenarios: list            # e.g. [-10%, -5%, +5%, +10%] for sensitivity
  cost_change_scenarios: list             # variable or fixed cost % changes
  step_fixed_costs:                       # optional: fixed costs change with volume tiers
    - {volume_threshold: number, fixed_costs: number}
  opportunity:                            # for opportunity_go_no_go
    volume_ramp: list                     # orders/month by quarter
    capex: number
    incremental_working_capital: number   # added inventory − added A/P
    steady_state_annual_operating_profit: number
```

## Missing Information Protocol
- If both `variable_cost_per_unit` and `cogs_pct` are missing, ask the founder for one; contribution margin cannot be computed without it.
- If fixed costs are unknown, pull from the income statement (rent, salaries, overhead) and confirm which costs are truly fixed vs. variable — misclassifying them invalidates break-even.
- For step-fixed costs (staffing added at volume tiers), require the tier schedule; a single fixed number would understate break-even after a step.
- For opportunity mode, if incremental working capital or capex is unknown, ask; initial investment drives ROI and payback.
- Never assume a price; if pricing is the question, present break-even at candidate prices rather than picking one.

## Diagnostic Questions
1. What is the contribution margin per unit and the contribution margin ratio?
2. How many units/how much revenue are needed to cover fixed costs (break-even)?
3. How far is current/forecast volume above break-even (margin of safety)?
4. How does break-even move if price changes by ±X%, or if variable/fixed costs change?
5. Do fixed costs step up at higher volume, and does break-even jump after each step?
6. For an opportunity: what is the initial investment, break-even volume, ROI, and payback?

## Analysis Framework
Separate fixed vs. variable costs first, compute contribution margin, then break-even, margin of safety, and sensitivities; for opportunities, add initial investment, ROI, and payback.

- **Cost separation:** variable costs move with volume (materials, per-unit labor, packaging, commissions); fixed costs do not (rent, salaried staff, base overhead). Break-even validity depends on correct separation. Salaries loaded with benefits/payroll-tax % where relevant.
- **Contribution margin:** each unit's price less its variable cost contributes this much toward fixed costs and then profit.
- **Break-even:** the volume where total contribution equals fixed costs (zero profit). With step-fixed costs, compute break-even within each tier and check which tier's volume is actually feasible.
- **Margin of safety:** how far actual/forecast volume exceeds break-even — the cushion before losses.
- **Price/cost sensitivity:** re-compute contribution margin and break-even under each price or cost change; a price cut raises break-even (more units needed), a price rise lowers it.
- **Opportunity economics:** initial investment = capex + net incremental working capital; ROI = steady-state annual operating profit / initial investment; payback = time for cumulative operating cash flow to recover the initial investment. Note: when COGS and inventory payment timing coincide, operating cash flow ≈ operating profit (state this simplifying assumption when used).

## Calculations
- **Contribution margin per unit (CM)** = Price − Variable cost per unit = Price × (1 − COGS%). (Worked: $50 × (1 − 0.45) = $27.50/order.)
- **Contribution margin ratio** = CM / Price = 1 − COGS%.
- **Break-even units** = Fixed costs (period) / CM per unit. (Worked: fixed $18,500 / $27.50 = ~673 orders; when staffing steps fixed to $30,500 → ~1,109 orders; full-year fixed $98,000 → ~3,564 orders.)
- **Break-even revenue** = Fixed costs / contribution margin ratio = Break-even units × Price.
- **Margin of safety (units)** = Current/forecast volume − Break-even units.
- **Margin of safety (%)** = (Current volume − Break-even volume) / Current volume × 100.
- **Target-profit volume** = (Fixed costs + Target profit) / CM per unit.
- **New break-even after a price change** = Fixed costs / (New price − Variable cost).
- **New break-even after a variable-cost change** = Fixed costs / (Price − New variable cost).
- **Initial investment** = Capex + Net incremental working capital (added inventory − added A/P). (Worked: inventory $1,500 − A/P $500 = $1,000 WC; capex $7,500 + $4,500 = $12,000; total $13,000.)
- **ROI** = Steady-state annual operating profit / Initial investment. (Worked: $43,000 / $13,000 ≈ 331%.)
- **Payback period** = time for cumulative operating cash flow to recover the initial investment.
- **Fully-loaded wage (for fixed-cost inputs)** = Base wage × (1 + benefits & payroll-tax %) (worked +25%).

## Decision Rules
- IF forecast volume < break-even → THEN the plan loses money at that price/cost structure; must raise price, cut cost, or increase volume before committing.
- IF margin of safety is thin (small % above break-even) → THEN the offering is fragile to demand dips; flag and recommend a cushion (lower fixed costs or higher CM).
- IF a price cut is proposed → THEN compute the new (higher) break-even and the extra volume needed to hold profit; if that volume is implausible vs. capacity/demand, advise against the cut.
- IF a price rise is proposed → THEN compute the new (lower) break-even and the volume you can afford to lose before profit falls; pair with demand/elasticity judgment.
- IF fixed costs step up with volume → THEN report break-even per tier and warn that crossing a step temporarily raises the break-even until volume catches up.
- IF variable cost per unit ≥ price → THEN contribution margin is zero/negative; every unit loses money — do not sell at this price (structural, not a volume problem).
- IF opportunity ROI < the cost of the capital funding it (or below the founder's hurdle) → THEN it destroys value; recommend against or re-scope.
- IF payback exceeds the founder's tolerance or the asset's useful life → THEN flag the opportunity as high-risk.

## Procedure
1. Confirm mode; separate fixed vs. variable costs (validate the classification).
2. Compute CM per unit and CM ratio.
3. Compute break-even units and revenue (per tier if step-fixed costs exist).
4. Compute margin of safety vs. current/forecast volume.
5. For price/cost sensitivity: recompute break-even and profit under each scenario; report the volume swing needed.
6. For opportunity mode: compute initial investment, ROI, and payback; state the OCF≈operating-profit assumption if used.
7. Emit break-even, margin of safety, sensitivity table, and (if applicable) go/no-go economics with a recommendation; write key metrics to `finance.position` (L1); record in `decisions`.

## Output
```yaml
output:
  mode: enum[break_even, price_sensitivity, cost_sensitivity, opportunity_go_no_go]
  contribution_margin_per_unit: number
  contribution_margin_ratio: number
  break_even_units: number
  break_even_revenue: number
  break_even_by_tier: list                # if step-fixed costs
  margin_of_safety_units: number
  margin_of_safety_pct: number
  price_sensitivity:                      # per scenario
    - {price_change_pct: number, new_break_even_units: number, volume_swing_needed: number, profit_at_current_volume: number}
  cost_sensitivity:
    - {cost_change_pct: number, new_break_even_units: number, profit_at_current_volume: number}
  opportunity:                            # if go/no-go
    initial_investment: number
    roi_pct: number
    payback_periods: number
    recommendation: enum[go, no_go, rescope]
  narrative: string
  handoffs: list
```

## Recommendations
For pricing: present break-even and margin of safety at each candidate price, with the volume swing each price implies, and pair the numbers with demand judgment — recommend the price that maximizes contribution given realistic volume, never a price cut that requires implausible volume. For opportunities: recommend go / no-go / re-scope based on ROI vs. hurdle and payback vs. tolerance. Prioritize structural fixes (raise CM) over volume heroics when margin of safety is thin. Flag that any actual price change to customers is an external commitment requiring approval.

## Execution Opportunities
- Write break-even, contribution margin, and margin of safety to `finance.position` (reversible, LOW; L1).
- Build a pricing sensitivity table / break-even chart for the founder (reversible, LOW).
- Create a go/no-go brief for an opportunity with ROI and payback (reversible, LOW).
- Feed opportunity economics to `financial-forecast-builder` for the full incremental model (reversible, LOW).

## Human Approval Requirements
- Break-even, contribution, sensitivity, and ROI/payback analysis: always allowed.
- Publishing or changing a price to customers: requires founder approval (external commitment).
- Committing capex or budget to launch an opportunity: ALWAYS requires founder approval (budget commitment / possible financing).
- Hiring the step-fixed staff implied by a volume tier: requires founder approval (routes to People Agent).

## Escalation Conditions
- Opportunity requires financing beyond available cash → founder + (financing needs approval; recommend accountant).
- Pricing move has tax, contract, or regulatory implications → accountant/attorney.
- Cost classification is genuinely ambiguous (mixed/semi-variable costs) → note the uncertainty; consider accountant input for material cases.
- Break-even implies infeasible capacity/demand → founder (strategic call).

## KPIs
- Break-even accuracy vs. realized volume/costs.
- Pricing decisions that improve contribution without losing more volume than modeled.
- Opportunities greenlit that meet or beat modeled ROI/payback.
- Margin-of-safety improvements after recommended structural changes.

## Monitoring
- Track actual volume vs. break-even each period; alert if it falls toward break-even.
- Monitor variable cost per unit and price realization for CM erosion.
- After a launch, compare actual ROI/payback to the model.

## Follow-Up
- Re-run on any price, cost-structure, or volume change, and before any launch or pricing decision.
- Re-run when `scenario-and-sensitivity-analysis` flags price/volume as a fragile assumption.

## Related Skills
- `financial-forecast-builder` (full incremental model of an opportunity).
- `scenario-and-sensitivity-analysis` (price/volume fragility across the whole plan).
- `working-capital-optimizer` (incremental working capital in initial investment).
- `financial-ratio-analysis` (margin context).

## Guardrails
- Correct fixed/variable separation is a precondition — validate it; misclassification invalidates break-even.
- Never recommend a price cut that requires implausible volume, nor a price with negative contribution margin.
- Account for step-fixed costs; a single fixed number understates break-even after a step.
- Price changes and capex commitments require founder approval; hiring routes through the People Agent + founder.
- State the OCF≈operating-profit simplification explicitly whenever used.
- Confidential financial data; audited writes to permitted namespaces.

## Example
**Founder input:** "I want to launch a take-out line. Average order $50, COGS 45% including packaging. First quarters cost a cook ($18k/qtr); I add a prep person later, raising staffing to $30k/qtr; other opex $500/qtr. Full-year fixed will be $98k. Equipment $7,500 + POS $4,500; I'll carry $1,500 more inventory and get $500 more supplier credit. Steady-state year makes ~$43k operating profit. Is it worth it?"

**Skill reasoning:** CM = $50 × (1 − 0.45) = $27.50/order. Quarter-1 fixed $18,000 + $500 = $18,500 → break-even 673 orders/qtr (~224/mo). After the staffing step: fixed $30,500 → break-even 1,109 orders/qtr. Full-year fixed $98,000 → break-even 3,564 orders/yr. Initial investment = capex $12,000 + net incremental WC ($1,500 − $500 = $1,000) = $13,000. ROI = $43,000 / $13,000 ≈ 331%. Payback: with steady-state operating profit ~$43k/yr (OCF≈operating profit assumed since COGS and inventory payment coincide), cumulative cash recovers $13,000 in roughly 4 months of steady-state → fast payback.

**Output:** CM $27.50; tiered break-even (673 → 1,109 orders/qtr; 3,564/yr); initial investment $13,000; ROI ~331%; payback ~4 months steady-state; recommendation GO if the ramp can clear ~1,100 orders/qtr after the staffing step. Handoff: `financial-forecast-builder` for the full incremental 3-statement view.

**Executed vs. approval:** metrics written, go/no-go brief and break-even chart created (L1); the equipment/POS capex, the prep-person hire, and the final menu price held for founder approval.

## Provenance
SOURCE. Derives from the Forecasting/Cash knowledge (contribution margin, break-even units, initial investment = capex + net incremental working capital, ROI, payback, step-fixed staffing, OCF≈operating-profit simplification, employee cost loading) and the opportunity-assessment framework. Branding stripped and generalized per PROVENANCE_MAP.
