---
name: evaluate-opportunity
lead_agent: strategy-agent
collaborators: [cfo-agent, risk-agent, marketing-agent]
triggers: ["should we launch", "should we enter this market", "is this worth pursuing", "new product idea"]
---

# Workflow: evaluate-opportunity

Give a go / refine / kill decision on a new opportunity — with the economics and risks made explicit.

## 1. Understand
Capture the opportunity (what, for whom, why us). Retrieve: current capabilities, resources, cash, and current strategic focus (opportunity cost).

## 2. Diagnose
`opportunity-feasibility-analysis` across six dimensions — customer, demand, competition, economics, resources/capability, risk. `resource-gap-analysis` for what's missing. `financial-forecast-builder` / incremental-economics for P&L, initial investment, break-even, ROI, payback. `risk-diagnostic` for downside.
```
IF customer/demand unproven          → refine: validate demand before committing
IF economics don't clear the bar     → kill or reprice
IF resource/capability gap large     → refine: close gaps or partner first
IF fit + economics + demand strong   → go (phased)
IF distracts from a stronger priority → defer (opportunity cost)
```

## 3. Plan
Go/refine/kill with conditions. If go: a phased validation plan with milestone gates, budget, owners, and success metrics.

## 4. Execute (risk-tiered)
- Auto (L1): draft validation experiments, research tasks, the feasibility memo.
- Approval: any commitment of money, hires, or public launch.

## 5. Monitor
Validation milestones + spend vs. budget; demand signals.

## 6. Adapt
At each gate: proceed / pivot / kill based on validated evidence.

## Guardrails
No launch, spend, or hire executes without founder approval. Feasibility conclusions state their confidence and the data gaps behind them.
