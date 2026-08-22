---
name: business-valuation
domain: finance
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [finance, offerings, market, metrics, company]
writes: [finance, decisions, metrics]
related_skills: [value-driver-analysis, financing-options-analysis, bankability-assessment, financial-statement-analysis, scenario-and-sensitivity-analysis]
owned_by_agents: [cfo-agent]
---

# Skill: Business Valuation

## Purpose
Produce a defensible estimate of what the business is worth by applying market transaction multiples to the company's own value drivers (revenue, EBITDA, SDE, net income), triangulating across methods, and reporting a value range with the margin story behind it. Gives the founder a credible number for a raise, an exit conversation, an internal decision, or a reality check — before spending on a formal appraisal.

## When to Use
- Founder asks "What is my business worth?" / "What would this sell for?" / "What valuation should I raise at?"
- Preparing for a capital raise, exit/M&A discussion, partner buy-in/buy-out, or estate/tax planning where an indicative number is needed first.
- A rough number is needed to size dilution in an equity round or to benchmark an unsolicited offer.
- Periodic (e.g., annual) tracking of enterprise value alongside financial statements.

## When NOT to Use
- A binding transaction (actual sale, official tax filing, litigation, divorce, buy-sell trigger) is imminent → escalate to a qualified business appraiser / CPA / attorney for a professional valuation report. This skill produces an *indicative estimate only*.
- The business is pre-revenue or a startup whose value rests on future potential not in trailing financials → use forward-looking methods (DCF / venture method); this skill's trailing multiples will understate value.
- The question is really "how do I raise my value?" → hand off to `value-driver-analysis`.
- Only normalized earnings are needed (recasting owner add-backs) → run the earnings-normalization step first, then return here.

## Required Context
- `finance` — trailing 12-month (or last full fiscal year) Revenue, COGS, Operating Expenses, Depreciation & Amortization, Interest, Taxes, Net Income; owner compensation and one-time/non-operating items for SDE normalization; long-term debt and cash (for equity-value bridge).
- `offerings` / `market` — industry/sector, business model (recurring vs. project), growth rate, customer concentration.
- `company` — size (revenue band), owner-dependence, purpose of the valuation.
- `market transaction multiple data` — comparable private-target sale multiples by sector; if unavailable, use the generic small-business ranges in Calculations.

## Inputs
```yaml
input:
  purpose: enum[raise, exit_sale, internal_decision, tax_estate, benchmark_offer, tracking]  # drives disclaimers & escalation
  period_label: string            # e.g. "FY2025 (TTM through 2026-06)"
  revenue: number                 # annual revenue, subject business
  cogs: number                    # cost of goods sold
  operating_expenses: number      # SG&A + development, excludes D&A
  depreciation_amortization: number
  interest_expense: number
  tax_expense: number
  net_income: number              # bottom line; if absent, computed
  owner_compensation: number      # owner salary + benefits above market-manager rate (for SDE)
  one_time_addbacks: number       # non-recurring / non-business expenses (for SDE)
  long_term_debt: number          # for equity-value bridge (optional)
  cash: number                    # for equity-value bridge (optional)
  industry: string
  business_model: enum[recurring, transactional, project, mixed]
  revenue_growth_rate: number     # yoy %, decimal
  net_margin: number              # optional; computed if absent
  customer_concentration: number  # % revenue from top customer (0-1), optional
  owner_dependence: enum[high, medium, low]
  comparables:                    # optional; if omitted use generic sector ranges
    - selling_price: number
      revenue: number
      ebitda: number
      net_income: number
      sde: number                 # optional
      recency_months: number      # months since transaction closed
      industry_match: boolean
```

## Missing Information Protocol
1. **Derive first.** Compute EBIT, EBITDA, SDE, net_margin from the P&L fields before asking anything (see Calculations).
2. **Fetch comparables** from `market transaction multiple data` for the industry + size band. If none, fall back to the generic small-business ranges and label the estimate `low-confidence, generic-range`.
3. **Ask the founder ONE batched question** only for fields that cannot be derived or fetched — typically: owner add-backs (owner_compensation, one_time_addbacks), long-term debt/cash for the equity bridge, and the valuation purpose.
4. **Never assume:** never invent comparable multiples, never guess revenue/EBITDA, never treat owner add-backs as zero silently, and never present an estimate without stating the method, comps used, and confidence.

## Diagnostic Questions
- What is the valuation *for*? (Purpose sets the disclaimer and whether to escalate.)
- Which earnings base best represents this business — EBITDA (default), SDE (owner-operated micro), or net income (stable/profitable)?
- Are the comparables truly comparable (industry, size, model) and recent (< ~6 months in a fast-moving market)?
- Do the revenue-multiple and EBITDA-multiple estimates diverge? What margin story explains the gap?
- Is there forward growth (signed contracts, pipeline) not reflected in trailing financials?
- Enterprise value vs. equity value — does the founder need the price for the business or the cash to the owner after debt?

## Analysis Framework
Relative (comparable / multiples) valuation, triangulated:
1. **Normalize earnings.** From the P&L, compute EBIT, EBITDA, and SDE. SDE adds owner comp and one-time items back to earnings — the right base for owner-operated micro-businesses.
2. **Select value drivers.** Objectively measurable: Revenue, EBITDA, Net Income, SDE. Intangibles (loyal customers, brand, team) are not valued directly — they show up through the revenue/profit/cash flow they generate and through *where in the range* the multiple lands.
3. **Build multiples.** For each comparable, multiple = Selling Price ÷ driver. Average each multiple across comps (using only recent, industry-matched comps). If no comps, use generic ranges anchored by the business's drivers.
4. **Position within the range.** Move up-range for: higher growth, higher-than-peer margin, recurring revenue, low customer concentration, low owner-dependence, clean/low-leverage balance sheet, larger size. Move down-range for the inverse.
5. **Apply & triangulate.** Value = driver × chosen multiple, for each method (A–C, plus SDE for micro). Report each estimate, the range, and the simple average as the indicated value.
6. **Read the margin story.** Compare the revenue-multiple estimate vs. the EBITDA/earnings-multiple estimate; divergence is a signal, not noise (see Decision Rules).
7. **Add forward value if evidenced.** If signed contracts/backlog materially raise future earnings, note an explicit uplift above the trailing-multiple estimate and flag DCF as the proper complement.
8. **Bridge to equity value if needed.** Equity value = enterprise value − long-term debt + cash.

## Calculations
Earnings base:
- **Gross Profit** = Revenue − COGS
- **EBIT (Operating Profit)** = Gross Profit − Operating Expenses
- **EBITDA** = EBIT + Depreciation + Amortization   *(cash-flow proxy; primary base)*
- **Net Income** = EBIT − Interest − Taxes  *(if not supplied)*
- **SDE** = Net Income + owner_compensation + interest + taxes + depreciation + amortization + one_time_addbacks
- **Net Profit Margin %** = Net Income ÷ Revenue
- **Gross Margin %** = Gross Profit ÷ Revenue

Multiples (per comparable, then averaged over recent industry-matched comps):
- **Revenue multiple** = Selling Price ÷ Revenue
- **EBITDA multiple** = Selling Price ÷ EBITDA
- **Net Income multiple** = Selling Price ÷ Net Income
- **SDE multiple** = Selling Price ÷ SDE

Value estimates:
- **Value (revenue method)** = Revenue × avg revenue multiple
- **Value (EBITDA method)** = EBITDA × avg EBITDA multiple   *(primary)*
- **Value (net income method)** = Net Income × avg net income multiple
- **Value (SDE method)** = SDE × avg SDE multiple
- **Indicated Value** = average of the applicable per-method estimates; also report min–max range.
- **Equity Value** = Indicated (enterprise) Value − Long-Term Debt + Cash

Generic small-business ranges (reasoning defaults ONLY when no comps; vary by industry/size/growth/margin):
| Base | Typical small-business range | Position drivers |
|---|---|---|
| Revenue multiple | ~0.5×–1.5× (higher-margin recurring/software materially higher; low-margin services lower) | growth, margin, model |
| EBITDA multiple | ~3×–7× (larger/faster/higher-margin at top and beyond) | size, growth, margin, concentration |
| SDE multiple (owner-operated micro) | ~1.5×–3.5× | owner-dependence, transferability |
| Net Income (P/E-style) multiple | ~9×–15× | stability, profitability |

## Decision Rules
- IF valuing any small business THEN use the **EBITDA multiple as primary**; cross-check with revenue and net-income multiples.
- IF the business is owner-operated / micro (revenue roughly < $1–2M, high owner involvement) THEN add the **SDE method** and weight it.
- IF revenue-multiple estimate >> EBITDA-multiple estimate THEN margins are **below** comparables → flag a margin-improvement opportunity (hand to `value-driver-analysis`) before any sale.
- IF EBITDA-multiple estimate >> revenue-multiple estimate THEN margins are **above** comparables → emphasize profitability as a value premium and position up-range.
- IF profits are negative/distorted THEN lean on the **revenue multiple** (and recommend DCF); do not lead with earnings multiples.
- IF material future growth exists that is NOT in trailing financials (e.g., signed contract) THEN add an explicit forward-value uplift with documented evidence and flag DCF as the proper method.
- IF comparables are > ~6 months old in a fast-moving market OR few are industry/size matched THEN downgrade confidence and widen the reported range.
- IF no usable comparables exist THEN use generic ranges and label the output `generic-range, low-confidence`.
- IF purpose ∈ {exit_sale, tax_estate} AND a transaction is imminent THEN present the estimate as indicative and **escalate to a qualified appraiser/CPA/attorney** for a formal report (typical cost ~$4k–$8k for a small business).
- IF top-customer concentration > ~30% OR owner_dependence == high THEN position toward the **bottom** of the multiple range and note it as a value risk.

## Procedure
1. Confirm the valuation purpose and the earnings base(s) to use.
2. Pull P&L and balance-sheet fields from `finance`; run the Missing Information Protocol for gaps.
3. Compute Gross Profit, EBIT, EBITDA, Net Income, SDE, and margins.
4. Fetch comparables from `market transaction multiple data` (industry + size); filter to recent, matched comps. If none, load generic ranges.
5. Compute per-comp multiples; average each; discard stale/unmatched comps.
6. Position within the range using growth, margin, recurring revenue, concentration, owner-dependence, size, leverage.
7. Compute value under each applicable method; compute the range and indicated (average) value.
8. Run the margin-story check (revenue vs. EBITDA estimate divergence).
9. Add documented forward-value uplift if applicable; bridge to equity value if requested.
10. Assemble output with methods, comps, range, confidence, disclaimers, and escalation flag.
11. Write an indicative valuation record to `finance`/`metrics` and a decision record; **do not** represent it as a formal appraisal.

## Output
```yaml
output:
  purpose: string
  as_of: date
  earnings_base:
    revenue: number
    ebit: number
    ebitda: number
    net_income: number
    sde: number
    gross_margin: number
    net_margin: number
  multiples_used:
    source: enum[market_transaction_multiple_data, generic_range]
    revenue_multiple: number
    ebitda_multiple: number
    net_income_multiple: number
    sde_multiple: number
    comps_count: number
    comps_recency_note: string
  estimates:
    revenue_method: number
    ebitda_method: number       # primary
    net_income_method: number
    sde_method: number
  indicated_value: number       # average of applicable methods (enterprise value)
  value_range: {low: number, high: number}
  equity_value: number          # enterprise value - LT debt + cash (if bridged)
  forward_value_uplift: {amount: number, evidence: string}   # if applicable
  margin_story: string          # what the revenue-vs-EBITDA divergence implies
  positioning_rationale: string # why the multiple sits where it does in the range
  confidence: enum[high, medium, low]
  disclaimer: string            # "indicative estimate, not a formal appraisal"
  escalate_to_appraiser: boolean
  recommended_next_skills: [string]
```

## Recommendations
Rank follow-ups by impact on realized value and effort: (1) if a margin gap is exposed, prioritize `value-driver-analysis`; (2) if concentration/owner-dependence caps the multiple, flag the specific levers; (3) if a transaction is real, prioritize commissioning a professional valuation. Every recommendation states the expected effect on the multiple or the value base, and its reversibility.

## Execution Opportunities
- **L0/L1 (allowed):** compute all methods, build the range, write the indicative valuation and decision records, draft a one-page valuation memo, create a follow-up task for value-driver work. All reversible, low-risk.
- Never auto-executes anything that commits money, price, or the company externally.

## Human Approval Requirements
- Any use of the valuation to **set a raise price, accept/counter an offer, agree an exit price, or file for tax/estate purposes** requires founder approval and, for exit/tax, a qualified appraiser/CPA/attorney sign-off.
- Sharing the number **externally** (investors, buyers, lenders) requires founder approval.
- Producing analysis internally is always allowed without approval (analysis is never gated).

## Escalation Conditions
- Imminent sale, M&A, buy-sell trigger, or litigation → qualified business appraiser + attorney.
- Tax, estate, or entity-value questions → CPA / tax professional.
- Financial decision above the founder's threshold that rests on this number → founder (+ recommend accountant).
- Comparable data conflicts or confidence is low → surface uncertainty to the founder; do not let a downstream action proceed on a shaky number.

## KPIs
- Estimate lands within a reasonable band of any subsequent professional appraisal or actual transaction price.
- Range width and confidence are honestly calibrated (narrow only when comps are strong).
- Margin-story flags reliably precede realized value-driver improvements.
- Founder reports the number was decision-useful.

## Monitoring
- Re-check when new comparable transactions appear in the sector, or when the subject's revenue/EBITDA/margin shifts materially.
- Watch for comp staleness; a valuation older than ~12 months (or after a material financial change) is stale.

## Follow-Up
- Re-run annually as part of financial-statement review, before any raise/exit conversation, and whenever a material contract, margin shift, or offer arrives.
- After a `value-driver-analysis` cycle, re-run to quantify the value change.

## Related Skills
- `value-driver-analysis` (raise the number) · `financing-options-analysis` (if valuation feeds a raise) · `bankability-assessment` (debt route) · `financial-statement-analysis` / earnings normalization (inputs) · `scenario-and-sensitivity-analysis` (range stress-testing).

## Guardrails
- **Indicative only.** Output is not a formal appraisal, fairness opinion, or tax valuation and must always carry that disclaimer.
- Do not use stale or non-comparable comps without downgrading confidence and widening the range.
- Do not silently zero out owner add-backs; SDE normalization must be explicit.
- Do not present a single point value as certainty — always report a range and confidence.
- Escalate exit/tax uses to licensed professionals; the agent does not give personalized investment or tax advice.
- Handle valuation figures as `confidential`; never expose externally without founder approval.

## Example
**Founder input:** "We're thinking about selling in a year or two — roughly what are we worth?" Company: sustainable consumer-goods manufacturer. FY revenue $8.0M; COGS $5.2M; OpEx $1.9M; D&A $0.10M; interest $0.05M; tax $0.20M; net income $0.65M. Owner-run but with a management team (owner_dependence medium). Growth ~15%/yr, net margin ~9% (industry-leading). Comparables from market transaction multiple data (recent, industry-matched) average: 0.93× revenue, 7.24× EBITDA, 12.99× net income.

**Reasoning:**
- Gross Profit = 8.0 − 5.2 = $2.8M. EBIT = 2.8 − 1.9 = $0.90M. EBITDA = 0.90 + 0.10 = $1.00M. Net income = $0.65M (given). Net margin = 0.65 ÷ 8.0 ≈ 8.1% → industry-leading → position up-range.
- Revenue method: 8.0 × 0.93 = **$7.44M**.
- EBITDA method (primary): 1.00 × 7.24 = **$7.24M**.
- Net income method: 0.65 × 12.99 = **$8.44M**.
- Indicated value = avg(7.44, 7.24, 8.44) ≈ **$7.7M**; range **$7.2M–$8.4M**.
- Margin story: revenue-method ($7.44M) and EBITDA-method ($7.24M) are close → margins roughly in line to slightly favorable; net-income method higher reflects strong bottom-line profitability → emphasize profitability as a premium; position toward upper-middle of range given growth + leading margin, tempered by medium owner-dependence.
- Purpose = exit within ~1–2 years → present as indicative, recommend a professional valuation before any real transaction.

**Output (abridged):** indicated_value $7.7M; range $7.2–8.4M; primary = EBITDA method $7.24M; confidence medium; margin_story "profitability supports upper-half positioning; no margin gap to fix"; escalate_to_appraiser true; recommended_next_skills [value-driver-analysis, exit-readiness].

**Executed vs. approval:** the agent computed the estimate, wrote the indicative valuation + decision records, and drafted a one-page memo (all L1, auto). Using the number to set an asking price or begin sale talks was held for founder approval and flagged for a qualified appraiser.

## Provenance
SOURCE — derived from the Valuation, Money & Financing domain knowledge (Relative/Comparable multiples framework, Methods A–D, market transaction multiple data ranges, margin-story decision rules). SDE base and equity-value bridge are CLAUDE-DERIVED standard practice, labeled as such. See internal provenance mapping.
