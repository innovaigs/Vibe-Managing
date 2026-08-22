---
name: financial-ratio-analysis
domain: finance
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [finance.income_statement, finance.balance_sheet, finance.cash_flow, finance.debt, finance.working_capital, company, offerings]
writes: [finance.position, finance.working_capital, decisions]
related_skills: [financial-statement-analysis, cash-flow-diagnostic, working-capital-optimizer, debt-service-and-covenant-analysis]
owned_by_agents: [cfo-agent, business-analyst-agent]
---

# Skill: Financial Ratio Analysis

## Purpose
Compute the full small-business ratio set — profitability, efficiency/turnover, working-capital cycle, liquidity, and leverage/coverage — plus a DuPont ROE decomposition, then flag each ratio against benchmarks, industry norms, and loan covenants with a healthy / warning / critical status. Gives the founder a one-glance diagnosis of financial health and its causes.

## When to Use
- "How healthy is my business, by the numbers?"
- "Break down my return on equity / why is ROE what it is?"
- "Am I in danger of breaching my loan covenant?"
- "How do my margins/turns/liquidity compare to my industry?"
- Monthly/quarterly review, pre-loan or pre-investor prep, or after `financial-statement-analysis` surfaces a margin or trend issue.

## When NOT to Use
- Statements are not yet built or don't tie out → run `financial-statement-analysis` first.
- The question is specifically about cash timing ("profitable but broke") → `cash-flow-diagnostic`.
- Deep dive on the cash conversion cycle and how to free trapped cash → `working-capital-optimizer`.
- Deep dive on debt capacity, DSCR, and covenant remediation planning → `debt-service-and-covenant-analysis`.
- Setting or renegotiating covenant terms with a lender → escalate to founder (and accountant/attorney for the agreement).

## Required Context
- Reconciled IS and BS for the period (and prior periods for time-series). Read from `finance.income_statement`, `finance.balance_sheet`.
- Business type (product vs. service) — service companies have N/A inventory turnover and quick ratio. Read from `company`.
- Interest expense, principal repayment schedule, and any covenant thresholds. Read from `finance.debt`.
- Optional industry benchmark values for cross-sectional comparison.

## Inputs
```yaml
input:
  business_type: enum[product, service]
  periods:                                    # 1+ periods; multiple enables time-series
    - period: string
      revenue: number
      cogs: number
      operating_expenses: number
      depreciation: number
      ebit: number
      interest_expense: number
      net_income: number
      credit_sales: number                    # for A/R turnover; falls back to revenue
      total_assets: number
      net_fixed_assets: number
      inventory: number
      accounts_receivable: number
      accounts_payable: number
      current_assets: number
      current_liabilities: number
      cash: number
      total_liabilities: number
      interest_bearing_debt: number
      equity: number
      principal_repayment: number             # annual, for Times Burden Covered
      tax_rate: number                        # for grossing up principal
  use_averages: boolean                       # avg vs. period-end balances (default period-end, be consistent)
  covenants:                                   # optional lender thresholds
    current_ratio_min: number                 # e.g. 1.5
    tie_min: number
    dscr_min: number
    debt_to_equity_max: number
  industry_benchmarks: map                     # optional {ratio_name: value}
```

## Missing Information Protocol
- If `credit_sales` is unavailable, substitute total revenue for A/R turnover and note the substitution.
- If prior periods are missing, run single-period cross-sectional analysis only and note that trend flags are unavailable.
- If covenant thresholds are unknown but debt exists, ask the founder once for the covenant terms (or note they are unverified) rather than assuming defaults.
- For service businesses, mark inventory turnover, inventory days, and quick ratio as N/A rather than computing meaningless values.
- If equity is zero or negative, report ROE and leverage as distorted/meaningless and explain why; do not present a spurious percentage.

## Diagnostic Questions
1. Is the business profitable, and at which level does profitability break down (gross, operating, net)?
2. Are assets used efficiently (turnover), and is cash trapped in the working-capital cycle?
3. Can the business meet near-term obligations (liquidity) and mandatory debt payments (coverage)?
4. Is ROE driven by real operating performance (margin, turnover) or merely by leverage?
5. Is any ratio near or through a covenant threshold?
6. How does each ratio compare to prior periods (trend) and to industry (benchmark)?

## Analysis Framework
Organizes ratios as a pyramid under ROE (DuPont), plus a parallel liquidity view, and compares both time-series and cross-sectional.

```
Return on Equity (ROE)
└─ Return on Assets (ROA)
   ├─ Net Profit Margin ── Gross Margin · Operating Margin · EBITDA Margin
   ├─ Asset Turnover ───── Fixed-Asset Turnover · Inventory Days · A/R Days · A/P Days
   └─ Financial Leverage ─ Debt-to-Assets · Debt-to-Equity · TIE · Times Burden Covered
Liquidity (parallel) ── Current Ratio · Quick Ratio · Cash Ratio · Cash Operating Cycle
```

DuPont: attribute any ROE movement to margin (operations), turnover (asset utilization), or leverage (financing). Always trace a ratio movement back to the operating decision or market condition behind it. Use both time-series (trend) and cross-sectional (benchmark/covenant) comparison.

## Calculations
Convention: percentages ×100 where noted. Use period-end or average balances consistently.

**Profitability**
- Gross Margin = (Revenue − COGS) / Revenue.
- Operating (EBIT) Margin = EBIT / Revenue.
- EBITDA Margin = (EBIT + D&A) / Revenue.
- Net Profit Margin = Net Income / Revenue.
- ROA = Net Income / Total Assets (= Net Margin × Asset Turnover).
- ROE = Net Income / Equity (= ROA × Financial Leverage).

**Efficiency / turnover**
- Total Asset Turnover = Revenue / Total Assets.
- Fixed-Asset Turnover = Revenue / Net Fixed Assets.
- Inventory Turnover = COGS / Inventory (product only).
- A/R Turnover = Credit Sales / A/R.
- A/P Turnover = COGS / A/P.

**Working-capital cycle (days)**
- A/R Days (DSO) = 365 / A/R Turnover.
- Inventory Days (DIO) = 365 / Inventory Turnover.
- A/P Days (DPO) = 365 / A/P Turnover.
- Cash (Net) Operating Cycle = DIO + DSO − DPO.

**Liquidity**
- Current Ratio = Current Assets / Current Liabilities.
- Quick / Acid-Test = (Current Assets − Inventory) / Current Liabilities (N/A pure service).
- Cash Ratio = Cash / Current Liabilities.

**Leverage / coverage**
- Financial Leverage (DuPont) = Total Assets / Equity.
- Debt-to-Equity = Total Liabilities / Equity (or interest-bearing debt / equity — state which).
- Debt-to-Assets = Total Liabilities / Total Assets.
- Interest-Bearing Debt-to-Assets = Interest-Bearing Liabilities / Total Assets.
- Times Interest Earned (TIE) = EBIT / Interest Expense.
- Times Burden Covered = EBIT / [Interest + Principal / (1 − tax rate)].

**DuPont identity:** ROE = (Net Income / Sales) × (Sales / Total Assets) × (Total Assets / Equity).

**Benchmark thresholds (healthy / warning / critical):**
| Ratio | Healthy | Warning | Critical |
|---|---|---|---|
| Gross Margin | ≥ industry avg, stable/rising | declining trend | below level needed to cover opex |
| Operating Margin | positive & stable | compressing | negative |
| Net Profit Margin | positive | thin/declining | negative |
| Current Ratio | ≥1.5 (covenant-safe) | 1.0–1.5 | <1.0 (floor breached) |
| Quick Ratio | ≥1.0 | 0.5–1.0 | <0.5 |
| Times Interest Earned | comfortably high | ~1.5–3 | <1.5 (financial stress) |
| Cash Operating Cycle | short/stable | lengthening | long & rising (cash trap) |
| A/R Days | ≤ terms granted | slightly > terms | well beyond terms |
| Inventory Days | in line with industry | rising vs. sales | obsolescence risk |
| Interest-bearing D/E | moderate | rising | equity near zero/negative |
| ROA | positive & rising | declining | negative |
| ROE (via DuPont) | positive from margin/turnover | mainly leverage-driven | negative/meaningless (neg. equity) |

Note: a very high current/quick ratio (≥3–4) is also a warning — idle cash, slow collections, obsolete inventory, or unused free trade credit. Excessively high TIE may signal under-leverage.

## Decision Rules
- IF Current Ratio < 1.0 → THEN no liquidity cushion; flag near-term solvency risk (critical).
- IF a covenant sets Current Ratio ≥ threshold AND actual < threshold → THEN loan is technically in default (possible acceleration, forced liquidation, higher rate, added collateral); flag critical and hand to `debt-service-and-covenant-analysis`.
- IF Current/Quick Ratio ≥ 3–4 → THEN investigate over-investment in non-earning assets (excess cash, uncollected A/R, slow inventory, unused trade credit).
- IF TIE < ~1.5 → THEN financial stress; reduce debt or raise EBIT before adding leverage.
- IF TIE / Times Burden Covered persistently very high → THEN possibly under-leveraged; note the option to create value with low-risk debt (do not recommend borrowing — that requires approval).
- IF Gross Margin declines over time → THEN diagnose price cuts, input-cost inflation, or mix shift; protect gross profit first.
- IF Operating Margin falls faster than Gross Margin → THEN the problem is in opex; identify which line rose as % of revenue via common-size.
- IF A/R Days > credit terms granted → THEN collection problem; hand to `working-capital-optimizer`.
- IF Inventory Days rising with flat/falling sales → THEN overstocking/obsolescence; hand to `working-capital-optimizer`.
- IF Cash Operating Cycle long/growing → THEN working-capital financing pressure; hand to `working-capital-optimizer`.
- IF ROE is high → THEN decompose via DuPont before celebrating; confirm whether from margin, turnover, or leverage.
- IF equity ≤ 0 → THEN ROE/leverage are meaningless; report as distorted, focus on solvency.

## Procedure
1. Confirm business_type and load period data (statements must be reconciled).
2. Compute the full ratio set for each period; mark N/A items for service businesses.
3. Compute DuPont: Net Margin × Asset Turnover × Financial Leverage = ROE; also ROA.
4. Assign each ratio a healthy/warning/critical status vs. the benchmark table, industry benchmarks (if provided), and covenants.
5. Run time-series comparison across periods; flag material trends with direction.
6. Attribute ROE movement to its DuPont lever and trace to the operating cause.
7. Emit the ratio panel, DuPont attribution, flagged findings, and prioritized handoffs.
8. Write summary metrics to `finance.position` and `finance.working_capital` (L1 staged); record findings in `decisions`.

## Output
```yaml
output:
  period: string
  business_type: enum[product, service]
  profitability: {gross_margin, operating_margin, ebitda_margin, net_margin, roa, roe}
  efficiency: {total_asset_turnover, fixed_asset_turnover, inventory_turnover, ar_turnover, ap_turnover}
  working_capital_cycle: {dso_days, dio_days, dpo_days, cash_operating_cycle_days}
  liquidity: {current_ratio, quick_ratio, cash_ratio}
  leverage_coverage: {financial_leverage, debt_to_equity, debt_to_assets, interest_bearing_debt_to_assets, tie, times_burden_covered}
  dupont: {net_margin, asset_turnover, financial_leverage, roe, roe_driver}   # roe_driver = margin|turnover|leverage
  status_flags:                                                               # per ratio
    - {ratio: string, value: number, status: enum[healthy, warning, critical], vs_prior: string, vs_benchmark: string, vs_covenant: string}
  covenant_breaches: list
  narrative: string
  handoffs: list
```

## Recommendations
Prioritized by severity (critical before warning), then by leverage over the outcome (the ratio whose improvement most moves ROE or removes a covenant breach), then by reversibility/effort. Each recommendation names the driving ratio and its DuPont lever, states the operating cause, and points to the skill that acts on it. Covenant breaches always rank first.

## Execution Opportunities
- Update `finance.position` and `finance.working_capital` with computed metrics (reversible, LOW; L1 staged).
- Refresh a ratio dashboard / scorecard (reversible, LOW).
- Create internal tasks for each warning/critical flag (reversible, LOW).
- Draft a founder-facing health summary (reversible, LOW; external sharing needs approval).
- Set internal monitoring alerts on ratios approaching covenant thresholds (reversible, LOW).

## Human Approval Requirements
- Ratio computation, flagging, and interpretation: always allowed.
- Any action that follows from a flag and moves money, takes on/refinances debt, commits budget, or applies for financing: ALWAYS requires founder approval (handled by the acting skill, never here).
- Negotiating or agreeing new covenant terms: founder approval; involve accountant/attorney.

## Escalation Conditions
- Covenant breach or imminent breach → founder immediately + recommend accountant.
- Negative/near-zero equity, sustained negative margins, or TIE < 1 → founder + accountant (solvency risk).
- Ratio interpretation depends on an accounting treatment in question → accountant/CPA.
- Industry benchmark unavailable and the level is ambiguous → surface uncertainty; do not over-claim "good/bad."

## KPIs
- Coverage: full ratio set computed with correct N/A handling by business type.
- Detection: covenant breaches and critical flags surfaced before the lender/founder finds them independently.
- DuPont attribution correctly explains ROE change (validated against recomputation).
- Founder actions taken on flagged ratios; subsequent improvement in the flagged metric.

## Monitoring
- Track each flagged ratio period-over-period; confirm warnings don't slide to critical.
- Watch covenant headroom every period; alert when within a set buffer of a threshold.
- Re-check DuPont driver each period to catch a shift from operating-driven to leverage-driven ROE.

## Follow-Up
- Run every close and before any financing, investor, or valuation event.
- Re-run immediately after any restatement or when new covenant terms take effect.

## Related Skills
- `financial-statement-analysis` (produces the inputs).
- `cash-flow-diagnostic`, `working-capital-optimizer`, `debt-service-and-covenant-analysis` (act on specific flags).
- `financial-forecast-builder` (uses ratios to validate forecast assumptions).

## Guardrails
- Never present ROE/leverage when equity ≤ 0 without labeling them distorted.
- Never assume covenant terms; verify with the founder/agreement.
- Mark service-business N/A ratios rather than computing meaningless numbers.
- A high ROE is not automatically good — always decompose before recommending.
- Do not recommend taking on debt as a fix, even when under-levered; surface it as an option for founder decision.
- Confidential financial data; audited writes only to permitted namespaces.

## Example
**Founder input:** "Run my ratios for FY2025 vs FY2024. I have a bank covenant requiring current ratio ≥ 1.5." Product business. FY2025: Revenue $2.72M, Net Income $54,400, Total Assets $1.0M, Equity $448k, EBIT $70,700, Interest $16,600, Current Assets $370k, Current Liabilities $250k, Inventory $114k, A/R $394k, A/P $103k, COGS $1.70M.

**Skill reasoning:** Net Margin 2.0%, Asset Turnover 2.72×, Financial Leverage 2.23× → DuPont ROE ≈ 2.0% × 2.72 × 2.23 ≈ 12.1%; ROA 5.4%. TIE = 70,700 / 16,600 = 4.26× (healthy). Current Ratio = 370k / 250k = 1.48 → below the 1.5 covenant → CRITICAL breach flag. Quick Ratio = (370k − 114k)/250k = 1.02. DSO = 365/(2.72M/394k) = 52.9 days; DIO = 365/(1.70M/114k) = 24.5 days; DPO = 365/(1.70M/103k) = 22.1 days; cash cycle ≈ 55.3 days. ROE driver = balanced but leverage-assisted.

**Output:** full panel; top finding: "Current ratio 1.48 breaches the 1.5 covenant — technically in default. Remediate before the next reporting date." Handoffs: `debt-service-and-covenant-analysis` (covenant), `working-capital-optimizer` (55-day cash cycle).

**Executed vs. approval:** metrics written to `finance.position`, dashboard refreshed, tasks created (L1); any remediation that moves money or renegotiates the loan held for founder approval.

## Provenance
SOURCE. Derives from the Finance — Statements & Ratios knowledge (full ratio taxonomy, DuPont decomposition, healthy/warning/critical KPI table, covenant rules) and the Forecasting/Cash knowledge (ratio pyramid, coverage formulas). Branding stripped and generalized per PROVENANCE_MAP.
