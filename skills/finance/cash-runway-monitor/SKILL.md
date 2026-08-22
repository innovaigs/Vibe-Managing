---
name: cash-runway-monitor
domain: finance
version: 0.1.0
autonomy_ceiling: L2
provenance: SOURCE
reads: [finance.position, finance.accounts, finance.cash_flow, finance.income_statement, company]
writes: [finance.position, decisions]
related_skills: [cash-flow-diagnostic, financial-forecast-builder, working-capital-optimizer, scenario-and-sensitivity-analysis]
owned_by_agents: [cfo-agent, business-analyst-agent]
---

# Skill: Cash Runway Monitor

## Purpose
Continuously track burn rate, months of runway, and the projected out-of-cash date, and raise tiered alerts as runway shortens — so the founder is warned early enough to raise capital, cut burn, or accelerate collections while options still exist. This is a survival-critical monitoring skill.

## When to Use
- "How long until we run out of cash?"
- "What's our burn rate / when do we go to zero?"
- "Alert me before cash gets dangerous."
- Standing monthly (or weekly for tight runways) monitoring of a pre-revenue or cash-negative business.
- After `cash-flow-diagnostic` shows sustained negative operating cash flow.

## When NOT to Use
- Explaining *why* profit and cash diverge → `cash-flow-diagnostic`.
- Building a full driver-based multi-statement projection → `financial-forecast-builder`.
- Stress-testing runway under multiple assumption bundles → `scenario-and-sensitivity-analysis` (this skill hands off to it).
- Deciding whether to actually raise debt/equity → founder decision; this skill informs it, it does not execute financing.

## Required Context
- Current cash + marketable securities on hand. Read from `finance.accounts`, `finance.position`.
- Recent monthly cash operating expenses and cash revenue (last 1–3 months for averaging). Read from `finance.income_statement`, `finance.cash_flow`.
- Any known upcoming lumpy inflows/outflows (tax payment, loan draw, large invoice) for adjusted runway.
- Alert threshold policy (default healthy >12 mo, warning 6–12 mo, critical <6 mo). Read from `company` config.

## Inputs
```yaml
input:
  cash_on_hand: number                    # cash + marketable securities
  stage: enum[pre_revenue, post_revenue]
  monthly_cash_opex: number               # recurring cash operating outflows
  monthly_cash_revenue: number            # 0 for pre_revenue
  averaging_window_months: integer        # months of history to average burn (default 3)
  history:                                 # optional, for averaged/trended burn
    - {month: string, cash_opex: number, cash_revenue: number, ending_cash: number}
  known_future_flows:                      # optional lumpy items
    - {month: string, description: string, amount: number}   # + inflow / − outflow
  thresholds:                              # alert bands in months
    healthy_min: number                    # default 12
    critical_max: number                   # default 6
  as_of_date: string
```

## Missing Information Protocol
- If `monthly_cash_opex`/`monthly_cash_revenue` are missing, compute from `history` averaged over the window; if no history, ask the founder for the last full month's cash outflows and inflows in ONE batch.
- If `cash_on_hand` is stale, refresh from `finance.accounts`; never estimate the current balance — request the current figure.
- If burn is volatile month to month, use the averaged burn AND report the single-worst-month burn as a conservative bound; state which is used.
- Do not silently assume zero for known future flows; ask if the founder mentioned any lumpy items.

## Diagnostic Questions
1. What is the current monthly burn (gross for pre-revenue; net for post-revenue)?
2. Is burn stable, rising, or falling over the averaging window?
3. How many months of runway remain at current burn, and on what date does cash hit zero?
4. Do any known lumpy inflows/outflows change the out-of-cash date?
5. Which alert band are we in, and how close to the next-worse band?
6. How much would burn have to fall (or revenue rise) to reach a safe runway?

## Analysis Framework
Compute burn, then runway, then out-of-cash date, then classify against thresholds and project the cash trajectory including lumpy flows.

- **Burn selection:** pre-revenue → gross burn = monthly cash opex. Post-revenue → net burn = monthly cash opex − monthly cash revenue (only a burn if positive; if revenue ≥ opex the business is cash-flow-positive and runway is effectively unlimited at current run-rate — report as such).
- **Trend:** compare current-month burn to the windowed average; flag rising burn (runway shrinks faster than a static calc implies).
- **Trajectory:** roll cash forward month by month subtracting net burn and applying known future flows; the first month ending cash ≤ 0 is the out-of-cash month.
- **Threshold classification:** map runway months to healthy/warning/critical bands.
- **Break-even distance:** how much revenue increase or opex cut reaches net burn = 0.

## Calculations
- **Gross burn (pre-revenue)** = monthly cash operating expenses.
- **Net burn (post-revenue)** = monthly cash opex − monthly cash revenue (report 0 / "cash-positive" if ≤ 0).
- **Averaged burn** = mean of the last N months' burn (window = averaging_window_months).
- **Runway (months)** = cash on hand / burn rate. (E.g., $24,000 / $3,000 = 8 months; if revenue cuts net burn to $1,000/mo → 24 months.)
- **Out-of-cash date** = as_of_date + runway months (calendar), refined by the month-by-month trajectory when lumpy flows exist.
- **Runway with lumpy flows** = smallest t such that cash_on_hand − Σ(net burn to month t) + Σ(future flows to month t) ≤ 0.
- **Revenue needed for safe runway** = opex − (cash_on_hand / target_runway_months) → minimum monthly revenue to hit the target band.
- **Burn cut needed for safe runway** = current burn − (cash_on_hand / target_runway_months).

**Alert thresholds (months of runway):** Healthy > 12 · Warning 6–12 · Critical < 6. (Configurable; defaults from source-aligned small-business norms.)

## Decision Rules
- IF runway > 12 months AND burn stable/falling → THEN healthy; report and continue monitoring.
- IF 6 ≤ runway ≤ 12 months → THEN WARNING; recommend a plan now (cut burn, accelerate collections, or begin fundraising — fundraising decision is the founder's); increase monitoring cadence.
- IF runway < 6 months → THEN CRITICAL; escalate to founder immediately with concrete options and their timelines; recommend `scenario-and-sensitivity-analysis` and `working-capital-optimizer`.
- IF burn is rising over the window → THEN recompute runway on current (not averaged) burn and warn that static runway understates the risk.
- IF net revenue ≥ opex → THEN business is cash-flow-positive; report unlimited runway at current run-rate but keep monitoring for reversal.
- IF a known future outflow (e.g., tax, balloon payment) pulls the out-of-cash date earlier → THEN alert on the adjusted date, not the static one.
- IF runway crosses from one band into a worse band since last run → THEN fire an alert even if the absolute level was already known.
- IF cash on hand or burn inputs are stale/uncertain → THEN request a refresh before publishing a runway figure (survival-critical accuracy).

## Procedure
1. Refresh cash on hand from `finance.accounts`; confirm as-of date.
2. Determine stage; compute current burn and averaged burn over the window; assess trend.
3. Compute runway months and out-of-cash date (static), then refine with the month-by-month trajectory including known future flows.
4. Classify against thresholds; detect any band crossing since the prior run.
5. Compute the revenue-increase and burn-cut needed to reach the safe band.
6. Emit the runway report; write `finance.position` (runway, burn) — L2 auto-update of internal metrics with notice.
7. Fire tiered alerts; on warning/critical, attach recommended handoffs and escalate per rules.

## Output
```yaml
output:
  as_of_date: string
  stage: enum[pre_revenue, post_revenue]
  cash_on_hand: number
  burn_rate_current: number
  burn_rate_averaged: number
  burn_trend: enum[rising, stable, falling, cash_positive]
  runway_months: number
  out_of_cash_date: string
  out_of_cash_date_adjusted: string          # with known lumpy flows
  alert_level: enum[healthy, warning, critical]
  band_crossed_since_last_run: boolean
  to_reach_safe_runway:
    target_months: number
    monthly_revenue_needed: number
    monthly_burn_cut_needed: number
  trajectory: list                           # [{month, ending_cash}]
  recommendations: list
  handoffs: list
```

## Recommendations
Runway extension levers, ordered by speed and reversibility: (1) accelerate collections / tighten working capital (fast, reversible → `working-capital-optimizer`); (2) cut discretionary burn (fast, reversible); (3) raise prices / accelerate revenue (medium); (4) raise debt or equity (slow, irreversible, founder decision). Always quantify each lever's runway impact in months. On critical runway, lead with the fastest cash-preserving actions and give the founder a clear decision window ("you have X weeks to act before options narrow").

## Execution Opportunities
- Auto-update `finance.position` runway/burn metrics each run (reversible, LOW; L2 — executed with notice).
- Refresh the cash dashboard and trend chart (reversible, LOW; L2).
- Fire internal alerts/reminders when a band is crossed or a threshold is approached (reversible, LOW; L2 — scheduling internal reminders is explicitly AI-ownable).
- Create internal tasks for recommended cash-preserving actions (reversible, LOW).
- Draft (not send) a fundraising-prep checklist or investor-update outline for the founder (reversible, LOW).

## Human Approval Requirements
- Monitoring, calculation, internal alerts, dashboard/metric updates, and task creation: AI-owned at L2 (reversible, low-risk, with notice).
- Raising debt or equity, drawing on a line of credit, or any money movement to extend runway: ALWAYS requires founder approval.
- Cutting a budget line or committing to spend changes: requires founder approval (budget commitment).
- Sending any external communication (investors, lenders, suppliers) about the cash position: requires founder approval.

## Escalation Conditions
- Runway < 6 months (critical) → founder immediately, with options and a decision deadline.
- Runway < 3 months or cash insufficient for next payroll → founder immediately (highest urgency) + recommend accountant.
- Rising burn with no clear cause → founder + run `cash-flow-diagnostic`.
- Any financing decision → founder + accountant.
- Stale/uncertain cash inputs → surface uncertainty; do not publish a runway number the founder might rely on.

## KPIs
- Alert lead time: warning fired with enough runway to act (target ≥ the time needed to raise capital or cut burn).
- Accuracy: projected out-of-cash date vs. actual trajectory (variance within tolerance).
- Zero missed band crossings.
- Founder acts on warning/critical alerts before the next-worse band.

## Monitoring
- Re-run monthly by default; weekly when runway < 6 months; on-demand after any large cash event.
- Watch for burn drift and revenue trend reversals.
- Track whether recommended levers actually extended runway as projected.

## Follow-Up
- Scheduled recurring run (cadence tied to alert level).
- Immediate re-run after any capital raise, large payment, or burn change.

## Related Skills
- `cash-flow-diagnostic` (why cash is leaving).
- `working-capital-optimizer` (fast cash-preserving lever).
- `scenario-and-sensitivity-analysis` (runway under downside cases).
- `financial-forecast-builder` (full forward projection and funding need).

## Guardrails
- Runway figures are survival-critical — never publish from stale or assumed cash inputs; refresh first.
- Always report both averaged and worst-month burn when burn is volatile; do not understate risk.
- Internal alerts and metric updates are AI-owned; any financing, spend change, or external communication is founder-approval-only.
- Cash-positive ≠ safe forever — keep monitoring for reversal.
- Confidential financial data; audited writes to permitted namespaces; sensitivity data stays confidential.

## Example
**Founder input:** "We have $180,000 in the bank. Last three months burned $28k, $31k, $34k. When do we run out, and what do I do?" Post-revenue; a $20,000 quarterly tax payment is due in month 2.

**Skill reasoning:** Burn is rising ($28k→$34k); averaged burn $31k, current $34k. Static runway on current burn = 180,000 / 34,000 = 5.3 months → CRITICAL. Trajectory with the $20k tax outflow in month 2: end M1 $146k, end M2 $92k (146 − 34 − 20), end M3 $58k, end M4 $24k, end M5 −$10k → out-of-cash mid-M5, but the tax payment and rising burn pull effective danger earlier. To reach a 12-month safe runway: monthly burn must fall to 180,000/12 = $15,000 (cut ~$19k) OR revenue must rise by ~$19k/mo. Band: critical, and burn is rising.

**Output:** alert_level critical, runway ~5.3 months (adjusted out-of-cash mid-M5 with tax), recommendations led by "cut ~$19k/mo burn or accelerate collections now; you have roughly 6–8 weeks to act before fundraising becomes forced." Handoffs: `working-capital-optimizer`, `scenario-and-sensitivity-analysis`.

**Executed vs. approval:** `finance.position` updated, critical alert fired to founder, cash-preservation tasks created (L2 with notice); any fundraising, budget cut, or lender/investor outreach held for founder approval.

## Provenance
SOURCE. Derives from the Statements & Ratios and Forecasting/Cash knowledge (burn-rate and runway framework — pre- vs. post-revenue burn, runway = cash ÷ burn, out-of-cash period, minimum-cash cushion, healthy/warning/critical runway bands). Branding stripped and generalized per PROVENANCE_MAP.
