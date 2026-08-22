---
name: marketing-strategy-builder
domain: marketing
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [customers, offerings, market, strategy, finance, goals, metrics, integrations]
writes: [strategy, goals, decisions]
related_skills: [customer-value-proposition-builder, marketing-funnel-planner, channel-selection, social-content-planner, keyword-and-search-map, website-conversion-audit, marketing-metrics-tracker]
owned_by_agents: [marketing-agent, growth-agent]
---

# Skill: Marketing Strategy Builder

## Purpose
Turns the pieces of marketing strategy — positioning/CVP, the buyer's-journey funnel, and the chosen channels — into a single dated action plan with an owner, a deadline, a channel, and a success metric for every step. It is the assembler that converts "we know who we are and where to reach them" into "here is exactly what we do, in what order, by when, and how we'll know it worked."

## When to Use
- The founder asks "build our marketing plan", "what's our marketing strategy?", "put it all together", "what do we actually do first?"
- After the upstream pieces exist (CVP, funnel plan, channel plan) and need sequencing into an executable plan.
- Quarterly/growth-plan refresh, or when a new offering/segment needs its own go-to-market plan.
- When a performance review (via `marketing-metrics-tracker`) says the current plan isn't working and it needs to be rebuilt.

## When NOT to Use
- Positioning, funnel, or channels are still undefined → run `customer-value-proposition-builder`, `marketing-funnel-planner`, and `channel-selection` first; this skill assembles their outputs, it doesn't originate them.
- The founder wants a single tactical artifact (one calendar, one audit) → use the specific skill (`social-content-planner`, `website-conversion-audit`).
- Pure measurement/monitoring → `marketing-metrics-tracker`.
- Company-wide strategy beyond marketing (pricing, product, financing) → Strategy/CFO agents; this skill stays within the marketing plan and defers cross-functional calls.

## Required Context
- `offerings.cvp_id` / `customer-value-proposition-builder` output — the positioning the plan communicates.
- `customers.personas` — who each track of the plan targets.
- `marketing-funnel-planner` output — the {message, tool, action} triple per funnel stage (the spine of the plan).
- `channel-selection` output — the channels attached to each stage/goal.
- `market.competitors` / `competitive-advantage-assessment` — the point-of-difference the plan leans on.
- `goals` + `strategy.growth_plan` — the objective, target metric, and target date the plan must serve.
- `finance` — marketing budget/runway constraints (any spend in the plan is checked against this).
- `team` (owners) and `metrics` (baselines) — to assign owners and set measurable targets.

## Inputs
```yaml
input:
  objective:                       # REQUIRED. The business outcome the plan serves.
    type: {statement: str, target_metric: str, target_value: number, target_date: date}
  cvp: str                         # REQUIRED (or cvp_id). The positioning to communicate.
  target_personas: [str]          # REQUIRED. Persona ids the plan addresses.
  funnel_plan:                     # REQUIRED. Per-stage message/tool/action (from funnel-planner).
    type: list[{stage: enum(awareness, interest, desire, action, retention),
                message: str, tool: str, action: str, influence_lever: str}]
  channel_plan:                    # REQUIRED. Channels per stage/goal (from channel-selection).
    type: list[{stage: str, channel: str, poem: enum(paid, owned, earned),
                paid_or_organic: enum(paid, organic)}]
  budget:                          # Optional. Total marketing budget for the horizon.
    type: {amount: number, currency: str} | "none"
  horizon: str                     # Optional. Planning window, e.g. "next 90 days". Default 90d.
  available_owners: [str]          # Optional. Who can be assigned steps.
  existing_baselines:              # Optional. Current metric values for target-setting.
    type: {metric_key: value}
  constraints: str                 # Optional. e.g. "no video capacity", "one marketer".
```

## Missing Information Protocol
1. **A required upstream piece is missing** (no CVP, funnel, or channel plan) → do NOT invent it; name the gap and hand off to the skill that produces it, then resume. The plan is only as sound as its inputs.
2. **No objective/target** → ask the founder ONE batched question: "What's the single marketing outcome for this horizon (e.g. leads, first orders, revenue), the number, and the date?" A plan without a target can't be sequenced or measured.
3. **No owners** → assign steps to "founder" by default and flag capacity risk if one person owns everything; recommend where a delegate or contractor is needed.
4. **No baselines** → set targets as directional ("+X% vs. prior" using the source's example-goal style) and label them provisional until `marketing-metrics-tracker` supplies a baseline.
5. **Never assume** budget is available, never schedule a step that depends on an unbuilt asset (e.g. "run ads to landing page" before the page exists), and never bury an approval-gated action inside the plan without flagging it.

## Diagnostic Questions
- What is the ONE objective, its target metric/value, and its date?
- Does every funnel stage (Awareness→Retention) have a message, a tool, a channel, and a defined action?
- What is the critical path — which steps must happen before others (e.g. build landing page → connect tracking → launch ads)?
- Who owns each step, and is any owner overloaded?
- Which steps require budget or approval, and have they been routed?
- What is the success metric and target for each step, and what's the baseline?
- What sequencing removes the most risk early (build + measure before spending)?
- Where does the plan depend on assets that don't exist yet?

## Analysis Framework
Assemble the plan in six passes (the marketing process chain: positioning → funnel → channels → tactics → action → measure):

1. **Anchor on the objective.** State the outcome, target metric, value, and date; every step must trace to it.
2. **Lay the funnel spine.** For each stage, take the {message, tool, action, influence lever} and attach the chosen channel(s). This produces the "what we do at each stage" backbone.
3. **Derive concrete action steps.** Break each stage into discrete, verb-first tasks (build, write, connect, launch, publish, review) — each independently doable.
4. **Sequence by dependency.** Order steps on the critical path: foundational owned assets and measurement first (build landing page, connect analytics), then organic activity, then paid amplification, then retention. Never schedule a step before its prerequisite.
5. **Assign owner, deadline, channel, metric.** Every step gets a single accountable owner, a due date within the horizon, its channel, and a success metric + target (baseline-relative if needed).
6. **Flag risk tier & approval.** Tag each step's risk tier and whether it needs approval (ad spend, public publishing, config changes); route budget to the CFO/runway check. Close with the measure→adapt loop (schedule `marketing-metrics-tracker` reviews).

## Calculations
Largely a sequencing/assembly skill; numeric work is light and defers to siblings.
- **Budget allocation across steps (CLAUDE-DERIVED)** = distribute `budget` across paid steps proportional to expected goal contribution; the sum must not exceed `budget` or trip the runway check. Flagged as a heuristic; CFO validates.
- **Target back-solve (CLAUDE-DERIVED, directional)** — from the objective's target and known funnel conversion rates (from `marketing-metrics-tracker`), estimate the top-of-funnel volume needed (e.g. to get 100 orders at a 2% site conversion, need ~5,000 visits). Used to set per-step targets; labeled an estimate when conversion rates are assumed.
- **Timeline feasibility (SYNTH)** — check that sequenced deadlines fit the horizon and no owner is double-booked past capacity; flag overloads.
- Detailed CAC/LTV/ROAS/engagement computation is NOT done here — it's owned by `marketing-metrics-tracker`; this skill only references its outputs.

## Decision Rules
- **IF** any funnel stage lacks a message, tool, channel, or action **THEN** the plan is incomplete — fill it (via `marketing-funnel-planner` / `channel-selection`) before finalizing. [SOURCE]
- **IF** a step depends on an asset that doesn't exist (landing page, tracking, content) **THEN** schedule the build/prerequisite step first and block the dependent step until it's done. [SYNTH]
- **IF** a step involves **ad spend** **THEN** tag it HIGH risk, mark needs_approval, and route the budget to the CFO/runway check — never schedule it as auto-execute. [POLICY]
- **IF** a step involves **publishing public content or an email blast** **THEN** tag it for founder approval; internal-review/staging steps may be L2. [POLICY]
- **IF** one owner is assigned more than they can deliver in the horizon **THEN** flag the capacity risk and recommend delegation, sequencing relief, or scope cut. [SYNTH]
- **IF** no baseline exists for a step's metric **THEN** set a provisional target and mark it for confirmation once `marketing-metrics-tracker` provides data. [SYNTH]
- **IF** the plan's total spend exceeds budget or threatens runway **THEN** hold and escalate to founder + CFO before committing. [POLICY]
- **IF** the objective, target, or date is missing **THEN** do not produce a plan; request it. [SOURCE]
- **IF** the plan serves multiple personas/segments with different buying behavior **THEN** build a separate track per persona rather than one blended plan. [SOURCE]
- **IF** sequencing puts paid amplification before measurement is in place **THEN** reorder so tracking exists before spend (you must be able to prove ROI). [SYNTH]

## Procedure
1. **Load** the objective, CVP, personas, funnel plan, channel plan, competitive advantage, budget, owners, baselines, constraints.
2. **Validate completeness** — every stage has message/tool/channel/action; if not, hand off to fill the gap and resume.
3. **Anchor** on the objective and its target metric/value/date.
4. **Backbone** — lay the funnel spine with channels attached.
5. **Decompose** each stage into concrete verb-first action steps.
6. **Sequence** by dependency along the critical path (build + measure → organic → paid → retain).
7. **Assign** owner, deadline, channel, and success metric+target to each step; back-solve targets from funnel math where possible.
8. **Risk-tag & route** — flag approval-gated steps (spend, publishing, email blasts, config), route budget to CFO check, flag owner overloads.
9. **Close the loop** — schedule `marketing-metrics-tracker` review checkpoints tied to the objective.
10. **Write back** the dated plan to `strategy`, register/refresh the objective in `goals`, log a decision record; return the plan with a clear separation of what will auto-run vs. what awaits approval.

## Output
```yaml
output:
  objective:
    statement: str
    target_metric: str
    target_value: number
    target_date: date
  positioning_summary: str          # the CVP the plan communicates
  tracks:                           # one per persona/segment
    - persona_id: str
      funnel_backbone:
        - stage: enum(awareness, interest, desire, action, retention)
          message: str
          channel: str
          action: str
          influence_lever: str
  action_plan:
    - step_id: str
      description: str              # verb-first, concrete
      stage: enum(awareness, interest, desire, action, retention)
      channel: str
      owner: str
      start: date
      due: date
      depends_on: [step_id]        # critical-path prerequisites
      success_metric: str
      target: number | "provisional"
      cost: number | 0
      risk_tier: enum(LOW, MEDIUM, HIGH, CRITICAL)
      needs_approval: bool
      approval_reason: str | none
  budget_summary:
    total_planned_spend: number
    within_budget: bool
    runway_check_required: bool
  capacity_flags: [str]            # overloaded owners / feasibility risks
  measurement_checkpoints: [{date: date, review: str}]
  prerequisites_missing: [str]     # upstream gaps that were handed off
  handoffs: [str]
  confidence: enum(low, medium, high)
```

## Recommendations
Steps are sequenced so the plan **de-risks early**: foundational owned assets and measurement first (reversible, low-cost, high-leverage), organic activity next, and paid/irreversible spend last and only once tracking can prove it. Within that, steps are prioritized by contribution to the objective ÷ effort. The plan explicitly separates the auto-runnable/prepared work (drafts, internal tasks, staging) from the approval-gated work (spend, public publishing, email blasts), and names the single first action on the critical path so the founder knows exactly where to start.

## Execution Opportunities
- **Draft and write** the full dated plan to `strategy`; register the objective in `goals` — reversible, L1.
- **Create the action steps as internal tasks** with owners/deadlines/dependencies — reversible, L2 candidate.
- **Schedule** the `marketing-metrics-tracker` review checkpoints — reversible, L2.
- **Prepare** (not launch) briefs for approval-gated steps (ad campaign brief, email-blast draft, publish package) — L1 draft.
- **Route** budget to the CFO/runway check and hand off gap-filling to sibling skills — reversible.

## Human Approval Requirements
- **Any ad spend / paid campaign** in the plan → ALWAYS founder approval + CFO runway check.
- **Publishing public content** (site pages, social posts, PR) → founder approval (via the relevant skill).
- **Email blasts / external communications that commit the company** → founder approval before send.
- **Committing the overall marketing budget** → founder approval; if it threatens runway, CFO sign-off.
- **Changing standing configuration** (integrations, auto-rules) named in a step → founder approval.
- Building the plan, drafting steps/briefs, and creating internal tasks require no approval (L1/analysis).

## Escalation Conditions
- **Total planned spend threatens runway or exceeds budget** → founder + CFO agent before any commitment.
- **Upstream pieces missing or low-confidence** (no real CVP/funnel/channels) → surface to founder; a plan on shaky inputs is flagged, not shipped.
- **Owner capacity infeasible** (one person can't deliver the plan) → founder (hiring/delegation decision → People/CFO).
- **Cross-functional dependency** (needs a pricing/product/legal change) → route to Strategy/CFO/Legal agents.
- **Regulated content/claims** in any step → Legal Liaison before publish.

## KPIs
- **Objective attainment** — did the plan hit its target metric by the target date (the ultimate measure).
- **Plan execution rate** — % of action steps completed on time.
- **Critical-path integrity** — no dependent step launched before its prerequisite (esp. no spend before tracking).
- **Forecast accuracy** — variance between the plan's back-solved targets and actuals (feeds the Learning layer).
- **Budget adherence** — actual spend vs. planned, within runway.

## Monitoring
Track step completion against deadlines and the objective's metric via `marketing-metrics-tracker` at the scheduled checkpoints. Watch for slipping critical-path steps (they cascade), owner overload materializing as missed dates, and spend outpacing plan. Record actual vs. expected outcomes against the decision record so the plan improves next cycle.

## Follow-Up
- **Time-triggered:** rebuild/refresh each quarter with the growth plan; review at each `marketing-metrics-tracker` checkpoint (monthly).
- **Event-triggered:** new offering/segment, a positioning or channel change upstream, or a performance review showing the objective at risk.

## Related Skills
- `customer-value-proposition-builder` — supplies the positioning the plan communicates.
- `marketing-funnel-planner` — supplies the per-stage message/tool/action backbone.
- `channel-selection` — supplies the channels attached to each stage.
- `competitive-advantage-assessment` — supplies the point-of-difference.
- `social-content-planner`, `keyword-and-search-map`, `website-conversion-audit` — execute individual steps the plan schedules.
- `marketing-metrics-tracker` — measures the plan and triggers rebuilds.

## Guardrails
- Never bury an approval-gated action (spend, publishing, email blast) inside the plan without flagging it and routing it.
- Never commit budget or launch spend autonomously; all money and public commitments are founder-approved and runway-checked.
- Never schedule a step before its prerequisite exists (no ads before the landing page, no spend before tracking).
- Do not fabricate upstream inputs; a plan built on missing CVP/funnel/channels is flagged as low-confidence and gaps are handed off.
- Label back-solved targets as estimates until real baselines exist; don't treat provisional misses as failures.
- Flag single-owner overload rather than shipping an infeasible plan; regulated content routes to Legal.

## Example
**Founder input:** "We've nailed the positioning, the funnel, and picked channels for the meal-prep subscription. Build me a 90-day marketing plan to hit 300 paying subscribers by Nov 30. Budget $4,500 total. It's basically just me running things."

**Skill reasoning:**
- Objective: 300 subscribers by 2026-11-30; target_metric = active_subscribers. Baselines from `marketing-metrics-tracker`: site conversion ~2%, ad CAC ~$22. Back-solve: 300 orders ÷ 2% ≈ 15,000 visits needed over 90 days (labeled estimate).
- Validate inputs: CVP ✓, funnel plan ✓ (5 stages with message/tool/action), channel plan ✓ (paid video ads + landing page + email + UGC). Complete.
- Sequence (de-risk early): (1) build/finish landing page (owned) → (2) connect conversion tracking → (3) prepare look-alike seed + ad creative → (4) launch first-box-discount paid video test → (5) email nurture sequence → (6) weekly organic content (via `social-content-planner`) → (7) solicit UGC/reviews (retention/earned) → measurement checkpoints at day 15/30/60/90.
- Budget allocation: ~$3,600 to paid video (the acquisition engine), ~$900 reserve for the winning-ad scale-up; total $4,500 = within budget, runway_check_required = true.
- Capacity: single owner (founder) on all 7 steps over 90 days → **capacity flag**: recommend a contractor for content/creative or stagger organic cadence.

**Output (abridged action_plan):**
- S1 build landing page — owner founder — due day 7 — LOW — no approval.
- S2 connect tracking — due day 8, depends_on S1 — LOW — no approval.
- S3 ad creative + seed — due day 12 — LOW — no approval.
- S4 launch $1,200/mo video test — due day 14, depends_on S1,S2,S3 — **HIGH — needs_approval (ad spend)**, runway check.
- S5 email nurture (draft now, staged) — due day 20 — MEDIUM — email send needs approval.
- S6 weekly content via social-content-planner — ongoing — L2 internal-review, public publish needs approval.
- S7 UGC/review solicitation — from day 30 — LOW.
- measurement_checkpoints: day 15/30/60/90 via `marketing-metrics-tracker`.

**Executed vs. approval:** The skill wrote the dated plan to `strategy`, registered the 300-subscriber goal in `goals`, created steps S1–S3, S5-draft, S7 as internal tasks, scheduled the tracker checkpoints, and prepared the S4 ad brief — all at L1/L2, no approval. The **paid ad launch (S4), the email nurture sends (S5), all public content publishing (S6), and committing the $4,500 budget were held for founder approval + CFO runway check**. The single-owner **capacity risk was flagged** with a recommendation to delegate content.

## Provenance
**SOURCE.** Derived from the Marketing & Customer domain knowledge (the end-to-end marketing process chain — positioning → funnel → channels → tactics → conversion; the Marketing & Communication Plan {message, tool, action} funnel structure with influence levers; the "separate persona/CVP/funnel per distinct segment" rule; the Marketing Action Plan worksheet — concrete action steps each with a deadline). The budget-allocation and target-back-solve heuristics, timeline-feasibility check, and the deferral of CAC/ROAS computation to the metrics tracker are **CLAUDE-DERIVED/SYNTH** and flagged inline. See internal/PROVENANCE_MAP.md.
