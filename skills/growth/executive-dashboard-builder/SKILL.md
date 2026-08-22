---
name: executive-dashboard-builder
domain: growth
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [company, founders, finance, customers, offerings, team, operations, market, metrics, goals, risks, integrations]
writes: [metrics]
related_skills: [kpi-design, monthly-business-review, variance-diagnosis, growth-plan-builder, business-health-diagnostic]
owned_by_agents: [growth-agent, business-analyst-agent]
---

# Skill: Executive Dashboard Builder

## Purpose
Assemble the company's monitoring dashboard as a three-lens matrix — YOU (founder), YOUR BUSINESS (internal performance), YOUR ENVIRONMENT (external/market) — where every tile carries not just a number but its source and the decision it drives. This gives the founder one glance that answers "what needs attention right now?" and connects each metric to an action, not just a reading.

## When to Use
- The founder asks to "build my dashboard," "show me one view of the business," "what should my exec dashboard look like?", or "arrange my KPIs so I can watch them."
- A growth plan is being assembled and needs its Orientation/Dashboard section populated.
- KPIs have been defined (via `kpi-design`) and now need arrangement, source-wiring, and decision annotation.
- The founder wants the monthly forecast-vs-actual monitoring layout (actual vs forecast/prior-month/prior-year headline tiles).

## When NOT to Use
- The KPIs themselves are not yet chosen or defined → run `kpi-design` first.
- The founder wants to run the actuals-vs-forecast comparison and diagnose it → use `monthly-business-review`.
- The founder wants root-cause on one metric → use `variance-diagnosis`.
- The founder wants the full narrative plan document → use `growth-plan-builder`.

## Required Context
- `metrics` — the defined KPI set (formula, threshold, cadence, owner, leading/lagging tag) from `kpi-design`.
- `founders` — founder-load / wellbeing signals for the YOU lens; the founder-load twin view.
- `finance` — forecast targets and actuals for headline financial tiles; the cash-runway and profitability-map twin views.
- `market` — external indicators for the ENVIRONMENT lens.
- `risks` — warning-signal metrics + thresholds to surface as alert tiles.
- `integrations` — which data sources are connected (accounting, CRM, web analytics, HRIS) to auto-populate tiles.

## Inputs
```yaml
input:
  kpi_set: list                    # from kpi-design: [{name, formula, classification, domain, threshold, cadence, owner, data_source}]
  view: enum(three_lens, monthly_monitor, both)   # matrix layout vs actual-vs-forecast headline layout
  section_metrics: object|null      # metrics contributed per growth-plan section (incremental build)
  forecast_targets: object|null     # for monthly_monitor comparison baselines
  actuals: object|null              # latest actuals if populating live values
  risk_signals: list|null           # [{risk, metric, threshold}]
  founder_signals: object|null      # decision load, hours, wellbeing, learning
  connected_sources: list|null      # available integrations
```

## Missing Information Protocol
1. Pull each tile's value and source from connected integrations / twin views before asking.
2. If a KPI has no connected source, render the tile with `source: manual / not connected` and add a data-gap note; do not leave it silently blank.
3. If forecast or actual is missing for a monthly-monitor tile, mark that tile `incomplete` (see the data-completeness gate) rather than showing a partial comparison.
4. Only if the KPI set itself is absent, route back to `kpi-design`. Never invent a metric value, a source, or a threshold.

## Diagnostic Questions
- Does every tile name its data source and the decision it drives (not just a number)?
- Are all three lenses populated (YOU / BUSINESS / ENVIRONMENT), including at least one leading indicator per lens the founder can act on?
- For each headline financial tile, are all three comparison baselines present (vs Forecast, vs Previous Period, vs Previous Year)?
- Are risk warning-signals surfaced as alert tiles with their thresholds visible?
- Is the founder-wellbeing/load lens present as a leading indicator of execution risk?
- Which tiles are stale or not connected, and is that flagged?

## Analysis Framework
1. **Choose the layout.**
   - *three_lens matrix*: rows = plan sections (or metric groups), columns = YOU / BUSINESS / ENVIRONMENT; each later plan section deposits its metrics into the buckets (incremental build).
   - *monthly_monitor*: headline tiles each showing actual + three comparisons (vs Forecast, vs Previous Period, vs Previous Year) + delta amount and %.
2. **Populate the three lenses.**
   - YOU: goals-on-time %, action-item completion %, learning hours, decision load, wellbeing (leading indicators of execution risk).
   - BUSINESS: revenue, gross/operating/net margin, cash balance, net cash flow, AR/DSO, AP/DPO, pipeline, win rate, retention/NRR, revenue per employee, operational quality.
   - ENVIRONMENT: market growth/CAGR, competitor moves tracked, regulatory changes, talent supply, funding-climate indicators.
3. **Build the monthly headline tiles:** Revenue (+ per-day rate, + breakdown by line), Expenses & Costs (+ breakdown), Operating Income & Margin, Net Profit & Margin, Cash Balance & Net Cash Flow, AR & Days-to-Get-Paid, AP & Days-to-Pay, and a **Top Movers** tile (largest actual-vs-comparison variance line items).
4. **Annotate each tile** with: source, cadence, owner, threshold band (green/amber/red), leading/lagging tag, and the decision it drives.
5. **Surface risk alert tiles** from the warning-signal metrics; light the tile when a threshold is crossed.
6. **Freshness pass:** flag stale or not-connected tiles; propagate confidence from source data.

## Calculations
- **Delta amount** = Actual − Baseline (Forecast / Previous Period / Previous Year).
- **Delta %** = (Actual − Baseline) / Baseline × 100 (undefined when Baseline = 0 → render "no comparison").
- **Revenue per day** = Revenue / days in period.
- **Days to get paid (DSO)** ≈ AR / (Revenue/day); **Days to pay (DPO)** ≈ AP / (Costs/day).
- **Top Movers rank** = sort line items by |contribution to total variance| descending.
- **Threshold state** = compare tile value against green/amber/red band from `kpi-design`.
- **Runway (months)** = Cash balance / monthly burn (from cash-runway twin view).
The dashboard displays computed values; it does not re-derive forecasts. Source figures come from `finance` / `kpi-design`.

## Decision Rules
- IF a tile is a headline financial metric THEN it must show all three baselines (Forecast, Previous Period, Previous Year); if any baseline is missing, mark the tile `incomplete` and do not show a partial comparison as if complete.
- IF a KPI has no connected data source THEN render `source: manual / not connected` and add a data-gap note.
- IF a tile value is older than its cadence period THEN flag it `stale` and reduce its displayed confidence.
- IF a risk warning-signal threshold is crossed THEN light the alert tile red and link it to the risk's contingency owner.
- IF any lens (YOU / BUSINESS / ENVIRONMENT) has zero tiles THEN flag a coverage gap — a single-lens dashboard hides either founder or market risk.
- IF the YOU lens has no leading wellbeing/load indicator THEN add one (founder load is a leading indicator of execution risk).
- IF a tile carries a number but no "decision it drives" annotation THEN it is not dashboard-ready; require the annotation before publishing.
- IF divide-by-zero on any delta % THEN render "no comparison," never 0% or ∞.

## Procedure
1. Read the KPI set and choose the layout(s) per `view`.
2. Wire each KPI to its data source (integration / twin view); mark unconnected ones.
3. Populate the three lenses; ensure each has at least one actionable leading indicator.
4. Build monthly headline tiles with the three baselines and Top Movers (if `monthly_monitor`).
5. Annotate every tile: source, owner, cadence, threshold band, leading/lagging tag, decision-it-drives.
6. Add risk alert tiles; run the freshness pass.
7. Emit the dashboard spec (L1 draft) with coverage gaps, data gaps, stale flags, and incomplete tiles listed.
8. On founder approval, register the dashboard layout to `metrics` and connect any approved sources.

## Output
```yaml
output:
  dashboard:
    layout: enum(three_lens, monthly_monitor, both)
    lenses:
      you: [ {tile} ]
      business: [ {tile} ]
      environment: [ {tile} ]
    headline_tiles:                # monthly_monitor
      - name: str
        actual: number|null
        vs_forecast: {delta, pct, band}
        vs_previous_period: {delta, pct}
        vs_previous_year: {delta, pct}
        status: enum(complete, incomplete)
        breakdown: [ {line, value} ] | null
    top_movers: [ {line, actual, baseline, change} ]
    alert_tiles: [ {risk, metric, threshold, state: enum(ok, tripped), owner} ]
    tile_spec:                     # applied to every tile
      # {name, value, source, owner, cadence, threshold_band, classification, decision_it_drives, freshness, confidence}
  coverage_gaps: [str]             # missing lens / missing early-warning
  data_gaps: [str]                 # unconnected sources
  stale_tiles: [str]
  incomplete_tiles: [str]          # missing a required baseline
```

## Recommendations
Recommendations are ordered by what most degrades decision quality: (1) incomplete headline tiles (missing a baseline) — the founder could misread a partial comparison; (2) tripped risk alerts; (3) coverage gaps (a dark lens); (4) stale/unconnected tiles. Each recommendation names the source to connect or the metric to add. Every tile is justified by the decision it drives; a tile that drives no decision is proposed for removal.

## Execution Opportunities
- Assemble/update the internal dashboard layout (reversible, LOW) — L1 draft, then auto-refresh once approved.
- Create tasks to connect unconnected data sources (reversible, LOW).
- Light and route risk alert tiles to their contingency owners (reversible, LOW — internal notice).
- Feed the assembled dashboard into `growth-plan-builder` Section 2 (reversible, LOW).

## Human Approval Requirements
- Connecting a new data integration to auto-populate tiles requires approval (standing-configuration change).
- Setting a tile's alert threshold to fire notifications requires founder confirmation.
- Publishing the dashboard as the company's authoritative monitoring view requires founder approval.
- Assembly, annotation, and internal refresh proceed at L1. Complies with AUTONOMY_AND_APPROVAL_MODEL.md.

## Escalation Conditions
- A headline tile cannot be completed because forecast or actuals are unavailable → surface the data gap; do not present a partial dashboard as complete.
- A risk alert tile trips → escalate per that risk's contingency (founder; and accountant/lawyer/HR as the risk dictates).
- A tile requires restricted data (individual comp/performance) → gate access; show an aggregate instead.
- Source data confidence is low/stale for a decision-critical tile → surface uncertainty, do not let the founder act on it unflagged.

## KPIs
- % of tiles with source + owner + decision-it-drives annotation (completeness).
- Lens coverage (all three populated) and early-warning coverage per lens.
- % of headline tiles with all three baselines present.
- Freshness rate (tiles current within cadence).
- Downstream: does the dashboard feed a clean monthly review with no missing baselines?

## Monitoring
After publishing, watch tile freshness, alert-tile firing rate (too noisy vs silent), and whether the founder acts on amber/red tiles. Re-tune thresholds that fire constantly and reconnect sources that go stale. Confirm the Top Movers tile reconciles with `variance-diagnosis` findings.

## Follow-Up
- Refresh continuously as data streams in; re-lay out at each quarterly growth-plan refresh.
- Event-triggered rebuild when new KPIs are added, a new integration connects, a new risk needs an alert tile, or the plan structure changes.

## Related Skills
Consumes `kpi-design` output; feeds `growth-plan-builder` (Section 2) and `monthly-business-review` (headline tiles + Top Movers layout); shares alert tiles with the risk register; supports `business-health-diagnostic` (health rollup) and `variance-diagnosis`.

## Guardrails
- Never show a partial comparison (missing a baseline) as if complete — mark it incomplete.
- Never invent a tile value or source; unconnected tiles are flagged, not filled.
- Propagate freshness/confidence from source data; a view built on stale inputs is itself flagged stale.
- Respect sensitivity tiers: restricted metrics are shown only in aggregate or access-gated.
- Every tile must earn its place with a decision it drives; resist dashboard sprawl.

## Example
**Founder input:** "Build me a dashboard I can check monthly. I care about revenue vs plan, cash, whether I'm the bottleneck, and my competitor's moves."

**Skill reasoning:**
- view = both. Pulls the KPI set from `kpi-design`.
- BUSINESS lens: Revenue tile with vs-Forecast/vs-Prev-Month/vs-Prev-Year (all three present from accounting integration); Cash Balance & Net Cash Flow (runway 7 months from cash-runway twin view); Gross Margin % (amber band). Expenses tile flagged: actual present but prior-year missing → marks tile `incomplete`.
- YOU lens: founder decision load (from founder-load twin view) + action-item completion % — both leading indicators of execution risk.
- ENVIRONMENT lens: competitor moves tracked (manual source → data-gap note) + market growth rate.
- Risk alert: customer-concentration signal at 34% vs red threshold 30% → alert tile tripped, routed to founder.
- Top Movers computed: office rent and a personnel line drove the month's expense variance.

**Output (abridged):** three-lens matrix + monthly headline tiles; incomplete_tiles = [Expenses (no prior-year)]; data_gaps = [competitor-moves source]; alert_tiles = [concentration TRIPPED]; coverage_gaps = none.

**Executed vs. approval:** Dashboard assembled, annotated, and Top Movers computed at L1; concentration alert routed internally. Connecting a live competitor-tracking source and enabling the concentration alert to push notifications held for founder approval.

## Provenance
SOURCE — derived from the Growth Execution domain knowledge (`09-growth-execution.md`): the three-domain YOU/BUSINESS/ENVIRONMENT dashboard structure, the incremental "each section deposits metrics" build, the monthly-monitor headline tiles with three comparison baselines plus Top Movers, and the risk warning-signal alert class. De-branded (generic "accounting/CRM/analytics tool," no named products). See internal/PROVENANCE_MAP.md.
