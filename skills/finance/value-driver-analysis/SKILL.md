---
name: value-driver-analysis
domain: finance
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [finance, offerings, customers, market, metrics, company, strategy]
writes: [finance, decisions, metrics, goals]
related_skills: [business-valuation, financing-options-analysis, bankability-assessment, financial-statement-analysis, break-even-and-pricing-analysis]
owned_by_agents: [cfo-agent]
---

# Skill: Value-Driver Analysis

## Purpose
Identify the specific levers that raise (or are depressing) the business's value, quantify their effect on the valuation multiple and the earnings base, and hand the founder a prioritized action list. Turns "the business is worth $X" into "here is how we make it worth more, ranked by impact and effort."

## When to Use
- Founder asks "How do I increase the value of my business?" / "What's holding our valuation back?" / "What should I fix before we raise or sell?"
- Right after a `business-valuation` run exposes a margin gap or a below-range multiple.
- Building a multi-quarter plan to be exit-ready or raise-ready.
- Diagnosing why an offer or indicative valuation came in lower than expected.

## When NOT to Use
- The founder just wants the number, not the levers → use `business-valuation`.
- The lever in question is purely operational efficiency unrelated to value/margins → route to the Operations Agent.
- A binding transaction is imminent → still run this for the punch-list, but escalate the transaction itself to an appraiser/CPA/attorney.
- Pricing model redesign is the core need → hand to `break-even-and-pricing-analysis`, then return.

## Required Context
- `finance` — Revenue, Gross/Net margin trend, EBITDA, long-term debt/leverage, revenue by period.
- `customers` — customer concentration (top-customer % of revenue), recurring vs. one-time revenue mix, retention/churn.
- `offerings` / `market` — business model, sector, demand tailwinds, competitive position.
- `company` — owner-dependence, size band.
- A current or recent `business-valuation` (indicated value + multiple positioning) is strongly preferred as the baseline.

## Inputs
```yaml
input:
  goal_horizon: enum[now, 6_12_months, 12_36_months]   # when value uplift is needed
  baseline_valuation: number          # from business-valuation, optional but preferred
  baseline_multiple: number           # EBITDA multiple currently positioned at
  revenue: number
  revenue_growth_rate: number         # yoy %, decimal
  gross_margin: number                # decimal
  net_margin: number                  # decimal
  ebitda: number
  industry_net_margin_benchmark: number  # peer median, decimal (from market data)
  recurring_revenue_pct: number       # decimal, share of revenue that recurs
  customer_concentration: number      # top-customer % of revenue, decimal
  churn_rate: number                  # decimal, optional
  long_term_debt: number
  debt_to_ebitda: number              # leverage, optional (computed if debt+ebitda present)
  owner_dependence: enum[high, medium, low]
  signed_forward_contracts: number    # future revenue under contract not in trailing financials
  demand_tailwind: enum[strong, neutral, headwind]
```

## Missing Information Protocol
1. **Pull the baseline** from the most recent `business-valuation` and from `finance`/`customers`. Compute derived ratios (debt_to_ebitda, margin gap vs. benchmark).
2. **Fetch the peer margin benchmark** from `market transaction multiple data` / sector data if absent.
3. **Ask the founder ONE batched question** only for judgment fields that cannot be pulled: owner_dependence, demand_tailwind, and any signed forward contracts.
4. **Never assume** the benchmark margin, never invent a baseline multiple, and never claim a value uplift without stating the mechanism (higher base × or higher multiple).

## Diagnostic Questions
- Which drivers move value here — the earnings *base* (grow revenue/EBITDA) or the *multiple* (de-risk the business), or both?
- Is net margin above, at, or below the peer benchmark? By how much?
- How concentrated is revenue in the top customer(s)? How recurring is it?
- How dependent is the business on the owner? Could it run without them?
- Is the balance sheet clean, or is leverage a drag on both value and bankability?
- Is there documented forward growth (contracts/pipeline) that justifies value above trailing multiples?
- Which levers are reachable inside the goal horizon?

## Analysis Framework
Value moves two ways — grow the **earnings base** and expand the **multiple** — so every lever is classified by which it affects, then scored:
1. **Base levers (raise Revenue/EBITDA):** grow revenue profitably; expand gross/net margin via vertical integration/cost control; invest in higher-margin channels (e.g., e-commerce); pricing discipline.
2. **Multiple levers (raise the ×, i.e., de-risk):** build recurring/defensible revenue; reduce customer concentration; reduce owner-dependence; deleverage the balance sheet; ride a structural demand tailwind; demonstrate reliable forecast-vs-actual.
3. **Forward-value levers:** convert pipeline to signed contracts that evidence future growth above trailing multiples.
4. **Score each lever** on Impact (expected effect on value), Effort, Cost, Risk, Reversibility, and Time-to-effect vs. the goal horizon.
5. **Identify value-destroyers** (inverse levers) currently active: over-reliance on debt, thin/volatile margins, customer concentration, owner-dependence, poor strategic discipline — these cap the multiple and must be addressed first if severe.
6. **Estimate the uplift** for the top levers using the valuation math (Calculations), so priorities are quantified, not vibes.
7. **Sequence** by impact-to-effort within the horizon, addressing severe value-destroyers first.

## Calculations
- **Margin gap** = industry_net_margin_benchmark − net_margin. (Positive = below peers = base+multiple opportunity.)
- **Base-lever uplift** ≈ Δ(EBITDA) × baseline_multiple. (Growing EBITDA by ΔE raises value by ΔE × current ×.)
  - e.g., a 2-pt gross-margin gain on revenue R adds ≈ 0.02 × R to EBITDA → × multiple = value uplift.
- **Multiple-lever uplift** ≈ EBITDA × Δ(multiple). (De-risking that moves the × from m₀ to m₁ raises value by EBITDA × (m₁ − m₀).)
- **Leverage** = debt_to_ebitda = long_term_debt ÷ EBITDA. (Lower = more bankable + higher multiple; > ~3× is a drag for small businesses.)
- **Concentration risk flag:** customer_concentration > ~0.30 caps the multiple (buyers discount concentrated revenue).
- **Recurring-revenue premium:** higher recurring_revenue_pct supports up-range positioning (mechanism: raises the multiple, not the base).
- **Forward-value:** signed_forward_contracts translated to incremental EBITDA justify value above trailing multiples (document evidence; DCF is the proper method for large forward value).
- **Impact score (ranking)** = normalized(expected_value_uplift) ÷ normalized(effort × cost × risk), gated by fits-within-horizon.

Multiple-positioning reference (where a business lands, from market transaction multiple data): industry/sector, size, growth rate, margin, customer concentration, recurring revenue, owner-dependence. Small-business EBITDA multiples commonly ~3×–7×; moving up-range is the multiple-lever prize.

## Decision Rules
- IF net_margin < industry benchmark THEN margin expansion is a **top base lever** (also lifts the multiple) → prioritize cost control / vertical integration / pricing.
- IF customer_concentration > ~0.30 THEN concentration is a **value-capping destroyer** → prioritize diversifying the customer base before a raise/sale.
- IF owner_dependence == high THEN reducing owner-dependence is a top **multiple lever** (buyers pay more for a business that runs without the founder).
- IF debt_to_ebitda > ~3× OR leverage flagged as a prior near-failure cause THEN **deleverage first** → improves both value and bankability.
- IF recurring_revenue_pct is low in a model that could recur THEN building recurring/defensible revenue is a high-impact multiple lever.
- IF demand_tailwind == strong AND position is early/leading THEN emphasize and invest into the tailwind → supports up-range multiple.
- IF signed_forward_contracts are material THEN document them as forward value to justify price above trailing multiples.
- IF revenue is growing but margin is flat/declining THEN growth is **not yet profitable** → fix margin before scaling further (unprofitable growth doesn't lift value proportionally).
- IF goal_horizon == now THEN drop long-lead levers (deleveraging, owner-transition) from the top of the list and surface quick base wins + documentation of forward value.

## Procedure
1. Load the baseline valuation and financial/customer facts; compute margin gap, leverage, concentration, recurring %.
2. Run the Missing Information Protocol for judgment fields.
3. Classify each candidate lever as base / multiple / forward-value.
4. Flag active value-destroyers and rank by severity.
5. Estimate value uplift per top lever using the Calculations.
6. Score levers on impact / effort / cost / risk / reversibility / time-to-effect vs. horizon.
7. Sequence into a prioritized action plan (address severe destroyers first, then highest impact-to-effort).
8. Quantify the plan's aggregate potential value uplift and the target multiple.
9. Write findings to `finance`/`decisions`; optionally create `goals` and internal tasks for approved actions.
10. Recommend re-running `business-valuation` after each cycle to measure realized change.

## Output
```yaml
output:
  baseline: {value: number, ebitda: number, multiple: number}
  margin_gap: number
  active_value_destroyers:
    - {name: string, severity: enum[high, medium, low], effect: string}
  levers:
    - name: string
      type: enum[base, multiple, forward_value]
      mechanism: string                 # how it raises value
      expected_value_uplift: number     # estimated $, with method
      effort: enum[low, medium, high]
      cost: enum[low, medium, high]
      risk: enum[low, medium, high]
      reversibility: enum[reversible, recoverable, irreversible]
      time_to_effect: enum[now, 6_12_months, 12_36_months]
      impact_score: number
      priority_rank: integer
  prioritized_actions: [string]         # ordered, horizon-fit
  target_multiple: number               # achievable × after plan
  aggregate_potential_uplift: number    # sum of prioritized levers' uplift
  confidence: enum[high, medium, low]
  recommended_next_skills: [string]
```

## Recommendations
Order by impact-to-effort within the goal horizon, with severe value-destroyers pulled to the front regardless of effort (they cap everything else). Each recommendation names the mechanism (base vs. multiple), the quantified uplift, cost, risk, and reversibility, and whether it needs founder approval or is internal analysis. Distinguish quick wins (now) from structural bets (12–36 months).

## Execution Opportunities
- **L0/L1 (allowed):** run the full analysis, quantify uplift, draft the prioritized plan, create `goals` and internal task drafts, update the value-tracking dashboard. All reversible, low-risk.
- Actions the levers imply (a pricing change, a capital raise to deleverage, a channel investment with spend, a hire to reduce owner-dependence) are **prepared** here but executed only by the owning skill/agent with the required approval.

## Human Approval Requirements
- Any lever that **commits money** (channel investment, hiring, capex to vertically integrate) → founder approval and routing to the owning agent (CFO for spend, People for hires).
- Any lever that involves **taking on debt or raising equity** to deleverage/grow → always founder approval (see `financing-options-analysis` / `bankability-assessment`).
- Pricing changes → founder approval (route via pricing skill / Sales + Strategy validation).
- Analysis, ranking, and plan drafting are always allowed without approval.

## Escalation Conditions
- Deleveraging or growth requiring new capital → founder (+ recommend accountant); route financing decision to the debt/equity skills.
- Structural/irreversible strategic bets (vertical integration, exiting a concentrated customer) → founder (+ executive/advisor).
- Exit/tax context → qualified appraiser/CPA/attorney.
- Low confidence in benchmark or baseline → surface to founder; do not overstate uplift.

## KPIs
- Realized change in the valuation multiple and indicated value after executing prioritized levers (measured by re-running `business-valuation`).
- Margin gap closed vs. peer benchmark over the horizon.
- Reduction in flagged value-destroyers (concentration, leverage, owner-dependence).
- Founder acts on the top-ranked levers.

## Monitoring
- Track margin trend, customer concentration, recurring %, and leverage each period.
- Watch for growth that outpaces margin (unprofitable growth), rising concentration, or creeping leverage — all erode value.

## Follow-Up
- Re-run after each valuation cycle, on material margin/concentration/leverage shifts, and before any raise or exit.
- Pair with `business-valuation` to quantify realized uplift after each lever executes.

## Related Skills
- `business-valuation` (baseline + measure uplift) · `financing-options-analysis` & `bankability-assessment` (if a lever needs capital) · `break-even-and-pricing-analysis` (margin/pricing levers) · `financial-statement-analysis` (inputs).

## Guardrails
- Never claim a value uplift without stating the mechanism (base × or Δ multiple) and the assumptions.
- Do not recommend unprofitable top-line growth as a value lever.
- Do not recommend debt/equity as a lever without routing through the financing skills and founder approval.
- Uplift estimates are indicative, not guarantees; label confidence.
- Escalate exit/tax framing to licensed professionals; no personalized investment advice.
- Treat concentration/leverage/margin figures as `confidential`.

## Example
**Founder input:** "Our indicative valuation came back around $7.7M at a 7.24× EBITDA. We want it materially higher before raising in ~18 months. What do we work on?" Facts: revenue $8.0M, EBITDA $1.0M, net margin 8.1% (peer benchmark ~10%), recurring_revenue_pct 0.20, customer_concentration 0.34, owner_dependence high, long_term_debt $2.5M (debt_to_ebitda 2.5×), demand_tailwind strong (sustainability), signed_forward_contracts $1.2M.

**Reasoning:**
- Margin gap = 10% − 8.1% = 1.9 pts → base lever. Closing it adds ≈ 0.019 × $8.0M = $0.152M EBITDA → × 7.24 ≈ **+$1.1M value**.
- Concentration 0.34 > 0.30 → value-destroyer capping the multiple (high severity). Diversifying could move the × toward ~8× → EBITDA $1.0M × (8.0 − 7.24) ≈ **+$0.76M**.
- Owner_dependence high → multiple lever; building a management layer supports up-range positioning (~+0.5× → +$0.5M) but is a 12–36 month effort.
- debt_to_ebitda 2.5× is moderate (< 3×) → deleveraging helpful for bankability but lower priority than concentration/margin.
- Recurring 20% low for the model → building subscription/replenishment revenue is a strong multiple lever.
- Forward contracts $1.2M → document as forward value to justify price above trailing multiple.

**Prioritized actions (18-mo horizon):** (1) diversify top customer below 25% [high impact, high effort, ~+$0.76M]; (2) close the margin gap via cost control/pricing [high impact, medium effort, ~+$1.1M]; (3) grow recurring revenue mix [high impact, medium effort]; (4) begin reducing owner-dependence [structural, +$0.5M]; (5) document forward contracts for the raise. target_multiple ≈ 8×; aggregate_potential_uplift ≈ +$2.3M+ (indicative).

**Executed vs. approval:** the agent ran the analysis, quantified uplift, drafted the plan, and created internal `goals`/tasks (L1, auto). Pricing changes, the channel investment, and the management hire were prepared and routed for founder approval; deleveraging was flagged to `financing-options-analysis`.

## Provenance
SOURCE — derived from the Value Drivers list and Market Multiple positioning drivers in the Valuation, Money & Financing domain (grow revenue profitably, margin/vertical integration, recurring/defensible model, low leverage, reduced owner-dependence, demand tailwinds, forward contracts; value-destroyer inverses). Uplift math and impact scoring are CLAUDE-DERIVED structuring, labeled as such.
