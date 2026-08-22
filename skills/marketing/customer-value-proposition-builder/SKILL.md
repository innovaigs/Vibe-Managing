---
name: customer-value-proposition-builder
domain: marketing
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [customers.personas, customers.segments, offerings, market.competitors, market.differentiation]
writes: [offerings, customers.personas, decisions]
related_skills: [customer-persona-builder, competitive-advantage-assessment, market-segmentation, marketing-funnel-planner, buyers-journey-mapper]
owned_by_agents: [marketing-agent, growth-agent]
---

# Skill: Customer Value Proposition Builder

## Purpose
Produce a sharp, scored Customer Value Proposition (CVP) — an internal statement of why a specific customer should buy from this company rather than a competitor — using a fixed formula, then grade it and suggest one improving edit. Founder outcome: a clear decision-rationale that anchors all messaging, pricing, and sales conversations. A CVP is internal reasoning, not a tagline. [SOURCE]

## When to Use
- Positioning work: "Why should anyone buy from us?", "What's our value prop?", "Tighten our pitch."
- After a persona and a competitive-advantage assessment exist and the founder needs to crystallize the value.
- Before building a funnel, writing content, or setting price — the CVP is the message spine.
- When sales conversations wander because there's no crisp "why us."

## When NOT to Use
- Writing external ad copy, a slogan, or a tagline → the CVP is internal-facing; hand it to a copy/content skill to derive external messaging. [SOURCE]
- No persona or differentiation exists → run `customer-persona-builder` and `competitive-advantage-assessment` first (they supply the "who/benefit" and "point-of-difference").
- Choosing the target segment → `market-segmentation`.

## Required Context
- `customers.personas` — the target group and their primary pain/need (the "who" + need).
- `offerings` — what the product/service is and its benefits (the "what" + benefits).
- `market.competitors` and `market.differentiation` — the point-of-difference vs. alternatives (from `competitive-advantage-assessment`).
- Whether the buyer is B2C, B2B, or B2G — selects the value menu emphasis.

## Inputs
```yaml
input:
  target_group_and_need: string    # who + the need/pain (from persona)
  brand: string                    # the product/service/company name to slot into the formula
  offering:
    what_it_is: string             # element 1: what the product/service is
    primary_benefits: [string]     # element 3: primary benefits to the target
  point_of_difference: string      # element 4: what makes it better than competitors (may include price)
  business_type: enum(B2C, B2B, B2G)
  cvp_coach_answers:               # optional; the 5 sharpening answers
    ideal_customer_plain: string
    problem_keeping_them_up: string
    how_it_fixes: string
    why_different_better: string
    proof: string
```

## Missing Information Protocol
1. Pull the "who + need" from the persona and the "point of difference" from `competitive-advantage-assessment` before asking the founder.
2. If any of the four required elements is missing, ask the 5 CVP-coach questions (below) in ONE batched message; do not invent benefits or differentiation.
3. If the point-of-difference is weak/unknown, route back to `competitive-advantage-assessment` rather than fabricating a claim.
4. Never assert a benefit or proof the company cannot substantiate — unproven claims are a compliance risk.

## Diagnostic Questions
CVP-coach question set (ask, then assemble): [SOURCE]
1. Who is my ideal customer, in plain language?
2. What problem/need keeps them up at night?
3. How does my product/service fix it?
4. Why is my solution different/better than the alternatives?
5. What proof/examples back up the claims?

## Analysis Framework
**The CVP formula (exact template):** [SOURCE]
> **To [target group and need], our [brand] can/will [provide service/benefits] that will [point-of-difference].**

**The four required elements** every CVP must contain: [SOURCE]
1. **What** the product or service is.
2. **Who** should use it (target customer).
3. **Primary benefits** to the target customer.
4. **Point of difference** — the benefits that make it better than competitors (may include price).

**What a CVP IS vs. IS NOT:** [SOURCE]
- IS: internally-facing; specifically targeted at potential customers (not employees/partners/suppliers); a decision-rationale for buying from you over competitors.
- IS NOT: a tagline; external ad copy; a marketing/advertising slogan.

**Value-created menu by customer type** (to sharpen the benefit language): [SOURCE]
- **B2C:** more time with family, improved health, live longer, increased happiness, financial security, pursue a passion.
- **B2B:** increasing revenue, reducing cost, improving processes.
- **B2G:** simplicity, efficiency, reliability.

## Calculations
**CVP Gauge (quality score):** [SOURCE]
- Identified **2 of 4** elements → **weak**.
- Identified **3 of 4** elements → **adequate**.
- Identified **all 4** elements AND the statement is impactful/specific → **strong**.

Score = count of the four elements present, plus an impact/specificity check that gates "strong."

## Decision Rules
- IF the CVP hits only 2–3 of the 4 elements THEN it is weak/adequate → revise until all four (what / who / benefit / point-of-difference) are present AND specific before publishing anything from it. [SOURCE]
- IF all 4 elements are present but the statement is vague/generic THEN it is at most "adequate," not "strong" — sharpen with concrete numbers or a named difference. [SOURCE]
- IF business_type is B2B THEN frame benefits as revenue up / cost down / process improved; IF B2G THEN simplicity / efficiency / reliability; IF B2C THEN the life-outcome menu. [SOURCE]
- IF a benefit or proof cannot be substantiated THEN remove or qualify it — do not ship unverifiable claims. [compliance guardrail]
- IF the point-of-difference is "price" alone THEN warn that price-only differentiation is fragile and recommend adding a non-price difference. [SOURCE intent]
- IF two personas differ materially THEN write a separate CVP per persona — one CVP cannot serve distinct buyers. [SOURCE]

## Procedure
1. Gather the four elements: who+need (persona), what+benefits (offering), point-of-difference (competitive assessment).
2. If gaps remain, run the 5 CVP-coach questions in one batch.
3. Assemble the statement into the exact formula: "To [target+need], our [brand] can/will [benefits] that will [point-of-difference]."
4. Tune benefit language using the value menu for the business type.
5. Score on the CVP Gauge (2/3/4 elements + impact check).
6. Suggest exactly ONE sharpening edit (add specificity, quantify, strengthen the difference).
7. If weak/adequate, iterate once with the founder; if strong, finalize.
8. Write the CVP to the offering (`offerings.cvp_id`) and link the persona; hand to `marketing-funnel-planner` and content skills.

## Output
```yaml
output:
  cvp:
    statement: string              # the filled formula
    elements_present:
      what: bool
      who: bool
      benefits: bool
      point_of_difference: bool
    score: enum(weak, adequate, strong)
    impactful_and_specific: bool
    business_type: enum(B2C, B2B, B2G)
    persona_id: string
    sharpening_edit: string        # the one recommended improvement
    unproven_claims_flagged: [string]
  provenance: {source: agent_analysis, as_of: date, confidence: 0.0-1.0}
```

## Recommendations
Do not release a CVP scored below "strong" for use in a funnel or content — an adequate CVP produces mushy messaging. Prioritize a single, specific, defensible point-of-difference over a long benefit list. Recommend a non-price difference if price is the only one. Always surface any claim the company cannot yet prove, so it's fixed before it reaches customers. [SOURCE]

## Execution Opportunities
- Write the CVP to `offerings.cvp_id` and link it to the persona (reversible, LOW). [L1 draft]
- Draft the CVP statement + gauge report for founder review (reversible, LOW).
- Create a task to gather proof/testimonials for any flagged unproven claim (reversible, LOW).
- Log a decision record capturing the chosen positioning (reversible, LOW).

## Human Approval Requirements
- Drafting and scoring the CVP: always allowed (internal analysis). [§5]
- The CVP itself is internal, so it needs no publishing approval. BUT any *external* content derived from it — ad copy, a public landing page, an email blast — must go through the owning content/channel skill, where **publishing public content and email blasts require founder approval**, and **ad spend requires founder approval**. Do not let CVP language ship externally without that approval. [§4; task approval model]
- Adopting the CVP as the offering's official positioning is presented for founder confirmation (it steers pricing and messaging).

## Escalation Conditions
- The point-of-difference is unclear or unsubstantiated → route to `competitive-advantage-assessment`; do not fabricate. [§7]
- A benefit claim touches a regulated area (health, financial, safety outcomes) → flag to Legal Liaison before any external use. [compliance]
- Persona/differentiation inputs are low-confidence → surface uncertainty; don't lock positioning.

## KPIs
- CVP strength: share of active offerings with a "strong" CVP.
- Message consistency: downstream content/sales use the CVP language.
- Conversion lift after messaging is aligned to the CVP.
- Claim integrity: zero unproven claims reaching external channels.

## Monitoring
Watch whether sales/content actually use the CVP and whether it improves conversion at the Evaluation stage. If competitors erode the point-of-difference, re-run. Re-check any claim as products change.

## Follow-Up
Re-run when the persona, offering, or competitive landscape changes; when a new offering launches; after a competitive-advantage refresh; or at the quarterly marketing refresh. Any "weak/adequate" CVP should be revisited before the next campaign.

## Related Skills
Consumes `customer-persona-builder` (who+need) and `competitive-advantage-assessment` (point-of-difference). Feeds `marketing-funnel-planner` (message spine), content/copy skills (external derivations), and pricing. Complements `buyers-journey-mapper` (Evaluation-stage differentiation).

## Guardrails
- The CVP is internal — never publish it verbatim as a tagline or ad. [SOURCE]
- Every benefit and proof must be substantiable; flag and hold unverifiable claims. [compliance]
- Price-only differentiation is fragile — warn and recommend a durable difference.
- One CVP per distinct persona; don't stretch one across incompatible buyers.

## Example
**Founder input:** target = "Maria — Thoughtful Local Gifter" (need: a unique gift that isn't generic); brand = "Ember & Oak Candles"; what = hand-poured small-batch candles; benefits = one-of-a-kind, supports a local maker, thoughtful presentation; point-of-difference = made-to-order scents you can't get at big-box stores, personalized gift notes; B2C.

**Skill reasoning:**
- Assemble formula: "To **thoughtful gift-givers who want something personal and not mass-produced**, our **Ember & Oak Candles** will **deliver hand-poured, made-to-order candles with custom scents and a personalized gift note** that will **give a one-of-a-kind, locally-made gift you can't find at big-box stores**."
- Elements: what ✓ / who ✓ / benefits ✓ / point-of-difference ✓ → 4 of 4.
- Impact/specificity: "made-to-order custom scents + personalized note + not available at big-box" is specific → **strong**.
- Value menu (B2C): maps to "increased happiness / pursue a passion (thoughtful giving)."
- Sharpening edit: quantify or name the difference further — e.g. "50+ custom scent combinations" — to make it even more concrete.
- Unproven claims: none, but verify "50+ scents" before using externally.

**Output:** strong CVP + one sharpening edit + a note to confirm the scent count before external use.

**Executed vs. approval:** Skill wrote the CVP to the offering and drafted it for review (LOW, auto). Using its language in the upcoming Instagram ad set is held for founder approval, since ad spend and public publishing require it.

## Provenance
SOURCE. Derives from the Customer Value Proposition model: the exact formula "To [target group and need], our [brand] can/will [benefits] that will [point-of-difference]," the four required elements, the IS/IS-NOT distinction, the value-created menu by customer type, and the CVP Gauge (2/3/4-element scoring). See `internal/PROVENANCE_MAP.md`.
