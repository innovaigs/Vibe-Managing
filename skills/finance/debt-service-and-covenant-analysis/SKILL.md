---
name: debt-service-and-covenant-analysis
domain: finance
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [finance.debt, finance.income_statement, finance.balance_sheet, finance.cash_flow, finance.forecasts, finance.position, company]
writes: [finance.debt, decisions]
related_skills: [financial-ratio-analysis, financial-forecast-builder, cash-flow-diagnostic, scenario-and-sensitivity-analysis]
owned_by_agents: [cfo-agent, business-analyst-agent]
---

# Skill: Debt Service & Covenant Analysis

## Purpose
Assess whether the business can safely carry its debt — computing interest and debt-service coverage (TIE, DSCR / Times Burden Covered), the maximum additional debt it could support, and the headroom or breach status against every loan covenant — with early alerts before a breach. Protects the founder from technical default and from over- or under-leveraging.

## When to Use
- "Can we afford to take on this loan / more debt?"
- "Are we close to breaching a covenant?"
- "What's the most debt we can safely support?"
- "How covered are our interest and principal payments?"
- Before a financing application, during covenant reporting periods, or after `financial-ratio-analysis` flags a leverage/coverage or covenant issue.

## When NOT to Use
- Full ratio panel → `financial-ratio-analysis` (this skill goes deep on coverage/covenants).
- Projecting the whole business forward → `financial-forecast-builder` (this skill consumes its projections for forward covenant checks).
- Explaining a cash shortfall from operations → `cash-flow-diagnostic`.
- Applying for, signing, or drawing financing, or negotiating covenant terms with the lender → founder decision + attorney/accountant; this skill analyzes capacity and risk, it does not execute or agree to financing.

## Required Context
- All debt instruments: balances, rates, principal schedules, maturities, covenant terms. Read from `finance.debt`.
- EBIT/EBITDA, interest expense, and tax rate. Read from `finance.income_statement`.
- Operating cash flow. Read from `finance.cash_flow`.
- Forward projections for forward-looking covenant/coverage checks. Read from `finance.forecasts`.

## Inputs
```yaml
input:
  mode: enum[coverage_check, covenant_check, max_supportable_debt, new_debt_assessment]
  ebit: number
  ebitda: number
  interest_expense: number                 # current annual interest
  operating_cash_flow: number
  tax_rate: number
  debt_instruments:
    - {id: string, type: enum[loan, line, card, bond], balance: number, rate: number, annual_principal: number, maturity: string}
  covenants:
    - {name: string, metric: enum[current_ratio, tie, dscr, debt_to_equity, debt_to_assets, min_ebitda], operator: enum[">=", "<=", ">", "<"], threshold: number, test_frequency: string}
  balance_sheet: {current_assets, current_liabilities, total_liabilities, total_assets, equity}
  new_debt:                                # for new_debt_assessment
    amount: number
    rate: number
    term_years: number
    use_of_proceeds: string
    expected_return_pct: number            # return on the project funded
  forecast_ref: string                     # for forward covenant checks
  target_coverage: {tie_min: number, dscr_min: number}   # policy minimums (defaults if unset)
```

## Missing Information Protocol
- If covenant terms are unknown but debt exists, ask the founder for the exact covenant definitions and thresholds (or request the loan agreement) — covenant math depends on the lender's specific definition; never assume.
- If EBITDA or operating cash flow is missing, compute from `finance.income_statement`/`finance.cash_flow`; if inputs are incomplete, ask.
- If a new debt's expected return is unknown, ask — the return-vs-rate test determines whether the debt creates or destroys value.
- Note which coverage numerator (EBIT vs. EBITDA) the lender uses; report both if unspecified and flag the assumption.
- Never sign, agree to, or draw financing; analysis only.

## Diagnostic Questions
1. How many times do operating earnings cover interest (TIE) and total debt service (DSCR / Times Burden Covered)?
2. Is coverage comfortable, thin, or below policy/lender minimums?
3. What is the maximum additional debt the business could service at target coverage?
4. What is the headroom on each covenant, and is any near or through its threshold?
5. Would proposed new debt breach a covenant or push coverage below the minimum, now or in the forecast?
6. Does the project the debt funds earn more than the debt's interest rate (value-creating), or less (value-destroying)?

## Analysis Framework
Compute coverage from current and projected earnings, test every covenant with headroom, solve for max supportable debt, and evaluate any new debt on coverage, covenant, and value grounds.

- **Coverage:** TIE = EBIT / Interest (or EBITDA / Interest as a cash proxy — report which). DSCR / Times Burden Covered = EBIT / [Interest + Principal/(1 − tax)] (principal grossed up because it is not tax-deductible); alt EBITDA / (Interest + Principal). Below ~1.5 TIE signals financial stress; DSCR must be ≥ 1 to cover mandatory payments, with cushion above.
- **Covenant testing:** for each covenant, evaluate the metric against its operator/threshold; compute headroom (distance to breach) and flag warning/breach. Forward-test using the forecast so a projected breach is caught before the reporting date.
- **Max supportable debt:** solve for the debt balance whose total debt service keeps DSCR at the target minimum, given EBIT/EBITDA and the rate — the ceiling on prudent borrowing.
- **New-debt assessment:** recompute coverage and every covenant with the new instrument added; check the value test (project return vs. debt rate). Under-leverage note: persistently very high coverage may mean the firm is missing low-risk value from prudent debt (surface as an option, not a recommendation to borrow).

## Calculations
- **Times Interest Earned (TIE)** = EBIT / Interest Expense (or EBITDA / Interest).
- **DSCR / Times Burden Covered** = EBIT / [Interest + Principal / (1 − tax rate)]. Alt cash form = EBITDA / (Interest + Principal).
- **Total annual debt service** = Σ(interest + annual principal) across instruments.
- **Interest on new debt** = new_amount × new_rate. **New annual principal** = new_amount / term_years (or per schedule).
- **Combined TIE (with new debt)** = EBIT / (Interest + new interest).
- **Combined DSCR** = EBIT / [(Interest + new interest) + (Principal + new principal)/(1 − tax)].
- **Max supportable total debt service (at target DSCR)** = EBIT / target_DSCR (using the grossed-up form: solve Interest + Principal/(1−tax) ≤ EBIT / target_DSCR).
- **Max supportable debt balance** ≈ [EBIT / target_DSCR − existing service_grossed_up] capitalized at the applicable rate/term (solve the debt whose grossed-up service consumes the remaining coverage capacity).
- **Covenant headroom** = |actual metric − threshold| expressed in the metric's units and as % of threshold; direction indicates pass/fail.
- **Debt-to-Equity** = Total Liabilities (or interest-bearing) / Equity. **Debt-to-Assets** = Total Liabilities / Total Assets.
- **Value test** = expected project return% vs. debt rate; return% < rate → value-destroying.

**Thresholds:** TIE < ~1.5 = financial stress (critical); DSCR < 1.0 = cannot cover mandatory payments (critical); covenant metric on the wrong side of its threshold = technical default (critical). Very high TIE/DSCR = possibly under-levered (informational).

## Decision Rules
- IF TIE < ~1.5 or DSCR < ~1.2 → THEN coverage is thin/stressed; do not add debt; reduce debt or raise EBIT first.
- IF DSCR < 1.0 → THEN the business cannot cover mandatory interest + principal from operating earnings — critical; escalate immediately.
- IF any covenant metric is on the wrong side of its threshold → THEN technical default (possible acceleration, forced asset sale, higher rate, added collateral); escalate to founder immediately and remediate before the test date.
- IF covenant headroom is within a set buffer (e.g., < 10% of threshold) → THEN warning; alert and monitor closely; recommend levers to restore headroom.
- IF proposed new debt drops combined TIE/DSCR below target or breaches any covenant (now or in the forecast) → THEN advise against it or resize it to fit capacity.
- IF the project a new debt funds has expected return < the debt's rate → THEN it destroys owner value; do not present it as accretive.
- IF coverage is persistently very high AND capacity is unused → THEN note the firm may be under-levered and could create low-risk value with prudent debt (surface as an option for founder decision, never an autonomous action).
- IF a forward covenant breach is projected → THEN flag the period and trigger `financial-forecast-builder`/`scenario-and-sensitivity-analysis` to test remediation.

## Procedure
1. Load debt instruments, covenants, earnings, and (for forward checks) the forecast.
2. Compute TIE and DSCR from current earnings; report EBIT- and EBITDA-based where the lender's definition is unspecified.
3. Test every covenant; compute headroom and flag warning/breach; forward-test against the forecast.
4. Solve for max supportable debt at the target DSCR.
5. For new-debt mode: recompute combined coverage and every covenant, run the value test, and give a fit/no-fit verdict with a safe size.
6. Emit coverage, covenant status/headroom, max supportable debt, and any new-debt verdict with remediation levers; write coverage/covenant status to `finance.debt` (L1); record in `decisions`.

## Output
```yaml
output:
  mode: enum[coverage_check, covenant_check, max_supportable_debt, new_debt_assessment]
  coverage:
    tie_ebit: number
    tie_ebitda: number
    dscr: number
    total_annual_debt_service: number
    status: enum[comfortable, thin, stressed, uncovered]
  covenant_status:
    - {name: string, metric: string, actual: number, threshold: number, headroom_pct: number, status: enum[pass, warning, breach], forward_breach_period: string}
  max_supportable_debt:
    additional_debt_balance: number
    at_target_dscr: number
  new_debt_verdict:                        # new_debt_assessment mode
    combined_tie: number
    combined_dscr: number
    covenant_impact: list
    value_test: enum[value_creating, value_destroying]
    verdict: enum[fits, resize, do_not_take]
    safe_size: number
  remediation_levers: list
  narrative: string
  handoffs: list
```

## Recommendations
For breaches/warnings: prioritize the fastest, lowest-cost levers to restore coverage or covenant headroom — accelerate collections/tighten working capital (raise cash and current ratio), defer discretionary spend, pay down the most expensive debt, or raise EBIT — before the reporting date; renegotiating covenants or refinancing is a founder decision with the lender (involve attorney/accountant). For new debt: recommend fit / resize / do-not-take based on combined coverage, covenant impact, and the value test, and state the safe size. Never recommend taking on debt as an autonomous action; frame it as an option for founder approval.

## Execution Opportunities
- Write coverage and covenant status to `finance.debt` (reversible, LOW; L1).
- Set covenant-headroom monitoring alerts (reversible, LOW).
- Create remediation tasks for warning/breach situations (reversible, LOW).
- Draft a debt-capacity / covenant-status summary or lender-communication outline for founder review (reversible, LOW; sending requires approval).
- Trigger forward covenant checks in `financial-forecast-builder`/`scenario-and-sensitivity-analysis` (reversible, LOW).

## Human Approval Requirements
- Coverage, covenant, capacity, and new-debt analysis: always allowed.
- Taking on debt, applying for financing, drawing on a facility, or any money movement: ALWAYS requires founder approval.
- Agreeing to, renegotiating, or signing covenant/loan terms: founder approval + attorney (contract) and accountant.
- Any external communication with the lender: requires founder approval.

## Escalation Conditions
- Covenant breach or projected breach → founder immediately + accountant; attorney if remediation involves the loan agreement.
- DSCR < 1.0 or TIE < 1.5 (cannot cover mandatory payments) → founder immediately + accountant (financial distress).
- New debt or refinancing decision → founder + accountant (and attorney for terms).
- Covenant definition ambiguity or complex accounting in the metric → accountant/CPA.
- Financial distress or restructuring territory → founder + accountant/attorney.

## KPIs
- Covenant breaches and warnings surfaced before the lender's test date (target: zero surprises).
- Coverage ratios kept above policy minimums.
- New-debt verdicts that hold up (funded projects earn above their rate; no covenant breach post-draw).
- Max-supportable-debt guidance that keeps the firm within safe leverage.

## Monitoring
- Track TIE, DSCR, and each covenant's headroom every period and against the forecast.
- Alert when headroom enters the warning buffer or a forward breach appears.
- Watch for rising rates or falling EBIT that erode coverage.

## Follow-Up
- Run each covenant reporting period, before any financing decision, and whenever earnings or debt change materially.
- Re-run after any covenant renegotiation, refinancing, or new draw.

## Related Skills
- `financial-ratio-analysis` (leverage/coverage context; flags that trigger this skill).
- `financial-forecast-builder` (forward coverage and covenant checks).
- `cash-flow-diagnostic` (whether operating cash actually supports debt service).
- `scenario-and-sensitivity-analysis` (coverage under downside).

## Guardrails
- Never assume covenant definitions or thresholds; use the lender's exact terms.
- Never recommend taking on debt as an autonomous action; borrowing, refinancing, and agreeing terms are founder-approved (with accountant/attorney).
- A project earning less than its debt rate destroys value — flag it; do not present it as accretive.
- Report both EBIT- and EBITDA-based coverage when the lender's definition is unspecified.
- Under-leverage is an option to surface, not an instruction to borrow.
- Confidential financial data; audited writes to permitted namespaces.

## Example
**Founder input:** "My bank covenant requires DSCR ≥ 1.25 and current ratio ≥ 1.5. EBIT is $70,700, interest $16,600, current annual principal $12,000, tax rate 25%. Current assets $370k, current liabilities $250k. I want a new $150k loan at 9% over 5 years to buy equipment I expect to earn 14% on. Can I take it, and am I covered?"

**Skill reasoning:** Current TIE = 70,700/16,600 = 4.26× (comfortable). Current DSCR = 70,700 / [16,600 + 12,000/(1−0.25)] = 70,700 / (16,600 + 16,000) = 70,700/32,600 = 2.17× (passes ≥1.25). Current ratio = 370k/250k = 1.48 → already below the 1.5 covenant → breach flagged now. New debt: interest +$13,500, principal +$30,000/yr. Combined DSCR = 70,700 / [(16,600+13,500) + (12,000+30,000)/0.75] = 70,700 / (30,100 + 56,000) = 70,700/86,100 = 0.82× → below 1.0 and far below the 1.25 covenant → the new loan is NOT serviceable at this size. Value test: project return 14% > 9% rate → value-creating in principle, but the business cannot service the debt. Max supportable additional service at DSCR 1.25 = 70,700/1.25 = $56,560 total; existing grossed-up service is $32,600, leaving ~$23,960 of capacity → a much smaller loan (roughly $60–70k at these terms) fits.

**Output:** coverage comfortable on interest but the $150k loan drops DSCR to 0.82× (do_not_take at that size; resize to ~$65k); current ratio 1.48 is already a covenant breach to remediate now; remediation levers = accelerate collections to lift current ratio above 1.5, defer discretionary spend. Handoffs: `working-capital-optimizer` (restore current ratio), `financial-forecast-builder` (forward covenant path).

**Executed vs. approval:** coverage/covenant status written to `finance.debt`, breach alert and remediation tasks created, capacity summary drafted (L1); taking any loan, resizing it, or contacting the lender held for founder approval (with accountant/attorney on terms).

## Provenance
SOURCE. Derives from the Statements & Ratios knowledge (Times Interest Earned, Times Burden Covered with grossed-up principal, covenant rules and consequences, under-/over-leverage guidance, return-vs-rate value test) and the Forecasting/Cash knowledge (debt-service coverage, forward covenant checks, DSCR formulas). Branding stripped and generalized per PROVENANCE_MAP.
