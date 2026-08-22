---
name: social-content-planner
domain: marketing
version: 0.1.0
autonomy_ceiling: L2
provenance: SOURCE
reads: [customers, offerings, strategy, goals, metrics, integrations]
writes: [strategy, metrics, decisions]
related_skills: [channel-selection, keyword-and-search-map, marketing-funnel-planner, marketing-metrics-tracker, customer-persona-builder, marketing-strategy-builder]
owned_by_agents: [marketing-agent]
---

# Skill: Social Content Planner

## Purpose
Produces a weekly social-media content calendar that honors the 80/20 value/promotion rule and the 3:1 non-promotional-to-promotional ratio, and analyzes recent post performance to decide what to reuse and what to drop. It keeps the founder posting content people actually want — serving identity, information, or emotion — instead of a stream of ads that the algorithm and the audience both punish.

## When to Use
- The founder asks "plan our posts", "what should we post this week/month?", "build a content calendar", "which of our posts are working?"
- After `channel-selection` picks social channels and content substance is needed.
- Recurring cadence: weekly calendar generation and post-performance review (this is an ongoing, L2 operating skill).
- After `keyword-and-search-map` surfaces informational topics that should become social content.

## When NOT to Use
- No social channel has been chosen or the persona isn't defined → run `channel-selection` / `customer-persona-builder` first.
- The founder wants paid social *ads* strategy/budget → that's `channel-selection` (paid) + approval; this skill plans organic/owned content (it may schedule internal-review drafts, not launch paid).
- The output needed is a full multi-channel dated marketing plan with owners → `marketing-strategy-builder`.
- Deep KPI computation and alerting across the funnel → `marketing-metrics-tracker` (this skill does lightweight post-level performance analysis and hands the numbers over).
- Writing long-form web/blog/SEO pages → `keyword-and-search-map` topics + web content, not the social calendar.

## Required Context
- `customers.personas` — the persona's motivations (identity / info-utility / emotional) and `where_they_are` (which platforms), so content serves a real reason people use social.
- `offerings` — what may be promoted in the ≤20% promotional slots.
- `strategy` / `channel-selection` output — which social channels are in play and each channel's goal.
- `goals` — the social goal(s) driving metric choice (community, lead-gen, awareness, engagement).
- `metrics` / `integrations` — connected social accounts + analytics for pulling post performance; a social scheduler (by function) for scheduling drafts.
- Calendar context — upcoming holidays, events, seasonal themes relevant to the audience.

## Inputs
```yaml
input:
  channels: [str]                  # REQUIRED. Social channels to plan for.
  target_persona_id: str           # REQUIRED. Whose motivations content must serve.
  social_goal:                     # REQUIRED. Sets which metric matters.
    type: enum(brand_awareness, engagement, community_building,
               lead_generation, sales_conversion, customer_service, market_research)
  cadence:                         # REQUIRED. Posts per week per channel.
    type: {posts_per_week: number, channels_map: {channel: posts_per_week}}
  content_capacity:                # Optional. What the founder can actually produce.
    type: {video: bool, image: bool, blog: bool, live: bool, ugc_available: bool}
  recent_posts:                    # Optional. For performance analysis (reuse/drop).
    type: list[{date: date, time: str, channel: str, caption: str, content_type: str,
                media_type: str, likes: number, comments: number, shares: number,
                clicks: number, impressions: number, reach: number}]
  promotions:                      # Optional. Offers to weave into the ≤20% promo slots.
    type: list[{offer: str, window: str}]
  calendar_events: [str]           # Optional. Holidays/events/themes to anchor content.
  approval_mode:                   # Optional. Default draft_for_review.
    type: enum(draft_for_review, schedule_internal_review)
```

## Missing Information Protocol
1. **Persona motivation missing** → do not fill the calendar with generic promo. Ask ONE batched question: "For [persona], what do they come to [channel] for — to express who they are (identity), to learn/keep up (info), or to feel something (humor/warmth) — and what are they NOT there for?" Content must serve one of the three motivations.
2. **No recent_posts for analysis** → produce the forward calendar and note that performance-based reuse/drop guidance is unavailable until a week of post metrics exists; recommend enabling analytics.
3. **Content_capacity unknown** → assume mixed image/text, prefer video where feasible (Pro Tip #1), and flag that curation + UGC solicitation can fill gaps if original-content bandwidth is low.
4. **No scheduler connected** → deliver the calendar as drafts for manual posting; do not claim it was scheduled.
5. **Never assume** the audience wants promotional content, never exceed the 20% promo ceiling to "hit a number," and never publish or schedule public posts without the required approval.

## Diagnostic Questions
- What is the social goal, and therefore which metric should this week's content move (engagement / reach / referrals / conversions)?
- Which of the three motivations (identity / info / emotional) does each planned post serve? ("No one is looking to shop.")
- Are we within the 80/20 rule (≤20% promotional) and the 3:1 ratio (3 non-promo : 1 promo)?
- What content types (6 buckets) and media types fit the persona and our capacity — and can we lead with video?
- What holidays/events/themes should anchor timing this week?
- From last week's posts: which content types/times drew the most engagement (reuse), and which underperformed (drop)?
- Are we mixing original content, curation, and UGC to stay sustainable?
- Is anything set to publish that would need founder approval before it goes public?

## Analysis Framework
**Part A — Performance analysis (reuse/drop), if recent_posts provided:**
1. Classify each recent post into one of the 6 content buckets (Entertainment, Inspirational, Educational, Connection, Conversation, Promotional) and its media type.
2. Compute per-post engagement (below) and rank; identify highest-engagement content types, media types, and posting times.
3. Assess the promo/non-promo balance vs. 80/20.
4. Output: **reuse** (what worked — content types/times/formats to repeat), **drop** (what underperformed), and any **balance correction** needed.

**Part B — Forward weekly calendar:**
1. **Motivation fit** — every slot serves identity, info, or emotion.
2. **Content bucket mix** — draw from the 6 buckets; enforce ≤20% promotional (80/20) and 3 non-promo : 1 promo (3:1).
3. **Media selection** — choose media type per slot (image, video, video story, live, infographic, ebook/white paper, blog link, external link); prefer video where possible; use curation + UGC to fill capacity gaps.
4. **Timing** — build a 7-day grid (day × AM/PM) anchored to holidays/events/themes and to the best-performing times found in Part A.
5. **Goal-metric alignment** — attach the metric each post is meant to move, tied to the social goal.
6. **Algorithm optimization** — favor native content that stays on-platform, frequency, and features (video/live/stories) that reach rewards.
7. **Measure → adapt → repeat** — every calendar closes the loop: it is generated *from* last cycle's performance and instruments this cycle for the next review.

## Calculations
[SOURCE-DERIVED unless noted]
- **Post Engagement Rate** = total engagements ÷ total impressions. (engagements = likes + comments + shares + clicks, per available fields.)
- **Click-Through Rate (CTR)** = clicks ÷ impressions.
- **Reach** ≈ own follower count + follower counts of accounts that shared the post (potential unique viewers).
- **Impressions** = times the post appeared in feeds/timelines (may exceed reach).
- **80/20 rule** = promotional posts ≤ 20% of all posts; ≥80% entertainment/inspiration/connection/conversation/education.
- **3:1 ratio** = 3 units of non-promotional content per 1 promotional offer.
- **Promo compliance check (derived)** = promotional_posts ÷ total_posts ≤ 0.20 AND non_promo:promo ≥ 3:1 for the planning window.
- **Best-time / best-type detection (CLAUDE-DERIVED heuristic)** = rank recent posts by engagement rate; the top quartile's content types, media, and posting times seed the next calendar. Flagged as a heuristic.

## Decision Rules
- **IF** promotional posts would exceed 20% of the window **THEN** replace the excess with non-promotional content (education/entertainment/connection) until 80/20 holds — "people do not want to be sold to on social media." [SOURCE]
- **IF** the non-promo:promo ratio falls below 3:1 **THEN** add non-promotional posts before scheduling. [SOURCE]
- **IF** a planned post serves none of identity/info/emotional **THEN** rework or drop it — it will not earn attention. [SOURCE]
- **IF** video is feasible for a slot **THEN** prefer video over a static image (Pro Tip #1). [SOURCE]
- **IF** original-content bandwidth is low **THEN** curate relevant external content and solicit UGC (reviews, customer photos/videos) to fill the calendar. [SOURCE]
- **IF** the goal is community-building **THEN** weight Connection/Conversation buckets and track engagement; **IF** lead-generation **THEN** include lead-capture posts and track referrals/conversions; **IF** awareness **THEN** weight reach/impressions and native shareable content. [SOURCE metric-goal alignment]
- **IF** optimizing for algorithm reach **THEN** favor posting frequency, native on-platform content (avoid outbound links in-feed where they suppress reach), and special features (live, video stories). [SOURCE]
- **IF** a recent content type/time is in the top engagement quartile **THEN** reuse it next cycle; **IF** bottom performers **THEN** drop or rework. [SOURCE audit intent]
- **IF** `approval_mode == schedule_internal_review` **THEN** the skill MAY schedule drafts into an internal-review queue at L2 (reversible, not public). [POLICY]
- **IF** any post is destined to **publish publicly** **THEN** hold for founder approval before it goes live — L2 does not cover public publishing. [POLICY]
- **IF** a promo references a price/offer/claim **THEN** verify it against `offerings` and route external-commitment claims for approval. [POLICY]

## Procedure
1. **Load context** — persona motivations, chosen channels, social goal, capacity, promotions, calendar events, connected analytics/scheduler.
2. **Run Part A** (if recent_posts present) — classify, compute engagement/CTR, rank, assess 80/20 balance → reuse/drop/balance-correction.
3. **Set the mix target** — number of posts per channel; allocate across the 6 buckets within 80/20 and 3:1.
4. **Fill slots** — for each day/AM-PM, assign content bucket + specific idea + media type + the motivation it serves + the metric it targets; seed with Part A's winners and anchor to events.
5. **Prefer video / add curation + UGC** to complete the grid within capacity.
6. **Validate ratios** — confirm ≤20% promo and ≥3:1 before finalizing; auto-rebalance if not.
7. **Draft captions** for each slot (or briefs if bandwidth-limited).
8. **Route by approval_mode** — draft_for_review (default) OR schedule into internal-review queue (L2); never auto-publish public posts.
9. **Instrument** — tag each post so `marketing-metrics-tracker` can capture its performance for next cycle.
10. **Write back** — calendar to `strategy`, performance snapshot to `metrics`, decision record noting reuse/drop choices; hand off to `marketing-metrics-tracker` and (weak USP/topics) to sibling skills.

## Output
```yaml
output:
  planning_window: str             # e.g. "week of 2026-09-01"
  social_goal: str
  channels: [str]
  performance_analysis:            # present if recent_posts provided
    reuse: [{content_type: str, media_type: str, best_time: str, why: str}]
    drop:  [{content_type: str, reason: str}]
    balance_correction: str
    top_metrics: {avg_engagement_rate: number, avg_ctr: number}
  weekly_calendar:
    - day: enum(Mon,Tue,Wed,Thu,Fri,Sat,Sun)
      slot: enum(AM, PM)
      channel: str
      content_bucket: enum(entertainment, inspirational, educational,
                           connection, conversation, promotional)
      media_type: enum(image, video, video_story, live, infographic,
                       ebook_whitepaper, blog_link, external_link)
      motivation_served: enum(identity, info_utility, emotional)
      idea: str
      caption_or_brief: str
      target_metric: str
      source: enum(original, curated, ugc)
  ratio_check:
    promo_pct: number              # must be <= 20
    non_promo_to_promo: str        # must be >= "3:1"
    compliant: bool
  approval_mode: enum(draft_for_review, schedule_internal_review)
  posts_needing_public_approval: [str]
  handoffs: [str]
  confidence: enum(low, medium, high)
```

## Recommendations
Calendar slots are prioritized by **goal-fit × expected engagement**, seeded from the prior cycle's top-quartile performers, and constrained hard by the 80/20 and 3:1 ratios (compliance is non-negotiable, not a preference). Sustainable-production wins: where original-content capacity is thin, the skill recommends curation and UGC over skipping the cadence. Reuse/drop guidance is ranked by measured engagement rate, and the single highest-leverage change (best time, best content type) is called out so the founder knows what to double down on.

## Execution Opportunities
- **Draft** the weekly calendar and captions; write to `strategy` — reversible, L1.
- **Schedule drafts into an internal-review queue** (not public) via a connected scheduler — reversible, **L2** (this skill's ceiling).
- **Pull post performance** from connected social analytics — read-only, L2.
- **Snapshot** engagement metrics to `metrics` for trend tracking — reversible, L2.
- **Create tasks** for content production (film video, gather UGC, design infographic) — reversible, L2.
- **Solicit UGC** by drafting (not sending) outreach/request copy — L1 draft.

## Human Approval Requirements
- **Publishing any post to a public social channel** → ALWAYS founder approval (external-facing content). L2 covers scheduling to an *internal-review* queue only, never public publishing.
- **Promotional posts making price/offer/claims** → founder approval and verification against `offerings`.
- **Any paid boost/ad spend** on a post → founder approval + CFO runway check (via `channel-selection`).
- **Connecting/authorizing a social account or scheduler** → founder approval (standing configuration).
- Drafting the calendar, captions, performance analysis, and internal-review scheduling require no public-publish approval.

## Escalation Conditions
- **Sensitive/timely context** (posting during a public tragedy, controversy, or crisis) → pause auto-scheduling, escalate to founder for a judgment call.
- **Regulated claims** in promotional content (health/financial/comparative) → Legal Liaison before publish.
- **Brand-voice or reputational risk** in a draft → founder review; do not publish.
- **Sudden engagement collapse** detected in Part A → flag to founder + `marketing-metrics-tracker` for diagnosis before continuing the same content.

## KPIs
- **Post Engagement Rate** and **CTR** trend across the cycle (primary quality signals). [SOURCE]
- Reach/impressions growth for awareness goals; referrals/social conversions for lead-gen/conversion goals. [SOURCE]
- 80/20 and 3:1 compliance rate (process KPI — should be 100%).
- Cycle-over-cycle improvement from reuse/drop decisions (did doubling down on winners raise average engagement?).
- Cadence adherence (planned vs. actually posted).

## Monitoring
After posts go live, watch engagement rate, reach/impressions, CTR, and social referrals/conversions via `marketing-metrics-tracker`; feed the results into next cycle's Part A. Watch for algorithm-reach drops (flat impressions despite steady posting) and for any post drawing negative sentiment. Confirm promotional posts didn't crowd out value content over the month, not just the week.

## Follow-Up
- **Time-triggered:** weekly — generate the next calendar and run the reuse/drop review (this is the core operating loop).
- **Event-triggered:** new promotion/launch, a holiday/seasonal moment, a channel added by `channel-selection`, or an engagement anomaly flagged by monitoring.

## Related Skills
- `channel-selection` — chooses which social channels this skill plans for.
- `customer-persona-builder` — supplies motivations content must serve.
- `keyword-and-search-map` — feeds informational topics into the calendar.
- `marketing-funnel-planner` — aligns post intent to funnel stage/message.
- `marketing-metrics-tracker` — captures post performance and closes the measure→adapt→repeat loop.
- `marketing-strategy-builder` — folds the content plan into the overall dated marketing plan.

## Guardrails
- 80/20 and 3:1 are hard constraints — never break them to push more promotion.
- Never publish or boost public content without founder approval; L2 autonomy stops at internal-review scheduling.
- Never post content that serves no genuine audience motivation, misrepresents an offer, or makes unverified claims.
- Do not fabricate or misattribute UGC; use only content the creator permitted.
- Pause scheduling around sensitive real-world events; defer to founder judgment.
- Do not present unmeasured guesses as performance facts; if analytics is absent, say the reuse/drop guidance is unavailable.

## Example
**Founder input:** "Plan next week's posts for my mobile dog-grooming Instagram. Goal is engagement + a few bookings. Here's last week's 6 posts with stats." (Persona = busy pet owner, motivations identity+emotional+info; capacity: video yes, UGC yes; one promo: "$15 off first groom, this month".)

**Part A (reuse/drop):** Classifies last week — a before/after grooming video (Educational/Entertainment) had the highest engagement rate (9.2%) at Sat AM; two "book now" promo posts had 1.1% (Promotional) and made promo = 33% of posts (violates 80/20). Reuse: before/after videos, Sat AM timing, customer-dog features. Drop: repetitive "book now" text posts. Balance correction: cut promo from 33%→≤20%.

**Part B (calendar, 7 posts):** Mon AM Educational video "3 signs your dog is overdue for a groom" (info); Tue PM Connection "Meet Bella, today's fluffiest client" UGC photo (identity/emotional); Wed AM Entertainment reel "grooming bloopers" (emotional, video); Thu PM Conversation "Poll: how often do you bathe your dog?" (info/identity); Fri AM Inspirational before/after transformation video (emotional, reuse winner); Sat AM Educational "how to brush between grooms" video (info, best-time slot); Sun PM **Promotional** "$15 off your first groom this month — book link in bio" (the single promo).
- ratio_check: promo_pct = 14% (1/7) ✓; non_promo:promo = 6:1 ✓; compliant = true.
- Prefer-video applied to 4 of 7 slots; 2 UGC posts fill capacity.

**Executed vs. approval:** Drafted the full calendar + captions, pulled last week's stats, snapshotted engagement to `metrics`, and (approval_mode = schedule_internal_review) **scheduled all 7 as drafts into the internal-review queue** at L2. The **public publishing of each post — and specifically the promotional post's "$15 off" claim — was held for founder approval** before going live.

## Provenance
**SOURCE.** Derived from the Marketing & Customer domain knowledge (Three Pillars of Social Media Strategy; three reasons people use social — identity/info/emotional; the 6 content buckets and media types; the 80/20 rule and 3:1 calendar ratio; prefer-video and curation/UGC pro tips; algorithm-reach factors; metric-goal alignment; the Social Content Planner + Weekly Calendar and Social Post Performance Audit worksheets; engagement rate / CTR / reach / impressions formulas). Best-time/best-type detection is a **CLAUDE-DERIVED** heuristic, flagged inline. See internal/PROVENANCE_MAP.md.
