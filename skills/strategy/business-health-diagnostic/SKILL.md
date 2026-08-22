---
name: business-health-diagnostic
domain: strategy
version: 0.1.0
autonomy_ceiling: L1
provenance: SYNTH
reads: [company, finance, customers, offerings, operations, team, market, metrics, risks, goals]
writes: [metrics, decisions, strategy]
related_skills: [opportunity-feasibility-analysis, growth-pathway-classifier, resource-gap-analysis, competitive-intelligence-analysis, strategic-planning, risk-diagnostic]
owned_by_agents: [orchestrator, strategy-agent]
---

# Skill: Business Health Diagnostic

## Purpose
Give the founder a single, honest, whole-company health scan — cash, revenue, margin, customers, operations, people, and risk — so they know what is actually well, what needs attention, and which capability to run next before making any big decision. This is the triage layer that routes the rest of the operating system.

## When to Use
- The founder asks an open, unscoped question: "How's the business doing?", "Where should I be worried?", "Give me the state of the company."
- On a scheduled cadence (monthly or quarterly) as a standing checkup.
- Immediately before a large or irreversible decision (raising money, hiring a senior role, signing a big lease, pursuing a new opportunity) to establish a baseline.
- After a shock (lost a major customer, a bad month, a crisis) to re-scan and re-rank priorities.

## When NOT to Use
- The founder already knows the problem and wants to act on ONE dimension (e.g., "fix my cash flow") — route straight to that specialist skill (cash-flow analysis, `growth-lever-selector`, etc.).
- A deep single-domain investigation is needed — this skill scans breadth, not depth; it hands off to the domain skill for depth.
- A specific opportunity needs validation — use `opportunity-feasibility-analysis`.

## Required Context
Reads the Business Digital Twin snapshot plus Business Memory namespaces: `company` (stage, model), `finance` (cash balance, runway, revenue trend, gross margin), `customers` (count, concentration, churn/retention), `offerings` (margin by line), `operations` (capacity, delivery reliability), `team` (headcount, key-person exposure), `market` (demand trend, competitive pressure), `metrics` (tracked KPIs with `as_of` freshness), `risks` (open register), `goals` (founder targets). Each fact carries `source`, `confidence`, and `as_of`; the diagnostic must weight stale/low-confidence facts accordingly and never treat a stale metric as current.

## Inputs
```yaml
input:
  as_of_date: date                 # the "today" the scan is anchored to
  lookback_months: int             # trailing window for trend calc (default 12)
  twin_snapshot: object            # computed live model (cash, runway, margins, retention)
  memory:
    finance:
      cash_on_hand: number
      monthly_burn: number         # net cash out per month
      monthly_revenue_series: [number]   # trailing series, oldest→newest
      gross_margin_pct: number
      ar_days: number              # avg days to collect receivables
    customers:
      active_count: int
      top_customer_revenue_pct: number   # % of revenue from largest customer
      retention_rate_pct: number
    offerings: [ {name: str, revenue_pct: number, gross_margin_pct: number} ]
    operations:
      capacity_utilization_pct: number
      on_time_delivery_pct: number
    team:
      headcount: int
      key_person_dependencies: [str]     # functions with a single point of failure
      open_critical_roles: [str]
    market:
      demand_trend: enum(rising, flat, declining, unknown)
      competitive_pressure: enum(low, moderate, high)
    risks_open_count: int
    goals: [ {metric: str, target: number, horizon: str} ]
  founder_stated_concerns: [str]    # optional: what the founder is already worried about
```

## Missing Information Protocol
1. Prefer to compute from the twin/integrations (accounting sync, CRM) before asking.
2. If a dimension's core inputs are missing, still score the other dimensions and mark the missing one `Insufficient-Data` (do not guess a status).
3. Batch at most ONE concise question set to the founder, listing only the highest-leverage gaps (e.g., "I don't have cash-on-hand or churn — can you confirm both?").
4. Never assume: cash balance, runway, churn, or margin. A fabricated number here misroutes the whole company. Flag any dimension scored on data older than the lookback window as `low-confidence`.

## Diagnostic Questions
Answered internally per dimension:
- **Cash:** How many months of runway at current burn? Is AR collection healthy (<45 days)? Is cash trending up or down?
- **Revenue:** Is revenue growing, flat, or declining vs. the trailing window? Does the shape look like a plateau (see `growth-pathway-classifier`)?
- **Margin:** Is gross margin healthy for the model? Which offering lines are dragging it down?
- **Customers:** How concentrated is revenue in the top customer? Is retention holding? Are new customers replacing lost ones?
- **Operations:** Is the business at, over, or under capacity? Is delivery reliable?
- **People:** Where is key-person risk? Are critical roles open? Is the founder working *on* vs. *in* the business?
- **Risk:** Are top risks owned, mitigated, and tracked, or is the register stale/empty?
- **Founder fit:** Do the founder's stated concerns match where the data says the problems are? (Mismatch is itself a finding.)

## Analysis Framework
A seven-dimension scan; each dimension gets a status via threshold rules, then findings are ranked by severity × leverage, then mapped to a next-skill.

**Dimensions:** Cash · Revenue · Margin · Customers · Operations · People · Risk.

**Status scale (per dimension):**
- **Healthy** — meets or beats threshold; no action.
- **Needs-Attention** — early warning; monitor and plan.
- **At-Risk** — threshold breached; act this quarter.
- **Critical** — existential or urgent; act now.
- **Insufficient-Data** — cannot be scored; close the data gap first.

**Ranking:** severity_rank (Critical=4, At-Risk=3, Needs-Attention=2, Healthy=1) × leverage (does fixing this unblock other dimensions? cash and customer concentration are high-leverage). Ties broken by reversibility of the underlying problem (harder-to-reverse first). Governed by the dashboard triad: Accountability | Alignment | Performance.

## Calculations
- **Runway (months)** = `cash_on_hand / monthly_burn`. Thresholds: Healthy ≥6, Needs-Attention 3–6, At-Risk 1.5–3, Critical <1.5. (If cash-flow positive, runway is not the binding constraint — mark Healthy and note.)
- **Revenue trend %** = `(latest_month − month_n_periods_ago) / month_n_periods_ago × 100` over the lookback window. Healthy >0 and tracking to plan; Needs-Attention flat (−2% to +2%, possible plateau); At-Risk sustained decline (−2% to −15%); Critical decline >15% or accelerating.
- **Gross margin %** = `(revenue − COGS) / revenue × 100`. Compare to the offering's target margin from memory; Needs-Attention if within 5 pts below target, At-Risk if 5–15 pts below, Critical if >15 pts below or negative.
- **Customer concentration** = `top_customer_revenue_pct`. Healthy <15%, Needs-Attention 15–25%, At-Risk 25–40%, Critical >40% (single-customer dependency).
- **Retention** = `retention_rate_pct`. Interpret against model; Needs-Attention if 5 pts below prior period, At-Risk if 10–20 pts below, Critical if >20 pts below or net customer count declining.
- **AR days** = `ar_days`. Healthy <45, Needs-Attention 45–60, At-Risk 60–90, Critical >90.
- **Capacity utilization** = `capacity_utilization_pct`. Healthy 70–90%; Needs-Attention <60% (underused) or 90–100%; At-Risk >100% (over capacity → quality/burnout risk, an episodic-growth signal).
- **Survival base-rate context (expectation-setting only, not a target):** roughly half of new businesses survive 5 years and a third survive 10 — use to calibrate the founder's expectations, never as a KPI.

## Decision Rules
- **IF** runway < 1.5 months **THEN** Cash = Critical; this becomes the #1 finding regardless of other scores; recommend cash-flow analysis + founder alert.
- **IF** revenue is flat within ±2% over the lookback **THEN** flag possible plateau and recommend `growth-pathway-classifier`.
- **IF** revenue declining >15% **THEN** Revenue = Critical; recommend `growth-pathway-classifier` then `growth-lever-selector`.
- **IF** top customer > 40% of revenue **THEN** Customers = Critical (concentration); recommend `growth-lever-selector` (diversify) + `risk-diagnostic`.
- **IF** gross margin > 15 pts below target or negative **THEN** Margin = At-Risk/Critical; recommend margin/pricing review + `initiative-prioritization`.
- **IF** capacity utilization > 100% AND revenue rising **THEN** Operations = At-Risk (episodic-growth constraint); recommend `resource-gap-analysis`.
- **IF** a critical function has a single key-person dependency **THEN** People = At-Risk; recommend `resource-gap-analysis` + `risk-diagnostic`.
- **IF** risk register is empty or stale (>6 months) **THEN** Risk = Needs-Attention minimum; recommend `risk-diagnostic`.
- **IF** founder_stated_concerns do NOT match the top data-driven finding **THEN** surface the mismatch explicitly as a finding (perception vs. reality gap).
- **IF** a dimension is Insufficient-Data **THEN** the first recommended action is to close that data gap, not to act on a guess.
- **IF** two or more dimensions are Critical **THEN** escalate to founder immediately with a triage summary rather than a full report.

## Procedure
1. Load twin snapshot + memory namespaces; record `as_of` freshness per fact.
2. Compute every metric in Calculations for the lookback window.
3. Assign a status to each of the seven dimensions via Decision Rules / thresholds.
4. Mark any dimension lacking core inputs as Insufficient-Data; batch one question set if the gaps are high-leverage.
5. Rank findings by severity × leverage; break ties by reversibility.
6. For each non-Healthy finding, map to the next skill to run and a one-line "why."
7. Compare founder_stated_concerns to the ranked findings; note any mismatch.
8. Assemble the output: overall health grade, ranked findings, recommended skill sequence, and data gaps.
9. Write a health snapshot to `metrics` and a decision record to `decisions`; propose (do not auto-run) the recommended next skills.

## Output
```yaml
output:
  as_of_date: date
  overall_health: enum(Healthy, Needs-Attention, At-Risk, Critical)
  overall_summary: str                    # 2-3 sentence EEC plain-language verdict
  dimensions:
    - name: enum(Cash, Revenue, Margin, Customers, Operations, People, Risk)
      status: enum(Healthy, Needs-Attention, At-Risk, Critical, Insufficient-Data)
      metric_value: number
      threshold_note: str
      finding: str                        # what this means for the founder
      confidence: enum(high, medium, low) # driven by data freshness
  ranked_findings:
    - rank: int
      dimension: str
      severity: enum(Critical, At-Risk, Needs-Attention)
      leverage: enum(high, medium, low)
      why_it_matters: str
      recommended_skill: str              # the skill to run next
  perception_gap: str                     # founder concern vs. data reality, or "aligned"
  data_gaps: [ {dimension: str, missing: str, source_to_close: str} ]
  recommended_sequence: [str]             # ordered list of skills to run
```

## Recommendations
Findings are ranked by severity × leverage, then reversibility. High-leverage fixes (cash, customer concentration) are surfaced first because they unblock other dimensions. Each recommendation names the exact next skill and the one-line reason, so the founder can approve a sequence rather than re-explaining context. Recommendations are proposals only — this skill diagnoses and routes; it does not execute business changes.

## Execution Opportunities
- Write the health snapshot to `metrics` and a decision record to `decisions` — reversible, LOW risk, auto at L2 (proposed at L1 ceiling here).
- Create internal tasks for each ranked finding (e.g., "Run growth-pathway-classifier") — reversible, LOW.
- Draft a founder briefing summarizing the scan — reversible, LOW.
- Schedule the next cadence scan as an internal reminder — reversible, LOW.
This skill never executes the recommended business changes themselves; it only prepares and routes.

## Human Approval Requirements
- No irreversible or external action is taken by this skill. Writing internal snapshots/tasks at L1 is prepared and shown to the founder.
- Any recommended downstream skill that would touch money, contracts, employees, or external comms carries its own approval requirements — this skill only proposes running it.
- Per `AUTONOMY_AND_APPROVAL_MODEL.md`, two-or-more Critical dimensions triggers an immediate founder alert before proceeding.

## Escalation Conditions
- **Cash Critical (runway <1.5 mo) or ≥2 Critical dimensions** → escalate to founder immediately (+ recommend accountant for cash).
- **Margin/financial anomaly that implies a bookkeeping error** → founder + accountant.
- **Data conflict or pervasive low-confidence inputs** → surface uncertainty to founder; do not issue a confident verdict.
- **A finding implying legal/regulatory or employment exposure** → note and route to the appropriate specialist skill (legal/HR), do not advise directly.

## KPIs
- Time-to-first-insight for the founder (scan completes and routes in one pass).
- Precision of routing: % of recommended next-skills the founder accepts and runs.
- Early-warning value: % of Critical findings raised at least one cycle before they became crises.
- Data-freshness coverage: % of dimensions scored on data within the lookback window.

## Monitoring
After the scan: track whether recommended skills were run and whether flagged dimensions improved by the next cadence. Watch that any dimension marked Insufficient-Data gets its data gap closed. Re-verify Critical findings on fresh data before they drive irreversible action.

## Follow-Up
- Time-triggered: monthly for early-stage/at-risk businesses, quarterly for stable ones.
- Event-triggered: before any major/irreversible decision, after a shock, or when any tracked warning metric breaches its threshold.

## Related Skills
Routes to: `growth-pathway-classifier`, `growth-lever-selector`, `resource-gap-analysis`, `competitive-intelligence-analysis`, `risk-diagnostic`, `opportunity-feasibility-analysis`, and feeds `strategic-planning` and `initiative-prioritization` with a prioritized problem list.

## Guardrails
- Never present a stale or low-confidence metric as current fact; always attach a confidence flag.
- Never fabricate cash, runway, margin, or churn — mark Insufficient-Data instead.
- This is a diagnostic, not advice on regulated matters (tax, legal, investment) — route those to specialists.
- Do not expose `restricted` data (individual compensation, employee performance) in the founder-facing summary beyond aggregate signals.
- The base-rate survival statistics are for expectation-setting only, never presented as targets or predictions about this specific business.

## Example
**Founder input:** "How's the business doing? I'm mostly worried we're not marketing enough."
**Data (twin + memory):** cash $48k, burn $32k/mo → runway 1.5 mo; revenue series flat (~$40k/mo, +1% over 12 mo); gross margin 41% vs. 55% target; top customer = 47% of revenue; retention 88%; capacity 72%; one key-person dependency (founder does all fulfillment); risk register empty.
**Reasoning:** Cash = Critical (runway 1.5 mo). Customers = Critical (47% concentration). Margin = At-Risk (14 pts below target). Revenue = Needs-Attention (plateau). People = At-Risk (key-person). Risk = Needs-Attention (empty register). Operations/Ops = Healthy. Founder's stated concern (marketing) does NOT match the top findings — perception gap flagged.
**Output (abridged):** overall_health = Critical. Ranked findings: (1) Cash Critical → cash-flow analysis + founder alert; (2) Customer concentration Critical → `growth-lever-selector` to diversify + `risk-diagnostic`; (3) Margin At-Risk → pricing/margin review; (4) Revenue plateau → `growth-pathway-classifier`. Perception gap: "You're focused on marketing, but the binding constraints are 1.5 months of runway and 47% revenue in one customer — those come first." Recommended sequence: [cash-flow analysis, risk-diagnostic, growth-pathway-classifier, growth-lever-selector].
**Executed vs. approval:** Wrote health snapshot to `metrics`, drafted the founder briefing and internal tasks (L1, shown for approval). Sent immediate founder alert for the two Critical dimensions. No business change executed — all routed.

## Provenance
SYNTH. Recombines the source's Three-Lens Business Dashboard (YOU / YOUR BUSINESS / YOUR ENVIRONMENT), the dashboard governance triad (Accountability | Alignment | Performance), the four common owner challenges (customers, employees, strategy, financing), the plateau signal from the Four Pathways to Growth, and the business-survival base rates — assembled into a cross-domain triage scan not present as a single tool in the source. See `internal/PROVENANCE_MAP.md`.
