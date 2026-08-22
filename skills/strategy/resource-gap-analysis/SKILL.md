---
name: resource-gap-analysis
domain: strategy
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [company, team, offerings, operations, finance, integrations, strategy, goals]
writes: [strategy, decisions, operations]
related_skills: [opportunity-feasibility-analysis, growth-lever-selector, strategic-planning, initiative-prioritization, risk-diagnostic]
owned_by_agents: [strategy-agent, operations-agent]
---

# Skill: Resource Gap Analysis

## Purpose
Before committing to a growth opportunity, find out exactly what the business already has, what it still needs, and the concrete action that closes each gap — organized across the six resource categories that are the building blocks of any business. Turns "we should grow" into a prioritized, ownable list of what to acquire, build, or hire first.

## When to Use
- After a "go"/"refine" from `opportunity-feasibility-analysis` or a chosen lever from `growth-lever-selector`: "what do we need to actually do this?"
- When `business-health-diagnostic` or `growth-pathway-classifier` flags a capacity or capability constraint (episodic/rapid growth).
- Before hiring, buying equipment, or taking on financing — to confirm the gap is real and prioritized.
- Periodically, to keep a current picture of resource readiness vs. the plan.

## When NOT to Use
- The opportunity hasn't been validated yet → run `opportunity-feasibility-analysis` first.
- The task is choosing which growth avenue → `growth-lever-selector`.
- The task is sequencing initiatives across the whole plan → `initiative-prioritization` (this feeds it).
- The gap is purely financial runway → route to cash-flow analysis.

## Required Context
Reads `team` (people, skills, roles), `company` (networks, reputation, systems, culture), `operations` (facilities, equipment, processes), `finance` (capital, banking, investor relationships), `integrations` (technology systems), `offerings`, and the target opportunity's requirements from `strategy`. Needs both the current inventory and the growth opportunity's demands to compute gaps.

## Inputs
```yaml
input:
  opportunity: str                    # the validated growth opportunity driving the requirements
  opportunity_requirements: [ {category: str, need: str, by_when: str} ]  # what the opportunity demands
  current_inventory:
    human: [str]                      # people, roles, skills, professional services on hand
    social: [str]                     # networks, memberships, partnerships, referral sources
    organizational: [str]             # culture, systems, processes, reputation, awards, IP
    physical: [str]                   # buildings, equipment, vehicles, inventory
    technological: [str]              # software, manufacturing/computer systems
    financial: [str]                  # cash, bank lines, equity investors, credit
  budget_available: number
  timeline: str                       # when the opportunity needs to be resourced by
```

## Missing Information Protocol
1. Pull the current inventory from memory/integrations (HR, accounting, asset registers) before asking.
2. Derive `opportunity_requirements` from the opportunity's feasibility output where possible; ask the founder only for requirements only they know.
3. If a category's inventory is unknown, mark that category `inventory-unknown` and make "inventory this category" the first action — do not assume the business has (or lacks) a resource.
4. Never assume budget or timeline — these gate prioritization; confirm in one batched question if missing.

## Diagnostic Questions
- What resources does the business have in each of the six categories?
- What does the growth opportunity require in each category?
- Where is the gap (need not met by what's on hand)?
- What single action step closes each gap (buy, build, hire, partner, finance, train)?
- Which gaps are blocking (the opportunity cannot start without them) vs. deferrable?
- Which gaps also represent a risk if unfilled (e.g., single key-person dependency)?

## Analysis Framework
The Resource Map Gap Grid across the six resource categories (the building blocks of any business):
1. **Human** — people, roles, skills; plus professional services (accountant, attorney, advisors).
2. **Social** — networks, memberships, partnerships, referral relationships.
3. **Organizational** — culture, systems, processes, reputation, awards, IP.
4. **Physical** — buildings, equipment, vehicles, inventory.
5. **Technological** — software, computer/manufacturing systems.
6. **Financial** — cash, bank lines, equity investors, credit.

For each category, a three-column grid: **What I Have** · **What I Need** · **Action Step**. Then each gap is classified (blocking vs. deferrable), prioritized, and given an owner and a target date. Ties to the Three Growth Factors: Human/Organizational map to "Management," Financial to "Money."

## Calculations
- **Gap per requirement:** for each requirement, `gap = need − have` (qualitative or quantitative). If met → no gap; if partially met → partial gap with the delta named.
- **Gap priority score (SYNTH heuristic, 0–100):** `Priority = 45·blocking + 30·time_pressure + 25·(1 − ease_to_close)`, each 0–1. Blocking gaps (opportunity can't start) dominate.
- **Cost-to-close estimate** per gap, summed → **total resourcing cost**; compare to `budget_available`. If total > budget → financing becomes its own gap (Financial category) and a `strategic-planning` input.
- **Coverage check:** count categories with `inventory-unknown` — each is a data-gap action before the analysis can be trusted.
- No source numeric benchmarks; the six categories and the have/need/action structure are source-derived; priority weights are SYNTH defaults.

## Decision Rules
- **IF** a gap is blocking (opportunity cannot begin without it) **THEN** it is top priority regardless of ease/cost.
- **IF** total cost-to-close > `budget_available` **THEN** raise a Financial gap and route financing to `strategic-planning` / founder (+ accountant).
- **IF** a Human gap is a single key-person dependency **THEN** also flag it as a risk → `risk-diagnostic`, and prefer a cross-training/backup action, not just a hire.
- **IF** a category is `inventory-unknown` **THEN** the first action for that category is to inventory it before relying on the gap list.
- **IF** a gap can be closed by partnership/outsourcing more cheaply than by building/hiring **THEN** recommend the reversible option first.
- **IF** an action step is hiring, signing a lease, buying major equipment, or taking financing **THEN** it is a recommendation only — flag for founder approval, do not execute.
- **IF** Management-related gaps (Human/Organizational) are severe **THEN** flag a Three-Growth-Factors "Management" weakness for `growth-lever-selector`/`strategic-planning`.

## Procedure
1. Load current inventory across the six categories; mark any `inventory-unknown`.
2. Load/derive the opportunity's requirements per category.
3. Build the have/need/action grid; compute the gap for each requirement.
4. Classify each gap blocking vs. deferrable; estimate cost and ease to close.
5. Compute priority scores; sum cost-to-close and compare to budget.
6. Assign a recommended action step, an owner, and a target date to each gap.
7. Flag key-person and Management-factor risks; route financing gaps.
8. Rank the closures; produce the prioritized action list.
9. Write the grid + prioritized closures to `strategy`/`operations`; propose (don't execute) the actions.

## Output
```yaml
output:
  opportunity: str
  grid:
    - category: enum(human, social, organizational, physical, technological, financial)
      have: [str]
      need: [str]
      gaps:
        - gap: str
          blocking: bool
          cost_to_close: number
          ease_to_close: enum(easy, moderate, hard)
          action_step: str            # buy/build/hire/partner/finance/train
          action_type: enum(reversible, recoverable, irreversible)
          owner: str
          target_date: str
          priority_score: number
          risk_flag: str              # e.g., "single key-person dependency" or "none"
  prioritized_closures: [ {rank: int, gap: str, action_step: str, why_first: str} ]
  total_cost_to_close: number
  budget_gap: number                  # total_cost_to_close - budget_available (>0 = financing needed)
  inventory_unknown_categories: [str]
  three_M_flags: {management: str, money: str}
  recommended_next_skills: [str]
```

## Recommendations
Closures are ranked blocking-first, then by time pressure and ease — so the founder tackles what the opportunity literally can't start without, before nice-to-haves. Reversible action steps (partner, outsource, train) are preferred over irreversible ones (hire, buy, lease) where they close the same gap, keeping optionality. Any closure that exceeds budget surfaces as a financing decision rather than being silently assumed.

## Execution Opportunities
- Write the resource grid + prioritized closures to `strategy`/`operations` and a decision record — reversible, LOW.
- Create internal tasks for each non-irreversible action step (e.g., "inventory technological systems," "cross-train backup for fulfillment") — reversible, LOW.
- Draft an RFP/vendor shortlist or job-description draft for the founder to review — reversible, LOW (drafting only).
- Route financing gaps to `strategic-planning` — reversible, LOW.
This skill never hires, signs leases, buys equipment, or takes on financing — those are irreversible and approval-gated.

## Human Approval Requirements
- Hiring, firing, signing leases/contracts, major equipment purchases, and taking on financing are ALWAYS founder-approved (and touch employment/legal/financial domains) — this skill only prepares them.
- Anything in the "always require approval" list of `AUTONOMY_AND_APPROVAL_MODEL.md` is prepared, not executed.

## Escalation Conditions
- **Financing gap (cost > budget)** → founder (+ recommend accountant).
- **Human gap involving hiring/role change** → founder (+ recommend HR for role definition/compliance).
- **Physical/equipment or lease commitment** → founder (+ attorney for the lease/contract terms).
- **Single key-person dependency on the founder** → founder + `risk-diagnostic` (business-continuity risk).
- **Inventory largely unknown** → surface that the gap list is provisional until inventoried.

## KPIs
- Closure rate: % of blocking gaps closed by their target date.
- Estimate accuracy: actual vs. estimated cost-to-close.
- Optionality: % of gaps closed via reversible actions (partner/train) vs. irreversible (hire/buy).
- Readiness: opportunity able to start on schedule because gaps were closed in priority order.

## Monitoring
Track each closure against its owner and target date. Watch for scope creep (new requirements emerging mid-execution) and for budget-gap growth. Re-flag any key-person risk that remains open. Re-inventory categories that were `inventory-unknown` once data arrives.

## Follow-Up
- Re-run when the opportunity's requirements change or a new lever is chosen.
- Feed the prioritized closures into `initiative-prioritization` and `strategic-planning` (resource allocation).

## Related Skills
Upstream: `opportunity-feasibility-analysis`, `growth-lever-selector`, `growth-pathway-classifier`. Feeds: `initiative-prioritization`, `strategic-planning`, `risk-diagnostic` (for key-person and continuity gaps).

## Guardrails
- Never assume a resource is present or absent — mark `inventory-unknown` and make inventorying the first action.
- Never execute hiring, leasing, purchasing, or financing — recommend and prepare only.
- Prefer reversible closures where they satisfy the same need.
- Treat single key-person dependencies as both a resource gap and a risk.
- Do not present cost-to-close estimates as firm quotes — label them estimates.

## Example
**Opportunity:** launch the concentrated-refill subscription line (from feasibility). Budget available: $30k, timeline 4 months.
**Grid (abridged):**
- **Human:** have — founder + 2 part-time packers; need — someone to run subscription ops. Gap (blocking): no ops owner. Action: cross-train an existing packer as subscription lead (reversible) rather than a new hire; priority 92.
- **Physical:** have — packing table; need — filling/refill equipment. Gap (blocking): no filling equipment, cost ~$18k, hard. Action: buy filling equipment (irreversible → founder approval); priority 88.
- **Technological:** have — basic Shopify store; need — subscription/recurring-billing module. Gap: no subscription billing, cost ~$1.2k, easy. Action: add subscription app (reversible); priority 70.
- **Financial:** have — $30k budget; need — ~$21k total. Budget gap: none (fits). 
- **Social/Organizational:** inventory known; minor gaps (supplier for concentrate) — action: source a second supplier (reversible), priority 60.
**total_cost_to_close:** ~$21k; budget_gap: −$9k (fits). three_M_flags: management "adequate (cross-train mitigates)", money "adequate."
**prioritized_closures:** (1) cross-train subscription lead; (2) buy filling equipment [approval]; (3) source concentrate supplier; (4) add subscription billing app.
**Executed vs. approval:** Wrote grid + closures, created tasks for cross-training, supplier sourcing, and the billing-app trial (all reversible, L1). The $18k equipment purchase is drafted with a vendor shortlist and held for founder approval.

## Provenance
SOURCE. Implements the Resource Map Gap Grid across the six resource categories (Human, Social, Organizational, Physical, Technological, Financial) with the What-I-Have / What-I-Need / Action-Step structure, linked to the Three Growth Factors (Management, Money) and to the risk register for key-person exposure. Priority-scoring weights are SYNTH defaults. See `internal/PROVENANCE_MAP.md`.
