---
name: marketing-metrics-tracker
domain: marketing
version: 0.1.0
autonomy_ceiling: L2
provenance: SYNTH
reads: [customers, offerings, finance, strategy, goals, metrics, integrations]
writes: [metrics, goals, decisions]
related_skills: [channel-selection, social-content-planner, website-conversion-audit, marketing-strategy-builder, marketing-funnel-planner]
owned_by_agents: [marketing-agent, growth-agent]
---

# Skill: Marketing Metrics Tracker

## Purpose
Computes, monitors, and alerts on the marketing numbers that tell the founder whether marketing is working: funnel conversion at each stage, social/engagement metrics, and the economics of acquisition (CAC, LTV, ROAS). It turns scattered platform stats into one dashboard with goal-aligned targets and threshold alerts, so weak channels, leaking funnel stages, and unprofitable spend surface early instead of at the end of the quarter.

## When to Use
- Continuous/recurring: the standing measurement loop behind every other marketing skill.
- The founder asks "is our marketing working?", "what's our CAC / ROAS / conversion rate?", "which channel is worth it?", "where are we losing people in the funnel?"
- After `channel-selection` picks channels or `social-content-planner` ships a cycle — to instrument and report results.
- When a growth or monthly business review needs the marketing scorecard.

## When NOT to Use
- No data source is connected and no numbers are provided → connect analytics or gather inputs first; this skill computes from data, it doesn't invent it.
- The founder wants channel *selection* or content *planning*, not measurement → use `channel-selection` / `social-content-planner`.
- Full financial statements / company-wide KPIs beyond marketing → hand to the CFO/finance skills; this skill owns marketing metrics and shares CAC/LTV with them.
- Deciding strategy from the numbers (the plan) → feed results to `marketing-strategy-builder`; this skill measures and alerts, it doesn't write the plan.

## Required Context
- `metrics` — historical marketing metric time series + existing targets (append-only; this skill writes here).
- `goals` — the marketing goals and their target values, to set each metric's target and status.
- `finance` — total sales+marketing spend and gross margin (needed for CAC and margin-based LTV); ad spend by channel (for ROAS).
- `customers.segments` — segment-level CAC/LTV/churn if tracked; order value and purchase frequency for LTV.
- `strategy` / `channel-selection` output — which channels/funnel stages are active and must be tracked.
- `integrations` — connected web analytics, social analytics, ad platforms, and email/CRM; each metric's data source and freshness.

## Inputs
```yaml
input:
  reporting_period: str            # REQUIRED. e.g. "2026-08" or a date range.
  scope:                           # REQUIRED. What to report.
    type: enum(full_dashboard, funnel_only, social_only, acquisition_economics, single_channel)
  channels: [str]                  # Which channels are in scope.
  funnel_data:                     # For funnel conversion. Counts entering each stage.
    type: {awareness: number, interest: number, desire: number,
           action: number, retention: number}
  social_data:                     # Per channel/post aggregates.
    type: list[{channel: str, followers: number, impressions: number, reach: number,
                engagements: number, clicks: number, referrals: number,
                conversions: number, mentions: number}]
  acquisition_data:                # For CAC/LTV/ROAS.
    type: {sales_marketing_spend: number, ad_spend: number, new_customers: number,
           ad_attributed_revenue: number, avg_order_value: number,
           purchase_frequency: number, avg_lifespan_periods: number,
           gross_margin_pct: number}
  targets:                         # Optional. Goal targets per metric (else pulled from goals).
    type: {metric_key: target_value}
  alert_config:                    # Optional. Thresholds; defaults applied if omitted.
    type: {metric_key: {warn_at: number, critical_at: number, direction: enum(above, below)}}
  prior_period_ref: str            # Optional. For trend/variance.
```

## Missing Information Protocol
1. **A metric's inputs are missing** → compute what's possible, mark the rest `unavailable`, and list exactly which input is needed and from which source (e.g. "ROAS needs ad_attributed_revenue from the ad platform"). Never fabricate a value.
2. **No targets** → pull from `goals`; if none exist, set a provisional target from the prior period (e.g. "≥ last period" or the source's example-style goal such as "+10% audience") and clearly label it provisional, not agreed.
3. **CAC/LTV/ROAS inputs partial** → compute the ones you can; for CAC prefer total sales+marketing spend ÷ new customers, and state whether spend is blended or paid-only. For LTV, state whether it's revenue-based or margin-based (× gross margin).
4. **Attribution unclear** (which channel drove a conversion) → report channel metrics with an attribution caveat; do not over-claim a single channel's ROAS when attribution is blended.
5. **Never assume** thresholds are "healthy" without stating they're CLAUDE-DERIVED defaults, and never present an estimated number as measured.

## Diagnostic Questions
- Which metrics map to the active goal(s), and what is each one's target?
- At which funnel stage is the biggest drop-off (the leak)?
- Is engagement/reach trending up, flat, or down since last period?
- Is CAC below LTV by a healthy margin (LTV:CAC ≥ 3:1)? Is ROAS above break-even?
- Which channel has the best cost-per-outcome; which is wasting spend?
- Are any metrics past their warn/critical thresholds — and is the trend improving or worsening?
- Is the data fresh and trustworthy, or stale/estimated (attribution caveats)?

## Analysis Framework
1. **Assemble the scorecard** — for each in-scope metric: current value, target, prior value, trend (▲/▼/→), and status (healthy / needs_attention / at_risk / critical) from thresholds.
2. **Funnel analysis** — compute stage-to-stage conversion rates; identify the stage with the steepest drop as the priority leak; compare to prior period.
3. **Engagement/reach analysis** — engagement rate, CTR, reach, impressions, referrals, conversions per channel; rank channels by the metric tied to the goal (prioritize reach/traffic over vanity likes).
4. **Acquisition economics** — CAC, LTV, LTV:CAC, ROAS per channel and blended; compare ROAS to break-even (ROAS = 1.0 covers ad cost only, not margin) and LTV:CAC to the 3:1 health signal.
5. **Alerting** — any metric crossing warn/critical raises an alert with severity, the value vs. threshold, the trend, and a recommended next action (route to the owning skill).
6. **Goal alignment & write-back** — align each metric to its goal, update `metrics` (time series) and `goals` (status), and log a decision record if an alert triggers a recommended action.

## Calculations
[SOURCE-DERIVED social metrics; CAC/LTV/ROAS/conversion-rate are CLAUDE-DERIVED — not part of the source financial — and are flagged throughout.]

**Social / engagement (SOURCE-DERIVED):**
- **Post Engagement Rate** = total engagements ÷ total impressions.
- **Click-Through Rate (CTR)** = clicks ÷ impressions.
- **Reach** ≈ own followers + followers of accounts that shared the post.
- **Impressions** = times a post appeared in feeds/timelines.
- **Social Referrals** = visitors to the site arriving from social.
- **Social Conversions** = purchases/leads from social-sourced visitors (the true social-ROI metric).

**Funnel & economics (CLAUDE-DERIVED — not source-taught):**
- **Conversion Rate (per funnel stage)** = (# advancing to next stage) ÷ (# entering the stage). [CLAUDE-DERIVED]
- **Overall funnel conversion** = customers at Action ÷ prospects at Awareness. [CLAUDE-DERIVED]
- **Website Conversion Rate** = conversions ÷ site visitors. [CLAUDE-DERIVED]
- **Customer Acquisition Cost (CAC)** = total sales+marketing spend ÷ new customers acquired. [CLAUDE-DERIVED]
- **Customer Lifetime Value (LTV)** = avg order value × purchase frequency × avg customer lifespan (× gross margin for margin-based LTV). [CLAUDE-DERIVED]
- **LTV:CAC ratio** = LTV ÷ CAC; ≥3:1 commonly treated as healthy. [CLAUDE-DERIVED]
- **Return on Ad Spend (ROAS)** = ad-attributed revenue ÷ ad spend; ROAS < 1.0 loses money on ad cost alone, and true profitability needs ROAS above the margin break-even. [CLAUDE-DERIVED]

**Default thresholds (CLAUDE-DERIVED — the source gives example goals only, not bands):**
| Metric | warn | critical | direction |
|---|---|---|---|
| LTV:CAC | < 3:1 | < 1:1 | below |
| ROAS | < margin break-even | < 1.0 | below |
| Stage conversion vs. prior | −10% | −25% | below |
| Engagement rate vs. prior | −15% | −30% | below |
| Reach/impressions vs. prior | flat | declining | below |
| CAC vs. target | +15% | +30% | above |
All bands are configurable; they are defaults, not source-taught truths.

## Decision Rules
- **IF** a stage-to-stage conversion rate is the lowest in the funnel **THEN** flag that stage as the priority leak and route a fix to the owning skill (Interest leak → `website-conversion-audit` / lead-capture; Action leak → friction/offer review). [SYNTH]
- **IF** LTV:CAC < 3:1 **THEN** raise `needs_attention`; **IF** < 1:1 **THEN** raise `critical` — acquisition is unprofitable; recommend pausing/rework of the worst channel and escalate spend to founder. [CLAUDE-DERIVED]
- **IF** ROAS < 1.0 on a paid channel **THEN** critical alert; recommend pause and route to `channel-selection` for reallocation (spend change is approval-gated). [CLAUDE-DERIVED]
- **IF** engagement rate or reach drops past its threshold **THEN** alert and route to `social-content-planner` (content off-target) with the reuse/drop signal. [SOURCE intent]
- **IF** a metric lacks required inputs **THEN** mark it `unavailable` and name the missing source; do not estimate silently. [SYNTH]
- **IF** choosing which metrics to headline **THEN** prioritize reach/impressions and traffic/conversions over vanity likes, aligned to the goal. [SOURCE]
- **IF** attribution is blended **THEN** report per-channel ROAS with a caveat and prefer blended CAC as the reliable figure. [SYNTH]
- **IF** an alert recommends **changing/pausing ad spend** **THEN** the recommendation is prepared but the spend change requires founder approval + CFO check. [POLICY]
- **IF** a target is provisional (auto-set) **THEN** label it and request founder confirmation before treating a miss as a real failure. [SYNTH]

## Procedure
1. **Load** period, scope, connected data sources, prior-period baseline, goals/targets, finance spend + margin.
2. **Pull/receive data** for the in-scope metrics from connected integrations (read-only) or from provided inputs.
3. **Compute** each metric with the formulas above; note SOURCE vs. CLAUDE-DERIVED provenance per metric.
4. **Funnel pass** — stage conversions + identify the leak.
5. **Channel pass** — rank channels by goal-aligned outcome; compute per-channel and blended CAC/ROAS where data allows.
6. **Status & trend** — assign status from thresholds; compute trend vs. prior period.
7. **Alerting** — generate alerts for threshold breaches with severity, evidence, trend, and a routed recommended action.
8. **Write back** — append actuals to `metrics`, update `goals` status, log a decision record for any alert-driven recommendation.
9. **Assemble dashboard** output; hand off recommended fixes to the owning skills (channel-selection / website-conversion-audit / social-content-planner / marketing-funnel-planner).

## Output
```yaml
output:
  reporting_period: str
  scope: str
  scorecard:
    - metric_key: str
      value: number | "unavailable"
      unit: str
      target: number
      provisional_target: bool
      prior_value: number
      trend: enum(up, down, flat)
      status: enum(healthy, needs_attention, at_risk, critical)
      provenance: enum(SOURCE, CLAUDE_DERIVED)
      data_source: str
      missing_inputs: [str]
  funnel:
    stage_conversions: {awareness_to_interest: number, interest_to_desire: number,
                        desire_to_action: number, action_to_retention: number}
    overall_conversion: number
    priority_leak: enum(awareness, interest, desire, action, retention)
  channel_ranking:
    - channel: str
      goal_metric: number
      cac: number | "unavailable"
      roas: number | "unavailable"
      verdict: enum(scale, keep, watch, pause)
  acquisition_economics:
    blended_cac: number | "unavailable"
    ltv: number | "unavailable"
    ltv_basis: enum(revenue, margin)
    ltv_cac_ratio: number | "unavailable"
    blended_roas: number | "unavailable"
    attribution_caveat: str
  alerts:
    - metric_key: str
      severity: enum(warning, critical)
      value_vs_threshold: str
      trend: enum(up, down, flat)
      recommended_action: str
      routed_to: str                 # skill to handle it
      needs_approval: bool
  handoffs: [str]
  confidence: enum(low, medium, high)
```

## Recommendations
Alerts are prioritized by **severity, then business impact** (unprofitable spend and funnel leaks outrank vanity-metric dips). Each recommendation is routed to the skill that can act on it and framed by reversibility: measurement, dashboard updates, and internal alerts execute autonomously (L2); anything that changes spend, pauses a campaign, or publishes is prepared as an approval-gated recommendation. The single most costly problem (worst LTV:CAC channel, steepest funnel leak) is surfaced first so the founder acts where money is actually leaking.

## Execution Opportunities
- **Compute and update** the marketing dashboard/scorecard; append actuals to `metrics` — reversible, **L2**.
- **Raise internal alerts / notifications** on threshold breaches — reversible, L2.
- **Update** `goals` status (on_track / at_risk / off_track) from measured actuals — reversible, L2.
- **Schedule** the recurring reporting run (weekly/monthly) — reversible, L2.
- **Pull** data from connected analytics/ad/CRM integrations — read-only, L2.
- **Prepare** (not execute) spend-reallocation or pause recommendations for approval — L1 draft.

## Human Approval Requirements
- **Changing, pausing, or reallocating ad spend** → ALWAYS founder approval + CFO runway check (money). The tracker recommends; it never moves budget.
- **Turning off / launching a campaign** → founder approval.
- **Changing integration configuration** (connecting/authorizing an ad or analytics account) → founder approval.
- Computing metrics, updating the internal dashboard, raising internal alerts, and updating goal status require no approval (L2, reversible, internal).

## Escalation Conditions
- **Acquisition unprofitable** (LTV:CAC < 1:1 or ROAS < 1.0 sustained) → founder + CFO agent; cash-at-risk framing.
- **Data conflict or attribution unreliable** for a spend decision → surface uncertainty to founder; do not recommend a spend change on bad data.
- **Metric can't be computed** because a source is disconnected/erroring → flag to founder + note in `integrations`.
- **Sustained funnel leak** no single skill can fix → escalate to `marketing-strategy-builder` / growth review.

## KPIs
This skill's own success = the measurement layer is trustworthy and timely:
- Coverage: % of active channels/funnel stages with a live, fresh metric.
- Alert precision: alerts that led to a real, useful action ÷ total alerts (low false-positive rate).
- Data freshness: age of the newest actual per metric within SLA.
- Decision support: % of marketing spend decisions backed by a current dashboard.
(Business outcomes it monitors — CAC, LTV:CAC, ROAS, funnel conversion, engagement/reach — are the KPIs of the channels/skills it measures, not of the tracker itself.)

## Monitoring
Continuously: threshold breaches, trend reversals, and data-source health (stale/erroring integrations). After any alert-driven action (e.g. a paused channel), monitor whether the metric recovers and record the outcome against the decision record so the Learning layer can compare expected vs. actual.

## Follow-Up
- **Time-triggered:** scheduled weekly (social/funnel) and monthly (economics) runs; feeds the monthly business/growth review.
- **Event-triggered:** a new channel/campaign goes live, a content cycle ships, spend changes, or a source integration reconnects.

## Related Skills
- `channel-selection` — receives channel verdicts (scale/keep/watch/pause) and reallocation recommendations.
- `website-conversion-audit` — receives an Interest/Action funnel-leak signal.
- `social-content-planner` — receives engagement/reach alerts and the reuse/drop signal.
- `marketing-funnel-planner` — receives stage-conversion diagnostics.
- `marketing-strategy-builder` — consumes the scorecard to adjust the dated plan.
- CFO/finance skills — share CAC/LTV and any spend-at-risk escalations.

## Guardrails
- Never fabricate a metric; mark missing inputs and their required source. Label estimates as estimates.
- Clearly tag which metrics are SOURCE vs. CLAUDE-DERIVED, and label default thresholds as configurable defaults, not source truths.
- Never move, pause, or reallocate spend autonomously — all budget changes are founder-approved and CFO-checked.
- Report per-channel ROAS with attribution caveats; prefer blended figures when attribution is unreliable.
- Respect data sensitivity: customer-level data stays internal; do not export PII in dashboards; margin/finance figures are confidential.
- Provisional targets must be labeled and confirmed before a "miss" is treated as failure.

## Example
**Founder input:** "Give me the August marketing dashboard for the meal-prep subscription. I spent $1,500 on video ads. Are they working?" Provided: funnel {awareness 40,000 impressions → interest 1,600 site visits → desire 480 added-to-cart → action 96 first orders → retention 70}; acquisition {sales+marketing spend $2,100 (incl. $1,500 ads), ad_attributed_revenue $2,880, new_customers 96, AOV $60, purchase_frequency 6/yr, avg_lifespan 1.5 yr, gross_margin 40%}; goal: profitable acquisition.

**Skill reasoning (computed):**
- Funnel conversions: awareness→interest 4.0%; interest→desire 30%; desire→action 20%; action→retention 73%. Overall (action ÷ awareness proxy) leak is steepest at **awareness→interest (4.0%)** — top-of-funnel creative/targeting, but also the action stage (20% cart→order) is a friction candidate.
- CAC = $2,100 ÷ 96 = **$21.9** (blended). Revenue-LTV = $60 × 6 × 1.5 = $540; margin-LTV = $540 × 0.40 = **$216**. LTV:CAC (margin) = 216 ÷ 21.9 ≈ **9.9:1** → healthy (≥3:1). ROAS = $2,880 ÷ $1,500 = **1.92** → above 1.0, above margin break-even (~2.5 would be needed for 40% margin to fully cover — flag: ROAS 1.92 covers ad cost but margin-adjusted contribution is thin; watch).
- Status: LTV:CAC healthy; ROAS needs_attention (below margin break-even of ~2.5 for 40% margin — [CLAUDE-DERIVED note]); awareness→interest flagged as priority leak.

**Alerts (abridged):**
- WARNING — ROAS 1.92 below ~2.5 margin break-even; recommended_action: tighten targeting / improve ad creative before scaling; routed_to `channel-selection` + `social-content-planner`; needs_approval (any spend change) = true.
- INFO/leak — awareness→interest 4.0% is the funnel's weakest step; routed_to `website-conversion-audit` (landing page) + `social-content-planner` (ad creative).

**Executed vs. approval:** Computed the full scorecard, appended August actuals to `metrics`, updated the "profitable acquisition" goal to `at_risk` (thin margin ROAS), and raised the two internal alerts — all at L2, no approval. The **recommendation to change ad targeting/spend was prepared and routed for founder approval + CFO check**; the tracker did not alter the budget itself. CAC/LTV/ROAS were tagged CLAUDE-DERIVED and the margin-break-even threshold labeled a default.

## Provenance
**SYNTH.** The engagement/reach/CTR/referral/conversion metric definitions and the metric-goal alignment and "prioritize reach/traffic over vanity likes" rules are SOURCE-DERIVED from the Marketing & Customer domain knowledge. The funnel conversion-rate, CAC, LTV, LTV:CAC, and ROAS formulas, and all numeric threshold bands, are **CLAUDE-DERIVED** additions the source material did not include — flagged per-metric throughout so downstream agents know which figures are source-grounded vs. Claude-supplied. See internal/PROVENANCE_MAP.md.
