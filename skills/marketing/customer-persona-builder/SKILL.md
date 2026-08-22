---
name: customer-persona-builder
domain: marketing
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [customers.segments, customers.personas, customers.accounts, offerings, market]
writes: [customers.personas, decisions]
related_skills: [market-segmentation, buying-center-mapper, buyers-journey-mapper, customer-value-proposition-builder, marketing-funnel-planner, channel-selection]
owned_by_agents: [marketing-agent, growth-agent]
---

# Skill: Customer Persona Builder

## Purpose
Turn a chosen market segment into a concrete, named persona card the whole business can picture — a fictional character standing in for the typical buyer, with their identity, motivations, pains, and daily life mapped out. Founder outcome: "I can see exactly who I'm selling to," which makes every message, channel, and offer decision sharper. [SOURCE]

## When to Use
- After picking a target segment: "Who is our customer, really?", "Build me a customer profile," "Who am I writing this ad for?"
- Before writing a CVP, a funnel, or content — the persona is the input that makes them specific.
- When the team keeps marketing generically because no one shares a clear picture of the buyer.
- When a segment serves two distinct buyer types (e.g. the user vs. the person who pays) and each needs its own card.

## When NOT to Use
- No target segment has been chosen yet → run `market-segmentation` first.
- The question is who signs off on a specific complex/B2B deal → use `buying-center-mapper` (roles in one purchase, not a segment archetype).
- Mapping what the persona does across the purchase → `buyers-journey-mapper`.
- You need the value statement, not the buyer profile → `customer-value-proposition-builder`.

## Required Context
- `customers.segments` — the target segment(s) this persona represents (from `market-segmentation`).
- `offerings` — what the persona would buy and its use-case.
- Any real customer knowledge in `customers.accounts` (interviews, reviews, order history) to ground the persona in reality rather than imagination.
- `market` — competitors the persona might also consider.

## Inputs
```yaml
input:
  segment:
    id: string
    name: string
    definition: string           # variables that define the segment
    business_type: enum(B2C, B2B, B2G)
  deep_dive_answers:             # the 7 going-deeper questions (see Diagnostic Questions)
    cares_about: string          # what they care about re: the solution (price/quality/service/delivery)
    wants_hopes_dreams_fears: string
    biggest_pain: string
    why_they_need_it: string     # build something / solve a problem / impulse
    where_they_get_info: [string]# website, store, search, social, print, radio, word-of-mouth
    desired_feeling_after: string# biggest intended takeaway
    age_band: string             # or firmographic anchor for B2B
  role_flag: enum(user, decision_maker, both)
  b2b_anchor:                    # if B2B/B2G
    job_title: string
    industry: string
    company_size: string
    geography: string
    responsibilities: [string]
```

## Missing Information Protocol
1. Prefer real evidence: pull from customer interviews, reviews, support tickets, and order history in `customers.accounts` before inventing traits.
2. If deep-dive answers are missing, ask the founder the 7 going-deeper questions in ONE batched message (not one at a time in a live-chat sense — a single form).
3. If only partial answers exist, build a DRAFT persona, fill gaps with clearly-labeled `assumption:` fields, and run the completeness check so the founder sees exactly what's missing.
4. Never present an assumption as a known fact; flag confidence per quadrant.

## Diagnostic Questions
The 7 going-deeper questions (asked/answered to fill the card): [SOURCE]
1. What does this group care about relative to my solution (price, quality, service, delivery)?
2. What are their wants, hopes, dreams, and fears that compel them to act?
3. What is their single biggest pain point that needs my solution?
4. Why do they need it — to build something else, solve a problem, or impulse?
5. Where do they get information / help / answers (website, store, search, social, print, radio)?
6. How should they feel after using the product — biggest intended takeaway?
7. Is this persona complete? Can I visualize this person? What is missing?

## Analysis Framework
Build the persona on **four quadrants**, then validate. [SOURCE]

| Quadrant | Answers | Fed by |
|---|---|---|
| **1. Identity / Demographic ("who")** | Name, age band or firmographic anchor, role/title, situation | segment definition + Q1 |
| **2. Motivations / Psychological ("why")** | Wants, hopes, dreams, fears; emotional triggers; decision criteria | Q2 + Q4 |
| **3. Biggest Pain(s)** | The single dominant pain the offering must solve; secondary pains | Q3 |
| **4. Day in the Life ("what")** | Routines, where they spend time, where they get information, how they buy | Q5 + Q6 |

Then: give the persona a **real first name**, and **tag it User vs. Decision-Maker (DM)** — it can be both. A segment with two distinct buyer types gets two cards. [SOURCE]

**AI prompt scaffold (de-branded)** to draft a persona quickly: "Build a persona of a [job title] at a [industry / size / geography] company with [roles/responsibilities], looking for help with [challenge] and considering [offering]. List their hopes/dreams, fears/concerns, emotional triggers, and decision criteria for choosing a vendor." [SOURCE]

## Calculations
None. Completeness is scored qualitatively (see Decision Rules), not numerically. [SOURCE]

## Decision Rules
- IF a segment contains a distinct User AND a distinct Decision-Maker THEN build a separate persona card for each, and tag each with its `role_flag`. [SOURCE]
- IF the persona cannot be visualized as a real single person (too generic, contradictory traits) THEN it fails the completeness check → gather more input or narrow the segment before proceeding. [SOURCE]
- IF any of the four quadrants is empty THEN mark the persona `draft` and list the missing quadrant as a gap; do not hand a draft persona to CVP/funnel skills as if final. [SOURCE]
- IF the "biggest pain" is vague or plural THEN force-rank to a single dominant pain — the CVP and funnel need one primary pain to anchor on. [SOURCE]
- IF two personas are near-duplicates THEN merge them; over-personifying fragments messaging. [SOURCE]
- IF the persona is a Decision-Maker who is NOT the user (e.g. a parent buying for a child, a manager buying for a team) THEN capture both the DM's decision criteria and the user's needs on the card. [SOURCE]

## Procedure
1. Load the target segment and any real customer evidence.
2. Collect the 7 going-deeper answers (from founder or from evidence).
3. Populate the four quadrants; anchor each field to its source (evidence vs. founder vs. assumption).
4. Assign a first name and the User/DM tag(s); split into two cards if needed.
5. Run the completeness check: is every quadrant filled? Can you picture this person? Is there a single dominant pain? What's missing?
6. Produce a one-page persona card per persona.
7. Write personas to `customers.personas`; hand off to `customer-value-proposition-builder` and `buyers-journey-mapper`.

## Output
```yaml
output:
  personas:
    - id: string
      name: string                       # real first name
      segment_id: string
      role_flag: enum(user, decision_maker, both)
      identity:                          # quadrant 1
        age_band_or_firmographic: string
        role_or_title: string
        situation: string
      motivations:                       # quadrant 2
        wants: [string]
        hopes_dreams: [string]
        fears_concerns: [string]
        emotional_triggers: [string]
        decision_criteria: [string]      # e.g. price, quality, service, delivery
      pains:                             # quadrant 3
        primary_pain: string
        secondary_pains: [string]
      day_in_life:                       # quadrant 4
        routines: string
        where_they_are: [string]         # channels / places
        where_they_get_info: [string]
        how_they_buy: string
      desired_takeaway: string           # how they should feel after
      completeness:
        status: enum(complete, draft)
        visualizable: bool
        gaps: [string]
      confidence_by_quadrant: {identity, motivations, pains, day_in_life}  # 0.0-1.0
  provenance: {source: agent_analysis, as_of: date, confidence: 0.0-1.0}
```

## Recommendations
Prioritize accuracy over vividness — a persona grounded in a real review beats an imaginative one. Recommend which persona is the *primary* target for the first campaign (usually the Decision-Maker if User≠DM, since they control the purchase). Flag the single dominant pain as the anchor the CVP should attack. Recommend interviewing 3–5 real customers to raise any `draft` persona to `complete`. [SOURCE]

## Execution Opportunities
- Write/refresh persona cards in `customers.personas` (reversible, LOW). [L1 draft → L2 once trusted]
- Draft the one-page persona card document for founder review (reversible, LOW).
- Create a task to run 3–5 customer interviews to validate a draft persona (reversible, LOW).
- Log a decision record noting which persona is the primary campaign target (reversible, LOW).

## Human Approval Requirements
- Building and scoring personas: always allowed (analysis). [§5]
- No ad spend, publishing, or email blasts are triggered by this skill, so those approvals don't apply here.
- Persona content that includes real, named individuals' data must respect `customers` sensitivity; do not export restricted personal data into external outputs without approval. [privacy]

## Escalation Conditions
- No real customer evidence exists and the founder can't answer the deep-dive questions → escalate: recommend customer discovery before committing to a persona (low-confidence input, §7).
- The persona relies on protected-class assumptions to target → flag for founder/legal review.
- User and Decision-Maker have conflicting needs the offering can't serve both → surface to founder (positioning conflict).

## KPIs
- Completeness rate: % of target segments with a `complete` (not draft) persona.
- Downstream usage: personas actually referenced by CVP, funnel, and content skills.
- Message resonance: engagement/conversion lift after messaging is aligned to the persona's dominant pain.
- Validation: personas confirmed against real customer interviews.

## Monitoring
Watch whether campaigns aimed at the persona's stated channels and pain actually convert. If a persona's "where they get info" channels underperform, revisit the day-in-the-life quadrant. Re-validate personas as customer feedback accumulates.

## Follow-Up
Re-run when a new segment is chosen, after a batch of customer interviews, when a persona-targeted campaign underperforms, or at the quarterly marketing refresh. Draft personas should be revisited within one cycle to reach `complete`.

## Related Skills
Consumes `market-segmentation` output. Feeds `customer-value-proposition-builder`, `buyers-journey-mapper`, `marketing-funnel-planner`, and `channel-selection`. Complements `buying-center-mapper` (deal-level roles vs. segment archetype).

## Guardrails
- Distinguish evidence-based fields from assumptions; never launder an assumption into a stated fact.
- Respect customer-data sensitivity; personas are internal artifacts — real individuals' restricted data stays gated.
- Do not encode discriminatory targeting via protected characteristics; describe the market, don't unlawfully exclude.
- A `draft` persona must not silently become the basis for spend — mark and surface its gaps.

## Example
**Founder input (segment = local handmade-gift buyers from segmentation):** "They're mostly women 30–55, care about supporting local makers and giving a thoughtful gift, hate generic mass-produced stuff, find us on Instagram and at the farmers' market, want to feel like they gave something special."

**Skill reasoning:**
- Quadrant 1 (identity): "Maria," 30–55, works, gives gifts for birthdays/holidays.
- Quadrant 2 (motivations): wants a thoughtful, unique gift; hopes to be seen as a considerate giver; fears giving something generic/impersonal; trigger = an upcoming occasion; decision criteria = uniqueness, supports-local, quality.
- Quadrant 3 (pain): primary = "everything at the big store feels generic and impersonal."
- Quadrant 4 (day in life): scrolls Instagram in the evening, weekend farmers' markets, gets ideas from IG and friends; buys via IG shop or in person.
- Desired takeaway: "I gave something special and supported a real person."
- role_flag = both (she chooses and gifts). Completeness: complete, visualizable, no empty quadrants.

**Output:** one persona card "Maria — Thoughtful Local Gifter," dominant pain = generic gifting, primary channels = Instagram + farmers' market. Handed to CVP builder as the anchor.

**Executed vs. approval:** Wrote the persona to `customers.personas` and drafted the card for review (LOW, auto). Recommended 3 quick customer chats to validate the "supports local" motivation before scaling ad spend — created as a task.

## Provenance
SOURCE. Derives from the Customer Persona model (four quadrants: Identity, Motivations, Pain, Day-in-the-Life), the 7 going-deeper questions, the User/Decision-Maker tag, and the completeness/visualizability check. AI prompt scaffold is source-derived and de-branded. See `internal/PROVENANCE_MAP.md`.
