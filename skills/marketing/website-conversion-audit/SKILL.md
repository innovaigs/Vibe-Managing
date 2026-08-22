---
name: website-conversion-audit
domain: marketing
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [customers, offerings, strategy, goals, metrics, integrations]
writes: [strategy, decisions, metrics]
related_skills: [channel-selection, keyword-and-search-map, marketing-funnel-planner, customer-value-proposition-builder, marketing-metrics-tracker]
owned_by_agents: [marketing-agent]
---

# Skill: Website Conversion Audit (4 C's)

## Purpose
Diagnoses why a website (usually the homepage or a key landing page) fails to turn visitors into customers, by scoring it against the four principles of conversion-centered design — Clarity, Attention, Congruence, Credibility — and returning a red/yellow/green scorecard plus a prioritized, specific fix list. It stops the founder from paying to send traffic to a page that leaks it.

## When to Use
- The founder asks "why don't visitors convert?", "why is my bounce rate high?", "can you review my website / landing page?", "is my homepage any good?"
- Before spending on any channel that drives traffic to the site (paid ads, SEO) — the destination must be conversion-ready first.
- After a redesign or new landing page launch, to validate it before scaling traffic.
- When `channel-selection` names an owned page as the conversion destination and flags that it needs to be built or checked.

## When NOT to Use
- There is no defined conversion goal for the page → first define primary + secondary conversions (this skill will ask; it cannot score congruence without a goal).
- The problem is "not enough traffic," not "traffic doesn't convert" → use `channel-selection` / `keyword-and-search-map` to drive traffic; this skill assumes traffic exists or is coming.
- The founder wants keyword/SEO coverage analysis → use `keyword-and-search-map`.
- The founder wants the value proposition itself written → use `customer-value-proposition-builder`; this skill only checks whether the USP is *clearly expressed* on the page.
- Deep technical performance/accessibility engineering (page speed internals, WCAG remediation code) → note the finding and hand to the appropriate specialist/tool; this skill flags them, it doesn't fix code.

## Required Context
- `customers.personas` — who the page is for, their `value_drivers`, and what they came to accomplish.
- `offerings.cvp_id` / `customer-value-proposition-builder` output — the intended USP, to check the page expresses it.
- `strategy` / `channel-selection` output — the page's role and the traffic it will receive.
- `goals` — the business objective the conversion serves.
- `metrics` / `integrations` — current conversion rate, bounce, traffic sources if web analytics is connected (turns a qualitative audit into a measured one).
- Site type must be known or inferred: retail/eCommerce, service/lead-gen, media, or social/blog — it sets the expected primary/secondary conversions.

## Inputs
```yaml
input:
  page_url: str                    # REQUIRED. The page to audit.
  page_content: str | rendered     # REQUIRED. Text + structure of the page (or a capture).
  site_type:                       # REQUIRED (or inferred).
    type: enum(retail_ecommerce, service_leadgen, media, social_blog)
  target_persona_id: str           # REQUIRED. Who this page serves.
  primary_conversion:              # REQUIRED. The one action the page must drive.
    type: str                      # e.g. "purchase", "book a call", "request a quote"
  secondary_conversions: [str]     # Optional. e.g. create account, email signup, download
  intended_usp: str                # Optional. The value proposition it should express.
  current_metrics:                 # Optional, if analytics connected.
    type: {conversion_rate: number, bounce_rate: number, avg_time_on_page: number,
           top_traffic_source: str}
  device_scope:                    # Optional.
    type: enum(desktop, mobile, both)
```

## Missing Information Protocol
1. **No defined conversion goal** → ask the founder ONE batched question: "What is the single most important action a visitor should take on this page, and what secondary actions would still be a win?" Do not audit without it — Congruence and Clarity are scored against the goal.
2. **Site type unknown** → infer from content and confirm; use it to load the expected conversion set (Retail → primary: Purchase; secondary: create account, email signup, premium upgrade. Service → primary: Contract/booking; secondary: request info, get a quote, download content).
3. **No analytics connected** → run a qualitative audit and clearly label scores as heuristic; add "connect web analytics to confirm" as a fix, and recommend re-audit once real conversion data exists.
4. **Intended USP missing** → still score Clarity/Credibility, but flag "USP not verifiable" and hand off to `customer-value-proposition-builder` if the page has no discernible differentiator.
5. **Never assume** the page converts because it "looks nice," never assume mobile is fine because desktop is, and never invent metric values — if analytics is absent, say so.

## Diagnostic Questions
- What type of site/page is this, and what should the visitor accomplish here?
- What is the primary conversion goal, and what are the secondary conversions?
- On a 5-second scan, is it clear what the page is, who it's for, and what to do next? (Clarity)
- Is there ONE obvious primary action, or is attention split across many competing elements? (Attention)
- Does every headline, image, and word push toward the conversion, or do some pull away? (Congruence)
- Are there ample, specific reasons to believe you'll deliver — proof, social proof, guarantees? (Credibility)
- Is the unique selling proposition clear and above the fold?
- Is there information overload? Is the info ordered by importance? Do clickable elements stand out?
- Does the experience hold up on mobile as well as desktop?

## Analysis Framework
Score the page on the **4 C's of Conversion-Centered Design**, each rated **Red / Yellow / Green**, plus two supporting 1–5 ratings.

1. **Clarity** — Can a first-time visitor tell, within a quick scan, what this is, who it's for, and what to do? Essential information present and ordered by importance; no jargon wall.
2. **Attention** — Is focus directed to the one key action? Count distractors competing with the primary CTA; fewer is better. The primary CTA should be visually dominant and unmistakable.
3. **Congruence** — Do all elements (headline, subhead, imagery, copy, CTA label) reinforce the single conversion? Flag anything that dilutes or contradicts the goal (off-message links, competing offers, generic stock imagery).
4. **Credibility** — Are there ample, specific reasons to believe? Social proof (reviews, ratings, logos, testimonials), authority signals (credentials, awards, guarantees), and evidence the business delivers.

Supporting ratings (1–5):
- **Information Overload** (1 = overwhelming, 5 = clean) — is the page trying to do too much on one screen?
- **USP Clarity** (1 = absent, 5 = crystal clear and prominent) — is the differentiator obvious and above the fold?

Design rules applied to generate fixes (SOURCE): don't do too much on one page; make the USP clear; order information by importance; split dense content into multiple pages; make clickable elements stand out; keep text short; prefer one dominant action per page.

## Calculations
Mostly qualitative scoring; supported by these where analytics exists.
- **Website Conversion Rate** = conversions ÷ site visitors. [CLAUDE-DERIVED — the source teaches the 4 C's qualitatively; the numeric conversion-rate benchmark is Claude-supplied.] Benchmark against site type rather than a universal number.
- **Bounce rate** and **avg time on page** — read from analytics if present; used to corroborate a Red Clarity/Attention score (high bounce + low time ⇒ confirms leak).
- **C-score roll-up (CLAUDE-DERIVED heuristic)** — map Green=2, Yellow=1, Red=0 across the 4 C's for an at-a-glance 0–8 readiness score; used only to prioritize, not published as an official metric.
- **Expected lift framing (CLAUDE-DERIVED, directional)** — when recommending a fix, estimate impact qualitatively (high/medium/low) rather than promising a specific % lift, unless A/B data exists.

## Decision Rules
- **IF** any of the 4 C's scores **Red** **THEN** record a specific fix to bring it to Green and mark the page "not traffic-ready" until fixed — do not scale paid traffic to it. [SOURCE]
- **IF** any C scores **Yellow** **THEN** record a fix but allow traffic to proceed with the fix scheduled. [SOURCE]
- **IF** all 4 C's are **Green** **THEN** the page is traffic-ready; recommend measurement + iterative A/B testing rather than a rebuild. [SOURCE]
- **IF** Attention shows more than one co-equal primary CTA **THEN** flag competing calls-to-action; recommend demoting all but one primary action. [SOURCE]
- **IF** Information Overload ≤ 2 **THEN** recommend splitting content across multiple pages and cutting text. [SOURCE design rules]
- **IF** USP Clarity ≤ 2 **THEN** flag missing/weak differentiator and hand off to `customer-value-proposition-builder`. [SOURCE]
- **IF** Congruence is Red because off-message links pull attention **THEN** recommend removing or relocating them below the fold / to secondary pages. [SOURCE]
- **IF** Credibility is Red **THEN** recommend adding specific social proof (reviews/ratings/testimonials/logos) and any authority signals available. [SOURCE, ties to influence levers]
- **IF** `site_type == retail_ecommerce` **THEN** expect Purchase as primary; secondary = create account, email signup, premium upgrade. **IF** `site_type == service_leadgen` **THEN** expect Contract/booking as primary; secondary = request info, quote, content download. [SOURCE]
- **IF** no analytics connected **THEN** label all scores heuristic and add "connect analytics + set up conversion tracking" as a prerequisite fix. [SYNTH]
- **IF** `device_scope != mobile` and traffic is largely mobile **THEN** require a mobile pass before sign-off. [SYNTH]
- **IF** a fix requires publishing/replacing live public content **THEN** hold the actual publish for founder approval; the audit and fix drafts do not. [POLICY]

## Procedure
1. **Confirm goal & type** — lock primary + secondary conversions and site type; load the expected conversion set.
2. **Load persona & USP** — know who the page serves and the differentiator it should express.
3. **Pull metrics** — if analytics connected, read conversion rate, bounce, time-on-page, top source to corroborate findings.
4. **5-second scan test** — assess Clarity first as a first-time visitor would.
5. **Score each C** Red/Yellow/Green with a one-line evidence note per score.
6. **Rate** Information Overload and USP Clarity (1–5).
7. **Mobile pass** if in scope.
8. **Generate fixes** — for every Yellow/Red, a specific, actionable fix mapped to the design rules; tag each fix with impact (H/M/L), effort, and whether it needs approval to publish.
9. **Prioritize** — Reds first (blocking), then Yellows by impact/effort; produce a traffic-readiness verdict.
10. **Write back** — save the scorecard + fix list to `strategy`, log a decision record, and (if analytics present) snapshot the baseline conversion metric to `metrics`. Hand off to `customer-value-proposition-builder` (weak USP), `keyword-and-search-map` (search-landing pages), and `marketing-metrics-tracker` (to track post-fix conversion).

## Output
```yaml
output:
  page_url: str
  site_type: enum(retail_ecommerce, service_leadgen, media, social_blog)
  primary_conversion: str
  secondary_conversions: [str]
  scorecard:
    clarity:     {rating: enum(red, yellow, green), evidence: str}
    attention:   {rating: enum(red, yellow, green), evidence: str}
    congruence:  {rating: enum(red, yellow, green), evidence: str}
    credibility: {rating: enum(red, yellow, green), evidence: str}
  information_overload: number     # 1-5
  usp_clarity: number              # 1-5
  c_score: number                  # 0-8 roll-up, heuristic
  traffic_ready: bool
  measured: bool                   # true if backed by analytics
  baseline_metrics:                # present only if measured
    type: {conversion_rate: number, bounce_rate: number, avg_time_on_page: number}
  fix_list:
    - fix: str
      addresses: enum(clarity, attention, congruence, credibility, overload, usp, mobile, tracking)
      severity: enum(blocking, high, medium, low)
      impact: enum(high, medium, low)
      effort: enum(low, medium, high)
      needs_publish_approval: bool
  verdict: str                     # plain-language summary + go/no-go on traffic
  handoffs: [str]
  confidence: enum(low, medium, high)
```

## Recommendations
Fixes are prioritized **blocking-first** (any Red that makes the page not traffic-ready), then by **impact ÷ effort**. Reversible edits that don't touch live content (copy drafts, layout mockups, adding staged social proof) are recommended for immediate preparation; anything that publishes to the live public site is presented as an approval-gated action. The single highest-leverage fix is called out explicitly, and the founder is told the one thing to fix before spending on traffic.

## Execution Opportunities
- **Draft** the scorecard and fix list; write to `strategy` — reversible, L1.
- **Draft revised copy / CTA labels / page structure** as proposals (not published) — reversible, L1.
- **Create internal tasks** for each fix with owner and effort — reversible, L2 candidate.
- **Set up / request** conversion tracking in connected analytics — configuration change, approval-gated.
- **Snapshot** the baseline conversion metric to `metrics` for before/after comparison — reversible, L2.
- **Schedule** a re-audit / A/B test after fixes ship — reversible, L2.

## Human Approval Requirements
- **Publishing or replacing any live public page content** → ALWAYS founder approval (external-facing, brand-critical).
- **Changing analytics/tracking configuration or standing site settings** → founder approval.
- **Adding testimonials/reviews/logos** → founder approval AND verify permission/authenticity (never fabricate social proof).
- The audit itself, drafts, mockups, and internal tasks require no approval (L1/analysis).

## Escalation Conditions
- **Legal/regulatory claims on the page** (health, financial, guarantees, comparative claims) → Legal Liaison agent before publishing changes.
- **Accessibility or serious technical performance defects** beyond copy/layout → flag to an engineering/design specialist.
- **No USP exists at all** (not just unclear) → escalate to `customer-value-proposition-builder` + founder; a conversion audit can't fix an absent value proposition.
- **Fixes require budget** (redesign, developer time) → founder + CFO for cost.

## KPIs
- Post-fix **website conversion rate** improvement vs. baseline (the core measure; CLAUDE-DERIVED benchmark by site type). [primary]
- Reduction in bounce rate / increase in time-on-page for the audited page.
- Number of Red items closed to Green; % of fix list shipped.
- Whether the page passed all 4 C's before paid traffic was scaled (leak prevented).

## Monitoring
After fixes ship, watch conversion rate, bounce, and time-on-page for the page (via `marketing-metrics-tracker`); compare against the baseline snapshot. If a fix didn't move the metric, re-open the corresponding C for a deeper look or an A/B test. Watch mobile vs. desktop conversion separately.

## Follow-Up
- **Event-triggered:** any redesign, new landing page, new campaign pointing traffic at the page, or a drop in conversion flagged by monitoring.
- **Time-triggered:** re-audit each time `channel-selection` designates the page as a paid-traffic destination, and on a periodic cadence for high-traffic pages.

## Related Skills
- `channel-selection` — designates the owned page as a conversion destination and triggers this audit before spend.
- `customer-value-proposition-builder` — supplies/repairs the USP the page must express.
- `keyword-and-search-map` — for search-landing pages, ensures the page also matches search intent.
- `marketing-funnel-planner` — the page is the "tool" for the Interest/Action funnel stage.
- `marketing-metrics-tracker` — measures conversion before and after fixes.

## Guardrails
- Never publish changes to a live public page without founder approval.
- Never fabricate or add unverifiable social proof, reviews, testimonials, or credentials — credibility fixes must use real, permitted evidence.
- Do not promise a specific conversion-rate lift; give directional impact unless A/B data supports a number.
- When analytics is absent, clearly mark scores as heuristic; do not present unmeasured judgments as measured facts.
- Do not overwrite the page's existing content in memory; store fixes as proposals.
- Flag regulated or legal claims for review before they ship.

## Example
**Founder input:** "Here's my homepage. I'm about to run ads to it but almost no one books a call. Can you check it?" (Service/lead-gen; persona = small-clinic office manager; primary conversion = "book a discovery call"; analytics connected: conversion 0.6%, bounce 74%.)

**Skill reasoning:**
- 5-second scan → the headline is a generic slogan ("Excellence in Healthcare Solutions"); unclear what's offered or for whom → **Clarity: Red**.
- Three co-equal buttons ("Book a Call", "Read our Blog", "See Pricing") plus a newsletter popup → attention split → **Attention: Red** (>1 primary CTA + distractor popup).
- Hero image is generic stock; body copy talks about the company's history, not the visitor's problem → some elements pull away from booking → **Congruence: Yellow**.
- No reviews, no client logos, no guarantee; one vague "trusted by many" line → **Credibility: Red**.
- Information Overload = 2 (dense history section); USP Clarity = 1 (no differentiator visible). Bounce 74% + conversion 0.6% corroborate the Clarity/Attention Reds.
- Verdict: NOT traffic-ready — 3 Reds. c_score = 1/8.

**Output (abridged):**
- Fixes (prioritized): (1) *blocking, high impact/low effort* — rewrite headline to name the offer + audience + outcome ("Fewer no-shows for small clinics — book a 15-min call"); addresses Clarity/USP. (2) *blocking, high/low* — make "Book a Call" the single dominant CTA; remove the newsletter popup and demote blog/pricing to the nav; addresses Attention. (3) *blocking, high/medium* — add 3 real client testimonials + logos + a satisfaction guarantee; addresses Credibility (needs_publish_approval + verify authenticity). (4) *high, low* — replace stock hero with a product/outcome visual; cut the history section (Congruence, Overload). (5) *medium* — confirm mobile layout.
- Handoffs: `customer-value-proposition-builder` (USP=1), `marketing-metrics-tracker` (track post-fix conversion).

**Executed vs. approval:** Drafted the scorecard, rewritten headline/CTA copy, and internal fix tasks with no approval. Snapshotted the 0.6% baseline. The **live publish of the new copy and the testimonials was held for founder approval** (external content + must verify testimonial authenticity), and the founder was advised **not to launch ads until the three Reds are Green**.

## Provenance
**SOURCE.** Derived from the Marketing & Customer domain knowledge (Conversion-Centered Design "4 C's" — Clarity/Attention/Congruence/Credibility; Red/Yellow/Green scoring; Information-Overload and USP-clarity ratings; site-type→conversion-goal reference; homepage design rules; the "fix red/yellow before spending on traffic" rule). The numeric website-conversion-rate benchmark, the 0–8 c-score roll-up, and directional-lift framing are **CLAUDE-DERIVED** and flagged inline. See internal/PROVENANCE_MAP.md.
