---
name: business-continuity-plan
domain: risk
version: 0.1.0
autonomy_ceiling: L1
provenance: SYNTH
reads: [risks, company, finance, operations, customers, team, market, strategy]
writes: [risks, strategy, metrics, decisions]
related_skills: [risk-diagnostic, crisis-response-planning, resource-gap-analysis, initiative-prioritization, ip-protection-audit]
owned_by_agents: [risk-agent, operations-agent]
---

# Skill: Business Continuity Plan (Single-Point-of-Failure & Concentration)

## Purpose
Find the places where the business would break if one thing failed — one customer, one employee, one supplier, one system, one channel — and turn each into a concrete diversification and redundancy plan. Concentration is invisible until it hurts; this skill makes it measurable, then reduces it so the business can keep operating through the loss of any single dependency.

## When to Use
- `risk-diagnostic` flags a concentration or continuity risk (one customer > ~20–25% of revenue, a sole-source supplier, a key person holding all of a capability, a single critical system with no backup).
- The founder asks "am I too dependent on X?", "what happens if [key person] leaves / [big client] leaves / our supplier goes down?", "we need a backup plan."
- After `crisis-response-planning` exposes a single-point-of-failure that must be structurally fixed so it can't recur.
- Proactively during scaling, when growth is amplifying a dependency (one account growing into dominance, one engineer becoming irreplaceable).
- Before onboarding a customer/supplier/system that would become a dominant dependency.

## When NOT to Use
- A dependency is *actively failing right now* → `crisis-response-planning` first (stabilize), then this skill to prevent recurrence.
- The founder wants a full risk inventory, not a continuity deep-dive → `risk-diagnostic`.
- The gap is purely a resource *shortfall* for a growth opportunity (not a single-point-of-failure) → `resource-gap-analysis`.
- The dependency is specifically about IP/trade-secret/knowledge protection and access controls → pair with `ip-protection-audit`.

## Required Context
- `customers`: revenue by account (concentration), contract terms, renewal dates.
- `operations`: vendors + `dependency_risk` + renewal dates, critical processes and their owners, tools/systems, `sop_ref` (is it documented?), capacity constraints.
- `team`: key-person roles, who holds which critical capability, headcount, turnover.
- `finance`: revenue mix, margins by line/customer, cash runway (buffer against a loss).
- `company`: business_model, single-channel vs. multi-channel, locations.
- `market`: alternative suppliers/partners available, competitive context.
- `risks`: existing concentration/continuity entries to update.

## Inputs
```yaml
input:
  dependencies:
    customers: [ {name_ref, revenue_share_pct, contract_end, switchable} ]
    suppliers: [ {name_ref, input_provided, is_sole_source, lead_time, alt_available} ]
    people:    [ {role, capability_held, is_sole_holder, documented, backup_exists} ]
    systems:   [ {name, function, is_critical, has_backup, recovery_time} ]
    channels:  [ {name, revenue_share_pct, owned_or_rented} ]  # e.g. one platform/marketplace
  financials:
    total_revenue: number
    cash_runway_months: number
    margin_by_line: [ {line, margin_pct} ]
  thresholds:                     # optional overrides of defaults
    customer_concentration_limit_pct: number
    supplier_sole_source_flag: bool
  scope: enum(full_continuity_scan, single_dependency)
```

## Missing Information Protocol
- **Compute concentration from data** (customer revenue share, channel share, margin mix) before asking anything.
- **Detect single-holder capabilities** from operations/team memory (a critical process whose `sop_ref` is empty and has one owner = undocumented single-point-of-failure).
- **Ask ONE batch** only for what data can't reveal: whether a customer/supplier is truly switchable, real lead times for alternatives, whether a backup person actually exists, and recovery-time expectations for systems.
- **Never assume** a supplier is replaceable, a person's knowledge is documented, a customer would stay, or a system has a working backup — verify each; unverified = `confidence: low` and "verify this dependency" as the first action.

## Diagnostic Questions
- **Customer:** what share of revenue is the largest account? top 3? Is it under contract, and when does it renew? If it left, how long could we survive on cash?
- **Supplier:** is any critical input single-sourced? What's the lead time to qualify an alternative? What's the cost of holding buffer inventory?
- **People (bus factor):** for each critical capability, how many people can do it? Is it documented (SOP)? Who is the sole holder of anything the business can't run without?
- **System/data:** which systems are critical? Do they have backups/redundancy? What's the recovery time if one fails? (Links to `ip-protection-audit` for access + data controls.)
- **Channel:** does most demand come through one channel/platform we don't own? What happens if its terms change or it de-platforms us?
- **Buffer:** how much cash/time buffer absorbs the loss of the biggest single dependency?

## Analysis Framework
1. **Map dependencies** across five classes: Customers, Suppliers, People, Systems/Data, Channels.
2. **Score each dependency** on two axes: **Concentration** (how much of the business rides on it) and **Substitutability** (how quickly/cheaply it can be replaced). High concentration + low substitutability = a true single-point-of-failure.
3. **Compute the resilience gap** per dependency: current state vs. a target where no single failure is fatal.
4. **Design redundancy/diversification** per gap, choosing the pattern that fits: *diversify* (add customers/suppliers/channels), *document* (SOPs so a capability isn't trapped in one head), *cross-train / hire backup* (raise the bus factor), *build backup/redundancy* (systems, data, buffer inventory), *contract for protection* (multi-source clauses, longer notice periods), or *build a buffer* (cash, inventory) to survive a loss.
5. **Convert each into a dated action-step chain** with an owner and a warning-signal metric (mirrors the Resource Map "have / need / action" and the Risk Audit's owner+metric discipline).
6. **Prioritize** by exposure (concentration × impact of loss) and by dependency/sequencing (some fixes unblock others). Hands off to `initiative-prioritization` when there are many.

This is SYNTHESIZED from the source Resource Map Gap Grid, the Risk Audit Tool, and the "growing too fast / concentration" risk prompts — recombined into a continuity discipline the running business needs.

## Calculations
- **Customer concentration** = largest customer revenue / total revenue. **Top-3 concentration** = top 3 / total. Trigger at > **20–25%** single / > **50%** top-3 (SYNTHESIZED defaults).
- **Channel concentration** = revenue via one channel / total.
- **Bus factor** = number of people who can perform a critical capability. Bus factor **= 1** is a single-point-of-failure; target ≥ 2.
- **Supplier risk** = sole-source (yes/no) × lead-time-to-replace (days) × input criticality (1–5).
- **Survival buffer** = cash_runway_months, tested against the revenue drop from losing the largest dependency: *adjusted runway* = cash / (burn adjusted for lost margin).
- **Resilience gap** per dependency = target redundancy − current redundancy (e.g. target bus factor 2 − current 1 = gap of 1 person to cross-train).
- **Exposure score** = concentration × impact-of-loss (1–5), used to rank fixes.
- **Recovery Time Objective (RTO)** for systems = acceptable downtime; flag any critical system whose recovery time > RTO.

## Decision Rules
- IF a single customer > 20–25% of revenue (or top-3 > 50%) THEN log a concentration risk and build a customer-diversification plan; set `largest_customer_share_pct` as a warning metric. (SYNTHESIZED)
- IF a critical input is single-sourced THEN qualify at least one alternative supplier and/or hold buffer inventory; add a multi-source or longer-notice contract clause (route contract terms to counsel). (SYNTHESIZED)
- IF a critical capability has bus factor = 1 THEN require documentation (SOP) **and** cross-training/backup; treat an undocumented sole-holder role as high priority. (SYNTHESIZED from Resource Map + key-person risk)
- IF a critical system has no backup OR recovery time > RTO THEN require redundancy/backup and a tested recovery procedure. (SYNTHESIZED)
- IF most demand flows through one channel the business doesn't own THEN develop a second, preferably owned, channel. (SYNTHESIZED)
- IF adjusted runway after losing the largest dependency < 3 months THEN raise the cash/inventory buffer and prioritize diversification urgently. (SYNTHESIZED)
- IF a fix requires a contract, hire, or spend THEN prepare it as an approval item; do not execute. (AUTONOMY model)
- IF the continuity gap involves IP/access/knowledge protection THEN also run `ip-protection-audit`. (SOURCE — trade-secret protection)
- IF a dependency is actively failing THEN switch to `crisis-response-planning`. (SYNTHESIZED)

## Procedure
1. **Pull dependency data** from memory (customers, operations/vendors, team, systems, channels) and compute all concentration/bus-factor/buffer metrics.
2. **Map the five dependency classes** and flag each as concentrated / substitutable / single-point-of-failure.
3. **Verify the risky ones** with the founder in one batch (switchability, lead times, real backups).
4. **Score exposure** (concentration × impact) and identify true single-points-of-failure.
5. **Design a mitigation** per gap using the pattern menu (diversify / document / cross-train / backup / contract / buffer).
6. **Turn each mitigation into a dated action-step chain** with an owner and a warning-signal metric.
7. **Prioritize** by exposure and sequencing; hand many initiatives to `initiative-prioritization`.
8. **Wire warning metrics** to the dashboard; update the `risks` register with the continuity entries and their plans.
9. **Record the plan** and set the next continuity review.

## Output
```yaml
output:
  continuity_map:
    - dependency: str
      class: enum(customer, supplier, people, system, channel)
      concentration_pct: number        # or bus_factor for people
      substitutability: enum(easy, moderate, hard)
      single_point_of_failure: bool
      impact_of_loss: int              # 1-5
      exposure_score: number           # concentration * impact
      current_state: str               # "what I have"
      target_state: str                # "what I need"
      mitigation_pattern: enum(diversify, document, cross_train, backup, contract, buffer)
      action_steps: [ {step, owner_id, deadline, reversible, needs_approval} ]
      warning_metric: {key, threshold, current_value}
      confidence: enum(low, medium, high)
  prioritized_initiatives: [ {dependency, exposure_score, rank} ]
  survival_test:
    largest_dependency: str
    adjusted_runway_months: number     # after losing it
    verdict: enum(resilient, fragile, critical)
  risk_register_updates: [ {risk, warning_metric} ]
  approvals_required: [str]
  next_review_date: date
```

## Recommendations
Prioritized by **exposure score (concentration × impact) and dependency sequencing**, with a strong bias toward the cheapest, most reversible fix that removes the single-point-of-failure: documenting a process (near-free) before hiring a backup; qualifying a second supplier before switching suppliers; adding a contract clause before restructuring a customer relationship. Fixes that both reduce a continuity risk *and* advance a growth objective (e.g. diversifying customers by entering a new segment) are elevated. Every fix that needs a spend, hire, or contract is separated out as an approval item with cost and rollback stated.

## Execution Opportunities
- **Draft SOPs / documentation** for undocumented sole-holder capabilities — reversible, LOW → prepare at L1.
- **Create cross-training / diversification tasks** with owners and deadlines — reversible, LOW.
- **Set up warning-signal metrics** (concentration %, bus factor, channel share) on the dashboard — reversible, LOW.
- **Update the risk register** with continuity entries — reversible, LOW.
- **Draft RFPs / outreach to alternative suppliers** (as drafts) — reversible; *sending* needs approval.
- Hiring a backup, signing a supplier/customer contract, buying redundant systems or buffer inventory → **never auto-executed**; approval items.

## Human Approval Requirements
Hold for founder approval (per `AUTONOMY_AND_APPROVAL_MODEL.md`):
- Any hire (backup/cross-hire) — employment action.
- Signing, changing, or terminating any supplier or customer contract, including multi-source or notice-period clauses — route contract terms to counsel.
- Any capital spend (redundant systems, buffer inventory, tooling).
- Deliberately *accepting* a concentration risk without mitigation — the founder owns and records that decision.

## Escalation Conditions
- **Founder:** any fragile/critical survival-test verdict; any deliberate acceptance of a single-point-of-failure.
- **CFO / accountant:** buffer sizing, financing a supplier switch, margin impact of diversification.
- **Attorney (via `legal-escalation-router`):** all contract clauses (multi-source, notice periods, exclusivity), and any customer/supplier agreement changes.
- **HR / attorney:** backup hires or role changes affecting specific employees.
- **IT / security specialist:** system redundancy, backups, and recovery testing (pair with `ip-protection-audit` for access/data controls).

## KPIs
- Largest-customer and top-3 revenue concentration trending down toward target.
- Channel concentration reduced (second owned channel live).
- Bus factor ≥ 2 for every critical capability; % of critical processes documented (SOP present).
- # of sole-source critical inputs reduced; qualified alternatives on file.
- Adjusted-runway survival test moving from fragile → resilient.
- % of continuity risks with an owner, dated plan, and warning metric.

## Monitoring
The Business Analyst Agent tracks each warning-signal metric (concentration %, bus factor, channel share, sole-source count) and fires when any drifts back toward its threshold — e.g. a customer growing into dominance again, or a newly critical process created without an SOP. Renewal dates for key customers/suppliers are watched so the business isn't caught flat-footed at contract end.

## Follow-Up
- **Time-triggered:** review quarterly (or with `risk-diagnostic`).
- **Event-triggered:** re-run when a new dominant dependency appears, before onboarding a would-be-dominant customer/supplier/system, after a near-miss, or when a warning metric drifts toward threshold.
- Retire a continuity risk only when the survival test passes and the redundancy is verified — record the outcome in `decisions`.

## Related Skills
- `risk-diagnostic` — source of the concentration/continuity flags; receives the continuity entries and metrics.
- `crisis-response-planning` — stabilizes an actively failing dependency; hands recurrence-prevention here.
- `resource-gap-analysis` — closes the resource gaps a continuity fix requires.
- `initiative-prioritization` — sequences many continuity initiatives.
- `ip-protection-audit` — for knowledge/data/access single-points-of-failure.

## Guardrails
- **Analysis auto-runs; contracts, hires, and spend do not** — all are approval items.
- **Never assume substitutability or a working backup** — verify; unverified dependencies are `confidence: low`, not "fine."
- **Contract clauses are drafted for counsel, never finalized here** — nothing may read as legal advice.
- **Diversification must not create a new fragility** (e.g. replacing one dominant customer with one dominant channel) — the plan is checked for shifted-concentration.
- **Documentation of a capability must respect IP/access controls** — sensitive procedures follow need-to-know (coordinate with `ip-protection-audit`).
- **Privacy:** customer/supplier identities and revenue shares are commercially sensitive; store restricted and never place in external URLs or payloads.

## Example
**Founder input:** "I keep hearing I'm too dependent. Where would we actually break?"

**Skill reasoning (data pulled + verified):**
- Customers: largest account = 45% of revenue, top-3 = 68%, under contract renewing in 4 months, not easily switchable → concentration SPOF, exposure = 0.45 × 5.
- People: one engineer is the sole holder of the deployment process, `sop_ref` empty → bus factor 1, undocumented → SPOF.
- Suppliers: one sole-source component, 6-week lead time, an alternative exists but unqualified → SPOF.
- Channel: 70% of leads via one marketplace the business doesn't own → channel SPOF.
- Survival test: losing the 45% customer drops adjusted runway from 5 → ~2.5 months → **fragile**.

**Output (abridged):**
| Dependency | Class | Conc/BusF | SPOF | Pattern | First action | Warning metric |
|---|---|---|---|---|---|---|
| 45% customer | customer | 45% | yes | diversify + buffer | 2-segment BD push; raise cash buffer | `largest_customer_share_pct` >40% |
| Deployment know-how | people | bf 1 | yes | document + cross-train | write SOP (this month); cross-train 2nd eng | `bus_factor`=1 |
| Sole-source part | supplier | — | yes | contract + backup | qualify alt supplier; buffer inventory; multi-source clause (**counsel**) | `sole_source_inputs` >0 |
| One marketplace | channel | 70% | yes | diversify | stand up owned channel (SEO/direct) | `channel_share_pct` >60% |

**Executed vs. approval:** the skill *auto-drafted* the deployment SOP outline, created cross-training and BD tasks, and wired the four warning metrics + risk entries (reversible, L1). It *held for approval*: the second-supplier contract and multi-source clause (counsel + founder), buffer-inventory spend (CFO), and the cross-hire (HR). It flagged that diversifying off the marketplace must not simply concentrate on a new single channel.

## Provenance
**SYNTH.** Recombines the Foundation & Strategy Resource Map Gap Grid (have / need / action across resource classes), the Risk Audit Tool (owner + deadline + warning-signal metric), and the source's concentration/continuity risk prompts ("growing too fast", customer/supplier/key-person dependency) into a continuity discipline the source implies but does not package. Concentration thresholds, bus-factor targets, and RTO logic are SYNTHESIZED defaults, configurable per business. All source program branding removed.
