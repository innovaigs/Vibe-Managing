---
name: initiative-prioritization
domain: strategy
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [strategy, finance, team, operations, goals, risks, metrics]
writes: [strategy, decisions, goals]
related_skills: [strategic-planning, business-health-diagnostic, resource-gap-analysis, growth-lever-selector, risk-diagnostic]
owned_by_agents: [strategy-agent, orchestrator]
---

# Skill: Initiative Prioritization

## Purpose
Take a pile of competing initiatives and turn it into a defensible, sequenced roadmap. Each initiative is scored on impact, effort, cost, risk, and dependency, then ordered so the business does the highest-value, lowest-friction, dependency-respecting work first — with capacity honored so the roadmap is real, not aspirational.

## When to Use
- After `strategic-planning` produces objectives with multiple initiatives to sequence.
- The founder asks "what should we do first?", "we can't do all this — what's the order?"
- When many good ideas/tasks compete for the same limited time, money, and people.
- Before a quarter/sprint to lock the sequence and set expectations.

## When NOT to Use
- There are no objectives yet → run `strategic-planning` first.
- The question is which growth avenue, not which initiative → `growth-lever-selector`.
- A single initiative needs validation → `opportunity-feasibility-analysis`.
- The problem is resource gaps, not sequencing → `resource-gap-analysis` (which feeds this).

## Required Context
Reads `strategy` (objectives + candidate initiatives), `finance` (budget/capital available), `team`/`operations` (capacity — people-weeks, throughput), `goals`, `risks` (initiative-level risks), `metrics`. Needs each initiative's rough impact, effort, cost, risk, and dependencies; missing values become estimates flagged as such.

## Inputs
```yaml
input:
  initiatives:
    - id: str
      name: str
      linked_objective: str
      impact_estimate: enum(low, medium, high)   # value toward the objective
      effort_estimate: str                       # people-weeks or t-shirt size
      cost_estimate: number
      risk_estimate: enum(low, medium, high)     # execution/failure risk
      reversibility: enum(reversible, recoverable, irreversible)
      dependencies: [str]                        # other initiative ids that must precede
      time_sensitivity: enum(none, soft_deadline, hard_deadline)
  capacity:
    people_weeks_per_period: number
    budget_per_period: number
    periods: int                                 # how many periods to sequence over
  strategic_weights: {impact: number, effort: number, cost: number, risk: number}  # optional override
```

## Missing Information Protocol
1. Pull impact/effort/cost/risk from `strategic-planning`, `resource-gap-analysis`, and feasibility outputs where available.
2. For any missing estimate, produce a flagged placeholder estimate (with rationale) rather than blocking — but mark the roadmap `provisional` until the founder confirms the material ones.
3. Capacity (people-weeks, budget) must be real — if unknown, ask; never sequence against imaginary capacity.
4. Never silently assume an initiative is dependency-free — if dependencies are unknown, flag it (a hidden dependency breaks a roadmap).

## Diagnostic Questions
- What value does each initiative deliver toward its objective (impact)?
- What will it cost in effort, money, and risk?
- What must happen before it (dependencies)? Is anything time-sensitive?
- How reversible is it (can we start small and learn)?
- Given real capacity, how many can run at once, and in what order?
- Which sequence delivers value earliest while respecting dependencies and capacity?

## Analysis Framework
A multi-criteria scoring + dependency-aware sequencing method:
1. **Score** each initiative on impact, effort, cost, and risk (and note reversibility).
2. **Rank** by a value/friction ratio (impact per unit of effort+cost+risk).
3. **Resolve dependencies** — topologically order so prerequisites precede dependents (no dependent can outrank its blocker).
4. **Respect capacity** — pack initiatives into periods without exceeding people-weeks or budget per period.
5. **Honor time-sensitivity** — pull hard-deadline items forward as needed, even at some efficiency cost.
6. **Prefer reversible-first** — front-load reversible, learnable initiatives to de-risk the roadmap.
Produces a sequenced roadmap by period with a clear "now / next / later" shape.

## Calculations
- **Priority score (SYNTH, 0–100):** `Score = w_i·impact − w_e·effort − w_c·cost_norm − w_r·risk`, with default weights `w_i=50, w_e=20, w_c=15, w_r=15` (overridable via `strategic_weights`); impact/risk on 0–1 (low/med/high = 0.2/0.5/1.0), effort and cost normalized 0–1 across the set.
- **Value/friction ratio** = `impact / (effort_norm + cost_norm + risk)` — a fast reversibility-agnostic rank; used as a tiebreak and sanity check on the weighted score.
- **Dependency constraint:** for any initiative D depending on B, `sequence_position(B) < sequence_position(D)`; violations are corrected by promotion of B.
- **Capacity packing:** per period, `sum(effort_in_period) ≤ people_weeks_per_period` AND `sum(cost_in_period) ≤ budget_per_period`; overflow spills to the next period.
- **Deadline override:** a `hard_deadline` initiative is scheduled no later than its deadline period even if that displaces a higher-scoring item (the displacement is logged).
- No source numeric benchmarks; the impact/effort/cost/risk/dependency criteria and the sequencing discipline are standard-practice (SOURCE-aligned with the source's resourcing/growth-plan sequencing); weights are SYNTH defaults.

## Decision Rules
- **IF** initiative D depends on B **THEN** B must be sequenced before D regardless of scores.
- **IF** a period's packed effort or cost exceeds capacity **THEN** spill the lowest-priority item to the next period; never over-pack.
- **IF** an initiative has a hard deadline **THEN** schedule it by that deadline even if it displaces a higher-scoring item (log the trade-off).
- **IF** two initiatives tie on score **THEN** prefer the more reversible one (start small, learn, adjust).
- **IF** a high-impact initiative is also high-risk and irreversible **THEN** recommend a reversible pilot/spike first, then re-score.
- **IF** an initiative has unknown dependencies **THEN** mark the roadmap provisional and flag the initiative for dependency clarification before it starts.
- **IF** total demand far exceeds total capacity across all periods **THEN** surface the over-scope explicitly and recommend cutting scope, not just deferring.
- **IF** an initiative's execution requires an approval-gated action (spend/hire/contract) **THEN** the roadmap schedules the "prepare + request approval" step, not auto-execution.

## Procedure
1. Load initiatives with estimates and dependencies; fill/flag missing estimates.
2. Normalize effort/cost across the set; compute priority scores and value/friction ratios.
3. Build the dependency graph; topologically constrain the order.
4. Pack initiatives into periods against real capacity (people-weeks + budget).
5. Apply hard-deadline overrides and reversible-first preference; log trade-offs.
6. Recommend pilots for high-risk/irreversible high-impact items.
7. Produce the sequenced roadmap (now/next/later) with per-period load.
8. Flag over-scope, provisional (unknown-dependency) items, and approval-gated steps.
9. Write the roadmap to `strategy`/`goals` and a decision record; present for founder approval.

## Output
```yaml
output:
  roadmap:
    - period: str                     # e.g., "Q1" / "weeks 1-4"
      initiatives:
        - id: str
          name: str
          priority_score: number
          impact: enum(low, medium, high)
          effort: str
          cost: number
          risk: enum(low, medium, high)
          reversibility: enum(reversible, recoverable, irreversible)
          starts_after: [str]         # dependency ids
          note: str                   # e.g., "pilot first", "pulled forward for deadline"
      period_load: {people_weeks: number, budget: number}
      capacity: {people_weeks: number, budget: number}
      over_capacity: bool
  now_next_later: {now: [str], next: [str], later: [str]}
  deferred_or_cut: [ {id: str, reason: str} ]
  provisional_flags: [ {id: str, reason: str} ]   # unknown dependencies/estimates
  approval_gated_steps: [ {id: str, action: str} ]
  tradeoff_log: [str]                 # deadline overrides, displacements
  recommended_next_skills: [str]
```

## Recommendations
The roadmap front-loads high-value, low-friction, reversible work while strictly respecting dependencies and real capacity — so early wins fund and de-risk later, bigger moves. Hard deadlines override efficiency only when they must, and every such trade-off is logged. High-risk irreversible bets are recommended as pilots first, so the business buys information before it buys commitment.

## Execution Opportunities
- Write the sequenced roadmap to `strategy`/`goals` and a decision record — reversible, LOW.
- Create internal tasks/milestones per period with owners — reversible, LOW.
- Schedule "prepare + request approval" steps for gated initiatives — reversible, LOW.
- Draft the now/next/later roadmap brief for the founder/team — reversible, LOW.
This skill sequences and schedules; it never executes the initiatives' business actions (spend, hire, contract, launch) — those run under their own approvals.

## Human Approval Requirements
- The roadmap (which commits the sequence of capacity/spend) is presented for founder approval.
- Each initiative involving money, hiring, contracts, or external commitments retains those approval requirements when its scheduled time comes.
- Cutting scope (dropping initiatives) is a founder decision — this skill recommends, the founder confirms.

## Escalation Conditions
- **Total demand >> capacity across all periods** → founder (scope-cut decision, not just deferral).
- **A dependency conflict has no feasible ordering** (circular dependency) → founder to break the cycle.
- **A hard-deadline initiative can't fit even with overrides** → founder (renegotiate deadline or scope).
- **An initiative requires financing/hiring to even start** → founder (+ accountant/HR).

## KPIs
- Throughput: initiatives completed per period vs. planned.
- Sequencing quality: rework/blockage caused by mis-ordered dependencies (target near zero).
- Capacity accuracy: planned vs. actual load per period.
- Early-value delivery: time-to-first-win from roadmap start.

## Monitoring
Track per-period load vs. capacity and dependency completion. Re-sequence if an initiative slips (cascading dependents), capacity changes, or a new high-priority initiative arrives. Watch that pilots for risky items actually gate the full commitment.

## Follow-Up
- Re-run each planning/sprint cycle and whenever the initiative set, capacity, or priorities change.
- Feeds execution tracking and reports back into `strategic-planning`.

## Related Skills
Consumes `strategic-planning` objectives and `resource-gap-analysis` closures; uses `risk-diagnostic` for initiative risk; feeds execution and `business-health-diagnostic` follow-up.

## Guardrails
- Never sequence against imaginary capacity — capacity must be real or the roadmap is provisional.
- Never violate a dependency ordering to chase a score.
- Never over-pack a period; spill or cut instead.
- Recommend pilots before high-risk irreversible commitments.
- Do not execute initiatives' business actions — schedule and prepare only.
- Flag, don't hide, over-scope; a roadmap that can't fit is a scoping problem to surface.

## Example
**Context:** From `strategic-planning`, four initiatives for the diversification + cash + margin objectives. Capacity: 6 people-weeks/period, $12k/period budget, 3 periods.
**Initiatives:** (A) add subscription billing app — impact med, effort 1pw, cost $1.2k, risk low, reversible, no deps. (B) buy + install filling equipment — impact high, effort 2pw, cost $18k, risk med, irreversible, no deps. (C) launch subscription to existing base — impact high, effort 3pw, cost $2k, risk med, recoverable, depends on A and B. (D) pricing/margin revision — impact high, effort 2pw, cost $0, risk med, reversible, no deps.
**Reasoning:** C depends on A+B → A and B must precede C. B is irreversible + $18k > single-period budget preference → recommend the purchase is approval-gated and scheduled period 1 (with a small-batch pilot of the filling process). D is high-impact, zero-cost, reversible → pull forward as an early win.
**Roadmap:** Period 1 — D (early margin win), A (enabler), begin B (approval-gated purchase + pilot); load 3pw/$1.2k+approval. Period 2 — complete B install; load fits. Period 3 — C (launch subscription), depends satisfied; 3pw/$2k. now/next/later: now [D, A, B-prep]; next [B-install]; later [C].
**approval_gated_steps:** B (equipment purchase $18k). tradeoff_log: "B scheduled early despite cost because C depends on it."
**Executed vs. approval:** Wrote the roadmap + per-period tasks, scheduled B's "prepare purchase + request approval" step (all L1). The $18k purchase itself is held for founder approval when period 1 begins.

## Provenance
SOURCE. Operationalizes the source's resourcing/sequencing discipline within the Growth Plan (do the highest-value, dependency-respecting work first within Management/Money capacity) using standard impact/effort/cost/risk/dependency multi-criteria prioritization, with reversibility from the platform autonomy model. Scoring weights are SYNTH defaults. See `internal/PROVENANCE_MAP.md`.
