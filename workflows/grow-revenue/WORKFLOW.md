---
name: grow-revenue
lead_agent: growth-agent
collaborators: [sales-agent, marketing-agent, cfo-agent]
triggers: ["grow revenue", "we need more customers", "sales slowed", "why did growth stop", "hit 20% this quarter"]
---

# Workflow: grow-revenue

Turn a revenue goal or slowdown into a diagnosed, prioritized, executing plan — not advice.

## 1. Understand
Retrieve: current & historical revenue; revenue by offering/segment; pipeline & conversion; pricing & gross margin; churn; acquisition channels & CAC; delivery capacity; cash runway (spend constraint).

## 2. Diagnose — isolate the binding constraint
Skills: `growth-pathway-classifier`, `variance-diagnosis`, then the constraint-specific skill.
```
IF traffic/leads down            → demand constraint    → channel-selection, marketing-funnel-planner
IF conversion down               → conversion constraint → website-conversion-audit, sales-process-design
IF churn up                      → retention constraint  → (improve-retention)
IF price/mix eroding margin      → pricing constraint    → break-even-and-pricing-analysis
IF demand ok, can't deliver      → capacity constraint   → (scale-operations)
IF one customer dominates        → concentration risk    → risk-diagnostic
```
Validate each hypothesis against data before acting.

## 3. Plan
`initiative-prioritization`: 2–4 initiatives with expected revenue impact, owner, timeline, budget, KPIs. CFO agent checks total spend against runway.

## 4. Execute (risk-tiered)
- Auto (L2, reversible): target lists, draft campaigns/content, CRM tasks, tracking dashboard, internal-review experiments.
- Approval: ad budget, price changes, public content, customer outreach.

## 5. Monitor
Leading: traffic, leads, reply/booking rate, conversion, pipeline coverage. Lagging: revenue, CAC, margin, churn.

## 6. Adapt
Weekly/monthly `variance-diagnosis`: underperforming initiative → diagnose → adjust or kill → next experiment. Write lessons to the decision store.

## Guardrails
No spend, pricing change, or public/customer communication executes without founder approval. Growth that increases customer concentration is flagged, not celebrated.
