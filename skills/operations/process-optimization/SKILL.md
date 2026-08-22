---
name: process-optimization
domain: operations
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [operations, offerings, customers, metrics, strategy, finance]
writes: [operations, metrics, decisions]
related_skills: [process-mapping, bottleneck-analysis, automation-triage, sop-writer, operational-audit, technology-evaluation]
owned_by_agents: [operations-agent]
---

# Skill: Process Optimization

## Purpose
Tag every step of a process as value-creating or value-destroying, eliminate or redesign the waste, and project how the process must evolve to support growth — so the business delivers "better, faster, cheaper" what customers actually value, and the process won't break as it scales.

## When to Use
- "This process is slow / has too many steps / is a mess", "how can we streamline this?", "we're wasting time here".
- After `process-mapping` produces a map with non-value-added tags to act on.
- After `bottleneck-analysis` where the cheapest relief is removing waste/hand-offs (no-spend relief) rather than adding capacity.
- When planning growth: projecting how a process must change over 1–3 years to support higher volume (scaling evolution).
- Before codifying an SOP — improve the process first so you don't document waste.

## When NOT to Use
- The process isn't mapped yet → `process-mapping` first.
- You need to find *which* step is the throughput ceiling → `bottleneck-analysis`.
- The improvement is specifically "should we automate/outsource/delegate this?" per step → `automation-triage`.
- You need the whole-business scan → `operational-audit`.
- The improved process is agreed and now needs documenting → `sop-writer`.

## Required Context
- `operations.processes` — the current map with steps, timings, defect_rate, hand-offs.
- `offerings` — the output and what customers pay for (defines value).
- `customers.personas` — value_drivers and decision_criteria (the arbiter of "value-added").
- `metrics` — cycle time, PCE, defect rate, throughput baselines.
- `strategy.growth_plan` — the 1–3 year volume/target the process must evolve to support.
- `finance` — cost of steps (labor/material) to size waste in dollars.

## Inputs
```yaml
input:
  process: object|string                # process map (preferred) or name to pull from memory
  current_metrics:                      # whatever is measured
    cycle_time: number|null
    value_added_time: number|null
    defect_rate: number|null
    handoff_count: number|null
    throughput: number|null
  step_costs: map[step -> cost]         # optional; labor/material cost per step
  customer_value_drivers: list[string]  # what the customer actually pays for / values
  growth_plan:
    target_volume: number|null
    horizon: string                     # e.g. "3 years"
  constraints: list[string]             # budget, headcount, compliance limits on what can change
```

## Missing Information Protocol
1. Prefer a `process-mapping` output with value tags; if only a name is given, pull the map from memory.
2. If customer value drivers are unknown, pull from `customers.personas`; if still unknown, ask the founder "what specifically would the customer pay more for / notice if it were gone?" — the value test needs this.
3. If step timings/costs are missing, work qualitatively (value vs. waste tags) and mark quantified savings as estimates until measured.
4. Never delete/redesign a step on assumption that it's non-value-added — confirm against the customer value driver and check for a hidden compliance/quality reason before recommending elimination.
5. For scaling projection, if the growth plan is absent, ask for the target volume and horizon — ONE batched ask.

## Diagnostic Questions
- For each step: does the customer perceive value in it — would they pay for it? (value-added vs non-value-added vs business-required)
- Where does work wait (queues, backlogs, inventories)? Wait time is pure waste.
- How many hand-offs are there — can any be removed by merging steps or changing ownership?
- Which steps are redundant or duplicated?
- Where do defects originate vs. get detected? (detection far downstream = expensive rework)
- Is anything missing? What could improve? How can the process be revised to create more value for the customer and/or lower cost?
- How must this process evolve over the next 1–3 years to support the growth plan, specifically? What is needed to make it happen?

## Analysis Framework
1. **Value test on every step** (Input→Transformation→Output model): tag each transformation `value_added` (customer perceives value), `business_required` (no customer value but legally/operationally necessary — e.g. compliance, safety), or `non_value_added` (waste — customer wouldn't pay, not required).
2. **Waste identification.** For non-value-added steps, classify the waste type: waiting/queue, over-processing, rework/defects, unnecessary hand-off, redundant step, unnecessary motion/transport, excess inventory/WIP.
3. **Effectiveness/Efficiency/Competitiveness check.** Ensure changes keep the process effective (still works) and efficient (less waste) while improving competitiveness (efficiently delivers customer-valued output).
4. **Eliminate → Reduce → Redesign → Automate ladder.** For each waste: eliminate if possible; if not, reduce/simplify; if it must stay, redesign (merge steps, remove hand-offs, move detection upstream, add fail-safe); if repetitive/rule-based, route to automation.
5. **Fail-safe & recovery.** Where defects/failures cause the waste, design poka-yoke to prevent them and a recovery process for when they occur.
6. **Scaling evolution projection.** For the growth horizon, project how each step behaves at target volume; identify which steps break, and specify what's needed (people, tools, redesign) to make the process support the growth plan. Produce the top 3 process changes required to drive growth.
7. **Quantify.** Compute before/after cycle time, PCE, hand-off count, defect rate, and dollar waste where data exists.

## Calculations
- **Process cycle efficiency (PCE)** = value-added time ÷ total cycle time. Target improvement toward >25% (healthy); <10% = mostly waste. The headline optimization metric.
- **Wait/queue time** = cycle time − value-added time (the elimination target).
- **Cycle time reduction** = old cycle time − projected new cycle time (and %).
- **Hand-off reduction** = old count − new count (each removed hand-off cuts a delay + error risk).
- **Defect/rework rate** = defects (or rework units) ÷ total; moving detection upstream lowers downstream rework cost.
- **First-pass yield** = clean units ÷ started (target >95%).
- **Dollar waste** = Σ(cost of non-value-added steps + rework cost + cost of wait-driven delays), where step_costs exist.
- **Throughput impact** = new throughput vs old (Little's Law: throughput = WIP ÷ cycle time — cutting cycle time raises throughput at equal WIP).
- **Automation ROI** (for steps routed to automate) = (annual manual cost saved − annual tool cost) ÷ annual tool cost.

## Decision Rules
- IF a step is non-value-added (customer wouldn't pay, not required) THEN eliminate it; if it can't be eliminated, reduce/minimize it; if still needed, automate it.
- IF a step is business_required (compliance/safety/quality) but no customer value THEN keep but streamline; never eliminate a compliance step to save time.
- IF wait/queue time dominates cycle time (low PCE) THEN prioritize removing the wait (pull work forward, remove the queue, add fail-safe reminders) before touching processing steps.
- IF hand-offs are numerous THEN merge steps / reassign ownership to cut hand-offs (each is delay + error risk).
- IF defects are detected far downstream from where they originate THEN move detection/prevention upstream and add a fail-safe (poka-yoke).
- IF a step is repetitive/rule-based/high-volume THEN route to `automation-triage` rather than optimizing the manual version.
- IF a change would relieve the throughput constraint THEN coordinate with `bottleneck-analysis` (optimize the constraint, not non-constraints).
- IF a redesign changes the customer's experience or a commitment THEN it is a proposal held for founder approval.
- IF projecting to target volume shows a step breaks THEN specify the required evolution (people/tool/redesign) and add it to the scaling roadmap.
- IF a step's value can't be confirmed THEN do not recommend elimination; flag for founder confirmation.

## Procedure
1. Load the mapped process and current metrics; confirm the customer value drivers.
2. Tag every step value_added / business_required / non_value_added; classify each waste.
3. Apply the eliminate→reduce→redesign→automate ladder to each non-value-added step; add fail-safes/recovery where failures drive waste.
4. Design the improved process flow; compute before/after metrics and dollar waste.
5. Run the scaling projection at target volume; identify breaking steps; specify required evolution; produce the top-3 growth-critical changes.
6. Compile prioritized recommendations (impact/effort/reversibility) with the downstream skill for each.
7. Produce output; write the improved-map proposal and scaling roadmap to memory (as proposals); create draft tasks; route automations to `automation-triage` and the final flow to `sop-writer`.

## Output
```yaml
output:
  process: string
  step_value_tags:
    - step: string
      tag: enum(value_added, business_required, non_value_added)
      waste_type: enum(waiting, over_processing, rework, handoff, redundancy, motion_transport, inventory_wip, none)
      disposition: enum(keep, eliminate, reduce, redesign, automate)
      rationale: string
  redesigned_flow: list[object]         # proposed step sequence after changes
  before_after:
    cycle_time: {before: number, after: number}
    pce: {before: number, after: number}
    handoff_count: {before: number, after: number}
    defect_rate: {before: number, after: number}
    dollar_waste_removed: number|null
  fail_safes_added: list[string]
  recovery_added: list[string]
  scaling_evolution:                    # 1-3 year projection
    horizon: string
    target_volume: number|null
    steps_that_break: list[string]
    required_changes: list[object]      # {change, what_is_needed, when}
    top_3_growth_changes: list[string]
  recommendations:
    - action: string
      impact: enum(low, medium, high)
      effort: enum(low, medium, high)
      reversibility: enum(reversible, recoverable, irreversible)
      routes_to: string
      requires_approval: boolean
  new_dashboard_metrics: list[string]
  open_questions: list[string]
```

## Recommendations
Prioritize by **customer-value gain + cost/time removed, weighted by reversibility, discounted by effort.** Order: (1) eliminate pure waste (free, reversible, immediate); (2) remove waits and hand-offs; (3) move quality upstream + add fail-safes (prevents costly rework); (4) automate repetitive steps (route out); (5) capacity/tool changes for scaling (higher effort, staged, approval). Always present the before/after metrics so the gain is quantified, and separate "do now" quick wins from the scaling roadmap.

## Execution Opportunities
- Write the redesigned-flow proposal and scaling roadmap to `operations` memory as proposals (L1).
- Create draft tasks for each quick-win change (L1).
- Draft the new dashboard metrics (L1 draft).
- Route automation-candidate steps to `automation-triage` and the finalized flow to `sop-writer` (L1 hand-off).
- No auto-execution of any live process change, customer-facing change, or spend.

## Human Approval Requirements
- Any change that affects the customer's experience or a commitment/guarantee → founder approval (per AUTONOMY_AND_APPROVAL_MODEL §4: process changes affecting customers).
- Eliminating a step that could have a compliance/quality/safety reason → confirm with founder + compliance before removal.
- Any change requiring spend (tools, equipment) or headcount → founder approval (route spend to `technology-evaluation`).
- Reassigning a specific person's work as part of a hand-off removal → founder approval + People Agent.

## Escalation Conditions
- A candidate-for-elimination step turns out to be compliance/safety/regulatory → legal/compliance before any removal.
- Scaling projection shows the process cannot support the growth plan without major capital → founder + finance.
- Removing a hand-off implies an employee role change → People Agent / HR.
- Customer value of a step is genuinely unknown/contested → surface to founder; do not eliminate on assumption.

## KPIs
- PCE improvement (value-added share of cycle time) — the headline.
- Cycle-time reduction and hand-off reduction.
- Defect/rework rate reduction and first-pass-yield increase.
- Dollar waste removed.
- Scaling readiness: does the process now support target volume without breaking?
- Adoption: % of recommended changes implemented and holding.

## Monitoring
After changes, watch PCE, cycle time, hand-off count, defect rate/first-pass yield, and throughput against baselines. Confirm removed waste didn't reappear and that no quality/compliance step was lost. Re-check the scaling roadmap as actual volume rises.

## Follow-Up
- Re-optimize after volume steps up, a new tool lands, or metrics regress.
- Update the scaling roadmap each quarter against the growth plan.
- Hand the improved, stable flow to `sop-writer` to codify, and route automations to `automation-triage`.

## Related Skills
- `process-mapping` — supplies the tagged map (upstream).
- `bottleneck-analysis` — ensures optimization targets the real constraint.
- `automation-triage` — acts on automate-disposition steps.
- `sop-writer` — codifies the improved process.
- `technology-evaluation` — evaluates tools the redesign requires.

## Guardrails
- Execution ceiling L1; no live process, customer-facing, or spend change is auto-executed.
- Never eliminate a step on assumption — confirm it's non-value-added against the customer value driver and rule out a compliance/quality reason.
- Don't optimize non-constraint steps for throughput; coordinate with `bottleneck-analysis`.
- Improve before you codify — don't hand waste to `sop-writer`.
- Keep the process effective (it must still work) and compliant while making it efficient.
- Label estimated savings as estimates until measured.

## Example
**Founder input:** e-commerce fulfillment process, 9 steps, cycle time ~48 hrs, customer values "fast, accurate delivery." Map shows: order received → manual re-key into shipping tool → wait for daily batch → pick → pack → **quality check at the very end** → print label → hand to carrier → send tracking email. Complaints: slow, occasional wrong items. current_metrics: cycle_time 48h, value_added_time ~4h (PCE ≈ 8%), handoff_count 4, defect_rate 4%.

**Skill reasoning:** Value tags — value_added: pick, pack, ship; non_value_added: manual re-key (over-processing/duplicate entry), wait-for-daily-batch (waiting — dominates the 48h), end-of-line QC catches errors after packing (rework, detection too far downstream). business_required: label print. Ladder: eliminate re-key by integrating order → shipping (automate, route out); eliminate the daily-batch wait by processing on receipt (removes ~bulk of cycle time); move the quality check upstream to the pick step + add a scan-verify fail-safe (poka-yoke) so wrong items can't be packed. Before/after: cycle time 48h → ~6h; PCE 8% → ~55%; hand-offs 4 → 2; defect rate 4% → target <1%. Scaling projection at 3x volume: manual pick becomes the next constraint → required change: pick-path optimization / added picker (route to `bottleneck-analysis`). Top-3 growth changes: order-to-ship integration, continuous (non-batch) processing, upstream scan-verify QC.

**Output (excerpt):** dollar_waste_removed estimated from re-key labor + rework; new_dashboard_metrics = [PCE, cycle time, first-pass yield, on-time delivery]; automation routed = ["order-to-shipping data entry"]; finalized flow routed to `sop-writer`.

**Executed vs. approval:** Wrote the redesigned-flow proposal + scaling roadmap to memory and created quick-win draft tasks (auto, L1). The order→shipping integration (tool spend) and the change to when tracking emails go to customers were flagged `requires_approval: true`.

## Provenance
SOURCE — derived from the operations knowledge base: the value-creation/value-destruction test on every transformation step, the Effectiveness/Efficiency/Competitiveness triad ("better, faster, cheaper"), the good-process-map diagnostics (redundant/non-value-added steps, points of failure, recovery, fail-safe/poka-yoke), the "how must this process evolve over 1–3 years to support growth + top-3 changes" scaling exercise, and the eliminate/minimize/automate rule for non-value-added steps. Formulas/thresholds (PCE, cycle time, ROI) are SYNTHESIZED industry standards, flagged as such. De-branded per repository rules.
