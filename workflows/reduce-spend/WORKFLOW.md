---
name: reduce-spend
lead_agent: cfo-agent
collaborators: [operations-agent, people-agent]
triggers: ["spending too much", "where's the money going", "cut costs", "reduce burn"]
---

# Workflow: reduce-spend

Find where money goes and cut the right things without breaking the business.

## 1. Understand
Retrieve: income statement (12 mo) with categories, vendor list + contracts, payroll totals, tool/software spend, spend trend vs. revenue.

## 2. Diagnose
`financial-statement-analysis` (common-size + trend) + `variance-diagnosis`: rank cost lines by size, growth, and % of revenue; find where spend outgrew revenue.
```
IF payroll % of revenue rising      → structural people cost → org/capacity review
IF tool/vendor sprawl               → consolidation opportunity
IF a line spiked vs. trend          → investigate the driver
IF COGS creep                        → pricing/supplier review
```

## 3. Plan
Rank cuts by savings × reversibility × business-risk. Never cut what drives revenue or breaches obligations. Produce a savings plan with expected $/mo and timeline.

## 4. Execute (risk-tiered)
- Auto (L2): build spend dashboard, tag transactions, draft a consolidation list with cancellation steps.
- Approval: cancel/downgrade subscriptions, renegotiate/terminate vendors, any people cost change (→ People + founder).

## 5. Monitor
opex %, category spend, vendor spend, payroll-to-revenue.

## 6. Adapt
Compare realized savings vs. expected; escalate the lever mix if short.

## Guardrails
Vendor terminations, people-cost changes, and any commitment require founder approval. Cuts that damage revenue or delivery are flagged, not made.
