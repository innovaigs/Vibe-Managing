---
name: kpi-design
domain: growth
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [company, strategy, finance, customers, offerings, team, operations, market, metrics, goals, risks]
writes: [metrics, goals]
related_skills: [executive-dashboard-builder, growth-plan-builder, monthly-business-review, variance-diagnosis, business-health-diagnostic]
owned_by_agents: [growth-agent, business-analyst-agent]
---

# Skill: KPI Design

## Purpose
Select the small set of KPIs that actually predict and confirm this company's success — pairing leading indicators (which let the founder act early) with lagging indicators (which confirm outcomes) — and define each one precisely: formula, data source, threshold band, and review cadence. This turns vague intentions ("grow revenue," "improve retention") into a measurable, decision-ready metric set.

## When to Use
- The founder asks "what should I be tracking?", "which KPIs matter for my business?", "I have too many metrics — what actually counts?", or "define the metrics for my growth plan."
- A growth plan or dashboard is being built and needs its metric layer specified.
- A Success Factor or initiative has been defined but has no metric attached (execution-readiness gap).
- An existing metric set is noisy, redundant, or all lagging (no early-warning signal).

## When NOT to Use
- The metrics already exist and the founder wants them arranged into the three-lens matrix → use `executive-dashboard-builder`.
- The founder wants to compare this month's actuals to forecast → use `monthly-business-review`.
- The founder wants root-cause on a specific metric miss → use `variance-diagnosis`.
- The founder needs the full financial statement/ratio set for lending → defer financial-ratio depth to the CFO agent's finance skills.

## Required Context
- `strategy` — the 3 Success Factors, the growth pathway, and prioritized initiatives (KPIs must map to these).
- `company` — business model, revenue model (one-time vs recurring changes which KPIs apply), stage.
- `finance` — forecast and existing financial key metrics; cost structure by line/segment.
- `customers` / `offerings` — funnel stages, segments, service lines.
- `risks` — the risk register; each risk's warning-signal metric is a distinct KPI class.
- `goals` — targets that thresholds must be set against.

## Inputs
```yaml
input:
  success_factors: list            # the 3 things that must go right (from strategy/goals)
  business_model: str
  revenue_model: enum(one_time, recurring, usage, retainer, mixed)
  stage: enum(startup, established, scaling, mature)
  domains_to_cover: list           # subset of [you, business, environment]; default all three
  service_lines: list|null         # for margin-by-line / error-by-line metrics
  funnel_stages: list|null         # awareness->interest->desire->action->retention
  risk_register: list|null         # [{risk, warning_signal_metric, threshold}]
  existing_metrics: list|null       # current metrics to audit/rationalize
  targets: object|null              # forecast/plan targets to derive thresholds from
  data_sources_available: list|null # accounting, CRM, web analytics, HRIS, etc.
```

## Missing Information Protocol
1. Derive candidate KPIs from Success Factors, revenue model, and funnel/service-line structure before asking anything.
2. Pull thresholds from `targets`/forecast where available; pull warning-signals from the risk register.
3. If a candidate KPI has no available data source, mark it `data_gap: <source needed>` rather than dropping it — the gap itself is actionable.
4. Only if Success Factors or revenue model are unknown, ask the founder ONE batched question. Never assume the revenue model (it determines whether MRR/NRR even apply) or invent threshold numbers — mark thresholds `to_set` if no basis exists.

## Diagnostic Questions
- For each Success Factor, what is the single leading metric that predicts it and the single lagging metric that confirms it?
- Does the set include at least one early-warning (leading) signal for each domain the founder can actually influence?
- Is each metric owned by someone, computable from an available source, and comparable to a threshold?
- Is any metric vanity (moves without informing a decision)? If so, cut it.
- Does every top risk have its warning-signal metric represented?
- Is the cadence matched to how fast the metric moves and how fast the founder can act?

## Analysis Framework
1. **Map metrics to Success Factors.** Every KPI must trace to a Success Factor, an initiative, or a risk warning-signal. Orphan metrics are cut.
2. **Classify each candidate as leading or lagging.**
   - *Leading* (predict, act early): leads/week, discovery/validation calls, pipeline value, win rate on proposals, sales-cycle length, cash runway (months), burn rate, time-to-fill, eNPS, website conversion, compliance-readiness %, action-item completion %.
   - *Lagging* (confirm outcomes): MRR/ARR, revenue vs plan, net/gross margin, retention/NRR, revenue per employee, cash balance.
   - *Risk warning-signal* (distinct leading class): each risk's metric + threshold that fires before the risk materializes.
3. **Assign each to a domain lens:** YOU (founder), BUSINESS (internal performance), ENVIRONMENT (external/market).
4. **Pair leading↔lagging.** For each key outcome, ensure at least one leading metric predicts the lagging one, so a miss is visible before it lands.
5. **Define each KPI fully:** name, formula, unit, data source, threshold band (green/amber/red), cadence, owner, leading/lagging tag, domain.
6. **Prune to a decision-ready set.** Prefer ~5 financial key ratios plus the leading and warning-signal metrics tied to the Success Factors; cut redundancy and vanity.

## Calculations
Standard formulas the skill instantiates (defer exact figures to source data):
- **Variance %** = (Actual − Forecast) / Forecast × 100 (undefined when Forecast = 0 → "no comparison").
- **Growth rate (PoP)** = (Value_t − Value_t−1) / Value_t−1 × 100.
- **CAGR** = (Ending / Beginning)^(1/years) − 1.
- **Gross Margin %** = (Revenue − Direct Costs) / Revenue; by line = (Line rev − Line direct cost) / Line rev.
- **Operating Margin** = Operating Income / Revenue; **Net Profit Margin** = Net Profit / Revenue.
- **MRR growth rate** = % change in recurring monthly revenue (only if revenue_model includes recurring).
- **LTV:CAC** = (Avg contract value × retention × gross margin) / CAC.
- **NRR** = (retained + expansion revenue from existing accounts) / starting revenue of those accounts.
- **Rule of 40** = Revenue Growth Rate % + Net Profit Margin % (target ≥ 40).
- **Revenue per employee** = Revenue / Head count.
- **Cash runway (months)** = Cash balance / monthly burn.
- **DSO (Days to get paid)** ≈ AR / (Revenue/day); **DPO (Days to pay)** ≈ AP / (Costs/day).
Threshold bands are set from targets/forecast; where no basis exists, mark `to_set`.

## Decision Rules
- IF a candidate metric maps to no Success Factor, initiative, or risk THEN cut it as vanity.
- IF a Success Factor has only lagging metrics THEN add at least one leading metric that predicts it (no early-warning = blind spot).
- IF `revenue_model` excludes recurring THEN do not include MRR/ARR/NRR; use order frequency, repeat-purchase rate, and average order value instead.
- IF a risk in the register lacks a warning-signal metric THEN create one (metric + threshold) and tag it risk-warning.
- IF a KPI has no available data source THEN keep it but mark `data_gap` and propose the source/integration to close it.
- IF a threshold has no basis in targets/forecast THEN mark it `to_set` and request the founder's target rather than inventing a number.
- IF the set exceeds a decision-ready count (roughly a dozen headline KPIs) THEN prune redundant/overlapping metrics, keeping the leading↔lagging pairing intact.
- IF `stage == startup` THEN weight leading/activity metrics (validation calls, pipeline, runway) over lagging outcome metrics that lack history.

## Procedure
1. Read Success Factors, revenue model, funnel/service-line structure, and the risk register.
2. Generate candidate KPIs from each source (Success Factors, funnel stages, service lines, risks, financial headline set).
3. Classify each candidate: leading / lagging / risk-warning; assign a domain lens.
4. Pair leading↔lagging for each key outcome; fill early-warning gaps.
5. Define each surviving KPI fully (formula, source, threshold band, cadence, owner, tags).
6. Prune to a decision-ready set; audit any `existing_metrics` for redundancy/vanity and recommend cuts.
7. Emit the KPI specification (L1 draft) with data-gap and threshold-to-set flags; hand the set to `executive-dashboard-builder` for arrangement.
8. On founder approval, write the KPI definitions to `metrics` and link them to `goals`.

## Output
```yaml
output:
  kpi_set:
    - name: str
      definition: str
      formula: str
      unit: str
      classification: enum(leading, lagging, risk_warning)
      domain: enum(you, business, environment)
      maps_to: str                 # Success Factor / initiative / risk id
      data_source: str
      data_gap: str|null           # source/integration needed, if any
      threshold: {green: any, amber: any, red: any} | to_set
      cadence: enum(daily, weekly, monthly, quarterly)
      owner: str
      paired_with: str|null        # the leading/lagging counterpart
  cut_metrics: [ {metric, reason} ]  # vanity/redundant metrics recommended for removal
  coverage:
    success_factors_covered: number  # / 3
    early_warning_gaps: [str]
    risks_without_signal: [str]
  thresholds_to_set: [str]
  data_gaps: [str]
```

## Recommendations
Recommendations are ordered by decision value: first, early-warning gaps (Success Factors with no leading metric) — the highest-leverage fix; then risks without a signal; then thresholds to set; then vanity metrics to cut. Each KPI is justified by the decision it informs, not by availability. Prefer fewer, sharper metrics: a metric earns its place only if a plausible reading of it would change an action.

## Execution Opportunities
- Produce the KPI specification and definitions (reversible, LOW) — L1 draft.
- Create internal tasks to close each data gap (connect a source/integration) (reversible, LOW).
- Propose warning-signal metrics for uncovered risks and pass them to the risk register (reversible, LOW).
- Hand the finished set to `executive-dashboard-builder` (reversible, LOW).

## Human Approval Requirements
- Setting thresholds that become alert triggers or commitments requires founder confirmation (a threshold is a decision, not a default).
- Writing KPI definitions to `metrics` as authoritative requires founder approval.
- Connecting a new data integration to close a data gap requires approval (standing-configuration change).
- Analysis, classification, and drafting proceed at L1. Complies with AUTONOMY_AND_APPROVAL_MODEL.md.

## Escalation Conditions
- Success Factors are undefined or contradictory → founder (cannot design KPIs without them).
- A required threshold implies a financial commitment beyond confirmed capacity → founder (+ accountant).
- A metric requires restricted data (individual compensation/performance) → gate access; do not expose at KPI level.
- Data sources cannot support any leading metric for a critical Success Factor → surface the measurement gap to the founder.

## KPIs
(How this skill's own success is judged.)
- % of Success Factors with a paired leading+lagging metric.
- Reduction in metric count vs prior set while preserving coverage (signal-to-noise).
- % of KPIs with a defined formula, source, threshold, owner, and cadence (completeness).
- Downstream: fewer "which number do I trust?" questions; cleaner monthly reviews.

## Monitoring
After adoption, watch whether each KPI actually gets populated on cadence, whether thresholds fire appropriately (not too noisy, not silent), and whether leading metrics genuinely precede movements in their paired lagging metric. Retune metrics that never inform a decision or thresholds that fire constantly.

## Follow-Up
- Re-run at each quarterly growth-plan refresh, or when the Success Factors, revenue model, or org structure change.
- Event-triggered when a new risk is added (needs a warning-signal), a new service line launches, or the monthly review repeatedly surfaces a blind spot.

## Related Skills
Hands the finished set to `executive-dashboard-builder`; feeds `monthly-business-review` and `variance-diagnosis` (they consume these definitions and thresholds); supplies the metric layer to `growth-plan-builder`; shares warning-signal metrics with the risk register; supports `business-health-diagnostic`.

## Guardrails
- Never invent threshold numbers — mark `to_set` and get the founder's target.
- Never include a metric that cannot change a decision (vanity), regardless of how easy it is to measure.
- Match cadence to metric velocity and to how fast the founder can act; daily tracking of a slow-moving metric creates noise, not insight.
- Respect data sensitivity; restricted metrics stay access-gated.
- A leading metric is a prediction, not a promise — label confidence where a leading↔lagging link is unproven.

## Example
**Founder input:** "I run a services business moving to monthly retainers. What KPIs should I track? My three success factors are: land 10 retainer clients, keep gross margin above 55%, and stop being the bottleneck."

**Skill reasoning:**
- revenue_model = mixed→recurring, so MRR/NRR now apply.
- SF1 (10 retainer clients): leading = discovery calls/week + proposal win rate + pipeline value; lagging = MRR + number of active retainers. Pairs win rate → MRR.
- SF2 (gross margin ≥ 55%): leading = margin-by-service-line trend + utilization; lagging = blended gross margin %. Threshold band green ≥55 / amber 50–55 / red <50 (from founder's stated target).
- SF3 (founder not the bottleneck): domain = YOU; leading = founder decision load + action-item completion %; lagging = revenue per employee. Flags founder-load twin view.
- Risk register has "customer concentration" with no signal → creates warning-signal: top-client revenue share, red > 30%.
- Cuts "social media followers" (vanity — maps to no Success Factor).
- Data gap: utilization has no source (no time-tracking) → task to connect one.

**Output (abridged):** ~9 KPIs across the three lenses, each with formula/source/threshold/cadence/owner and leading↔lagging pairing; cut_metrics = [followers]; early_warning_gaps = none; risks_without_signal resolved (concentration signal added); data_gaps = [utilization source]; thresholds_to_set = none (all derived from targets).

**Executed vs. approval:** KPI spec drafted and data-gap task created at L1. Confirming the 55% band as a live alert threshold and writing definitions to `metrics` held for founder approval.

## Provenance
SOURCE — derived from the Growth Execution domain knowledge (`09-growth-execution.md`): the leading-vs-lagging classification, the risk warning-signal metric class, the YOU/BUSINESS/ENVIRONMENT metric domains, the canonical metric library and formulas, and the "Financial Forecast Key Metrics" worksheet (metric × definition × what-it-tells × link-to-success). De-branded per repo standards. See internal/PROVENANCE_MAP.md.
