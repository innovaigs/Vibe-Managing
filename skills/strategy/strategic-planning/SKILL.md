---
name: strategic-planning
domain: strategy
version: 0.1.0
autonomy_ceiling: L1
provenance: SYNTH
reads: [company, founders, finance, customers, offerings, market, team, metrics, risks, goals, strategy]
writes: [strategy, goals, decisions, metrics]
related_skills: [business-health-diagnostic, opportunity-feasibility-analysis, growth-lever-selector, resource-gap-analysis, initiative-prioritization, exit-readiness-analysis, risk-diagnostic]
owned_by_agents: [strategy-agent, orchestrator]
---

# Skill: Strategic Planning

## Purpose
Convert diagnosis and opportunity into a targeted, tactical, time-bound plan: a small set of prioritized objectives, the resource allocation behind them, measurable targets, and named owners. Produces the founder-owned operational plan that ties the foundation work (opportunity, feasibility, resources, risks, aspiration, exit) into one coherent direction everyone can act on.

## When to Use
- The founder asks "what should we focus on?", "what's the plan for the next quarter/year?"
- After `business-health-diagnostic` surfaces a prioritized problem list, or after a "go" opportunity is validated.
- At the start of a planning cycle (quarterly/annual) or after a major change (new opportunity, crisis, funding).
- To align disparate analyses (levers, resource gaps, risks) into a single set of objectives.

## When NOT to Use
- No diagnosis/opportunity exists yet → run `business-health-diagnostic` and/or `opportunity-feasibility-analysis` first.
- The task is only to rank/sequence a known initiative list → `initiative-prioritization` (this skill calls it).
- The task is a single-domain deep plan (e.g., a marketing campaign plan) → the domain skill.
- The founder wants creative options, not a plan → `idea-expansion`.

## Required Context
Reads the full strategic picture: `company` (mission/vision/values, stage, model), `founders` (aspiration, capacity, exit intent), `finance` (capital, runway, margins — the "Money" factor), `customers`, `offerings`, `market`, `team` (the "Management" factor), `metrics`, `risks`, `goals`. Requires at least one of: a health diagnosis, a validated opportunity, or an explicit founder goal to plan toward. Aspiration and exit intent shape the plan's ambition and horizon.

## Inputs
```yaml
input:
  planning_horizon: str               # e.g., "next 12 months" (targeted/tactical/timely)
  inputs_from_upstream:
    health_findings: [object]         # ranked findings from business-health-diagnostic
    validated_opportunities: [object] # go/refine verdicts from opportunity-feasibility-analysis
    chosen_levers: [object]           # from growth-lever-selector
    resource_gaps: [object]           # from resource-gap-analysis
    open_risks: [object]              # from risk-diagnostic
  founder:
    aspiration: str                   # how big / what kind of business
    exit_intent: str                  # from exit-readiness-analysis, if set
    constraints: [str]                # budget, no-new-hires, time, values
    mission_vision_values: object
  resources_available: {capital: number, people_capacity: str, time: str}
  three_M: {management: enum(strong, adequate, weak), market: enum(favorable, neutral, unfavorable), money: number}
```

## Missing Information Protocol
1. Pull upstream analysis outputs from memory; if a key one is missing (e.g., no validated opportunity for a growth objective), run or request it rather than planning on an unvalidated basis.
2. Aspiration, exit intent, and constraints must come from the founder — ask in one batched set if absent; do not assume ambition or timeline.
3. If resources_available is unknown, flag it as a gating unknown — a plan without a resource picture is a wish list.
4. Never allocate money or people the business doesn't have; if objectives exceed capacity, surface the over-commitment explicitly.

## Diagnostic Questions
- Where do we want to go (aspiration), and by when (horizon)?
- What must be true to get there — which few objectives matter most this cycle?
- Are Management, Market, and Money adequate for these objectives? Which is the binding constraint?
- What are we NOT doing this cycle (explicit non-goals)?
- How is each objective measured (target, metric, owner, deadline)?
- Does the plan align with the founder's values, aspiration, and exit intent?
- What risks could derail it, and are they owned?

## Analysis Framework
A synthesis-and-allocation method producing a Growth-Plan-style operational plan (targeted, tactical, timely, founder-owned):
1. **Consolidate** upstream inputs (health findings, opportunities, levers, resource gaps, risks) into candidate objectives.
2. **Prioritize to a few** objectives (typically 3–5) — focus beats breadth; capacity is finite.
3. **3M gate** each objective — confirm Management/Market/Money adequacy; gate or sequence any that fail.
4. **Allocate** resources (capital, people, time) across the chosen objectives; check total vs. available.
5. **Make measurable** — every objective gets a target metric (with purpose, source, and the decision it drives), an owner, and a deadline.
6. **Set non-goals** — name what is explicitly deprioritized this cycle.
7. **Align** — check the plan against aspiration, values, and exit intent.
8. **Sequence** — hand the objective's initiatives to `initiative-prioritization` for a roadmap.
Governed by the dashboard triad: Accountability | Alignment | Performance.

## Calculations
- **Resource allocation balance:** `sum(objective_allocations) ≤ resources_available` for capital, people-capacity, and time. If demand > supply → over-commitment flag with the overage quantified.
- **Objective priority score (SYNTH):** `Priority = 0.4·strategic_impact + 0.3·alignment_to_aspiration + 0.2·three_M_readiness + 0.1·(1 − risk)`, each 0–1. Used to cut a long candidate list to the vital few.
- **3M adequacy per objective:** `min(management, market, money_adequacy)`; "weak" → gate or sequence-later.
- **Target-setting patterns (illustrative, from source examples):** objectives can be quantified as a target revenue lift (e.g., +X%), a target margin, a market-capture target, or a customer-milestone ladder (first 5 → next 25 → next 100). These are targeting patterns, not benchmarks.
- **Metric-design rule:** every objective's metric must have a stated purpose (why), a named data source, and the decision it drives.

## Decision Rules
- **IF** candidate objectives exceed ~3–5 **THEN** cut to the vital few by priority score — an unfocused plan is a failure mode.
- **IF** total allocation > resources available **THEN** either cut an objective or reduce scope; never publish an over-committed plan without flagging it.
- **IF** an objective's binding 3M factor is weak **THEN** sequence a "fix the factor" objective first, or gate the objective.
- **IF** the plan conflicts with the founder's exit intent (e.g., heavy owner-dependent build when planning to sell soon) **THEN** flag the misalignment for the founder.
- **IF** an objective lacks a measurable target, owner, or deadline **THEN** it is not plan-ready — complete it or drop it.
- **IF** a high open risk threatens an objective **THEN** attach its mitigation as a plan dependency.
- **IF** aspiration is conservative **THEN** favor stability/quality objectives over aggressive expansion.
- **IF** cash runway is short **THEN** a cash/stability objective takes precedence over growth objectives.

## Procedure
1. Gather upstream inputs and founder aspiration/exit/constraints.
2. Consolidate candidate objectives; score and cut to the vital few (3–5).
3. Apply the 3M gate; sequence or gate weak-factor objectives.
4. Allocate capital/people/time; check against availability; flag over-commitment.
5. Attach a measurable target (metric + purpose + source + decision), owner, and deadline to each objective.
6. Define explicit non-goals for the cycle.
7. Align the plan with values, aspiration, and exit intent; flag conflicts.
8. Attach risk mitigations as dependencies for at-risk objectives.
9. Hand initiatives to `initiative-prioritization` for sequencing.
10. Write the plan to `strategy`/`goals` and a decision record; present to the founder for approval (L1).

## Output
```yaml
output:
  horizon: str
  north_star: str                     # the one thing this cycle is really about
  objectives:
    - objective: str
      priority_rank: int
      strategic_rationale: str
      target: {metric: str, value: number, purpose: str, data_source: str, decision_it_drives: str}
      owner: str
      deadline: str
      allocation: {capital: number, people: str, time: str}
      three_M_status: {management: str, market: str, money: str, binding_constraint: str, gated: bool}
      dependencies: [str]             # incl. risk mitigations, resource closures
      linked_initiatives: [str]       # handed to initiative-prioritization
  non_goals: [str]                    # explicitly deprioritized this cycle
  allocation_summary: {capital_used: number, capital_available: number, over_committed: bool}
  alignment_check: {aspiration: str, values: str, exit_intent: str}   # aligned / conflict + note
  key_risks_to_plan: [ {risk: str, mitigation: str, owner: str} ]
  recommended_next_skills: [str]
```

## Recommendations
The plan is deliberately narrow — a north star plus 3–5 measurable objectives — because focus and finite capacity are the whole point; a long list is treated as a failure. Every objective is plan-ready only if it has a target, an owner, and a deadline, and survives the 3M gate and the resource-allocation check. Alignment to aspiration, values, and exit intent is explicit, so the plan serves the founder's actual goals, not generic growth.

## Execution Opportunities
- Write the plan to `strategy`/`goals`, set the target metrics on the dashboard, and record a decision — reversible, LOW.
- Create internal objectives/tasks and hand initiatives to `initiative-prioritization` — reversible, LOW.
- Draft a one-page plan brief for the founder and team — reversible, LOW.
- Schedule the plan review cadence as internal reminders — reversible, LOW.
The plan itself is a proposal; the business actions inside it (hiring, spending, market entry, contracts) are executed by their own skills under their own approvals — never by this skill.

## Human Approval Requirements
- The overall plan and its resource allocation require founder approval before it becomes the operating plan (it commits money and people).
- Any objective involving hiring, financing, contracts, or external commitments carries those domains' approval requirements when executed.
- Over-committed plans are never finalized without the founder explicitly accepting the trade-off.

## Escalation Conditions
- **Plan requires capital/financing beyond available** → founder (+ accountant).
- **Plan implies hiring/role changes** → founder (+ HR).
- **Plan conflicts with exit intent or values** → founder (strategic/values call).
- **Objectives exceed capacity and the founder won't cut** → surface the over-commitment risk; do not silently proceed.
- **A regulated objective (tax, legal, compliance)** → route to the specialist.

## KPIs
- Objective attainment: % of objectives hitting their target by deadline.
- Focus: number of active objectives held to the vital few (no scope creep).
- Allocation accuracy: planned vs. actual resource use.
- Alignment: founder-reported fit between the plan and their aspiration/exit intent.

## Monitoring
Review objectives against targets on the plan cadence; watch for scope creep (new objectives added mid-cycle), over-allocation, and slipping dependencies. Re-run planning if a Critical health finding, a new validated opportunity, or a resource/risk change invalidates the basis.

## Follow-Up
- Time-triggered: each planning cycle (quarterly/annual).
- Event-triggered: after a Critical `business-health-diagnostic` finding, a new "go" opportunity, a crisis, or a funding change.
- Feeds `initiative-prioritization` (sequencing) and is checked against `exit-readiness-analysis`.

## Related Skills
Consumes outputs of `business-health-diagnostic`, `opportunity-feasibility-analysis`, `growth-lever-selector`, `resource-gap-analysis`, `risk-diagnostic`, and `exit-readiness-analysis`. Hands off to `initiative-prioritization`.

## Guardrails
- Never finalize an over-committed plan without an explicit founder trade-off decision.
- Never allocate money/people the business doesn't have.
- Keep objectives to the vital few; resist an everything-list.
- Every objective must be measurable, owned, and dated or it is dropped.
- Align to the founder's real aspiration and exit intent — do not impose generic aggressive growth.
- Do not execute the plan's business actions — route each to its approval-gated skill.

## Example
**Context:** From `business-health-diagnostic`: Cash Critical (1.5 mo runway), customer concentration 47%, margin 14 pts below target, revenue plateau. Founder aspiration: balanced growth, exit intent "sell to a strategic buyer in ~5 years." Resources: $30k discretionary, founder + 2 staff, 12-month horizon.
**Reasoning:** Cash-critical → stability objective first. Concentration + plateau → diversification objective (validated channel lever). Margin → pricing objective. Vital few = 3. Exit intent (sell in 5 yrs) aligns with reducing owner-dependence and concentration → reinforces the diversification objective; flag any owner-dependent build.
**Objectives (abridged):**
1. **Stabilize cash** — target: runway ≥4 months by month 3 (metric: months of runway; source: accounting; drives go/no-go on spending). Owner: founder (+accountant). Allocation: minimal capital, high founder time. Priority 1.
2. **Diversify revenue via subscription channel** — target: reduce top-customer share to <30% and add $6k/mo recurring by month 9. Owner: cross-trained lead. Allocation: $21k, staff time. Depends on `resource-gap-analysis` closures. Priority 2.
3. **Restore margin** — target: gross margin +8 pts by month 6 via pricing + COGS. Owner: founder. Priority 3.
**Non-goals:** regional wholesale expansion (deferred), new product tiers (deferred).
**allocation_summary:** capital_used $21k ≤ $30k → not over-committed. **alignment_check:** aspiration aligned; exit_intent aligned (diversification + less owner-dependence raises sale value); values aligned.
**Executed vs. approval:** Wrote the 3-objective plan + dashboard targets, handed initiatives to `initiative-prioritization`, drafted the founder brief (all L1). The plan and its $21k allocation are held for founder approval before becoming the operating plan.

## Provenance
SYNTH. Assembles the source's Growth Plan deliverable model (targeted/tactical/timely, founder-owned, opportunity-anchored), the Three Growth Factors gate (Management/Market/Money), the metric-design rule (purpose/source/decision), aspiration and exit-strategy alignment, and the dashboard governance triad into an integrated planning-and-allocation capability. Priority-scoring weights are SYNTH defaults. See `internal/PROVENANCE_MAP.md`.
