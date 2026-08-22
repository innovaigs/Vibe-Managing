---
name: bankability-assessment
domain: finance
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [finance, offerings, market, metrics, company, strategy, goals]
writes: [finance, decisions]
related_skills: [financing-options-analysis, debt-service-and-covenant-analysis, financial-forecast-builder, business-valuation, value-driver-analysis]
owned_by_agents: [cfo-agent]
---

# Skill: Bankability Assessment

## Purpose
Assess whether the business is creditworthy enough to secure the capital it wants — before approaching a lender — by testing it against standard lender criteria (the 5 C's of credit, debt service coverage, and owner equity contribution). Outputs a pass/marginal/fail verdict per criterion, the gaps, and a concrete action list to become fundable. "Being bankable" = able to describe the growth opportunity in financial terms and then show a credible source of capital and repayment plan.

## When to Use
- Founder asks "Will a bank fund this?" / "Am I creditworthy?" / "What do I need before I approach a lender?"
- Before submitting any loan application, to catch gaps that would trigger a rejection.
- After `financing-options-analysis` recommends debt, to test feasibility of the debt route.
- Diagnosing a loan denial or a lender's request for more equity/collateral.

## When NOT to Use
- The question is which instrument to use (debt vs. equity vs. grant) → run `financing-options-analysis` first; this skill tests the debt route once chosen.
- A detailed amortization schedule or covenant compliance check is needed → hand to `debt-service-and-covenant-analysis`.
- There is no forecast yet → build one with `financial-forecast-builder` (funders always want a forecast), then return.
- Equity is clearly the path (uncertain cash flows) → this skill's debt lens won't apply; use `financing-options-analysis` / `business-valuation`.

## Required Context
- `finance` — historical statements (ideally several clean years), current operating profit, existing debt and payments, cash, assets available as collateral, and a forecast covering the loan term.
- `company` / `founders` — owner credit history / track record, management reputation, owner equity available to contribute.
- `strategy` / `goals` — the growth opportunity and use of funds (described in financial terms).
- `market` — rate/economic conditions (part of "Conditions").

## Inputs
```yaml
input:
  loan_amount: number
  use_of_funds: string
  term_years: number
  market_rate: number                       # decimal, assumed/quoted interest rate
  existing_operating_profit: number         # annual, before the new plan
  incremental_operating_profit: number      # annual new operating profit the plan generates
  existing_debt_payments: number            # annual debt service already carried
  owner_equity_available: number            # cash owner will contribute
  assets_for_collateral: number             # liquidation/pledgeable value
  credit_history: enum[strong, fair, limited, poor]   # Character proxy
  management_track_record: enum[strong, fair, limited]  # Character
  years_of_clean_financials: number
  forecast_exists: boolean
  forecast_confidence: enum[high, medium, low]
  customer_concentration: number            # decimal, top customer share (Conditions/risk)
  industry_outlook: enum[favorable, neutral, headwind]  # Conditions
```

## Missing Information Protocol
1. **Pull** operating profit, existing debt payments, collateral value, cash, and the forecast from `finance`; pull credit/track-record signals from `founders`/`company`.
2. **Compute** the annual payment (amortization) and both DSCRs, and the owner equity % before asking anything.
3. **Ask the founder ONE batched question** only for what can't be pulled: credit_history, management_track_record, owner_equity_available, and forecast_confidence if unknown.
4. **Never assume** a forecast exists (if not, that is itself a fail on Capacity — funders always want a forecast), never invent operating profit or collateral, and never issue a verdict without stating the DSCR, the 5 C's scoring, and the specific gaps.

## Diagnostic Questions
- Is there a credible forecast, and does it show new operating profit covering the loan payment (repayment story)?
- What is the DSCR under the funded plan? Does it clear the lender minimum (≥ 1.25)?
- How much equity is the owner contributing (skin in the game)?
- What is the owner's credit history and management track record (Character)?
- Is there collateral to secure the loan?
- What are the Conditions — loan purpose, terms, and the economic/industry environment?
- Can the growth opportunity be described in financial terms/metrics (the essence of bankability)?

## Analysis Framework
Score the business against lender criteria, then convert gaps into actions:
1. **The 5 C's of Credit** (score each pass / marginal / fail):
   - **Character** — credit history, track record, management reputation.
   - **Capacity** — cash flow to service debt; the *quantified* test is DSCR, and a credible forecast must exist.
   - **Capital** — owner's own money invested (equity contribution).
   - **Collateral** — assets pledged to secure the loan.
   - **Conditions** — loan purpose, amount, terms, and the economic/industry environment.
2. **Quantify Capacity with DSCR** (two views): whole-business (all operating profit ÷ all debt service including the new loan) and project (incremental operating profit ÷ new payment). Both should clear thresholds; the binding one is the lower.
3. **Test Capital** via owner equity contribution % vs. the 10–25% norm.
4. **Bankability essence check:** can the opportunity be stated in financial terms with a forecast and a repayment plan? No forecast → not bankable yet.
5. **Overall verdict** = bankable / marginal / not-bankable, driven by the weakest C (a fail on Capacity or a missing forecast is disqualifying; a fail on Collateral may be curable via a guaranteed loan).
6. **Gap-to-action mapping:** for each failing/marginal C, prescribe the fix (reduce loan size, extend term, add owner equity, add collateral, improve the plan/margins, build the forecast) and route to the relevant skill.

## Calculations
- **Annual loan payment (amortizing)** = P × [ r(1+r)^n ] ÷ [ (1+r)^n − 1 ], P = loan_amount, r = market_rate, n = term_years. (Reference: $100k @ ~10% / 5 yrs ≈ $26k/yr.)
- **Total annual debt service** = existing_debt_payments + new annual loan payment.
- **DSCR (whole business)** = (existing_operating_profit + incremental_operating_profit) ÷ total annual debt service.
- **DSCR (project)** = incremental_operating_profit ÷ new annual loan payment.
- **Binding DSCR** = min(whole-business, project).
- **Owner equity contribution %** = owner_equity_available ÷ (loan_amount + owner_equity_available)  *(or ÷ total project cost)*.
- **Collateral coverage** = assets_for_collateral ÷ loan_amount.

Thresholds (agent defaults):
| Criterion | Metric | Minimum | Strong |
|---|---|---|---|
| Capacity | binding DSCR | ≥ 1.25 | 1.5 – 3.0 |
| Capital | owner equity % | ~10% | ~25% |
| Collateral | collateral coverage | ≥ 1.0× (curable via guarantee if short) | > 1.25× |
| Character | credit_history / track record | fair | strong |
| Conditions | purpose + environment | clear purpose, neutral outlook | clear purpose, favorable outlook |
| Bankability | forecast + repayment plan | must exist | forecast reliably beats plan |

## Decision Rules
- IF no forecast exists THEN **not bankable yet** → build the forecast first (funders always require one).
- IF binding DSCR ≥ 1.25 AND owner equity % ≥ ~10% AND collateral coverage ≥ 1.0× AND credit_history ≥ fair THEN **bankable** (verdict scales up as DSCR approaches 1.5–3.0 and equity approaches 25%).
- IF DSCR is between ~1.0 and 1.25 THEN **marginal** → reduce loan size, extend term, or add owner equity to lift DSCR above 1.25.
- IF DSCR < 1.0 THEN **not bankable as debt** → the plan can't service the loan → restructure materially or switch to equity (route to `financing-options-analysis`).
- IF owner equity % < ~10% THEN Capital fails → increase the owner contribution (skin in the game) before applying.
- IF collateral coverage < 1.0× BUT DSCR/Character are strong THEN consider a **guaranteed small-business loan** (curable collateral gap).
- IF credit_history == poor OR management_track_record == limited THEN Character is the binding gap → strengthen credit / add a co-guarantor / provide a stronger track-record narrative; some lenders will decline regardless.
- IF customer_concentration > ~0.30 OR industry_outlook == headwind THEN Conditions weaken → note the elevated risk and expect tighter terms / more equity/collateral required.
- IF verdict is bankable THEN the founder still must approve the actual application/borrowing — this skill never initiates it.

## Procedure
1. Confirm the loan amount, term, rate, and use of funds.
2. Pull operating profit, existing debt service, collateral, cash, forecast, and credit/track-record signals; run the Missing Information Protocol.
3. Compute the annual payment, both DSCRs (and the binding one), owner equity %, and collateral coverage.
4. Score each of the 5 C's pass/marginal/fail against thresholds.
5. Run the bankability-essence check (forecast + repayment story stated in financial terms).
6. Determine the overall verdict from the weakest binding C.
7. Map each gap to a specific fix and the skill/specialist that owns it.
8. Assemble the assessment + action list; write a decision record to `finance`/`decisions`.
9. Route any actual application or borrowing to founder approval; escalate legal/tax/credit specifics.

## Output
```yaml
output:
  loan: {amount: number, term_years: number, rate: number, use_of_funds: string}
  annual_payment: number
  dscr: {whole_business: number, project: number, binding: number}
  owner_equity_pct: number
  collateral_coverage: number
  five_cs:
    character: {score: enum[pass, marginal, fail], note: string}
    capacity:  {score: enum[pass, marginal, fail], note: string}   # DSCR-driven
    capital:   {score: enum[pass, marginal, fail], note: string}
    collateral:{score: enum[pass, marginal, fail], note: string}
    conditions:{score: enum[pass, marginal, fail], note: string}
  forecast_present: boolean
  verdict: enum[bankable, marginal, not_bankable]
  binding_gap: string                 # the weakest criterion driving the verdict
  gaps_and_actions:
    - {criterion: string, gap: string, action: string, owning_skill: string}
  recommended_terms_adjustment: string   # e.g., "reduce to $75k or extend to 7 yrs to reach DSCR 1.5"
  confidence: enum[high, medium, low]
  recommended_next_skills: [string]
```

## Recommendations
Lead with the binding gap (the weakest C) since it drives the verdict, then order remaining fixes by ease of closing (add owner equity and right-size the loan are usually fastest; building credit or collateral is slower). Prescribe concrete parameter changes (loan size, term, equity %) that would move the DSCR above 1.25 (and toward 1.5–3.0), and route each fix to its owning skill/specialist. State whether the business is ready to apply now, ready-after-fixes, or should switch to equity.

## Execution Opportunities
- **L0/L1 (allowed):** score the 5 C's, compute DSCR/equity/collateral, produce the verdict and action list, and **draft** the forecast-backed repayment narrative and application package. All reversible, low-risk.
- Drafting the lender package is preparation only — it is never submitted here.

## Human Approval Requirements
- **Submitting a loan application, accepting terms, signing a personal guarantee, or drawing/borrowing any funds ALWAYS requires founder approval** — this skill never initiates them (autonomy model: taking on debt / financing applications / capital commitments).
- Anything requiring a credit pull or sharing financials with a lender → founder approval.
- Scoring, diagnosis, and draft materials are always allowed without approval.

## Escalation Conditions
- Loan terms, covenants, personal guarantees, security agreements → attorney.
- Tax treatment of debt, or entity/credit-structure questions → CPA / tax professional.
- Credit-repair or personal-credit specifics → founder + qualified credit/financial advisor (no personalized financial advice from the agent).
- Financing decision above the founder's cash-risk threshold → founder (+ recommend accountant).
- No forecast or low-confidence forecast → do not issue a "bankable" verdict; require forecast work first.

## KPIs
- Predicted verdict matches the lender's actual decision (few "surprise" denials for businesses marked bankable).
- Gaps flagged are the ones lenders actually raise; closing them yields approval.
- Binding DSCR after any recommended restructuring clears ≥ 1.25 and holds post-funding.
- Founder approaches lenders only when ready, reducing wasted applications and hard credit pulls.

## Monitoring
- After funding: track actual DSCR vs. modeled, covenant headroom, and equity/collateral position.
- Watch for erosion in any C (rising leverage, falling margins, concentration, credit events) that would jeopardize a future raise.

## Follow-Up
- Re-run before each new borrowing, after material financial changes, and after executing gap-closing actions.
- Hand to `debt-service-and-covenant-analysis` once a specific structure is chosen, and back to `financing-options-analysis` if the verdict pushes toward equity.

## Related Skills
- `financing-options-analysis` (instrument selection; switch to equity if not bankable) · `debt-service-and-covenant-analysis` (schedule + covenants) · `financial-forecast-builder` (the required forecast) · `value-driver-analysis` (improve margins/deleverage to lift DSCR) · `business-valuation` (equity path sizing).

## Guardrails
- Never submit an application, trigger a credit pull, or borrow — draft/assess only; all debt execution is founder-approved.
- Never issue a "bankable" verdict without a credible forecast and a stated repayment story.
- DSCR/verdict are indicative of lender behavior, not a guarantee of approval — label confidence.
- Do not give personalized credit/financial advice; escalate legal/tax/credit specifics.
- Treat credit history, financials, and terms as `confidential` / partly `restricted`; never expose externally without approval.

## Example
**Founder input:** "I want a $100k loan for the new packaging line. Am I bankable before I go to the bank?" Facts: incremental_operating_profit $70k/yr; existing_operating_profit strong with modest existing_debt_payments $10k/yr; owner_equity_available $25k; assets_for_collateral ~$90k; credit_history strong; management_track_record strong; years_of_clean_financials 4; forecast_exists true (confidence high); customer_concentration 0.20; industry_outlook favorable; market_rate 10%, term 5 yrs.

**Reasoning:**
- Annual payment on $100k @ 10% / 5 yrs ≈ **$26k**. (If only $75k is financed after the $25k owner contribution, ≈ $19k.)
- DSCR (project) = $70k ÷ $26k ≈ **2.7**. DSCR (whole business) = (existing + $70k) ÷ ($10k + $26k) — comfortably above 1.5. Binding DSCR ≈ 2.7 → **strong** (in the 1.5–3.0 band, well over the 1.25 minimum).
- Owner equity % = 25k ÷ 125k = **20%** → within the 10–25% norm → Capital passes.
- Collateral coverage = 90k ÷ 100k = 0.9× → slightly under 1.0× → Collateral **marginal** (curable; strong DSCR/Character offset it, or use a guaranteed loan / finance $75k).
- Character pass (strong credit + track record); Conditions pass (clear asset purpose, favorable outlook, low concentration); forecast present with a clean repayment story.

**Output (abridged):** dscr binding 2.7; owner_equity_pct 0.20; collateral_coverage 0.9; five_cs: character pass, capacity pass, capital pass, collateral marginal, conditions pass; verdict **bankable**; binding_gap "collateral slightly under 1.0× — finance $75k after $25k equity, or seek a guaranteed loan"; recommended_terms_adjustment "finance $75k (payment ≈ $19k, DSCR ≈ 3.7) to fully cover collateral"; recommended_next_skills [debt-service-and-covenant-analysis].

**Executed vs. approval:** the agent scored the 5 C's, computed DSCR/equity/collateral, issued the verdict, and drafted the forecast-backed lender package (L1, auto). Submitting the application, authorizing a credit pull, and signing were held for founder approval; term language was flagged for attorney review.

## Provenance
SOURCE — derived from the Bankability / Creditworthiness Criteria in the Valuation, Money & Financing domain ("being bankable" = describe growth in financial terms + credible repayment; forecast always required; owner skin-in-the-game; DSCR ≥ 1.25 min / 1.5–3.0 strong; ~10–25% owner equity). The 5 C's of Credit and the amortization formula are CLAUDE-DERIVED standard lending knowledge, labeled as such.
