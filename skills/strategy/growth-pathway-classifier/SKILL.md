---
name: growth-pathway-classifier
domain: strategy
version: 0.1.0
autonomy_ceiling: L0
provenance: SOURCE
reads: [company, finance, metrics, market, operations, goals]
writes: [strategy, metrics]
related_skills: [business-health-diagnostic, growth-lever-selector, resource-gap-analysis, strategic-planning]
owned_by_agents: [strategy-agent]
---

# Skill: Growth Pathway Classifier

## Purpose
Reject the myth of the single smooth upward sales curve. Given a revenue history and projection, classify which of four growth shapes the business is actually on — rapid, incremental, episodic, or plateau — so the founder can tell stage-normal problems apart from problems that need special attention, and pick the right lever for their actual pathway.

## When to Use
- The founder asks "why has our growth changed?", "is this normal?", "are we stuck?"
- As a standing input to `business-health-diagnostic` when revenue looks flat or lumpy.
- Before choosing a growth strategy — the right lever depends on the pathway.
- After a period of surprising sales behavior (a sudden jump, a stall, an irregular pattern).

## When NOT to Use
- No revenue time series exists yet (pre-revenue) — there is nothing to classify.
- The founder wants to choose a growth avenue, not diagnose the shape → `growth-lever-selector` (this skill feeds it).
- The question is whole-company health → `business-health-diagnostic` (which calls this skill).
- The task is projecting future revenue (forecasting), not classifying observed shape.

## Required Context
Reads `finance`/`metrics` for the revenue (or chosen growth-measure) time series, `company` for stage/founding date, `market` for demand trend and competitive context, `operations` for capacity signals (needed to distinguish episodic-from-capacity vs. plateau-from-market). Series should carry `as_of` and be continuous; gaps are interpolated conservatively and flagged.

## Inputs
```yaml
input:
  growth_measure: str                 # what "growth" is measured by (usually revenue)
  history_series: [ {period: str, value: number} ]   # oldest→newest, up to ~10 years for detail
  projection_series: [ {period: str, value: number} ] # up to ~5 years forward
  today_marker: str                   # the period that separates actual from projected
  founding_period: str
  context:
    demand_trend: enum(rising, flat, declining, unknown)
    capacity_utilization_pct: number  # to distinguish episodic (capacity-limited) shapes
    known_roadblocks: [str]           # technology, staffing, deployment blockers
    recent_events: [str]              # one-off wins/losses that could cause blips
```

## Missing Information Protocol
1. Prefer to build the series from the accounting integration; only ask the founder for periods integrations can't supply.
2. Require a minimum of ~6–8 continuous periods to classify with confidence; below that, return a provisional classification flagged `low-confidence`.
3. Never fabricate periods — interpolate a single missing interior period conservatively and flag it; refuse to classify across large gaps.
4. If capacity data is missing, still classify shape but note that episodic-vs-plateau causation is uncertain without it.

## Diagnostic Questions
- How do you measure growth, and what is the history of that measure?
- Plotted since founding plus projection, what is the overall shape?
- Is the recent slope steep and sustained (rapid), steady and modest (incremental), irregular blips/steps (episodic), or flat (plateau)?
- For a plateau: is it demand-driven or roadblock-driven (technology/staffing/deployment)? Is it temporary?
- For episodic: are the blips external (customer wins/losses) or internal (capability/management-structure limits)?
- Which current problems are stage-normal for this pathway, and which are exceptional and need special attention?

## Analysis Framework
The Four Pathways to Growth model. Plot the growth measure over time with a "today" line separating actual from projected, then classify the recent-window shape:
- **Rapid Growth** — steep, sustained climb. Drivers: right offering at the right time/price; favorable macro/micro forces; competition avoided via niche/geography; strong customer relationships.
- **Incremental Growth** — steady, modest climb. Drivers: response to business climate; owner preference for a manageable size; natural maturation.
- **Episodic Growth** — irregular blips/steps rather than a steady trajectory. Drivers: internal capability limits needing structural/management adjustment; customer-related sales blips.
- **Plateau Growth** — a flat stretch. Usually temporary and reversible; broken by a changed strategy/tactics/orientation, or by resolving technology/staffing/deployment roadblocks.

For the classified pathway, separate **stage-normal problems** (expected for this shape) from **exceptional problems** (need special attention), then name the primary lever.

## Calculations
- **Period growth rate** `g_t = (v_t − v_{t-1}) / v_{t-1} × 100` for each period.
- **Trailing CAGR** over the recent window `= (v_end / v_start)^(1/years) − 1`.
- **Slope trend**: sign and magnitude of the recent-window average `g_t`.
- **Volatility (coefficient of variation of g_t)** `= stdev(g_t) / mean(|g_t|)` over the recent window — high volatility with near-flat mean signals episodic.
- **Classification thresholds (SYNTH defaults over the source's qualitative shapes; tune per business):**
  - **Rapid** — recent avg `g_t` sustained high (heuristic ≥ ~20%/yr) with low-to-moderate volatility.
  - **Incremental** — recent avg `g_t` modest positive (heuristic ~2–15%/yr), low volatility.
  - **Plateau** — recent avg `g_t` within ±2%/period, low volatility (flat line).
  - **Episodic** — high volatility (CV of `g_t` high) with no steady trend — blips/steps up and down.
- **Reference conventions:** plot up to 10 years of history for detail and ~5 years of projection; mark "today."

## Decision Rules
- **IF** recent avg `g_t` is within ±2% and volatility is low **THEN** classify Plateau; treat as temporary/reversible, NOT terminal.
- **IF** Plateau AND a technology/staffing/deployment roadblock exists **THEN** the lever is resolving that roadblock; else test a strategy/tactics/orientation change → recommend `growth-lever-selector`.
- **IF** volatility is high with no steady trend **THEN** classify Episodic; investigate internal capability/management-structure limits, not only external demand → recommend `resource-gap-analysis`.
- **IF** Episodic AND capacity utilization > ~90–100% at the blips **THEN** the constraint is internal capacity/structure (stage-normal for episodic), not demand.
- **IF** recent avg `g_t` is sustained high with low volatility **THEN** classify Rapid; stage-normal problems are capacity, cash-to-fund-growth, and hiring → recommend `resource-gap-analysis` + cash check.
- **IF** recent avg `g_t` is modest and steady **THEN** classify Incremental; confirm it matches the founder's aspiration (a deliberate choice vs. an unwanted ceiling).
- **IF** history < 6 periods **THEN** return provisional classification flagged low-confidence; do not drive irreversible decisions from it.
- **IF** a single recent event explains a blip **THEN** note it so a one-off is not mis-read as an episodic pattern.

## Procedure
1. Assemble/validate the growth-measure series; mark "today"; interpolate/flag any single gap.
2. Compute period growth rates, trailing CAGR, slope trend, and volatility over the recent window.
3. Classify the pathway using the thresholds and context (demand + capacity).
4. For Plateau/Episodic, determine causation (roadblock vs. demand; internal vs. external).
5. List stage-normal problems for the pathway and separate exceptional problems needing special attention.
6. Name the primary lever and the recommended next skill.
7. Confirm Incremental classifications against the founder's growth aspiration (chosen vs. capped).
8. Write the classification + interpretation to `strategy`/`metrics`.

## Output
```yaml
output:
  pathway: enum(rapid, incremental, episodic, plateau)
  confidence: enum(high, medium, low)   # driven by series length/continuity
  metrics: {recent_avg_growth_pct: number, trailing_cagr_pct: number, volatility_cv: number}
  causation: str                        # roadblock/demand/internal-capacity/external, as applicable
  stage_normal_problems: [str]          # expected for this pathway
  exceptional_problems: [str]           # need special attention
  primary_lever: str
  aspiration_check: str                 # for incremental: chosen size vs. unwanted ceiling; else "n/a"
  recommended_next_skills: [str]
  chart_spec: {history: [...], projection: [...], today_marker: str}   # for the founder dashboard
```

## Recommendations
The classification is only useful if it changes what the founder worries about — so the output leads with the separation of stage-normal from exceptional problems, then a single primary lever. A plateau is explicitly framed as reversible to prevent premature drastic action; an incremental shape is checked against aspiration so a deliberate lifestyle-size business isn't "fixed" against the founder's wishes.

## Execution Opportunities
- Write the pathway classification and chart spec to `strategy`/`metrics` and the founder dashboard — reversible, LOW.
- Auto-propose `growth-lever-selector` (plateau/incremental) or `resource-gap-analysis` (episodic/rapid) — reversible, LOW.
- Draft a one-line interpretation for the founder briefing — reversible, LOW.
Autonomy ceiling L0 — analysis and internal notes only; no business action.

## Human Approval Requirements
- None to classify (analysis is always allowed).
- Any lever the founder chooses to pursue is decided and approved downstream.

## Escalation Conditions
- **Declining trend misclassified risk** — if the series is actually declining (not plateau), flag it and escalate to `business-health-diagnostic` / founder as a revenue risk.
- **Series too short/gappy for a confident call** → surface low confidence; do not let a provisional call drive an irreversible bet.
- **Incremental shape conflicts with an aggressive founder goal** → founder (aspiration vs. reality conversation).

## KPIs
- Classification accuracy: does the pathway hold when more periods arrive?
- Decision usefulness: did separating stage-normal from exceptional problems prevent an over-reaction (or catch a real one)?
- Lever fit: did the recommended lever match what actually moved growth?

## Monitoring
Re-check the classification as each new period lands. Watch for a plateau tipping into decline (escalate) or an episodic pattern smoothing into incremental (structural fix worked). Flag if a "one-off event" blip repeats and becomes a pattern.

## Follow-Up
- Re-run each reporting period, or whenever the shape visibly changes.
- Feed the pathway into `growth-lever-selector` and `strategic-planning`.

## Related Skills
Called by `business-health-diagnostic`. Feeds `growth-lever-selector`, `resource-gap-analysis`, and `strategic-planning`.

## Guardrails
- Never label a plateau as terminal — the model treats it as reversible.
- Do not "fix" an incremental business the founder deliberately chose to keep small — confirm aspiration first.
- Do not classify confidently on <6 periods or across large data gaps.
- Distinguish a one-off event from a genuine episodic pattern before recommending a structural change.

## Example
**Founder input:** "Revenue has been about $52k/mo for 14 months. Before that we were climbing steadily. Are we stuck? Capacity is at 68%, no major roadblocks I know of."
**Reasoning:** Recent 14-period avg `g_t` ≈ +0.4% within ±2%, low volatility → **Plateau**. Capacity 68% (not capacity-limited) and no named roadblock → causation is likely market/tactics, not internal. Stage-normal problems for plateau: demand saturation in the current segment, stale marketing. Exceptional: none critical (not declining). Primary lever: test a strategy/tactics/orientation change — new segment, new channel, or new offering.
**Output:** pathway = plateau (confidence high); metrics {recent_avg_growth 0.4%, cagr 0.5%, volatility low}; causation "demand-side, current segment saturating; not roadblock-driven"; stage_normal_problems ["segment saturation","marketing gone stale"]; exceptional_problems []; primary_lever "reorient tactics / open a new avenue"; recommended_next_skills ["growth-lever-selector","competitive-intelligence-analysis"].
**Executed vs. approval:** Wrote classification + chart to the dashboard, proposed running `growth-lever-selector`. No action committed.

## Provenance
SOURCE. Implements the Four Pathways to Growth model (rapid/incremental/episodic/plateau), the "growth occurs in stages" and "no single normal curve" principles, the plateau-is-reversible and episodic-is-internal-capability rules, and the 10-year-history / 5-year-projection / "today"-marker graphing convention. Threshold values for the four shapes are SYNTH defaults over the source's qualitative descriptions. See `internal/PROVENANCE_MAP.md`.
