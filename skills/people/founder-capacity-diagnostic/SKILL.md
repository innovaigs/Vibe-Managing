---
name: founder-capacity-diagnostic
domain: people
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [founders, team.people, team.org, goals, operations, metrics]
writes: [decisions, goals]
related_skills: [delegation-planner, hiring-plan-builder, organizational-design, onboarding-builder]
owned_by_agents: [people-agent]
---

# Skill: Founder Capacity Diagnostic

## Purpose
Detect when the founder has become the bottleneck of their own business and produce a concrete offload plan: which tasks to delegate (and at what authority level), which to automate, which to outsource, and which justify a hire — so the founder buys back discretionary time and the business stops stalling on one person.

## When to Use
- Founder says: "I'm doing too much", "everything runs through me", "I have no time", "I'm the bottleneck", "I can't take a vacation."
- Decisions are visibly stalling waiting on the founder; growth goals are blocked on founder capacity.
- Before `hiring-plan-builder` (to confirm the gap is real and not solvable by delegation) and during org reviews.

## When NOT to Use
- To actually construct a delegation for a specific task/person → `delegation-planner` (this skill feeds it).
- To decide headcount/affordability → `hiring-plan-builder` (this skill feeds it).
- To redesign the whole org → `organizational-design`.
- To assess a non-founder employee's overload → capacity analysis in `organizational-design` / operations, not this skill.

## Required Context
- `founders.time_allocation` — where the founder's hours currently go (by function/task).
- `founders.strengths` / `development_areas` and `goals_personal` (incl. quality of life).
- `team.people` — who exists, their capabilities, and current authority levels (potential receivers).
- `goals` — growth goals and whether they require capacity the founder doesn't have.
- `operations` — which critical tasks only the founder can do (single points of failure).

## Inputs
```yaml
input:
  founder_task_inventory:
    - task: str
      hours_per_week: number
      only_founder_can_do: bool
      strategic: bool                # advances the vision vs. operational upkeep
      enjoys: bool                   # energizing vs. draining
      recurring: bool
  decision_flow:
    decisions_stalled_on_founder: [str]
    avg_decision_wait_days: number|null
  founder_state:
    weekly_hours: number
    discretionary_hours: number      # unstructured/strategic time available
    quality_of_life_rating: int      # 1-5, from goals_personal
  growth_goals: [str]
  available_receivers:               # existing people who could take work
    - person_id: str
      capabilities: [str]
      spare_capacity_pct: number
      authority_level: enum(A_none, B_minimal, C_medium, D_complete)
```

## Missing Information Protocol
1. Pull `time_allocation` and team capabilities from memory before asking.
2. If the founder's task inventory is thin, ask **one batched question**: "List your recurring tasks with rough hours/week, mark which only you can do, and which drain vs. energize you."
3. Do not proceed to recommend a *hire* without checking cheaper levers first (delegation/automation/outsourcing).
4. **Never assume** a task truly requires the founder (challenge every `only_founder_can_do`) or that a receiver is competent without evidence.

## Diagnostic Questions
(DG2 — the "founder doing too much" diagnostic)
- Are decisions stalled waiting on the founder? Is the founder the only person who can do critical tasks?
- Which tasks is the founder doing that a Level C/D delegate could own?
- Does the founder lack discretionary time — the payoff Level D is supposed to buy back?
- Do the growth goals require capacity the founder doesn't currently have?
- For each founder task: is it strategic or operational upkeep? Energizing or draining? Only-founder or delegable? Recurring (automatable) or one-off?
- Is any "only I can do this" belief actually a trust/documentation gap rather than a true constraint?

## Analysis Framework
Applies the founder-capacity diagnostic (DG2), the delegate-vs-do rule (R5), and the cheapest-sufficient-lever ordering (delegate → automate → outsource → hire).

1. **Task triage grid** — plot each founder task on two axes: *strategic vs. operational* and *only-founder vs. delegable*. Operational + delegable tasks are the primary offload candidates; strategic + only-founder tasks are the ones to protect.
2. **Single-point-of-failure scan** — flag tasks nobody else can do; these are business-continuity risks even if the founder isn't overloaded.
3. **Drain scan** — flag draining, low-value tasks the founder keeps; these erode quality of life and are prime to offload.
4. **Lever selection per offload candidate** (cheapest sufficient first):
   - **Delegate** to a competent existing person (→ `delegation-planner`, pick the level via competence).
   - **Automate** if recurring and rule-based (→ integrations/workflows).
   - **Outsource** if specialized and intermittent (→ contractor).
   - **Hire** only if durable volume/capability gap remains (→ `hiring-plan-builder`).
5. **Bottleneck quantification** — estimate hours reclaimable and decision-latency reduction.
6. **Capacity-vs-goals check** — does reclaimed capacity cover what the growth goals demand, or is a hire still required?
7. **Protect strategic time** — recommend a floor of discretionary/strategic hours to defend.

## Calculations
- **Reclaimable hours/week** = Σ hours of offload-candidate tasks (delegable/automatable/outsourceable).
- **Founder utilization** = weekly_hours ÷ sustainable_hours (default sustainable ≈ 50). >1.0 = over capacity.
- **Discretionary-time gap** = target_discretionary_hours − current discretionary_hours (target default ≥ 20% of the week for a founder in scaling stage).
- **Single-point-of-failure count** = number of tasks with `only_founder_can_do = true` and no documented backup.
- **Bottleneck severity** = f(decision_wait_days, SPOF_count, discretionary_gap, quality_of_life_rating). High severity if decisions wait >3 days OR SPOF_count high OR QoL ≤ 2.
- **Offload priority per task** = (hours × drain × non-strategic) ÷ receiver_readiness_cost.

## Decision Rules
- IF a task is operational AND delegable AND a competent receiver exists THEN recommend delegation at the highest justified level (C/D) → `delegation-planner`; do NOT recommend a hire for it. (R5)
- IF a task is recurring and rule-based THEN recommend automation before delegation-to-a-person.
- IF a task is specialized and intermittent THEN recommend outsourcing (contractor) over an FTE.
- IF a durable volume/capability gap remains after cheaper levers THEN recommend a hire → `hiring-plan-builder`.
- IF a task is `only_founder_can_do` with no backup THEN flag a single-point-of-failure/continuity risk and recommend documenting + cross-training (even if not overloaded).
- IF the founder's discretionary time is below the floor THEN prioritize offloads that restore strategic time, and protect it explicitly.
- IF an "only I can do this" belief lacks a real constraint THEN challenge it as a trust/documentation gap and route to `delegation-planner` (and note delegation-readiness).
- IF any offload touches a specific person's status/comp THEN founder + HR/legal.

## Procedure
1. Load founder time allocation, growth goals, and available receivers.
2. Build the task triage grid; run the SPOF and drain scans.
3. For each offload candidate, select the cheapest sufficient lever (delegate → automate → outsource → hire).
4. Quantify reclaimable hours, discretionary gap, SPOF count, and bottleneck severity.
5. Check whether reclaimed capacity meets the growth goals; if not, note the residual hire need.
6. Prioritize offloads and set a discretionary-time floor to protect.
7. Produce the offload plan; write a `decisions` record; route delegations to `delegation-planner`, automations to workflows, hires to `hiring-plan-builder`.

## Output
```yaml
output:
  bottleneck_severity: enum(low, moderate, high, critical)
  summary: str
  metrics:
    reclaimable_hours_per_week: number
    founder_utilization: number
    discretionary_time_gap_hours: number
    single_point_of_failure_count: int
    avg_decision_wait_days: number|null
  task_triage:
    - task: str
      quadrant: enum(strategic_only_founder, strategic_delegable, operational_only_founder, operational_delegable)
      hours_per_week: number
      drain: bool
      recommended_lever: enum(protect, delegate, automate, outsource, hire, document_and_cross_train)
      target_person: str             # if delegate
      target_authority_level: enum(A_none, B_minimal, C_medium, D_complete)  # if delegate
      next_skill: str                # delegation-planner / hiring-plan-builder / workflow
  continuity_risks: [str]            # single points of failure to backfill/document
  protected_strategic_time_hours: number
  residual_hire_need: str            # "" or the gap cheaper levers can't close
  next_skills: [str]
```

## Recommendations
Attack drains and operational-delegable tasks first — they buy back the most time for the least risk. Always try delegation/automation/outsourcing before recommending a hire (cheaper, reversible). Protect a floor of strategic time explicitly; the whole point of Level-D delegation is to free the founder's discretion, not just to redistribute busywork. Treat single points of failure as risks even when the founder isn't yet overloaded.

## Execution Opportunities
- Produce the offload plan and task triage (reversible, LOW) — L1 prepare.
- Create internal tasks/reminders for documenting SPOF tasks and cross-training (reversible, LOW).
- Hand delegations to `delegation-planner`, automations to workflow config drafts, hires to `hiring-plan-builder` (all prepared, not committed).
- Write a `decisions` record (reversible, LOW).
- NOT executed: any hire, any authority change, any status/comp change.

## Human Approval Requirements
- **Any resulting hire requires founder approval** (via `hiring-plan-builder`) — employment + spend action.
- **Any delegation/authority change requires founder approval** (via `delegation-planner`).
- Any offload that changes a specific person's role/status/comp ALWAYS requires founder approval AND HR/legal review.
- Automation that touches financial or external-facing actions must respect the control-plane always-approve list.

## Escalation Conditions
- Founder quality-of-life rating ≤ 2 or burnout signals → surface to founder directly; prioritize offload.
- Residual gap requires a hire that strains runway → founder + accountant (via `hiring-plan-builder`).
- An offload implies moving/backfilling a specific person → founder + HR professional.
- Critical single point of failure with no backup → founder (business-continuity risk) + risk agent.

## KPIs
- Founder discretionary/strategic hours reclaimed (primary).
- Reduction in decision wait time and stalled-decision count.
- Single-point-of-failure count trending to zero (documented/cross-trained).
- Delegation depth (Level C/D share) rising; founder utilization moving toward sustainable.
- Growth-goal progress unblocked by capacity.

## Monitoring
After the plan runs, track actual hours reclaimed vs. projected, whether delegated tasks stick (or bounce back to the founder), decision latency, and founder quality-of-life. A task that bounces back signals a delegation-readiness or competence gap → re-plan.

## Follow-Up
Re-run monthly (People Agent's capacity loop), whenever the founder reports overload, before any hiring decision, and after major growth-goal changes. Feed persistent capacity gaps into `hiring-plan-builder` and `organizational-design`.

## Related Skills
`delegation-planner` (executes each delegation with the right level), `hiring-plan-builder` (when a durable gap remains), `organizational-design` (systemic capacity roadmap), `onboarding-builder` (bring a new hire up so delegation can follow).

## Guardrails
- Exhaust cheaper, reversible levers (delegate/automate/outsource) before recommending a hire (R5).
- Challenge every "only I can do this" — most are trust/documentation gaps, not true constraints.
- Never execute a hire, authority change, or status/comp change — prepare and route for founder (and HR/legal where a specific person is affected).
- Treat individual team and founder data as confidential/restricted.
- Flag continuity risks even absent overload.

## Example
**Founder input:** "I work 65 hours a week, approve every invoice and every social post, do all fulfillment QA, and I haven't had a strategic day in a month. Priya (ops, Level B, 40% spare) is sharp."

**Reasoning:** Utilization 65/50 = 1.3 (over capacity); discretionary gap large; QoL implied low. Triage: invoice approval = operational/delegable, recurring, rule-based → automate approval under a threshold + delegate exceptions to Priya; social post approval = operational/delegable → delegate to Priya at Level C (Requests) with brand guardrails (method_matters → specify method); fulfillment QA = operational, currently only-founder but delegable → delegate to Priya at Level B first (emerging competence), document the checklist to remove the SPOF; strategic planning = strategic/only-founder → protect. Reclaimable ≈ 15 hrs/week. Cheaper levers cover most of it; no hire needed yet, residual = none.

**Output (abridged):** bottleneck_severity high; reclaimable ~15 hrs/wk; triage with levers (automate invoices under threshold, delegate social@C, delegate QA@B + document, protect 8 strategic hrs); continuity_risks: ["fulfillment QA had no backup — now documented"]; residual_hire_need: ""; next_skills: [delegation-planner ×2, workflow-automation draft].

**Executed vs. approval:** Produced the offload plan, staged the delegations and the invoice-automation draft, and created cross-training tasks (L1). Delegations, the authority changes, and the payment-approval automation were **held for founder approval** (the automation also respects the money-movement always-approve rule).

## Provenance
SOURCE — derived from the "founder doing too much"/capacity diagnostic (DG2), the delegate-vs-do rule (R5), the Levels of Authority payoff (Level-D buys back founder time), and the org-as-system capacity logic in `05-people-org.md`, with the cheapest-sufficient-lever ordering (delegate→automate→outsource→hire) added to make the offload plan executable.
