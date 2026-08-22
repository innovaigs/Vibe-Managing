---
name: marketing-funnel-planner
domain: marketing
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [customers.personas, offerings, market.differentiation, customers.segments, metrics]
writes: [strategy, decisions]
related_skills: [buyers-journey-mapper, customer-value-proposition-builder, competitive-advantage-assessment, customer-persona-builder, channel-selection]
owned_by_agents: [marketing-agent, growth-agent]
---

# Skill: Marketing Funnel Planner

## Purpose
Build the seller-side mirror of the buyer's journey: for each funnel stage, define one critical activity as a {Message, Tool, Action} triple and attach the persuasion lever that moves the buyer forward. Founder outcome: a concrete, per-stage marketing plan that pushes a persona from first awareness to repeat advocacy, with a defined action and influence tactic at every step — no more "post and pray." [SOURCE]

## When to Use
- Turning positioning into an executable plan: "How do we actually market this?", "Build our funnel," "What do we do at each stage?"
- After a persona, CVP, and buyer's-journey map exist and the founder needs the marketing response.
- A funnel leaks and the founder needs a message/tool/action defined at the leaking stage.
- Designing a campaign that must nurture from awareness through retention, not just drive one-off sales.

## When NOT to Use
- Mapping the *buyer's* behavior (their questions/stages) → use `buyers-journey-mapper` first (this skill is the seller-side response).
- Choosing which platforms to use → `channel-selection` (this skill names the tool type per stage; channel-selection picks the specific platforms).
- Producing the value statement → `customer-value-proposition-builder`.
- Computing funnel KPIs → `marketing-metrics-tracker`.

## Required Context
- `customers.personas` — the persona this funnel serves (one funnel per persona).
- The persona's buyer's-journey map (from `buyers-journey-mapper`) — the stages to respond to.
- `customer-value-proposition-builder` output — the message spine.
- `competitive-advantage-assessment` / `market.differentiation` — the Evaluation-stage comparison content.

## Inputs
```yaml
input:
  persona:
    id: string
    name: string
    primary_pain: string
    where_they_are: [string]         # real channels
  cvp_statement: string              # the message spine
  point_of_difference: string        # for the Evaluation/Desire stage
  journey_map_ref: string            # from buyers-journey-mapper
  offering:
    name: string
    price: number
  budget_available: number           # gates any paid-media recommendations
  customer_mode: enum(acquire_new, nurture_existing, both)
```

## Missing Information Protocol
1. Pull stages from the persona's journey map and the message spine from the CVP before asking anything.
2. If the point-of-difference is missing, route to `competitive-advantage-assessment`; the Desire stage needs it.
3. If budget is unknown, plan organic-first and mark any paid-media step `requires_budget: true` + founder approval.
4. Never plan a stage without a defined action — a stage with no target action is invalid.

## Diagnostic Questions
- Do I have a Message, Tool, and Action defined at EVERY stage? [SOURCE]
- Am I capturing contact info at the Interest stage (or losing leads)? [SOURCE]
- Is the purchase process frictionless, or is friction killing conversion? [SOURCE]
- Am I doing anything to retain and reactivate post-purchase? [SOURCE]
- Which stage is hardest to fill (the common failure/leak point)? [SOURCE]
- Am I acquiring new customers, nurturing existing ones, or both — and does the plan match? [SOURCE]

## Analysis Framework
The **marketing funnel** = Awareness → Interest → Desire → Action → Retention (AIDA + Retention), the seller's mirror of the 5-stage buyer's journey. For each stage define a **{Message, Tool, Action}** triple and attach an **Element of Influence** (persuasion lever). [SOURCE]

**Per-stage marketing job + tools + action:** [SOURCE]

| Funnel stage | Buyer's-journey stage | Marketing job | Typical tool | Target action |
|---|---|---|---|---|
| **Awareness** (Top) | Need Recognition | Get attention; activate triggers | Social, ads, SEO, PPC, radio, email, tradeshows | Visit website / click |
| **Interest** (Top→Mid) | Info Search | Provide info, education, testimonials; capture the lead | Website / custom landing page | Collect email / contact info |
| **Desire** (Middle) | Evaluation | Show comparisons, value, competitive advantage, demos | Social, email, phone, trials/samples | Show why you beat competitors |
| **Action** (Bottom) | Purchase | Remove friction; incentivize buying now | Frictionless checkout, email, phone, coupon | Complete the purchase |
| **Retention** | Post-Purchase | Support, community, advocacy | Social, email | Get customers to refer / review |

**Elements of Influence per stage** (six persuasion levers — Reciprocity, Consistency, Social Proof, Authority, Liking, Scarcity — applied where each works best): [SOURCE]
- **Awareness →** Authority (awards, credentials) + Reciprocity (free guide).
- **Interest →** Social Proof (reviews/ratings) + Reciprocity (buying guide).
- **Desire →** Reciprocity (comparison guide) + Social Proof (best-of reviews).
- **Action →** Liking (helpful staff/rapport) + Scarcity (limited bonus/offer).
- **Retention →** Social Proof + Consistency (rewards program, repeat-purchase badges).

**Acquire vs. nurture:** IF acquiring NEW customers → paid/sponsored awareness using look-alike audiences (people resembling existing customers). IF nurturing EXISTING → organic mid-funnel activity to keep them engaged and generate referrals. [SOURCE]

## Calculations
No formula for building the plan. Health of the resulting funnel is measured by `marketing-metrics-tracker`: conversion rate per stage = # advancing ÷ # entering [CLAUDE]; and the source engagement metrics (CTR = clicks ÷ impressions; engagement rate = engagements ÷ impressions). [SOURCE / CLAUDE]

## Decision Rules
- IF any stage lacks a Message, Tool, OR Action THEN the plan is incomplete — fill it before execution. [SOURCE]
- IF at Awareness THEN use attention/trigger content (ads, social, SEO, PPC) to drive to the website; attach Authority + Reciprocity. [SOURCE]
- IF at Interest THEN deploy a lead-capture asset on a landing page (e.g. a downloadable guide) to collect contact info; attach Social Proof + Reciprocity. [SOURCE]
- IF at Desire THEN lead with comparisons, competitive advantage, demos/trials, and social proof; attach Reciprocity + Social Proof. [SOURCE]
- IF at Action THEN remove friction and add an incentive (coupon, free delivery, bonus item); attach Liking + Scarcity. [SOURCE]
- IF Post-Purchase THEN shift to retention: support, community, care content, loyalty/rewards, referral prompts; attach Social Proof + Consistency. [SOURCE]
- IF customer_mode is acquire_new THEN weight paid awareness with look-alike audiences; IF nurture_existing THEN weight organic mid-funnel + referrals. [SOURCE]
- IF budget is zero/unknown THEN plan organic-first and mark paid steps as requiring budget + approval. [SOURCE intent]
- IF no lead capture exists at Interest THEN flag it as the top fix — uncaptured Interest traffic is lost demand. [SOURCE]

## Procedure
1. Load the persona, its journey map, the CVP (message spine), and the point-of-difference.
2. Confirm customer_mode (acquire / nurture / both) and available budget.
3. For each of the five funnel stages, write the {Message, Tool, Action} triple, using the persona's real channels for Tool.
4. Attach the recommended Element(s) of Influence to each stage.
5. Ensure Interest has a lead-capture asset and Action is frictionless with an incentive.
6. Mark any paid-media step as budget/approval-gated.
7. Identify the priority stage (usually the mapped leak) to build first.
8. Write the funnel plan to `strategy`; hand specifics to `channel-selection` and content skills; hand KPIs to `marketing-metrics-tracker`.

## Output
```yaml
output:
  funnel_plan:
    persona_id: string
    customer_mode: enum(acquire_new, nurture_existing, both)
    stages:
      - stage: enum(Awareness, Interest, Desire, Action, Retention)
        message: string               # what to say (rooted in the CVP)
        tool: string                  # channel/asset type (persona's real channels)
        action: string                # the target action
        influence_levers: [enum(Reciprocity, Consistency, Social_Proof, Authority, Liking, Scarcity)]
        paid: bool                    # true if it needs ad spend
        requires_approval: bool       # true for ad spend / public publishing / email blast
    lead_capture_defined: bool
    priority_stage: string            # build-first stage (usually the leak)
    look_alike_audience_recommended: bool
  provenance: {source: agent_analysis, as_of: date, confidence: 0.0-1.0}
```

## Recommendations
Build the priority (leak) stage first for fastest ROI. Insist on a lead-capture asset at Interest — it's the most common leak. Keep each stage to ONE critical activity rather than many diffuse ones. Prefer organic tactics when budget is tight; reserve paid for awareness with look-alike audiences. Always name which steps need founder approval (ad spend, public publishing, email blasts) so nothing ships unapproved. [SOURCE]

## Execution Opportunities
- Write the funnel plan to `strategy` and create tasks per stage (reversible, LOW, auto). [L1]
- Draft the content assets named in each triple (e.g. the lead-magnet guide) as drafts for review (reversible, LOW).
- Set up internal analytics/reminders to measure each stage (reversible, LOW).
- **Launch paid awareness campaigns / publish public content / send an email blast — held for approval (see below).**

## Human Approval Requirements
Per the platform approval model, these funnel actions require **founder approval before execution** and are named explicitly here: [§4; task approval model]
- **Ad spend** — launching any paid awareness/retargeting campaign or committing budget.
- **Publishing public content** — posting to public social profiles, publishing a landing page or blog.
- **Email blasts** — sending marketing email to a list.
Analysis, planning, drafting assets, and internal task creation are always allowed without approval. [§5]

## Escalation Conditions
- A planned paid campaign's budget would strain runway → route to CFO Agent for a runway check before requesting founder approval. [§7 financial threshold]
- Content makes a claim that touches a regulated area → Legal Liaison before publishing.
- The point-of-difference (Desire stage) is missing/weak → back to `competitive-advantage-assessment`.
- Low-confidence persona/journey inputs → surface uncertainty; don't commit spend.

## KPIs
- Completeness: every stage has message + tool + action + lever.
- Lead capture: contact-capture rate at Interest.
- Stage conversion: advance rate per stage (via `marketing-metrics-tracker`).
- Retention/advocacy: referral and repeat-purchase rate at Retention.
- Efficiency: CAC and ROAS on paid awareness (once running). [CLAUDE for CAC/ROAS]

## Monitoring
Track stage-to-stage conversion and CTR/engagement per stage. If the plan's priority (leak) stage doesn't improve after launch, revise the message or lever there. Watch that lead capture actually collects contacts and that the Action stage stays frictionless.

## Follow-Up
Re-run when the persona, CVP, or journey changes; when metrics reveal a new leak; when budget/mode shifts (acquire↔nurture); or at the quarterly refresh. Retention tactics should be revisited as the customer base grows.

## Related Skills
Consumes `buyers-journey-mapper`, `customer-value-proposition-builder`, `competitive-advantage-assessment`, and `customer-persona-builder`. Feeds `channel-selection` (specific platforms), content/copy skills (asset production), and `marketing-metrics-tracker` (per-stage KPIs). Escalates budget to the CFO Agent.

## Guardrails
- No stage ships without a defined action.
- Ad spend, public publishing, and email blasts are held for founder approval — never auto-executed by this skill.
- Respect the persona's real channels; don't plan on platforms the audience doesn't use.
- Any external claim must trace to a substantiated CVP benefit.

## Example
**Founder input:** persona "Maria — Thoughtful Local Gifter"; CVP = the Ember & Oak strong CVP; point-of-difference = made-to-order custom scents + personalized notes; channels = Instagram + farmers' market; budget ≈ $1,500/mo; mode = both.

**Skill reasoning — {Message, Tool, Action} + lever per stage:**
- **Awareness:** message = "Give a gift they can't get anywhere else — hand-poured, made-to-order candles." Tool = Instagram (paid, look-alike audience) + local SEO. Action = click to profile. Levers = Authority (handmade craft) + Reciprocity (free "Thoughtful Gifting Guide"). paid=true, requires_approval=true.
- **Interest:** message = "Download our free gift guide." Tool = simple landing page with email capture. Action = collect email in exchange for the guide. Levers = Social Proof (reviews) + Reciprocity (the guide). lead_capture_defined=true.
- **Desire:** message = "Why made-to-order beats a big-box candle" comparison + behind-the-scenes pour videos. Tool = Instagram + email. Action = show the difference. Levers = Reciprocity (comparison guide) + Social Proof.
- **Action:** message = "Order now — free personalized note + 10% off your first candle this week." Tool = frictionless IG checkout + market card reader. Action = complete purchase. Levers = Liking (personal service) + Scarcity (this-week offer). paid=false.
- **Retention:** message = "How to care for your candle" + "refer a friend, both get a treat." Tool = email + Instagram. Action = referral/review. Levers = Social Proof + Consistency (a simple rewards punch-card).

priority_stage = Interest (the mapped leak — no capture today). look_alike_audience_recommended = true.

**Executed vs. approval:** Skill wrote the plan, drafted the gift-guide lead magnet and the landing-page copy, and created per-stage tasks (LOW, auto). The Instagram paid awareness set (ad spend), publishing the public landing page, and the first email blast to the captured list are each held for founder approval; runway impact of the $1.5k/mo spend routed to the CFO Agent first.

## Provenance
SOURCE. Derives from the Marketing Funnel model (Awareness→Interest→Desire→Action→Retention as the seller-side mirror of the buyer's journey), the {Message, Tool, Action} planning triple, the Elements of Influence per-stage mapping (six persuasion levers, adapted from Cialdini), and the acquire-new-vs-nurture-existing / look-alike-audience rules. CAC/ROAS/conversion-rate references are CLAUDE-flagged. See `internal/PROVENANCE_MAP.md`.
