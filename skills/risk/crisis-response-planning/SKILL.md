---
name: crisis-response-planning
domain: risk
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [risks, company, finance, operations, market, customers, team, strategy, decisions]
writes: [risks, decisions, strategy, metrics]
related_skills: [risk-diagnostic, business-continuity-plan, opportunity-feasibility-analysis, cash-flow-diagnostic, legal-escalation-router]
owned_by_agents: [risk-agent, strategy-agent]
---

# Skill: Crisis Response Planning

## Purpose
When a low-probability, high-impact event hits — or is about to — this skill helps the founder respond with a clear head: assess the real impact, protect the business's viability, decide fast under ambiguity, and then extract the new opportunity and the lessons the crisis reveals. A crisis is not only a threat to survive; run correctly, it surfaces new customer needs, exposes resource gaps worth fixing, and can seed the next growth opportunity.

## When to Use
- An acute disruption is happening or imminent: loss of the largest customer, a key employee's sudden departure, a supply-chain break, a natural disaster or facility loss, a data breach, a cash cliff, a demand collapse, a reputational hit, or a regulatory/legal shock.
- A `risk-diagnostic` warning-signal metric just breached its threshold on a Critical, Low-probability/High-impact risk.
- The founder says "everything just changed", "we might not make payroll", "we lost [the big client]", "I don't know what to do first."
- Pre-emptively, to build a contingency plan for a specific Low-probability/High-impact risk *before* it happens (crisis pre-mortem).

## When NOT to Use
- The threat is not yet real and the founder wants to inventory/score risks broadly → `risk-diagnostic`.
- The issue is chronic concentration / single-point-of-failure without an acute trigger → `business-continuity-plan`.
- It's a routine cash-tightness question, not an existential one → `cash-flow-diagnostic`.
- The crisis is fundamentally a legal event (lawsuit served, subpoena, government audit, harassment/discrimination claim) — run the stabilization steps but immediately route the legal substance via `legal-escalation-router`; do not craft the legal response here.

## Required Context
- `company`: stage, entity, jurisdictions, locations, business_model.
- `finance`: current cash balance, runway, burn, AR/AP, covenants — the survival math.
- `operations`: critical processes, vendors and their `dependency_risk`, capacity, tools.
- `customers`: largest accounts, concentration, contracts at risk.
- `team`: key-person roles, headcount.
- `market`: competitors, trends, regulatory_context.
- `risks`: the register (was this crisis a known risk? was there a contingency plan?).
- `strategy` / `decisions`: current priorities and any relevant prior decisions.
If the crisis is fast-moving and context is incomplete, proceed with a stabilization pass on what is known and flag data gaps rather than stalling.

## Inputs
```yaml
input:
  crisis:
    description: str                 # what happened / is happening
    onset: enum(imminent, active, aftermath)
    trigger_type: enum(customer_loss, key_person_loss, supply_chain, facility, cash,
                       demand_shock, reputational, cyber_data, regulatory_legal, other)
    detected_at: datetime
    was_known_risk: bool             # did it appear on the risk register?
    had_contingency_plan: bool
  survival_snapshot:
    cash_on_hand: number
    monthly_burn: number
    runway_months: number
    obligations_next_30d: [ {item, amount, due_date} ]   # payroll, rent, loan, key vendors
  affected:
    customers: [str]                 # accounts at risk
    revenue_at_risk_pct: number
    operations_disrupted: [str]
    people_affected: [str]
  constraints:
    time_pressure: enum(hours, days, weeks)
    decision_owner: str
```

## Missing Information Protocol
- **Stabilize first, complete later.** In an active crisis, do not block on missing fields — run the immediate-stabilization triage on what's known and mark the rest as gaps to close within hours.
- **Compute the survival math** (runway = cash / burn; can the next 30 days of obligations be met?) from finance data before asking the founder anything.
- **Ask ONE focused batch** for the few decision-critical unknowns (exact cash position, which obligations are non-negotiable, which customers/contracts are truly lost vs. wobbling).
- **Never assume** the crisis is contained, that a customer is fully lost, that insurance covers it, or that a legal exposure is minor. Never fabricate the cash position — if unknown, that *is* the first emergency task.

## Diagnostic Questions
**Is this a crisis? (SOURCE — crisis definition; typically all present):** low-probability + high-impact; threatens organizational viability; highly ambiguous; time pressure to decide; often a surprise; shatters prior assumptions. If most hold, treat as a crisis.

**Stabilization triage:** Can we make payroll / rent / critical vendor payments in the next 30 days? What must not fail (people safety, cash, key customer relationships, data/legal obligations)? What can be paused without permanent damage?

**Three-part crisis analysis (SOURCE):**
1. **Impact** — effect on product/service; operations (buildings, equipment, tech, people); supply chain; customers; reputation; competitive advantage; finances.
2. **Resources** — which resources are most critical now; can resources be redirected; what knowledge/skills did we have vs. need; what gaps appeared and how were they filled.
3. **New Opportunities** — what new customer needs did the crisis create; what problems now need solving; a possible new product/service; a possible new market (size, and is it temporary or lasting).

## Analysis Framework
Two-phase: **Stabilize, then Reframe.**

**Phase 1 — Protect viability (triage).**
- Run the crisis-definition check to confirm scope.
- Compute the **survival window**: runway and whether the next 30/60/90 days of obligations can be met.
- Rank actions by "prevents an irreversible loss soonest": protect people/safety and legal obligations → protect cash and the ability to operate → protect the most valuable customer relationships → protect reputation. Anything that stops an irreversible loss with the least commitment goes first.
- Identify decisions that can wait vs. those forced now by time pressure; make the minimum irreversible commitments.

**Phase 2 — Crisis → Opportunity reframe (SOURCE).**
- Run the three-part Impact / Resources / New-Opportunities analysis.
- Feed the **resource gaps** discovered into `business-continuity-plan` / `resource-gap-analysis`.
- Feed any **new opportunity candidate** back into the opportunity pipeline (`opportunity-feasibility-analysis`) — sized, and tagged temporary vs. lasting.
- Capture **lessons learned** and update the risk register: was this a known risk? did the contingency plan work? what warning signal should have fired earlier?

## Calculations
- **Runway (months)** = cash_on_hand / monthly_burn.
- **30/60/90-day obligation coverage** = cash_on_hand − Σ(non-deferrable obligations due in window); negative = a cash cliff requiring immediate action.
- **Revenue at risk %** = revenue tied to affected customers / total revenue.
- **Concentration exposure** (if customer-loss crisis) = lost customer revenue / total revenue.
- **Break-even under reduced revenue** = fixed costs / (1 − variable cost ratio), recomputed at the post-crisis revenue level to test whether the current cost base is survivable.
- **New-opportunity sizing (from the reframe)** = estimated addressable demand created by the crisis × capture assumption, tagged temporary vs. lasting.
- **Time-to-stabilize** = elapsed time from detection to "viability secured" (a KPI for future preparedness).
(All are standard survival math; thresholds like "6 months runway" are SYNTHESIZED defaults, configurable.)

## Decision Rules
- IF most crisis-definition criteria hold THEN treat as a crisis: prioritize stabilization over analysis paralysis, and make only the minimum irreversible commitments. (SOURCE)
- IF the next-30-day obligation coverage is negative THEN a cash cliff is the top priority: trigger cash-preservation + financing options immediately (route financing to founder + CFO). (SYNTHESIZED)
- IF runway < 3 months THEN escalate to founder now; prepare cost-reduction and financing options as approval items. (SYNTHESIZED)
- IF the crisis threatens people safety, legal obligations, or data/privacy THEN those take precedence over financial optimization, and legal/privacy items route to counsel immediately. (SOURCE guardrail)
- IF the crisis is a legal event (suit, subpoena, audit, protected-class claim, breach) THEN stabilize operations but route the legal substance via `legal-escalation-router`; do not draft the legal response. (SOURCE — legal guardrail)
- IF the crisis was a **known risk with a contingency plan** THEN activate that plan and measure whether it worked. (SOURCE)
- IF the crisis was **not** on the register OR had no plan THEN, after stabilizing, add it and design the warning signal that should have fired. (SOURCE)
- IF the crisis reveals a resource gap THEN feed it to `business-continuity-plan` / `resource-gap-analysis`. (SOURCE)
- IF the crisis creates a credible new opportunity THEN feed it (sized, temporary-vs-lasting) into `opportunity-feasibility-analysis`. (SOURCE)
- IF time_pressure is "hours" AND data is incomplete THEN act on the stabilization triage now and close data gaps in parallel — do not wait for full information. (SOURCE — decide under ambiguity)

## Procedure
1. **Confirm it's a crisis** via the definition check; set onset (imminent/active/aftermath).
2. **Compute the survival window** from finance data (runway, 30/60/90-day obligation coverage).
3. **Triage immediate actions** ranked by "prevents irreversible loss soonest": safety/legal → cash → key customers → reputation. Separate must-do-now from can-wait.
4. **Draft the immediate action plan** — each action with an owner, a deadline (hours/days), and whether it's reversible or needs approval.
5. **Run the three-part analysis** (Impact / Resources / New Opportunities) once the bleeding is stopped.
6. **Identify resource gaps** and hand them to continuity/resource skills.
7. **Surface new-opportunity candidates**, size them, tag temporary vs. lasting, and route to the opportunity pipeline.
8. **Capture lessons learned**; update the `risks` register and its warning signals; record the whole episode in `decisions` (context, options, decision, expected vs. actual).
9. **Set monitoring** for the recovery (which metrics confirm stabilization) and a debrief follow-up.

## Output
```yaml
output:
  crisis_assessment:
    is_crisis: bool
    onset: enum(imminent, active, aftermath)
    viability_threat: enum(low, moderate, severe, existential)
    survival_window_months: number
    obligation_coverage_30d: number     # negative = cash cliff
  immediate_action_plan:
    - action: str
      priority: int                     # 1 = do first
      owner_id: str
      deadline: datetime
      reversibility: enum(reversible, recoverable, irreversible)
      needs_approval: bool
  impact_assessment:                    # SOURCE 3-part, section 1
    product_service: str
    operations: str
    supply_chain: str
    customers: str
    reputation: str
    competitive_advantage: str
    finances: str
  resource_findings:                    # section 2
    most_critical_resources: [str]
    redirected: [str]
    gaps_discovered: [str]
    how_filled: [str]
  new_opportunities:                    # section 3
    - description: str
      new_need_created: str
      est_size: str
      horizon: enum(temporary, lasting)
      route_to: str                     # opportunity-feasibility-analysis
  lessons_learned: [str]
  risk_register_updates: [ {risk, was_known, plan_worked, new_warning_signal} ]
  recovery_metrics: [ {key, target, checkpoint_date} ]
  approvals_required: [str]
  escalations: [str]
  decision_record_id: str
```

## Recommendations
Immediate actions are ranked by **speed-to-prevent-irreversible-loss**, not by ROI — in a crisis, avoiding a fatal outcome beats optimizing a good one. Within that, prefer reversible moves (pause spend, defer non-critical projects, open a conversation with the key customer) before irreversible ones (layoffs, taking on debt, terminating contracts). Every irreversible or financial action is presented as an approval item with its rollback (or "irreversible") stated. In the reframe phase, opportunities are prioritized by whether the created need is *lasting* (worth pursuing) vs. *temporary* (worth a short-term play only), and by fit with the existing competitive advantage.

## Execution Opportunities
- **Draft the immediate action plan and assign tasks** (internal task system) — reversible, LOW → prepare at L1.
- **Recompute and publish the survival dashboard** (runway, obligation coverage) — reversible, LOW.
- **Record the crisis + decisions** in `decisions` and update `risks` — reversible, LOW.
- **Draft internal/holding communications** (to team, to a key customer) — reversible drafts, but *sending* external communication needs approval.
- **Open a new-opportunity candidate** in the pipeline — reversible, LOW.
- Layoffs, financing, contract termination/signing, external statements, insurance claims → **never auto-executed**; approval items only.

## Human Approval Requirements
Always hold for founder approval (per `AUTONOMY_AND_APPROVAL_MODEL.md` — these are HIGH/CRITICAL):
- Any money movement: drawing debt, emergency financing, large payments, refunds.
- Any employment action: layoffs, furloughs, terminations, comp changes.
- Any external communication that commits the company (statements to customers, press, regulators).
- Signing, amending, or terminating any contract.
- Any legal response or filing.
- Any irreversible operational shutdown or asset disposal.
The agent prepares options with recommendations and rollback notes; the founder decides.

## Escalation Conditions
- **Founder (immediately):** any existential viability threat, cash cliff, or irreversible decision.
- **Accountant / CPA:** cash, solvency, tax, and financing dimensions.
- **Attorney (via `legal-escalation-router`):** any legal trigger — lawsuit, subpoena, audit, breach, protected-class claim, contract termination, or layoff execution.
- **HR / attorney:** people actions affecting specific employees.
- **Insurer / broker:** where coverage may apply (claim filed by the founder, not the agent).
- **Cybersecurity / privacy specialist:** data breach — plus mandatory breach-notification analysis by counsel.
Escalations carry: situation, what's known, confidence, decision needed, recommended option + rationale, and the deadline forced by time pressure.

## KPIs
- Time-to-stabilize (detection → viability secured).
- Whether the survival window was correctly assessed (predicted vs. actual runway).
- % of immediate actions completed on time.
- Revenue / customers retained vs. at-risk after the crisis.
- Whether the crisis was a known risk with a working plan (preparedness).
- # of new opportunities identified and advanced from the reframe.
- Lessons converted into updated risk register entries + warning signals.

## Monitoring
During the crisis, monitor the survival dashboard (cash, obligation coverage, retained revenue) at high frequency. After stabilization, monitor recovery metrics to confirm the business is out of danger and watch for secondary crises (a customer loss triggering a cash crisis triggering a talent exodus). Feed the new warning signals into the ongoing `risk-diagnostic` monitoring so the same crisis is caught earlier next time.

## Follow-Up
- **Event-triggered:** re-run if the crisis worsens or a secondary crisis emerges.
- **Post-crisis debrief:** run a formal lessons-learned pass once stabilized; update `risks`, `decisions`, and the dashboard.
- **Feed-forward:** each identified Low-probability/High-impact risk should get a *pre-built* contingency plan via this skill in pre-mortem mode, so future crises start from a plan, not a blank page.

## Related Skills
- `risk-diagnostic` — source of the risk register; receives updates and new warning signals.
- `business-continuity-plan` — receives resource gaps and single-point-of-failure findings.
- `resource-gap-analysis` — closes the resource gaps the crisis exposed.
- `opportunity-feasibility-analysis` — validates new-opportunity candidates from the reframe.
- `cash-flow-diagnostic` — deepens the survival math.
- `legal-escalation-router` — for any legal dimension of the crisis.

## Guardrails
- **People, safety, legal, and data obligations outrank financial optimization.**
- **Decide under ambiguity, but only the minimum irreversible commitment** — prefer reversible moves and preserve optionality.
- **No legal response is drafted here** — legal substance always routes to counsel; nothing may read as legal advice.
- **No money, employment, external-comms, or contract action is auto-executed** — all are approval items with rollback stated.
- **Never fabricate the cash position or the extent of the damage** — unknowns become emergency information tasks, not assumptions.
- **The opportunity reframe must not distract from stabilization** — it runs *after* viability is secured (or in parallel only once the bleeding is stopped).
- **Privacy:** crisis details (insolvency, breach, layoffs, litigation) are restricted-sensitivity; never place them in external URLs, payloads, or shared docs.

## Example
**Founder input (aftermath onset):** "Our biggest client (45% of revenue) just gave notice — they leave in 60 days. Can we survive?"

**Skill reasoning:**
- Crisis check: high impact ✔, threatens viability ✔, surprise ✔, time pressure (60 days) ✔ → crisis confirmed, onset = active/aftermath.
- Survival math: cash $180k, burn $60k/mo → runway 3 months at current cost; post-loss revenue drops 45% → new burn-adjusted runway ~2 months unless costs cut. 30-day obligations (payroll $40k, rent $8k, key vendor $5k) covered now; 60–90 day window turns negative → cash cliff approaching.
- Triage (ranked): (1) protect cash — freeze discretionary spend, defer non-critical projects [reversible, do now]; (2) protect the relationship — founder call to the departing client to understand *why* and explore a scaled-down/transition contract [reversible]; (3) accelerate pipeline to replace revenue; (4) model cost reductions incl. possible role changes [approval item].
- Three-part analysis: **Impact** — 45% revenue gone, delivery team over-capacity, reputation risk if churn is public. **Resources** — sales capacity is the binding constraint; over-reliance on one account was the gap. **New opportunities** — the freed delivery capacity + the reason for churn (client wanted a capability we underinvested in) points to a new productized offering; likely *lasting* need.
- Lessons: this was on the register as "customer concentration, score 20, Critical" — the warning metric (`largest_customer_share_pct > 40%`) had fired but no contingency plan existed. Add the plan now.

**Output (abridged):**
- Immediate plan: freeze spend (owner: founder, today, reversible); client retention/transition call (founder, 48h, reversible); pipeline sprint (sales, 2 weeks); cost-reduction model incl. role review (CFO, 1 week, **approval**).
- New opportunity: productized version of the capability the client left for → routed to `opportunity-feasibility-analysis`, sized, tagged lasting.
- Risk updates: add contingency plan to the concentration risk; hand the concentration + capacity gap to `business-continuity-plan`.

**Executed vs. approval:** the skill *auto-drafted* the action plan, recomputed the survival dashboard, recorded the decision, and opened the opportunity candidate (all reversible, L1). It *held for approval*: any cost reduction touching specific roles (founder + HR/attorney), and any emergency financing (founder + CFO). No layoff, financing, or external statement was executed by the agent.

## Provenance
**SOURCE.** Derives from the Foundation & Strategy domain: the Organizational Crisis → Opportunity Reframe (crisis definition; the three-part Impact / Resources / New-Opportunities analysis; feeding new opportunities back into the pipeline), the Risk vs. Uncertainty distinction (crises live in the "unknown world" and can't be managed by forecast alone), and the Entrepreneurial Mindset stance for deciding under ambiguity. Survival-math formulas and runway thresholds are standard finance / SYNTHESIZED defaults. All source program branding and named case studies removed.
