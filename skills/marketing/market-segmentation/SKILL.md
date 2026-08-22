---
name: market-segmentation
domain: marketing
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [customers.segments, customers.accounts, customers.concentration, offerings, market, finance.income_statement, metrics]
writes: [customers.segments, decisions]
related_skills: [customer-persona-builder, competitive-advantage-assessment, customer-value-proposition-builder, buyers-journey-mapper, marketing-funnel-planner]
owned_by_agents: [marketing-agent, growth-agent]
---

# Skill: Market Segmentation

## Purpose
Divide the company's total addressable market into distinct sub-groups of similar buyers, then pick which segment(s) to serve — so every downstream marketing dollar, persona, message, and channel is aimed at a chosen target instead of "everyone." Founder outcome: a short, ranked list of target segments with a defensible reason for each. [SOURCE]

## When to Use
- The founder is trying to figure out who to target: "Who should we go after?", "We're marketing to everyone and it's not working," "Who's actually our best customer?"
- Launching a new offering, entering a new geography, or a channel underperforms because the audience is too broad.
- Revenue is concentrated and the founder wants to know which customer types to double down on vs. drop.
- Before building personas, a CVP, a funnel, or a channel plan — segmentation is the input to all of them.

## When NOT to Use
- The founder wants a deep profile of a single already-chosen segment → use `customer-persona-builder`.
- The question is who signs off on one specific deal → use `buying-center-mapper`.
- The question is competitive positioning within a segment → use `competitive-advantage-assessment`.
- Sizing the whole market (TAM/SAM/SOM) or deciding whether the market is worth entering → that is a strategy/market-assessment task, not segmentation.

## Required Context
- `offerings` — what the company sells, its use-case(s), price, and margin.
- `customers.accounts` and `customers.concentration` — who buys today and revenue mix by customer type (`finance.income_statement` if account-level data is thin).
- `market` — known competitors and trends, to sanity-check reachability.
- Company `stage` and rough marketing resources/budget (from `finance.position`) — a segment is only "Actionable" relative to what the business can afford to do. [SOURCE]

## Inputs
```yaml
input:
  offering:
    name: string                 # product/service being segmented for
    use_case: string             # primary use / application of the offering
    price_point: number          # typical price
    business_type: enum(B2C, B2B, B2G, mixed)
  current_customers:
    - type: string               # rough label for a group buying today
      revenue_share_pct: number  # % of revenue this group represents
      notes: string
  candidate_variables:           # optional; skill proposes these if omitted
    demographic: [string]        # B2C: age, income, gender, education... | B2B/B2G: company size, revenue, industry, stage, channel
    geographic: [string]         # zip, urban/suburban/rural, domestic/intl, radius
    behavioral: [string]         # frequency of use, seasonality, use-case, operational traits
    psychographic: [string]      # attitudes, values, life stage, personality, beliefs
  resources:
    marketing_budget: number     # available spend (drives Actionable/Accessible scoring)
    reach_channels: [string]     # channels the company can realistically operate
  constraints: string            # geography, regulation, capacity limits
```

## Missing Information Protocol
1. If revenue mix by customer type is missing, attempt to compute it from `customers.accounts` / `finance.income_statement` (revenue from a type ÷ total revenue). [SOURCE intent]
2. If candidate segmentation variables are missing, propose a default set across all four variable families from the offering + use-case. Do not invent customer data.
3. If reachability/budget is unknown, ask the founder ONE batched question covering: current best customers, marketing budget, and channels they can operate.
4. Never assume a segment's size or profitability — if unknown, mark it `size_estimate: unknown` and score `Worthwhile` as `unverified`, not a guess.

## Diagnostic Questions
- Who is the customer today, and why do they choose this company? [SOURCE]
- What is the primary use / use-case of the offering? [SOURCE]
- What key variables split this market into distinct sub-groups — demographic, geographic, behavioral, psychographic? [SOURCE]
- Which segments can we realistically serve (Actionable / Accessible)? Are they distinguishable (Measurable)? Which is most Worthwhile? Can any be sub-divided further? [SOURCE]
- What % of revenue does each customer type represent today? [SOURCE]
- Consumer, business, or government? If business — which industry, and what business stage? [SOURCE]

## Analysis Framework
Two-step model: **segment, then evaluate.** [SOURCE]

**Step 1 — Segment.** Divide the market using variables from the four families where members are alike on the variables that matter to buying:
- **Demographic** — B2C: race, ethnicity, language, ability, gender, age, income, education, marital status, religion, military status. B2B/B2G: company size, revenue, industry, business phase/stage, channel.
- **Geographic** — zip code, urban/suburban/rural, domestic/international, radius from location.
- **Behavioral** — operational characteristics, seasonal purchase, frequency of use, application/use-case.
- **Psychographic / lifestyle** — attitudes, personality traits, beliefs, life stage, values.

**Step 2 — Evaluate each candidate segment on MAAW.** [SOURCE]
- **Measurable** — Can you make clear distinctions between segments? (Are members identifiable and countable?)
- **Accessible** — Can the business realistically reach and serve this segment (channels, geography, distribution)?
- **Actionable** — Can the business realistically impact this segment given its resources (budget, capacity)?
- **Worthwhile** — Is the segment large enough / profitable enough to matter?

Score each MAAW criterion High / Medium / Low (or 1–3). A segment must clear a minimum bar on all four to be a primary target. Where two segments buy differently, they are different segments and get separate downstream treatment. [SOURCE]

## Calculations
- **Revenue mix by customer type** = revenue from a customer type ÷ total revenue. Used to rank existing segments by current contribution. [SOURCE]
- **MAAW score** = sum of the four criteria (each 1=Low, 2=Medium, 3=High); max 12. Used only to rank *within* the set of segments that individually pass every criterion (no single Low). [SOURCE model, CLAUDE scoring convention]
- **Concentration risk flag** = TRUE if one target segment would represent >50% of revenue (`customers.concentration.top_customer_pct_revenue`). Surface as a risk, not a blocker. [CLAUDE]

## Decision Rules
- IF a segment scores Low on ANY of Measurable / Accessible / Actionable / Worthwhile THEN do not target it as a primary segment; either re-segment more precisely or deprioritize. [SOURCE]
- IF two candidate groups buy with clearly different behavior (e.g. low-volume/infrequent vs. bulk/frequent) THEN split them into separate segments — each later gets its own persona, CVP, and funnel; never market to them the same way. [SOURCE]
- IF a segment is large but the company cannot reach or afford it (Accessible/Actionable Low) THEN shelve it as a "future" segment and note the capability gap that would unlock it. [SOURCE]
- IF a single target segment would exceed ~50% of revenue THEN flag concentration risk and recommend a secondary segment for diversification. [CLAUDE]
- IF candidate segments overlap heavily on the variables that matter THEN merge them — over-segmenting fragments spend. [SOURCE]
- IF business_type is B2B/B2G THEN prefer firmographic variables (company size, revenue, industry, business stage, channel) over consumer demographics. [SOURCE]

## Procedure
1. Load offering, use-case, current customers, revenue mix, and resource constraints from memory + inputs.
2. Confirm business_type (B2C / B2B / B2G / mixed) — it selects the demographic vs. firmographic variable set.
3. Generate candidate segments by combining the most relevant variables across the four families (propose if founder didn't supply them).
4. For each candidate, estimate size/profit potential (use revenue mix for existing groups; mark unknown for new ones).
5. Score every candidate on MAAW (High/Medium/Low per criterion).
6. Drop any segment with a Low on any criterion; rank the survivors by total MAAW score, breaking ties with Worthwhile then current revenue share.
7. Recommend 1–3 primary target segment(s) + optionally 1 "future" segment with its unlock condition.
8. Note concentration risk and any segment that should be sub-divided further.
9. Write ranked segments to `customers.segments`; hand the top segment(s) to `customer-persona-builder`.

## Output
```yaml
output:
  segments:
    - id: string
      name: string
      definition: string                 # the variables that define this segment
      business_type: enum(B2C, B2B, B2G)
      variables_used: [string]
      size_estimate: string | number | unknown
      current_revenue_share_pct: number | null
      maaw:
        measurable: enum(High, Medium, Low)
        accessible: enum(High, Medium, Low)
        actionable: enum(High, Medium, Low)
        worthwhile: enum(High, Medium, Low) | unverified
        score: number                    # 4–12
      verdict: enum(primary_target, secondary_target, future, deprioritize)
      rationale: string
  recommended_targets: [string]          # ordered segment ids
  future_segments: [ {id, unlock_condition} ]
  concentration_risk: {flag: bool, note: string}
  provenance: {source: agent_analysis, as_of: date, confidence: 0.0-1.0}
```

## Recommendations
Rank primary targets by MAAW score, then Worthwhile, then reachability given current budget. Prefer segments the company can serve now (high Actionable/Accessible) over larger segments it cannot yet reach — reachability beats raw size for an early-stage business. Always name at least one reason to NOT pursue each deprioritized segment so the founder sees the trade-off. Cap primary targets at 3 to keep spend focused. [SOURCE]

## Execution Opportunities
- Write/refresh `customers.segments` in Business Memory (reversible, LOW). [L1 draft → L2 once trusted]
- Create an internal task to build a persona for each chosen target segment (reversible, LOW).
- Draft a one-page segmentation summary for the founder (reversible, LOW).
- Log a decision record capturing which segments were chosen and why (reversible, LOW).

## Human Approval Requirements
- Analysis, scoring, and recommendations: always allowed (no approval). [AUTONOMY_AND_APPROVAL_MODEL §5]
- Changing the company's *official* target segment(s) in memory — since it redirects marketing spend and strategy — is presented for founder confirmation before it becomes the standing target. [SOURCE emphasis; §4 "changing standing configuration"]
- This skill triggers no ad spend, publishing, or email blasts, so none of the named spend/publish/blast approvals apply directly here; downstream skills carry them.

## Escalation Conditions
- Revenue-mix or account data is missing/low-confidence and materially changes the ranking → surface uncertainty to the founder; do not finalize targets. [§7 data conflict]
- A "Worthwhile" judgment depends on market-size data the company doesn't have → recommend a market-sizing step (strategy) before committing budget.
- Concentration risk is severe (one segment dominates) → flag to Risk Agent / founder.

## KPIs
- Adoption: chosen segments actually used by persona/CVP/funnel skills downstream.
- Fit: revenue growth and CAC within targeted segments vs. untargeted spend.
- Precision: reduction in wasted spend on non-target audiences after retargeting.
- Stability: how often targets get re-picked (churn in targets signals weak segmentation).

## Monitoring
After targets are set, watch revenue share, CAC, and conversion by segment (via `marketing-metrics-tracker`). If a target segment underperforms on reachability or profitability for two review cycles, re-run this skill.

## Follow-Up
Re-run: quarterly (with the growth-plan refresh), when a new offering launches, when entering a new geography, when revenue concentration shifts materially, or when a channel consistently underperforms against a target segment. [SOURCE cadence intent]

## Related Skills
Feeds `customer-persona-builder` (one persona per target), `competitive-advantage-assessment`, `customer-value-proposition-builder`, `buyers-journey-mapper`, `marketing-funnel-planner`, and `channel-selection`. Consumes competitor/trend context from `competitive-intelligence-analysis`.

## Guardrails
- Do not fabricate segment sizes or profitability; mark unknowns explicitly and score them `unverified`.
- Do not use protected demographic variables (race, religion, ability, military status) as *targeting exclusion* criteria — they may describe a market but must not be used to unlawfully exclude; flag any use that risks discrimination for founder/legal review. [privacy/compliance guardrail]
- Segmentation redirects real spend — treat a change to standing targets as a decision worth a record and founder confirmation.
- Low-confidence inputs must be surfaced, not smoothed over.

## Example
**Founder input:** "We sell handmade candles. Right now we sell to walk-in retail shoppers, a few gift shops that reorder, and we just got asked about corporate holiday gifting. Budget is about $1,500/mo, we run Instagram and a local farmers' market. Who should we focus on?"

**Skill reasoning:**
- business_type = mixed (B2C retail + B2B wholesale + B2B corporate).
- Candidate segments: (A) local individual gift buyers (B2C, geographic radius + psychographic "supports local/handmade"); (B) independent gift shops (B2B, firmographic small retailer, behavioral = reorders); (C) corporate bulk gifting (B2B, firmographic mid-size employers, behavioral = seasonal bulk).
- Revenue mix today ≈ A 70% / B 25% / C 0%.
- MAAW:
  - A: Measurable H, Accessible H (IG + market), Actionable H ($1.5k works), Worthwhile M → score 11 → primary.
  - B: Measurable H, Accessible M, Actionable H, Worthwhile M → score 10 → secondary.
  - C: Measurable M, Accessible L (no B2B outbound motion, no sales capacity), Actionable L (budget/capacity), Worthwhile H → has two Lows → **future**, unlock = build an outbound/wholesale motion + capacity.

**Output (abridged):** primary = local handmade-gift buyers; secondary = independent gift shops; future = corporate bulk gifting (unlock: wholesale capacity + outbound). Concentration risk flagged (segment A ~70%) → grow B to diversify.

**Executed vs. approval:** Skill wrote the three scored segments to `customers.segments` and created a task to build the segment-A persona (LOW, auto). Setting segment A + B as the *official* marketing targets was presented to the founder for confirmation before redirecting the ad budget.

## Provenance
SOURCE. Derives from the Marketing & Customer domain: Market Segmentation model (four variable families) and the MAAW segment-evaluation model (Measurable / Accessible / Actionable / Worthwhile), plus revenue-mix prioritization. MAAW summation scoring and the concentration-risk flag are CLAUDE conventions layered on the source model and marked inline. See `internal/PROVENANCE_MAP.md`.
