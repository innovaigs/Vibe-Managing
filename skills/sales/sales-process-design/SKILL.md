---
name: sales-process-design
domain: sales
version: 0.1.0
autonomy_ceiling: L1
provenance: CLAUDE
reads: [company, customers, offerings, buyers_journey, personas, cvp, competitive_advantage, metrics, team, goals]
writes: [sales, metrics, decisions, tasks]
related_skills: [pipeline-and-forecast-review, proposal-builder, negotiation-preparation, map-buyers-journey, build-marketing-funnel-plan, craft-cvp]
owned_by_agents: [orchestrator, sales-agent]
---

# Skill: Sales Process Design

## Purpose
Turn ad-hoc, founder-in-the-head selling into a repeatable, measurable pipeline: a named set of stages, an explicit exit criterion for each stage, a defined next action, conversion targets, and the KPIs that tell the founder whether the process is working. This is the backbone every other sales capability (pipeline review, proposal builder, negotiation prep) plugs into — without it there is nothing to forecast, diagnose, or improve.

## When to Use
- The founder is selling but has no defined pipeline: "I just talk to people until they buy," "deals live in my head / a messy spreadsheet."
- Deals stall unpredictably and no one can say why or at which point.
- The founder is about to hire a first salesperson or hand selling to someone else and needs a process to teach.
- Revenue is inconsistent and the founder wants to know which stage leaks.
- Example founder phrasings: "Help me build a sales pipeline," "What stages should my deals go through?", "I want a repeatable sales process," "Set up my CRM stages," "How do I know if a deal is real?"

## When NOT to Use
- The founder wants to diagnose an EXISTING pipeline's coverage/conversion or build a forecast → use `pipeline-and-forecast-review`.
- The founder needs to draft a specific customer proposal → use `proposal-builder`.
- The founder is preparing for a specific negotiation → use `negotiation-preparation`.
- The upstream marketing funnel (Awareness→Retention, message/tool/action per stage) is undefined → run `build-marketing-funnel-plan` and `map-buyers-journey` first; sales process design begins where the marketing funnel hands off a qualified lead.
- There is no defined customer/CVP yet → run `craft-cvp` first; you cannot design a sales process without knowing who you sell to and why they buy.

## Required Context
Reads Business Memory: `company` (business model B2C/B2B/B2G, stage, avg deal size, sales-cycle length if known), `customers` (segments, active count), `offerings` (products/services, price points, margin), `buyers_journey` (the 5-stage map from `map-buyers-journey`), `personas` (buying center roles — who initiates/decides/gatekeeps), `cvp` (value proposition and point-of-difference to arm reps with), `competitive_advantage` (differentiation to use at the evaluation stage), `metrics` (any existing win rate, cycle time), `team` (who sells today, capacity), `goals` (revenue target, quota). Each fact carries `source`, `confidence`, `as_of`; treat stale cycle-time or win-rate data as low-confidence and flag it.

The sales process is the seller-side operational mirror of the buyer's journey (Need Recognition → Info Search → Evaluation → Purchase → Post-Purchase) and the marketing funnel (Awareness → Interest → Desire → Action → Retention). B2B/B2G buyers add Product Specification and RFP steps — the process must reflect that.

## Inputs
```yaml
input:
  business_model: enum(B2C, B2B, B2G, mixed)
  offering:
    name: str
    avg_deal_value: number            # average contract / order value
    gross_margin_pct: number
  buyers_journey:                      # from map-buyers-journey (may be partial)
    stages: [ {name: str, buyer_question: str, buyer_behavior: str} ]
  buying_center:                       # from personas; who is involved in the decision
    roles: [ {role: enum(initiator,user,decision_maker,influencer,buyer,gatekeeper), who: str} ]
  current_state:
    has_defined_pipeline: bool
    existing_stages: [str]             # if any
    known_win_rate_pct: number         # optional, overall lead→close
    known_cycle_days: int              # optional, first-touch→close
    lead_sources: [str]                # where qualified leads come from (from marketing funnel)
  volume:
    leads_per_month: int               # qualified leads entering the pipeline
    revenue_target: number             # over a stated horizon
    target_horizon_months: int
  sales_capacity:
    sellers: int                       # people who can carry deals (incl. founder)
    selling_hours_per_week: number     # realistic capacity
  crm_in_use: str                      # tool name or "none" (generalized to function)
```

## Missing Information Protocol
1. Prefer to derive stages from the existing `buyers_journey` map and `buying_center` in memory before asking anything.
2. If `known_win_rate_pct` / `known_cycle_days` are absent, do NOT invent them — design the process with target (not historical) conversion rates, label them `target/assumed`, and note that `pipeline-and-forecast-review` will replace them with observed rates once data accrues.
3. If `business_model` is unknown, ask ONE question — it changes whether Product-Spec/RFP stages are added.
4. Batch at most one concise question set covering the highest-leverage gaps (typically: model, avg deal value, leads/month, revenue target).
5. Never assume avg deal value, margin, or revenue target — these size the whole process and any fabricated number misleads capacity and quota math.

## Diagnostic Questions
Answered internally to design well:
- What does the buyer actually do at each journey stage, and what must be TRUE for a deal to legitimately move to the next stage (the exit criterion)? A stage without an exit criterion is a wish, not a stage.
- Who in the buying center must be engaged before a deal can close (especially the decision-maker and gatekeeper in B2B/B2G)?
- Is this a transactional (short, few-touch) or complex (long, multi-stakeholder, RFP) sale? That sets the number of stages.
- Where does marketing hand off — what makes a lead "qualified" enough to enter stage 1?
- What is the single most likely leak point given the buyer's behavior (often Info Search→Evaluation, i.e., getting a real evaluation, or Evaluation→Purchase, i.e., closing)?
- Does the founder have the capacity to work the volume implied by the revenue target and the conversion math? If not, the process must flag a capacity gap.
- What defines a WON deal vs. a LOST deal vs. a DISqualified deal (removed, not lost)?

## Analysis Framework
A five-step design method:

**1. Map stages to the buyer's journey.** Each sales stage is the seller's action that helps the buyer complete one journey step. Baseline stage set (adapt to model):

| # | Sales stage | Mirrors buyer's-journey / funnel | Seller's job |
|---|---|---|---|
| 0 | **Lead (qualified)** | Awareness→Interest handoff | Confirm fit vs. ICP; entry gate |
| 1 | **Discovery / Qualify** | Info Search / Interest | Understand need, budget, authority, timing |
| 2 | **Solution / Demo** | Evaluation of Alternatives / Desire | Show fit, competitive advantage, proof |
| 3 | **Proposal / Quote** | Evaluation→Purchase | Put price + terms in writing (→ `proposal-builder`) |
| 4 | **Negotiation** | Purchase | Align on price/terms (→ `negotiation-preparation`) |
| 5 | **Closed-Won / Closed-Lost** | Action | Commitment recorded; onboarding trigger |
| 6 | **Onboard / Retain** | Post-Purchase / Retention | Deliver, seed referrals & renewals |

For **B2B/B2G**, insert **Requirements / Spec** (buyer's "Determine Product Specification") between Discovery and Solution, and treat **RFP response** as a formal variant of Proposal. For simple **B2C/transactional** sales, collapse Discovery+Solution and Proposal+Negotiation to keep it to ~3 stages — do not over-engineer.

**2. Define exit criteria (the heart of the design).** For each stage write the objective, verifiable condition that must be met to advance — expressed as evidence, not feeling. Exit criteria prevent "happy-ears" pipeline inflation. Qualification is anchored on the classic dimensions: **Need, Budget, Authority (decision-maker engaged), Timing** (and Fit vs. ICP at entry).

**3. Set the next action + owner + SLA per stage.** Every stage names the one action that moves the deal, who does it, and a max time-in-stage before the deal is flagged stale.

**4. Set conversion targets per stage transition.** Either observed (if data exists) or target rates. These feed the volume/capacity math and later the forecast.

**5. Define KPIs + won/lost/disqualify rules.** Name the metrics that reveal health, and the exact definitions of Won, Lost, and Disqualified so the pipeline stays honest.

## Calculations
Let `L` = qualified leads/month, `cᵢ` = conversion rate of stage transition i, `V` = avg deal value, `M` = gross margin %.

- **Overall lead→close conversion (win rate)** = product of every stage conversion `c₁ × c₂ × … × cₙ`. [CLAUDE-DERIVED]
- **Expected new customers / month** = `L × overall_conversion`. [CLAUDE-DERIVED]
- **Expected new bookings / month** = `L × overall_conversion × V`. [CLAUDE-DERIVED]
- **Leads required to hit target** = `revenue_target ÷ (target_horizon_months × overall_conversion × V)` per month. Reveals whether the top of funnel is big enough. [CLAUDE-DERIVED]
- **Pipeline coverage needed** = `(revenue_target / horizon) ÷ overall_conversion` = open pipeline value required at any time to expect the target (commonly 3×–5× of target when win rate is 20–33%). Handed to `pipeline-and-forecast-review`. [CLAUDE-DERIVED]
- **Sales capacity check** = `sellers × selling_hours_per_week × 4.3 ÷ hours_per_deal_touch` vs. deals in flight; if demand > capacity, flag capacity gap. [CLAUDE-DERIVED]
- **Sales cycle length** = median days first-touch → Closed-Won (observed) or sum of per-stage SLA targets (planned). [CLAUDE-DERIVED]
- **Stage conversion benchmark bands (targets, not guarantees):** Discovery→Solution 50–70%; Solution→Proposal 50–60%; Proposal→Negotiation 60–80%; Negotiation→Won 60–80%; overall lead→won commonly 15–33% for considered B2B sales. Bands are CLAUDE-DERIVED planning defaults — replace with observed rates as soon as `pipeline-and-forecast-review` produces them.

## Decision Rules
- **IF** business_model is B2B or B2G **THEN** add a Requirements/Spec stage and an RFP variant of Proposal, and require the decision-maker AND gatekeeper to be identified before Proposal. [buying-center]
- **IF** the sale is transactional / low deal value (short cycle, single buyer) **THEN** collapse to ≤3 stages; do NOT impose a 6-stage process — process weight should match deal complexity.
- **IF** a proposed stage has no objective exit criterion **THEN** it is not a valid stage; merge it or define the criterion before finalizing.
- **IF** the decision-maker (Authority) is not engaged **THEN** the deal cannot pass Discovery/Qualify — hold it, regardless of enthusiasm from a non-decider.
- **IF** Budget or Timing is unknown at Qualify **THEN** the deal stays in Qualify (or is Disqualified), not advanced on optimism.
- **IF** leads_required_to_hit_target > leads_per_month **THEN** flag a top-of-funnel gap and route to marketing (`build-marketing-funnel-plan` / `select-channels`).
- **IF** demand implied by target > sales_capacity **THEN** flag a capacity gap (hire, tooling, or lower target) — surface to founder, do not silently assume more hours.
- **IF** a deal exceeds its stage SLA (time-in-stage) **THEN** mark it stale for the next pipeline review; stalls are the primary forecast risk.
- **IF** overall_conversion is only a target (no history) **THEN** label the whole forecast `assumed` and schedule a re-calibration after N closed deals.
- **IF** win rate < 15% at the same stage repeatedly **THEN** the leak is upstream (qualification too loose) — tighten stage-0/1 exit criteria before adding more leads.
- **IF** a lost deal was never truly qualified **THEN** classify it Disqualified, not Lost, so win-rate math is not distorted.

## Procedure
1. Load `buyers_journey`, `buying_center`, `cvp`, `competitive_advantage`, `offering`, and any existing pipeline/metrics from memory.
2. Choose the stage set: baseline 6-stage, expanded for B2B/B2G (add Spec/RFP), or collapsed for transactional. Justify the count against deal complexity.
3. For each stage write: **exit criterion** (objective evidence), **next action**, **owner**, **time-in-stage SLA**, and the **Vibe Managing skill it hands off to** (Proposal→`proposal-builder`, Negotiation→`negotiation-preparation`).
4. Define entry qualification (Fit/ICP + Need/Budget/Authority/Timing) and the Won / Lost / Disqualified definitions.
5. Assign conversion targets per transition (observed if available, else target bands, labeled).
6. Run the volume/capacity math (leads required, pipeline coverage, capacity check); flag top-of-funnel or capacity gaps.
7. Select KPIs and set their target/warning thresholds.
8. Map the process to the CRM/tool in use (as stage fields + required fields per stage), generalized to function if no tool named.
9. Assemble output: stage table, KPI set, conversion plan, gaps, CRM mapping.
10. Write the process definition to `sales`, a decision record to `decisions`, and draft internal setup tasks — all at L1 (prepared, shown for approval). Propose (do not auto-run) `pipeline-and-forecast-review` once real deals populate the stages.

## Output
```yaml
output:
  business_model: enum(B2C, B2B, B2G, mixed)
  process_name: str
  stages:
    - order: int
      name: str
      mirrors_journey_stage: str
      entry_condition: str
      exit_criterion: str              # objective, verifiable
      next_action: str
      owner: str
      time_in_stage_sla_days: int
      required_fields: [str]           # what must be captured to advance
      hands_off_to_skill: str          # or "none"
  qualification_model:
    entry_fit_criteria: [str]          # ICP fit
    dimensions: [Need, Budget, Authority, Timing]
  outcome_definitions:
    won: str
    lost: str
    disqualified: str
  conversion_plan:
    - transition: str                  # e.g. "Discovery→Solution"
      target_rate_pct: number
      basis: enum(observed, target_assumed)
    overall_conversion_pct: number
    overall_basis: enum(observed, target_assumed)
  volume_math:
    leads_per_month: int
    expected_new_customers_per_month: number
    expected_bookings_per_month: number
    leads_required_for_target: number
    pipeline_coverage_multiple_needed: number
  gaps:
    - type: enum(top_of_funnel, capacity, qualification, data)
      detail: str
      recommended_skill: str
  kpis: [ {name: str, definition: str, target: number, warning: number} ]
  crm_mapping:
    tool_function: str
    stage_fields: [str]
    required_fields_by_stage: object
  confidence: enum(high, medium, low)  # low if conversion rates are assumed
```

## Recommendations
Recommendations are ordered by leverage: (1) fix the biggest structural leak (usually qualification exit criteria) before adding volume; (2) close any top-of-funnel or capacity gap that makes the revenue target arithmetically impossible; (3) instrument the KPIs so the next review has real data. Each recommendation names the exact next skill and the one-line reason. Effort/reversibility are noted — defining stages is reversible and cheap; hiring to close a capacity gap is not and routes to the founder + `resource-gap-analysis`.

## Execution Opportunities
- Write the sales-process definition to `sales` and a decision record to `decisions` — reversible, LOW risk (prepared at L1 ceiling).
- Draft internal setup tasks: configure CRM stages, add required fields, create stage checklists — reversible, LOW.
- Draft internal enablement notes (per-stage talk track referencing the CVP and competitive advantage) — reversible, LOW.
- Schedule the first `pipeline-and-forecast-review` as an internal reminder once N deals exist — reversible, LOW.
This skill designs and instruments the process; it never contacts customers, sends anything external, or commits pricing.

## Human Approval Requirements
- No external or irreversible action. All artifacts (process definition, CRM config tasks, enablement notes) are prepared at L1 and shown to the founder before anything is written to a live CRM or shared with a hired seller.
- Any downstream action that touches a customer (proposal send, quote, negotiation commitment, contract) carries its own approval requirement in its skill — this skill only defines WHERE those approvals sit in the flow. Per `AUTONOMY_AND_APPROVAL_MODEL.md`, sending proposals/quotes, committing pricing/terms, external customer communication, and signing contracts ALWAYS require founder approval.
- If the design implies hiring or spending (to close a capacity gap), that is founder-approved and routed to the relevant skill — never assumed.

## Escalation Conditions
- **Revenue target arithmetically impossible** with current leads × conversion × deal value and no feasible fix → escalate to founder (reset target, or fund demand-gen/hiring).
- **Capacity gap** (demand > seller hours) → founder + `resource-gap-analysis`.
- **Pervasive low-confidence data** (no historical win rate/cycle) → surface that the process runs on assumptions until calibrated; do not present assumed rates as fact.
- **Model/legal structure of the sale unclear** (e.g., government procurement rules, regulated product) → route to appropriate specialist; do not design compliance steps as if advice.

## KPIs
This skill's own success is measured by whether the process it produces is adopted and improves selling:
- Adoption: % of deals actually tracked through the defined stages within one cycle.
- Forecast readiness: whether `pipeline-and-forecast-review` can run on the resulting data.
- Leak visibility: whether the founder can now name the lowest-converting stage (previously unknown).
- Cycle-time and win-rate trend after adoption (improvement over the pre-process baseline).

## Monitoring
After adoption: watch stage conversion rates vs. targets, time-in-stage vs. SLA (stall detection), win/loss/disqualify mix, and whether required fields are actually captured. Re-calibrate conversion targets from observed data after the first cohort of closed deals. Watch for "stage skipping" (deals jumping stages) which signals the process is being bypassed.

## Follow-Up
- Event-triggered: re-run when the business model changes, a new offering with a different sales motion launches, the first salesperson is hired, or average deal size shifts materially.
- Time-triggered: revisit quarterly; re-calibrate conversion targets from observed data at each `pipeline-and-forecast-review`.

## Related Skills
Feeds and is fed by: `map-buyers-journey` and `build-marketing-funnel-plan` (upstream inputs), `pipeline-and-forecast-review` (consumes the stages/conversions), `proposal-builder` and `negotiation-preparation` (invoked at their stages), `craft-cvp` and `assess-competitive-advantage` (arm the enablement content), `resource-gap-analysis` (capacity gaps).

## Guardrails
- A stage without an objective exit criterion is not allowed — it reintroduces happy-ears forecasting.
- Never present assumed/target conversion rates as if observed; always label the basis and confidence.
- Do not over-engineer: process complexity must match deal complexity, or reps will abandon it.
- Never fabricate deal value, margin, cycle time, or win rate — mark data gaps and design against targets flagged as assumed.
- This skill defines process only; it must not itself send customer communications, commit pricing, or bypass the approval gates it places into the flow.
- Keep individual-seller performance data out of any shared enablement artifact beyond aggregate targets.

## Example
**Founder input:** "I sell a $12k done-for-you onboarding service to mid-size B2B companies. Deals are all in my head. About 20 qualified leads a month come in from webinars. I want $600k in the next 12 months. How should my pipeline work?"

**Reasoning:**
- Model = B2B, considered purchase, one clear decision-maker + a gatekeeper (ops manager) → use the expanded stage set with a Requirements/Spec step.
- No historical win rate → use target bands, labeled assumed. Assume overall lead→won 20%.
- Volume math: revenue_target $600k / 12 = $50k/mo needed. Per deal $12k. Deals/mo needed = 50k/12k ≈ 4.2. Leads/mo needed = 4.2 / 0.20 ≈ 21. Founder has ~20 → essentially at the edge; top-of-funnel is the binding constraint, flag it. Pipeline coverage needed ≈ $50k / 0.20 = $250k open pipeline at any time (~5×).
- Capacity: ~4 deals closing/mo plus discovery/demo load on a solo founder → flag likely capacity gap before hiring.

**Output (abridged):** 6 stages — Lead(qualified) → Discovery/Qualify (exit: Need+Budget confirmed, decision-maker on a call) → Requirements/Spec (exit: written scope agreed) → Solution/Demo (exit: buyer confirms fit vs. 2 named competitors) → Proposal (exit: written proposal delivered → `proposal-builder`) → Negotiation (→ `negotiation-preparation`) → Closed-Won → Onboard/Retain. Conversion plan target 20% overall (assumed). Gaps: top_of_funnel (need ~21 leads/mo, have 20 → route to `select-channels`); capacity (solo founder near ceiling → `resource-gap-analysis`). KPIs: stage conversion, time-in-stage SLA (Discovery 7d, Proposal 5d), win rate, cycle time, pipeline coverage ≥5×.

**Executed vs. approval:** Wrote the process definition to `sales`, drafted CRM stage-config tasks and per-stage enablement notes at L1 for founder approval. No customer contacted; no pricing committed. Proposed running `pipeline-and-forecast-review` after the first 10 deals populate the stages.

## Provenance
CLAUDE. The stage/exit-criterion/KPI machinery, the Need-Budget-Authority-Timing qualification model, the conversion-chain and pipeline-coverage math, and the benchmark bands are CLAUDE-DERIVED standard sales-operations practice, explicitly built ON TOP OF the SOURCE-DERIVED buyer's-journey and marketing-funnel frameworks from the Marketing & Customer domain (Need Recognition→Post-Purchase; Awareness→Retention; B2B/B2G Product-Spec + RFP steps; buying-center roles). CLAUDE-derived numeric bands are planning defaults to be replaced by observed data. See `internal/PROVENANCE_MAP.md`.
