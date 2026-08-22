# MASTER_ORCHESTRATOR

**Deliverable 17 — The system responsible for: Intent → Adaptation → Understanding → Diagnosis → Planning → Execution → Monitoring → Learning.**

The Orchestrator is the front door of Vibe Managing. It receives the founder's natural-language intent, configures the operating logic for the company's business archetype, industry, business model, lifecycle, maturity, geography, and regulatory intensity, then calls skills and agents, consults memory and the twin, routes actions through the control plane, and closes the loop with monitoring and learning.

Implementation home: `core/orchestrator/`.

---

## Input

Anything the founder says:
- a goal ("grow revenue 20% this quarter")
- a problem ("we're running out of cash")
- a constraint ("I can't spend more than $10k")
- a decision ("should we hire three salespeople?")
- an outcome ("show me what needs my attention")

## The 18-step orchestration loop

```
 1. CLASSIFY intent        → intent type + domain(s) + urgency (see INTENT_LIBRARY.md)
 2. ADAPT operating logic  → archetype + industry + model + stage + maturity + geography + regulation
 3. DETERMINE context      → memory namespaces + twin views + profiles required
 4. INSPECT data           → load them; assess lineage, freshness & confidence
 5. IDENTIFY gaps          → required data missing/stale/low-confidence
 6. RESOLVE gaps           → integrations, computation, or ONE tight founder question batch
 7. SELECT capabilities    → smallest sufficient skill + agent + tool sequence
 8. DIAGNOSE               → ranked, evidence-backed causal hypotheses
 9. VALIDATE hypotheses    → test against data, counterfactuals, and twin simulations
10. OPTIMIZE options       → maximize confidence-weighted enterprise outcome inside hard constraints
11. PLAN                   → initiatives, impact, owners, timeline, budget, dependencies, KPIs
12. ENUMERATE actions      → concrete actions with reversibility, authority, and stop/scale rules
13. CLASSIFY action risk   → risk-tier each action (AUTONOMY_AND_APPROVAL_MODEL.md)
14. EXECUTE authorized     → low-risk reversible actions via agents/tools; log
15. REQUEST approval       → bundle restricted actions into one decision-quality request
16. MONITOR                → leading indicators, guardrails, thresholds, and profile cadence
17. REPORT                 → found, decided, done, awaiting, and next best action
18. REMEMBER & LEARN       → decision record, profile overrides, expected/actual, lessons
```

Steps 8–11 may fan out to multiple agents in parallel; step 14 respects per-action autonomy; steps 16–18 hand off to the Monitoring, Cadence, and Learning components.

## Universal adaptation gate

Before domain reasoning, the Orchestrator invokes `dynamic-skill-routing` with the context produced by `business-archetype-classifier`, `industry-operating-profile`, `stage-and-maturity-assessment`, and `regulatory-intensity-classifier`. The resulting context determines metric definitions, formulas, benchmarks, cadence, required integrations, specialist gates, and autonomy ceilings. See `UNIVERSAL_BUSINESS_ADAPTATION.md`.

## Intent classification

The Orchestrator tags each request:

```yaml
classified_intent:
  raw: "we're profitable but I never have cash"
  type: diagnose            # {ask, diagnose, plan, decide, execute, monitor, learn}
  primary_domain: finance
  secondary_domains: [operations]
  urgency: high             # {low, normal, high, critical}
  entities: [cash, profit, working_capital]
  suggested_skills: [cash-flow-diagnostic, working-capital-optimizer]
  suggested_agents: [cfo-agent]
  requires_context: [finance.*, offerings, customers.concentration]
```

Ambiguous intents are disambiguated with a single clarifying question, not a guess.

## Missing-information protocol

Before diagnosing, the Orchestrator checks that required inputs exist, are fresh, and are trusted:

```
IF required datum missing:
    IF obtainable via a connected integration → fetch it
    ELIF computable from existing data        → compute it
    ELSE                                       → add to founder question batch
IF datum present but stale (as_of > freshness_budget) → refresh or flag
IF datum present but confidence < threshold           → flag; do not act on it silently
```

The founder is asked at most one concise batch of questions per request — never an interrogation, never one question at a time.

## Hypothesis discipline

Diagnosis is explicit and testable:

```yaml
hypothesis:
  claim: "Cash gap is driven by lengthening receivables, not by losses"
  test: "DSO trend over last 6 months vs. net margin trend"
  evidence: {dso: [42,48,55,61], net_margin_pct: [11,11,12,11]}
  verdict: supported            # {supported, rejected, inconclusive}
  confidence: 0.82
```

Rejected and inconclusive hypotheses are kept in the decision record so the Learning layer can improve future diagnosis.

## Plan object

```yaml
plan:
  objective: "Restore cash runway to >6 months within 60 days"
  diagnosis_ref: ...
  initiatives:
    - id, name, hypothesis, expected_impact:{metric, delta, by_date},
      actions:[...], owner, cost, risk_tier, kpis:[...]
  sequencing: [initiative_ids in order]
  total_cost, expected_outcome, confidence
  monitoring: {leading_indicators:[...], review_cadence}
```

## Execution & approval routing

Each action from the plan is dispatched:

```
for action in plan.actions:
    tier = classify_risk(action)
    level = granted_autonomy(agent, action.type)
    route = decision_matrix(tier, level)   # auto | notify | approve | prepare-only
    if route == auto:      agent.execute(action); audit()
    if route == notify:    agent.execute(action); audit(); notify_founder()
    if route in (approve, prepare-only): queue_for_approval(action); audit()
```

## Output to the founder

The Orchestrator always returns a decision-quality summary, not raw data:

```
1. What I found        (diagnosis + evidence + confidence)
2. What I did          (auto-executed, reversible actions, with undo)
3. What I need from you (approval requests, ranked, with recommendation)
4. What I'll watch      (leading indicators + when I'll report back)
```

## Closing the loop

- Registers the plan's leading indicators with the **Business Health Engine** (`core/monitoring/`).
- Writes a **Decision record** to Business Memory with `expected_outcome`.
- Schedules a **Learning review** (`core/learning/`) to compare expected vs. actual and update assumptions.
- Surfaces the next-best-actions on the following cadence cycle.

## Guarantees

- **No irreversible action without approval.** Ever.
- **No action on stale/low-confidence data without flagging it.**
- **Every action is auditable and linked to the decision that authorized it.**
- **Every plan is measurable** — if a plan has no KPI, the Orchestrator refuses to finalize it.

## Worked trace

See `examples/` for full traces, including "I'm spending too much money and I don't know where" and "Can we hire three salespeople?" walked through all 16 steps.
