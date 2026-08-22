---
name: financing-options-analysis
domain: finance
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [finance, offerings, market, metrics, company, strategy, goals]
writes: [finance, decisions]
related_skills: [bankability-assessment, business-valuation, value-driver-analysis, financial-forecast-builder, debt-service-and-covenant-analysis]
owned_by_agents: [cfo-agent]
---

# Skill: Financing Options Analysis

## Purpose
Match a specific capital need to the most appropriate financing instrument(s) — term loan, line of credit, guaranteed small-business loan, equity, grants, or self-funding — by weighing cost, requirements, time horizon, and the founder's willingness to trade ownership vs. take on repayment. Outputs a ranked recommendation with the "how much, what for, how repaid" story, so the founder chooses funding on the merits rather than by default.

## When to Use
- Founder asks "How should I fund this?" / "Should I take a loan or raise money?" / "What's the best way to pay for [asset/expansion/hire/working-capital gap]?"
- A growth plan, capex, acquisition, or seasonal gap creates a funding need that internal cash won't cover.
- Before approaching any lender or investor, to pick the right instrument and frame the ask.
- Comparing two offers (e.g., a bank term loan vs. an equity check).

## When NOT to Use
- The question is "am I creditworthy / will a lender say yes?" → run `bankability-assessment` (this skill selects the instrument; that one tests fundability).
- A precise debt-service schedule or covenant check is needed → hand to `debt-service-and-covenant-analysis`.
- No forecast exists yet → build one first with `financial-forecast-builder`, then return.
- The need is really a valuation for an equity round → run `business-valuation` first.

## Required Context
- `finance` — current cash, operating cash flow, existing debt and payments, receivables (for a line of credit), forecast cash flows under the funded plan.
- `strategy` / `goals` — what the capital funds and the expected return/growth.
- `company` — owner's ownership/control preferences and risk tolerance.
- `market` — prevailing rate environment (affects cost assumptions; "the value of capital moves with the cost/availability of financing").
- A forecast (from `financial-forecast-builder`) covering the repayment horizon.

## Inputs
```yaml
input:
  amount_needed: number
  use_of_funds: enum[fixed_asset, expansion, working_capital, seasonal_gap, acquisition, hire, r_and_d, refinance]
  time_horizon: enum[short_term, long_term]        # short = <~1yr / seasonal; long = asset/growth
  ownership_preference: enum[keep_full, open_to_dilution]
  repayment_capacity_known: boolean                # is DSCR modeled?
  incremental_operating_profit: number             # new operating profit the plan generates (annual)
  existing_operating_profit: number
  current_cash: number
  internal_cash_available: number                  # retained earnings usable without harm
  receivables: number                              # for line-of-credit sizing
  owner_equity_available: number                   # cash the owner can contribute
  assets_for_collateral: number
  credit_history: enum[strong, fair, limited, poor]
  plan_uncertainty: enum[low, medium, high]        # reliability of the forecast cash flow
  community_impact: boolean                         # mission/community-aligned (grant eligibility)
  market_rate: number                              # assumed interest rate, decimal (default ~market)
  term_years: number                               # intended loan term if debt
```

## Missing Information Protocol
1. **Pull** cash, operating profit, receivables, existing debt, and the forecast from `finance`. Compute internal cash available and a first-pass DSCR if the incremental profit and loan terms are known.
2. **Fetch** a market rate assumption from `market` if not supplied; label it an assumption.
3. **Ask the founder ONE batched question** for the decision-critical judgment fields that can't be derived: ownership_preference, use_of_funds/time_horizon (if ambiguous), owner_equity_available, and plan_uncertainty.
4. **Never assume** ownership preference, never invent forecast cash flows, and never recommend an instrument without stating cost, key requirements, and the repayment (or exit-for-investor) story.

## Diagnostic Questions
- How much is needed, exactly what for, and over what horizon?
- Can current + forecast cash flow reliably service debt (DSCR)? Or is the risk better shared via equity?
- Does the founder want to keep full ownership, or trade equity for capital and expertise?
- Is the need short-term/seasonal (→ revolving) or a long-term asset/growth (→ term or equity)?
- How much equity can the owner contribute (skin in the game)?
- Is there collateral and credit history to support debt?
- Is the plan mission/community-aligned (grant eligibility)?
- What is the rate environment / cost of capital right now?

## Analysis Framework
Match funding source to (a) amount, (b) use, (c) time horizon, (d) ownership vs. repayment preference, then compare on cost + requirements + fit:
1. **Screen by horizon.** Short-term/seasonal need → revolving instruments (line of credit); long-term asset/growth → term loan or equity. Never fund a long-term asset with short-term credit or a short-term gap with permanent equity.
2. **Debt-vs-equity test.** Debt = keep ownership + tax-deductible interest, but fixed repayment and default risk — use when forecast cash flow can service it. Equity = no repayment obligation and shared risk, but permanent dilution and lost control — use when cash flows are uncertain or the amount/risk is too large for debt.
3. **Self-fund check.** If internal cash covers it without straining runway, self-funding preserves control at the opportunity cost of the cash.
4. **Enumerate the option catalog** (below), each with when-appropriate, cost, and requirements.
5. **Cost comparison.** Estimate the annual cost of each viable option (interest for debt; dilution/expected value share for equity; reporting burden for grants; opportunity cost for self-funding).
6. **Fit + feasibility.** Cross-check each viable option's requirements against the company's reality (forecast, DSCR, equity contribution, collateral, credit). Hand the fundability question to `bankability-assessment`.
7. **Rank** by fit-then-cost, and frame the ask (how much, what for, how repaid / investor exit).

Option catalog (option → when appropriate → cost → key requirements):
- **Term loan (bank / mission lender / community development lender)** → fund a specific asset or expansion with predictable repayment while keeping full ownership → cost = interest (assume ~market rate) → forecast, positive debt-service coverage (target DSCR comfortably > 1, ideal ~1.5–3×), owner equity contribution, collateral, creditworthiness.
- **Guaranteed small-business loan** → larger amounts or thin collateral, longer terms → cost = interest + fees → business plan, forecast, personal guarantee, credit history.
- **Line of credit** → short-term working capital / seasonal gaps (NOT long-term assets) → cost = interest on drawn balance → revenue history, receivables.
- **Equity investment** → high-growth or high-uncertainty plans where repayment cash flow isn't yet reliable, and the owner will trade ownership for capital + expertise → cost = dilution / share of future value + investor governance → credible valuation, growth story, investor exit path.
- **Founder / retained-earnings self-funding** → smaller needs; preserves control → cost = opportunity cost of cash → sufficient internal cash flow.
- **Grants / community funders** → mission-aligned or community-impact plans → cost = low/none but reporting burden → eligibility, community-impact narrative.

## Calculations
- **Internal cash available** = internal_cash_available (retained earnings usable without straining runway). If ≥ amount_needed and not needed as buffer → self-funding viable.
- **Annual loan payment (amortizing)** = P × [ r(1+r)^n ] ÷ [ (1+r)^n − 1 ], where P = amount financed, r = market_rate, n = term_years. (Reference: $100k at ~10% over 5 yrs ≈ $26k/yr.)
- **Pro-forma DSCR** = (existing_operating_profit + incremental_operating_profit) ÷ annual_debt_payment. Bankable if ≥ 1.25; strong at 1.5–3.0. (For a pure project view, use incremental_operating_profit ÷ payment.)
- **Owner equity contribution %** = owner_equity_available ÷ amount_needed. Lenders like ~10–25%.
- **Approx. debt cost (year 1)** ≈ amount_financed × market_rate (interest portion, before principal).
- **Approx. equity cost** ≈ (ownership_% sold) × expected_future_value_at_exit — i.e., permanent share of value given up; use the `business-valuation` figure to size dilution for a given check.
- **Line-of-credit sizing** ≈ a fraction of receivables + seasonal revenue swing (only the drawn balance accrues interest).

## Decision Rules
- IF time_horizon == short_term OR use_of_funds ∈ {working_capital, seasonal_gap} THEN recommend a **line of credit**, not a term loan or equity.
- IF time_horizon == long_term (fixed_asset/expansion) AND pro-forma DSCR ≥ 1.25 AND ownership_preference == keep_full THEN prefer a **term loan** (keep ownership).
- IF amount is large or collateral is thin AND debt is still the right shape THEN consider a **guaranteed small-business loan** (longer term, personal guarantee).
- IF plan_uncertainty == high OR forecast cash flow cannot reliably service debt (DSCR < 1.25 even after restructuring) THEN recommend **equity** (share the risk).
- IF internal_cash_available ≥ amount_needed AND leaves adequate runway buffer THEN recommend **self-funding** first (preserves control).
- IF community_impact == true AND the plan is mission-aligned THEN add **grants/community funders** to the mix (cheapest capital, reporting burden).
- IF DSCR is between ~1.0 and 1.25 THEN debt is marginal → restructure (smaller loan, longer term, add owner equity) or blend with equity; route to `bankability-assessment`.
- IF ownership_preference == keep_full BUT only equity is feasible THEN surface the trade-off explicitly to the founder rather than forcing either side.
- IF any recommended path involves taking on debt or raising equity THEN mark it **founder-approval-required** (never auto-execute a financing application or capital commitment).

## Procedure
1. Clarify amount, use of funds, and horizon; classify short vs. long term.
2. Pull cash, operating profit, receivables, existing debt, forecast; run the Missing Information Protocol.
3. Compute internal cash available, pro-forma DSCR, owner equity %, and per-option costs.
4. Screen options by horizon, then apply the debt-vs-equity and self-fund tests.
5. Build the option comparison (cost, requirements, fit) for each viable instrument.
6. Cross-check feasibility; hand fundability to `bankability-assessment` where debt is in play.
7. Rank options by fit-then-cost; frame the "how much / what for / how repaid (or investor exit)" narrative.
8. Write the analysis + decision record to `finance`/`decisions`; draft (not submit) any application/pitch materials.
9. Route any actual application or capital commitment to founder approval and the appropriate specialist.

## Output
```yaml
output:
  need: {amount: number, use_of_funds: string, time_horizon: string}
  internal_cash_available: number
  pro_forma_dscr: number
  owner_equity_pct: number
  options:
    - instrument: enum[term_loan, guaranteed_sb_loan, line_of_credit, equity, self_funding, grant]
      fit: enum[strong, possible, poor]
      when_appropriate: string
      estimated_annual_cost: number      # interest, dilution value, or opportunity cost
      cost_type: enum[interest, dilution, opportunity_cost, reporting_burden]
      key_requirements: [string]
      pros: [string]
      cons: [string]
      approval_required: boolean
  recommendation:
    primary: string
    rationale: string                    # ties to amount/use/horizon/ownership + cost
    blend: [string]                      # if a mix is best (e.g., loan + owner equity + grant)
    repayment_or_exit_story: string
  confidence: enum[high, medium, low]
  recommended_next_skills: [string]      # e.g., bankability-assessment, debt-service-and-covenant-analysis
```

## Recommendations
Rank by **fit first** (horizon + ownership + risk match), then by **cost** (annual interest vs. permanent dilution vs. opportunity cost), then by **feasibility** (does the company meet the requirements). Always present the trade-off honestly when the cheapest option isn't the best fit, and prefer a blend (e.g., term loan + owner equity + grant) when it lowers cost or improves bankability. Every recommendation carries the "how much / what for / how repaid" story and flags approval + escalation needs.

## Execution Opportunities
- **L0/L1 (allowed):** run the comparison, compute costs and pro-forma DSCR, draft the recommendation, and **draft** loan-application or investor-pitch documents and the repayment narrative. All reversible, low-risk.
- Preparing a financing pitch / application package is drafting only — it is never submitted without approval.

## Human Approval Requirements
- **Taking on debt, submitting any financing application, accepting an investment, or any capital commitment ALWAYS requires explicit founder approval** — this skill never auto-executes them (per the autonomy model's "moving money / commitments" rule).
- Signing loan documents, term sheets, personal guarantees, or investor agreements → founder approval + attorney review.
- Analysis, comparison, and draft materials are always allowed without approval.

## Escalation Conditions
- Any financing decision above the founder's cash-risk threshold → founder (+ recommend accountant).
- Loan terms, covenants, personal guarantees, security, or investor governance/legal terms → attorney (and CPA for tax treatment of debt/equity).
- Equity round sizing that depends on a valuation → route to `business-valuation`; if a real raise, escalate valuation to a qualified appraiser.
- Forecast is missing or low-confidence → do not recommend committing capital; build/validate the forecast first.

## KPIs
- Recommended instrument matches the need's horizon and the founder's ownership preference.
- Chosen financing is obtained on terms at/near the modeled cost; pro-forma DSCR holds after funding.
- No mismatch failures (e.g., long-term asset funded by short-term credit).
- Founder reports the framing made the lender/investor conversation easier.

## Monitoring
- After funding: track actual DSCR vs. modeled, drawn balance on lines of credit, covenant headroom, and rate changes.
- Watch the rate environment; a shift changes the debt-vs-equity calculus.

## Follow-Up
- Re-run when the amount, use, or rate environment changes, or when an offer arrives to compare.
- Hand to `debt-service-and-covenant-analysis` once a specific debt structure is on the table, and to `bankability-assessment` before approaching a lender.

## Related Skills
- `bankability-assessment` (will a lender say yes) · `debt-service-and-covenant-analysis` (schedule + covenants) · `business-valuation` (dilution sizing for equity) · `financial-forecast-builder` (repayment forecast) · `value-driver-analysis` (deleverage/grow to change the calculus).

## Guardrails
- Never submit an application or commit capital — draft only; all financing execution is founder-approved.
- Never recommend funding a long-term asset with short-term credit, or a short-term gap with permanent equity.
- State cost, requirements, and repayment/exit story for every option; label rate and forecast assumptions.
- Do not give personalized investment advice; escalate legal/tax terms to attorney/CPA.
- If the forecast is weak, say so and withhold a commit recommendation.
- Treat financing figures and terms as `confidential`.

## Example
**Founder input:** "I want to buy a $100k packaging line to bring production in-house. I'd rather not give up equity. Can we fund this with a loan?" Facts: incremental_operating_profit from the line ≈ $70k/yr; existing operating profit healthy; owner_equity_available $25k; assets_for_collateral present; credit_history strong; time_horizon long_term; use_of_funds fixed_asset; plan_uncertainty low; assume market_rate 10%, term 5 yrs; not community-specific.

**Reasoning:**
- Horizon = long-term fixed asset → term loan or equity (not a line of credit).
- Owner wants to keep full ownership → favor debt if it services.
- Finance $100k − $25k owner equity = $75k (owner contributes 25% — top of the healthy 10–25% band). Amortize $75k at 10% over 5 yrs ≈ $19k/yr; even the full $100k ≈ $26k/yr.
- Pro-forma project DSCR = $70k ÷ $26k ≈ **2.7** ("almost 3:1") → well above the 1.25 minimum, in the strong 1.5–3.0 band → clearly bankable as debt.
- plan_uncertainty low, collateral + strong credit present → term loan (or community development lender) is the strong-fit, lowest-cost option that preserves ownership.
- Equity would be unnecessary dilution here; self-funding alone ($25k) is insufficient.

**Recommendation:** primary = **term loan** ~$75k with a $25k owner equity contribution; estimated annual cost ≈ interest on $75k (~$7.5k yr-1, declining); repayment story = the new $70k operating profit covers the ~$19–26k payment ~2.7×. Blend already includes owner equity. approval_required = true. recommended_next_skills = [bankability-assessment, debt-service-and-covenant-analysis].

**Executed vs. approval:** the agent ran the comparison, computed DSCR and costs, and drafted the loan-application package + repayment narrative (L1, auto). Actually applying for, signing, or drawing the loan was held for founder approval and flagged for attorney review of terms.

## Provenance
SOURCE — derived from the Financing Options Logic and Debt-vs-Equity framework in the Valuation, Money & Financing domain (option catalog with when/cost/requirements, match-to-horizon rule, DSCR and owner-equity thresholds, worked $100k loan pitch). Amortization formula and cost-comparison structuring are CLAUDE-DERIVED, labeled as such.
