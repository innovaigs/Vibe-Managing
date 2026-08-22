---
name: raise-capital
lead_agent: cfo-agent
collaborators: [strategy-agent]
triggers: ["we need funding", "prepare to raise", "should we get a loan", "are we fundable"]
---

# Workflow: raise-capital

Determine how much is needed, whether the business is fundable, which instrument fits, and prepare the package — with the founder authorizing anything binding.

## 1. Understand
Retrieve: financials (statements + forecast), cash & runway, existing debt + covenants, the use of funds, ownership/control preferences, credit profile, collateral.

## 2. Diagnose
`bankability-assessment` (5 C's, DSCR, equity) → gaps to fundability. `financial-forecast-builder` sizes the need and the ability to service/return capital.
```
IF DSCR < 1.25                       → not debt-ready → fix cash generation first or seek equity
IF strong cash flow, control-averse  → favor debt
IF pre-cash-flow / high growth       → favor equity/alternative
IF small, short need                 → line of credit / revenue-based
```

## 3. Plan
`financing-options-analysis`: match need → instrument (cost, requirements, dilution, fit) + `business-valuation` if equity. Produce the recommendation + a fundability-gap closure plan.

## 4. Execute (risk-tiered)
- Auto (L1): assemble the financials package, forecast, and a data-room checklist; draft the funding narrative.
- Approval (always): submitting applications, signing term sheets, taking on debt, issuing equity.
- Escalate: attorney (terms, equity), accountant (financials).

## 5. Monitor
Fundability metrics; application status; covenant implications of any offer.

## 6. Adapt
If declined or terms poor, close the flagged gaps and revisit instrument choice.

## Guardrails
No application, signing, debt, or equity issuance executes without founder approval + professional review.
