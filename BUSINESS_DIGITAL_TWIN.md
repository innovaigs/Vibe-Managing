# BUSINESS_DIGITAL_TWIN

**Deliverable 9 — Business representation model.**

The Business Digital Twin is a live, computed model of the company that agents reason over. Where **Business Memory** stores *facts and history*, the Twin is the *working simulation of the current business*: objects, their relationships, the events that change them, the metrics they produce, and the states they are in.

The purpose: let an agent ask "what happens to runway if we hire two people?" or "which customer concentration puts revenue at risk?" and get an answer computed from the actual company — not a generic template.

---

## What the twin is

- A **graph of business objects** (nodes) connected by **relationships** (edges).
- Each object has **attributes**, a **state**, and **metrics**.
- Objects change through **events**.
- **Derived views** (runway, health, capacity, concentration) are computed continuously from the graph.
- The twin is **queryable** ("show me every process that depends on this one employee") and **simulatable** ("apply this hiring plan and recompute cash").

```
            ┌───────────────────── BUSINESS DIGITAL TWIN ─────────────────────┐
            │  Objects (nodes) ── Relationships (edges) ── State ── Metrics    │
   Memory   │        ▲                                              │          │
  (facts) ──┼────────┘   events update the graph                   ▼          │
            │  Derived views: runway · health · capacity · concentration · … │
            └──────────────────────────────────────────────────────────────┘
                         ▲ agents query & simulate ▼
```

## 1. Objects (node types)

| Object | Represents | Key attributes | Key metrics |
|---|---|---|---|
| `Company` | the business | stage, model, mission | overall health score |
| `Founder` | owner(s) | leadership style, time allocation | over-extension index |
| `Customer` / `Segment` | who pays | segment, status, health | LTV, churn, concentration |
| `Offering` | product/service | price, cost, lifecycle | gross margin, revenue share |
| `RevenueStream` | a way money comes in | model, recurrence | MRR/ARR, growth rate |
| `CostItem` | a way money leaves | fixed/variable, category | % of revenue, trend |
| `CashAccount` | money on hand | balance | runway contribution |
| `Employee` / `Role` | the team | function, authority level, capacity | utilization, cost |
| `Process` | how work gets done | steps, owner, cycle time | throughput, bottleneck flag |
| `Tool` / `Vendor` | operational dependencies | cost, criticality | dependency risk |
| `Pipeline` / `Deal` | future revenue | stage, value, probability | weighted pipeline, conversion |
| `Campaign` / `Channel` | demand generation | spend, stage | CAC, ROAS, contribution |
| `Initiative` | a growth/strategic bet | hypothesis, owner, status | expected vs actual impact |
| `Goal` | a target | metric, target, deadline | on-track status |
| `Risk` | a threat | likelihood, impact | risk score |
| `Decision` | a choice made | expected/actual outcome | variance |
| `IndustryProfile` / `BusinessModelProfile` | active operating assumptions | version, overrides, evidence | fit confidence |
| `ProductBet` / `DiscoveryEvidence` | product outcome and uncertainty | hypothesis, evidence, lifecycle | adoption, retention, contribution |
| `CustomerSuccessPlan` | customer value realization | milestone, risk, owner | time-to-value, health |
| `Supplier` / `InventoryItem` / `LogisticsNode` | supply network | lead time, capacity, policy | service, turns, landed cost |
| `TechnologyService` / `DataProduct` | digital and analytical capability | owner, tier, lineage, SLO | availability, quality, cost |
| `SecurityControl` / `PrivacyActivity` | protection and processing | coverage, owner, review | exposure, compliance |
| `QualityControl` / `CorrectiveAction` | conformance and improvement | standard, evidence, status | yield, recurrence |
| `Project` / `Program` / `Benefit` | change delivery | dependencies, resources, baseline | predictability, realized value |
| `Policy` / `BoardAction` | governance mechanism | authority, version, due date | compliance, closure |
| `Jurisdiction` / `SustainabilityImpact` | external context and effect | obligations, exposure, evidence | risk, intensity, outcome |

## 2. Relationships (edges)

```
Offering        —generates→        RevenueStream
Customer        —buys→             Offering
Segment         —contains→         Customer
RevenueStream   —funds→            CashAccount
CostItem        —drains→           CashAccount
Employee        —reports_to→       Employee
Employee        —owns→             Process
Process         —depends_on→       Process | Tool | Vendor | Employee
Process         —delivers→         Offering
Pipeline/Deal   —converts_to→      Customer
Campaign        —feeds→            Pipeline
Initiative      —targets→          Goal
Initiative      —affects→          RevenueStream | CostItem | Process | Employee
Risk            —threatens→        (any object)
Decision        —authorizes→       Initiative | action
```

These edges are what let the twin answer cross-functional questions — e.g. "a hiring decision affects runway" is `Employee —drains→ CashAccount`, and "a marketing decision affects cash" is `Campaign —drains→ CashAccount` while `Campaign —feeds→ Pipeline —converts_to→ Customer —buys→ Offering —generates→ RevenueStream —funds→ CashAccount`.

## 3. States

Each object carries a lifecycle state and a health state.

- **Lifecycle** (object-specific): e.g. `Deal: {lead, qualified, proposal, won, lost}`; `Initiative: {proposed, active, paused, done, abandoned}`; `Offering: {new, growth, mature, declining}`.
- **Health** (universal 4-band, aligned with the Business Health Engine): `Healthy | Needs Attention | At Risk | Critical`.

## 4. Events (what changes the graph)

Events are the append-only stream that mutates the twin and feeds the Learning layer.

```yaml
event:
  id, timestamp, type, source(integration|agent|founder)
  object_ref, change: {attribute, from, to}
  caused_by: decision_id | action_id | external
```

Examples: `payment_received`, `invoice_raised`, `deal_stage_changed`, `employee_hired`, `expense_recorded`, `campaign_launched`, `churned`, `process_changed`, `metric_updated`.

## 5. Derived views (computed, not stored)

The twin continuously recomputes cross-object views agents rely on:

| View | Computed from | Answers |
|---|---|---|
| **Cash & runway** | CashAccounts, RevenueStreams, CostItems | "How long until we run out?" |
| **Profitability map** | Offerings, RevenueStreams, CostItems | "Which offerings actually make money?" |
| **Customer concentration** | Customers, RevenueStreams | "How exposed are we to one customer?" |
| **Capacity & bottlenecks** | Employees, Processes | "What limits how much we can deliver?" |
| **Pipeline coverage** | Pipeline, Goals | "Is there enough pipeline to hit the target?" |
| **Founder load** | Founder, Processes, Employees | "What is only the founder doing?" |
| **Health rollup** | all object health states | "What needs attention right now?" |
| **Growth-plan progress** | Initiatives, Goals, metrics | "Are we executing the strategy?" |
| **Context fit** | Profiles, overrides, maturity, jurisdictions | "Are we using the right operating logic?" |
| **Product & customer value** | ProductBets, Customers, SuccessPlans | "Are customers adopting and realizing value?" |
| **Supply resilience** | Suppliers, Items, Nodes, Risks | "Where can demand or supply fail?" |
| **Technology, data & security** | Services, DataProducts, Controls | "Can the digital operating layer be trusted?" |
| **Change portfolio** | Projects, Programs, Benefits, Capacity | "Are initiatives creating the promised value?" |

## 6. Simulation (the twin's superpower)

Agents can fork the twin, apply a proposed change, and recompute — without touching reality.

```
simulate(twin, change_set) → projected_twin, deltas
```

Examples:
- **Hiring:** add 3 `Employee` nodes with cost + ramp → recompute runway, capacity, break-even.
- **Pricing:** change an `Offering.price` → recompute margin, revenue, expected churn sensitivity.
- **Growth initiative:** apply an `Initiative`'s expected impact → project revenue/cash path and compare to the goal.

Simulation results become the `projected_outcome` in a Decision record; the Learning layer later compares them to `actual_outcome`.

## 7. Permissions & memory

- The twin inherits **sensitivity** from the underlying memory records (individual `Employee` comp is `restricted`).
- Agents query the twin only within their role's read scope.
- The twin never writes to reality directly — proposed changes go through the **autonomy/approval** control plane; only executed actions produce events that update the twin.

## 8. Update mechanisms

1. **Integrations** stream external events (a payment in the bank, a deal moved in the CRM) → twin updates.
2. **Agent analysis** writes computed attributes (e.g. a health score, a bottleneck flag).
3. **Founder input** confirms or corrects facts.
4. **Decisions/actions** produce events on execution.

Freshness and confidence propagate from memory: a view computed from stale inputs is itself flagged stale, and agents must surface that when acting.

## 9. Schema

Machine-readable node/edge/event schemas live in `schemas/digital-twin.schema.json`. The twin can be backed by a graph store, a relational store with a graph view, or an in-memory model for a single company — the specification is storage-neutral.
