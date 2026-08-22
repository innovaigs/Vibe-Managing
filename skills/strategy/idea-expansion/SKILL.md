---
name: idea-expansion
domain: strategy
version: 0.1.0
autonomy_ceiling: L0
provenance: SOURCE
reads: [company, founders, offerings, customers, market, strategy, goals]
writes: [strategy]
related_skills: [opportunity-feasibility-analysis, growth-lever-selector, competitive-intelligence-analysis, strategic-planning]
owned_by_agents: [strategy-agent]
---

# Skill: Idea Expansion

## Purpose
Stop the business from locking onto the first obvious idea. Given a core opportunity or problem, deliberately diverge into a wide option set across three altitudes — grounded, adjacent/unconstrained, and blue-sky — then converge on the 1–2 most promising ideas to carry into feasibility. Volume first, then filter: the best way to have a good idea is to have lots of ideas.

## When to Use
- The founder has one idea and asks "how else could we do this?" or "what are we not seeing?"
- Before feasibility testing, to make sure the strongest version of an opportunity is on the table.
- When a plan feels obvious/imitable and the founder wants a more differentiated angle.
- When a plateau or a crisis calls for reorientation and fresh options.

## When NOT to Use
- An idea is already chosen and needs validation → `opportunity-feasibility-analysis`.
- The founder wants to pick among defined growth avenues → `growth-lever-selector`.
- Execution planning is needed → `strategic-planning` / `initiative-prioritization`.
- The task is analysis of a competitor or market, not idea generation → the relevant analysis skill.

## Required Context
Reads `company` (model, competitive advantage), `founders` (goals, risk appetite), `offerings`, `customers` (segments and pains), `market` (trends, adjacent segments), `goals`. Needs the core opportunity or problem statement to expand from. Low-confidence market facts are fine here — this is divergence, not validation — but they are labeled so convergence doesn't over-weight them.

## Inputs
```yaml
input:
  core_opportunity: str            # the opportunity/problem to expand (ideally an opportunity statement)
  constraints: [str]               # hard constraints to respect during convergence (e.g., "no new hires this year")
  founder_ambition: enum(conservative, balanced, bold)   # tunes the target altitude
  known_advantages: [str]          # competitive advantages ideas should try to leverage
  customer_pains: [str]            # pains to solve, if known
  min_ideas_per_tier: int          # default 2
```

## Missing Information Protocol
1. If `core_opportunity` is vague, restate it as a one-sentence problem/opportunity and confirm with the founder in one line before diverging.
2. Pull customer pains and advantages from memory rather than asking.
3. This skill does not require validated data — it generates options. It must NOT, however, present any generated idea as validated; validation is `opportunity-feasibility-analysis`.
4. If constraints are unknown, generate freely but mark which converged picks depend on relaxing a likely constraint.

## Diagnostic Questions
- What is the core opportunity in one sentence?
- What customer pain(s) are we ultimately trying to solve?
- Which competitive advantage(s) could an idea leverage?
- What would the safe, obvious version look like? (grounded)
- If there were no rules, budget, or physics limits, what would we do? (unconstrained)
- What is ambitious-yet-actionable — novel and exciting but still realistic? (blue-sky, the target zone)
- Which 1–2 ideas are most intriguing AND fit the founder's ambition and constraints?

## Analysis Framework
The IdeaSpace divergent-then-convergent method, three altitude tiers:
- **Grounded** — safe, incremental, obvious, imitable, predictable. Establishes the baseline.
- **Spaced-Out** — crazy, whacky, absurd, unconstrained. Deliberately breaks assumptions; not meant to ship, meant to unlock.
- **Blue-Sky** — forward-looking, novel, unique, exciting, risky-but-fresh; ambition tempered by realism. This is the target zone where converged picks usually live.

**Procedure:** (1) state the core opportunity; (2) generate ≥`min_ideas_per_tier` Grounded ideas; (3) push to Spaced-Out to break constraints; (4) pull back to Blue-Sky ideas that are ambitious yet actionable; (5) select the 1–2 most intriguing to carry forward. `founder_ambition` shifts the convergence target: conservative → best Grounded/low Blue-Sky; balanced → Blue-Sky; bold → high Blue-Sky informed by a Spaced-Out insight.

## Calculations
None (this is a divergent-creative skill). Convergence uses a lightweight qualitative screen rather than a numeric model — a soft pre-check against the Five Characteristics of a Good Opportunity (does it plausibly solve a pain, offer something new, leverage an advantage, have a profit path, fit the founder?). No score is computed; the check only filters obviously non-viable ideas out of the shortlist.

## Decision Rules
- **IF** `founder_ambition` = conservative **THEN** converged picks come from Grounded or low-risk Blue-Sky.
- **IF** `founder_ambition` = bold **THEN** at least one converged pick must be a Blue-Sky idea seeded by a Spaced-Out insight.
- **IF** a generated idea does not plausibly solve a customer pain **THEN** exclude it from the converged shortlist (keep it in the tier list for reference).
- **IF** a converged pick requires relaxing a stated hard constraint **THEN** label it and surface the constraint trade-off explicitly.
- **IF** fewer than 2 viable ideas survive convergence **THEN** re-diverge with a reframed opportunity statement rather than forcing a weak pick.
- **IF** all surviving ideas are Grounded/imitable **THEN** flag "differentiation risk" and push one more Blue-Sky round.
- **NEVER** present any idea as validated — hand converged picks to `opportunity-feasibility-analysis`.

## Procedure
1. Restate the core opportunity as one sentence; confirm if ambiguous.
2. Generate ≥`min_ideas_per_tier` Grounded ideas.
3. Generate ≥`min_ideas_per_tier` Spaced-Out ideas to break assumptions.
4. Translate the most useful Spaced-Out insights into Blue-Sky ideas (ambitious yet actionable).
5. Apply the soft Five-Characteristics pre-check to filter non-viable ideas.
6. Converge to the 1–2 most intriguing picks per `founder_ambition` and constraints.
7. For each pick, note the advantage it leverages, the pain it solves, and any constraint trade-off.
8. Write the idea set to `strategy` and recommend feasibility testing of the top pick(s).

## Output
```yaml
output:
  core_opportunity_restated: str
  tiers:
    grounded: [ {idea: str, leverages: str, solves_pain: str} ]
    spaced_out: [ {idea: str, insight_unlocked: str} ]
    blue_sky: [ {idea: str, leverages: str, solves_pain: str, why_exciting: str, key_risk: str} ]
  converged_picks:
    - idea: str
      tier: enum(grounded, blue_sky)
      why_selected: str
      constraint_tradeoff: str        # or "none"
      soft_five_char_check: {solves_pain: bool, new_offering_or_market: bool, leverages_advantage: bool, profit_path: bool, fits_founder: bool}
  differentiation_flag: bool          # true if picks risk being imitable/undifferentiated
  recommended_next_skill: str         # typically opportunity-feasibility-analysis
```

## Recommendations
Convergence favors ideas that are simultaneously intriguing, aligned to the founder's ambition, and plausibly viable on the soft screen. The output is deliberately short (1–2 picks) so momentum isn't lost — but the full tier lists are retained so the founder can revisit discarded ideas. Every pick is explicitly framed as "candidate, not validated," with the next step being feasibility.

## Execution Opportunities
- Write the idea set and converged picks to `strategy` — reversible, LOW.
- Auto-trigger `opportunity-feasibility-analysis` on the top pick (as a proposal) — reversible, LOW.
- Draft a short "options memo" for the founder — reversible, LOW.
No external, financial, or irreversible action. Autonomy ceiling is L0 (observe/recommend) — this skill only produces analysis and internal notes.

## Human Approval Requirements
- None required to generate ideas (analysis is always allowed).
- Choosing to pursue any idea, and any downstream commitment, is the founder's decision and out of scope here.

## Escalation Conditions
- **Founder repeatedly rejects all converged picks** → escalate the reframing question to the founder (the core opportunity statement may be wrong).
- **A blue-sky pick implies legal/regulatory novelty** (new licensing regime, IP) → note and route to attorney at feasibility, not here.
- **Low confidence that any viable idea exists** → surface honestly rather than manufacturing a weak pick.

## KPIs
- Fraction of converged picks that pass `opportunity-feasibility-analysis`.
- Differentiation: fraction of shipped ideas that were Blue-Sky rather than imitable Grounded.
- Founder engagement: picks the founder chooses to advance.
- Idea volume generated before convergence (leading indicator of quality).

## Monitoring
Track whether converged picks advance to feasibility and how they fare there. If Grounded picks consistently beat Blue-Sky at feasibility, recalibrate the ambition tuning. If the founder keeps rejecting picks, revisit the core-opportunity framing.

## Follow-Up
- Re-run when feasibility kills the top pick (expand again from the runner-up or a reframed opportunity).
- Re-run at plateau or post-crisis, when reorientation options are needed.

## Related Skills
Feeds `opportunity-feasibility-analysis` (validates picks). Pairs with `growth-lever-selector` (which supplies structured avenues to expand within). Outputs can seed `strategic-planning`.

## Guardrails
- Never present a generated idea as validated or as a recommendation to commit resources.
- Keep Spaced-Out ideas clearly labeled as assumption-breakers, not proposals, so they aren't mistaken for real plans.
- Respect stated hard constraints in convergence; if a pick violates one, surface the trade-off rather than hiding it.
- Do not fabricate market evidence to make an idea look viable — the soft screen is qualitative and labeled as such.

## Example
**Founder input:** "We run a local bakery. Core opportunity: grow revenue without opening a second storefront. Ambition: balanced. Constraint: no new full-time hires this year."
**Grounded:** (1) extend hours / add weekend brunch; (2) add a loyalty punch-card; (3) sell day-old goods at a discount.
**Spaced-Out:** (1) bake bread on a moving train; (2) 3 a.m. dream-delivery drones — *insight unlocked:* people want fresh bread without coming to the shop.
**Blue-Sky:** (1) a subscription "fresh loaf" pickup + neighborhood drop program using existing staff on the morning route (leverages: existing production + brand loyalty; solves: convenience; risk: logistics); (2) wholesale supply to nearby cafés (leverages: excess morning capacity; solves: cafés' need for fresh product; risk: margin pressure).
**Converged picks (balanced):** (1) subscription fresh-loaf program — no new hires (uses morning capacity), differentiated, recurring revenue; (2) café wholesale — leverages idle capacity. Differentiation flag: false. Soft five-char check on pick 1: all plausible.
**Executed vs. approval:** Wrote idea set + two picks to `strategy`, proposed running `opportunity-feasibility-analysis` on the subscription program. Nothing committed — pursuit is the founder's call.

## Provenance
SOURCE. Directly implements the IdeaSpace Divergent Ideation Framework (Grounded / Spaced-Out / Blue-Sky tiers, diverge-then-converge, "lots of ideas" operating principle) with a soft pre-screen against the Five Characteristics of a Good Opportunity. See `internal/PROVENANCE_MAP.md`.
