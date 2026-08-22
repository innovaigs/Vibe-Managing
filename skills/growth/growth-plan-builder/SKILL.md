---
name: growth-plan-builder
domain: growth
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [company, founders, customers, offerings, finance, team, operations, market, strategy, metrics, goals, risks]
writes: [strategy, goals, metrics, decisions]
related_skills: [kpi-design, executive-dashboard-builder, growth-pitch-generator, monthly-business-review, initiative-prioritization, resource-gap-analysis, opportunity-feasibility-analysis, financial-forecast-builder]
owned_by_agents: [growth-agent]
---

# Skill: Growth Plan Builder

## Purpose
Assemble the company's end-to-end growth plan into a single living document by pulling the already-produced outputs of the Foundation, Finance, Go-To-Market, and Operations skills into one coherent, ordered narrative — with the Executive Summary written last and the monitoring dashboard threaded throughout. This gives the founder one authoritative artifact that says where the business is now, where it is going, why the plan will work, and how success is measured.

## When to Use
- The founder asks to "put the whole growth plan together," "assemble my plan," "write up my growth strategy," or "I have all the pieces, make it one document."
- Enough upstream analysis exists (opportunity, feasibility, resources, risks, forecast, GTM, org, operations) that the job is now composition and reconciliation rather than net-new analysis.
- Quarterly growth-plan refresh cycle is due, or the founder needs a plan version for a specific audience (e.g., a lending/financing conversation).

## When NOT to Use
- The underlying analysis does not yet exist. Do not fabricate sections. Route to the producing skill first: `opportunity-feasibility-analysis`, `resource-gap-analysis`, `initiative-prioritization`, `financial-forecast-builder`, GTM/marketing skills, `operations` skills.
- The founder only wants the compressed 3-point pitch, not the full document → use `growth-pitch-generator`.
- The founder wants to run the monthly forecast-vs-actual loop → use `monthly-business-review`.
- The founder wants only the metric matrix → use `executive-dashboard-builder`.

## Required Context
Before assembling, the following must exist in Business Memory or be supplied as skill outputs:
- `company` — legal structure, business model, revenue model, stage, locations, mission/vision/values.
- `strategy` — the Opportunity Statement and its feasibility verdict; growth pathway; prioritized initiative roadmap; competitive mapping.
- `finance` — the multi-year forecast (P&L, balance sheet, cash flow) and the ~5 chosen financial key metrics; the 5 critical forecast assumptions with confidence levels.
- `customers` / `offerings` — personas, buyer's journey, CVP, marketing & communication plan.
- `team` / `operations` — organizational development plan and operational audit summary.
- `risks` — the scored risk register with warning-signal metrics and owners.
- `goals` — the 3 Success Factors, 3 Progress Metrics, 3 dated Next Steps.

## Inputs
```yaml
input:
  as_of: date                      # plan preparation date
  audience: enum(internal, financing, board, general)   # tailors Executive Summary emphasis
  foundation:
    business_story: text           # origin, purpose, products, structure, pivotal decisions, mission
    resource_map: object           # 6 classes x (have/need/action step)
    risk_register: list            # [{risk, score_1_10, mitigation, owner, deadline, warning_signal_metric}]
    social_value: text|null        # where social responsibility is a competitive advantage; optional profit-commitment %
  growth:
    opportunity_statement: text     # the EEC north-star sentence
    feasibility_summary: object     # go/no-go across 6 dimensions
    competitive_mapping: list       # current + aspirational competitors
  finance:
    forecast_summary: text          # narrative of the multi-year forecast
    key_metrics: list               # [{metric, definition, what_it_tells, link_to_success}] (~5)
    key_assumptions: list           # [{assumption, why_critical, source, confidence, better_data_plan}] (5)
  gtm:
    buyers_journey: object
    persona: object
    cvp: text
    marketing_comm_plan: list       # funnel stage x tool x influence element x target volume
    digital_social: object|null
  people_ops:
    org_dev_plan: object            # need/have/fit/gap/fill-plan/timetable/challenge
    operational_audit_summary: text
  execution:
    exit_strategy: object|null      # chosen exit + how plan enables it + tracking metrics
    success_factors: list           # exactly 3
    progress_metrics: list          # exactly 3
    next_steps: list                # exactly 3, each with a deadline
  dashboard_metrics: object|null    # existing YOU/BUSINESS/ENVIRONMENT matrix if already built
```

## Missing Information Protocol
1. Attempt to read each missing piece from Business Memory / the corresponding twin view (e.g., `cash-runway`, `profitability-map` for the forecast narrative).
2. If a whole section's producing analysis is absent, do NOT invent it. Mark the section `STATUS: not ready — run <skill>` in the assembled document and list it in a single consolidated gap notice.
3. Only after exhausting fetch/compute, ask the founder ONE batched question listing every genuinely missing input.
4. Never assume: financial figures, the go/no-go verdict, risk scores, ownership of initiatives, or any deadline. These must come from source outputs or the founder.

## Diagnostic Questions
- Is there exactly one Opportunity Statement anchoring the plan, and did it pass all six feasibility gates?
- Do the forecast, the initiative roadmap, and the Next Steps all point at the same opportunity (internal consistency)?
- Does every low-confidence assumption have a validation task somewhere in the plan?
- Does every top risk carry an owner, a deadline, and a warning-signal metric wired to the dashboard?
- Are there exactly 3 Success Factors, 3 Progress Metrics, and 3 dated Next Steps?
- Does the dashboard cover all three domains (YOU / BUSINESS / ENVIRONMENT) and both leading and lagging indicators?

## Analysis Framework
Assemble in the canonical section order; write the Executive Summary last; keep the dashboard as a living backbone.

1. **Cover / Metadata** — confidentiality marker, company name, "prepared [Month Year]", owner + contact.
2. **Orientation — Dashboard & Metrics** — placeholder for the YOU / BUSINESS / ENVIRONMENT matrix; populated incrementally as each later section deposits candidate metrics (delegate assembly to `executive-dashboard-builder`).
3. **Foundation — You & Your Business** — business story (as narrative, not Q&A), resource map (have/need/action across 6 classes), risk assessment (top 4–5 risks with score/mitigation/owner/deadline/warning-signal), social value/purpose.
4. **Growth & Opportunities** — opportunity pre-work synthesis, the Opportunity Statement, feasibility assessment across the 6 dimensions, feasibility go/no-go summary, competitive mapping (current + aspirational).
5. **Money & Metrics** — the 5 critical forecasting assumptions with confidence and better-data plans.
6. **Leadership** — leadership development, 3 personal metrics (→ YOU column), vision plan (mission/vision/values + 3 implementation actions).
7. **People / Organization** — organizational audit summary, organizational development plan, org-change summary.
8. **Marketing & Selling** — buyer's journey, persona, competitive advantage, CVP, marketing & communication plan by funnel stage, digital/website, social media strategy.
9. **Operations & Processes** — operational audit, operational-change summary.
10. **Being Bankable (Financials)** — forecast summary & analysis narrative, financial key metrics (~5).
11. **Action for Growth** — exit strategy (if any), and the execution triad: 3 Success Factors, 3 Progress Metrics, 3 dated Next Steps.
12. **Appendices** — forecasted statements (P&L, balance sheet, cash flow), reflection notes per section.
13. **Executive Summary (written LAST)** — synthesize the whole: current state → target state → why it will succeed → key financial + operational success metrics; tailored to `audience`.

Cross-section reconciliation pass: verify the opportunity, forecast, initiatives, risks, and next steps are mutually consistent before finalizing.

## Calculations
This skill composes rather than computes; it validates figures produced upstream. Cross-checks it performs:
- **Internal consistency check** — forecast revenue trajectory should reflect the chosen initiatives' expected impact; flag if Next Steps imply activity absent from the forecast.
- **Completeness ratio** = sections ready / total sections; surfaced in the gap notice.
- **Execution-readiness check** per initiative/next-step: has owner AND deadline AND metric? (all three required).
For all financial formulas (margins, runway, CAGR, Rule of 40, LTV:CAC), defer to the source figures from `financial-forecast-builder` / `kpi-design`; do not recompute silently.

## Decision Rules
- IF the Opportunity Statement is missing OR its feasibility verdict is not "go" THEN block assembly of the full plan and surface the feasibility gap (a plan without a validated opportunity is not a plan).
- IF a section's producing analysis is absent THEN mark it `not ready — run <skill>` and include it in the consolidated gap notice; do not fabricate content.
- IF an initiative or Next Step lacks owner, deadline, OR metric THEN mark it not-execution-ready and exclude it from the committed plan until completed.
- IF Success Factors ≠ 3 OR Progress Metrics ≠ 3 OR Next Steps ≠ 3 THEN flag the execution triad as malformed and request correction.
- IF a forecast assumption has low confidence AND has no validation task THEN auto-add a validation task to Next Steps candidates and flag for founder review.
- IF the forecast and the initiative roadmap are inconsistent (e.g., revenue growth with no demand-gen initiative) THEN raise an internal-consistency warning to the founder.
- IF `audience == financing` THEN emphasize bankability metrics, cash runway, debt-service capacity, and the forecast's evidentiary basis in the Executive Summary.

## Procedure
1. Load all upstream outputs from Business Memory / twin views; record provenance and freshness for each.
2. Run the data-completeness pass; build the consolidated gap notice.
3. If the opportunity/feasibility gate fails, stop and surface it.
4. Assemble sections 0–11 in canonical order, inserting `not ready` markers where applicable.
5. Delegate dashboard assembly to `executive-dashboard-builder`; embed the returned YOU/BUSINESS/ENVIRONMENT matrix in Section 2.
6. Run the cross-section reconciliation and execution-readiness checks; attach warnings.
7. Write the Executive Summary last, tailored to `audience`.
8. Emit the assembled plan as a draft (L1) with the gap notice, consistency warnings, and a change list; hold for founder review.
9. On founder approval, write plan metadata, the execution triad, and chosen metrics back to `strategy`/`goals`/`metrics`, and log a decision record.

## Output
```yaml
output:
  growth_plan:
    metadata: {company, prepared: date, owner, audience, confidentiality}
    executive_summary: text          # written last
    sections:                        # ordered, canonical
      - {id, title, status: enum(ready, not_ready), content, source_skill, provenance, as_of}
    dashboard_ref: id                # link to executive-dashboard-builder output
    execution_triad:
      success_factors: [str, str, str]
      progress_metrics: [str, str, str]
      next_steps: [{step, owner, deadline}, {..}, {..}]
    appendices: {pnl_ref, balance_sheet_ref, cash_flow_ref}
  quality:
    completeness_ratio: number       # sections ready / total
    gap_notice: [ {section, missing, run_skill} ]
    consistency_warnings: [str]
    not_execution_ready: [str]
  provenance_map: [ {section, source, confidence, as_of} ]
```

## Recommendations
Recommendations are surfaced as the gap notice and consistency warnings, ordered by blocking severity: (1) hard blockers (missing opportunity/feasibility), (2) execution-readiness failures (missing owner/deadline/metric), (3) internal-consistency mismatches, (4) freshness/low-confidence flags. Each item names the exact producing skill or the specific founder decision required, so the path to a complete plan is unambiguous.

## Execution Opportunities
- Assemble the draft plan document (reversible, LOW) — automatable at L1 (draft only).
- Create internal tasks for each `not ready` section and each low-confidence assumption validation (reversible, LOW).
- Update the internal dashboard / plan record after founder approval (reversible, LOW).
- Draft a financing-audience version of the Executive Summary (reversible, LOW) — content only; any external sharing is a separate approved action.

## Human Approval Requirements
- Finalizing/publishing the plan as the company's committed plan requires founder approval.
- Any public or external commitment derived from the plan (targets shared with lenders, customers, staff, or partners) requires founder approval before it leaves the system.
- Writing the execution triad and chosen metrics back to Business Memory as authoritative requires founder confirmation.
- Analysis, drafting, and internal task creation proceed at L1 without external commitment. Complies with AUTONOMY_AND_APPROVAL_MODEL.md.

## Escalation Conditions
- Feasibility verdict is not "go," or the opportunity is undefined → founder (strategic decision).
- Forecast and strategy are materially inconsistent and cannot be reconciled from available data → founder (+ CFO agent / accountant).
- Financing-audience plan implies commitments beyond confirmed capacity → founder (+ accountant).
- Low confidence in core inputs (stale forecast, unvalidated assumptions) → surface uncertainty, do not present as settled.

## KPIs
- Completeness ratio at first assembly and at approval.
- Number of consistency warnings resolved before finalization.
- Founder edit/override rate on the assembled draft (lower over time = better assembly).
- Time from "assemble" request to founder-approved plan.
- Downstream: does the plan feed a clean monthly-business-review (no missing baselines)?

## Monitoring
After the plan is approved, watch: whether Next-Step deadlines are met, whether the forecast tracks actuals in `monthly-business-review`, whether any risk warning-signal trips, and whether assumptions flagged low-confidence get validated. Trigger a refresh when any of these drift.

## Follow-Up
- Quarterly growth-plan refresh (time-triggered).
- Event-triggered rebuild when: the opportunity changes, the forecast is materially revised, a top risk materializes, or ≥2 consecutive monthly reviews show the same assumption wrong.

## Related Skills
Calls/hands off to: `executive-dashboard-builder` (Section 2), `kpi-design` (metric selection), `financial-forecast-builder` (Section 10 + appendices), `initiative-prioritization` and `resource-gap-analysis` (Section 4 roadmap), `opportunity-feasibility-analysis` (Section 4 gate), `growth-pitch-generator` (compressed output), `monthly-business-review` (downstream learning loop).

## Guardrails
- Never fabricate financials, risk scores, verdicts, owners, or deadlines — mark them missing instead.
- Preserve provenance and freshness on every section; flag stale inputs rather than presenting them as current.
- Respect sensitivity tiers: restricted data (individual compensation, employee performance) is summarized, not exposed, in any audience version.
- A financing-audience version is a factual restatement, never an optimistic re-forecast; do not adjust numbers to suit an audience.
- The assembled draft is a proposal, not a commitment, until the founder approves it.

## Example
**Founder input:** "I've done the feasibility work, the forecast, and the GTM plan — put my growth plan together for a bank conversation."

**Skill reasoning:**
- Loads outputs: Opportunity Statement present, feasibility = "go" across all 6 dimensions. Forecast present (5-year P&L/BS/CF) with 5 key metrics and 5 assumptions (2 flagged low-confidence). GTM plan present. Operations audit summary present. Risk register present (5 risks, all with owners/deadlines/warning-signals). Execution triad present but only 2 Next Steps carry deadlines.
- Data-completeness pass: org development plan is missing → marks Section 7 `not ready — run org-development skill`. Completeness ratio 11/12.
- Execution-readiness: one Next Step lacks a deadline → flagged not-execution-ready.
- Low-confidence assumptions have no validation tasks → auto-adds two validation tasks to Next-Steps candidates.
- Assembles sections in order; delegates dashboard to `executive-dashboard-builder`; writes the Executive Summary last with `audience: financing` emphasis (runway, debt-service capacity, evidentiary basis for revenue).

**Output (abridged):** Full ordered plan draft + Executive Summary (financing-tuned); gap notice = [org development plan]; not_execution_ready = [Next Step 3 missing deadline]; consistency warnings = [none]; two new validation tasks proposed.

**Executed vs. approval:** Draft document, internal validation tasks, and dashboard embed executed at L1. Publishing the plan as the committed/financing version and sharing any figures with the bank held for founder approval.

## Provenance
SOURCE — derived from the Growth Execution domain knowledge (`09-growth-execution.md`): the end-to-end Growth Plan Template section order, the "Executive Summary written last / Dashboard updated continuously" rule, and the execution-triad (3 Success Factors / 3 Progress Metrics / 3 dated Next Steps) structure. De-branded per repo standards. See internal/PROVENANCE_MAP.md.
