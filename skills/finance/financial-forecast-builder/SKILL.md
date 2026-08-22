---
name: financial-forecast-builder
domain: finance
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [finance.income_statement, finance.balance_sheet, finance.cash_flow, finance.working_capital, finance.debt, finance.position, company, offerings]
writes: [finance.forecasts, decisions]
related_skills: [scenario-and-sensitivity-analysis, budget-builder, debt-service-and-covenant-analysis, working-capital-optimizer, cash-runway-monitor]
owned_by_agents: [cfo-agent, business-analyst-agent]
---

# Skill: Financial Forecast Builder

## Purpose
Build a fully-linked, driver-based three-statement forecast (monthly for year one, annual for multiple years) from a documented assumption set, then read off the funding needed to keep the balance sheet balanced and check the plan against loan covenants and the minimum-cash cushion. Gives the founder a defensible, reconciled financial plan for growth, fundraising, and lending decisions.

## When to Use
- "Build me a financial forecast / 3-year plan / monthly cash projection."
- "How much funding will I need to hit this growth plan, and when?"
- "Model adding this new product line/location on top of the existing business."
- Before fundraising, a loan application, a budget cycle, or a major growth decision.

## When NOT to Use
- Stress-testing an existing forecast across scenarios / single-variable sensitivities → `scenario-and-sensitivity-analysis` (this skill builds the base model it flexes).
- A quick go/no-go on one opportunity without a full 3-statement build → use the opportunity-assessment quarterly forecast pattern (still within this skill's incremental mode) or `break-even-and-pricing-analysis` for the unit economics.
- Turning the forecast into an operating budget with variance tracking → `budget-builder`.
- Deciding whether to actually take the funding → founder decision; this skill sizes and times the need, it does not apply for or draw financing.

## Required Context
- Most recent actual IS and BS as the base-period anchor. Read from `finance.income_statement`, `finance.balance_sheet`.
- Existing debt: balances, rates, amortization schedules, covenants. Read from `finance.debt`.
- Working-capital days (DSO/DIO/DPO) and minimum-cash target. Read from `finance.working_capital`, `finance.position`.
- Revenue model inputs (growth %, or units × price, or a monthly ramp) and cost drivers. Read from `offerings`, `company`.

## Inputs
```yaml
input:
  base_period:                            # Layer 0 anchor (actuals)
    income_statement: {revenue, cogs, opex{selling_marketing, g_and_a, r_and_d, depreciation}, interest_expense, tax}
    balance_sheet: {cash, accounts_receivable, inventory, prepaid, fixed_assets{gross, accum_dep}, accounts_payable, accrued, short_term_debt, long_term_debt, equity{common_stock, retained_earnings}}
  horizon_years: integer                  # e.g. 5
  monthly_first_year: boolean             # true = monthly y1 + annual thereafter
  revenue_driver:
    method: enum[growth_rate, units_price, monthly_ramp]
    growth_pct_by_year: list              # for growth_rate (can differ per year)
    units_by_period: list                 # for units_price
    price_per_unit: number
    ramp_schedule: list                   # for monthly_ramp
  cogs_pct_by_year: list                  # can decline with scale (e.g. 62,61,60...)
  opex_assumptions:
    selling_marketing: {fixed: number, variable_pct: number}
    g_and_a: {base: number, growth_pct: number}   # e.g. grow at half revenue growth
    r_and_d: {pct_of_revenue: number}
    salaries: {base: number, loading_pct: number} # +benefits/payroll tax, e.g. 25%
    occupancy: {fixed: number}
  depreciation: {method: straight_line}
  capex_by_year: list                     # gross PP&E additions
  asset_useful_life_years: number
  working_capital_days: {dso: number, dio: number, dpo: number, accrued_pct_of_opex: number}
  min_cash_balance: number                # cushion target (e.g. 10k–15k)
  debt:
    long_term: {balance: number, rate: number, annual_principal: number}
    revolver: {rate: number, cap: number, opening_balance: number}   # the plug
  tax_rate: number
  owner_withdrawals_by_year: list
  covenants: {current_ratio_min, tie_min, dscr_min, debt_to_equity_max}   # optional
  incremental_opportunity:                # optional; modeled on top of existing business
    revenue_driver: {...}
    cogs_pct: number
    incremental_opex: {...}
    capex: number
    incremental_working_capital_days: {dso, dio, dpo}
```

## Missing Information Protocol
- If the base period is missing, run `financial-statement-analysis` first; a forecast must anchor to reconciled actuals.
- If a driver is unknown, ask the founder in ONE batch, and offer a benchmark-derived default (validated via industry data) clearly labeled as an assumption — never bury an unverified assumption.
- If working-capital days are unknown, pull from `working-capital-optimizer`/`finance.working_capital`; if none, use the base-period implied days and note it.
- If revolver terms or covenants are unknown but debt exists, ask; do not assume a cap or rate.
- Document every assumption with its source (actual, founder-stated, benchmark, or default) so the forecast is auditable.

## Diagnostic Questions
1. Which revenue method fits each stream (growth %, units × price, or a ramp)?
2. Does COGS% improve with scale, or hold flat?
3. Which opex lines are fixed, which scale with revenue, and which grow on their own schedule?
4. What working-capital days convert the income statement into balance-sheet stocks?
5. What is the minimum-cash cushion, and does any projected month breach it (triggering a revolver draw)?
6. Where does the projected balance sheet fail to balance — i.e., how much external funding is needed, and when?
7. Does the plan stay within covenant limits and the revolver cap in every period?

## Analysis Framework
Rebuilds the driver-based linked three-statement model in dependency order (Layers 0–9), resolving the interest/debt circularity iteratively.

- **Layer 0 Base:** anchor to the latest actual IS + BS.
- **Layer 1 Revenue:** growth-rate `Revenue_t = Revenue_{t−1} × (1 + growth%_t)`, or units × price, or an explicit monthly ramp; sum multi-stream.
- **Layer 2 COGS:** `COGS = Revenue × COGS%` (COGS% may decline with scale); Gross Profit = Revenue − COGS.
- **Layer 3 Opex:** each line as fixed $, % of revenue, a growth series, or fixed+variable split; salaries loaded with benefits/payroll-tax %.
- **Layer 4 Depreciation:** straight-line = asset cost / useful life; feeds IS expense and BS accumulated depreciation; non-cash (added back in CF).
- **Layer 5 Below-the-line:** EBIT = Gross Profit − Opex; Interest = rate × debt balance; EBT = EBIT − Interest; Tax = rate × EBT; Net Income = EBT − Tax.
- **Layer 6 Working capital:** A/R = (Revenue/365) × DSO; Inventory = (COGS/365) × DIO; A/P = (COGS/365) × DPO; Accrued = accrued% × opex.
- **Layer 7 Fixed assets:** Net PP&E = Gross PP&E − Accumulated Depreciation; add capex.
- **Layer 8 Financing & cash plug:** enforce minimum cash; long-term debt follows its amortization; the revolver is the plug (draw if cash < min, up to cap; repay if cash > min); owner withdrawals reduce cash and equity.
- **Layer 9 Cash flow statement:** Operating CF = NI + Dep − ΔA/R − ΔInventory + ΔA/P + ΔAccrued; Investing = −capex; Financing = draws − repayments + equity − dividends; Ending cash = beginning + net, which feeds back to Layer 8.
- **Circularity:** interest depends on debt, which depends on the cash plug, which depends on net income (via interest) — iterate until convergence.
- **Funding needed:** if projected Assets ≠ Liabilities + Equity (after the revolver hits its cap), the gap is the external funding required; report its size and timing.
- **Incremental modeling:** model a growth opportunity's assumptions as incremental to the existing business, keep the two side by side, and sum.

## Calculations
- **Revenue (growth)** = Revenue_{t−1} × (1 + growth%_t). **(units)** = units × price. **(ramp)** = Σ monthly ramp.
- **COGS** = Revenue × COGS%. **Gross Profit** = Revenue − COGS. **Gross Margin%** = 1 − COGS%.
- **Opex line (variable)** = % × Revenue; **(growth)** = base × (1 + g)^t; **(loaded salary)** = base × (1 + loading%).
- **Depreciation (straight-line)** = asset cost / useful life. **Net PP&E** = Gross − Accumulated Dep.
- **EBIT** = Gross Profit − Total Opex. **Interest** = rate × outstanding debt. **EBT** = EBIT − Interest. **Tax** = tax_rate × EBT. **Net Income** = EBT − Tax.
- **A/R** = (Revenue/365) × DSO; **Inventory** = (COGS/365) × DIO; **A/P** = (COGS/365) × DPO; **Accrued** = accrued% × Opex.
- **Operating CF** = NI + Dep − ΔA/R − ΔInventory + ΔA/P + ΔAccrued (indirect).
- **Ending Cash** = Beginning Cash + Operating CF + Investing CF + Financing CF.
- **Revolver plug:** if Ending Cash < min_cash → draw = min(min_cash − Ending Cash, cap − revolver_balance); if Ending Cash > min_cash → repay = min(Ending Cash − min_cash, revolver_balance).
- **Funding needed** = Total Assets − (Total Liabilities + Equity) when the revolver is capped out (the financing plug).
- **Covenant checks:** Current Ratio = CA/CL ≥ covenant min; TIE = EBIT/Interest ≥ min; DSCR (Times Burden Covered) = EBIT / [Interest + Principal/(1−tax)] ≥ min; Debt/Equity ≤ max — each tested every period.
- **Minimum-cash breach:** any projected period with pre-financing cash < min_cash triggers a revolver draw (or a funding-need flag if the cap is hit).

## Decision Rules
- IF projected cash < minimum cash balance → THEN draw on the revolver up to its cap. IF the draw exceeds the cap → THEN flag a financing gap (renegotiate the facility or raise capital — founder decision).
- IF projected cash > minimum cash balance → THEN pay down short-term/revolver debt with the excess.
- IF projected Assets ≠ Liabilities + Equity after the revolver is exhausted → THEN report the funding needed and its timing; propose a prioritized close plan (see Recommendations) — raising it requires founder approval.
- IF COGS% is expected to fall with scale → THEN model it declining across years, not flat.
- IF any covenant is breached in a projected period → THEN flag the period and severity; hand to `debt-service-and-covenant-analysis`.
- IF interest/debt fail to converge after iteration → THEN report non-convergence rather than a spurious balanced sheet.
- IF evaluating a growth opportunity → THEN model incrementally on top of existing business and present combined + standalone views.
- IF assumptions are material and uncertain → THEN recommend `scenario-and-sensitivity-analysis` before the founder relies on the base case.
- IF a debt-funded project's return < the debt's interest rate → THEN flag that it destroys owner value; do not present it as accretive.

## Procedure
1. Anchor to reconciled base-period actuals; document every assumption with its source.
2. Project revenue (chosen method), then COGS/Gross Profit, then each opex line, then depreciation.
3. Compute EBIT; iterate interest ↔ debt ↔ cash-plug to resolve circularity.
4. Compute EBT, tax, net income.
5. Convert flows to balance-sheet stocks via working-capital days; roll fixed assets with capex/depreciation.
6. Apply financing logic: amortize long-term debt, run the revolver plug against minimum cash, deduct owner withdrawals.
7. Assemble the cash-flow statement; confirm ending cash ties and the balance sheet balances (or report the funding gap).
8. Run covenant and minimum-cash checks every period; flag breaches.
9. If an incremental opportunity is provided, model it separately and combine.
10. Emit monthly (y1) + annual statements, funding-needed schedule, covenant status; write to `finance.forecasts` (L1 staged); record in `decisions`.

## Output
```yaml
output:
  horizon_years: integer
  granularity: enum[monthly_y1_annual, annual]
  assumptions_log:                        # every assumption with source
    - {driver: string, value: any, source: enum[actual, founder, benchmark, default]}
  income_statement: list                  # per period
  balance_sheet: list                     # per period, with balances: boolean
  cash_flow: list                         # per period
  funding_needed:                         # by period
    - {period: string, amount: number, cumulative: number, revolver_drawn: number, gap_beyond_cap: number}
  covenant_status:                        # per period
    - {period: string, current_ratio: number, tie: number, dscr: number, debt_to_equity: number, breaches: list}
  min_cash_breaches: list
  incremental_view: {standalone: object, combined: object}   # if opportunity modeled
  convergence: boolean
  narrative: string
  handoffs: list
```

## Recommendations
When a funding gap appears, propose an ordered close plan (funding-shortfall remediation stack): reduce the minimum-cash target; accelerate A/R and tighten inventory (raise turnover); extend A/P within terms; renegotiate the revolver/credit-line schedule; shift sales comp from fixed to variable; secure supplier prompt-pay discounts; then external financing (debt or equity) as the last, founder-approved step. Rank by cost, reversibility, and speed. Always separate operational levers (can proceed as tasks) from financing (founder approval). Recommend running scenarios before committing to the base plan.

## Execution Opportunities
- Write the forecast and funding schedule to `finance.forecasts` (reversible, LOW; L1 staged).
- Create internal tasks for operational levers that close a funding gap (reversible, LOW).
- Draft a funding-need summary / lender or investor packet outline for founder review (reversible, LOW; sending requires approval).
- Feed the base model to `scenario-and-sensitivity-analysis` and the year-1 plan to `budget-builder` (reversible, LOW).

## Human Approval Requirements
- Building, projecting, and interpreting the forecast: always allowed.
- Applying for financing, drawing debt, or any money movement to close a funding gap: ALWAYS requires founder approval.
- Committing to a budget derived from the forecast, or to capex/hiring in the plan: requires founder approval (budget commitment).
- Sharing the forecast externally (lenders, investors): requires founder approval.

## Escalation Conditions
- Projected funding gap the founder cannot cover from operations → founder + recommend accountant; consider financing options (approval-gated).
- Covenant breach projected → founder + `debt-service-and-covenant-analysis`.
- Tax, entity, or complex-accounting assumptions materially affect the model → accountant/CPA.
- Non-convergence or an implausible result → surface to founder; do not present an unreconciled forecast as reliable.

## KPIs
- Base sheet balances every projected period (or funding gap correctly quantified).
- Forecast vs. actuals accuracy over time (revenue, net income, ending cash within tolerance).
- Funding need identified with enough lead time to arrange it.
- Covenant/min-cash breaches caught before they occur.

## Monitoring
- Re-forecast vs. actuals each close; track assumption drift.
- Watch the funding-needed timeline and revolver headroom.
- Monitor projected covenant status as actuals update.

## Follow-Up
- Re-run at each planning cycle, before fundraising/lending, and after any material assumption change or actual variance.
- Re-run when `budget-builder` variance or `cash-runway-monitor` signals the plan is off track.

## Related Skills
- `financial-statement-analysis` (base-period anchor).
- `scenario-and-sensitivity-analysis` (stress-tests this model).
- `budget-builder` (turns year-1 into an operating budget).
- `debt-service-and-covenant-analysis` (covenant checks, debt capacity).
- `working-capital-optimizer` (supplies days drivers).
- `cash-runway-monitor` (near-term cash view).

## Guardrails
- Anchor to reconciled actuals; never forecast off unvalidated statements.
- Document every assumption with its source; never bury an unverified assumption.
- Report non-convergence and funding gaps honestly; never plug a balance to look balanced.
- A debt-funded project earning less than its interest rate destroys value — flag it.
- Financing, budget commitments, and external sharing require founder approval; tax/entity assumptions escalate to an accountant.
- Confidential financial data; audited writes to permitted namespaces; sensitivity stays confidential.

## Example
**Founder input:** "Model my next 3 years. Base revenue $2.0M growing 20%/yr; COGS 60% improving 1 pt/yr; S&M fixed $120k + 5% of revenue; G&A $200k growing 10%/yr; DSO 45, DIO 30, DPO 40; min cash $50k; long-term debt $300k at 8% with $50k/yr principal; revolver at 9% capped $200k; tax 25%; owner draws $60k/yr. Bank covenant current ratio ≥ 1.5."

**Skill reasoning:** Year 1 revenue $2.4M, COGS 59% = $1.416M, Gross Profit $984k; S&M $240k, G&A $220k, depreciation from schedule; EBIT computed; interest on $300k LT + revolver iterated with the cash plug against the $50k minimum; tax 25%; net income derived. Working capital: A/R = 2.4M/365×45 = $296k, Inventory = 1.416M/365×30 = $116k, A/P = 1.416M/365×40 = $155k. Cash plug: if projected cash < $50k, draw revolver; Year-2 growth lifts A/R/inventory faster than cash generation, drawing ~$140k on the revolver (within the $200k cap → no external gap yet). Covenant: current ratio projected 1.6 → passes with thin headroom; flagged as at-risk if growth accelerates.

**Output:** 3-year linked statements (monthly year 1), funding-needed schedule showing peak revolver draw ~$140k in year 2, covenant status passing but tight, assumptions log with sources. Handoffs: `scenario-and-sensitivity-analysis` (test 10% growth-miss), `budget-builder`.

**Executed vs. approval:** forecast written to `finance.forecasts`, lever tasks and a funding-summary draft created (L1); any actual borrowing, budget commitment, or external sharing held for founder approval.

## Provenance
SOURCE. Derives from the Forecasting/Cash knowledge (driver-based linked three-statement model Layers 0–9, revolver cash-plug logic, working-capital-days drivers, incremental opportunity modeling, interest/debt circularity) and the Statements & Ratios knowledge (assumption-driven five-year projection, funding-shortfall remediation stack, covenant thresholds). Branding stripped and generalized per PROVENANCE_MAP.
