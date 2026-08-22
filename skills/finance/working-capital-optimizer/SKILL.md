---
name: working-capital-optimizer
domain: finance
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [finance.working_capital, finance.income_statement, finance.balance_sheet, company, offerings, customers]
writes: [finance.working_capital, decisions]
related_skills: [cash-flow-diagnostic, financial-ratio-analysis, cash-runway-monitor, financial-forecast-builder]
owned_by_agents: [cfo-agent, business-analyst-agent]
---

# Skill: Working Capital Optimizer

## Purpose
Measure the cash conversion cycle (DSO / DIO / DPO), quantify how much cash is trapped in receivables and inventory or freed by payables, and recommend concrete levers to shorten the cycle and release cash — without harming supplier relationships or sales. Turns the biggest hidden cash lever in most small businesses into a prioritized action plan.

## When to Use
- "How much cash is stuck in receivables and inventory, and how do I free it?"
- "Our cash conversion cycle is too long — what do I fix first?"
- "Are we collecting too slowly / paying suppliers too fast / holding too much stock?"
- After `cash-flow-diagnostic` identifies A/R, inventory, or A/P as a dominant cash driver, or `cash-runway-monitor` needs a fast cash-preserving lever.

## When NOT to Use
- Explaining the profit-vs-cash gap holistically → `cash-flow-diagnostic`.
- Computing the full ratio panel → `financial-ratio-analysis`.
- Projecting future working-capital balances in a full model → `financial-forecast-builder` (this skill supplies the days drivers).
- Renegotiating supplier contracts or customer terms with the counterparty → founder approval (external commitment).

## Required Context
- COGS and revenue (annualized or period, consistent). Read from `finance.income_statement`.
- A/R, inventory, and A/P balances (current, and prior for averages). Read from `finance.balance_sheet`, `finance.working_capital`.
- Customer credit terms granted and supplier terms received (days). Read from `offerings`, `company`.
- Industry benchmark days for DSO/DIO/DPO if available.

## Inputs
```yaml
input:
  period_days: integer                   # 365 for annual figures
  revenue: number
  credit_sales: number                   # falls back to revenue if unavailable
  cogs: number
  accounts_receivable: number
  inventory: number                      # 0 / N/A for pure service
  accounts_payable: number
  use_averages: boolean                  # average of opening+closing balances
  opening_balances: {accounts_receivable, inventory, accounts_payable}   # if use_averages
  customer_terms_days: number            # terms granted to customers
  supplier_terms_days: number            # terms received from suppliers
  business_type: enum[product, service]
  industry_benchmarks: {dso, dio, dpo}   # optional
  target_cash_release: number            # optional goal
```

## Missing Information Protocol
- If `credit_sales` is unknown, use total revenue for DSO and note the substitution.
- If `customer_terms_days` / `supplier_terms_days` are unknown, ask the founder once — the actual-vs-terms gap is the core diagnostic and cannot be assumed.
- For service businesses, treat inventory (DIO) as N/A and focus on DSO and DPO.
- If only period-end balances exist, use them and note that averages would be more accurate.
- Never assume a benchmark days figure; if no benchmark is provided, compare actual-vs-terms and trend only.

## Diagnostic Questions
1. How many days is cash tied up in the cash conversion cycle (DIO + DSO − DPO)?
2. Are we collecting faster or slower than the terms we granted (DSO vs. customer terms)?
3. Are we paying suppliers faster than we need to (DPO vs. supplier terms)?
4. Is inventory turning at an industry-appropriate rate, or is cash trapped in slow/obsolete stock?
5. How much cash would each 1-day improvement in DSO/DIO/DPO release?
6. Which lever frees the most cash with the least risk to sales or supply?

## Analysis Framework
Compute the three cycle components, benchmark each against terms/industry, quantify cash trapped and cash-per-day, then rank levers by cash freed and risk.

- **DSO (collections):** compare to customer terms. DSO > terms = collection problem (money earned, not collected). Averages hide concentration — check whether a few slow/large accounts drag the mean.
- **DIO (inventory):** compare to industry and to sales trend. Rising DIO with flat/falling sales = overstocking/obsolescence.
- **DPO (payments):** compare to supplier terms. Paying faster than terms (DPO < terms) forgoes free trade credit — a cash lever. Stretching past terms conserves cash short-term but risks service/quality degradation or stopped shipments.
- **Cash conversion cycle (CCC):** DIO + DSO − DPO. Shorter = less working-capital need, better liquidity. Can be negative (collect before paying suppliers — rare).
- **Too-liquid check:** very low CCC / very high current ratio can mean idle cash or unused free trade credit — also a form of poor working-capital management.

## Calculations
- **A/R Turnover** = Credit Sales / A/R. **DSO** = 365 / A/R Turnover = A/R / (Revenue/365).
- **Inventory Turnover** = COGS / Inventory. **DIO** = 365 / Inventory Turnover = Inventory / (COGS/365).
- **A/P Turnover** = COGS / A/P. **DPO** = 365 / A/P Turnover = A/P / (COGS/365).
- **Cash Conversion Cycle (CCC)** = DIO + DSO − DPO.
- **Cash per day of DSO** = Revenue / 365 (each day of DSO reduction releases ~this much A/R cash).
- **Cash per day of DIO** = COGS / 365.
- **Cash per day of DPO** = COGS / 365 (each additional day of DPO, within terms, retains ~this much).
- **Cash released by a target** = ΔDSO × (Revenue/365) + ΔDIO × (COGS/365) + ΔDPO × (COGS/365).
- **A/R needed to hit target DSO** = target_DSO × (Revenue/365); cash freed = current A/R − that.
- **Balances-from-days (for forecasting handoff):** A/R = (Revenue/365) × DSO; Inventory = (COGS/365) × DIO; A/P = (COGS/365) × DPO.

Worked reference (source): DIO 61.1 + DSO 52.8 − DPO 81.6 = CCC 32.3 days.

## Decision Rules
- IF DSO > customer terms → THEN collection problem; tighten collections (reminders, deposits, milestone billing, early-pay discounts); review individual slow/large accounts (averages hide concentration).
- IF DIO rising with flat/falling sales → THEN overstocking/obsolescence; reduce purchasing, run promotions, or liquidate slow SKUs.
- IF DPO < supplier terms → THEN paying too fast; extend payments to (not beyond) supplier terms to retain free trade credit — quantify cash retained.
- IF DPO materially > supplier terms → THEN stretching is short-term only; warn of supply-disruption/quality risk; do not recommend as a durable fix.
- IF CCC is long/growing → THEN working-capital financing pressure rises; prioritize the highest cash-per-day lever with acceptable risk.
- IF CCC is negative or very low AND current ratio very high → THEN check for idle cash / unused trade credit (too-liquid is also suboptimal).
- IF an early-pay discount offered by a supplier exceeds the cost of the cash used → THEN taking it can beat holding the payable (analysis only; paying early is a money movement requiring approval).
- IF target_cash_release is set → THEN solve for the DSO/DIO/DPO changes that reach it and present the least-risk combination.

## Procedure
1. Load revenue, COGS, and A/R/inventory/A/P balances (averages if available).
2. Compute DSO, DIO, DPO, and CCC; mark DIO N/A for service.
3. Benchmark each against terms and industry; flag actual-vs-terms gaps.
4. Compute cash-per-day for each lever and the cash trapped vs. a reasonable target.
5. Rank levers by cash freed and risk (collections and payable-timing usually lead; inventory next).
6. If a target is set, solve for the days changes and cash released.
7. Emit CCC, gaps, quantified levers, and a prioritized plan with handoffs.
8. Write DSO/DIO/DPO/CCC to `finance.working_capital` (L1 staged); record findings in `decisions`.

## Output
```yaml
output:
  period: string
  dso_days: number
  dio_days: number                        # N/A for service
  dpo_days: number
  cash_conversion_cycle_days: number
  vs_terms: {dso_minus_customer_terms: number, dpo_minus_supplier_terms: number}
  cash_per_day: {dso: number, dio: number, dpo: number}
  cash_trapped_estimate: number           # vs. reasonable target
  levers:                                 # ranked
    - {lever: string, target_days: number, cash_released: number, risk: enum[low, medium, high], reversibility: enum[reversible, recoverable, irreversible]}
  recommended_plan: list
  narrative: string
  handoffs: list
```

## Recommendations
Ranked by cash freed per unit of risk: (1) collect overdue A/R and tighten collection process (low risk, fast); (2) extend A/P to — never beyond — supplier terms (low risk if within terms); (3) reduce/liquidate slow inventory and cut over-ordering (medium risk, protects against obsolescence); (4) restructure customer terms or require deposits/milestone billing (medium risk — affects sales, external). Each lever states cash released and risk. Flag clearly that changing customer/supplier terms and paying early/late are external commitments or money movements requiring approval.

## Execution Opportunities
- Write DSO/DIO/DPO/CCC to `finance.working_capital` (reversible, LOW; L1 staged).
- Create internal tasks for each lever (e.g., "call top 5 overdue accounts") (reversible, LOW).
- Draft collection reminder / statement templates for founder review (reversible, LOW; sending to customers requires approval).
- Build an aged-receivables and slow-inventory report (reversible, LOW).
- Feed the days drivers into `financial-forecast-builder` (reversible, LOW).

## Human Approval Requirements
- Analysis, cash-trapped quantification, and lever ranking: always allowed.
- Sending collection communications to customers, or changing customer/supplier terms: requires founder approval (external commitment).
- Paying a supplier early to capture a discount, or any change to payment timing that moves money: ALWAYS requires founder approval.
- Liquidating inventory below cost or committing to purchasing changes with budget impact: requires founder approval.

## Escalation Conditions
- A few concentrated accounts driving DSO with collectability doubt → founder; consider `risk` concentration review; possible collections/legal escalation (attorney) for large delinquencies.
- Supplier already threatening to stop shipments over stretched A/P → founder immediately.
- Inventory obsolescence write-down needed → accountant/CPA (accounting treatment).
- Cash trap is severe and runway short → founder + `cash-runway-monitor`.

## KPIs
- CCC reduction (days) vs. baseline.
- Cash actually freed vs. projected by lever.
- DSO closing toward customer terms; DPO reaching (not exceeding) supplier terms.
- Inventory days trending to industry norm; obsolescence avoided.

## Monitoring
- Track DSO/DIO/DPO/CCC every period; confirm levers are working.
- Watch DPO to ensure it does not drift past supplier terms.
- Monitor aged-receivables concentration and slow-moving inventory.

## Follow-Up
- Re-run monthly/quarterly and after any collection, purchasing, or terms change.
- Re-run when `cash-runway-monitor` or `cash-flow-diagnostic` flags a working-capital driver.

## Related Skills
- `cash-flow-diagnostic` (identifies which driver dominates).
- `financial-ratio-analysis` (cycle ratios in context).
- `cash-runway-monitor` (working capital as a runway lever).
- `financial-forecast-builder` (uses days drivers to project balances).

## Guardrails
- Never recommend stretching A/P beyond supplier terms as a durable fix — flag the supply-disruption risk.
- Averages hide concentration — always check individual large/slow accounts before concluding "collections are fine/broken."
- Changing customer/supplier terms, paying early/late, and collection outreach are external/money actions requiring founder approval.
- Do not recommend liquidating inventory below cost without flagging the accounting/tax implications for an accountant.
- Confidential financial and customer data; audited writes to permitted namespaces.

## Example
**Founder input:** "Cash is tight. I have $394k in receivables, $114k inventory, $103k payables. Annual revenue $2.72M, COGS $1.70M. I give customers net-30 and my suppliers give me net-45. What do I fix first?" Product business.

**Skill reasoning:** DSO = 394k/(2.72M/365) = 52.9 days (vs. 30 granted → 23 days too slow). DIO = 114k/(1.70M/365) = 24.5 days. DPO = 103k/(1.70M/365) = 22.1 days (vs. 45 available → paying 23 days too fast). CCC = 24.5 + 52.9 − 22.1 = 55.3 days. Cash-per-day: DSO $7,452; DPO $4,658. Levers: (1) collect A/R to net-30 → ΔDSO 23 days × $7,452 ≈ $171k freed (low risk, fast). (2) extend A/P to net-45 → ΔDPO 23 days × $4,658 ≈ $107k retained (low risk, within terms). Combined ≈ $278k of cash released, cutting CCC from 55 to ~9 days. Inventory is already lean — leave it.

**Output:** CCC 55.3 days; top plan: "Tighten collections to net-30 (frees ~$171k) and slow payments to your full net-45 terms (retains ~$107k) — together ~$278k without touching sales or supply." Handoffs: `cash-runway-monitor` (apply freed cash to runway).

**Executed vs. approval:** metrics written, aged-A/R report and collection tasks/templates created (L1); sending reminders to customers and changing payment timing held for founder approval.

## Provenance
SOURCE. Derives from the Statements & Ratios and Forecasting/Cash knowledge (cash operating cycle DSO/DIO/DPO formulas, actual-vs-terms diagnostics, balances-from-days drivers, funding-shortfall working-capital levers, too-liquid warning). Branding stripped and generalized per PROVENANCE_MAP.
