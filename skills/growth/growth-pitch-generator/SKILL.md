---
name: growth-pitch-generator
domain: growth
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [company, strategy, finance, metrics, goals, customers, offerings]
writes: [strategy]
related_skills: [growth-plan-builder, kpi-design, executive-dashboard-builder, monthly-business-review]
owned_by_agents: [growth-agent]
---

# Skill: Growth Pitch Generator

## Purpose
Compress a full growth plan into a tight, three-minute pitch: what the business is, the three key points of the plan, the critical success factors tracked on the dashboard, and the three next steps to execute — all backed by specific metrics. This gives the founder a communicable, memorable summary of the whole plan that fits on three slides and survives a hallway conversation.

## When to Use
- The founder asks for "the short version," "my elevator pitch," "a 3-slide summary of my plan," "how do I explain this in 3 minutes?", or "the pitch version."
- A full growth plan exists (via `growth-plan-builder`) and now needs a compressed communication artifact.
- The founder is preparing to brief a partner, advisor, team, or lender at a high level (content only; any external sharing is separately approved).

## When NOT to Use
- The full plan does not exist yet → run `growth-plan-builder` first; the pitch is a compression of it, not a substitute.
- The founder needs the detailed working document → use `growth-plan-builder`.
- The founder needs the live metric monitoring view → use `executive-dashboard-builder`.
- This is a fundraising pitch requiring valuation, use-of-funds, and cap-table detail → that exceeds this skill; escalate to a dedicated financing/valuation flow.

## Required Context
- `company` — what the business is (model, offering) for the opening line.
- `strategy` — the Opportunity Statement and the growth pathway (source of the three key points).
- `goals` — the 3 Success Factors, 3 Progress Metrics, and 3 dated Next Steps (the execution triad).
- `finance` / `metrics` — the specific numbers that make each point concrete (targets, key ratios).

## Inputs
```yaml
input:
  growth_plan_ref: id|null         # link to the assembled plan, if available
  business_summary: text|null       # what the business is/does
  opportunity_statement: text|null  # the EEC north-star sentence
  key_points: list|null             # candidate plan highlights to compress to exactly 3
  success_factors: list|null        # the 3 critical success factors (dashboard-tracked)
  progress_metrics: list|null       # the 3 metrics proving progress
  next_steps: list|null             # exactly 3, each with a deadline
  headline_metrics: object|null     # specific numbers to anchor the points (revenue target, margin, MRR, etc.)
  audience: enum(internal, advisor, team, general)  # tunes tone/emphasis, not the facts
```

## Missing Information Protocol
1. Pull every element from the assembled growth plan / Business Memory first; the pitch should require no new analysis.
2. If the execution triad (Success Factors / Progress Metrics / Next Steps) is missing, route to `growth-plan-builder` — the pitch cannot be fabricated from nothing.
3. If specific metrics are unavailable for a point, mark the point `needs a number` rather than shipping a vague claim; a metric-free pitch violates the standard.
4. Never invent a target, a metric, or a deadline to make the pitch sound complete.

## Diagnostic Questions
- Can the business be stated in one clear sentence a stranger would understand?
- Which three plan points, if the founder could say only three things, best capture the strategy?
- Is each point anchored by a specific metric (not an adjective)?
- Are the critical success factors the same ones tracked on the dashboard (consistency)?
- Are there exactly three next steps, each with a deadline?
- Is every claim traceable to the full plan (no drift, no embellishment)?

## Analysis Framework
Compress to the canonical four-part pitch structure (efficient, effective, compelling — essential content, clear, no jargon):

1. **What is the business** — one or two sentences: model, offering, who it serves. Draw from `company` + the Opportunity Statement.
2. **3 key points of the growth plan** — the three highest-signal moves of the strategy (e.g., value-chain repositioning, offer expansion, revenue-model shift). Each point carries a specific metric that makes it concrete.
3. **Critical success factors (tracked on the dashboard)** — the 3 Success Factors and the Progress Metrics that prove them; these must match the dashboard so the pitch and the monitoring layer tell the same story.
4. **3 next steps to execute** — exactly three, each with a deadline and (ideally) an owner.

Compression discipline: cut everything that is not one of these four; every retained sentence must earn its place; every point must include a number.

## Calculations
This skill does not compute new figures; it selects and restates figures from the plan. It performs consistency checks only:
- **Metric-coverage check** = each key point and each success factor has ≥ 1 specific metric attached (pass/fail per element).
- **Triad-count check** = Success Factors = 3, Progress Metrics = 3, Next Steps = 3, each Next Step has a deadline.
- **Traceability check** = every claim maps back to a growth-plan section (no orphan claims).

## Decision Rules
- IF the execution triad is missing THEN route to `growth-plan-builder`; do not generate a pitch from nothing.
- IF a key point or success factor has no specific metric THEN mark it `needs a number` and request it rather than shipping a vague claim.
- IF Success Factors ≠ 3 OR Next Steps ≠ 3 OR any Next Step lacks a deadline THEN flag the triad as malformed and correct before finalizing.
- IF the pitch's success factors differ from the dashboard's THEN reconcile to the dashboard (single source of truth).
- IF a claim cannot be traced to the plan THEN drop it (the pitch never adds facts the plan does not support).
- IF `audience` changes THEN adjust tone/emphasis ONLY — never the underlying numbers or claims.
- IF the compression would omit a metric to fit length THEN cut a sentence instead; metrics are non-negotiable.

## Procedure
1. Load the growth plan and the execution triad from Business Memory / the plan reference.
2. Draft part 1 (what the business is) from `company` + Opportunity Statement.
3. Select the 3 key points; attach a specific metric to each.
4. State the 3 critical success factors + progress metrics; reconcile them to the dashboard.
5. List exactly 3 next steps, each with a deadline.
6. Run the metric-coverage, triad-count, and traceability checks; mark any `needs a number`.
7. Emit the pitch (L1 draft) tuned to `audience`, plus the check results and any gaps.
8. On founder approval, store the pitch as the current compressed summary in `strategy`.

## Output
```yaml
output:
  pitch:
    what_is_the_business: text     # 1-2 sentences
    key_points:                    # exactly 3
      - {point: str, metric: str}
    critical_success_factors:      # exactly 3, dashboard-tracked
      - {factor: str, progress_metric: str}
    next_steps:                    # exactly 3
      - {step: str, deadline: date, owner: str|null}
    audience: enum(internal, advisor, team, general)
  checks:
    metric_coverage: enum(pass, fail)
    triad_counts_ok: bool
    dashboard_consistent: bool
    traceable: bool
  gaps: [str]                      # elements marked "needs a number" or missing
  slide_form: [ {slide, headline, bullets} ]   # optional 3-slide rendering
```

## Recommendations
The pitch surfaces, as gaps, any point or success factor lacking a specific metric — because a metric-free pitch is the most common failure of this artifact. Gaps are ordered: missing metrics first (they undermine credibility), then triad malformation, then dashboard inconsistency. The recommendation is always to fill the number from the plan or the founder, never to soften the claim into an adjective. Tone is adapted to audience; facts never are.

## Execution Opportunities
- Produce the compressed pitch and optional 3-slide rendering (reversible, LOW) — L1 draft.
- Store the pitch as the current compressed summary in `strategy` after approval (reversible, LOW).
- Generate audience-tuned variants (internal vs advisor) with identical facts (reversible, LOW).

## Human Approval Requirements
- Any external delivery of the pitch (to a lender, partner, advisor, or team beyond the founder) requires founder approval before it leaves the system — the pitch may contain forward-looking targets that read as commitments.
- Storing the pitch as the authoritative summary requires founder confirmation.
- Drafting and internal variants proceed at L1. Complies with AUTONOMY_AND_APPROVAL_MODEL.md.

## Escalation Conditions
- The full growth plan does not exist → route to `growth-plan-builder` (cannot compress nothing).
- The pitch would imply targets beyond confirmed capacity or a public commitment → founder (and accountant if financial).
- The request is actually a fundraising ask requiring valuation/use-of-funds → escalate to a dedicated financing flow.
- Plan facts are stale or low-confidence → surface the uncertainty; do not present forecast targets as settled commitments.

## KPIs
- Metric-coverage rate (every point and factor carries a number).
- Consistency with the dashboard and full plan (no drift).
- Founder edit rate on the draft (lower = better compression fidelity).
- Whether the pitch is reused unchanged across audiences (a sign it captured the essence).

## Monitoring
After the pitch is generated, watch for divergence: if the plan, dashboard, or forecast changes, the pitch is stale and must be regenerated. Track whether the three next steps and success factors in the pitch stay aligned with what `monthly-business-review` is actually tracking.

## Follow-Up
- Regenerate whenever the growth plan is refreshed (quarterly) or materially changed (opportunity, forecast, or execution triad update).
- Event-triggered before any high-level briefing where the founder needs the short version.

## Related Skills
Compresses the output of `growth-plan-builder`; pulls success factors/metrics consistent with `executive-dashboard-builder` and `kpi-design`; its three next steps and success factors are the same ones `monthly-business-review` tracks over time.

## Guardrails
- Never ship a pitch without a specific metric on every key point and success factor.
- Never add a fact the full plan does not support; the pitch compresses, it does not embellish.
- Adjust tone for audience, never the numbers.
- Forward-looking targets in the pitch are projections, not promises — label them as such, and hold external delivery for approval.
- Enforce exactly three key points, three success factors, and three dated next steps — the discipline is the point.

## Example
**Founder input:** "Give me the 3-minute version of my growth plan for a chat with my advisor."

**Skill reasoning:**
- Loads the assembled plan. Business is a services firm moving from subcontractor work to direct, retainer-based client relationships.
- Part 1: "We provide [service]; today mostly as a subcontractor, and we're moving to direct retainer clients for higher margin and predictable revenue."
- 3 key points, each with a metric: (a) reposition up the value chain to direct clients — target 10 retainer clients in 12 months; (b) shift to recurring revenue — grow MRR to $40k/month; (c) protect margin while scaling — hold gross margin ≥ 55%.
- Critical success factors (dashboard-tracked): land 10 retainers (progress metric: signed retainers/quarter); MRR growth (progress metric: MRR); margin discipline (progress metric: blended gross margin %). Reconciled to the dashboard — consistent.
- 3 next steps: (1) convert 2 current subcontract clients to retainers by end of Q1; (2) hire a delivery lead by end of Q2; (3) launch the retainer offer page by end of month.
- Checks: metric_coverage pass, triad counts ok, dashboard_consistent true, traceable true. gaps = none.

**Output (abridged):** four-part pitch + optional 3-slide rendering, advisor tone; all checks pass; no gaps.

**Executed vs. approval:** Pitch drafted and stored internally at L1. Delivering it to the advisor (external) held for founder approval, since the MRR and client targets are forward-looking.

## Provenance
SOURCE — derived from the Growth Execution domain knowledge (`09-growth-execution.md`): the "Growth Plan Pitch" compressed output form (what-is-the-business + 3 key points + critical success factors tracked on the dashboard + 3 next steps, with specific metrics required) and the EEC (efficient/effective/compelling) communication standard. The classroom framing ("3 slides / 3 minutes" as an exercise, presentation logistics) was discarded per the knowledge file; only the content structure is retained. De-branded, no named company. See internal/PROVENANCE_MAP.md.
