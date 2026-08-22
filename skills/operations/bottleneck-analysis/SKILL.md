---
name: bottleneck-analysis
domain: operations
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [operations, offerings, metrics, strategy, finance, team]
writes: [operations, metrics, risks, decisions]
related_skills: [process-mapping, operational-audit, process-optimization, automation-triage, technology-evaluation]
owned_by_agents: [operations-agent]
---

# Skill: Bottleneck Analysis

## Purpose
Find the single step that caps how much the business can produce or deliver — its throughput constraint — quantify that step's capacity ceiling, identify where it strains most under load, and recommend the specific relief action, so the founder fixes the one thing that actually limits growth instead of optimizing steps that don't matter.

## When to Use
- "Delivery is too slow", "we can't take on more clients", "orders pile up", "we're maxed out".
- After `operational-audit` names a primary scaling constraint that needs quantifying.
- Before a growth push, a big new contract, or a seasonal spike — to know the ceiling first.
- When adding capacity/hiring/buying equipment and the founder needs to know *where* the money actually relieves the constraint.

## When NOT to Use
- You don't yet have the process broken into steps → run `process-mapping` first.
- The whole business needs a scan, not one flow → `operational-audit`.
- The constraint is known and the ask is "cut the waste / redesign it" → `process-optimization`.
- The relief is clearly "buy a tool" and needs vendor due diligence → `technology-evaluation`.

## Required Context
- `operations.processes` — steps, cycle_time, capacity, bottleneck_flag per step.
- `operations.capacity` — resources, available vs used, utilization, constraint_flag.
- `offerings.capacity_constraint` — what limits how much can be sold/delivered.
- `metrics` — demand/volume trend, throughput history.
- `strategy.growth_plan` — the target volume the constraint must eventually support.

## Inputs
```yaml
input:
  process: object|string                # a process map (preferred) or process name to pull from memory
  step_capacities:                      # per step, whatever is known
    - step: string
      capacity_per_period: number|null  # max units the step can handle per unit time
      time_per_unit: number|null        # processing time per unit
      resource: string                  # person/machine/tool that does it
      resource_count: number            # how many of that resource
      utilization_pct: number|null
  demand_per_period: number             # current customer demand (units/time)
  demand_trend: string                  # direction/magnitude (e.g. "+40% YoY", "3x in Q4")
  available_time_per_period: number     # working time available per period
  target_demand: number                 # optional; from growth plan
  period_unit: string                   # e.g. "week", "day", "month"
```

## Missing Information Protocol
1. Prefer a `process-mapping` output; if only a name is given, pull the map from `operations.processes`.
2. If step capacities are missing, estimate from `time_per_unit × resource_count` and available time, and mark the result directional (`confidence: low`) until measured.
3. If demand/trend is unknown, ask the founder for current volume and direction — ONE batched question — because the constraint under load can't be found without it.
4. Never assume a step's capacity or resource count; where unknown, list it as the highest-value thing to measure next.
5. Analysis proceeds on estimates, clearly labeled; recommendations that spend money are held until the constraint is confirmed with real numbers.

## Diagnostic Questions
- Which single step, if it stopped, halts everything downstream? (the constraint)
- What is each step's capacity per period, and which is lowest? (the slowest step sets the ceiling)
- Where does work sit waiting — what queue grows fastest? (WIP piling up in front of a step points at it)
- Does the strained step change when volume rises? (constraint under load — the audit's key probe)
- Is the constraint a person, a machine, a tool, the physical layout, or a hand-off?
- What is the takt time (pace required to meet demand) vs. the constraint's cycle time?
- How far below target demand is the constraint's ceiling?
- Is the constraint truly capacity, or is it caused by an upstream defect/rework loop feeding it bad work?

## Analysis Framework
Constraint-theory logic applied to the mapped process:
1. **Establish demand and takt.** Takt time = available time ÷ demand. This is the pace every step must sustain to meet demand.
2. **Rate each step's capacity.** For each step compute capacity per period (from time_per_unit, resource_count, available_time) or use measured throughput.
3. **Find the slowest step = the bottleneck.** Overall process capacity ≤ bottleneck capacity. Confirm with the queue signal: WIP accumulates *in front of* the true constraint.
4. **Compute the ceiling and the gap.** Bottleneck capacity is the process ceiling; gap = demand (or target demand) − ceiling.
5. **Test under load.** Recompute with demand_trend / target_demand: does the binding constraint change as volume rises? Name the *next* constraint that appears after the first is relieved.
6. **Classify the strain point.** Is the constraint labor, equipment, tool/software, layout/space, or a hand-off? Is it real capacity or induced by upstream rework?
7. **Select relief.** Match the relief action to the constraint type (see Decision Rules), then re-check where the constraint moves to.

## Calculations
- **Takt time** = available production time per period ÷ customer demand per period. (Required pace.)
- **Step capacity** = (available time × resource_count) ÷ time_per_unit, per period.
- **Bottleneck / constraint capacity** = min(step capacities) = the process throughput ceiling.
- **Capacity gap** = demand − bottleneck capacity (and target_demand − bottleneck capacity for the growth ceiling).
- **Capacity utilization** = actual output ÷ max possible output × 100%. Healthy 70–85%; >95% = no slack/fragile (bottleneck signal); <40% = idle/waste.
- **Throughput (Little's Law)** = WIP ÷ cycle time; equivalently WIP = throughput × cycle time (a growing WIP queue in front of a step localizes the constraint).
- **Cycle time** = total elapsed start→output per unit; the bottleneck dominates it.
- **Relief impact** = new bottleneck capacity after the proposed change (recompute min across steps) − current ceiling.
- **Automation ROI** (if relief is a tool) = (annual manual cost saved − annual tool cost) ÷ annual tool cost.
- Threshold read: if bottleneck utilization > 95% AND capacity gap > 0, the process is at/over its ceiling — growth is blocked until relieved.

## Decision Rules
- IF one step's capacity is the minimum across all steps THEN it is the bottleneck; do not optimize any non-constraint step for throughput (it won't raise output).
- IF WIP/queue grows fastest in front of a step THEN confirm that step as the constraint even if nominal capacities look close.
- IF demand > bottleneck capacity THEN the process is at its ceiling; prioritize relieving that step before accepting more volume.
- IF the binding constraint changes as volume rises THEN plan relief for both the current and the next constraint (sequence the investments).
- IF the constraint is a person AND the step is documented THEN relieve by delegating/adding a person or off-loading their non-constraint work (route to People Agent / delegation).
- IF the constraint is a machine/equipment/layout THEN relieve via capacity investment (equipment, arrangement, space) — founder approval to spend.
- IF the constraint is a repetitive rule-based step THEN relieve via automation → `automation-triage` / `technology-evaluation`.
- IF the constraint is a hand-off/queue THEN relieve by removing the hand-off or re-sequencing (route to `process-optimization`) before spending money.
- IF the bottleneck is fed bad work (upstream defects cause rework) THEN fix the upstream defect first — the constraint is quality, not capacity.
- IF capacities are only estimated THEN recommend measuring the top-two candidate steps before any spend.

## Procedure
1. Load or ingest the process map and demand data.
2. Compute takt time and each step's capacity.
3. Identify the minimum-capacity step; corroborate with the queue/WIP and utilization signals.
4. Compute the ceiling, current gap, and target-demand gap.
5. Run the under-load test; name the next constraint that would appear.
6. Classify the constraint type and whether it's true-capacity or rework-induced.
7. Select and size the relief action(s); recompute the ceiling after each to show where the constraint moves.
8. Produce output; write bottleneck_flag and capacity findings to memory; register a scaling risk if gap > 0; route relief to the downstream skill.

## Output
```yaml
output:
  process: string
  takt_time: number                     # required pace to meet demand
  step_capacities:
    - step: string
      capacity_per_period: number
      utilization_pct: number|null
      is_bottleneck: boolean
      confidence: enum(low, medium, high)
  bottleneck:
    step: string
    capacity_ceiling: number            # process throughput ceiling
    constraint_type: enum(labor, equipment, tool, layout, handoff, upstream_quality)
    strain_signal: string               # e.g. "WIP queue growing in front of build step"
  gaps:
    current_gap: number                 # demand - ceiling
    target_gap: number                  # target_demand - ceiling
    at_or_over_ceiling: boolean
  under_load:
    binding_constraint_now: string
    next_constraint_after_relief: string|null
  relief_options:
    - action: string
      constraint_addressed: string
      new_ceiling_estimate: number
      cost_or_effort: string
      reversibility: enum(reversible, recoverable, irreversible)
      routes_to: string
      requires_approval: boolean
  recommended_relief: string
  measure_next: list[string]            # steps to instrument before spending
  open_questions: list[string]
```

## Recommendations
Rank relief options by **throughput gained per dollar/effort, then reversibility.** Prefer, in order: (1) fix upstream quality feeding the constraint (often free, high impact); (2) off-load non-constraint work from the constrained resource; (3) re-sequence/remove hand-offs; (4) automate the constrained step if rule-based; (5) add people/equipment/space (capacity spend, founder approval). Always show where the constraint *moves to* after the recommended relief — the goal is to elevate the constraint knowingly, not to be surprised by the next one.

## Execution Opportunities
- Set `bottleneck_flag` and capacity numbers on the process in `operations` memory (L2, reversible).
- Register a scaling risk in `risks` when target_gap > 0 (L1 draft).
- Create draft tasks for the recommended relief and for measurement (L1).
- Draft a capacity dashboard tracking bottleneck utilization vs. takt (L1 draft).
- No auto-spend, no vendor commitment, no headcount action.

## Human Approval Requirements
- Any relief that spends money (equipment, tools, space) or commits a vendor → founder approval (route tool spend to `technology-evaluation`).
- Any relief that changes headcount or reallocates a specific person's work → founder approval + People Agent.
- Accepting or declining new customer volume based on the ceiling is a founder decision; the skill only supplies the number.

## Escalation Conditions
- Demand already exceeds ceiling with no cheap relief → escalate to founder: risk of missed commitments / churn.
- Relief requires capital beyond a set threshold → founder + recommend finance/accountant review of ROI and cash impact.
- Constraint is a single key person (key-person risk) → founder + People Agent (continuity risk).
- Inputs are all estimates and a large spend hinges on them → surface uncertainty; recommend measurement before acting.

## KPIs
- Constraint accuracy: did relieving the named step actually raise output? (throughput before vs. after).
- Ceiling accuracy: predicted vs. realized capacity ceiling.
- Gap closure: reduction in capacity gap after relief.
- Move-prediction accuracy: did the "next constraint" appear where predicted?
- Utilization normalization: constrained resource utilization returning to the 70–85% healthy band.

## Monitoring
Track bottleneck utilization vs. takt, WIP/queue length in front of the constraint, throughput, and on-time delivery. Re-run after each relief action because the constraint moves; watch for the predicted next constraint emerging.

## Follow-Up
- Re-run after any relief action (the constraint relocates), after a demand step-change, and each quarter as part of the scaling plan.
- Feed the moved constraint back into the loop until the ceiling comfortably exceeds target demand.

## Related Skills
- `process-mapping` — supplies the step breakdown this skill needs.
- `operational-audit` — nominates the primary scaling constraint.
- `process-optimization` — removes hand-offs/waste as a no-spend relief.
- `automation-triage` / `technology-evaluation` — relief via tooling.

## Guardrails
- Execution ceiling L1; no money moved, no vendor committed, no person reassigned by this skill.
- Do not optimize non-constraint steps for throughput — it wastes effort and money without raising output.
- Clearly label estimate-based ceilings low-confidence; require measurement before large spend.
- Distinguish true capacity limits from rework-induced ones — don't buy capacity to process defects.
- Flag key-person constraints as continuity risks, not just throughput problems.

## Example
**Founder input:** custom cabinetry shop. Steps + capacity/week: quoting (10 jobs), material ordering (12), build (4 jobs — 1 shop, ~10 hrs/job over a 40-hr week), install (6 — 3 installers). demand = 6 jobs/week, demand_trend "+40% YoY", available_time = 40 hrs, target_demand = 8 jobs/week.

**Skill reasoning:** Takt = 40 hrs ÷ 6 = 6.7 hrs/job required pace. Step capacities/week: quote 10, material 12, build 4, install 6. Minimum = **build at 4 jobs/week** → capacity ceiling = 4. Demand 6 > 4 → current_gap = 2 (at/over ceiling; WIP piling up before build confirms it). Constraint type = equipment/labor at a single shop station. Under load at target 8: target_gap = 4; if build is relieved to 8, next constraint becomes **install at 6**. Build cycle time (10 hrs) > takt (6.7 hrs) — build cannot keep pace.

**Relief options:** (a) add a second build station / builder → new ceiling ~8 (capital + hire, irreversible-ish, founder approval); (b) off-load finishing/sanding sub-tasks from the builder to reduce build time per job toward takt (low cost, route to `process-optimization`); (c) check whether rework from bad measurements inflates build time (upstream quality — likely free). Recommended: confirm build time is real (not rework) → relieve build → then plan install capacity for target=8. `measure_next`: build hours/job and install hours/job.

**Executed vs. approval:** Set bottleneck_flag on "build", registered a scaling risk (gap>0), drafted a capacity dashboard and measurement tasks (auto, L1). Buying a second station and hiring a builder were flagged `requires_approval: true` with ROI routed to finance.

## Provenance
SOURCE — derived from the operations knowledge base: the bottleneck/constraint logic (the slowest step sets the ceiling; overall capacity ≤ bottleneck capacity), the "constraint under load / what strains most when sales increase" audit probe, points-of-failure (queues/backlogs/hand-offs) diagnostics, and the physical-layout/capacity-lever guidance. Formulas (takt, capacity, Little's Law, utilization, ROI) and thresholds are SYNTHESIZED industry standards, flagged as such. De-branded per repository rules.
