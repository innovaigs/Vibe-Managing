---
name: automation-triage
domain: operations
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [operations, offerings, team, finance, metrics, strategy, integrations]
writes: [operations, metrics, decisions]
related_skills: [process-mapping, process-optimization, technology-evaluation, sop-writer, bottleneck-analysis, operational-audit]
owned_by_agents: [operations-agent]
---

# Skill: Automation Triage

## Purpose
For each step of a process, decide the right disposition — automate, document, delegate, outsource, or keep manual — based on the step's volume, judgment, value, and core-competency profile, and note the tool fit and price point, so the founder invests effort where it pays off and stops doing work that a system or someone else should own.

## When to Use
- "Automate this", "what should we automate?", "I'm doing too much manual work here", "should we outsource this?"
- After `process-mapping` flags automation candidates, or `process-optimization` tags steps `automate`.
- When freeing founder/owner time by routing owner-dependent steps to systems or people.
- Before buying tools or hiring — to confirm the *disposition* (automate vs. delegate vs. outsource) before choosing the specific tool/vendor.

## When NOT to Use
- The process isn't mapped into steps yet → `process-mapping` first.
- You've decided to automate and now need to pick/compare specific tools with due diligence → `technology-evaluation`.
- The step is waste that should be removed, not automated → `process-optimization` (eliminate before automating).
- The whole business needs a scan → `operational-audit`.
- You need to write the human procedure for a "document/delegate" disposition → `sop-writer` (downstream of this skill).

## Required Context
- `operations.processes` — the mapped steps, with volume, judgment level, and current owner.
- `operations.tools` and `integrations` — what's already in place (avoid buying what you have; prefer integration).
- `offerings` — which steps are the core competency / competitive advantage (never outsource these).
- `finance` — step cost (labor) and available budget, to size ROI.
- `team.org` — who could own delegated steps (authority level, capacity).
- `strategy.growth_plan` — volume trajectory (automation pays off more as volume grows).

## Inputs
```yaml
input:
  process: object|string                # mapped process (preferred) or name
  steps:
    - step: string
      volume_per_period: number|null    # how often it runs
      judgment_level: enum(none, low, medium, high)   # how much human judgment it needs
      rule_based: boolean               # deterministic rules vs. ambiguous
      customer_value: enum(none, low, medium, high)    # customer-perceived value
      is_core_competency: boolean       # source of competitive advantage
      current_owner: string             # who does it today (role)
      manual_cost_per_period: number|null   # labor/time cost
      error_prone: boolean
  budget: number|null                   # available for tooling/outsourcing
  existing_tools: list[string]
  constraints: list[string]             # compliance, data-sensitivity, integration limits
```

## Missing Information Protocol
1. Prefer a `process-mapping`/`process-optimization` output; pull step profiles from `operations.processes` where possible.
2. For each step, the four attributes that decide disposition are volume, judgment, customer value, and core-competency. If any is unknown for a candidate step, ask the founder a single batched matrix ("for each of these steps: how often, how much judgment, does the customer value it, is it your special sauce?").
3. Never assume a step is non-core or low-judgment to justify automating/outsourcing it — misclassifying the core competency is the costly error. Confirm core-competency status before recommending outsource.
4. If manual cost is unknown, estimate from time × loaded labor rate and mark ROI directional.
5. Start from the burning need (the problem the disposition solves), not the tool — do not name a specific product here; that's `technology-evaluation`.

## Diagnostic Questions
- Is this step repetitive, rule-based, high-volume, and low-judgment? → automate.
- Is it recurring, needs some judgment/skill, and currently tribal knowledge? → document (then it can be learned/monitored/delegated).
- Is it documented and ownable by an employee with clear metrics? → delegate.
- Is it non-core, low customer-visible value, and someone else can do it better/cheaper? → outsource/buy.
- Is it low-volume, high-judgment, or lacking a right-fit affordable tool? → keep manual (for now).
- Is this step the core competency / source of competitive advantage? → never outsource; keep in-house (automate/delegate at most).
- Does a right-fit tool exist at the right price, and does it integrate with existing systems?
- What's the burning need this disposition solves, and what value is created?

## Analysis Framework
Per-step disposition routing (the automate / document / delegate / outsource / keep-manual decision):
1. **Screen for waste first.** If the step is non-value-added and removable, route to `process-optimization` to eliminate — don't automate waste.
2. **Screen for core competency.** If `is_core_competency`, remove outsource from the option set (keep in-house; automate/delegate only).
3. **Score the step** on volume, judgment, rule-based, customer value.
4. **Route** using the decision rules below.
5. **Tool/price note** (for automate/outsource dispositions): does a right-fit, right-price tool/provider plausibly exist, and does it integrate? Note fit and rough price band — but defer the specific selection to `technology-evaluation`.
6. **ROI gate** (for automate/outsource with cost): compute automation ROI; require positive ROI / reasonable payback before recommending spend.
7. **Sequence.** Order dispositions by value released vs. effort; note dependencies (e.g. must `document` before `delegate`).

## Calculations
- **Automation ROI** = (annual manual cost saved − annual tool cost) ÷ annual tool cost. Positive with payback < ~12 months = strong candidate.
- **Annual manual cost** = manual_cost_per_period × periods per year (or time × loaded labor rate × frequency).
- **Payback period** = tool/setup cost ÷ annual cost saved.
- **Volume-judgment score** (routing heuristic): high volume + low judgment + rule-based → automate; low volume + high judgment → keep manual/delegate. (Qualitative matrix; not a single number.)
- **Outsourcing cost comparison** = in-house fully-loaded cost vs. vendor quote (only compare for non-core, low-value steps).
- **Time released** = founder/owner hours returned per period by the disposition (key benefit for owner-dependent steps).
- Note: automation ROI rises with volume/growth — re-score borderline steps against the growth plan's projected volume.

## Decision Rules
- IF a step is non-value-added and removable THEN eliminate it first (`process-optimization`) — do not automate waste.
- IF a step is repetitive, rule-based, high-volume, low-judgment AND a right-fit affordable tool plausibly exists THEN **automate** → confirm tool via `technology-evaluation`.
- IF a step recurs, needs some judgment/skill, and is currently tribal knowledge THEN **document** (write SOP → `sop-writer`) so it can be learned and monitored.
- IF a step is documented and can be owned by an employee with defined metrics and ownership THEN **delegate** (→ People Agent delegation) — this frees the owner and builds scale.
- IF a step is non-core, low customer-visible value, and someone external can do it more effectively/cheaply THEN **outsource/buy**.
- IF a step is the core competency or a source of competitive advantage THEN never outsource; keep in-house (automate/delegate at most).
- IF a step is low-volume, high-judgment, or has no right-fit affordable tool THEN **keep manual** (for now); re-score as volume grows.
- IF automation ROI is negative or payback is very long THEN do not automate now; keep manual or delegate.
- IF a right-fit tool would be wrong-fit or wrong-price for this specific business THEN do not adopt; require due diligence (`technology-evaluation`) first.
- IF a step must be documented before it can be delegated/automated THEN sequence document → delegate/automate (dependency).
- IF a step handles sensitive/regulated data THEN add a compliance constraint to any automate/outsource disposition (data leaves the business only with approval).

## Procedure
1. Ingest the mapped steps and profiles; pull existing tools/integrations and budget.
2. Screen out removable waste (route to `process-optimization`).
3. Flag core-competency steps (lock out outsourcing).
4. Score each step on volume/judgment/rule-based/customer-value.
5. Route each step to a disposition per the rules; note tool fit + price band and any compliance constraint.
6. Compute ROI/payback for cost-bearing dispositions; apply the ROI gate.
7. Sequence dispositions (respect document-before-delegate dependencies); estimate time released.
8. Produce the per-step disposition table; route each to its downstream skill; create draft tasks. Nothing that spends money, commits a vendor, or reassigns a person is executed — those are proposals.

## Output
```yaml
output:
  process: string
  dispositions:
    - step: string
      disposition: enum(automate, document, delegate, outsource, keep_manual, eliminate)
      rationale: string
      volume: string
      judgment_level: enum(none, low, medium, high)
      is_core_competency: boolean
      tool_fit_note: string|null        # function-level, not a product name; price band
      roi:
        annual_cost_saved: number|null
        est_tool_or_vendor_cost: number|null
        payback_months: number|null
        ratio: number|null
      compliance_constraint: string|null
      routes_to: string                 # downstream skill/agent
      depends_on: string|null           # e.g. "document before delegate"
      requires_approval: boolean
  sequencing: list[string]              # ordered plan of dispositions
  founder_time_released_per_period: number|null
  quick_wins: list[string]              # high-value, low-effort, low-risk dispositions
  open_questions: list[string]
```

## Recommendations
Prioritize by **value released (time/cost/scale) ÷ effort, respecting dependencies and reversibility.** Lead with quick wins: high-volume rule-based steps with a cheap right-fit tool, and owner-dependent steps that can be documented-then-delegated to release founder time. Present outsourcing only for confirmed non-core, low-value steps. Every automate/outsource recommendation states the burning need it solves and the value created, and hands the specific-tool decision to `technology-evaluation` — never commit a product here.

## Execution Opportunities
- Write the disposition table and sequencing plan to `operations` memory as proposals (L1).
- Create draft tasks for each disposition and route them (document→`sop-writer`, tool→`technology-evaluation`, delegate→People Agent) (L1).
- Draft ROI summaries for cost-bearing dispositions (L1 draft).
- No purchasing, no vendor/outsourcing commitment, no headcount/delegation to a specific person is auto-executed.

## Human Approval Requirements
- Purchasing or committing to any automation tool → founder approval (via `technology-evaluation` due diligence first).
- Any outsourcing / vendor commitment → founder approval (vendor commitment per AUTONOMY_AND_APPROVAL_MODEL §4).
- Delegating a step to a specific employee → founder approval + People Agent (employee-specific action).
- Any disposition that changes a customer-facing step → founder approval.
- Automating/outsourcing a step handling sensitive/regulated data → founder approval + compliance review.

## Escalation Conditions
- A step proposed for outsource turns out to be core/competitive-advantage → escalate to founder before proceeding (misclassification risk).
- Outsourcing/automation of regulated or sensitive-data steps → legal/compliance.
- Delegation implies a role/authority change → People Agent / HR.
- ROI hinges on estimated manual costs and a large spend is implied → surface uncertainty; recommend measuring before committing.

## KPIs
- Time released: founder/owner hours returned per period.
- Cost saved / ROI realized vs. projected for executed dispositions.
- Disposition accuracy: did automated steps stay automated (no revert), delegated steps hold, outsourced steps meet quality?
- Coverage: % of eligible steps triaged.
- Growth readiness: manual steps that would break at target volume, addressed ahead of time.

## Monitoring
After a disposition is executed (elsewhere), watch: for automation — reliability/error rate and realized savings; for delegation — the delegate's quality metrics and whether the owner truly stepped back; for outsourcing — vendor quality/SLA and cost vs. estimate. Re-triage borderline "keep manual" steps as volume grows.

## Follow-Up
- Re-run when volume steps up (more steps cross the automate threshold), a new tool/integration lands, or after `process-optimization`.
- Feed executed automations back to `sop-writer` (document the manual fallback) and to the metrics dashboard.

## Related Skills
- `process-mapping` / `process-optimization` — supply the steps and remove waste first.
- `technology-evaluation` — selects and vets the specific tool for automate/outsource dispositions.
- `sop-writer` — writes the procedure for document/delegate dispositions.
- `bottleneck-analysis` — automation of the constraint step yields the most throughput.

## Guardrails
- Execution ceiling L1; no purchase, vendor commitment, delegation-to-person, or customer-facing change is auto-executed.
- Start from the burning need, not the tool; never name/commit a specific product here.
- Never outsource the core competency or a competitive advantage — confirm classification before recommending outsource.
- Eliminate waste before automating it.
- Require positive ROI / reasonable payback and right-fit-right-price due diligence before recommending spend.
- Add a compliance constraint to any disposition touching sensitive/regulated data; such data leaves the business only with approval.

## Example
**Founder input:** solo consultant's client-delivery process, 6 steps. (1) schedule kickoff — volume high, judgment low, rule-based, customer value low, not core; (2) run discovery workshop — high judgment, high customer value, IS core competency; (3) send follow-up notes — high volume, low judgment, rule-based, some customer value, not core; (4) build the strategy deck — high judgment, high value, core; (5) invoice — high volume, rule-based, no customer value, not core, error-prone; (6) bookkeeping/expense categorization — recurring, low value, not core. Budget modest.

**Skill reasoning:**
- (1) schedule kickoff → **automate** (rule-based scheduling; right-fit cheap tool exists; ROI high; route to `technology-evaluation`).
- (2) discovery workshop → **keep manual** (core competency, high judgment — never automate/outsource).
- (3) follow-up notes → **document** now (tribal knowledge → `sop-writer`), then **automate** the send/formatting later; some judgment in content stays manual.
- (4) strategy deck → **keep manual** (core).
- (5) invoicing → **automate** (rule-based, error-prone, no customer value; ROI strong once billing data is structured).
- (6) bookkeeping → **outsource** (non-core, low value; a bookkeeper does it better/cheaper) — founder approval.
- Sequencing: automate scheduling + invoicing (quick wins) → document follow-ups → outsource bookkeeping. founder_time_released estimated in hours/week.

**Output (excerpt):** dispositions table as above; quick_wins = ["automate scheduling", "automate invoicing"]; routes: scheduling/invoicing → `technology-evaluation`, follow-ups → `sop-writer`, bookkeeping → founder approval + vendor selection. open_questions = ["confirm invoicing tool integrates with current accounting"].

**Executed vs. approval:** Wrote the disposition plan and draft tasks (auto, L1). Buying the scheduling/invoicing tools and engaging a bookkeeper were flagged `requires_approval: true`; nothing was purchased or committed.

## Provenance
SOURCE — derived from the operations knowledge base: the automate / document / delegate / outsource / keep-manual routing criteria, the "right technology at the right price for a specific business + do due diligence" principle, the "burning need → solution → value created" problem-first framing, the outsource-non-core / never-outsource-core-competency rule, and the document-before-delegate lifecycle rule. ROI/payback formulas are SYNTHESIZED industry standards, flagged as such. De-branded per repository rules (tools referenced by function, not product).
