---
name: organizational-design
domain: people
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [team.people, team.org, team.culture, company, goals, operations, metrics, founders]
writes: [team.org, decisions, goals]
related_skills: [hiring-plan-builder, founder-capacity-diagnostic, delegation-planner, hr-process-coverage-audit, culture-diagnostic, onboarding-builder]
owned_by_agents: [people-agent]
---

# Skill: Organizational Design

## Purpose
Audit the business as a system (inputs → org → results, bound by culture) and turn the company's vision into a capacity roadmap: what the org NEEDS, what it HAS, where the gaps are, and a sequenced plan to close them. Surfaces mis-seated people, missing processes, and structural constraints before they cap growth.

## When to Use
- Scaling, reorg, or planning the next stage of the company.
- Founder asks: "Is my team set up right?", "Who should we hire next and why?", "What's missing to hit the vision?", "Is everyone in the right seat?"
- After `founder-capacity-diagnostic` or `hiring-plan-builder` reveals systemic (not single-task) capacity issues.
- Periodic org review (People Agent monthly loop).

## When NOT to Use
- To construct a single delegation → `delegation-planner`.
- To size/cost a specific hire → `hiring-plan-builder` (this skill defines the roles it prioritizes).
- To audit only HR procedures → `hr-process-coverage-audit` (this skill calls it as a sub-step).
- To assess culture health specifically → `culture-diagnostic` (called as a sub-step).
- Any specific-person status/comp/performance decision → founder + HR/legal.

## Required Context
- `company.vision`/`mission`/`values` and `stage`.
- `goals` — the targets the org must be built to hit.
- `team.people` (roles, capabilities, responsibilities, authority levels, capacity), `team.org` (structure, spans of control, open roles).
- `team.culture` — stated values and observed signals.
- `metrics` — results/outcome satisfaction inputs (profitability, growth, productivity, turnover, learning, founder quality of life).
- HR process inventory (from `hr-process-coverage-audit`).

## Inputs
```yaml
input:
  vision: str                        # where the company is going, required
  goals: [str]
  current_results:                   # Org Audit Part I outcomes
    profitability: enum(highly_satisfied, satisfied, dissatisfied)
    growth: enum(highly_satisfied, satisfied, dissatisfied)
    productivity_efficiency: enum(highly_satisfied, satisfied, dissatisfied)
    employee_commitment: enum(highly_satisfied, satisfied, dissatisfied)
    turnover: enum(highly_satisfied, satisfied, dissatisfied)
    team_learning: enum(highly_satisfied, satisfied, dissatisfied)
    founder_learning: enum(highly_satisfied, satisfied, dissatisfied)
    founder_quality_of_life: enum(highly_satisfied, satisfied, dissatisfied)
  key_people:                        # Org Audit Part II (2-3 key employees)
    - person_id: str
      role: str
      fit_with_current_job: int      # 1-5
      development_potential: int     # 1-5
      working_style: str
      values: [str]
  org_structure:
    reports: { manager_id: [report_id] }
    spans_of_control: { manager_id: int }
  critical_tasks: [str]              # the tasks the org must reliably perform
  hr_process_inventory: [str]        # from hr-process-coverage-audit
  culture_observations: [str]        # from culture-diagnostic
```

## Missing Information Protocol
1. Pull results metrics, people data, structure, and process inventory from memory before asking.
2. Call `hr-process-coverage-audit` and `culture-diagnostic` for their inputs rather than re-collecting.
3. If key-people fit/potential ratings are missing, ask the founder to rate the 2–3 key employees on fit (1–5) and potential (1–5).
4. **Never assume** a person's fit/potential without founder input, and never propose moving a specific person without flagging it for founder + HR/legal.

## Diagnostic Questions
- Treating the business as a system (F6): are the *inputs* (founder, strategy, environment), the *org* (critical tasks + people via processes), and the *outputs* (results) aligned — and where does the system leak?
- Which outcomes are we dissatisfied with (Part I), and what in the org system causes each?
- Are the right people in the right seats (Part II): fit (1–5) and development potential (1–5) per key person? Who is mis-seated or a development bet?
- Which critical tasks have no clear owner, or an owner without the competence/authority to run them?
- Are spans of control healthy, or is a manager overloaded / a layer missing?
- Which formal HR processes exist vs. are missing (DG5) — process gaps that cap the system?
- To hit the vision, what do we NEED (people, roles, processes/systems), what do we HAVE, what fits, and what are the gaps?

## Analysis Framework
Combines the Organizational Audit (W5, Parts I–III), the org-as-system model (F6), right-people-right-seats (DG3), the HR-process maturity diagnostic (DG5), and the Organizational Development Plan (W6).

1. **System map (F6):** lay out inputs → org (critical tasks + people + processes) → outputs; identify where results break down.
2. **Results audit (Part I):** rate the 8 outcomes; for each dissatisfied outcome, hypothesize the org-system cause (people, process, structure, or culture).
3. **Right-people-right-seats (Part II / DG3):** score key people on fit and potential; classify: strong-fit/high-potential (grow & retain), strong-fit/low-potential (stabilize), low-fit/high-potential (re-seat/develop), low-fit/low-potential (address — founder + HR/legal).
4. **Critical-task ownership:** map each critical task to an owner and authority level; flag orphaned or under-authorized tasks (feeds `delegation-planner`).
5. **Structure & spans:** check spans of control and layers; flag overload/missing layers.
6. **Process & culture maturity:** fold in `hr-process-coverage-audit` gaps (DG5) and `culture-diagnostic` signals.
7. **Capacity roadmap (W6):** build the I-Need / I-Have / Fits / Gaps / Plan / Timetable / Challenges table from vision + audit; each people-gap routes to `hiring-plan-builder` or `delegation-planner`, each process-gap to `hr-process-coverage-audit`.

## Calculations
- **Span of control** = direct reports per manager (flag < 3 as possibly over-layered, > 8 as possibly overloaded — heuristic, stage-dependent).
- **Right-seat quadrant** from fit (1–5) × potential (1–5): fit ≥ 4 = good seat; potential ≥ 4 = growth bet; both low = intervention needed.
- **Delegation depth** = share of tasks at Level C/D vs. A/B (from `team.people` authority levels).
- **HR-process coverage** = processes_present ÷ standard_process_set (from DG5 list).
- **Results-satisfaction score** = count of outcomes rated dissatisfied (each is a system-improvement target).
- No single composite; the roadmap prioritizes gaps by impact on the vision × urgency.

## Decision Rules
- IF an outcome (Part I) is "dissatisfied" THEN trace it to a specific org-system cause (people/process/structure/culture) and add a gap to the roadmap.
- IF a key person is low-fit/high-potential THEN recommend re-seating/development (route the seat change to founder + HR/legal).
- IF a key person is low-fit/low-potential THEN flag for founder + HR/legal — this is an employee-specific decision, never auto-acted.
- IF a critical task has no owner or an under-authorized owner THEN route to `delegation-planner` (or add a role to the roadmap).
- IF a span of control is unhealthy THEN recommend a structure change (add a layer / rebalance) — as a proposal, founder-approved.
- IF a formal HR process is missing (DG5) THEN add it to the roadmap and route to `hr-process-coverage-audit` (flag legal-sensitive ones — termination/discipline/protected-class — for HR/legal, R11).
- IF a people-gap is genuine and durable THEN route to `hiring-plan-builder`; IF closable by delegation THEN route to `delegation-planner`.
- IF any recommendation moves, restructures, or affects a specific person's status/comp THEN founder approval + HR/legal review is mandatory.

## Procedure
1. Load vision, goals, results metrics, people, structure, process inventory, and culture observations.
2. Draw the system map (F6) and run the results audit (Part I) with cause hypotheses.
3. Score key people on fit/potential (DG3); classify seats.
4. Map critical-task ownership and authority; flag orphans/under-authorization.
5. Check spans of control and layers.
6. Fold in HR-process gaps (`hr-process-coverage-audit`) and culture signals (`culture-diagnostic`).
7. Build the capacity roadmap (I-Need/I-Have/Fits/Gaps/Plan/Timetable/Challenges).
8. Route each gap to the right skill (hiring/delegation/process) and sequence with dependencies.
9. Write `team.org` proposals and a `decisions` record; present the audit + roadmap for founder approval.

## Output
```yaml
output:
  system_map:
    inputs: str
    org_transformer: str            # critical tasks + people + processes
    outputs: str
    leak_points: [str]
  results_audit:
    - outcome: str
      rating: enum(highly_satisfied, satisfied, dissatisfied)
      hypothesized_cause: str
      cause_type: enum(people, process, structure, culture)
  right_seats:
    - person_ref: str
      fit: int
      potential: int
      quadrant: enum(grow_and_retain, stabilize, reseat_develop, address)
      action: str                    # seat changes flagged for founder + HR/legal
  critical_task_ownership:
    - task: str
      owner: str                     # "" if orphaned
      authority_level: enum(A_none, B_minimal, C_medium, D_complete, none)
      flag: str                      # orphaned / under-authorized / ok
  structure_findings:
    spans_of_control: { manager: int }
    issues: [str]
  process_gaps: [str]                # from hr-process-coverage-audit
  culture_signals: [str]            # from culture-diagnostic
  capacity_roadmap:
    - i_need: str                    # role / process / system
      i_have: str
      fits: bool
      gap: str
      plan: str
      route_to_skill: str           # hiring-plan-builder / delegation-planner / hr-process-coverage-audit
      timetable: str
      challenges: str
      priority_rank: int
  employee_specific_flags: [str]     # anything requiring founder + HR/legal
  next_skills: [str]
```

## Recommendations
Prioritize gaps by their leverage on the vision and on the dissatisfied outcomes, then sequence by dependency (owners before managers, processes before scale). Fix orphaned critical tasks and unhealthy spans early — they silently cap everything. Route people-gaps to the cheapest sufficient lever (delegate before hire). Every seat change or structural move affecting a named person is a proposal for the founder + HR/legal, never an executed action.

## Execution Opportunities
- Produce the org audit + capacity roadmap (reversible, LOW) — L1 prepare.
- Draft `team.org` structure proposals and `open_roles` (reversible, LOW) — staged.
- Route gaps to downstream skills as prepared hand-offs (reversible, LOW).
- Write a `decisions` record (reversible, LOW).
- NOT executed: reorgs, seat changes, hires, or any specific-person action.

## Human Approval Requirements
- **Any structural change, seat change, hire, or role redefinition affecting a specific person ALWAYS requires founder approval AND HR/legal review** (employment actions per AUTONOMY_AND_APPROVAL_MODEL §4). This skill prepares proposals (L1) only.
- Building or changing standing HR processes (discipline, termination, non-discrimination) requires founder + HR/legal.
- Any move that changes compensation requires founder + comp/legal.

## Escalation Conditions
- A low-fit/low-potential person or any performance-based seat change → HR professional / attorney; founder decides. (R11)
- Protected-class, termination, or disciplinary dimensions in any restructuring → HR/legal, do not proceed.
- Structural change with financial impact (new layer, senior hire) → founder + accountant (cost via `hiring-plan-builder`).
- Culture signals indicating systemic bias or engagement collapse → `culture-diagnostic` + founder.

## KPIs
- Results-satisfaction improvement across the 8 outcomes.
- Right-seat ratio (share of key people with fit ≥ 4).
- Critical-task ownership coverage (orphaned tasks → 0); delegation depth (C/D share) rising.
- Span-of-control health; HR-process coverage %.
- Roadmap execution rate and time-to-close per gap; turnover trend.

## Monitoring
Track whether closed gaps stay closed, whether re-seated people improve in fit, span-of-control drift as headcount grows, and results-outcome trends. Re-audit when any outcome degrades or the org grows past a stage threshold.

## Follow-Up
Run at each stage transition, quarterly org review, after major growth-goal changes, or when results outcomes degrade. Continuously feeds `hiring-plan-builder`, `delegation-planner`, and `hr-process-coverage-audit`.

## Related Skills
`hiring-plan-builder` (costs/sequences people-gaps), `delegation-planner` (fixes ownership/authority gaps), `founder-capacity-diagnostic` (founder-as-node in the system), `hr-process-coverage-audit` (process gaps), `culture-diagnostic` (culture as the system's medium), `onboarding-builder` (integrating new roles).

## Guardrails
- The org is a system — every proposed change is evaluated for ripple effects before recommending (F6, DG1).
- No specific-person seat/status/comp/performance action is ever executed here — founder + HR/legal only. (R11)
- Prefer delegation over hiring where competence exists (cheapest sufficient lever).
- Route legal-sensitive process gaps (discipline/termination/protected-class) to HR/legal (R11).
- Individual people data is `restricted`; do not expose fit/potential/comp externally.

## Example
**Input:** Vision to double revenue in 18 months. Part I: dissatisfied with productivity and founder quality of life; satisfied elsewhere. Key people: Priya (fit 5, potential 5), Sam (fit 2, potential 4). Critical task "customer onboarding" has no clear owner; founder still runs it. Span: founder has 6 direct reports. HR-process audit: no documented performance-evaluation or onboarding process.

**Reasoning:** System leak = founder is the transformer for onboarding (productivity + QoL both trace to this). Right seats: Priya = grow_and_retain (candidate to own onboarding at Level C/D); Sam = low-fit/high-potential → reseat/develop (flag to founder + HR/legal). Orphaned critical task "customer onboarding" → assign to Priya via `delegation-planner`. Process gaps: build onboarding process (`onboarding-builder`) and performance-evaluation process (route to `hr-process-coverage-audit`, legal-reviewed). Span of 6 is fine now but will strain at 2× — plan a team-lead layer.

**Output (abridged):** results_audit ties productivity + QoL to founder-owned onboarding; right_seats with Priya grow_and_retain and Sam reseat_develop (flagged); critical_task_ownership flags onboarding orphaned → route delegation-planner; capacity_roadmap rows: [own onboarding via delegation, build onboarding process, build performance-eval process, plan team-lead layer for scale]; employee_specific_flags: ["Sam re-seat — founder + HR"].

**Executed vs. approval:** Produced the audit, roadmap, and staged proposals (L1). The Sam re-seat, the delegation, the new layer, and the performance-evaluation process were all **held for founder approval**, with the performance/re-seat items routed to HR/legal.

## Provenance
SOURCE — derived from the Organizational Audit Parts I–III (W5), the org-as-system model (F6), the right-people-right-seats diagnostic (DG3), the HR-process maturity diagnostic (DG5), the Organizational Development Plan I-Need/I-Have/Gaps roadmap (W6), and the separation-gating rule (R11) in `05-people-org.md`.
