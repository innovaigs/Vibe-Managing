# Agent: <Human Readable Name>

> Template for every Vibe Managing agent spec. Each agent folder contains this `AGENT.md` (the human-readable specification) plus `agent.yaml` (the machine-readable config that conforms to `schemas/agent.schema.json`). Fill every section substantively — an empty section means an undefined agent. See `AGENT_REGISTRY.md` for the responsibility map and `AUTONOMY_AND_APPROVAL_MODEL.md` for the permission rules every section below must obey.

---

## Agent Name
`<agent-name>` (kebab-case, matches folder and `agent.yaml:name`). One line on the seat this agent holds.

## Mission
<The single outcome this agent exists to produce, in founder-outcome terms. One or two sentences.>

## Business Responsibilities
<What this agent owns end-to-end. A bulleted list of the business functions, artifacts, and outcomes it is accountable for.>

## Skills Available
<The exact skills from `SKILL_REGISTRY.md` this agent composes, each with a one-line note on when it fires. Delegated skills (owned by another agent but invoked through it) are marked as such.>

## Data Required
<The Business Memory namespaces and Digital Twin views this agent reads and writes, and the external data it depends on. Reference `BUSINESS_MEMORY_SCHEMA.md`. Note sensitivity tiers where relevant.>

## Systems It Connects To
<The integration categories (finance, crm_sales, marketing, people, operations, comms, data, documents) this agent draws on, described by function — never by vendor name. See `INTEGRATION_ARCHITECTURE.md`.>

## Tools It Can Use
<The connector capabilities available to this agent, expressed as generic functions (e.g. "bookkeeping read", "CRM write", "internal task creation"). Governed by least-privilege scopes.>

## Decisions It Can Make
<The judgments this agent is authorized to reach on its own (analysis conclusions, prioritizations, recommendations). These are decisions, not executable actions.>

## Actions It Can Perform Autonomously
<Reversible, low-risk actions this agent may execute at its granted autonomy level (L2 unless noted), with notice and audit. Each must be reversible and pre-approved by action-type.>

## Actions Requiring Founder Approval
<Actions this agent may prepare (L1 draft) but must route to the founder before execution. Must include every always-approval action from the autonomy model that this agent could touch.>

## Actions Prohibited Entirely
<Actions this agent must never take, even with approval — it directs the founder or a specialist to perform them. Mirrors the platform safety rules.>

## KPIs Owned
<The metrics this agent is accountable for moving/monitoring, with definitions where non-obvious. These feed the Business Health Engine.>

## Recurring Responsibilities
### Daily
<What this agent does every day (or on the continuous loop).>
### Weekly
<Weekly loop responsibilities.>
### Monthly
<Monthly loop responsibilities.>
### Quarterly
<Quarterly loop responsibilities.>

## Trigger-Based Workflows
<Event-driven workflows this agent leads or joins (from `WORKFLOW_REGISTRY.md`), and the conditions that fire them.>

## Escalation Logic
<When this agent stops and escalates rather than acting, and to whom (founder, accountant, attorney, HR, other specialist). Follows the escalation ladder in the autonomy model. Every escalation carries situation, knowledge, confidence, decision needed, recommendation.>

## Collaboration With Other Agents
<Which agents this one hands off to, requests inputs from, or is cross-checked by. Cross-impact rules (e.g. cost checks, runway checks, legal checks) are explicit here.>

## Memory Requirements
<What this agent must persist to Business Memory (decisions, metrics, artifacts) and what it must read before acting. All writes to finance/team/decisions are audited.>

## Audit Requirements
<Every proposed, approved, executed, or rejected action writes an immutable audit entry linked to a decision record. State any agent-specific audit obligations here.>
