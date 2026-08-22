# OPERATING_CADENCE

**Deliverable 13 — Daily / weekly / monthly / quarterly management system.**

Vibe Managing runs the company on a rhythm so nothing important is missed and the founder is never buried in dashboards. Each cadence cycle assembles itself automatically from live business data (Business Memory + Digital Twin + Business Health Engine) and presents the founder with *decisions and attention items*, not raw numbers.

Home: `core/cadence/`. Cadence cycles are scheduled jobs that call the Business Analyst agent to assemble briefings and the owning agents to prepare actions.

---

## The rhythm

Every cadence is configured by the adaptation layer. A high-volume restaurant may inspect labor, waste, cash, service, and safety daily; a project-services firm may center weekly capacity, backlog, realization, scope, and receivables; a SaaS company may center product reliability, activation, retention, recurring revenue, and acquisition economics. The cadence engine composes the active industry and business-model profiles instead of forcing one universal dashboard.

| Cadence | Question it answers | Who assembles | Founder time |
|---|---|---|---|
| **Continuous** | "Did something just break?" | Health Engine | only when alerted |
| **Daily** | "What needs my attention today?" | Business Analyst | ~2 min |
| **Weekly** | "What changed this week?" | Business Analyst + function agents | ~15 min |
| **Monthly** | "How is the company performing?" | CFO + Growth + Analyst | ~45 min |
| **Quarterly** | "Are we executing the strategy?" | Strategy + all agents | ~half day |
| **Annual** | "Where are we going next?" | Strategy + founder | planning session |

---

## Continuous — event monitoring & alerts
- The Health Engine evaluates indicators as data arrives (a payment lands, a deal moves, an expense posts).
- 🟠/🔴 breaches or anomalies trigger an immediate, explained alert with pre-drafted corrective actions (held for approval).
- Cash, covenant, and irreversible-risk indicators are always live.
- Everything else is batched into the daily brief to avoid noise.

## Daily — "What needs my attention today?"
Assembled each morning:
```
1. Anything 🔴/🟠 since yesterday (with cause + recommended action)
2. Cash position + runway delta
3. Today's decisions awaiting approval (ranked, with recommendation)
4. Commitments/deadlines due today (from ops/people/sales)
5. What the system did autonomously in the last 24h (reversible actions log)
```
Output is a short, ranked list. If nothing needs attention, it says so in one line.

## Weekly — "What changed this week?"
```
1. Scorecard: key metrics vs. last week vs. target (cash, revenue, pipeline, delivery, capacity)
2. Wins & regressions (what moved and why — variance-diagnosis on notable changes)
3. Pipeline & forecast: coverage, conversion, at-risk deals
4. Operations: delivery/SLA, bottleneck load, defects
5. People: capacity, open roles, founder-load index
6. Initiatives: on-track / slipping (from the growth plan)
7. Decisions needed this week (ranked, with recommendations)
8. Next-best-actions the system recommends
```
Each function agent contributes its slice; the Business Analyst consolidates.

## Monthly — "How is the company performing?"
Anchored by the **forecast-vs-actual review** (the learning loop):
```
1. Financial close review: P&L, balance sheet, cash flow vs. forecast
2. Variance analysis: classify every material variance, identify Top Movers, diagnose root cause
   (favorable cost variance is checked against activity — cheap-because-stalled is flagged, not celebrated)
3. Ratio & health panel: liquidity/leverage/profitability/efficiency vs. benchmarks & covenants
4. KPI dashboard: leading + lagging indicators vs. targets
5. Customer review: acquisition, churn, concentration, LTV:CAC
6. Marketing & sales: channel performance, CAC, funnel, win rate
7. Operations: throughput, cycle time, capacity trends
8. Learning: update assumptions where actual diverged from expected; record lessons
9. Re-forecast: adjust the forward model; surface funding-needed changes
10. Reprioritize: adjust initiatives for next month
```
Feeds the `monthly-business-review` and `variance-diagnosis` skills; writes lessons to the Decision store.

## Quarterly — "Are we executing the strategy?"
```
1. Strategy review: progress on objectives & priorities vs. plan
2. Growth-plan refresh: initiative outcomes (expected vs. actual impact), reprioritize
3. Financial re-forecast & budget re-baseline for the quarter ahead
4. Market & competitive update: threats, opportunities, positioning
5. Org & capacity review: hiring plan vs. growth, founder-load, structure
6. Risk review: register update, concentration, continuity
7. Resource allocation: shift attention/budget to highest-value work
8. Decisions: kill/scale/start initiatives; set next quarter's priorities
```

## Annual — "Where are we going next?"
```
1. Full-year performance vs. goals + lessons synthesis
2. Vision & mission check; multi-year direction
3. Next-year goals, growth plan, budget, and hiring plan
4. Valuation & value-driver review; exit-readiness alignment (if relevant)
5. Big-bet decisions (markets, products, capital)
```

---

## How briefings assemble themselves

```
scheduled trigger → Business Analyst pulls health_snapshot + relevant twin views
  → each owning agent contributes its section + prepares risk-tiered actions
  → Analyst consolidates, de-duplicates, ranks by impact
  → present to founder: findings → what was done → decisions needed (with recommendations)
  → founder decisions execute via the control plane
  → outcomes + lessons written to memory → next cycle starts smarter
```

## Configuration
- Cadence times, timezone, and which sections appear are set in `core/cadence/cadence.config.yaml`.
- A founder can invoke any cadence on demand ("give me the weekly now") or ask the underlying question directly ("what should I focus on today?").
- Quiet by default: cycles with nothing material to report collapse to a one-line "all healthy" so the rhythm never becomes noise.
- At least quarterly—and whenever the model, geography, ownership, regulation, or lifecycle changes—the Adaptation Agent revalidates the company archetype, profiles, maturity, jurisdictions, metric definitions, specialist gates, and autonomy limits.
