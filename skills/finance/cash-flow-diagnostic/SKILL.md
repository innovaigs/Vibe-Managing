---
name: cash-flow-diagnostic
domain: finance
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [finance.income_statement, finance.balance_sheet, finance.cash_flow, finance.working_capital, finance.position, company]
writes: [finance.cash_flow, decisions]
related_skills: [financial-statement-analysis, financial-ratio-analysis, working-capital-optimizer, cash-runway-monitor]
owned_by_agents: [cfo-agent, business-analyst-agent]
---

# Skill: Cash Flow Diagnostic ("Profitable but No Cash")

## Purpose
Explain why a business can show accounting profit yet have no cash — by building a net-income → operating-cash bridge, ranking the drivers that consumed cash (A/R growth, inventory build, low A/P, capex, principal repayment, prepaid), and recommending targeted fixes. Resolves the single most common and most dangerous small-business surprise.

## When to Use
- "We're profitable on paper but there's no money in the bank — why?"
- "Where did all the cash go this quarter?"
- "Net income is up but our balance keeps dropping."
- After `financial-statement-analysis` or `financial-ratio-analysis` flags positive net income with negative or weak operating cash flow.

## When NOT to Use
- The business is unprofitable (negative net income) — that's an earnings problem, not a cash-timing problem; use `financial-statement-analysis` / `financial-ratio-analysis` to diagnose margins first.
- "How long until we run out of cash?" → `cash-runway-monitor`.
- Deep optimization of the cash conversion cycle → `working-capital-optimizer` (this skill hands off to it).
- Building forward projections of cash → `financial-forecast-builder`.

## Required Context
- Two consecutive periods of IS and BS (to compute working-capital changes). Read from `finance.income_statement`, `finance.balance_sheet`.
- Capex for the period and principal (not interest) debt repayments. Read from `finance.cash_flow`, `finance.debt`.
- Depreciation for the period. Read from `finance.income_statement`.
- Customer terms and supplier terms for context on collections/payments. Read from `company`, `offerings`.

## Inputs
```yaml
input:
  period_current: string
  period_prior: string
  net_income: number
  depreciation: number
  balance_sheet_current: {accounts_receivable, inventory, prepaid_expenses, accounts_payable, accrued_expenses, unearned_revenue}
  balance_sheet_prior:   {accounts_receivable, inventory, prepaid_expenses, accounts_payable, accrued_expenses, unearned_revenue}
  capex: number                         # cash spent on fixed assets this period (Investing)
  principal_repaid: number              # debt principal repaid this period (Financing, not an IS expense)
  dividends_or_withdrawals: number      # owner cash taken out (Financing)
  beginning_cash: number
  ending_cash: number                   # for reconciliation check
  customer_terms_days: number           # optional, for A/R context
  supplier_terms_days: number           # optional, for A/P context
```

## Missing Information Protocol
- If a prior-period balance sheet is missing, pull it from `finance.balance_sheet`; if unavailable, ask the founder for the specific opening balances of A/R, inventory, A/P, accrued, prepaid, unearned in ONE batch.
- If capex, principal repaid, or withdrawals are unknown, ask — these are below the net-income line and are common hidden cash drains; do not assume zero silently (note the assumption if the founder confirms zero).
- If depreciation is missing, pull from the IS; it is a required add-back.
- Never infer a cash figure to force the bridge to reconcile; if it doesn't reconcile, report the gap (see Decision Rules).

## Diagnostic Questions
1. Is net income positive while operating cash flow is negative or much smaller?
2. How much cash did each working-capital movement consume or release (ΔA/R, ΔInventory, ΔA/P, ΔAccrued, ΔPrepaid, ΔUnearned)?
3. How much cash left below the profit line via capex, principal repayment, and owner withdrawals?
4. Which single driver is the largest cash consumer this period?
5. Are collections slower than customer terms / are we paying suppliers faster than needed?
6. Is this a one-time growth-driven consumption (financeable) or a structural leak (must fix operations)?

## Analysis Framework
Builds the indirect-method operating-cash bridge, then extends it to a full cash bridge including investing and financing, and ranks drivers by absolute cash impact.

**Bridge structure (each item is a cash driver):**
1. Start: Net Income.
2. + Depreciation (non-cash add-back; the real outflow was the earlier capex).
3. − Increase in A/R (revenue booked, cash not collected) / + decrease.
4. − Increase in Inventory (cash tied in unsold goods) / + decrease.
5. − Increase in Prepaid (cash paid ahead) / + decrease.
6. + Increase in A/P (supplier financing, cash conserved) / − decrease.
7. + Increase in Accrued (expense incurred, cash not yet paid) / − decrease.
8. + Increase in Unearned Revenue (cash received ahead of earning) / − decrease.
9. = Operating Cash Flow.
10. − Capex (Investing).
11. − Principal Repaid − Dividends/Withdrawals (+ debt draws / equity raised) (Financing).
12. = Net Change in Cash → reconcile to Ending − Beginning Cash.

Then rank all line items 3–11 by |cash impact| to identify the dominant driver(s). Interpret whether the drain is growth-driven (A/R/inventory scaling with sales — bridgeable with financing) or structural (collections/payments/obsolescence — must be fixed operationally).

## Calculations
- **Operating Cash Flow (indirect)** = Net Income + Depreciation − ΔA/R − ΔInventory − ΔPrepaid + ΔA/P + ΔAccrued + ΔUnearned.
  - Δ = current − prior. A rise in an asset (A/R, inventory, prepaid) uses cash (negative). A rise in a liability (A/P, accrued, unearned) sources cash (positive).
- **Net Change in Cash** = Operating CF − Capex − Principal Repaid − Dividends/Withdrawals (+ debt draws + equity raised).
- **Reconciliation check** = Beginning Cash + Net Change in Cash must equal Ending Cash (|difference| should be 0; flag if not).
- **Cash Conversion Cycle context** = DIO + DSO − DPO (from `working-capital-optimizer` inputs) to size how many days cash is tied up.
- **Driver share %** = |driver cash impact| / Σ|all driver cash impacts| × 100 (for ranking).
- **Profit-to-cash gap** = Net Income − Operating Cash Flow (the amount profit overstates cash this period).

Worked reference points from source: net income +$27,000 with operating CF −$52,500; net income +$2,100 with operating CF −$9,600 — both driven by working-capital swings, confirming profit ≠ cash.

## Decision Rules
- IF Net Income > 0 AND Operating CF < 0 → THEN investigate the bridge; the profit is not yet cash.
- IF the dominant driver is rising A/R AND A/R days > customer terms → THEN collection problem; hand to `working-capital-optimizer` (tighten collections).
- IF the dominant driver is rising Inventory with flat/falling sales → THEN overstocking/obsolescence; hand to `working-capital-optimizer` (reduce purchasing / liquidate).
- IF the dominant driver is falling/low A/P AND supplier terms allow longer → THEN paying too fast; extend payables within terms to conserve cash.
- IF the dominant driver is capex → THEN a one-time Category-1 investment drained cash; check runway (`cash-runway-monitor`) and financing options (approval required to borrow).
- IF the dominant driver is principal repayment → THEN debt service is consuming cash below the profit line; check `debt-service-and-covenant-analysis`.
- IF the drain is growth-driven (A/R and inventory scaling with rising sales) → THEN it is financeable working-capital need; ensure liquidity to bridge, do NOT mistake it for a broken business.
- IF Operating CF is negative for multiple consecutive periods → THEN a capital infusion is coming; surface early and run `cash-runway-monitor`.
- IF the bridge does not reconcile to ending cash → THEN a cash item is mis-bucketed or omitted; report the gap and re-run `financial-statement-analysis`.

## Procedure
1. Confirm net income is positive (else redirect to earnings diagnosis).
2. Load current and prior balances; compute each Δ working-capital item.
3. Build the operating-cash bridge (add-backs and working-capital changes).
4. Extend to net change in cash (capex, principal, withdrawals, draws).
5. Reconcile computed net change to Ending − Beginning cash; flag any gap.
6. Rank drivers by |cash impact| and compute driver share %.
7. Classify each dominant driver as growth-driven vs. structural.
8. Produce the bridge, ranked drivers, classification, and fixes with handoffs.
9. Write the reconciled cash bridge to `finance.cash_flow` (L1 staged); record findings in `decisions`.

## Output
```yaml
output:
  period: string
  profit_to_cash_gap: number                 # NI − Operating CF
  bridge:
    net_income: number
    add_depreciation: number
    delta_ar: number                         # negative = used cash
    delta_inventory: number
    delta_prepaid: number
    delta_ap: number                         # positive = sourced cash
    delta_accrued: number
    delta_unearned: number
    operating_cash_flow: number
    less_capex: number
    less_principal_repaid: number
    less_dividends_withdrawals: number
    add_debt_draws_equity: number
    net_change_in_cash: number
  reconciliation: {beginning_cash, ending_cash, computed_ending_cash, reconciles: boolean, gap: number}
  ranked_drivers:                            # largest cash consumer first
    - {driver: string, cash_impact: number, share_pct: number, classification: enum[growth_driven, structural]}
  diagnosis: string                          # plain-language "why no cash"
  fixes: list                                # each with target driver and handoff skill
  handoffs: list
```

## Recommendations
Ranked by (1) cash freed per unit of effort — attack the largest structural driver first; (2) reversibility and speed — collections and payable-timing fixes are fast and low-risk; (3) whether the drain is growth-driven (finance it) vs. structural (fix operations). Each fix names the driver, the expected cash release, and the skill that executes it. Distinguish clearly between "raise financing to bridge growth" (requires founder approval) and "operational tightening" (can proceed as tasks).

## Execution Opportunities
- Write the reconciled cash bridge to `finance.cash_flow` (reversible, LOW; L1 staged).
- Create internal tasks for each fix (e.g., "send collection reminders on A/R > terms") (reversible, LOW).
- Draft collection-reminder templates for the founder to review (reversible, LOW; sending to customers requires approval).
- Update the cash dashboard and trigger `cash-runway-monitor` if operating CF is negative (reversible, LOW).

## Human Approval Requirements
- Analysis and bridge construction: always allowed.
- Raising financing, drawing on a line of credit, taking on debt, or any money movement to bridge the gap: ALWAYS requires founder approval.
- Sending collection communications to customers or changing customer/supplier terms: requires founder approval (external-facing commitment).
- Changing standing payment configuration (auto-pay, payment runs): requires founder approval.

## Escalation Conditions
- Operating cash flow negative across multiple periods with limited runway → founder immediately + recommend accountant; run `cash-runway-monitor`.
- Bridge won't reconcile due to suspected misstatement → accountant/CPA.
- Cash shortfall threatens payroll or supplier continuity → founder immediately (highest priority).
- Any need to borrow or restructure debt → founder + accountant.

## KPIs
- Bridge reconciles to ending cash (target 100%).
- Dominant driver correctly identified (validated against subsequent period).
- Cash freed after recommended fixes vs. projected.
- Reduction in the profit-to-cash gap over subsequent periods.

## Monitoring
- Track operating cash flow and the profit-to-cash gap every period.
- Monitor the ranked drivers to confirm fixes are working (e.g., A/R days falling).
- Alert if a new driver becomes dominant or if operating CF turns/stays negative.

## Follow-Up
- Re-run each close, and whenever profit and cash diverge again.
- Re-run after any fix to measure cash actually freed.

## Related Skills
- `financial-statement-analysis` (source data; re-run if bridge won't reconcile).
- `working-capital-optimizer` (executes A/R/inventory/A/P fixes).
- `cash-runway-monitor` (if operating CF is negative).
- `debt-service-and-covenant-analysis` (if principal repayment dominates).
- `financial-forecast-builder` (project the cash effect of fixes).

## Guardrails
- Never conclude "the business is fine" from positive net income alone — cash is the survival test.
- Never infer a cash figure to force reconciliation; report the gap.
- Distinguish growth-driven (financeable) from structural (must fix) drains; do not recommend borrowing to cover a structural leak.
- Any money movement, borrowing, or customer/supplier communication requires founder approval.
- Confidential financial data; audited writes to permitted namespaces only.

## Example
**Founder input:** "Q3 net income was +$27,000 but our bank balance dropped $52,500 — where did the money go?" Prior→current: A/R $40k→$95k, Inventory $30k→$70k, A/P $25k→$20k, Accrued flat, no capex, $9,500 principal repaid, no withdrawals; depreciation $5,000.

**Skill reasoning:** Bridge: NI $27,000 + Dep $5,000 − ΔA/R $55,000 − ΔInventory $40,000 + ΔA/P (−$5,000, a decrease → uses cash) = Operating CF = 27,000 + 5,000 − 55,000 − 40,000 − 5,000 = −$68,000. Less principal $9,500 → net change −$77,500. Reconciliation: this exceeds the reported −$52,500 drop → gap flagged; ask founder for a possible debt draw or missing item (illustrates the reconcile-don't-plug rule). Ranked drivers: ΔA/R $55k (structural — A/R days now well beyond terms), ΔInventory $40k (structural — building faster than sales), ΔA/P −$5k (paying too fast). Classification: mostly structural.

**Output:** "You are profitable but cash-negative because $95k is sitting in receivables and $70k in inventory, and you paid down A/P instead of using it. Fixes: accelerate collections on overdue A/R, pause purchasing until inventory turns, extend A/P to supplier terms. There is also a $25,000 reconciliation gap — confirm any loan draw or omitted transaction." Handoffs: `working-capital-optimizer`, `financial-statement-analysis` (reconcile gap), `cash-runway-monitor`.

**Executed vs. approval:** bridge written to `finance.cash_flow`, tasks and draft collection reminders created (L1); sending reminders to customers and any borrowing held for founder approval.

## Provenance
SOURCE. Derives from the Forecasting/Cash knowledge ("profitable but no cash" diagnostics, net-income→operating-cash bridge, indirect-method formula, worked examples of positive NI with negative operating CF) and the Statements & Ratios knowledge (operating cash flow identity, working-capital timing accounts). Branding stripped and generalized per PROVENANCE_MAP.
