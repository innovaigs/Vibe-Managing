---
name: monthly-review
lead_agent: business-analyst-agent
collaborators: [cfo-agent, growth-agent]
triggers: ["monthly review", "how did we do last month", "period close", cadence:monthly]
---

# Workflow: monthly-review

The learning loop. Compare plan to reality, understand every material gap, and adapt — so the system gets smarter each month.

## 1. Understand (data-completeness gate)
Assemble the month's actuals: P&L, balance sheet, cash flow, KPIs, and the forecast/plan for the same period. **Gate:** if key actuals are missing or unreconciled, flag and pause — do not diagnose on incomplete data.

## 2. Diagnose — COMPARE → CLASSIFY → DIAGNOSE
`monthly-business-review` + `variance-diagnosis`.
- **Compare** each line to three baselines: forecast, prior month, prior year.
- **Classify** variances by size band (immaterial / notable / material).
- **Diagnose Top Movers**: attribute each material variance to line-item drivers.
```
IF revenue miss                → decompose to volume/price/mix/channel; find the driver
IF favorable COST variance     → CHECK activity: is it cheap because something stalled?
                                 (do NOT celebrate a cost saving that means work didn't happen)
IF metrics that co-move diverge → flag as a data or process problem, not a win
```

## 3. Adapt (Plan)
Update assumptions where actual diverged from expected; re-forecast forward; reprioritize next month's initiatives.

## 4. Execute (risk-tiered)
- Auto (L1–L2): update dashboards, write the review report, adjust the forward forecast model, create follow-up tasks.
- Approval: any spend/plan change that commits money or people.

## 5. Monitor
Carry the updated leading indicators into the next cycle.

## 6. Remember
Write decision records for each adaptation with expected outcomes; these are what next month's review measures against.

## Guardrails
Never present incomplete-data results as conclusions. A favorable variance is not a win until activity confirms it.
