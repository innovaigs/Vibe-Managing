---
name: should-we-hire
lead_agent: people-agent
collaborators: [cfo-agent]
triggers: ["can we hire", "should I hire", "need to hire", "what roles next year", "I'm doing too much"]
---

# Workflow: should-we-hire

Decide whether, whom, and when to hire — grounded in capacity and cash, with the decision itself held for the founder.

## 1. Understand
Retrieve: workload & capacity by function; founder-load index; revenue & pipeline; gross margin; cash & runway; comp structure; role-specific productivity (e.g. sales).

## 2. Diagnose
`founder-capacity-diagnostic` (is the founder the bottleneck? is the work delegable?) and confirm the need is real vs. a process/automation fix (`automation-triage`). For revenue roles, confirm pipeline supports added capacity.

## 3. Plan
`hiring-plan-builder` + `financial-forecast-builder`: role(s), timing, fully-loaded cost, expected contribution, ramp-to-productivity, payback; test against runway and break-even.
```
IF runway after hires < threshold           → don't hire now; stage or bridge first
IF revenue role & pipeline supports          → phase hires to pipeline ramp
IF need episodic/uncertain                   → contractor/fractional before FTE
IF founder time freed value > hire cost       → strong hire case
```

## 4. Execute (risk-tiered)
- Auto (L1–L2): draft job descriptions, interview guides + scorecards, onboarding plans, the hiring-plan document + scenarios.
- Approval (always): the hire decision, offers, compensation — with HR/legal escalation.

## 5. Monitor
Post-hire: ramp vs. plan, capacity relief, runway impact vs. forecast.

## 6. Adapt
If a hire underdelivers vs. expected contribution by the review point, diagnose (fit/ramp/pipeline) and adjust.

## Guardrails
Hiring, offers, and compensation ALWAYS require founder approval and route employment-law questions to HR/attorney. Individual comp/performance stays in restricted scope.
