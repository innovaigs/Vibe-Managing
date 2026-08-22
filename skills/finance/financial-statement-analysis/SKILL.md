---
name: financial-statement-analysis
domain: finance
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [finance.income_statement, finance.balance_sheet, finance.cash_flow, finance.accounts, company, offerings]
writes: [finance.income_statement, finance.balance_sheet, finance.cash_flow, decisions]
related_skills: [financial-ratio-analysis, cash-flow-diagnostic, working-capital-optimizer, financial-forecast-builder]
owned_by_agents: [cfo-agent, business-analyst-agent]
---

# Skill: Financial Statement Analysis

## Purpose
Build, validate, and interpret the three core financial statements — Income Statement (IS), Balance Sheet (BS), and Statement of Cash Flows (SCF) — so the founder always has a reconciled, trustworthy picture of profitability, resources, and cash. Includes constructing statements from a raw transaction log, cross-statement reconciliation, common-size recasting, and multi-year trend analysis.

## When to Use
- "Turn my transactions/bookkeeping export into real financial statements."
- "Do my statements actually tie out / balance?"
- "What do my financials say about the business — what's the story?"
- "Show me the trend over the last 3 years / which cost lines are creeping up."
- Month-end or year-end close review; before a loan application, investor conversation, or valuation.
- As the upstream data-prep step feeding ratio analysis, cash diagnostics, or forecasting.

## When NOT to Use
- You need ratios, benchmarks, or covenant flags → use `financial-ratio-analysis`.
- The question is "profitable but no cash, why?" → use `cash-flow-diagnostic`.
- You need forward-looking projections → use `financial-forecast-builder`.
- The task requires GAAP judgment calls, tax treatment, entity accounting, revenue-recognition rulings, or an audit opinion → escalate to an accountant/CPA. This skill organizes and interprets; it does not certify GAAP compliance.

## Required Context
- Business type (product vs. service) and reporting basis (cash vs. accrual). Read from `company`.
- Chart of accounts or transaction log with beginning balances, OR pre-built statement figures. Read from `finance.income_statement`, `finance.balance_sheet`, `finance.cash_flow`, `finance.accounts`.
- Period definitions (month/quarter/year) and prior-period comparatives for trend work.
- Fixed-asset register with cost and useful life (for depreciation) if building from transactions.

## Inputs
```yaml
input:
  mode: enum[build_from_transactions, validate_existing, interpret, common_size, trend]  # what to do
  business_type: enum[product, service]        # service uses Cost of Services (salaries) not COGS
  reporting_basis: enum[accrual, cash]         # accrual assumed unless stated
  period: string                               # e.g. "2026-Q2" or "FY2025"
  beginning_balances:                          # required for build_from_transactions
    cash: number
    accounts_receivable: number
    inventory: number
    prepaid_expenses: number
    fixed_assets_gross: number
    accumulated_depreciation: number
    accounts_payable: number
    accrued_expenses: number
    short_term_debt: number
    long_term_debt: number
    common_stock: number
    retained_earnings: number
  transactions:                                # required for build_from_transactions
    - {date: string, description: string, amount: number, accounts_affected: list}
  statements:                                  # required for validate/interpret/common_size/trend
    income_statement: {revenue, cogs, opex{selling_marketing, g_and_a, r_and_d, depreciation}, interest_expense, tax}
    balance_sheet: {current_assets{...}, fixed_assets{gross, accum_dep}, current_liabilities{...}, long_term_debt, equity{common_stock, retained_earnings}}
    cash_flow: {operating, investing, financing}
  prior_periods: list                          # for trend mode: array of prior statements
  fixed_asset_register:                        # for straight-line depreciation
    - {asset: string, cost: number, useful_life_years: number, in_service_date: string}
```

## Missing Information Protocol
- If beginning balances are missing for `build_from_transactions`, pull the prior period's ending balance sheet from `finance.balance_sheet`; if none exists, ask the founder for opening balances in ONE batch (list every account needed).
- If a transaction's account mapping is ambiguous, do NOT guess the accounting treatment — list the ambiguous items and ask the founder or route the classification question to the accountant.
- If useful life for depreciation is unknown, ask; never assume a life that changes reported income without confirmation.
- Never fabricate figures to force a balance. If the sheet will not balance, report the imbalance and its size (see Decision Rules), do not plug it silently.
- If reporting basis is unstated, assume accrual, state the assumption explicitly in the output.

## Diagnostic Questions
1. Is the business profitable this period, and is profit rising or falling vs. prior periods?
2. Does the balance sheet balance (Assets = Liabilities + Equity), and does net income tie to the change in retained earnings?
3. Does ending cash on the SCF equal cash on the BS?
4. Which income-statement lines are growing faster/slower than revenue (common-size drift)?
5. Is the business generating positive operating cash flow, or funding itself from investing/financing?
6. What one transaction type or account is driving the biggest period-over-period change?

## Analysis Framework
Uses the Balance Sheet Equation (BSE) construction engine and common-size/trend analysis.

**A. Build-from-transactions (BSE grid).** Lay out columns: Cash | A/R | Inventory | Prepaid | Fixed Assets (gross) | Accum. Dep. || A/P | Accrued | Short-term Debt | Long-term Debt || Common Stock | Retained Earnings. Post each transaction as offsetting entries so that after every row `Assets = Liabilities + Equity` still holds. Then extract:
- **Income Statement** = the Retained Earnings column entries (revenues positive, expenses negative).
- **Balance Sheet** = the ending (bottom) row of balances.
- **Statement of Cash Flows** = the Cash column entries, bucketed Operating / Investing / Financing.

**B. Cash-flow bucketing rules.** Operating = cash from customers; cash paid to suppliers, employees, rent, utilities, insurance, interest, taxes. Investing = purchase/sale of fixed assets and intangibles. Financing = owner contributions, dividends/withdrawals, and borrowing/repaying interest-bearing debt (loans, credit lines, credit cards). A/P and accrued expenses are Operating, NOT Financing.

**C. Validation (three-way tie-out).** (1) BS balances; (2) net income from IS equals change in retained earnings; (3) ending cash on SCF equals cash on BS.

**D. Common-size.** IS: every line ÷ Revenue. BS: every line ÷ Total Assets. Surfaces margin structure and cost creep normalized for size.

**E. Trend.** Place periods side by side, compute period-over-period growth and common-size deltas, flag lines drifting adversely (classic pattern: revenue up while net income down).

## Calculations
Variable key: R = Revenue; COGS = cost of goods sold (service: Cost of Services = delivery salaries); Opex = operating expenses; D = depreciation; Int = interest expense; T = tax; NI = net income.

- **Gross Profit** = R − COGS. **Gross Margin %** = Gross Profit / R.
- **Operating Income (EBIT)** = Gross Profit − Total Opex.
- **EBITDA** = EBIT + D&A.
- **EBT (pre-tax)** = EBIT − Int.
- **Net Income** = EBT − T.
- **Straight-line Depreciation** = Asset Cost / Useful Life (years).
- **Net Fixed Assets** = Gross Fixed Assets − Accumulated Depreciation.
- **Balance Sheet Identity** = Assets = Liabilities + Owners' Equity (must hold per transaction and in total).
- **Ending Retained Earnings** = Beginning R/E + Net Income − Dividends.
- **Operating Cash Flow (indirect)** = NI + D ± ΔWorking-capital items (−ΔA/R, −ΔInventory, +ΔA/P, +ΔAccrued, −ΔPrepaid, +ΔUnearned).
- **Change in Cash** = Operating CF + Investing CF + Financing CF; **Ending Cash** = Beginning Cash + Change in Cash.
- **Common-size IS line** = Line / Revenue × 100. **Common-size BS line** = Line / Total Assets × 100.
- **Period-over-period growth %** = (Current − Prior) / Prior × 100.

**Validation thresholds:** balance imbalance must be exactly 0 (report any |imbalance| > 0). Rounding differences up to $1 are acceptable if all inputs were rounded; flag anything larger as an error, not a rounding artifact.

## Decision Rules
- IF |Assets − (Liabilities + Equity)| > 0 → THEN the statements do NOT tie out; report the exact imbalance and the most likely offending account; do NOT plug it. Route to accountant if the cause is a classification/treatment question.
- IF NI (from IS) ≠ ΔRetained Earnings (excluding dividends) → THEN a revenue/expense item is miscategorized or a dividend is unrecorded; flag for correction.
- IF Ending Cash (SCF) ≠ Cash (BS) → THEN a cash transaction is mis-bucketed or omitted; reconcile before publishing.
- IF a cost line rises as a % of revenue across periods (common-size) → THEN flag it as cost creep and name the specific line.
- IF revenue grew but net income fell → THEN run common-size to identify which line (COGS or a specific opex) absorbed the growth; hand off to `financial-ratio-analysis` for margin diagnosis.
- IF Operating CF is negative while NI is positive → THEN hand off to `cash-flow-diagnostic` (profit ≠ cash).
- IF reporting basis is cash but the founder needs A/R, A/P, or accrual insight → THEN note that timing accounts are not captured and recommend accrual conversion or an accountant.

## Procedure
1. Determine `mode` and `business_type`; confirm reporting basis (state assumption if unstated).
2. **build_from_transactions:** load beginning balances → post each transaction to the BSE grid, checking A = L + E after every row → compute period depreciation from the fixed-asset register → extract IS (R/E column), BS (ending row), SCF (cash column, bucketed).
3. **validate_existing:** run the three-way tie-out (balance, NI↔ΔR/E, ending cash↔BS cash). Report each check pass/fail with the numeric difference.
4. **common_size:** recast IS as % of revenue and BS as % of total assets.
5. **trend:** align periods, compute growth and common-size deltas, flag adverse drifts.
6. **interpret:** narrate the story — profitability, resource/funding mix, cash generation — citing the specific line or ratio behind each finding.
7. Write reconciled statements to `finance.*` (staged for approval — L1) and record findings in `decisions`.
8. Hand off to the appropriate downstream skill (ratios, cash diagnostic, forecast) as flagged.

## Output
```yaml
output:
  period: string
  reporting_basis: enum[accrual, cash]
  income_statement:
    revenue: number
    cogs: number
    gross_profit: number
    gross_margin_pct: number
    operating_expenses: {selling_marketing, g_and_a, r_and_d, depreciation}
    ebit: number
    ebitda: number
    interest_expense: number
    ebt: number
    tax: number
    net_income: number
  balance_sheet:
    current_assets: {cash, accounts_receivable, inventory, prepaid, other}
    fixed_assets: {gross, accumulated_depreciation, net}
    total_assets: number
    current_liabilities: {accounts_payable, accrued, short_term_debt, other}
    long_term_debt: number
    total_liabilities: number
    equity: {common_stock, retained_earnings, total}
    balances: boolean
  cash_flow:
    operating: number
    investing: number
    financing: number
    net_change: number
    ending_cash: number
  validation:
    balance_sheet_balances: boolean
    imbalance_amount: number
    ni_ties_to_retained_earnings: boolean
    ending_cash_ties_to_bs: boolean
  common_size: {income_statement: map, balance_sheet: map}   # optional
  trend_flags: list                                          # adverse drifts, each citing the line
  narrative: string                                          # cited interpretation
  handoffs: list                                             # downstream skills recommended
```

## Recommendations
Recommendations are prioritized by (1) integrity first — any failed tie-out is fixed before interpretation is trusted; (2) materiality — the largest common-size drifts and period-over-period swings; (3) actionability — each flagged line pairs with a concrete next step (e.g., "COGS rose from 58% to 63% of revenue → investigate supplier pricing or mix; see `financial-ratio-analysis`"). Every finding cites the exact line/figure that triggered it.

## Execution Opportunities
- Write reconciled statements into Business Memory `finance.*` (reversible, LOW — staged as L1 draft for founder confirmation).
- Create internal tasks for each unreconciled item or cost-creep flag (reversible, LOW).
- Update an internal financial dashboard with the period's statements and common-size view (reversible, LOW).
- Draft a plain-language monthly financial summary for the founder (reversible, LOW; sending externally requires approval).

## Human Approval Requirements
- Analysis, construction, validation, and interpretation: always allowed (no money moves).
- Committing statements as the official/finalized record of the period requires founder confirmation.
- Any correction that changes reported income, tax basis, or an accounting treatment: hold for accountant/CPA review before it is treated as final.
- No action in this skill moves money, takes on debt, commits budget, or files anything — those are out of scope here and always require approval elsewhere.

## Escalation Conditions
- GAAP treatment, revenue recognition, entity/tax accounting, or classification uncertainty → accountant/CPA.
- Statements will not tie out and the cause is not a data-entry error → accountant/CPA + founder.
- Suspected material misstatement or fraud indicators → founder immediately, then accountant.
- Low confidence in input data quality → surface uncertainty to founder; do not present unreliable statements as fact.

## KPIs
- Three-way tie-out pass rate (target 100% before publishing).
- Balance imbalance = $0 on published statements.
- Time from transaction log to reconciled statements.
- Number of cost-creep/adverse drifts surfaced that the founder acts on.
- Downstream reuse: statements consumed cleanly by ratio/forecast skills without rework.

## Monitoring
- Watch for period-over-period swings > 20% in any major line and re-flag.
- Re-run validation whenever underlying transactions change.
- Track whether flagged cost creep reverses or worsens in subsequent periods.

## Follow-Up
- Run every close (monthly/quarterly/annual) and before any loan, investor, valuation, or budgeting exercise.
- Re-run immediately if bookkeeping data is corrected or a prior period is restated.

## Related Skills
- `financial-ratio-analysis` (consumes these statements for ratios/benchmarks).
- `cash-flow-diagnostic` (when NI and operating cash diverge).
- `working-capital-optimizer` (uses A/R, inventory, A/P balances).
- `financial-forecast-builder` (uses the base period as its anchor).
- `budget-builder` (variance vs. actuals).

## Guardrails
- Never plug an imbalance to force a tie-out; report it.
- Never assume account classifications, useful lives, or reporting basis that change reported results — confirm first.
- Do not certify GAAP compliance or issue anything resembling an audit opinion; this is management analysis.
- Treat low-quality/low-confidence inputs as uncertain and label them; do not present estimates as audited fact.
- Financial data is confidential; write only to permitted `finance.*` namespaces; writes are audited.

## Example
**Founder input:** "Here are my Q2 opening balances and 30 transactions from my bookkeeping export — build my statements and tell me if they tie out." Business type: product, accrual. Opening cash $40,000; among the transactions: $120,000 credit sales, $70,000 COGS purchased on account, $12,000 cash collected on old A/R, $8,000 rent paid, $5,000 equipment bought for cash (5-yr life), $10,000 loan principal repaid.

**Skill reasoning:** Posts each to the BSE grid. Depreciation on the new $5,000 asset for the quarter = 5,000 / 5 / 4 = $250. Extracts: Revenue $120,000; COGS $70,000 → Gross Profit $50,000; less rent $8,000 and depreciation $250 → EBIT $41,750 (no interest/tax this simplified period). Cash column: +$12,000 collections, −$8,000 rent, −$5,000 equipment (Investing), −$10,000 loan repayment (Financing). Operating CF = NI $41,750 + Dep $250 − ΔA/R (rise $108,000 from $120k booked less $12k collected) + ΔA/P (rise $70,000) = −$36,000. Checks: BS balances (imbalance $0); NI $41,750 = ΔRetained Earnings; ending cash on SCF equals BS cash.

**Output:** reconciled IS/BS/SCF, all three tie-out checks pass, plus a flag: "Operating cash flow is −$36,000 despite $41,750 net income — driven by a $108,000 rise in A/R. Hand off to `cash-flow-diagnostic`."

**Executed vs. approval:** statements staged to `finance.*` and dashboard updated automatically (L1 draft); finalizing them as the official Q2 record held for founder confirmation.

## Provenance
SOURCE. Derives from the Finance — Statements & Ratios knowledge (Balance Sheet Equation construction engine, three-statement definitions, cash-flow bucketing, common-size and trend frameworks) and the Forecasting/Cash knowledge (BSE transaction engine, statement reconciliation). Branding stripped and generalized to function per PROVENANCE_MAP.
