---
name: <skill-name>            # kebab-case, matches folder
domain: <strategy|finance|growth|sales|marketing|operations|people|leadership|risk|legal>
version: 0.1.0
autonomy_ceiling: <L0|L1|L2|L3>   # max autonomy this skill's ACTIONS may reach; analysis is always allowed
provenance: <SOURCE|SYNTH|CLAUDE>
reads: [<memory namespaces / twin views>]
writes: [<memory namespaces>]
related_skills: [<skill-name>, ...]
owned_by_agents: [<agent-name>, ...]
---

# Skill: <Human Readable Name>

## Purpose
<What business problem this solves, in one or two sentences. Founder-outcome framing.>

## When to Use
<The user intent(s) or business condition(s) that should trigger this skill. Include example founder phrasings.>

## When NOT to Use
<Situations that require another skill, a specialist, or a human. Point to the right alternative.>

## Required Context
<What must be known about the company before this skill can run. Reference Business Memory namespaces / twin views.>

## Inputs
```yaml
# Structured input schema
input:
  <field>: <type>   # description
```

## Missing Information Protocol
<What the agent does when a required input is unavailable: fetch via integration, compute, or ask the founder ONE concise batch. What it must never assume.>

## Diagnostic Questions
<The questions the agent asks or answers internally to do the work well.>

## Analysis Framework
<The exact reasoning framework / method the skill applies. Steps, models, structure.>

## Calculations
<Every relevant formula, with variable definitions and benchmark/threshold values. "None" if not applicable.>

## Decision Rules
<Explicit IF <condition> THEN <action/conclusion> rules.>

## Procedure
<Step-by-step operating procedure the agent follows, start to finish.>

## Output
```yaml
# Exact structured output
output:
  <field>: <type>   # description
```

## Recommendations
<How recommendations are formed and prioritized (impact, effort, cost, risk, reversibility).>

## Execution Opportunities
<Which actions this skill could automate (create tasks, draft docs, update dashboards, etc.), each with its risk tier.>

## Human Approval Requirements
<Which actions must be held for founder/human approval before execution. Must comply with AUTONOMY_AND_APPROVAL_MODEL.md.>

## Escalation Conditions
<When to escalate, and to whom: founder, accountant, lawyer, HR, executive, other specialist.>

## KPIs
<How the success of this skill's output is measured.>

## Monitoring
<What to watch after the skill runs / after any action it triggers.>

## Follow-Up
<When this skill should run again (event- or time-triggered).>

## Related Skills
<Other Vibe Managing skills this one calls or hands off to.>

## Guardrails
<Financial, compliance, legal, employment, privacy risks; irreversible actions; handling of uncertain/low-confidence information.>

## Example
<At least one realistic worked example: founder input → skill reasoning → output → what got executed vs. sent for approval.>

## Provenance
<SOURCE / SYNTH / CLAUDE, and which source domain/framework it derives from. See internal/PROVENANCE_MAP.md.>
