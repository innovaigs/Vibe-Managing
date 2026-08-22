---
name: manage-crisis
lead_agent: risk-agent
collaborators: [cfo-agent, strategy-agent, legal-liaison-agent]
triggers: ["we just lost our biggest client", "emergency", "major disruption", "we're in trouble"]
---

# Workflow: manage-crisis

Stabilize, understand, and recover from an acute disruption — fast, without panic decisions.

## 1. Understand
Capture the event and its blast radius. Retrieve: cash & runway (first), the affected revenue/customers/operations, obligations at risk, and available resources.

## 2. Diagnose
`cash-runway-monitor` (immediate survival window) + `crisis-response-planning` (impact assessment, what must be protected, what can flex) + `risk-diagnostic` (secondary risks triggered).
```
IF runway now < safe threshold        → trigger fix-cash immediately (parallel)
IF a key dependency failed            → business-continuity-plan (backup/redundancy)
IF obligations at legal risk           → legal-liaison-agent → attorney
```

## 3. Plan
A stabilization plan (protect cash, customers, obligations) + a staged recovery plan with milestones. Reframe: what opportunity or structural fix does this crisis reveal?

## 4. Execute (risk-tiered)
- Auto (L1–L2): assemble the situation brief, model cash scenarios, draft internal + (for approval) external communications, create action tasks.
- Approval (always): external communications, financial moves, contractual/legal actions, people actions.
- Escalate: founder immediately; attorney/accountant as triggered.

## 5. Monitor
Daily (or intraday) cash, obligation deadlines, recovery milestones.

## 6. Adapt
Adjust as the situation evolves; capture lessons and convert them into continuity improvements once stable.

## Guardrails
Crisis does not lower the approval bar: money, legal, external, and people actions still require the founder/specialist. The system prepares fast and waits for the human on anything irreversible.
