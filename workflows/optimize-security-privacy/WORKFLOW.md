# Workflow: Optimize Security & Privacy

## Founder intents
"Improve our security & privacy outcomes." · "What is holding this part of the company back?" · "Build and execute the best plan for this area."

## Objective
Optimize security posture, identity, privacy, incident response, and cyber resilience, subject to company cash, capacity, safety, legal, privacy, people, trust, and strategic constraints.

## Orchestration

1. **Adapt:** run `business-archetype-classifier`, `industry-operating-profile`, `stage-and-maturity-assessment`, and `regulatory-intensity-classifier`.
2. **Understand:** retrieve goals, domain state, dependencies, prior decisions, profile overrides, metrics, risk appetite, and delegated authority.
3. **Diagnose:** invoke `security-posture-assessment`, `identity-access-governance`, `security-incident-response`, `privacy-impact-assessment` as required; distinguish evidence from assumptions and symptoms from causes.
4. **Plan:** generate alternatives, counterfactual, scenarios, expected value, constraints, dependencies, owners, budget, leading indicators, and stop/scale rules.
5. **Control:** classify every proposed action by risk, reversibility, scope, and authority. Route approval and specialist review where required.
6. **Execute:** perform only authorized reversible actions; coordinate agents and tools; log all changes.
7. **Monitor:** track critical exposure time, access-policy compliance, incident containment time and guardrail metrics at the appropriate cadence.
8. **Learn:** compare expected to actual, explain variance, update assumptions and profile overrides, and recommend the next best action.

## Output contract
```yaml
workflow_result:
  intent: string
  adaptation_context: object
  diagnosis: [object]
  selected_skills: [string]
  options: [object]
  recommendation: object
  plan: [object]
  approval_queue: [object]
  executed_actions: [object]
  monitoring_plan: object
  decision_record: object
```

## Safety
No optimization may improve a domain metric by silently transferring unacceptable harm or risk elsewhere. High-consequence uncertainty lowers autonomy and increases human review.
