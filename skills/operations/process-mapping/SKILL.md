---
name: process-mapping
domain: operations
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [operations, offerings, team, customers, metrics, strategy]
writes: [operations, metrics, decisions]
related_skills: [operational-audit, bottleneck-analysis, process-optimization, automation-triage, sop-writer]
owned_by_agents: [operations-agent]
---

# Skill: Process Mapping

## Purpose
Turn a fuzzy, in-someone's-head process into an explicit, linked map of sub-processes — each with its concrete actions, standards, scripts, data, automations, and hand-offs — then overlay value/failure diagnostics and attach candidate metrics, so the process can be understood, improved, delegated, and measured.

## When to Use
- The founder wants to "document how X works," "map out our delivery process," or "figure out why this keeps going wrong."
- A process was flagged as key or constrained by `operational-audit` and needs deep decomposition.
- Before writing an SOP (mapping is the raw material), before automating, or before delegating a process.
- When a process is about to scale and its steps/interrelationships must be made visible first.

## When NOT to Use
- You need the whole-business scan, not one process → `operational-audit`.
- The map already exists and you only need the throughput constraint → `bottleneck-analysis`.
- The map exists and you want to cut waste/redesign → `process-optimization`.
- You need a polished, quality-controlled operating document to hand to staff → `sop-writer` (which consumes this map).

## Required Context
- `operations.processes` — any existing partial map, cycle_time, capacity, defect_rate, sop_ref.
- `offerings` — the output this process produces and its capacity_constraint.
- `team.org` — who performs each step (for hand-off and ownership capture).
- `customers.personas` — to judge which steps create customer-perceived value.
- `strategy.growth_plan` — so candidate metrics align with where the business is going.

## Inputs
```yaml
input:
  process_name: string                  # the process to map
  required_output: string               # what this process must produce (the end state)
  trigger: string                       # what starts the process
  walkthrough: string|list[string]      # founder/operator narration of how it works today, step by step
  known_problems: list[string]          # optional: where it breaks, complaints, delays
  customer_facing_steps: list[string]   # optional: which steps a customer sees/experiences
  step_timings: map[step -> duration]   # optional: measured or estimated time per step
  existing_tools: list[string]          # optional: tools/automations already used in the process
```

## Missing Information Protocol
1. Pull any existing partial map and timings from `operations.processes`.
2. If the walkthrough is thin, ask the operator to narrate the process start-to-finish once ("what happens first, then what?"), plus the exit condition — ONE batched request.
3. Do the first-pass map from whatever is available, then present it and ask "what's missing or out of order?" (the source method explicitly expects the first pass to miss steps).
4. Never invent steps, standards, scripts, or automations that weren't described. Mark inferred nodes `inferred: true, confidence: low`.
5. If step timings are unknown, still map the sequence; flag that metrics are directional until measured.

## Diagnostic Questions
- What is the required output, and what triggers the process?
- What is the ordered sequence of sub-processes from trigger to output?
- For each step: what exact actions are performed? what standard defines "done well"? is there a script (customer-facing language)? what data is captured? what automation fires? what is guaranteed/committed? what hands off to the next step?
- Where does work sit waiting (backlogs, queues, inventories between steps)?
- Which steps are non-value-added — a customer wouldn't pay for them?
- Where are the common points of failure (bottleneck, hand-off, hotspot)? Is there a recovery process when a step fails? Could a fail-safe make the failure impossible?
- Which steps are customer-facing / create direct visible value?
- How will the effectiveness of this process be measured?

## Analysis Framework
The 8-step process-mapping method:
1. **Select the process** (given, or pulled from the audit as customer-/cost-/competitiveness-critical).
2. **Identify start (trigger) and end (required output).**
3. **Decompose into ordered sub-processes** — the steps from input to required output.
4. **Capture Details per sub-process** — actions, standards, scripts, data captured, automations triggered, guarantees, hand-offs.
5. **Link steps in sequence**; continue across linked "sheets"/sections for long processes.
6. **Iterate** — do multiple passes; the first will miss steps, interrelationships, and complexity.
7. **Overlay good-map diagnostics** — highlight redundant/non-value-added steps; identify points of failure (backlogs, queues, bottlenecks, inventories, hand-offs, hotspots); establish recovery processes; identify fail-safe (poka-yoke) opportunities.
8. **Attach metrics** — define how the process's effectiveness will be measured.

Notation is deliberately lightweight: named nodes in sequence, each with a Details bullet list, chained trigger → … → output. Not formal BPMN; readability over symbol precision.

## Calculations
Applied when step timings/volumes exist (definitions with default thresholds):
- **Cycle time** = total elapsed time from trigger to required-output completion, per unit.
- **Process (value-added) time** = sum of time in value-added steps only.
- **Process cycle efficiency (PCE)** = value-added time ÷ cycle time. Healthy >25% / warning 10–25% / critical <10%.
- **Number of hand-offs** = count of ownership/role transfers (proxy for delay + error risk); minimize.
- **Throughput** = units of output per unit time.
- **Little's Law** = WIP = throughput × cycle time (i.e. throughput = WIP ÷ cycle time).
- **Defect rate** = defective units ÷ total units × 100% (healthy <2% / warning 2–5% / critical >5%).
- **First-pass yield** = units completed with no rework ÷ units started (healthy >95%).
- **On-time delivery** = orders met by promise date ÷ total (healthy ≥95%).
- **Wait/queue time** = cycle time − process time (the waste target).

## Decision Rules
- IF a step is non-value-added / redundant (customer wouldn't pay for it) THEN tag it eliminate/reduce and route to `process-optimization`.
- IF a step is a recurring point of failure (backlog/queue/bottleneck/hand-off/hotspot) THEN attach a recovery process AND propose a fail-safe to prevent recurrence.
- IF one step's throughput caps the whole map THEN tag it the bottleneck and route to `bottleneck-analysis`.
- IF a step is repetitive, rule-based, high-volume, low-judgment THEN tag it an automation candidate → `automation-triage`.
- IF PCE < 10% THEN the process is mostly waiting/waste — prioritize wait-time removal.
- IF a customer-facing step has no script/standard THEN flag a consistency risk (codify in `sop-writer`).
- IF hand-off count is high THEN flag each hand-off as delay+error risk and test whether any can be removed by merging steps.
- IF the process is undocumented and about to be delegated/scaled THEN route the finished map to `sop-writer`.

## Procedure
1. Confirm process_name, trigger, and required_output.
2. Decompose the walkthrough into an ordered list of sub-processes.
3. For each sub-process, populate the Details fields (actions, standard, script, data, automation, guarantee, hand-off).
4. Present the first-pass map; ask "what's missing / out of order?"; iterate until stable.
5. Overlay diagnostics: tag each step value-added vs non-value-added; mark points of failure; note where recovery exists vs. is missing; list fail-safe opportunities.
6. Compute metrics where timings/volumes exist; otherwise propose the metric set to start measuring.
7. Compile improvement opportunities (from tags) and candidate metrics.
8. Write the map to `operations.processes`; produce output; route flagged items downstream.

## Output
```yaml
output:
  process_name: string
  trigger: string
  required_output: string
  steps:
    - seq: integer
      sub_process: string
      details:
        actions: list[string]
        standard: string|null           # quality/service standard for "done well"
        script: string|null             # exact customer-facing language, if any
        data_captured: list[string]
        automation: list[string]        # automations triggered at this step
        guarantee: string|null          # commitment made at this step
        hand_off_to: string|null        # next owner/step
      value_tag: enum(value_added, non_value_added, business_required)
      failure_points: list[string]      # backlog/queue/bottleneck/handoff/hotspot
      recovery_process: string|null
      fail_safe_opportunity: string|null
      customer_facing: boolean
      timing: string|null
      inferred: boolean
  diagnostics:
    non_value_added_steps: list[string]
    bottleneck_candidate: string|null
    handoff_count: integer
    missing_recovery: list[string]
    fail_safe_opportunities: list[string]
  metrics:
    computed: map[metric -> value]       # where data existed
    candidate_metric_set: list[object]   # {metric, definition, formula, healthy/warning/critical}
  improvement_opportunities:
    - description: string
      type: enum(eliminate, automate, fail_safe, add_standard, reduce_handoff, add_recovery)
      routes_to: string
  open_questions: list[string]
```

## Recommendations
Improvement opportunities are ordered by customer-value impact and reversibility: (1) fail-safes that prevent customer-visible failures; (2) elimination of non-value-added steps; (3) hand-off reductions; (4) automations of repetitive steps; (5) adding missing standards/scripts and recovery processes. Each opportunity names the downstream skill that acts on it. Present the map first, opportunities second — the founder should recognize their own process before being told how to change it.

## Execution Opportunities
- Write/update the process record in `operations.processes` (L2, reversible).
- Create the candidate metric set as a draft dashboard (L1 draft).
- Create draft tasks for each improvement opportunity (L1).
- Draft an SOP skeleton from the map for `sop-writer` (L1 draft).
- No auto-execution of anything that changes the live process, touches customers, or commits money.

## Human Approval Requirements
- Any change to how a customer-facing step actually runs (new script, new guarantee, altered timing commitment) is a proposal held for founder approval.
- Adding/removing an automation that touches customers or external systems requires founder approval.
- Committing a vendor/tool implied by an automation is founder-approval only (route to `technology-evaluation`).

## Escalation Conditions
- A step involves a regulated/compliance activity → flag for legal/compliance review before proposing changes.
- A guarantee/commitment implies contractual liability → attorney.
- The map reveals a critical process with no recovery and high customer exposure → escalate to founder as a risk.
- Operator narrations conflict on how the process actually runs → surface the conflict; do not pick one silently.

## KPIs
- Map completeness: % of steps the operator confirms as accurate on review (target ≥95% after ≤2 iterations).
- Diagnostic yield: number of actionable improvement opportunities surfaced.
- Downstream usage: map feeds a successful SOP / optimization / automation.
- Metric adoption: candidate metrics actually tracked afterward.

## Monitoring
After mapping, watch the candidate metrics once instrumented (cycle time, PCE, hand-off count, defect/first-pass-yield). Re-open the map if reality diverges from it, or after any step change.

## Follow-Up
- Re-map when the process changes materially, a new tool is adopted, volume steps up, or an incident reveals an unmapped step.
- Feed the map into `sop-writer` (for delegation/scaling) and revisit during quarterly process review.

## Related Skills
- `operational-audit` — selects which processes to map.
- `bottleneck-analysis` — quantifies the bottleneck candidate the map flags.
- `process-optimization` — acts on non-value-added tags and redesign opportunities.
- `automation-triage` — routes automation-candidate steps.
- `sop-writer` — turns the finished map into a monitorable operating document.

## Guardrails
- Execution ceiling L1; the live process is never altered by this skill directly.
- Never fabricate steps, standards, scripts, or automations — mark inferred nodes low-confidence.
- Preserve exact customer-facing scripts/guarantees as stated; changing them is a founder decision.
- Do not expose individual employee performance data; reference roles for hand-offs.
- Treat the first pass as incomplete by design — always iterate before finalizing.

## Example
**Founder input:** process_name = "New client onboarding" (a bookkeeping firm); required_output = "client fully set up and first month reconciled"; trigger = "signed engagement letter"; walkthrough = "we email them a welcome, ask for bank logins and last year's returns, set them up in our software, wait for docs, then a bookkeeper starts the first reconciliation." known_problems = "clients take forever to send docs; sometimes we start setup twice."

**Skill reasoning (abridged):** Decomposed to 7 sub-processes: welcome email → request access & docs → client uploads docs → create client in software → verify docs complete → assign bookkeeper → first reconciliation. Overlay: "request access & docs" → "client uploads" is a **queue/backlog point of failure** (the "clients take forever" delay). "Create client in software" done before docs verified causes the **duplicate-setup** rework (a fail-safe: don't create the client record until a checklist of required docs is confirmed → poka-yoke). "Welcome email" is a manual repetitive step → automation candidate. Metrics: cycle time (engagement → first recon done), PCE (mostly waiting on client = low PCE), first-pass yield (duplicate setups hurt it), on-time onboarding rate.

**Output (excerpt):** bottleneck_candidate = "client document upload (waiting)"; non_value_added_steps = ["duplicate client setup rework"]; fail_safe_opportunities = ["gate software setup behind a required-docs checklist", "automated document-request reminders to remove the wait"]; candidate metrics = cycle time, PCE, first-pass yield, on-time onboarding %. Improvement opportunities routed: reminder automation → `automation-triage`; setup gate → `process-optimization`; the whole map → `sop-writer`.

**Executed vs. approval:** Wrote the process map to memory and created draft tasks + a draft metric set (auto, L1). Any change to the client-facing welcome/reminder emails was flagged for founder approval.

## Provenance
SOURCE — derived from the operations knowledge base: the process-map definition (sub-process + Details nodes), the 8-step mapping method, the "what makes a good process map" diagnostics (non-value-added, points of failure, recovery, fail-safe/poka-yoke), and the worked customer-intake example (structure only, brand-neutral). Formulas/thresholds are SYNTHESIZED industry standards, flagged as such. De-branded per repository rules.
