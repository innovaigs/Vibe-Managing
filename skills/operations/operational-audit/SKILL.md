---
name: operational-audit
domain: operations
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [company, offerings, operations, finance, team, metrics, strategy, market]
writes: [operations, risks, metrics, decisions]
related_skills: [process-mapping, bottleneck-analysis, automation-triage, technology-evaluation, sop-writer, process-optimization]
owned_by_agents: [operations-agent]
---

# Skill: Operational Audit

## Purpose
Run a structured multi-dimension sweep of a business's operations to answer "why can't we scale / where do we leak time, cost, and quality?" — surfacing the top operational constraints, documentation gaps, non-value-added activities, and automation/outsourcing candidates so the founder knows exactly where to invest next.

## When to Use
- The founder asks a scaling or friction question: "why can't we scale?", "everything feels chaotic when we get busy", "where are we wasting money in operations?", "what should I fix first?"
- Onboarding a new business into Vibe Managing (baseline the operating system).
- Before a growth push, funding round, hiring wave, or new-market entry — to know what will break under load.
- Quarterly operations review (the Operations Agent's scaling-plan loop).
- After a major incident (missed deliveries, quality complaints, capacity crunch) to find root operational gaps.

## When NOT to Use
- A single named process needs documenting or improving → use `process-mapping` then `process-optimization`.
- Delivery is slow and the founder already knows the culprit process → go straight to `bottleneck-analysis`.
- The question is purely "which tool should I buy?" → use `technology-evaluation`.
- The question is financial performance (margins, runway, pricing), not operational flow → hand to the CFO/finance skills.
- People/role/span-of-control redesign is the real need → hand to the People Agent (this skill only cross-references org data).

## Required Context
Before running, load from Business Memory:
- `company` — business model, stage, revenue model, locations, industry.
- `offerings` — products/services and each one's `capacity_constraint`.
- `operations` — existing `processes`, `sops`, `tools`, `vendors`, `capacity`.
- `finance.position` — to relate strain to volume/revenue trend.
- `team.org` — spans of control, who owns which process (Dimension C cross-reference).
- `metrics` — any existing operational time series.
- `strategy.growth_plan` — the 1–3 year target, so constraints are ranked against where the business is going.

## Inputs
```yaml
input:
  business_description: string          # what the business does, in the founder's words
  offerings: list[string]               # products/services delivered
  sales_trend: string|object            # direction + rough magnitude of volume/revenue change (e.g. "+30% YoY", "flat", "seasonal 3x in Q4")
  current_tools: list[string]           # software/equipment in use today (function-level ok)
  org_data:                             # optional; pulled from team.org if present
    headcount: integer
    key_roles: list[string]
    process_owners: map[process -> owner]   # who owns what today
  known_pain_points: list[string]       # optional founder-volunteered symptoms
  growth_plan: string                   # optional; 1-3 year objective if not in memory
  focus_dimensions: list[enum]          # optional filter: [operations_overview, finance_ops, organizational, market_customers, metrics]; default = all five
```

## Missing Information Protocol
1. Pull each field from Business Memory first (`operations`, `offerings`, `team`, `finance`, `strategy`).
2. Compute what can be computed (e.g. process documentation coverage = documented ÷ key processes).
3. If required inputs are still missing, ask the founder ONE batched set of questions, organized by the five dimensions — never a drip of one-at-a-time questions.
4. Never assume: sales trend/volume direction, which processes are "key," who owns a process, whether an SOP exists, or a tool's true cost. If unknown, mark the finding `confidence: low` and list it as an open question rather than asserting it.
5. Analysis may always proceed on partial data; label gaps explicitly and lower the confidence of any dependent conclusion.

## Diagnostic Questions
Answered internally (or asked) across the five audit dimensions:

**A — Operations Overview**
- What processes deliver the product/service, and which are *key* (critical to customers, cost, or competitiveness) and why?
- Which part of operations feels the most strain when sales increase? (primary bottleneck signal — "constraint under load")
- Is there an operational manual / SOP for each key process? (codification gap)
- Is there a contingency/emergency plan for the critical processes? (resilience gap)
- Does the physical layout / equipment / people mix cap throughput?
- Have remote/virtual customer & supplier processes been developed and documented?

**B — Finance operations**
- How are sales and payments tracked? What is the billing and collection process? How are bills paid? How are financial reports produced? (manual, error-prone, or un-automated steps here are prime automation candidates)

**C — Organizational**
- Cross-reference org data: who owns each key process; is any critical process owner-dependent (only the founder can do it)?

**D — Market & Customers (value mapping)**
- What in operations is *really special* (core competency / competitive advantage)?
- Which parts give customers direct, visible value? Which give little/no value (outsource candidates)?
- Where is the business *under-investing* in a way that could create a dramatic advantage?

**E — Metrics**
- What numbers measure each process's health? How does the owner know things are on track? Is the data timely, detailed, and accurate — and where does it come from?

## Analysis Framework
Apply, in order:
1. **Operations System model (Input → Transformation → Output).** Frame the whole business as inputs (people, tech, capital, equipment, materials, information) → transformation processes → outputs (goods/services). Enumerate the transformation processes; this is the process inventory.
2. **Scope-of-operations sweep.** Ensure every applicable process domain has at least one identified process: production/delivery, supplier management, HR, finance ops, inventory, customer relations, information systems, scheduling, marketing & sales, order processing, shipping/receiving.
3. **Five-dimension audit (A–E above).** Collect a finding per bullet.
4. **Effectiveness → Efficiency → Competitiveness triad.** Score each key process: does it work at all (effective)? does it work with least waste (efficient)? does it efficiently produce what customers *value* (competitive)?
5. **Value test on the aggregate.** Flag activities that add cost/time without adding customer-perceived value (destroy-value) as elimination/outsourcing candidates.
6. **Process Lifecycle maturity rating.** Rate each key process on the ladder understood → rationalized → codified → monitored. Anything below "codified" is a scaling risk.
7. **Constraint-under-load synthesis.** Identify the process(es) that strain most as volume rises — the scaling constraint(s).
8. **Prioritize** (see Recommendations).

## Calculations
- **Process documentation coverage** = documented key processes ÷ total key processes × 100%. Threshold: 100% healthy / 60–99% warning / <60% critical.
- **Number of hand-offs** (per key process) = count of ownership/role transfers. Higher = more delay + error risk.
- **Owner-dependency count** = number of key processes only the founder/one person can run. Any >0 is a scaling risk.
- **Capacity utilization** (where data exists) = actual output ÷ max possible output × 100%. Two-sided: 70–85% healthy; >95% = fragile/no slack; <40% = waste.
- **Automation ROI** (for each candidate) = (annual manual cost saved − annual tool cost) ÷ annual tool cost. Positive and >~1.0 (payback <1 yr) is a strong candidate; pass to `technology-evaluation` for due diligence.
- Full formula catalogue (cycle time, PCE, throughput, Little's Law, takt, defect rate, first-pass yield, on-time delivery) is applied inside `process-mapping`/`bottleneck-analysis`; here they are only invoked where a process already has timing/quality data.

## Decision Rules
- IF a key process is undocumented (no operational manual) THEN flag it and route to `sop-writer` before any delegation or scaling attempt.
- IF a process is critical AND owner-dependent THEN flag as a scaling constraint: document it (→ `sop-writer`) then delegate (→ delegation planning).
- IF a specific part of operations feels the most strain when sales increase THEN mark it the PRIMARY scaling constraint and route to `bottleneck-analysis`.
- IF a step/activity is non-value-added (customer wouldn't pay for it) AND not a core competency THEN mark for elimination or outsourcing.
- IF an activity provides little/no customer-visible value AND is not core THEN evaluate outsource/buy over build/staff.
- IF the business is under-investing in an operation that could create a dramatic competitive advantage THEN flag it as a high-priority investment.
- IF a step is repetitive, rule-based, high-volume, low-judgment THEN mark as automation candidate → `automation-triage`/`technology-evaluation`.
- IF physical layout/equipment/people mix caps throughput THEN flag environment/capacity constraint.
- IF there is no contingency plan for a critical process THEN flag a resilience gap.
- IF process data is not timely/detailed/accurate THEN flag a measurement gap and lower confidence on all decisions derived from that data — fix measurement first.

## Procedure
1. Load context from memory; confirm the process inventory using the Input→Transformation→Output frame and the scope-of-operations checklist.
2. Determine which processes are *key* and record the criticality rationale for each.
3. Run each of the five dimensions (or the `focus_dimensions` subset), collecting one finding per diagnostic bullet.
4. Rate each key process on the maturity ladder and the effectiveness/efficiency/competitiveness triad.
5. Compute the metrics above where data exists; where it doesn't, record a measurement gap.
6. Classify each finding into: constraint, documentation gap, non-value-added/outsource candidate, automation candidate, under-investment, resilience gap, or measurement gap.
7. Score and rank findings (Recommendations).
8. Produce the output report; write findings to memory (`operations`, `risks`, `metrics`); create draft follow-on tasks (L1 — proposed, not executed).
9. Route each prioritized item to its downstream skill.

## Output
```yaml
output:
  process_inventory:
    - name: string
      domain: string                 # e.g. order_processing, delivery, finance_ops
      is_key: boolean
      criticality_rationale: string
      maturity: enum(understood, rationalized, codified, monitored)
      triad: {effective: bool, efficient: bool, competitive: bool}
      owner: string|null
      owner_dependent: boolean
  findings:
    - id: string
      dimension: enum(operations_overview, finance_ops, organizational, market_customers, metrics)
      type: enum(constraint, documentation_gap, non_value_added, outsource_candidate, automation_candidate, under_investment, resilience_gap, measurement_gap)
      description: string
      evidence: string
      impact: enum(low, medium, high)
      effort: enum(low, medium, high)
      confidence: enum(low, medium, high)
  primary_scaling_constraint: string    # the part that strains most under load
  documentation_coverage_pct: number
  owner_dependency_count: integer
  prioritized_actions:
    - rank: integer
      action: string
      rationale: string
      routes_to: string               # downstream skill
      requires_approval: boolean
  open_questions: list[string]
  recommended_dashboard_metrics: list[string]
```

## Recommendations
Rank findings by a weighted score: **impact (customer + cost + scaling) × reversibility, discounted by effort and cost.** Ordering heuristic:
1. Constraints that break under load (fix before growth) — highest.
2. Owner-dependent critical processes (document → delegate) — unlock founder time.
3. High-ROI, low-effort automations of repetitive rule-based steps.
4. Non-value-added activities to eliminate; non-core low-value activities to outsource.
5. Under-investment areas that could create a dramatic advantage (higher effort, staged).
6. Resilience and measurement gaps (enable everything else; often low effort).
Always present the top 3 "do next" items with expected outcome and the downstream skill to run.

## Execution Opportunities
- Create draft internal tasks for each prioritized action (L1 — reversible, low risk).
- Update the operations section of Business Memory with the process inventory and maturity ratings (L2, reversible).
- Draft a new operations dashboard with the recommended metrics (L1 draft).
- Register newly identified operational risks in the `risks` namespace (L1 draft).
- Auto-run: none that touch customers, money, or vendors.

## Human Approval Requirements
- Any recommendation that changes a customer-facing process, commits money, or engages/commits a vendor is prepared as a proposal only and held for founder approval (per AUTONOMY_AND_APPROVAL_MODEL §4).
- Purchasing any tool or committing to outsourcing requires founder approval — never auto-executed.
- Writing to `operations` memory beyond drafts, or registering a risk as active, is notified to the founder.

## Escalation Conditions
- Financial exposure / cash risk uncovered → founder + recommend accountant.
- A finding implies a contract, IP, or liability question (e.g. outsourcing a regulated function) → attorney.
- Employee-specific reallocation or role change implied → People Agent / HR.
- Process data is conflicting or low-confidence and a material decision hinges on it → surface uncertainty to founder; do not act.

## KPIs
- Coverage: % of applicable process domains audited (target 100%).
- Actionability: % of prioritized actions the founder accepts.
- Constraint-hit rate: did the identified primary constraint match what actually broke under load next quarter?
- Downstream conversion: % of routed items completed by the downstream skill.
- Documentation coverage trend after remediation.

## Monitoring
After the audit, watch: the primary scaling constraint's load metric, documentation coverage %, owner-dependency count, and any newly created risk. Re-check whether strain shifted to a new step after each fix.

## Follow-Up
- Re-run quarterly (Operations Agent scaling loop) and on trigger: a sales-volume step-change, a new offering, a major incident, or a growth-plan change.
- After each prioritized action completes, re-audit the affected dimension to confirm the constraint moved.

## Related Skills
- `process-mapping` — deep-map any process flagged key or constrained.
- `bottleneck-analysis` — quantify the primary scaling constraint.
- `sop-writer` — codify undocumented key processes.
- `automation-triage` / `technology-evaluation` — act on automation/tool candidates.
- `process-optimization` — eliminate/redesign non-value-added steps.

## Guardrails
- Analysis is always allowed; execution ceiling is L1 (drafts/proposals only).
- Never assume tool costs, owners, or volumes — mark low-confidence and ask.
- Never recommend outsourcing a core competency or a source of competitive advantage.
- Do not commit money, sign vendor agreements, or change customer-facing processes without founder approval.
- Fix measurement gaps before trusting decisions derived from unreliable process data.
- Respect data sensitivity: individual performance/comp data is restricted and must not appear in the output; reference roles, not people, for delegation findings.

## Example
**Founder input:** "We do custom cabinetry. Sales are up ~40% this year but everything falls apart when we're busy — orders get lost and installs slip. Tools: email, a shared spreadsheet, QuickBooks. Just me plus 3 installers and a part-time bookkeeper."

**Skill reasoning (abridged):**
- Process inventory (Input→Transf→Output): lead intake → quote → order confirmation → material ordering → build scheduling → build → install scheduling → install → invoicing → collection.
- Key processes: order confirmation (data loss point), build+install scheduling (strain under load), material ordering (lead-time dependency).
- Dimension A: no operational manual (documentation coverage 0/5 key = 0%, critical). Order confirmation lives in the founder's inbox → owner-dependent (owner-dependency count = 3: order confirmation, scheduling, quoting). Strain-under-load = scheduling. No contingency plan.
- Dimension B: billing manual in QuickBooks off a spreadsheet — re-keying = automation candidate (repetitive, rule-based).
- Dimension D: core competency = custom build quality (visible value). Spreadsheet order tracking = non-value-added admin, no advantage. Under-investment = no job/project tracking system.
- Dimension E: no process metrics; data lives in one spreadsheet (measurement gap, stale).

**Output (top of report):**
- `primary_scaling_constraint`: build & install scheduling.
- `documentation_coverage_pct`: 0.
- `owner_dependency_count`: 3.
- Prioritized actions: (1) run `bottleneck-analysis` on scheduling before taking more orders; (2) `sop-writer` for order-confirmation + scheduling, then delegate order intake off the founder's inbox; (3) `technology-evaluation` for a job/project-tracking tool to replace the spreadsheet and auto-flag material lead times; (4) automate invoice creation from confirmed orders.

**Executed vs. approval:** Created 4 draft tasks and a draft ops dashboard (auto, L1). Tool purchase, moving invoicing into a new system, and any change to how customers get order confirmations were flagged `requires_approval: true` and held for the founder.

## Provenance
SOURCE — derived from the operations knowledge base: the Operational Audit five-dimension questionnaire (Operations Overview / Finance / Organizational / Market & Customers / Metrics), the Operations System (Input–Transformation–Output) model, the Effectiveness/Efficiency/Competitiveness triad, the Scope-of-Operations checklist, and the Process Lifecycle maturity ladder. Formulas and thresholds are SYNTHESIZED industry standards flagged as such. De-branded per repository rules.
