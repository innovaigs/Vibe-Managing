---
name: hiring-plan-builder
domain: people
version: 0.1.0
autonomy_ceiling: L1
provenance: SYNTH
reads: [team.people, team.org, team.culture, finance, goals, operations, metrics, founders]
writes: [team.org.open_roles, decisions, goals]
related_skills: [founder-capacity-diagnostic, organizational-design, job-description-builder, delegation-planner, culture-diagnostic, hr-process-coverage-audit]
owned_by_agents: [people-agent, cfo-agent]
---

# Skill: Hiring Plan Builder

## Purpose
Decide what roles the company actually needs, whether it can afford them, and when to hire — so the founder adds capacity deliberately instead of reactively. Turns a growth goal plus current workload and financials into a prioritized, costed, sequenced hiring plan.

## When to Use
- Founder asks: "Should we hire?", "What roles do we need next year?", "Can we afford another person?", "Who do I hire first?"
- A growth goal (revenue, output, new market/product) implies capacity the current team cannot deliver.
- The founder-capacity-diagnostic flagged the founder as a bottleneck and recommended a hire.
- Quarterly/annual planning, budget planning, or before committing to a large new contract that needs delivery capacity.

## When NOT to Use
- To offload a single task to an existing person → use `delegation-planner` (delegation may remove the need to hire).
- To confirm the founder is actually the bottleneck → run `founder-capacity-diagnostic` first.
- To redesign the whole org structure / build the full capacity roadmap → use `organizational-design` (this skill is the hiring slice of that plan).
- To write the actual job posting → use `job-description-builder` after a role is approved here.
- Any question about a specific named employee's status, pay, or performance → route to founder + HR/legal; not this skill.

## Required Context
- `goals` — the company vision and the specific growth targets driving the need (revenue, volume, timeline).
- `team.people` — current headcount, roles, responsibilities, `capacity_utilization_pct`, authority_level.
- `team.org.open_roles` — anything already planned/budgeted.
- `finance` — revenue run-rate, gross margin, cash on hand, monthly burn, runway; loaded via CFO agent for cost validation.
- `operations` — current throughput vs. demand, bottleneck locations (from `bottleneck-analysis` if available).
- `company.stage` and `market` — for realistic time-to-fill and comp expectations.

## Inputs
```yaml
input:
  planning_horizon: str              # e.g. "next 12 months", "H1", required
  growth_goals:                      # what the company is trying to achieve
    - goal: str                      # "grow revenue to $2M", "launch product line B"
      target_metric: str
      target_value: number
      by_date: date
  current_team:
    - person_id: str
      role: str
      key_responsibilities: [str]
      capacity_utilization_pct: number   # 0-120; >100 = overloaded
  workload_signals:
    demand_trend: enum(declining, flat, growing, surging)
    known_bottlenecks: [str]         # from operations/bottleneck-analysis
    founder_overloaded: bool         # from founder-capacity-diagnostic
    tasks_stalled_on_founder: [str]
  financials:
    monthly_revenue: number
    gross_margin_pct: number
    cash_on_hand: number
    monthly_burn: number
    runway_months: number
  candidate_roles:                   # optional roles founder already has in mind
    - title: str
      function: str
      reason: str
  constraints:
    max_new_annual_payroll: number   # optional budget cap
    min_runway_floor_months: number  # do not spend below this (default 6)
```

## Missing Information Protocol
1. **Compute before asking.** Derive capacity gaps from workload signals and utilization; derive affordability from `finance` (fully-loaded cost, runway impact). Pull comp benchmarks from `market`/integrations.
2. **Fetch** current team, utilization, and financials from Business Memory / CFO integration before prompting the founder.
3. If still missing, ask the founder **one batched question** covering only the blockers, e.g.: "To size this plan I need three things: (a) your revenue goal and date, (b) current cash and monthly burn, (c) which tasks are currently stuck on you."
4. **Never assume:** compensation levels, that a role is affordable, that demand growth is permanent, or that a person's utilization is accurate without a source. Flag every assumed figure with `assumption: true` and lower `confidence`.

## Diagnostic Questions
- What capability gap does each growth goal create, and is it a *volume* gap (need more hands) or a *capability* gap (need a skill nobody has)?
- Can the gap be closed by delegating (raising an existing person's authority level), automating, or outsourcing before hiring? (Cheapest capacity first.)
- What is the fully-loaded annual cost of each role, and what does it do to runway?
- Is the need durable, or a temporary spike better met by a contractor?
- What is the sequencing dependency — which hire unlocks or must precede another (e.g. hire a doer before a manager)?
- What is the cost of *not* hiring (lost revenue, founder burnout, missed goal, quality failures)?
- How does each hire change the system (ripple effects, who trains them, who they relieve)? → hand to `organizational-design` / new-hire impact.

## Analysis Framework
Synthesized capacity-planning method built on the org-as-system model (F6), the capacity diagnostic (DG2), and the I-Need/I-Have gap map (W6).

1. **Translate goals → capacity demand.** For each growth goal, state the work it requires and the roles/skills that produce that work.
2. **Inventory current capacity.** For each existing person, record utilization and spare/deficit capacity. Flag anyone >90% as effectively full; >100% as overloaded (quality/attrition risk).
3. **Compute the gap** per capability: `demand − current_capacity`. Classify each gap as volume vs. capability.
4. **Choose the cheapest sufficient lever** per gap, in order: delegate/re-seat → automate → outsource/contract → part-time hire → full-time hire. Only escalate to a hire when cheaper levers cannot close the gap.
5. **Cost each proposed hire** (fully loaded, see Calculations) and test against runway floor and budget cap.
6. **Prioritize** by impact × urgency ÷ (cost × risk), reversibility considered (contractor > FTE for reversibility).
7. **Sequence** hires across the horizon respecting dependencies, ramp time (time-to-productivity), and cash timing.
8. **Stress test** the plan: if demand growth is only flat, does the plan still hold? Mark demand-contingent hires as "trigger-based."

## Calculations
- **Fully-loaded annual cost** = base_salary × (1 + loading_factor). `loading_factor` default 0.25–0.40 (payroll tax, benefits, equipment, software, space). Use 0.30 if unknown; flag as assumption.
- **Monthly cost impact** = fully_loaded_annual_cost ÷ 12.
- **Post-hire runway** = cash_on_hand ÷ (current_monthly_burn + Σ monthly_cost_of_planned_hires). Must stay ≥ `min_runway_floor_months` (default 6).
- **Capacity gap (hours or FTE)** = required_capacity − available_capacity, where available = Σ(1 − utilization_pct) across relevant staff.
- **Breakeven / payback** = fully_loaded_annual_cost ÷ expected_annual_margin_contribution_of_role. Prefer roles with payback < 12 months where the role is revenue-linked.
- **Cost of not hiring** = estimated_lost_or_delayed_margin + founder_opportunity_cost. Qualitative if not quantifiable.
- **Priority score** = (impact_1to5 × urgency_1to5) ÷ (cost_tier_1to5 × risk_1to5). Higher = hire sooner.
- Thresholds: utilization >90% = at capacity; runway < floor after a hire = DO NOT auto-recommend that hire (defer or downgrade to contractor).

## Decision Rules
- IF a capability gap can be closed by delegating to a competent existing person THEN recommend `delegation-planner` (raise their authority level) instead of a hire. (DG2, R5)
- IF the need is temporary or demand trend is not "growing/surging" THEN recommend a contractor/part-time over an FTE (reversibility).
- IF post-hire runway < `min_runway_floor_months` THEN do NOT recommend the hire now; mark it "revenue-gated" with the revenue trigger that would fund it.
- IF a role is revenue-generating with payback < 12 months AND runway floor holds THEN prioritize it ahead of overhead roles.
- IF the founder is overloaded AND a task on their list is a proven, delegable, non-strategic task THEN prioritize the hire/delegation that reclaims founder discretionary time.
- IF hiring a manager THEN require the doer roles they will manage to exist or be hired first (sequencing dependency).
- IF two hires compete for the same budget THEN rank by priority score and stagger by dependency and ramp time.
- IF any recommended role touches the status/comp of a *specific existing person* (backfill of a person being moved, restructure) THEN hold for founder + HR/legal.
- IF a hire changes the org system materially THEN attach a new-hire impact check (DG1) and hand to `organizational-design`.

## Procedure
1. Load goals, team, utilization, financials from memory; request CFO cost validation.
2. Confirm the bottleneck/gap is real (reference `founder-capacity-diagnostic` / `bottleneck-analysis`); if unconfirmed, run/queue those first.
3. Translate each growth goal into required work and capabilities.
4. Inventory current capacity and compute per-capability gaps.
5. For each gap, select the cheapest sufficient lever; only genuine hire-needs proceed as roles.
6. For each proposed role, define: title, function, reason, whether FTE/PT/contractor, fully-loaded cost, target start, and the goal it serves.
7. Cost the full plan; compute post-hire runway at each step; drop/defer any hire that breaches the runway floor or budget cap.
8. Prioritize and sequence; mark demand- or revenue-gated hires with explicit triggers.
9. Draft each surviving role into `team.org.open_roles` (status: proposed) and write a `decisions` record with the rationale.
10. Present the plan for founder approval; on approval, hand each greenlit role to `job-description-builder`.

## Output
```yaml
output:
  summary: str                       # 2-3 sentence recommendation
  capacity_gaps:
    - capability: str
      gap_type: enum(volume, capability)
      size: str                      # FTE / hours / qualitative
      cheapest_lever: enum(delegate, automate, outsource, part_time, full_time)
  hiring_plan:
    - role_id: str
      title: str
      function: str
      employment_type: enum(FTE, PT, contractor)
      reason: str                    # which goal/gap it serves
      priority_rank: int
      target_start: date
      trigger: str                   # "" or revenue/demand gate that must fire first
      fully_loaded_annual_cost: number
      payback_months: number|null
      dependencies: [role_id]
      assumptions: [str]
      confidence: number             # 0-1
  financial_impact:
    total_added_annual_payroll: number
    post_plan_monthly_burn: number
    post_plan_runway_months: number
    runway_floor_respected: bool
  deferred_or_rejected:
    - role: str
      reason: str
  cost_of_inaction: str
  next_skills: [str]                  # e.g. job-description-builder, organizational-design
  approval_request_ref: str          # populated when sent for approval
```

## Recommendations
Rank hires by priority score (impact × urgency ÷ cost × risk), then re-order for dependency and cash timing. Prefer reversible capacity (delegate → contractor → PT → FTE) when the need is uncertain. Always present the cost of inaction beside the cost of the hire so the founder trades off real alternatives, and always show what happens to runway.

## Execution Opportunities
- Draft `open_roles` entries in `team.org` with status `proposed` (reversible, LOW) — auto at L2 if granted; otherwise staged at L1.
- Create internal planning tasks / calendar reminders for revenue-gated triggers (reversible, LOW).
- Write a `decisions` record capturing the plan and rationale (reversible, LOW).
- Assemble the approval request package (reversible, LOW).
- NOT executed here: posting a job, extending headcount commitments, or any spend.

## Human Approval Requirements
- **Approving the hiring plan and any headcount commitment ALWAYS requires founder approval** — hiring is an employment action and a spend commitment (per AUTONOMY_AND_APPROVAL_MODEL §4). This skill prepares (L1) only.
- Any plan element that changes a **specific existing employee's** role, seat, or comp requires founder approval AND HR/legal review before it is acted on.
- Committing budget/payroll requires founder (and CFO-agent cost sign-off) approval.

## Escalation Conditions
- Post-hire runway breaches the floor or the plan increases cash risk → founder + accountant.
- A hire implies restructuring or moving a specific person → founder + HR professional.
- Any protected-class, termination, or performance dimension surfaces (e.g. "replace X") → HR professional / attorney; do not proceed.
- Low confidence in demand or financial inputs → surface uncertainty to founder; do not finalize.

## KPIs
- Plan accuracy: roles actually needed vs. planned (avoid over/under-hiring).
- Time-to-fill and time-to-productivity vs. plan.
- Post-hire runway vs. projection; budget adherence.
- Quality-of-hire proxy (90/180-day performance & retention) for roles this plan created.
- % of capacity gaps first closed by cheaper levers (delegation/automation) rather than hiring.

## Monitoring
After approval, watch: actual utilization of the relieved staff, revenue triggers for gated hires, runway drift, and whether the growth goal the hire served is on track. Re-open the plan if demand trend or cash assumptions change materially.

## Follow-Up
Re-run at each planning cycle (quarterly/annual), when a growth goal changes, when a revenue/demand trigger fires, when runway changes materially, or immediately after `founder-capacity-diagnostic` flags a new bottleneck.

## Related Skills
`founder-capacity-diagnostic` (confirm the bottleneck), `organizational-design` (full capacity roadmap + system impact), `job-description-builder` (spec approved roles), `delegation-planner` (cheaper alternative to hiring), `culture-diagnostic` and `hr-process-coverage-audit` (readiness to absorb hires).

## Guardrails
- Never commit to a hire or spend — prepare and route for approval.
- Never recommend a hire that breaches the runway floor; downgrade or defer instead.
- Never touch a specific person's employment status/comp; that always goes to founder + HR/legal.
- Flag every assumed comp/cost/demand figure with `assumption: true` and reduced confidence; do not present estimates as facts.
- Treat individual team data as `restricted` sensitivity; do not expose comp externally.
- Prefer reversible capacity when the underlying need is uncertain.

## Example
**Founder input:** "We want to grow revenue from $1.2M to $2M next year. I'm buried in fulfillment and can't do sales. Cash is $180k, burn $60k/mo."

**Reasoning:** Runway = 180/60 = 3 months — already below the 6-month floor, so an FTE cannot be added blindly. Goal implies both a volume gap (fulfillment, where the founder is stuck) and a capability gap (sales, which nobody owns). Delegation check: an existing ops person at 70% utilization could absorb part of fulfillment if moved to Level C authority — cheapest lever. Sales is the revenue lever; a fully-loaded cost of ~$78k (base $60k × 1.3) would add $6.5k/mo burn, dropping runway further, so it is revenue-gated.

**Output (abridged):**
- Gap 1 (fulfillment, volume): close by delegating to existing ops hire at Level C → hand to `delegation-planner`. Cost ~$0.
- Gap 2 (sales, capability): hire 1 sales rep, FTE, fully-loaded $78k, payback ~7 months at target close rate — but **revenue-gated**: trigger = reach $130k/mo revenue OR raise cash to restore ≥6-month runway. Priority rank 1 once gated trigger fires.
- Deferred: a second fulfillment FTE — demand not yet durable; revisit at $1.6M run-rate.
- Financial impact: adding the rep drops runway below floor today → **do not hire yet**; gate on revenue.

**Executed vs. approval:** Drafted the sales `open_role` (status proposed) and the delegation hand-off, wrote a decision record, and assembled the approval request. The hire itself and the delegation change were **held for founder approval**; the runway warning was surfaced to founder + recommended accountant review.

## Provenance
SYNTH — assembled from the org-as-system model (F6), the founder-capacity/"doing too much" diagnostic (DG2), the I-Need/I-Have/Gaps capacity roadmap (W6), and the delegate-vs-do rule (R5) in `05-people-org.md`, combined with standard workforce-planning practice (fully-loaded cost, runway-gated hiring, cheapest-sufficient-lever sequencing) added to make it executable. Costing is validated by the CFO agent per the cross-impact rule in `AGENT_REGISTRY.md`.
