---
name: impact-measurement
description: Define a defensible chain from activity to output, outcome, and impact with baselines, attribution limits, and evidence. Use when a founder or agent needs an evidence-backed impact measurement decision or operating plan.
metadata:
  domain: sustainability
  version: 1.0.0
  autonomy_ceiling: L2
  provenance: CLAUDE
  reads: "company, goals, strategy, metrics, decisions, sustainability"
  writes: "sustainability, metrics, decisions, strategy"
  related_skills: "sustainability-materiality, resource-efficiency, enterprise-risk-management"
  owned_by_agents: "sustainability-agent, adaptation-agent, business-analyst-agent"
---

# Skill: Impact Measurement

## Purpose
Define a defensible chain from activity to output, outcome, and impact with baselines, attribution limits, and evidence. It operationalizes material impacts, resource efficiency, resilience, and defensible reporting for companies of different sizes, models, industries, stages, and jurisdictions.

## When to Use
- The founder asks for a impact measurement diagnosis, decision, plan, or review.
- A KPI, event, dependency, or recurring cadence indicates this capability may constrain a company objective.
- Before committing resources to a material decision in this area.

## When NOT to Use
- Do not use generic benchmarks before `benchmark-calibration` establishes comparability.
- Do not make legal, tax, clinical, safety, engineering, investment, or regulated determinations that require a licensed specialist.
- During an active emergency, invoke the relevant incident/crisis workflow first and use this skill only inside that command structure.

## Required Context
Load `company`, `goals`, `strategy`, relevant `metrics`, prior `decisions`, and the current Digital Twin. Run `business-archetype-classifier`, `industry-operating-profile`, `stage-and-maturity-assessment`, and `regulatory-intensity-classifier` whenever those context records are missing or stale.

## Inputs
```yaml
input:
  intent: string
  decision_horizon: string
  objective: {metric: string, baseline: number|null, target: number|null, deadline: date|null}
  constraints: [{type: string, value: any, hard: boolean}]
  current_state: object
  options: [object]
  evidence: [{claim: string, source: string, as_of: date, confidence: number}]
  industry_profile_id: string
  business_model_profile_ids: [string]
  stage: string
  maturity: integer
  jurisdictions: [string]
  risk_tolerance: object
  authority: {level: string, scopes: [string], budget_limit: number|null}
```

## Missing Information Protocol
1. Retrieve permitted facts from memory and connected systems.
2. Derive only values that have an explicit formula and preserve the source lineage.
3. Ask one concise batch for material facts that cannot be retrieved.
4. Continue with labeled scenarios if optional data is missing; stop if a missing fact could reverse the decision or change an approval boundary.
5. Never invent a benchmark, legal requirement, customer fact, cost, capacity, or probability.

## Diagnostic Questions
- What outcome is being optimized, for whom, by when, and subject to which hard constraints?
- Which business archetype, model, industry, stage, and jurisdiction alter the method?
- What is the current bottleneck, and is it causal or merely correlated?
- Which assumptions drive most of the outcome variance?
- What second-order effects appear in cash, customer value, delivery, people, risk, and strategy?
- Which actions are reversible, observable, and within delegated authority?

## Analysis Framework
1. **Define intended change.** Produce evidence, confidence, and a decision implication before continuing.
2. **map theory of change.** Produce evidence, confidence, and a decision implication before continuing.
3. **select indicators.** Produce evidence, confidence, and a decision implication before continuing.
4. **establish baseline.** Produce evidence, confidence, and a decision implication before continuing.
5. **collect evidence.** Produce evidence, confidence, and a decision implication before continuing.
6. **assess contribution.** Produce evidence, confidence, and a decision implication before continuing.
7. **report limitations.** Produce evidence, confidence, and a decision implication before continuing.
8. **Integrate.** Quantify cross-functional effects, dependencies, uncertainty, and opportunity cost in the Business Digital Twin.
9. **Decide.** Recommend the smallest action portfolio that clears hard constraints and maximizes risk-adjusted expected value.
10. **Learn.** Define leading indicators, review date, expected outcome, and conditions to stop, scale, reverse, or escalate.

Read [`references/domain-playbooks/sustainability.md`](../../../references/domain-playbooks/sustainability.md) when adapting this method to a specific industry, lifecycle stage, maturity level, or business model.

## Calculations
- `risk_adjusted_value = probability_of_success × expected_incremental_value − implementation_cost − expected_downside_loss`
- `expected_downside_loss = Σ(probability_scenario × impact_scenario)`
- `confidence_weighted_value = risk_adjusted_value × evidence_confidence`
- `constraint_headroom = limit − projected_use` for maximum constraints; invert for minimum constraints.
- Use the domain formulas in the referenced playbook and the active industry profile. Show units, period, definition, source, and uncertainty for every calculated metric.

## Decision Rules
- IF a hard constraint is breached in any credible scenario → THEN reject, redesign, sequence, or escalate the option.
- IF evidence could reasonably reverse the recommendation → THEN run the cheapest decision-relevant test before commitment.
- IF a lower-cost reversible action can produce equivalent information or value → THEN prefer it.
- IF expected value is positive but liquidity, safety, legal, privacy, employment, or trust exposure exceeds appetite → THEN require mitigation and human approval before action.
- IF the company lacks the maturity or capacity to absorb the proposed system → THEN recommend the next maturity step, not the end-state design.
- IF actual leading indicators cross a stop or escalation threshold → THEN pause automation, preserve evidence, and route to the accountable human.

## Procedure
1. Classify intent, stakes, reversibility, and required decision date.
2. Load and validate adaptation context; mark stale or low-confidence facts.
3. Establish baseline, target, counterfactual, and hard constraints.
4. Execute the analysis framework and quantify alternatives.
5. Simulate primary, downside, and stress cases in the Digital Twin.
6. Rank options by constraint compliance, risk-adjusted value, confidence, time-to-value, and reversibility.
7. Produce decision, plan, owners, dependencies, approvals, monitoring, and learning record.
8. Execute only authorized low-risk reversible actions; log every action and result.

## Output
```yaml
output:
  diagnosis: {finding: string, evidence: [string], confidence: number}
  context_fit: {archetype: string, industry: string, models: [string], stage: string, maturity: integer}
  options:
    - {id: string, expected_value: number|null, downside: number|null, confidence: number, constraints_passed: boolean, dependencies: [string]}
  recommendation: {option_id: string, rationale: string, assumptions: [string]}
  plan:
    - {action: string, owner: string, due: date|null, cost: number|null, risk_tier: string, approval: string|null}
  metrics: [{key: string, baseline: number|null, target: number|null, leading: boolean, threshold: object}]
  monitoring: {cadence: string, stop_conditions: [string], scale_conditions: [string], review_date: date|null}
  escalations: [{condition: string, role: string, reason: string}]
  decision_record: object
```

## Recommendations
Prioritize mandatory controls first, then constraint removal, then highest confidence-weighted value. Prefer actions that are reversible, fast to learn from, cash-conscious, compatible with operating maturity, and beneficial across multiple scenarios. State what should not be done and why.

## Execution Opportunities
- Read and reconcile scoped records; calculate metrics; run simulations; create internal drafts, tasks, dashboards, scorecards, and alerts (L0–L2).
- Update approved internal plans and append decision/learning records when schemas validate (L1–L2).
- Never infer authorization to communicate externally, commit money, change employment, alter production, or accept legal obligations.

## Human Approval Requirements
Approval is required for money movement, binding commitments, external publication or communication, pricing changes, customer-impacting changes, production or safety changes, employment actions, access changes, personal-data use, policy exceptions, and actions above budget or risk limits.

## Escalation Conditions
- Escalate regulated interpretation to qualified legal/compliance specialists.
- Escalate accounting, tax, assurance, valuation reliance, or financing commitments to the CFO/accountant and founder.
- Escalate safety, clinical, engineering, cybersecurity, privacy, labor, and environmental matters to the appropriate accountable professional.
- Escalate cross-functional tradeoffs beyond delegated authority to the founder or executive owner.

## KPIs
- `outcome progress` — baseline, target, actual, trend, confidence, and owner.
- `evidence strength` — baseline, target, actual, trend, confidence, and owner.
- `beneficiary coverage` — baseline, target, actual, trend, confidence, and owner.
- Recommendation calibration: expected versus actual result, with variance explanation.
- Execution quality: actions completed, control exceptions, time-to-value, and unintended effects.

## Monitoring
Monitor leading indicators at the shortest useful cadence, outcome metrics at the natural business cycle, constraint headroom continuously where possible, and decision assumptions whenever relevant external or internal conditions change.

## Follow-Up
Re-run after a material event, threshold breach, assumption change, strategy update, or completed learning cycle. Otherwise review at the cadence specified by the active industry profile and business stage.

## Related Skills
- `sustainability-materiality`
- `resource-efficiency`
- `enterprise-risk-management`

## Guardrails
- Preserve human ownership of values, major strategy, regulated judgments, irreversible actions, and material capital or people decisions.
- Minimize sensitive data; enforce purpose limitation, least privilege, retention, and auditability.
- Separate facts, estimates, assumptions, and recommendations. Attach confidence and freshness to each.
- Optimize the whole business, not one metric; explicitly check for harm transferred to customers, workers, suppliers, cash, quality, security, society, or future capability.
- Do not treat profile defaults or benchmarks as facts about the company.

## Example
**Founder intent:** "Use impact measurement to improve our outcome without exceeding our cash, risk, or capacity limits."

The agent loads the company's archetype, industry, business models, stage, maturity, jurisdictions, objective, and live twin. It identifies the binding constraint, compares at least three feasible options against the counterfactual, and recommends the option with the highest confidence-weighted value that passes every hard constraint. It prepares the plan and monitoring record, executes only authorized reversible internal actions, and routes material commitments to the named approver. At review, it compares expected versus actual results and updates the assumption record.

## Provenance
`CLAUDE-DERIVED`. Added as a business-necessary advanced capability beyond the original source material. It must be validated against authoritative industry, jurisdiction, and company evidence before consequential use. See `internal/PROVENANCE_MAP.md`.
