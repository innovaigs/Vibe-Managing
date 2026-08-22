---
name: fix-cash
lead_agent: cfo-agent
collaborators: [operations-agent, strategy-agent]
triggers: ["running out of cash", "profitable but no money", "cash is tight", "will we make payroll"]
---

# Workflow: fix-cash

Stabilize cash and fix the cause — not just the symptom.

## 1. Understand
Retrieve: cash & accounts; monthly burn; income statement + balance sheet (≥2 periods); A/R + aging; A/P + terms; inventory; debt schedule + covenants; upcoming large outflows.

## 2. Diagnose
`cash-runway-monitor` (how long) + `cash-flow-diagnostic` (why — the net-income→operating-cash bridge).
```
IF net income negative            → profitability   → (reduce-spend / pricing / grow-revenue)
IF DSO rising (A/R up)            → collections     → working-capital-optimizer
IF DIO rising (inventory up)      → inventory       → working-capital-optimizer
IF DPO too low (paying too fast)  → payables timing → renegotiate terms
IF capex/principal spike          → financing       → debt-service-and-covenant-analysis
IF one-off timing                 → timing          → short bridge plan
```

## 3. Plan
Cash-recovery plan: prioritized levers (collections, inventory, payables timing, cost cuts, pricing, financing) with expected cash freed + timeline. `scenario-and-sensitivity-analysis` base/downside. Target: runway above the safe threshold.

## 4. Execute (risk-tiered)
- Auto (L2): draft collection reminders (approval to send), flag slow-pay accounts, build cash dashboard, model scenarios.
- Approval (always): sending customer comms, changing terms, drawing credit, cost cuts affecting people/vendors, any financing.
- Escalate: accountant/CPA (tax/accounting); founder (all money moves).

## 5. Monitor
Daily cash watch; weekly A/R aging + burn; covenant headroom.

## 6. Adapt
Compare cash-freed actual vs. expected; if collections lag, shift the lever mix; re-forecast.

## Guardrails
No money movement, term change, or customer communication executes without founder approval. Cash/covenant indicators evaluated every cycle.
