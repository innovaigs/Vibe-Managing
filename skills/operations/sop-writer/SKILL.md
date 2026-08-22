---
name: sop-writer
domain: operations
version: 0.1.0
autonomy_ceiling: L2
provenance: SOURCE
reads: [operations, offerings, team, customers, strategy, metrics]
writes: [operations, metrics, decisions]
related_skills: [process-mapping, process-optimization, automation-triage, operational-audit, bottleneck-analysis]
owned_by_agents: [operations-agent]
---

# Skill: SOP Writer

## Purpose
Convert tribal knowledge — a process that only lives in someone's head — into a clear, documented, learnable, and monitorable Standard Operating Procedure with explicit steps, quality standards, checkpoints, recovery steps, and metrics, so the process can be delegated, scaled, and measured instead of depending on one person.

## When to Use
- "Write this down", "document how we do X", "I need to hand this off but it's all in my head".
- A key process was flagged undocumented by `operational-audit` (documentation coverage gap) and must be codified before delegation or scaling.
- Before delegating an owner-dependent process to an employee.
- Before onboarding/training new staff on a recurring task.
- After `process-mapping` produces a stable map that now needs to become an operating document staff actually follow.

## When NOT to Use
- The process isn't understood yet / steps are unknown → run `process-mapping` first (mapping is the input to this skill).
- You want to *cut waste or redesign* the process, not document the current one → `process-optimization` (document the improved version afterward).
- You want to automate the steps rather than codify human execution → `automation-triage`.
- The "document" needed is a customer-facing spec or contract, not an internal operating procedure → route to the relevant domain (legal/marketing).

## Required Context
- `operations.processes` — the process map (steps, details, standards, hand-offs) this SOP codifies; and `operations.sops` for existing/related SOPs.
- `team.org` — the role that will own/perform the process (write to the role, not the person; comp/performance data is restricted and out of scope).
- `offerings` — the output and any quality/service standard the SOP must guarantee.
- `customers.personas` — for customer-facing standards/scripts and what "good" looks like to the customer.
- `strategy.growth_plan` — so the SOP is written to be scalable/monitorable, not just descriptive.

## Inputs
```yaml
input:
  process_name: string
  process_map: object|null              # from process-mapping (preferred); if null, ask for a walkthrough
  walkthrough: string|list[string]|null # operator narration, if no map
  purpose: string                       # why the process matters to the business/customer
  required_output: string               # the defined "done" state
  quality_standards: list[string]       # what "done well" means (from map or founder)
  scripts: list[string]                 # exact customer-facing language, if any
  owner_role: string                    # role that will own/perform it
  tools_used: list[string]              # systems/tools/equipment the steps rely on
  known_failure_points: list[string]    # where it breaks; feeds recovery + fail-safe steps
  compliance_notes: list[string]        # any regulatory/safety requirements
```

## Missing Information Protocol
1. Prefer a `process-mapping` output; if absent, request the map or a start-to-finish walkthrough — ONE batched ask.
2. Interview for the tacit parts explicitly: the standards, the "how do you know it's done right," the exceptions, and the recovery steps ("what do you do when it goes wrong?"). These are the tribal-knowledge pieces that make an SOP useful.
3. Never invent a quality standard, threshold, script, or compliance requirement. If unknown, insert a `[TO CONFIRM]` placeholder and list it as an open question — do not ship an SOP with fabricated standards.
4. If the process is not yet stable/agreed, flag that codifying an unstable process locks in waste; recommend `process-optimization` first.
5. Preserve exact customer-facing scripts and guarantees verbatim; do not paraphrase commitments.

## Diagnostic Questions
- Is this process actually understood and correct/necessary/effective, or should it be improved before it's codified? (don't cement waste)
- What triggers it, what is the required output, and how does the operator *know* it was done well?
- What is the exact ordered step list, with the concrete actions inside each step?
- What is the quality standard/checkpoint at each critical step?
- What scripts / exact language are used at customer-facing steps?
- What data is captured, in which tool, at which step?
- Where does it commonly fail, and what is the recovery step? Can a step be fail-safed so the error can't happen?
- Which steps need judgment/training vs. which are rote (informs training notes)?
- What metrics will show the SOP is being followed and working?

## Analysis Framework
Follows the Process Lifecycle ladder — the SOP takes a process from *understood* to *codified* and sets up *monitored*:
1. **Confirm understanding** — validate the map/walkthrough is complete and correct with the operator.
2. **Rationalize before codifying** — quick check: is each step correct, necessary, effective? Flag obvious waste to `process-optimization` rather than documenting it.
3. **Codify** — write the SOP in a standard structure (below) so it can be communicated clearly and learned readily.
4. **Embed quality control** — checkpoints, standards, recovery, and fail-safes at the right steps ("what makes a good process map" carried into the document).
5. **Instrument for monitoring** — attach the metrics that show the SOP is followed and effective.
6. **Prepare for delegation** — write to a role with clear ownership and success criteria.

**SOP document structure:**
- Title, process owner (role), purpose, scope, trigger, required output (definition of done).
- Prerequisites: access, tools, inputs needed before starting.
- Numbered steps: each with action(s), the standard for that step, the tool/where data goes, and any script.
- Quality checkpoints: explicit "verify X before proceeding" gates.
- Exceptions & recovery: what to do when a step fails.
- Fail-safes: design elements that prevent errors.
- Escalation: when to stop and ask a human, and whom.
- Metrics: how the process is measured; target values.
- Revision info: version, last reviewed, review cadence.

## Calculations
Primarily a documentation skill; it *specifies* the metrics the process will be monitored by (computed elsewhere once instrumented):
- **Process documentation coverage** contribution = this SOP moves one key process from undocumented → documented (raises coverage toward 100% target).
- **First-pass yield** = units completed with no rework ÷ units started (SOP target typically >95%).
- **Defect rate** = defects ÷ total (target <2%).
- **On-time delivery** = on-time ÷ total (target ≥95%).
- **Cycle time** and **cycle-time variance** — an SOP should reduce variance (consistency is the point).
- **SOP adherence rate** = executions following the SOP ÷ total executions (target ≥95% once trained).
Each metric is written into the SOP with a healthy/warning/critical band tuned to the business.

## Decision Rules
- IF the process is not yet understood/mapped THEN stop and route to `process-mapping` before writing.
- IF a step contains obvious non-value-added waste THEN flag to `process-optimization` and document the *improved* step, not the wasteful one.
- IF a step is repetitive/rule-based/high-volume THEN note it as an automation candidate (→ `automation-triage`) while still documenting the manual fallback.
- IF a step has a known failure point THEN the SOP MUST include a recovery step AND propose a fail-safe.
- IF a step involves regulatory/safety/compliance requirements THEN mark it mandatory, cite the requirement, and route the SOP for compliance/legal review before it goes live.
- IF a required standard/threshold is unknown THEN insert `[TO CONFIRM]` and list as open question — never guess.
- IF the SOP is for delegating an owner-dependent process THEN include explicit ownership, success metrics, and an escalation path so responsibility genuinely transfers.
- IF a customer-facing script exists THEN reproduce it verbatim and mark it non-negotiable.

## Procedure
1. Ingest the process map (or run the walkthrough interview).
2. Rationalize: quick correct/necessary/effective check; route obvious waste out to `process-optimization`.
3. Draft the SOP in the standard structure, writing to the owner role.
4. Embed quality checkpoints, recovery steps, fail-safes, and the escalation path at the right steps.
5. Insert metrics with target bands; mark unknown standards `[TO CONFIRM]`.
6. Add training notes (which steps need judgment/training).
7. Review draft with the operator/owner for accuracy; iterate.
8. Publish the SOP to `operations.sops`, link it to the process (`sop_ref`), and set the review cadence (L2 — reversible, notified). Create a training/delegation task and register the coverage improvement.

## Output
```yaml
output:
  sop:
    title: string
    process_name: string
    owner_role: string
    purpose: string
    scope: string
    trigger: string
    required_output: string             # definition of done
    prerequisites: list[string]
    steps:
      - number: integer
        action: string
        standard: string|null           # quality standard for this step ([TO CONFIRM] if unknown)
        tool: string|null               # where it's done / where data goes
        script: string|null             # verbatim customer-facing language
        is_checkpoint: boolean
        automation_candidate: boolean
    quality_checkpoints: list[string]
    exceptions_and_recovery: list[object]  # {failure, recovery_step}
    fail_safes: list[string]
    escalation: list[object]             # {condition, escalate_to}
    metrics: list[object]                # {name, formula, target, healthy/warning/critical}
    training_notes: list[string]
    version: string
    review_cadence: string
  coverage_delta: string                 # e.g. "3/5 -> 4/5 key processes documented"
  open_questions: list[string]           # every [TO CONFIRM]
  routed_out:
    to_optimization: list[string]        # waste flagged for redesign
    to_automation: list[string]          # steps flagged to automate
  requires_review: enum(none, compliance, legal, founder)
```

## Recommendations
Recommend the SOP be validated by the person who actually does the work before it's treated as authoritative, and that it launch paired with training and the adherence metric. Prioritize documenting: (1) owner-dependent critical processes (biggest delegation unlock); (2) processes with known failure points (SOP adds recovery/fail-safe); (3) high-variance processes (SOP adds consistency). Recommend a review cadence proportional to change rate (e.g. quarterly for stable, monthly for evolving).

## Execution Opportunities
- Publish the SOP to `operations.sops` and set `sop_ref` on the process (L2, reversible, founder notified).
- Create a draft training/delegation task for the owner role (L1).
- Register the documentation-coverage improvement in `metrics` (L2).
- Draft a delegation-conversation outline (for handing the process to a person) as input to the People Agent (L1 draft).
- Schedule the SOP review reminder (L2, reversible).
- Not auto-executed: making the SOP the enforced live procedure that changes customer experience, or delegating to a *specific* named person.

## Human Approval Requirements
- Making an SOP the official live procedure that changes how customers are handled → founder approval.
- Any SOP touching regulatory/safety/compliance → compliance/legal review before go-live (per AUTONOMY_AND_APPROVAL_MODEL §4).
- Assigning the SOP to a specific employee (delegation) → founder approval + People Agent (employee-specific action).
- Publishing beyond internal draft or overwriting an existing authoritative SOP → founder-notified; overwriting a record requires approval.

## Escalation Conditions
- Regulatory/safety/employment content in the process → legal/compliance/HR before publishing.
- Operator can't articulate the standard for a critical step → escalate to founder (the standard is a business decision, not a documentation guess).
- The process is unstable or contested (people disagree on how it's done) → surface to founder; recommend optimization/agreement first.
- Codifying would lock in a known bottleneck/waste → recommend `bottleneck-analysis`/`process-optimization` first.

## KPIs
- Documentation coverage: contribution toward 100% of key processes with an SOP.
- Adherence rate: ≥95% of executions follow the SOP after training.
- Outcome lift: first-pass yield ↑ / defect rate ↓ / cycle-time variance ↓ after adoption.
- Delegation success: process successfully run by someone other than the original owner.
- SOP freshness: % of SOPs reviewed on cadence (not stale).

## Monitoring
After publish, watch adherence rate, first-pass yield, defect rate, and cycle-time variance for the process. Watch for drift (reality diverging from the SOP) and stale SOPs past their review date; trigger a revision when the process changes or metrics degrade.

## Follow-Up
- Review on the set cadence; revise on any process change, tool change, new failure mode, or metric degradation.
- Once documented, pair with delegation (People Agent) and, where flagged, `automation-triage`.
- Feed adherence/outcome data back to `operational-audit` as coverage improves.

## Related Skills
- `process-mapping` — produces the map this SOP codifies (upstream).
- `process-optimization` — improve before you codify; document the improved version.
- `automation-triage` — automate the steps this SOP marks as candidates.
- `operational-audit` — sources the documentation-gap that triggers this skill.

## Guardrails
- Execution ceiling L2 (reversible publishing/notified writes); customer-facing enforcement and specific-person delegation stay founder-approved.
- Never fabricate standards, thresholds, scripts, or compliance requirements — use `[TO CONFIRM]`.
- Don't codify a broken/wasteful process; rationalize (or optimize) first.
- Reproduce customer-facing scripts/guarantees verbatim; changing a commitment is a founder decision.
- Write to roles, not named individuals; individual performance/comp data is restricted and excluded.
- Every SOP with a known failure point must ship with a recovery step and an escalation path.

## Example
**Founder input:** process_name = "Monthly client reporting" (a marketing agency); owner intends to hand it to a new account coordinator. purpose = "clients get their results on time, consistently formatted"; required_output = "approved report delivered by the 5th business day"; known_failure_points = ["data pulled from the wrong date range", "sent before the account manager reviews"]. No map yet, but a clear walkthrough given.

**Skill reasoning:** Rationalized the walkthrough into 6 steps: pull metrics (specify exact date range = fail-safe against the wrong-range error), populate template, write insights, **checkpoint: account-manager review (gate before send)**, incorporate edits, send to client (verbatim delivery script). Recovery: if data looks anomalous, flag AM before proceeding. Fail-safe: report template auto-locks the reporting period so the wrong range can't be selected. Metrics: on-time delivery %, first-pass yield (reports sent with no client-requested corrections), cycle-time variance. Training notes: insight-writing needs judgment/training; data pull is rote (automation candidate → routed out). Escalation: anomalous data or missed deadline → account manager. Standard for "good insight" was vague → `[TO CONFIRM]` open question to founder.

**Output (excerpt):** SOP with 6 steps, a mandatory AM-review checkpoint, two fail-safes, on-time/first-pass metrics, review cadence quarterly. `routed_out.to_automation`: ["metrics data pull"]. `requires_review`: none. `open_questions`: ["define the quality bar for a 'good insight' section"]. coverage_delta noted.

**Executed vs. approval:** Published the SOP draft to `operations.sops`, linked it to the process, scheduled the review reminder, and created a training task for the coordinator role (auto/notified, L2). Assigning it to the specific new hire and making it the enforced client-facing procedure were flagged for founder approval + People Agent.

## Provenance
SOURCE — derived from the operations knowledge base: the "codify tribal knowledge / operational manual" guidance, the Process Lifecycle ladder (understood → rationalized → codified → monitored), the good-process-map quality elements carried into documentation (standards, scripts, data capture, points of failure, recovery, fail-safe/poka-yoke), and the document-then-delegate rule. Metrics/thresholds are SYNTHESIZED industry standards, flagged as such. De-branded per repository rules.
