---
name: competitive-advantage-assessment
domain: marketing
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [market.competitors, market.differentiation, customers.personas, customers.segments, offerings, metrics]
writes: [market.differentiation, offerings, decisions, risks]
related_skills: [customer-value-proposition-builder, customer-persona-builder, market-segmentation, competitive-intelligence-analysis, marketing-funnel-planner]
owned_by_agents: [marketing-agent, strategy-agent]
---

# Skill: Competitive Advantage Assessment

## Purpose
Rate the company's capabilities against competitors on the specific variables the target customer actually cares about, produce a differentiation matrix, and turn the gaps and strengths into concrete improvement actions and a defensible point-of-difference. Founder outcome: a clear, customer-anchored answer to "where do we win, where do we lose, and what should we fix?" — the raw material for the CVP's point-of-difference. [SOURCE]

## When to Use
- Positioning/strategy work: "How do we stack up against competitor X?", "Why should someone pick us over them?", "Where are we weak?"
- Before writing a CVP — its point-of-difference comes from this assessment.
- When a competitor launches something, wins deals against you, or changes price.
- When choosing where to invest to build a durable advantage.

## When NOT to Use
- Broad competitor profiling (who they are, threat levels, market context) → use `competitive-intelligence-analysis` (this skill scores you *against* them on customer-valued variables, using that profiling as input).
- Writing the value statement itself → `customer-value-proposition-builder`.
- Picking the target segment → `market-segmentation`.
- Building the persona → `customer-persona-builder`.

## Required Context
- `market.competitors` — the competitor set (ideally from `competitive-intelligence-analysis`).
- `customers.personas` — the target persona's **decision criteria** (these ARE the variables that matter to the customer). [SOURCE]
- `offerings` — the company's own capabilities to rate.
- Any performance evidence (reviews, win/loss notes, delivery metrics) to ground the ratings.

## Inputs
```yaml
input:
  target_persona:
    id: string
    decision_criteria: [string]      # what the customer values (source of the variables)
  competitors:
    - name: string                   # from market.competitors
      known_strengths: [string]
      price_posture: enum(premium, parity, discount)
  customer_valued_variables: [string]# the variables that matter (from persona if omitted)
  our_capabilities:                  # optional; skill will assess if evidence provided
    - variable: string
      self_rating: enum(strong, average, weak)
      evidence: string
  differentiation_dimensions: [string] # candidate axes: customer service, quality, process, turnaround, materials, expertise, luxury/premium, price
```

## Missing Information Protocol
1. Derive the customer-valued variables from the persona's `decision_criteria` if not supplied — never invent variables the customer doesn't care about. [SOURCE]
2. Ground each capability rating in evidence (reviews, win/loss, delivery data); if none exists, mark the rating `unverified` and lower confidence.
3. If competitor capabilities are unknown, pull from `competitive-intelligence-analysis`; if still unknown, mark `competitor_rating: unknown` — do not guess a competitor's strength.
4. Ask the founder ONE batched question only if both the variables AND the competitor set are missing.

## Diagnostic Questions
- What variables actually matter to THIS customer? (Not what we think is impressive.) [SOURCE]
- How do we perform against each competitor on each of those variables? [SOURCE]
- Where are we weak, and how can we improve performance on those variables? [SOURCE]
- How do we maintain the advantage over time? [SOURCE]
- On which dimension can we differentiate durably — customer service, quality, process, turnaround, materials, expertise, premium, or price? [SOURCE]

## Analysis Framework
**Differentiate on any of** (the dimension menu): customer service, quality, better processes, faster turnaround, materials, consulting/expertise, luxury/premium, price. [SOURCE]

**Method — the Competitive Advantage Matrix:** [SOURCE]
1. List the **Key Competitive Variables that matter to the customer** (from the persona's decision criteria) — rows.
2. List the company and each competitor — columns.
3. Rate **Your Capabilities vs. each competitor** on every variable (strong / average / weak, or a 1–5 scale).
4. Read the matrix: variables where you are strongest relative to competitors AND that the customer values highly = your **point-of-difference candidates**. Variables where you are weak on a high-value criterion = **priority fixes**.
5. For each weakness on a valued variable, define an improvement action; for each strength, define how to **maintain** it over time. [SOURCE]

The output's point-of-difference feeds directly into the CVP's fourth element. [SOURCE]

## Calculations
- **Weighted advantage score (optional):** for each variable, (your rating − best competitor's rating) × customer-importance weight; sum across variables for a net differentiation score. Ratings 1–5; importance weight 1–3. Positive = net advantage. [CLAUDE scoring convention layered on the SOURCE matrix]
- **Advantage durability check:** a strength is durable if it is hard for competitors to copy (e.g. proprietary process, brand, relationships) vs. easily copied (e.g. a temporary price cut). Qualitative flag, not a number. [SOURCE intent]

## Decision Rules
- IF a variable does not matter to the target customer THEN exclude it from the matrix — only customer-valued variables count. [SOURCE]
- IF the company is weak on a HIGH-importance variable THEN it is a priority fix → define an improvement action before leaning on any other advantage. [SOURCE]
- IF the company is strong on a high-importance variable AND competitors are not THEN it is the point-of-difference → feed it to the CVP. [SOURCE]
- IF the only advantage is price THEN flag it as fragile (easily matched) and recommend building a non-price, harder-to-copy advantage. [SOURCE intent]
- IF a competitor rating is unknown THEN mark it and lower confidence; do not fabricate the competitor's capability. [guardrail]
- IF no variable shows a clear advantage THEN escalate — the offering may lack differentiation and positioning/strategy work is needed. [SOURCE]
- IF a strength is easily copied THEN pair it with a plan to deepen it (durability) rather than treating it as a moat. [SOURCE]

## Procedure
1. Pull the customer-valued variables from the target persona's decision criteria.
2. Assemble the competitor set (from `competitive-intelligence-analysis` / `market.competitors`).
3. Build the matrix: variables × (company + competitors).
4. Rate the company on each variable, grounded in evidence; rate competitors from intel (mark unknowns).
5. Optionally compute the weighted advantage score using customer-importance weights.
6. Identify point-of-difference candidates (strong + high-value + durable) and priority fixes (weak + high-value).
7. For each fix, write an improvement action; for each strength, write a maintenance action.
8. Assess durability of the top advantage.
9. Write differentiation to `market.differentiation`; hand the point-of-difference to `customer-value-proposition-builder`; log any capability gap as a `risk` if it threatens the position.

## Output
```yaml
output:
  matrix:
    variables:
      - name: string
        customer_importance: enum(high, medium, low)
        our_rating: enum(strong, average, weak) | unverified
        competitor_ratings: [{competitor: string, rating: enum(strong, average, weak) | unknown}]
        verdict: enum(point_of_difference, parity, priority_fix)
  weighted_advantage_score: number | null
  point_of_difference: string          # the primary durable advantage → feeds CVP element 4
  point_of_difference_durability: enum(durable, moderate, fragile)
  priority_fixes:
    - variable: string
      gap: string
      improvement_action: string
      effort: enum(low, medium, high)
  maintenance_actions: [string]        # how to defend current strengths
  price_only_flag: bool
  capability_risk_flagged: bool
  provenance: {source: agent_analysis, as_of: date, confidence: 0.0-1.0}
```

## Recommendations
Lead the positioning with the strongest, most durable advantage on a high-importance variable — not the one the founder is proudest of. Prioritize fixes by (customer importance × gap size) ÷ effort so the highest-leverage improvement comes first. Warn against price-only differentiation and recommend a harder-to-copy axis. If nothing differentiates, recommend a strategy conversation before spending on marketing. [SOURCE]

## Execution Opportunities
- Write the differentiation matrix + point-of-difference to `market.differentiation` (reversible, LOW). [L1]
- Create improvement-action tasks for each priority fix (reversible, LOW).
- Log a capability-gap `risk` if a weakness threatens the position (reversible, LOW).
- Draft the competitive matrix document for founder review (reversible, LOW).
- Hand the point-of-difference to `customer-value-proposition-builder` (reversible, LOW).

## Human Approval Requirements
- Assessment, matrix, and recommendations: always allowed (analysis). [§5]
- This skill produces internal analysis — it triggers no ad spend, publishing, or email blasts, so those approvals don't apply here. Any external competitive *comparison content* derived from this (e.g. a public "us vs. them" page) goes through the content/channel skills where **publishing public content requires founder approval**, and comparative claims about named competitors should be checked with Legal Liaison. [§4]
- Improvement actions that require budget or headcount route to the CFO/Operations/People agents and the founder for approval before execution.

## Escalation Conditions
- No variable shows a clear advantage → escalate to Strategy Agent/founder (possible lack of differentiation). [§7 strategic]
- A priority fix requires material spend or hiring → route to CFO / People agents. [§7 financial/people]
- Public comparative claims about a named competitor → Legal Liaison (disparagement/false-advertising risk). [compliance]
- Competitor data is low-confidence and would change the verdict → surface uncertainty; don't lock positioning. [§7 data]

## KPIs
- Positioning clarity: a durable point-of-difference identified on a high-value variable.
- Win/loss: win-rate improvement vs. the assessed competitors after acting on fixes.
- Fix execution: priority fixes closed over time.
- Durability: how long the advantage holds before competitors close the gap.

## Monitoring
Track win/loss reasons against the matrix — if you keep losing on a variable rated "strong," the rating (or the customer's perception) is wrong. Re-check when a competitor changes offering or price. Watch that priority fixes actually move the variable.

## Follow-Up
Re-run when a competitor changes strategy/price, when win/loss patterns shift, before each CVP revision, after acting on a priority fix, or at the quarterly strategy/marketing refresh.

## Related Skills
Consumes `competitive-intelligence-analysis` (competitor profiles) and `customer-persona-builder` (decision criteria = the variables). Directly feeds `customer-value-proposition-builder` (point-of-difference) and `marketing-funnel-planner` (Desire-stage comparison content). Escalates fixes to CFO / Operations / People agents.

## Guardrails
- Rate only variables the customer values; a strength the customer doesn't care about is not an advantage. [SOURCE]
- Ground ratings in evidence; mark unverified/unknown honestly and lower confidence.
- Do not fabricate competitor capabilities.
- Price-only advantage is fragile — flag it.
- Comparative claims about named competitors must be truthful and, for public use, legally reviewed.

## Example
**Founder input:** Ember & Oak Candles vs. two competitors — "BigBox Home" (mass-market retailer) and "Luxe Wick Co." (premium online candle brand). Target persona = "Maria," whose decision criteria are: uniqueness, supports-local, quality/scent, price, and gift presentation.

**Skill reasoning — matrix (customer-valued variables only):**

| Variable | Importance | Ember & Oak | BigBox Home | Luxe Wick | Verdict |
|---|---|---|---|---|---|
| Uniqueness (made-to-order) | high | strong | weak | average | **point of difference** |
| Supports-local | high | strong | weak | weak | **point of difference** |
| Quality / scent | high | strong | average | strong | parity (vs. Luxe) |
| Gift presentation (personal note) | medium | strong | weak | average | point of difference |
| Price | medium | average | strong | weak | **priority fix** (BigBox undercuts) |

- Weighted advantage score: positive net (strong on three high-importance variables).
- point_of_difference = "made-to-order custom scents + local, hand-poured craft with a personalized gift note" — **durable** (hard for BigBox to copy at scale; distinct from Luxe's premium-generic line).
- Priority fix: price gap vs. BigBox — but do NOT compete on price (fragile). Improvement action = justify the price with the uniqueness/local story and add a lower-priced entry SKU (medium effort). price_only_flag = false.
- Maintenance: protect the made-to-order advantage by expanding scent options faster than competitors.

**Output:** matrix + durable point-of-difference (→ CVP), one priority fix (entry-price SKU, not a price war), maintenance action (scent library). No capability risk severe enough to log.

**Executed vs. approval:** Skill wrote the matrix and point-of-difference to `market.differentiation`, drafted the document, handed the point-of-difference to the CVP builder, and created the "entry SKU" fix task (all LOW, auto). The entry-SKU decision (pricing/margin impact) routes to the CFO Agent + founder before execution; any public "why us vs. big-box" comparison page would need publishing approval + legal review.

## Provenance
SOURCE. Derives from the Competitive Advantage / Differentiation model: the differentiation dimension menu (service, quality, process, turnaround, materials, expertise, premium, price) and the Competitive Advantage Matrix method (rate Your Capabilities vs. competitors on the Key Competitive Variables that matter to the customer, then act on weaknesses). The weighted-advantage score and durability framing are CLAUDE conventions layered on the source matrix and flagged inline. See `internal/PROVENANCE_MAP.md`.
