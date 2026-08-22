---
name: channel-selection
domain: marketing
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [customers, offerings, market, strategy, goals, metrics, integrations]
writes: [strategy, decisions]
related_skills: [customer-persona-builder, marketing-funnel-planner, marketing-strategy-builder, social-content-planner, keyword-and-search-map, marketing-metrics-tracker]
owned_by_agents: [marketing-agent, growth-agent]
---

# Skill: Channel Selection (Paid / Owned / Earned)

## Purpose
Tells the founder *where* to spend marketing effort: given a specific marketing goal and a target persona, it recommends a prioritized mix of paid, owned, and earned channels (the POEM model) mapped to the buyer's-journey stage the goal serves. It prevents the two most common wastes — advertising on platforms the customer never visits, and paying for reach that could be earned or owned — before any budget is committed.

## When to Use
- The founder asks "where should we market?", "which platforms should we be on?", "should we run ads?", "is [platform] worth it for us?", or "how do we reach [segment]?"
- A new offering, segment, or campaign needs a channel plan before content or spend.
- A funnel plan (`marketing-funnel-planner`) named a tool/action per stage and now needs concrete channels attached.
- Reallocating marketing effort after a performance review flagged a weak channel.

## When NOT to Use
- The persona is undefined or the goal is vague → run `customer-persona-builder` and clarify the goal first; channel choice is meaningless without knowing who and why.
- The question is "what should we say" (messaging/content) → use `social-content-planner` or `marketing-funnel-planner`.
- The question is purely "which keywords / how do we rank in search" → use `keyword-and-search-map` (this skill only names search as a channel and hands off).
- The founder wants a full dated marketing plan across all channels and stages → this skill feeds `marketing-strategy-builder`, which assembles the plan.
- Actual ad-account setup, bidding, or budget execution → out of scope; this skill recommends, the founder (or a specialist) executes.

## Required Context
Read from Business Memory before running:
- `customers.personas` — for each target persona: `where_they_are` (channels they frequent), `value_drivers`, and the underlying social-media motivation (identity / info-utility / emotional).
- `customers.segments` — whether the goal targets NEW customers (acquisition) vs. EXISTING customers (retention/referral); segment `cac`/`ltv` if known.
- `offerings` — B2C / B2B / B2G type and price point (affects channel norms).
- `market.competitors` — where competitors already have presence (parity vs. white-space).
- `strategy.growth_plan` and `goals` — the objective and target metric the channel plan must serve.
- `metrics` — historical channel performance if this is a reallocation.
- `integrations` — which ad/social/analytics platforms are already connected (feasibility of measurement).
If persona motivations or "where_they_are" are absent, that is the first gap to close.

## Inputs
```yaml
input:
  marketing_goal:          # REQUIRED. One primary objective for this plan.
    type: enum(brand_awareness, traffic_to_site, lead_generation,
               sales_conversion, retention, referral_advocacy,
               community_building, customer_service, market_research)
  target_persona_id: str   # REQUIRED. Reference to customers.personas[].id
  audience_type:           # REQUIRED. Drives paid-vs-organic default.
    type: enum(new_customers, existing_customers, mixed)
  business_type:           # REQUIRED for channel norms.
    type: enum(B2C, B2B, B2G)
  funnel_stage:            # Optional; inferred from goal if omitted.
    type: enum(awareness, interest, desire, action, retention)
  budget_available:        # Optional. Number + currency, or "none".
    type: {amount: number, currency: str} | "none"
  timeframe: str           # Optional, e.g. "next 90 days".
  existing_channels:       # Optional. Channels already in use + rough result.
    type: list[{channel: str, status: enum(working, flat, underperforming), note: str}]
  measurement_available: bool   # Optional. Is web/social analytics connected?
  constraints: str         # Optional. e.g. "no video capacity", "regulated ad category".
```

## Missing Information Protocol
1. **Persona motivation / where_they_are missing** → do NOT guess a platform. Fetch from `customers.personas`; if absent, ask the founder ONE batched question: "For [persona], where do they go for information and entertainment (which social platforms, search, print, events), and are we trying to reach *new* people or keep *existing* customers engaged?"
2. **Budget unknown** → proceed, but produce two plans: an organic-first (zero-spend) plan and a paid-augmented plan, and label which channels require budget.
3. **Measurement not connected** → still recommend channels, but flag that lead-gen/conversion goals cannot be proven without analytics, and add "connect analytics" as a prerequisite action.
4. **Never assume** the customer is on a platform just because it is popular, that paid always beats organic, or that a channel that works for competitors works for this persona. Where evidence is thin, state confidence as low and recommend a small test before scaling.

## Diagnostic Questions
- What is the ONE goal this plan serves, and which funnel stage does it sit at (awareness / interest / desire / action / retention)?
- Where do THIS persona's customers actually spend attention — and which of the three motivations (identity, info/utility, emotional) does each place serve?
- Are we acquiring NEW customers (favors paid awareness + look-alike audiences) or nurturing EXISTING ones (favors organic mid-funnel + referral)?
- For each candidate channel, does it primarily drive traffic (paid), capture/convert (owned), or amplify credibility (earned)?
- Which channels can we actually measure given connected integrations?
- Where do competitors already dominate (fight there only with a real edge) vs. where is there white space?
- Given budget and capacity constraints, what is the smallest viable channel set that can move the goal?

## Analysis Framework
Apply the POEM + Paid/Organic method in five passes:

1. **Goal → funnel stage → channel job.** Map the goal to a funnel stage, then to the marketing job for that stage (awareness = get attention/drive to site; interest = capture leads; desire = comparisons/proof; action = remove friction; retention = support/community/referral).

2. **POEM classification.** Sort every candidate channel into:
   - **Paid** — advertising whose job is to *drive traffic to owned media* (PPC/search ads, paid social, display/banner, shopping ads, affiliate; non-digital: TV, radio, print, OOH, tradeshows).
   - **Owned** — assets you control whose job is to *capture and convert* (website, landing pages, blog, social profiles, email, mobile app).
   - **Earned** — customer-created activity whose job is to *amplify credibility* (reviews, mentions, shares, reposts, word-of-mouth; non-digital: PR, networking).

3. **Paid vs. Organic split (the audience rule).**
   - NEW customers → lead with **paid** awareness using **look-alike audiences** (people resembling existing customers) to drive traffic to owned media.
   - EXISTING customers → lead with **organic** mid-funnel activity to keep them engaged and generate referrals from their networks.

4. **Persona-fit filter.** For each candidate channel, confirm the persona is actually there (`where_they_are`) and that the channel serves one of the three motivations (identity / info / emotional) — "no one is looking to shop." Drop channels that fail the fit test regardless of popularity.

5. **Feasibility & prioritization.** Score survivors on Reach-fit, Cost, Measurability, Capacity-to-produce, and Competitive-whitespace; rank into a Primary (1–2 channels), Secondary (1–2 to test), and Avoid list. Every plan must include at least one **owned** channel (the conversion destination) — paid and earned point *to* owned.

## Calculations
This skill is primarily qualitative, but uses these to prioritize and to set expectations. (Detailed KPI computation belongs to `marketing-metrics-tracker`.)
- **Channel fit score (0–5, CLAUDE-DERIVED heuristic)** = average of {Reach-fit, Inverse-cost, Measurability, Capacity, Whitespace}, each scored 0–5. Used only to rank candidates, not as a published metric.
- **Expected reach (organic, SOURCE-DERIVED)** ≈ own follower count + follower counts of accounts likely to share. Used to sanity-check whether an organic channel can plausibly hit an awareness goal.
- **Look-alike seed sufficiency (CLAUDE-DERIVED rule of thumb)** — paid look-alike audiences need a seed list of existing customers/converters large enough for the platform to model; if the seed is tiny, recommend broad-interest targeting first. Flag as low-confidence guidance, not a source formula.
- No CAC/ROAS targets are set here; those are computed and monitored by `marketing-metrics-tracker` after spend begins.

## Decision Rules
- **IF** `audience_type == new_customers` **THEN** lead the plan with a **paid awareness** channel using look-alike audiences pointing to an owned landing page. [SOURCE]
- **IF** `audience_type == existing_customers` **THEN** lead with **organic** owned+earned mid-funnel activity (email, organic social, community) and add referral prompts; do not default to paid. [SOURCE]
- **IF** the goal is `brand_awareness` or `traffic_to_site` **THEN** the plan centers on Paid + top-of-funnel Owned/Earned; the required action is "drive to website." [SOURCE]
- **IF** the goal is `lead_generation` **THEN** require an Owned lead-capture asset (landing page + form/offer) as the conversion destination; a paid or organic channel may feed it but is never the endpoint. [SOURCE]
- **IF** the goal is `sales_conversion` (action stage) **THEN** prioritize Owned channels that remove friction (frictionless checkout, retargeting email) plus a scarcity/incentive offer; de-prioritize pure awareness channels. [SOURCE]
- **IF** the goal is `retention`, `referral_advocacy`, or `community_building` **THEN** prioritize Owned (email, community) + Earned (reviews, UGC) and explicitly exclude paid acquisition as primary. [SOURCE]
- **IF** the persona's `where_they_are` does not include a candidate platform **THEN** drop that platform regardless of its general popularity ("stay where YOUR customers are"). [SOURCE]
- **IF** no channel in the plan is Owned **THEN** the plan is invalid — add the owned conversion destination before finalizing. [SOURCE, derived from POEM intent]
- **IF** `measurement_available == false` AND goal is lead_gen/conversion **THEN** add "connect web/social analytics" as a prerequisite action and mark ROI as unprovable until then. [SYNTH]
- **IF** `budget_available == none` **THEN** output the organic-first plan only and label any paid channel as "requires budget — deferred." [SYNTH]
- **IF** a competitor dominates a channel and the founder has no clear edge there **THEN** recommend a differentiated or white-space channel rather than head-to-head spend. [SOURCE, competitive-advantage intent]
- **IF** the recommendation implies **ad spend** **THEN** hold for founder approval and route the budget to CFO/runway check — never auto-launch. [POLICY]

## Procedure
1. **Load context** — pull persona, segment, offering type, competitor presence, connected integrations, and any historical channel metrics from Business Memory.
2. **Lock the goal & stage** — confirm the single primary goal; infer or confirm the funnel stage and its marketing job.
3. **Set the audience rule** — new vs. existing → paid-lead vs. organic-lead default.
4. **Enumerate candidates** — list plausible channels across Paid / Owned / Earned and digital / non-digital.
5. **POEM-classify** each candidate and note its job (drive / capture-convert / amplify).
6. **Persona-fit filter** — drop channels the persona doesn't frequent or that don't serve identity/info/emotional motivation.
7. **Score & rank** survivors on the 5 feasibility factors; guarantee at least one owned conversion destination.
8. **Assemble the plan** — Primary (1–2), Secondary/test (1–2), Avoid, each with: POEM tag, funnel job, rationale, paid/organic, budget flag, measurement note.
9. **Attach next actions** — e.g. "build landing page (owned)", "connect analytics", "prepare look-alike seed list", each tagged with its risk tier and whether it needs approval.
10. **Write back** a decision record to `decisions` and the channel plan to `strategy`; hand off to `social-content-planner` (content), `keyword-and-search-map` (if search selected), and `marketing-metrics-tracker` (to instrument the chosen channels).

## Output
```yaml
output:
  goal: str
  funnel_stage: enum(awareness, interest, desire, action, retention)
  audience_type: enum(new_customers, existing_customers, mixed)
  paid_organic_default: enum(paid_lead, organic_lead)
  recommended_channels:
    primary:
      - channel: str
        poem: enum(paid, owned, earned)
        digital: bool
        funnel_job: str            # drive / capture-convert / amplify
        paid_or_organic: enum(paid, organic)
        rationale: str
        budget_flag: enum(no_cost, requires_budget)
        measurable: bool
        fit_score: number          # 0-5, heuristic
    secondary_test: [ ... same shape ... ]
    avoid:
      - channel: str
        reason: str
  conversion_destination:          # the mandatory owned asset
    channel: str
    exists: bool
    action_if_missing: str
  prerequisites: [str]             # e.g. "connect analytics", "build landing page"
  next_actions:
    - action: str
      owner: str
      risk_tier: enum(LOW, MEDIUM, HIGH, CRITICAL)
      needs_approval: bool
  budget_note: str
  confidence: enum(low, medium, high)
  assumptions: [str]
  handoffs: [str]                  # skills to run next
```

## Recommendations
Recommendations are ranked by **expected goal impact ÷ (cost × capacity-to-produce)**, then broken by reversibility: organic/owned actions (reversible, low-risk) are recommended for immediate execution/prep; paid actions (spend, less reversible) are always presented as approval-gated options with a small-test-first framing. Ties break toward the channel with better measurability (you can prove it) and toward white-space over head-to-head with a dominant competitor. Every recommendation names the ONE action that most unblocks the goal (usually the owned conversion destination).

## Execution Opportunities
- **Draft** the channel plan document and write it to `strategy` — reversible, L1.
- **Create internal tasks** for prerequisites (build landing page, connect analytics, prepare content brief) — reversible, L2 candidate.
- **Schedule** a channel-performance review checkpoint — reversible, L2.
- **Prepare** (not launch) a paid-campaign brief with proposed audience, budget, and creative angle for founder review — L1 draft only.
- **Hand off** content and measurement tasks to sibling skills automatically — reversible, L2.

## Human Approval Requirements
Per AUTONOMY_AND_APPROVAL_MODEL.md:
- **Ad spend / launching any paid campaign** → ALWAYS founder approval (money + external commitment); also route budget to CFO/runway check. Never auto-executed regardless of level.
- **Publishing public content** on a recommended channel → founder approval (handled by the content skill).
- **Changing standing configuration** (connecting an ad account, setting auto-bidding) → founder approval.
- Producing the plan, drafts, briefs, and internal tasks requires no approval (L1/analysis).

## Escalation Conditions
- **Budget exceeds threshold or threatens runway** → founder + CFO agent.
- **Persona/where_they_are data missing or low-confidence** → surface uncertainty to founder; do not commit spend on a guess.
- **Regulated ad category** (e.g. finance, health, alcohol) or platform policy risk → Legal Liaison agent before any paid activity.
- **Competitive channel with no clear edge** and founder still wants to spend → flag risk, recommend test budget, escalate the strategic call to founder (+ Strategy agent).

## KPIs
Success of this skill's output is judged by whether the chosen channels actually moved the stated goal:
- Goal-aligned primary metric hit (e.g. awareness → reach/impressions up; lead-gen → leads/CTR; retention → repeat rate/referrals). [SOURCE metric-goal alignment]
- Share of recommended primary channels that reached "working" status within the timeframe.
- Reduction in wasted spend on dropped/avoid channels vs. prior period.
- Downstream: CAC and ROAS trend once spend begins (computed by `marketing-metrics-tracker`; CLAUDE-DERIVED).

## Monitoring
After the plan runs, watch (via `marketing-metrics-tracker`): reach/impressions and traffic-to-site for awareness channels; CTR and lead volume for lead-gen; conversion and CAC/ROAS once paid spend is live; engagement and referral counts for retention channels. Flag any primary channel that stays flat or underperforms past the test window for re-selection.

## Follow-Up
- **Event-triggered:** new persona/segment created, new offering launched, competitor makes a major channel move, or a channel is flagged underperforming in a performance review.
- **Time-triggered:** re-run at each quarterly growth-plan refresh, or 30 days into any new paid channel test to keep/kill.

## Related Skills
- `customer-persona-builder` — supplies persona motivations and `where_they_are` (prerequisite).
- `marketing-funnel-planner` — supplies the stage/message/tool/action this skill attaches channels to.
- `keyword-and-search-map` — invoked when search is a selected channel.
- `social-content-planner` — invoked to produce content for selected social channels.
- `marketing-metrics-tracker` — instruments and monitors the chosen channels.
- `marketing-strategy-builder` — consumes this channel plan into the dated, owner-assigned plan.

## Guardrails
- Never commit or "auto-launch" paid spend; ad spend is always approval-gated and runway-checked.
- Never recommend a channel purely because it is trendy or because competitors use it — the persona-fit and audience rules override popularity.
- Do not promise ROI on lead-gen/conversion goals when measurement isn't connected; state the limitation.
- Flag low-confidence recommendations explicitly and prefer a small reversible test over a large irreversible bet.
- Do not place personal customer data into ad-platform targeting beyond what the founder has approved and what privacy policy allows; look-alike seed lists must use permitted first-party data only.
- Where the plan touches regulated categories, defer to Legal before spend.

## Example
**Founder input:** "We just launched a monthly meal-prep subscription for busy young professionals. I have about $1,500/month to spend. Where should we market?"

**Skill reasoning:**
- Goal = `sales_conversion` leaning on `lead_generation` (get trials/first orders); funnel stage = interest→action. Persona "Maya, 29, urban professional" — `where_they_are`: short-form video + photo social, food/lifestyle search; motivation mix = identity (health-conscious self-image) + info-utility (quick recipes) + emotional (convenience relief). `audience_type` = new_customers → **paid-lead** default. Business_type = B2C. Measurement: web analytics connected; email tool connected.
- Candidates → POEM: paid short-form video ads + paid photo-social ads (Paid, drive); landing page + email (Owned, capture-convert); reviews/UGC food photos (Earned, amplify); organic recipe search/SEO (Owned/organic, drive later).
- Persona-fit filter: keep video + photo social (she's there, serves identity+emotional); keep search (info-utility); drop professional-network and broadcast (not where she seeks food).
- Audience rule: new customers → lead with paid look-alike video ads → owned landing page with a first-box discount (scarcity/incentive) → email nurture → solicit UGC reviews (earned).

**Output (abridged):**
- Primary: (1) Paid short-form video ads, paid, drive, look-alike audience, requires_budget, measurable, fit 4.5; (2) Landing page + first-box-discount offer, owned, capture-convert, no_cost to run (build required), measurable, fit 5.
- Secondary/test: paid photo-social ads (fit 3.5); recipe SEO content (fit 3, slow-burn organic).
- Avoid: professional network ads (persona not there for food); broadcast/print (unmeasurable, over budget).
- Conversion destination: landing page — does not yet exist → action: build before spend.
- Prerequisites: build landing page; set up conversion tracking; prepare look-alike seed from early customers.
- Next actions: [build landing page — owner: founder — LOW — no approval]; [set up tracking — LOW — no approval]; [launch $1,500/mo video ad test — HIGH — **needs approval**, route to CFO runway check].

**Executed vs. approval:** The skill drafted the plan, created the landing-page and tracking tasks, and prepared the paid-ad brief — all without approval. The actual **$1,500/month ad launch was held for founder approval** and flagged for a runway check, per policy.

## Provenance
**SOURCE.** Derived from the Marketing & Customer domain knowledge (POEM media model; Paid vs. Organic × Digital/Traditional matrix; the "stay where your customers are" and three-social-motivations rules; the look-alike / new-vs-existing audience rule; buyer's-journey→funnel→tool mapping; metric-goal alignment). The channel fit-scoring heuristic and the note that CAC/ROAS/measurement targets are set downstream are **CLAUDE-DERIVED** and flagged inline. See internal/PROVENANCE_MAP.md.
