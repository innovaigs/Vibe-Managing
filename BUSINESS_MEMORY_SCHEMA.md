# BUSINESS_MEMORY_SCHEMA

**Deliverable 8 — Persistent company memory.**

Business Memory is the durable, structured record of everything Vibe Managing knows about a company. It is what makes agents reason about *this* business instead of answering generic questions. Memory is read by every skill and written back after every decision and outcome.

Memory is **facts and history**. The **Business Digital Twin** (see `BUSINESS_DIGITAL_TWIN.md`) is the *live, computed model* built on top of these facts. Memory is the ground truth; the twin is the working model.

Canonical machine-readable schemas live in `schemas/` (JSON Schema). This document is the human-readable specification.

---

## Design principles

- **Every fact has provenance and freshness.** Each record carries `source`, `confidence`, `as_of`, and `verified_by`. Agents must know how stale or certain a fact is before acting on it.
- **Append-only history for anything that changes.** Metrics, decisions, and states are versioned, never silently overwritten — the Learning layer depends on history.
- **IDs and relationships, not prose.** Entities reference each other by id so the twin can traverse them.
- **Privacy tiers.** Every record has a `sensitivity` (`public | internal | confidential | restricted`). Restricted (e.g. individual compensation, employee performance) is access-gated and never leaves the system without explicit approval.

## Top-level namespaces

```
company · adaptation · founders · customers · offerings · product · customer_success · finance · team ·
operations · supply_chain · technology · data · security_privacy · quality · projects · governance ·
international · sustainability · market · strategy · metrics · decisions · goals · risks · integrations
```

---

## 1. Company

```yaml
company:
  id: str
  legal_name: str
  dba: str
  entity_type: enum(sole_prop, llc, s_corp, c_corp, partnership, nonprofit, other)
  formation_date: date
  jurisdictions: [str]
  ein_ref: secret_ref              # never stored in plaintext
  mission: str
  vision: str
  values: [str]
  business_model: str              # how it makes money
  revenue_model: enum(one_time, recurring, usage, retainer, mixed, ...)
  stage: enum(startup, established, scaling, mature)
  locations: [ {id, type, address_ref, headcount} ]
  industry: {naics: str, sector: str}
  provenance: {source, as_of, confidence}
```

## 2. Founders & owners

## Adaptation context

```yaml
adaptation:
  primary_archetype: str
  secondary_archetypes: [str]
  industry_profiles: [ {id, version, verified_at, local_overrides:[...]} ]
  business_model_profiles: [ {id, revenue_share, economic_unit, verified_at} ]
  lifecycle_stage: enum(formation, validation, repeatability, scaling, mature, renewal, decline, exit)
  functional_maturity: { domain: 0-5 }
  jurisdictions: [ {country, region, local, activities, regulatory_intensity} ]
  ownership_model: str
  risk_appetite_ref: str
  metric_overrides: [ {metric, profile_definition, local_definition, reason, evidence, review_date} ]
  routing_overrides: [ {intent, required_skills, prohibited_actions, specialist_gate} ]
```

Profile files are routing defaults, not facts. Every override is versioned with evidence and review date.

## Advanced operating namespaces

The advanced domains use the same cross-cutting record envelope and append-only rules:

- `product`: opportunities, product outcomes, roadmap bets, lifecycle, adoption, discovery evidence.
- `customer_success`: success plans, health signals, value milestones, renewal/expansion, feedback themes.
- `supply_chain`: demand plans, suppliers, item policies, inventory, logistics nodes, disruption scenarios.
- `technology`: capabilities, applications, architecture, service levels, incidents, automation portfolio, technical debt.
- `data`: data products, critical data elements, metric definitions, lineage, quality rules, models, experiments.
- `security_privacy`: assets, identities, entitlements, threats, controls, incidents, processing activities, retention.
- `quality`: standards, controls, audits, defects, root causes, corrective actions, effectiveness checks.
- `projects`: projects, programs, dependencies, milestones, resources, risks, benefits, decisions.
- `governance`: decision rights, policies, board calendar, stakeholder commitments, action registers.
- `international`: markets, entities, currencies, localizations, cross-border flows, jurisdiction exposures.
- `sustainability`: material topics, resource flows, impact chains, claims, evidence, resilience actions.

```yaml
founders:
  - id: str
    name_ref: str                  # PII → reference
    role: str
    ownership_pct: number
    leadership_style: str          # output of leadership-style-assessment skill
    strengths: [str]
    development_areas: [str]
    time_allocation: { function: pct }   # where the founder's hours go
    goals_personal: [str]
    sensitivity: confidential
```

## 3. Customers

```yaml
customers:
  icps:                            # ideal customer profiles
    - id, name, description, firmographics|demographics, why_fit
  personas:
    - id, name, role, goals, pains, objections, buying_triggers,
      decision_criteria, where_they_are (channels), value_drivers
  segments:
    - id, name, definition, size_estimate, revenue_share, cac, ltv, churn_rate
  accounts:                        # known individual customers (if tracked)
    - id, name_ref, segment_id, status, mrr|arr|order_history_ref,
      health_score, first_order_date, last_order_date, concentration_flag
  concentration:
    top_customer_pct_revenue: number
    top5_pct_revenue: number
```

## 4. Offerings (products & services)

```yaml
offerings:
  - id, name, type(product|service), description
    price, unit, cost_of_delivery, gross_margin_pct
    positioning, cvp_id                 # links to a value proposition
    lifecycle: enum(new, growth, mature, declining)
    revenue_share_pct
    capacity_constraint: str            # what limits how much can be sold/delivered
```

## 5. Finance

```yaml
finance:
  accounts: [ {id, type(bank|card|loan|line), institution_ref, balance, as_of} ]
  income_statement:                 # periodized, append-only
    - period, revenue, cogs, gross_profit, opex{...}, ebitda, net_income, source
  balance_sheet:
    - period, assets{current, fixed}, liabilities{current, long_term}, equity, source
  cash_flow:
    - period, operating, investing, financing, net_change, ending_cash, source
  working_capital:
    ar_balance, ap_balance, inventory_balance, dso, dpo, dio, ccc
  position:
    cash_on_hand, monthly_burn, runway_months, mrr|arr, gross_margin_pct,
    net_margin_pct, break_even_revenue
  debt:
    - {id, principal, rate, monthly_payment, maturity, covenant_terms, dscr}
  budgets: [ {id, period, lines[...], approved_by} ]
  forecasts: [ {id, scenario(base|upside|downside), horizon, drivers{...}, outputs_ref} ]
  sensitivity: confidential
```

## 6. Team

```yaml
team:
  people:
    - id, name_ref, role, function, reports_to_id, employment_type(FTE|PT|contractor),
      start_date, capabilities:[str], responsibilities:[str],
      authority_level: enum(A_none, B_minimal, C_medium, D_complete),   # delegation model
      capacity_utilization_pct, performance_rating, comp_ref(restricted), flight_risk
  org:
    structure: tree(person_id → [reports])
    spans_of_control: { manager_id: count }
    open_roles: [ {id, title, function, reason, priority, budgeted_cost, status} ]
  culture:
    stated_values:[str], observed_signals:[str], engagement_indicators:{...}
  sensitivity: restricted            # individual people data
```

## 7. Operations

```yaml
operations:
  processes:
    - id, name, owner_id, trigger, steps:[...], inputs, outputs,
      cycle_time, capacity, bottleneck_flag, defect_rate, sop_ref, automation_status
  sops: [ {id, process_id, doc_ref, last_reviewed} ]
  tools: [ {id, name, category, cost, owner, integration_id} ]
  vendors: [ {id, name_ref, service, cost, contract_ref, dependency_risk, renewal_date} ]
  capacity:
    - resource, available, used, utilization_pct, constraint_flag
```

## 8. Market

```yaml
market:
  size: {tam, sam, som, source}
  trends: [ {description, direction, impact, as_of} ]
  competitors:
    - id, name_ref, positioning, strengths, weaknesses, price_posture, threat_level
  differentiation: [str]
  regulatory_context: [str]
```

## 9. Strategy

```yaml
strategy:
  current_priorities: [ {id, statement, rank, owner_id, horizon} ]
  growth_plan:
    objective, target_metric, target_value, target_date
    initiatives: [ {id, name, hypothesis, expected_impact, cost, owner, status, kpis} ]
  hypotheses: [ {id, statement, status(open|validated|rejected), evidence_ref} ]
  experiments: [ {id, hypothesis_id, design, metric, result, learning} ]
```

## 10. Metrics (append-only time series)

```yaml
metrics:
  - key: str                        # e.g. "cash_runway_months", "sales_conversion_rate"
    value: number
    unit: str
    period: date | range
    target: number
    status: enum(healthy, needs_attention, at_risk, critical)
    source: str
    computed_by: skill_id | integration_id
```

Metric definitions (formula, thresholds) are catalogued in `BUSINESS_HEALTH_ENGINE.md`; memory stores the **time series of actuals + targets**.

## 11. Goals

```yaml
goals:
  - id, statement, metric_key, baseline, target, deadline, owner_id,
    status(on_track|at_risk|off_track|achieved), linked_initiatives:[id]
```

## 12. Decisions (the learning substrate)

Every material decision is recorded so outcomes can be compared to expectations.

```yaml
decisions:
  - id: str
    date: date
    context: str                    # situation that prompted it
    question: str
    options_considered: [ {option, pros, cons, projected_outcome} ]
    assumptions: [str]
    decision: str
    rationale: str
    owner_id: str
    authorized_by: str              # founder | agent + autonomy level
    expected_outcome: {metric_key, expected_value, by_date}
    actual_outcome: {metric_key, actual_value, measured_at}   # filled later
    variance: number                # computed by Learning layer
    lesson: str                     # written after the fact
    linked_audit_ids: [str]
```

## 13. Risks

```yaml
risks:
  - id, category(financial|operational|market|legal|people|concentration|continuity),
    description, likelihood(1-5), impact(1-5), score, status,
    mitigation, owner_id, review_date, escalation_path
```

## 14. Integrations (connection registry)

```yaml
integrations:
  - id, category, provider, status(connected|error|disconnected),
    scopes_read:[str], scopes_write:[str], last_sync, owner, credentials_ref(secret)
```

---

## Cross-cutting record envelope

Every record, in every namespace, is wrapped with:

```yaml
_meta:
  id, created_at, updated_at, version
  source: enum(integration, founder_input, agent_analysis, document, external)
  confidence: 0.0-1.0
  as_of: date                       # when the fact was true
  sensitivity: public|internal|confidential|restricted
  verified_by: str | null
```

## Access & write rules

- Agents read only the namespaces their role grants (see `core/permissions/`).
- Writes to `finance`, `team`, and `decisions` are audited.
- `restricted` records (individual comp/performance) require elevated scope and never appear in external outputs.
- Conflicting facts are not silently merged — the lower-confidence/staler record is flagged for reconciliation and, if material, surfaced to the founder.

## Relationship to other components

- **Digital Twin** computes live state (runway, health, bottlenecks) from these facts.
- **Skills** declare which namespaces they read/write in their `Required Context` and `Output`.
- **Learning layer** reads/writes `decisions` and `metrics` history.
- **Cadence** reads `metrics`, `goals`, and `strategy` to assemble briefings.
