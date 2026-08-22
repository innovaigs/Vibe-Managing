---
name: buyers-journey-mapper
domain: marketing
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [customers.personas, customers.segments, offerings, market, customers.accounts]
writes: [customers.personas, strategy, decisions]
related_skills: [customer-persona-builder, buying-center-mapper, marketing-funnel-planner, customer-value-proposition-builder, channel-selection]
owned_by_agents: [marketing-agent, growth-agent]
---

# Skill: Buyer's Journey Mapper

## Purpose
Map the multi-stage process a persona goes through to make a purchase — from first realizing they have a need to becoming a repeat advocate — and define the marketing job, tool, and action at each stage. Founder outcome: a stage-by-stage picture of how customers actually decide, so marketing meets them with the right message at the right moment instead of pushing "buy now" at people who don't yet know they have a problem. [SOURCE]

## When to Use
- Designing go-to-market for a persona: "How do people actually decide to buy this?", "What should we say at each step?"
- A funnel leaks and the founder needs to see where in the journey buyers drop off.
- Selling into B2B/B2G where the process is formal (specs, RFPs) and needs the extra stages mapped.
- Before building a marketing funnel plan — the journey is the buyer-side input to the seller-side funnel.

## When NOT to Use
- You need the *seller-side* activities (message/tool/action + persuasion lever) as an executable plan → use `marketing-funnel-planner` (this skill maps the buyer's behavior; the funnel planner builds the response).
- Identifying who decides one specific deal → `buying-center-mapper`.
- No persona exists yet → run `customer-persona-builder` first.
- Choosing channels → `channel-selection`.

## Required Context
- `customers.personas` — the persona whose journey is being mapped (each persona can have a distinct journey).
- `offerings` — price, complexity, and consideration level (a $10 impulse buy has a near-collapsed journey; a $50k system has a long one).
- Business type (B2C vs. B2B/B2G) — determines whether the extra Specification and RFP stages apply.
- `customers.accounts` — real evidence of how customers found and bought (reviews, sales notes) to ground the map.

## Inputs
```yaml
input:
  persona:
    id: string
    name: string
    primary_pain: string
    where_they_get_info: [string]
    decision_criteria: [string]
  offering:
    name: string
    price: number
    consideration_level: enum(impulse, considered, complex)
  business_type: enum(B2C, B2B, B2G)
  evidence:                      # optional real data on how customers currently buy
    triggers_observed: [string]
    info_sources_observed: [string]
    purchase_mechanism: string
```

## Missing Information Protocol
1. Ground each stage in real evidence (reviews, sales notes, analytics) where available before inferring from the persona.
2. If the purchase mechanism or triggers are unknown, infer from the persona's day-in-life and decision criteria, and label inferred fields `assumption:`.
3. If business_type is unclear, ask ONE question; default B2B/B2G to the 6-stage (with Specification + RFP) map when price/complexity is high.
4. Never assume the customer is at the purchase stage — most demand lives in the earlier stages.

## Diagnostic Questions
For the persona, answer "what do your customers do?" at each stage: [SOURCE]
- **Need Recognition:** What triggers awareness of the need? ("Do I have a need?")
- **Info Search:** Where do they get information — friends, website, search, social? ("Where do I get information?")
- **Evaluation:** How do they compare the options? ("How do I compare?")
- **Purchase:** How do they buy? ("How do I buy?")
- **Post-Purchase:** How do they feel and act after buying? ("How do I feel now?")
- (B2B/B2G) How is the product spec determined, and is there a formal RFP?

## Analysis Framework
The **5-stage buyer's journey** — the customer's (largely subconscious) point of view — each stage carrying its buyer question, funnel position, marketing job, typical tools, and target action: [SOURCE]

| # | Stage | Buyer's question / behavior | Funnel stage (position) | Marketing job | Typical tools | Action / goal |
|---|---|---|---|---|---|---|
| 1 | **Need Recognition / Trigger** | "Do I have a need?" — what triggers awareness? | Awareness (Top) | Get attention; activate triggers | Social media, advertising, SEO, PPC, radio, email, tradeshows | Push customer to visit website / click |
| 2 | **Info Search** | "Where do I get information?" (friends, web, search, social) | Interest (Top→Mid) | Provide information, tools, education, testimonials | Website / custom landing page, visits, calls/inquiries | Collect email / contact info (lead capture) |
| 3 | **Evaluation of Alternatives** | "How do I compare the options?" | Desire (Middle) | Show comparisons, value, competitive advantage, demos | Social, email, phone, trials/samples | Highlight why you beat competitors |
| 4 | **Purchase** | "How do I buy?" | Action (Bottom) | Remove friction; give an incentive to buy now | Frictionless checkout, email, phone, coupon/offer | Complete the purchase |
| 5 | **Post-Purchase** | "How do I feel / act after buying?" | Retention | Build community & support; drive advocacy | Social media, email | Get customers to tell others (referrals, reviews) |

**B2C vs. B2B/B2G variation:** [SOURCE]
- **B2C:** Need Recognition → Info Search → Evaluation → Purchase → Post-Purchase.
- **B2B/B2G adds two steps:** after Need Recognition insert **"Determine Product Specification,"** and formalize evaluation as **"Requests for Proposals (RFP)."** Full path: Need Recognition → Determine Product Specification → Info Search → Evaluation + RFPs → Purchase → Post-Purchase.

## Calculations
None taught for this mapping stage. (Stage-to-stage conversion rates are computed by `marketing-metrics-tracker`; conversion rate per stage = # advancing ÷ # entering — CLAUDE.) [SOURCE / CLAUDE]

## Decision Rules
- IF business_type is B2B/B2G THEN expand the journey to include the Product Specification and RFP steps, and map the buying center per stage (esp. gatekeeper + procurement approver). [SOURCE]
- IF consideration_level is impulse THEN collapse Info Search and Evaluation — the journey compresses toward Need Recognition → Purchase; don't over-engineer mid-funnel education. [SOURCE intent]
- IF consideration_level is complex/high-price THEN lengthen the map, add trials/demos at Evaluation, and expect multiple stakeholders (hand to `buying-center-mapper`). [SOURCE]
- IF the persona's info sources are known THEN populate the Info Search and Awareness tools with those exact channels, not generic ones. [SOURCE]
- IF two personas buy differently THEN map a separate journey for each — do not reuse one journey across distinct buyers. [SOURCE]
- IF there is no defined action at any stage THEN the map is incomplete — every stage needs a target action. [SOURCE]

## Procedure
1. Load the persona (pain, info sources, decision criteria) and the offering's consideration level.
2. Select the 5-stage (B2C) or 6-stage (B2B/B2G) template.
3. For each stage, fill: buyer's question, buyer behavior (grounded in evidence where possible), marketing job, tools (using the persona's real channels), and the target action.
4. Note the trigger(s) at Need Recognition and the purchase mechanism at Purchase.
5. Add B2B/B2G Specification + RFP detail if applicable.
6. Identify the likely leak point (the stage hardest to move buyers through).
7. Write the journey map to the persona record; hand to `marketing-funnel-planner` to build the seller-side response.

## Output
```yaml
output:
  journey:
    persona_id: string
    business_type: enum(B2C, B2B, B2G)
    stages:
      - name: string                 # Need Recognition | Determine Spec | Info Search | Evaluation/RFP | Purchase | Post-Purchase
        buyer_question: string
        buyer_behavior: string       # what the customer actually does here
        funnel_position: enum(Awareness, Interest, Desire, Action, Retention)
        marketing_job: string
        tools: [string]              # the persona's real channels
        target_action: string
        evidence_level: enum(observed, inferred)
    trigger_events: [string]
    purchase_mechanism: string
    likely_leak_stage: string
  provenance: {source: agent_analysis, as_of: date, confidence: 0.0-1.0}
```

## Recommendations
Weight attention toward the earliest stages (most buyers are pre-purchase) and toward the identified leak stage. Recommend the single highest-leverage fix (e.g. "add a lead-capture asset at Info Search — you're losing contacts"). For B2B/B2G, recommend mapping the buying center so each stage targets the right role. Prefer the persona's real channels over generic ones. [SOURCE]

## Execution Opportunities
- Write the journey map to the persona/strategy in memory (reversible, LOW). [L1 draft]
- Draft the visual journey map document for founder review (reversible, LOW).
- Create tasks to instrument each stage (e.g. add analytics to detect the leak) (reversible, LOW).
- Log a decision record noting the identified leak stage and chosen fix (reversible, LOW).

## Human Approval Requirements
- Mapping and analysis: always allowed. [§5]
- This skill produces a map, not live campaigns — it triggers no ad spend, publishing, or email blasts. The downstream `marketing-funnel-planner` and channel/content skills carry those approvals: ad spend, publishing public content, and email blasts require founder approval.

## Escalation Conditions
- No evidence of how customers actually buy and the founder can't describe it → recommend customer discovery before committing a funnel budget (low confidence, §7).
- B2B/B2G RFP/procurement rules may exceed the company's capability → flag to Legal Liaison / founder.
- The journey reveals the offering can't be bought easily (broken purchase mechanism) → flag to Operations.

## KPIs
- Coverage: every stage has a defined action and channel.
- Leak identification: whether the mapped leak stage matches where analytics show real drop-off.
- Downstream lift: conversion improvement after the funnel plan addresses the leak stage.
- Accuracy: share of stages marked `observed` vs. `inferred`.

## Monitoring
Instrument stage-to-stage conversion (via `marketing-metrics-tracker`). If the real leak differs from the mapped one, revise. Watch Info Search → lead capture especially, since lost leads there are invisible without instrumentation.

## Follow-Up
Re-map when the persona changes, when a new offering with a different consideration level launches, when analytics reveal a new leak, or at the quarterly refresh. B2B/B2G maps update when procurement/RFP processes change.

## Related Skills
Consumes `customer-persona-builder` (and `buying-center-mapper` for B2B/B2G). Directly feeds `marketing-funnel-planner` (seller-side response per stage), `channel-selection`, and `customer-value-proposition-builder` (the Evaluation-stage differentiation).

## Guardrails
- Distinguish observed behavior from inferred; don't present inferences as fact.
- Don't force every offering into a 5-stage map — impulse buys compress, complex buys expand.
- Respect customer-data sensitivity when using account evidence.
- An incomplete map (missing actions) must not be handed downstream as final.

## Example
**Founder input:** "Handmade candles, ~$28 each, sold to the 'Maria — Thoughtful Local Gifter' persona. She finds us on Instagram and the farmers' market."

**Skill reasoning (B2C, considered-impulse):**
1. Need Recognition — trigger: upcoming birthday/holiday. Behavior: starts thinking about a gift. Tools: Instagram ads, farmers'-market presence, SEO for "unique local gift." Action: click to profile / visit stall.
2. Info Search — behavior: browses IG feed, reads captions, checks reviews. Tools: Instagram profile + a simple site/landing page. Action: capture email (offer a "gift guide" in exchange). ← **likely leak stage** (no lead capture today).
3. Evaluation — behavior: compares to big-box generic gifts. Tools: IG posts showing story/handmade process, reviews. Action: show why handmade-local beats generic.
4. Purchase — behavior: buys via IG shop or at the stall. Tools: frictionless IG checkout, market card reader, a small "first-order 10% off." Action: complete purchase.
5. Post-Purchase — behavior: gives the gift, feels good. Tools: email + IG. Action: prompt a review / referral / repeat for the next occasion.

**Output:** 5-stage map, leak = Info Search (no email capture), recommended fix = a gift-guide lead magnet on the profile/landing page.

**Executed vs. approval:** Wrote the journey to the persona, drafted the map, and created a task to add a lead-capture gift guide (LOW, auto). Building and spending on the actual funnel is handed to `marketing-funnel-planner` where ad spend needs founder approval.

## Provenance
SOURCE. Derives from the Buyer's Journey model (5 stages with per-stage buyer question, funnel position, marketing job, tools, and action) and the B2B/B2G variation (added Product Specification + RFP steps). Per-stage conversion-rate note is CLAUDE-flagged. See `internal/PROVENANCE_MAP.md`.
