---
name: competitive-intelligence-analysis
domain: strategy
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [company, offerings, customers, market, strategy, goals]
writes: [market, strategy, decisions]
related_skills: [opportunity-feasibility-analysis, growth-lever-selector, strategic-planning, risk-diagnostic]
owned_by_agents: [strategy-agent]
---

# Skill: Competitive Intelligence Analysis

## Purpose
Give the founder a clear-eyed map of who the business competes with now, who it should benchmark against as it scales, and how it stacks up on the dimensions customers actually value — plus a threat level per competitor and a concrete plan to learn what isn't yet known. Turns vague "we have competitors" anxiety into an ongoing, actionable intelligence grid.

## When to Use
- The founder asks "who are we up against?", "why are we losing deals?", "who should we watch?"
- During `opportunity-feasibility-analysis` (the Competition dimension calls this skill).
- Before entering a new market/segment (from `growth-lever-selector`) — to size the competitive barrier.
- On a periodic cadence (recommended every ~6 months) to keep the intelligence fresh.

## When NOT to Use
- The task is internal capability/resource gaps → `resource-gap-analysis`.
- The task is choosing a growth avenue → `growth-lever-selector`.
- A specific competitor's legal/IP threat needs handling → route to attorney.
- No customer-valued dimensions are known yet — establish those first (from `customers`/feasibility) so the benchmark is meaningful.

## Required Context
Reads `customers` (what this segment values — the benchmark dimensions), `offerings` (own position), `company` (competitive advantage, aspiration/scale target), `market` (segment, known competitors, trends), `goals`. Needs the customer-valued dimensions to benchmark on; without them, the grid measures the wrong things. Public/observable competitor data feeds the "what I know" columns; unknowns become the research plan.

## Inputs
```yaml
input:
  own_business: {name: str, offering: str, competitive_advantage: str, aspiration_scale: str}
  customer_valued_dimensions: [str]   # what THIS segment actually cares about (price, speed, quality, service, selection, convenience, trust...)
  current_competitors: [ {name: str, known: object} ]      # who we compete with now
  aspirational_competitors: [ {name: str, known: object} ] # who we want to compete with as we scale
  observable_data:                    # public/observable signals to populate the grid
    general_info: object
    market_share: object
    uniqueness: object
  research_budget: enum(none, light, moderate)   # how much effort to spend closing gaps
```

## Missing Information Protocol
1. Populate the grid from observable/public data and memory first (websites, pricing pages, reviews, marketplace listings).
2. For every cell that cannot be filled, DO NOT guess a competitor's number — log it in "what I need to learn" with "how I will learn it" (the framework's core rule).
3. Ask the founder only for what they uniquely know (why they win/lose specific deals, which competitor customers switch to).
4. Never state a competitor's market share, cost structure, or roadmap as fact unless sourced — label inferences as inferences with confidence.

## Diagnostic Questions
- Who are your current competitors, and what do you know about them (general info, market share, uniqueness)?
- On the dimensions customers value, how does each competitor compare to you?
- What do you provide that they cannot — and what do they provide that you cannot?
- How easily can you enter their space, and how easily can others enter yours (barriers)?
- Who should your competitors be as you grow (aspirational benchmarks)?
- What don't you know about each competitor, and how/where will you learn it?

## Analysis Framework
The Competitive Mapping / Benchmarking Grid plus a customer-valued-dimension benchmark and a threat assessment:
- **Rows:** Current Competitors and Aspirational Competitors (who you want to compete with as you scale).
- **Know-columns:** General Info · Market Share · Uniqueness.
- **Learn-columns:** What I Need to Learn · How I Will Learn It.
- **Benchmark overlay:** score self and each competitor on each `customer_valued_dimension` (relative scale) to reveal where you win, where you're at parity, and where you're beaten.
- **Threat assessment:** per competitor, combine competitive strength (how well they serve the valued dimensions) with momentum (are they growing/entering your space) and entry barriers into a threat level.
- **Barriers analysis:** ease of your entry into their space vs. ease of others entering yours.

## Calculations
- **Relative benchmark score:** for each competitor and each `customer_valued_dimension`, score −2 (much worse than us) … 0 (parity) … +2 (much better than us). Sum across dimensions (optionally weighted by how much the segment values each) → a relative-strength index per competitor.
- **Win/parity/loss profile:** count dimensions where we lead (+), match (0), lag (−) each competitor.
- **Threat level (SYNTH heuristic):** `Threat = competitive_strength × momentum × (1 / entry_barrier_to_our_space)`, mapped to High / Medium / Low. A strong competitor actively entering our space with low barriers = High threat; a strong but static competitor in an adjacent niche = Medium; a weak/distant one = Low.
- **Differentiation index:** number of valued dimensions on which we are the sole "+" performer (our defensible edge).
- No source numeric benchmarks; the grid and column structure are source-derived; threat/benchmark scoring is SYNTH.

## Decision Rules
- **IF** we lag a competitor on a dimension the segment values highly **THEN** flag a competitive weakness → feed `strategic-planning` / `initiative-prioritization`.
- **IF** we lead on a valued dimension no competitor matches **THEN** that is a defensible advantage to protect and amplify in positioning.
- **IF** a competitor is strong AND gaining momentum AND barriers to our space are low **THEN** threat = High → escalate to founder + `risk-diagnostic`.
- **IF** barriers to others entering our space are low **THEN** flag an entry-threat risk regardless of current competitors.
- **IF** a competitor cell is unknown **THEN** add it to the research plan with a named method; do not fabricate.
- **IF** aspirational competitors far outperform on valued dimensions **THEN** the gap defines the capability roadmap for scaling → `resource-gap-analysis`.
- **IF** the customer_valued_dimensions are guessed rather than evidenced **THEN** flag low confidence and recommend validating them with customers before acting on the benchmark.
- **NEVER** obtain competitor intelligence through deception, misrepresentation, or unauthorized access — public/observable and voluntarily-shared sources only.

## Procedure
1. Confirm the customer-valued dimensions (from `customers`/feasibility); flag if unvalidated.
2. List current and aspirational competitors.
3. Populate the know-columns (general info, market share, uniqueness) from observable data + memory.
4. Score self and each competitor on each valued dimension; compute relative-strength, win/parity/loss, and differentiation index.
5. Assess entry barriers (ours into theirs; others into ours).
6. Compute threat level per competitor.
7. For every unknown cell, write "what I need to learn" + "how I will learn it," scoped to `research_budget`.
8. Identify defensible advantages and competitive weaknesses.
9. Write the grid + threat map + research plan to `market`/`strategy`; propose follow-on skills.

## Output
```yaml
output:
  benchmark_dimensions: [str]
  dimensions_confidence: enum(validated, assumed)
  grid:
    - competitor: str
      type: enum(current, aspirational)
      general_info: str
      market_share: str               # sourced or "unknown → research plan"
      uniqueness: str
      dimension_scores: {<dimension>: int}   # -2..+2 relative to us
      relative_strength_index: number
      win_parity_loss: {win: int, parity: int, loss: int}
      entry_barrier_to_our_space: enum(low, medium, high)
      threat_level: enum(High, Medium, Low)
      what_to_learn: [str]
      how_to_learn: [str]
  our_defensible_advantages: [str]     # valued dimensions where we alone lead
  our_competitive_weaknesses: [str]    # valued dimensions where we lag
  differentiation_index: int
  entry_threat_to_our_space: enum(high, medium, low)
  research_plan: [ {competitor: str, question: str, method: str, effort: enum(light, moderate) } ]
  recommended_next_skills: [str]
```

## Recommendations
The output leads with two lists the founder can act on immediately — defensible advantages (protect and market these) and competitive weaknesses (close or route to planning) — followed by a threat-ranked competitor map. Every unknown becomes a scoped research task rather than a guess, so the intelligence gets more accurate over time. Benchmarks built on assumed (unvalidated) customer priorities are explicitly flagged so the founder doesn't over-trust them.

## Execution Opportunities
- Write the benchmarking grid + threat map to `market`/`strategy` and a decision record — reversible, LOW.
- Create research tasks for each intelligence gap (with method + effort) — reversible, LOW.
- Draft a positioning note highlighting defensible advantages for marketing to use — reversible, LOW (drafting only; publishing is out of scope).
- Route High-threat competitors to `risk-diagnostic` — reversible, LOW.
No external outreach, no competitor contact, no published content — all such actions are out of scope and approval-gated elsewhere.

## Human Approval Requirements
- Any externally published competitive positioning/claims require founder (and brand/legal) approval — this skill only drafts internally.
- Purchasing paid market/competitor data reports requires founder approval.
- Any research method involving contacting or engaging a competitor requires founder approval and must be ethical/lawful.

## Escalation Conditions
- **High-threat competitor entering our space with low barriers** → founder + `risk-diagnostic`.
- **Competitor IP/patent or trademark conflict surfaced** → attorney.
- **Aspirational-competitor gap implies a major capability build** → founder + `resource-gap-analysis`.
- **Only assumed (unvalidated) customer priorities available** → surface low confidence; recommend validating with customers before strategic action.

## KPIs
- Intelligence coverage: % of grid cells filled with sourced data vs. open research tasks.
- Research closure rate: % of research-plan items completed each cycle.
- Predictive value: threat levels that correctly anticipated competitor moves / deal losses.
- Positioning impact: win-rate change on dimensions where a defensible advantage was emphasized.

## Monitoring
Refresh the grid on cadence and whenever a competitor makes a visible move (price change, new entry, funding, product launch). Watch entry barriers to your space and any competitor gaining momentum. Track whether closing research gaps changes the threat assessment.

## Follow-Up
- Time-triggered: refresh roughly every 6 months (source-recommended competitive-analysis cadence), identifying key differentiation/improvement areas each time.
- Event-triggered: before entering a new market, or when deal-loss patterns shift.

## Related Skills
Called by `opportunity-feasibility-analysis` (Competition dimension) and `growth-lever-selector` (market-entry barriers). Feeds `strategic-planning`, `initiative-prioritization`, and `risk-diagnostic`. Pairs with `resource-gap-analysis` for aspirational-competitor capability gaps.

## Guardrails
- Obtain intelligence only from public/observable/voluntarily-shared sources — never through deception, misrepresentation, pretexting, or unauthorized access.
- Never state a competitor's private data (share, cost, roadmap) as fact without a source; label inferences and their confidence.
- Do not publish competitive claims externally from this skill — draft only.
- Flag benchmarks built on assumed customer priorities; validate before acting.
- Respect IP/trademark boundaries; route conflicts to legal.

## Example
**Founder input:** "Boutique fitness studio. We keep losing new sign-ups to a big-box gym and a nearby class-pass studio. Customers seem to value class quality, schedule flexibility, community, and price. I want to eventually compete with the premium regional chain."
**Dimensions (validated from member surveys):** class quality, schedule flexibility, community, price.
**Grid (abridged):**
- Big-box gym (current): general — 24/7, low price; share — large locally; uniqueness — price + hours. Scores vs. us: quality −1, flexibility +2, community −2, price +2 → relative strength +1; win/parity/loss for us = 2/0/2. Entry barrier to our space: medium. Threat: **Medium** (strong on price/hours, weak on our core community/quality).
- Class-pass studio (current): quality 0, flexibility +1, community 0, price +1 → relative strength +2; threat **High** (closest substitute, momentum rising, low barrier). What to learn: their retention + pricing tiers → method: mystery-shop + public pricing page.
- Premium regional chain (aspirational): scores mostly +1/+2 → defines capability roadmap; what to learn: their per-studio economics → method: industry reports (moderate effort).
**our_defensible_advantages:** community, class quality (sole "+" on both vs. current competitors). **weaknesses:** schedule flexibility, price. **entry_threat_to_our_space:** medium. **differentiation_index:** 2.
**research_plan:** mystery-shop the class-pass studio's onboarding + pricing (light); pull regional-chain economics from industry data (moderate).
**Executed vs. approval:** Wrote grid + threat map + research plan to `market`, created two research tasks, drafted an internal positioning note ("lead with community + quality; address flexibility gap"). Routed the High-threat class-pass studio to `risk-diagnostic`. No external content published, no competitor contacted.

## Provenance
SOURCE. Implements the Competitive Mapping / Benchmarking Grid (current vs. aspirational rows; General Info / Market Share / Uniqueness know-columns; What-to-Learn / How-to-Learn research columns) plus the source's every-6-months competitive-analysis cadence, overlaid with a customer-valued-dimension benchmark and a threat assessment (SYNTH scoring). See `internal/PROVENANCE_MAP.md`.
