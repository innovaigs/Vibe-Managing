---
name: keyword-and-search-map
domain: marketing
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [customers, offerings, market, strategy, metrics, integrations]
writes: [strategy, decisions]
related_skills: [website-conversion-audit, channel-selection, social-content-planner, marketing-funnel-planner, customer-persona-builder]
owned_by_agents: [marketing-agent]
---

# Skill: Keyword & Search Map

## Purpose
Builds an intent-tagged keyword map for the business and reveals where its site fails to cover the searches customers actually make. It classifies each keyword by search intent (navigational / informational / transactional), maps keywords to buyer's-journey stages, checks coverage against existing pages, and applies the EEAT quality lens so the founder knows both *which* terms to target and *what kind of content* will rank for them.

## When to Use
- The founder asks "what keywords should we target?", "how do we show up in search?", "why aren't we ranking?", "what should our blog/content be about for SEO?"
- Planning content, a blog, or new landing pages and needing a topic/keyword backbone.
- `channel-selection` selected organic search / SEO as a channel and now needs the keyword substance.
- Auditing why search brings little traffic despite the site being live.

## When NOT to Use
- The site itself can't convert the traffic it gets → run `website-conversion-audit` first; ranking for terms is wasted if the page leaks.
- The founder wants a social content calendar → use `social-content-planner` (this skill only supplies search-driven topic ideas as input).
- The question is which channels to use at all → use `channel-selection`; this skill assumes search is (or is being considered as) a channel.
- Paid-search bidding/ad-copy execution → out of scope; this skill informs the keyword substance, it does not run the ad account.
- No persona/offering defined → run `customer-persona-builder` first; intent mapping needs to know who searches and why.

## Required Context
- `customers.personas` — what the persona searches for, in their own words, at each journey stage; their `value_drivers` and pains phrased as queries.
- `offerings` — the products/services and their plain-language names, categories, and use-cases (seed terms).
- `market.competitors` — competitor names/brands (navigational terms) and the terms they appear to target.
- `strategy` / existing site — the current pages and their topics (to measure coverage).
- `metrics` / `integrations` — search analytics / keyword-research tooling if connected (search volume, current rankings, impressions/clicks from search).
- The business's EEAT assets: what the founder has genuine Experience and Expertise in, what they're known/cited for (Authority), and existing social proof (Trust) — these determine which content can credibly rank.

## Inputs
```yaml
input:
  business_terms: [str]            # REQUIRED. Seed words: products, services, categories, problems solved.
  target_persona_id: str           # REQUIRED. Whose searches we're mapping.
  business_type: enum(B2C, B2B, B2G)   # Optional; shifts journey steps (RFP for B2B/B2G).
  current_pages:                   # REQUIRED for coverage analysis (or "unknown").
    type: list[{url: str, topic: str, target_terms: [str]}]
  competitors: [str]               # Optional. For navigational + gap terms.
  geography: str                   # Optional. Local vs. national vs. international intent.
  eeat_assets:                     # Optional but recommended.
    type: {experience: [str], expertise: [str], authority_signals: [str], trust_signals: [str]}
  research_tool_connected: bool    # Optional. Is a keyword-volume/trends tool available?
```

## Missing Information Protocol
1. **No persona-phrased queries** → derive candidate queries from the persona's pains/goals, but ask the founder ONE batched question: "In your customers' own words, what do they type into search when they (a) first realize they have this problem, and (b) are ready to buy?" — capturing informational and transactional phrasing.
2. **current_pages == unknown** → still produce the keyword map, but mark coverage as "unverified" and add "inventory existing pages" as a prerequisite; coverage gaps can't be confirmed without the page list.
3. **No research tool connected** → produce the intent map and gaps from reasoning + persona language, and label volume/competitiveness as *estimated, not measured*; recommend connecting a keyword-research/trends tool to validate volume before heavy content investment.
4. **EEAT assets unknown** → still map keywords, but flag which target topics the business may lack the Experience/Expertise/Authority to rank for, and recommend either building that authority or de-prioritizing those terms.
5. **Never assume** search volume figures, never invent rankings, and never recommend targeting high-competition terms the business has no EEAT basis to win.

## Diagnostic Questions
- What does this persona type into search at each journey stage — need recognition, info search, evaluation, purchase?
- For each seed term, is the intent Navigational (find a specific site/brand/location), Informational (seeking knowledge), or Transactional (seeking to do/buy)?
- Is the keyword set balanced across intents, or all one type? (Informational dominates early stages; transactional dominates purchase.)
- Which of these terms do current pages already cover, and how many times / how well do they appear?
- Where are the coverage gaps — journey stages or intents with no matching page?
- Does the business have genuine Experience, Expertise, Authority, and Trust to create content that ranks for the target terms?
- Are there local/geographic modifiers the persona uses?
- Which terms are realistically winnable vs. dominated by large competitors?

## Analysis Framework
1. **Seed expansion.** From `business_terms` + persona language, brainstorm the full candidate keyword set (products, categories, problems, questions, comparisons, brand/competitor names, local modifiers).

2. **Intent tagging (Search Intent model).** Tag every keyword:
   - **Navigational** — looking for a specific site, brand, or location (often includes a brand/competitor name).
   - **Informational** — seeking knowledge ("how to…", "what is…", "best way to…").
   - **Transactional** — seeking to do or buy ("buy…", "book…", "near me", "pricing", "hire…").

3. **Journey mapping.** Place each keyword on the buyer's-journey stage: informational terms dominate Need-Recognition and Info-Search (top of funnel); transactional terms dominate Purchase (bottom). For B2B/B2G, add specification/RFP-style terms. Ensure every stage has at least one keyword.

4. **Coverage analysis.** For each keyword, count appearances on the homepage/key pages and identify which page (if any) targets it. Rate each keyword on **Relevance** (does it match what we actually offer?) and **Intent match** (does the ranking page satisfy the searcher's intent?).

5. **Gap identification.** Flag: (a) intents with no coverage (e.g. all transactional, no informational — nothing to attract early-stage searchers); (b) journey stages with no keyword/page; (c) high-relevance persona queries with zero page coverage.

6. **EEAT feasibility lens.** For each gap/target, assess whether the business can create content that ranks: **Experience** (firsthand experience with the topic), **Expertise** (demonstrable knowledge, tips/tricks), **Authority** (known/cited for it; backlinks), **Trustworthiness** (social proof, engagement). De-prioritize targets with no EEAT basis; prioritize where EEAT is strong and a gap exists.

## Calculations
Primarily qualitative; volume figures come from connected tools, never invented.
- **Coverage count** = number of times a keyword appears on the homepage/key pages (SOURCE worksheet metric). Low/zero for a relevant term = a gap.
- **Intent balance** = share of keywords that are informational vs. transactional vs. navigational; used to detect single-intent sets. [SOURCE rule: cover both informational and transactional.]
- **Priority score (CLAUDE-DERIVED heuristic, 0–5)** = f(Relevance, Journey-stage need, EEAT-feasibility, and — if a tool is connected — Volume and inverse Competition). Used to rank targets; flagged as a heuristic, not a source formula.
- **Search volume / keyword difficulty** — read from a connected keyword-research tool only; if none, mark as *estimated* and do not present as fact. [Volume/difficulty are tool-supplied, not source-taught numbers.]

## Decision Rules
- **IF** the keyword set is entirely one intent type **THEN** add keywords so BOTH informational and transactional intents are covered across the journey. [SOURCE]
- **IF** a journey stage has no matching keyword/page **THEN** flag a coverage gap and recommend content for that stage (informational for early, transactional for purchase). [SOURCE]
- **IF** a high-relevance persona query has zero page coverage **THEN** recommend a new/expanded page targeting it. [SOURCE]
- **IF** a target term has strong search relevance but the business lacks EEAT to rank **THEN** either recommend building that authority first or de-prioritize the term; do not chase terms you can't credibly win. [SOURCE]
- **IF** no keyword-research tool is connected **THEN** label all volume/competition estimates as unverified and recommend connecting a tool before major content spend. [SYNTH]
- **IF** `business_type` is B2B/B2G **THEN** add specification and RFP/comparison-style keywords for the extra journey steps. [SOURCE]
- **IF** the persona uses local/geographic language **THEN** add geo-modified transactional terms ("near me", city names) and map them to purchase-stage. [SOURCE intent]
- **IF** current_pages is unknown **THEN** mark coverage "unverified" and require a page inventory before confirming gaps. [SYNTH]
- **IF** a term is purely navigational for a competitor's brand **THEN** treat it as low-priority organic target (hard to rank; often better via comparison content or paid). [SOURCE/SYNTH]
- **IF** producing content for the targets would require **publishing public pages** **THEN** the content drafts are L1, but the actual publish is founder-approved. [POLICY]

## Procedure
1. **Load context** — persona queries, offerings, competitors, current pages, EEAT assets, connected tooling.
2. **Expand seeds** into the full candidate keyword set (include questions, comparisons, local modifiers, brand/competitor terms).
3. **Tag intent** for every keyword (navigational / informational / transactional).
4. **Map to journey stage**; ensure every stage is represented; add B2B/B2G steps if applicable.
5. **Pull volume/difficulty** from a connected tool if available; otherwise estimate and label.
6. **Analyze coverage** — match keywords to current pages, count appearances, rate Relevance + Intent match.
7. **Identify gaps** — missing intents, missing stages, uncovered high-relevance queries.
8. **Apply EEAT lens** — mark which targets are winnable now vs. need authority-building; drop the un-winnable low-value ones.
9. **Prioritize** with the 0–5 heuristic into Priority / Consider / Skip tiers, each with a recommended content type (page, blog/how-to, comparison, product/category page).
10. **Write back** the keyword table + gap list + content recommendations to `strategy`; log a decision record; hand off content topics to `social-content-planner`, page targets to `website-conversion-audit`, and any paid-search terms to `channel-selection`.

## Output
```yaml
output:
  persona_id: str
  keyword_table:
    - keyword: str
      intent: enum(navigational, informational, transactional)
      journey_stage: enum(need_recognition, info_search, evaluation, purchase, post_purchase)
      relevance: enum(high, medium, low)
      site_appearances: number          # coverage count; -1 if unverified
      covered_by_page: str | none
      intent_match: enum(good, weak, none)
      volume_estimate: number | "unverified"
      eeat_feasibility: enum(strong, buildable, weak)
      priority: number                  # 0-5 heuristic
      tier: enum(priority, consider, skip)
  intent_balance:
    navigational_pct: number
    informational_pct: number
    transactional_pct: number
  coverage_gaps:
    - gap: str
      type: enum(missing_intent, missing_stage, uncovered_query)
      recommended_content: str          # page / how-to blog / comparison / category page
      journey_stage: enum(...)
      eeat_note: str
  eeat_summary: str                     # where the business can credibly rank
  measured: bool                        # true if a research tool was connected
  prerequisites: [str]                  # e.g. "inventory pages", "connect keyword tool"
  handoffs: [str]
  confidence: enum(low, medium, high)
```

## Recommendations
Targets are prioritized by the 0–5 heuristic (relevance × journey-need × EEAT-feasibility, weighted by volume/competition when measured), then filtered so the final list always **covers both informational and transactional intent across the journey**. Quick wins (high relevance + strong EEAT + existing page needing only optimization) are recommended first; net-new content that requires authority-building is sequenced later. Every recommendation names the content type and the journey stage it serves, so the founder sees not just a word list but a content plan.

## Execution Opportunities
- **Draft** the keyword table, intent/journey map, and gap list; write to `strategy` — reversible, L1.
- **Draft content briefs / outlines** for priority gaps (topic, target term, intent, EEAT angle) — reversible, L1.
- **Create internal tasks** for content creation and page optimization — reversible, L2 candidate.
- **Query** a connected keyword-research/trends tool for volume/competition — read-only, L2.
- **Snapshot** current search rankings/impressions if analytics connected — reversible, L2.
- **Hand off** content topics to `social-content-planner` and page targets to `website-conversion-audit`.

## Human Approval Requirements
- **Publishing any public page or blog content** produced from these keywords → founder approval (external content).
- **Changing site structure / URLs / meta configuration** → founder approval (standing configuration).
- **Any paid-search budget** implied by transactional terms → founder approval + CFO runway check (handled via `channel-selection`).
- The keyword map, briefs, and internal tasks require no approval (L1/analysis).

## Escalation Conditions
- **Regulated-claim terms** (health, financial, legal advice keywords) → Legal Liaison before publishing content targeting them.
- **Target terms require EEAT the business genuinely lacks** and founder still wants to pursue → surface the credibility risk; recommend authority-building or a specialist writer.
- **Trademark/brand terms** of competitors for paid use → Legal Liaison (bidding on competitor brands can carry risk).
- **No reliable volume data and large content investment proposed** → flag to founder + CFO before committing budget on unverified demand.

## KPIs
- Growth in organic search traffic / impressions / clicks to the site over time (via search analytics). [SOURCE metrics]
- Number of coverage gaps closed (pages/content shipped for uncovered stages/intents).
- Rankings/appearances improvement for priority keywords (measured only if a tool is connected).
- Intent balance achieved (both informational and transactional covered across the journey).
- Downstream: search-sourced leads/conversions (via `marketing-metrics-tracker`).

## Monitoring
After content ships, watch organic impressions/clicks and rankings for priority terms; re-check coverage as pages are added; watch that new content actually satisfies searcher intent (bounce/time-on-page on the ranking pages). Re-estimate priorities if a research tool later reveals volumes differ from assumptions.

## Follow-Up
- **Event-triggered:** new offering, new persona, competitor launches a content push, a new page ships, or search analytics shows a ranking drop.
- **Time-triggered:** periodic refresh (search demand shifts seasonally); re-run when a keyword-research tool is newly connected to replace estimates with measured volume.

## Related Skills
- `customer-persona-builder` — supplies the persona's search language (prerequisite).
- `channel-selection` — decides whether search (organic/paid) is a chosen channel; consumes navigational/transactional terms for paid search.
- `website-conversion-audit` — ensures the pages targeting these keywords actually convert.
- `social-content-planner` — turns informational keyword gaps into content-calendar topics.
- `marketing-funnel-planner` — aligns keyword intent to funnel-stage messaging.
- `marketing-metrics-tracker` — measures search-sourced traffic and conversions.

## Guardrails
- Never invent search volumes or rankings; label everything unmeasured as estimated and recommend connecting a tool.
- Do not recommend chasing high-competition terms the business has no EEAT basis to rank for.
- Never publish content targeting these keywords without founder approval; regulated-claim content goes through Legal.
- Do not scrape or store personal data via search tooling; use only permitted, aggregate keyword data.
- Keep content authentic to real Experience/Expertise — recommending thin/AI-spun content that misrepresents authority is out of bounds.
- Do not bid on or target competitor trademarks without Legal review.

## Example
**Founder input:** "I run a mobile dog-grooming service in Austin. My website has one page and I get basically no traffic from Google. What keywords should I go after?" (Persona = busy pet owner; B2C; current_pages: 1 homepage targeting "Austin mobile dog grooming"; no research tool connected; EEAT: 8 years grooming experience, certified, 200+ five-star reviews.)

**Skill reasoning:**
- Seed expansion → "mobile dog grooming Austin", "dog grooming near me", "how often should I groom my dog", "how to calm a dog for grooming", "dog grooming prices Austin", "best mobile dog groomer Austin", "de-shedding treatment dog".
- Intent tags → transactional: "mobile dog grooming Austin", "dog grooming near me", "dog grooming prices Austin", "book mobile dog groomer". Informational: "how often should I groom my dog", "how to calm a dog for grooming", "de-shedding tips". Navigational: competitor brand names.
- Journey map → informational terms = need-recognition/info-search (none currently covered); transactional = purchase (partially covered by the one homepage).
- Coverage → only "Austin mobile dog grooming" is covered; site_appearances for all informational terms = 0. Intent balance = ~100% transactional, 0% informational → **single-intent gap**.
- EEAT → strong Experience/Expertise/Trust (8 yrs, certified, 200 reviews) → highly feasible to rank for how-to informational content and to strengthen the transactional page with reviews.

**Output (abridged):**
- Priority tier: optimize homepage for "mobile dog grooming Austin" + add "dog grooming near me" and pricing (transactional, purchase, EEAT strong); create how-to posts "How often should you groom your dog" and "How to calm an anxious dog for grooming" (informational, top-of-funnel gap, EEAT strong).
- Coverage gaps: missing_intent = no informational content; missing_stage = need-recognition/info-search uncovered → recommend two how-to articles feeding the transactional page.
- Prerequisites: inventory any hidden pages; connect a keyword tool to confirm local volumes (currently estimated).
- Handoffs: `social-content-planner` (the two how-to topics), `website-conversion-audit` (the grooming/pricing page).

**Executed vs. approval:** Drafted the keyword table, gap list, and two content briefs; created content tasks — no approval needed. The **actual publishing of the new pages/blog posts was held for founder approval**, and volume figures were labeled *estimated* pending a connected keyword tool.

## Provenance
**SOURCE.** Derived from the Marketing & Customer domain knowledge (Search Intent model — navigational/informational/transactional; keyword-to-journey-stage mapping; the Keyword Map worksheet with intent tagging, relevance/intent checks, and site-appearance coverage counts; the rule to cover both informational and transactional intent; the EEAT content-quality model). Search volume/difficulty numbers come from connected tools (not source-taught), and the 0–5 priority heuristic is **CLAUDE-DERIVED**; both are flagged inline. See internal/PROVENANCE_MAP.md.
