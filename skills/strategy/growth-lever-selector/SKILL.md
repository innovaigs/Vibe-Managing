---
name: growth-lever-selector
domain: strategy
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [company, offerings, customers, market, finance, team, goals, strategy]
writes: [strategy, decisions]
related_skills: [growth-pathway-classifier, opportunity-feasibility-analysis, resource-gap-analysis, competitive-intelligence-analysis, initiative-prioritization, strategic-planning]
owned_by_agents: [strategy-agent]
---

# Skill: Growth Lever Selector

## Purpose
When the founder wants to grow but doesn't know which direction, this skill maps the full menu of growth avenues, screens each against the business's aspirations and its Management/Market/Money capacity, and returns a short ranked list of the highest-fit growth levers with rationale — so effort goes into the avenue most likely to work, not the first one that comes to mind.

## When to Use
- The founder asks "how should we grow?", "what's our next move?", "where's the biggest upside?"
- Following `growth-pathway-classifier` when a plateau/incremental pathway calls for a new avenue.
- After `business-health-diagnostic` flags revenue stagnation or customer concentration.
- When choosing among expansion directions before committing to feasibility on any one.

## When NOT to Use
- A specific avenue is already chosen and needs validation → `opportunity-feasibility-analysis`.
- The founder needs to generate creative options within an avenue → `idea-expansion`.
- The task is sequencing already-chosen initiatives → `initiative-prioritization`.
- The business's constraint is survival (cash critical), not growth → route to cash/health first.

## Required Context
Reads `company` (current scope, competitive advantage, stage), `offerings` (current products/margins), `customers` (current segments/geographies), `market` (adjacent segments, trends, competitive pressure), `finance` (capital available, margins — the "Money" factor), `team` (capacity/skills — the "Management" factor), `goals` (aspiration/target size), and any pathway classification from `growth-pathway-classifier`. Aspiration ("how big do I want to get?") is required — it changes which levers fit.

## Inputs
```yaml
input:
  current_scope:
    segments: [str]                  # demographics served
    geographies: [str]               # local/regional/national/export reach
    products: [str]
    channels: [str]                  # e-commerce, brick-and-mortar, wholesale, etc.
  competitive_advantages: [str]
  aspiration:
    how_big_want: str                # founder's desired size/ambition
    horizon: str                     # timeframe
    ambition: enum(conservative, balanced, bold)
  three_M:
    management: enum(strong, adequate, weak)   # team/leadership capacity for growth
    market: enum(favorable, neutral, unfavorable)
    money: number                    # capital available to fund growth
  pathway: enum(rapid, incremental, episodic, plateau, unknown)  # from growth-pathway-classifier
  constraints: [str]                 # e.g., "no acquisitions", "stay local"
```

## Missing Information Protocol
1. Pull scope, margins, and capacity from memory/integrations before asking.
2. Aspiration and ambition must come from the founder if unknown — ask in one line ("how big do you want to get, and by when?"); do not assume.
3. For each lever needing external data (new-market size, channel economics), if unknown, recommend it but attach the data gap to be closed in `opportunity-feasibility-analysis` — do not fabricate the size.
4. Never assume the founder wants maximum growth — an incremental/lifestyle aspiration is valid and reshapes the ranking.

## Diagnostic Questions
- What does the business currently sell, to whom, where, and through what channel?
- What is the competitive advantage each lever could leverage?
- How big does the founder want to get, and in what timeframe?
- Are Management, Market, and Money each adequate for the intended growth? Which is the weakest?
- Which levers extend from current strength vs. require building new capability?
- Which levers reduce a known risk (e.g., customer concentration) as a side effect?

## Analysis Framework
Screen every lever in the Ways-to-Grow taxonomy, then rank by fit:
- **New markets** — new demographic; new industry; new geography (local → regional → national → export).
- **New products/services** — including new features/extensions to existing offerings.
- **New channels** — e-commerce; brick-and-mortar; wholesale; marketplaces.
- **Strategic partnerships.**
- **Acquisitions.**

Each candidate lever is scored on: (1) **advantage leverage** — does it build on an existing competitive advantage? (2) **aspiration fit** — does its upside match how big the founder wants to get? (3) **3M readiness** — are Management, Market, Money adequate for it? (4) **risk/reversibility** — how committing and irreversible is entering it? (5) **side-benefit** — does it also reduce a known risk (e.g., concentration)? The **Three Growth Factors gate** is binding: if a lever needs a 3M the business lacks, it is downgraded or gated behind fixing that factor first.

## Calculations
- **Fit score (SYNTH ranking heuristic, 0–100):** `Fit = 30·advantage_leverage + 25·aspiration_fit + 25·three_M_readiness + 20·(1 − irreversibility)`, each sub-factor scored 0–1. Higher = better fit. Side-benefit (risk reduction) applied as a +5 tiebreak bonus.
- **3M adequacy gate:** for a lever, `min(management_score, market_score, money_adequacy)`; if any is "weak"/inadequate, cap the lever's fit at "gated" and name the factor to fix first.
- **Money adequacy** = `available_capital ≥ estimated_entry_capital` for the lever (estimate flagged as a data gap where unknown).
- **Aspiration alignment:** conservative ambition down-weights high-commitment levers (acquisitions, national/export); bold ambition up-weights them.
- No source-stated numeric benchmarks exist for lever selection — the taxonomy is source-derived; the scoring weights are SYNTH defaults, tunable.

## Decision Rules
- **IF** any of Management, Market, or Money is weak for a lever **THEN** gate that lever behind fixing the weak factor first; do not rank it top.
- **IF** a lever does not leverage an existing competitive advantage **THEN** down-weight it (entering from weakness = higher execution risk).
- **IF** aspiration = conservative **THEN** rank low-commitment, adjacent levers (new features, e-commerce channel, local partnerships) above acquisitions/export.
- **IF** aspiration = bold AND Money adequate **THEN** allow high-commitment levers (national/export, acquisitions) into the top ranks.
- **IF** pathway = plateau **THEN** favor levers that reorient (new segment, new channel, new offering) over doubling down on the saturating one.
- **IF** pathway = episodic/rapid **THEN** favor levers that fit within current capacity or explicitly pair with `resource-gap-analysis` before scaling.
- **IF** customer concentration is a known risk **THEN** apply the side-benefit bonus to levers that diversify the customer base.
- **IF** a lever is high-commitment/irreversible (acquisition, export entry) **THEN** it may only be RECOMMENDED for feasibility, never executed by this skill.
- **IF** two levers tie **THEN** prefer the more reversible one.

## Procedure
1. Load current scope, advantages, aspiration, 3M capacity, pathway, and constraints.
2. Enumerate candidate levers from the taxonomy, excluding any the founder ruled out.
3. For each, assess advantage leverage, aspiration fit, 3M readiness (apply the gate), reversibility, and side-benefits.
4. Compute the fit score; gate levers with a weak binding 3M factor.
5. Rank the levers; keep the top 2–3 as recommendations, each with rationale and the first data gap to close.
6. For each recommended lever, name the fix-first factor (if gated) and the follow-on skill (`opportunity-feasibility-analysis`, `resource-gap-analysis`, `competitive-intelligence-analysis`).
7. Write the ranked levers to `strategy` and a decision record to `decisions`.

## Output
```yaml
output:
  ranked_levers:
    - lever: str                     # e.g., "New geography: regional expansion"
      category: enum(new_market, new_product, new_channel, partnership, acquisition)
      fit_score: number              # 0-100
      advantage_leveraged: str
      aspiration_fit: enum(strong, moderate, weak)
      three_M_status: {management: str, market: str, money: str, binding_constraint: str}
      gated: bool                    # true if a weak 3M factor must be fixed first
      fix_first: str                 # the factor/skill to resolve before pursuing (or "none")
      reversibility: enum(reversible, recoverable, irreversible)
      side_benefit: str              # e.g., "reduces top-customer concentration"
      first_data_gap: str
      next_skill: str
  top_recommendation: str
  rationale: str                     # why this lever over the others
  excluded_levers: [ {lever: str, reason: str} ]
```

## Recommendations
Levers are ranked by fit score, with the 3M gate binding — a high-upside lever the business can't yet staff or fund is presented as "gated: fix X first," not as the top pick. The output is deliberately short (2–3 levers) and each carries the exact next skill, so the founder moves from "how do we grow?" to a concrete, testable direction. Reversibility breaks ties in favor of lower-commitment moves.

## Execution Opportunities
- Write the ranked levers + rationale to `strategy` and a decision record — reversible, LOW.
- Auto-propose `opportunity-feasibility-analysis` on the top lever and `resource-gap-analysis`/`competitive-intelligence-analysis` where gated — reversible, LOW.
- Draft a founder brief comparing the top 2–3 levers — reversible, LOW.
This skill selects and recommends; it never enters a market, signs a partnership, or executes an acquisition — all of those are irreversible and approval-gated downstream.

## Human Approval Requirements
- Recommendations only. Pursuing any lever, and especially high-commitment levers (acquisitions, export entry, partnerships that create obligations), requires founder approval and its own feasibility pass.
- Any lever implying a contract, capital outlay, or hiring is flagged for approval per `AUTONOMY_AND_APPROVAL_MODEL.md`.

## Escalation Conditions
- **Acquisition or partnership lever ranks top** → founder (+ recommend attorney for structure/terms, accountant for financing).
- **Top lever requires capital beyond available Money** → founder (+ accountant) — financing decision.
- **Aspiration is unclear or internally contradictory** → founder (the ranking depends on it).
- **Bold aspiration with weak Management/Money** → surface the mismatch honestly rather than ranking an unachievable lever first.

## KPIs
- Selection quality: % of top-recommended levers that pass feasibility and are pursued.
- Fit accuracy: did the pursued lever grow revenue as expected within the horizon?
- Gate value: instances where the 3M gate correctly stopped a premature high-commitment move.
- Diversification: reduction in customer concentration when a side-benefit lever was chosen.

## Monitoring
Track whether the recommended lever advanced to feasibility and how it performed. Watch the binding 3M constraint — if it's being fixed, the gated lever may become available. Re-run if aspiration, capacity, or pathway changes materially.

## Follow-Up
- Re-run when the pathway changes, aspiration shifts, or a gating 3M factor is resolved.
- Feed the top lever into `opportunity-feasibility-analysis`, then `strategic-planning` / `initiative-prioritization`.

## Related Skills
Upstream: `growth-pathway-classifier`, `business-health-diagnostic`. Feeds: `opportunity-feasibility-analysis`, `resource-gap-analysis`, `competitive-intelligence-analysis`, `initiative-prioritization`, `strategic-planning`. Pairs with `idea-expansion` to generate options within a chosen avenue.

## Guardrails
- Enforce the 3M gate — never rank a lever top when a required Management/Market/Money factor is weak; name the fix-first factor.
- Never present a fabricated new-market size — attach it as a data gap for feasibility.
- Do not push maximum growth onto a founder with a conservative/lifestyle aspiration.
- High-commitment levers are recommendations only, never executed here.

## Example
**Founder input:** "Regional coffee roaster, sells to local cafés and a small e-commerce store. Revenue plateaued. I want to roughly double in 3 years — balanced ambition. Management adequate, Market favorable, Money ~$60k available. Top customer is 38% of revenue. No acquisitions."
**Screen:** New geography (regional→national wholesale) — leverages roasting quality + brand; aspiration fit strong; 3M ok (money tight but adequate for a phased entry); diversifies concentration (+side-benefit); reversibility recoverable. New channel (grow e-commerce / subscription) — leverages brand + margins; strong aspiration fit; low capital; highly reversible; diversifies away from café concentration. New product (single-origin/subscription tiers) — leverages advantage; moderate fit. Acquisition — excluded per constraint.
**Ranking:** (1) Grow e-commerce/subscription channel — fit ~86, reversible, diversifies concentration, low capital, next skill `opportunity-feasibility-analysis`; (2) Regional wholesale expansion — fit ~80, recoverable, diversifies, pair with `resource-gap-analysis` (logistics) + `competitive-intelligence-analysis`; (3) New subscription product tiers — fit ~72.
**top_recommendation:** grow the subscription/e-commerce channel first (fastest, most reversible, reduces the 38% concentration risk), then phase regional wholesale.
**Executed vs. approval:** Wrote ranked levers + rationale to `strategy`, proposed feasibility on the channel lever. No market entered, no contract signed.

## Provenance
SOURCE. Implements the Ways-to-Grow Taxonomy (new markets/products/channels, partnerships, acquisitions) as a screenable menu, gated by the Three Growth Factors (Management, Market, Money) and aligned to the founder's growth aspiration ("how big do I want to get?"), with reversibility from the platform autonomy model. Fit-score weights are SYNTH defaults over the source taxonomy. See `internal/PROVENANCE_MAP.md`.
