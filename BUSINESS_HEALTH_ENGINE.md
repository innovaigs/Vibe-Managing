# BUSINESS_HEALTH_ENGINE

**Deliverable 12 — Continuous diagnostic and monitoring model.**

The Business Health Engine is Vibe Managing's always-on sensor. It continuously computes indicators across every part of the business, compares them to thresholds and trends, detects anomalies, traces root causes, and raises the issues a founder should act on **before they are asked**. It powers Layer 5 (Monitoring) and feeds the operating cadence and the orchestrator.

Home: `core/monitoring/`. It reads the metric time-series in Business Memory and the derived views in the Digital Twin.

---

## Health states

Every indicator, category, and the company overall resolves to one of four states:

| State | Meaning | System behavior |
|---|---|---|
| 🟢 **Healthy** | within target band | track only |
| 🟡 **Needs Attention** | drifting toward a threshold or mild breach | surface in next cadence briefing + recommend a skill |
| 🟠 **At Risk** | threshold breached or adverse trend | alert now + prepare corrective actions for approval |
| 🔴 **Critical** | severe breach / existential | alert immediately + escalate + propose emergency plan |

State is computed from three signals combined: **level** (vs. threshold), **trend** (direction/velocity over recent periods), and **anomaly** (deviation from expected/seasonal pattern). The worst of the three sets the state.

---

## Monitored categories & indicators

Thresholds below are sensible defaults; each is overridable per business in `core/monitoring/thresholds.config.yaml` and refined by industry benchmarks. Formulas are defined in the finance/operations/marketing skills and catalogued here for the engine.

### Cash & liquidity  *(highest priority — cash is survival)*
| Indicator | Formula | 🟢 | 🟡 | 🟠 | 🔴 |
|---|---|---|---|---|---|
| Cash runway (months) | cash ÷ avg monthly net burn | >6 | 4–6 | 2–4 | <2 |
| Current ratio | current assets ÷ current liabilities | >1.5 | 1.2–1.5 | 1.0–1.2 | <1.0 |
| Quick ratio | (current assets − inventory) ÷ current liab. | >1.0 | 0.8–1.0 | 0.5–0.8 | <0.5 |
| Operating cash flow | from cash-flow statement | positive & rising | positive flat | slightly negative | sustained negative |
| Cash conversion cycle | DSO + DIO − DPO | improving/low | stable | lengthening | sharply lengthening |

### Revenue & growth
| Indicator | Formula | Signal |
|---|---|---|
| Revenue growth rate | (rev_t − rev_t−1) ÷ rev_t−1 | vs. plan; negative or decelerating → 🟠 |
| Revenue vs. forecast | actual ÷ forecast | <90% → 🟡, <80% → 🟠 |
| Recurring revenue / MRR-ARR | sum of recurring | decline → 🟠 |
| Pipeline coverage | weighted pipeline ÷ target | <3× → 🟡, <2× → 🟠 |

### Profitability & margin
| Indicator | Formula | Signal |
|---|---|---|
| Gross margin % | gross profit ÷ revenue | falling trend → 🟡/🟠 |
| Net margin % | net income ÷ revenue | negative → 🟠 |
| Break-even headroom | (revenue − break-even) ÷ revenue | <10% → 🟠 |
| DuPont ROE drift | margin × turnover × leverage | leverage-driven gains → 🟡 (flag risk) |

### Customers
| Indicator | Formula | Signal |
|---|---|---|
| Customer concentration | top-customer rev ÷ total | >25% → 🟡, >40% → 🟠 |
| Churn rate | lost ÷ starting customers | rising → 🟠 |
| Conversion rate | won ÷ opportunities | drop ≥15% MoM → 🟠 |
| CAC / LTV:CAC | (SYNTH) | LTV:CAC <3 → 🟡, <1 → 🔴 |

### Receivables & payables
| Indicator | Formula | Signal |
|---|---|---|
| DSO | (A/R ÷ revenue) × days | rising vs. terms → 🟠 (cash trap) |
| A/R aging >90d | overdue ÷ total A/R | rising → 🟠 |
| DPO vs. terms | (A/P ÷ COGS) × days | paying too fast while cash tight → 🟡 |

### Operations & delivery
| Indicator | Formula | Signal |
|---|---|---|
| On-time delivery | on-time ÷ total | <95% → 🟡, <85% → 🟠 |
| Cycle time | end − start | rising → 🟡 |
| Defect / rework rate | defects ÷ output | rising → 🟠 |
| Capacity utilization | used ÷ available | >90% sustained → 🟠 (no slack) |
| Bottleneck load | throughput vs. constraint capacity | at ceiling → 🟠 |

### People
| Indicator | Formula | Signal |
|---|---|---|
| Founder-load index | founder hrs on delegable work ÷ total | high → 🟠 (founder = bottleneck) |
| Team capacity utilization | committed ÷ available | >90% → 🟡, >100% → 🟠 |
| Key-person dependency | processes with single owner | >1 critical → 🟠 |
| Open critical roles | count past target start | >0 aging → 🟡 |

### Risk & compliance
| Indicator | Signal |
|---|---|
| Open high-severity risks (likelihood×impact ≥ threshold) | any → 🟠 |
| Covenant headroom | near breach → 🟠, breach → 🔴 |
| Vendor/supply single points of failure | any critical → 🟠 |
| Compliance gaps (from legal scans) | any open → 🟡/🟠 |

### Strategic execution
| Indicator | Signal |
|---|---|
| Initiative on-track rate | <70% → 🟡 |
| Goal attainment vs. plan | behind pace → 🟠 |
| Growth-plan review completed | overdue → 🟡 |

---

## Anomaly detection

### Advanced domain health

The active industry and business-model profiles select only the relevant indicators below and calibrate definitions and thresholds to the company. Profile defaults are hypotheses; verified company targets and control limits take precedence.

| Domain | Core indicators | Typical root-cause branches |
|---|---|---|
| Product | adoption, activation, retention, product contribution, roadmap confidence | wrong problem · usability · reliability · pricing · onboarding · segment mismatch |
| Customer success | time-to-value, health coverage, gross/net retention, repeat/expansion | value gap · poor onboarding · product issue · service failure · relationship risk |
| Supply chain | forecast error/bias, fill rate, stockout, turns, supplier quality, landed cost | demand error · lead-time variation · policy · supplier · logistics · master data |
| Technology | service availability, change failure, recovery time, technical debt, cost/capability | architecture · change control · capacity · vendor · support · skills |
| Data & analytics | critical-data quality, freshness, lineage, metric certification, model drift | source process · definition · integration · ownership · access · transformation |
| Security & privacy | critical exposure age, excess privilege, incident containment, high-risk processing | identity · vulnerability · configuration · third party · behavior · governance |
| Quality | first-pass yield, defect escape, process capability, corrective-action effectiveness | design · material · method · machine · measurement · environment · training |
| Projects & programs | benefit realization, schedule confidence, critical dependency age, portfolio throughput | scope · estimate · capacity · dependency · governance · adoption |
| Governance | decision latency, policy coverage, control exceptions, board-action closure | rights · information · ownership · cadence · capability · enforcement |
| International | local conversion, landed margin, cross-border cash cycle, jurisdiction exposure | localization · channel · currency · tax/duty · regulation · operations |
| Sustainability | resource intensity, verified savings, material-impact progress, resilience readiness | process loss · asset · supplier · design · claim evidence · physical exposure |
| Adaptation | context completeness, profile confidence, override freshness, routing accuracy | wrong archetype · stale profile · business-model mix · maturity mismatch · jurisdiction gap |

---

Beyond fixed thresholds, the engine flags:
- **Trend breaks** — a metric that reverses a sustained direction.
- **Velocity spikes** — change rate far above the metric's normal variation (e.g. expense line jumps > x% MoM).
- **Seasonality misses** — actual outside the expected seasonal band.
- **Divergence pairs** — two metrics that normally move together decoupling (e.g. revenue flat but AR rising = collection problem; profit up but cash down = working-capital drain).

Anomaly method is intentionally simple and explainable (rolling mean/variance bands + ratio-of-changes), never a black box — every alert must be explainable to the founder.

## Root-cause trees

Each 🟠/🔴 indicator has a diagnostic tree that routes to the right skill. Examples:

```
Cash runway ↓
├─ Is net income negative?           → cash-flow-diagnostic → cost/pricing skills
├─ Is A/R rising (DSO up)?           → working-capital-optimizer (collections)
├─ Is inventory rising (DIO up)?     → working-capital-optimizer (inventory)
├─ Did capex/debt payment spike?     → debt-service-and-covenant-analysis
└─ Did a big customer churn?         → customer concentration + retention

Revenue miss ↓
├─ Traffic/leads down?               → channel-selection / marketing-metrics-tracker
├─ Conversion down?                  → website-conversion-audit / sales-process-design
├─ Pricing/mix shift?               → break-even-and-pricing-analysis
├─ Churn up?                         → churn diagnosis (growth)
└─ Capacity limiting delivery?       → bottleneck-analysis

Delivery slipping ↓
├─ Bottleneck at a step?             → bottleneck-analysis
├─ Defects/rework?                   → process-optimization
├─ Capacity maxed?                   → hiring-plan-builder / automation-triage
└─ Undocumented process?            → sop-writer
```

## Alert lifecycle

```
compute → classify state → (if 🟡+) explain (level+trend+anomaly) →
trace root cause → recommend skill(s) → prepare corrective actions (risk-tiered) →
notify per cadence/urgency → track to resolution → write outcome to memory (learning)
```

Alerts carry: indicator, current value, threshold, trend, likely cause, recommended skill, and pre-drafted actions (held for approval per the autonomy model). Duplicate/related alerts are grouped so the founder sees issues, not noise.

## Output: the health snapshot

```yaml
health_snapshot:
  as_of: date
  overall: 🟢|🟡|🟠|🔴
  categories:
    cash_liquidity: {state, top_indicator, value, trend, cause?, recommended_skill?}
    revenue_growth: {...}
    profitability: {...}
    customers: {...}
    operations: {...}
    people: {...}
    risk: {...}
    strategy: {...}
  attention_now: [ {title, state, why, recommended_action, approval_needed} ]   # ranked
```

This snapshot is what the daily/weekly/monthly cadence briefings and the "what should I focus on?" founder query are assembled from (see `OPERATING_CADENCE.md`).

## Guarantees

- Every alert is **explainable** (level + trend + anomaly + cause).
- Cash and covenant indicators are evaluated **every cycle** — never skipped.
- The engine **recommends and prepares** but does not auto-execute corrective actions above L2; it routes them through the control plane.
- Alerts computed on **stale or low-confidence data are marked as such** and never presented as certain.
