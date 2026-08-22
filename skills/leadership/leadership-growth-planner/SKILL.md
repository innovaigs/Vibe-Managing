---
name: leadership-growth-planner
domain: leadership
version: 0.1.0
autonomy_ceiling: L0
provenance: SOURCE
reads: [leader, team, company, goals, metrics]
writes: [leader, metrics]
related_skills: [leadership-style-assessment, delegation-readiness-audit, motivation-mapper, mission-vision-builder]
owned_by_agents: [leadership-agent, orchestrator]
---

# Skill: Leadership Growth Planner

## Purpose
Turn the founder's leadership self-awareness into a concrete personal development plan with named actions and three trackable growth metrics — so "become a better leader" becomes a plan you can actually execute and measure. The aim is that the founder grows fast enough to grow the organization, and earns the best performance and highest commitment from employees, because people follow a leader they want to follow rather than one they're made to.

## When to Use
- After `leadership-style-assessment`, `delegation-readiness-audit`, or `motivation-mapper` surfaces growth edges the founder wants to act on.
- The founder asks: "How do I get better as a leader?", "What should I work on?", "How do I know if I'm actually improving?"
- The founder is scaling and knows they must level up to lead a bigger org.
- On a periodic cadence to review progress and reset development goals.

## When NOT to Use
- The founder wants to classify their style or detect stress behavior → `leadership-style-assessment`.
- The plan is about the *company's* strategy/goals, not the founder's personal development → `strategic-planning`.
- The development need is a hard technical/functional skill better served by a domain skill or external training the founder already knows they want (this skill can still fold that in as an action, but doesn't teach it).
- The issue is a specific employee's development → People domain.

## Required Context
Reads Business Memory: `leader` (style profile, growth edges/watch-outs, delegation-readiness, motives, prior development plans and their status), `team` (feedback signals, engagement/retention of key people as effectiveness indicators), `company` (stage — the leadership demanded by the current stage), `goals` (the founder's personal goals the plan should progress toward), `metrics` (any existing leadership metrics to continue tracking). Facts carry `source`, `confidence`, `as_of`. All plan and self-assessment data is `restricted` founder data.

## Inputs
```yaml
input:
  strengths: [str]                 # current leadership strengths (from assessment)
  weaknesses: [str]                # growth edges / watch-outs (from assessment)
  growth_edges_from_domain:        # inputs from the other leadership diagnostics
    style: str                     # primary style + stress behavior
    delegation_band: enum(Ready, Mixed, At-Risk, unknown)
    motive_alignment_gaps: [str]
  personal_goals: [str]            # what the founder wants for themselves (from goals/motivation-mapper)
  development_appetite: enum(light, moderate, intensive)   # how much the founder will invest
  candidate_actions: [str]         # actions the founder already has in mind (e.g., "hire a coach")
  existing_metrics: [ {name: str, current: number, target: number} ]  # any metrics already tracked
```

## Missing Information Protocol
1. Pull strengths/weaknesses and growth edges directly from `leader` (populated by the other leadership skills) before asking; run `leadership-style-assessment` first if no profile exists.
2. If personal goals are absent, ask the founder ONE concise batch — a development plan must progress toward the founder's own goals, not a generic ideal.
3. Do not invent metrics with fabricated baselines; if a baseline is unknown, include the metric with a "measure baseline first" step.
4. Never prescribe a clinical intervention; if a growth edge is really a mental-health matter, refer to a professional.
5. Do not pad the plan — match scope to `development_appetite`; an over-ambitious plan that won't be executed is worse than a focused one.

## Diagnostic Questions
Answered internally:
- What steps should the founder take to develop so they can grow the organization and earn the best performance and highest commitment from employees?
- Which growth edge, if improved, would most unblock the company at its current stage?
- What are the founder's strengths to build on (not just weaknesses to fix)?
- What three metrics will tell the founder they are growing as a leader and progressing toward their personal goals?
- Is the plan sized to what the founder will actually do?

## Analysis Framework
The Leadership Growth Plan (D7). Inputs: today's strengths/weaknesses; development steps; three growth metrics. Output: a development plan with named actions and three trackable metrics.

The three metrics should span the three things leadership growth is supposed to move (the founder must define their own three; these are the canonical categories to instantiate):
1. **Employee performance / commitment indicator** — e.g., % of key employees whose non-monetary motivators the founder can name (from `motivation-mapper`); engagement or retention of key people; team-feedback score.
2. **Delegation indicator** — e.g., % of decisions made without the founder; hours/week the founder spends on non-owner work (from `delegation-readiness-audit`).
3. **Founder-development indicator** — e.g., coaching sessions completed, a course finished, a feedback-solicitation cadence sustained.

Effectiveness signals the plan is ultimately serving (from the compassionate-leadership model): trust, collaboration quality, loyalty, and perceived competence.

Plan structure per action: `growth_edge → action → owner (founder) → cadence → what "done"/progress looks like`, sequenced from the highest-leverage edge for the current company stage.

## Calculations
No financial formulas. Metric instantiation and progress math:
- **Growth metric target** = a founder-set target with a baseline and a horizon; progress = `(current − baseline) / (target − baseline) × 100%`.
- **Leverage ranking of growth edges** = severity of the edge × relevance to the current company stage (a delegation edge is high-leverage for a founder trying to scale; a public-speaking edge is high-leverage for a founder about to fundraise).
- **Plan sizing** = number of concurrent actions capped by `development_appetite` (light ≈ 1–2, moderate ≈ 3, intensive ≈ 4–5) — deliberately bounded so the plan is executed.

## Decision Rules
- IF no style profile exists THEN run `leadership-style-assessment` first — the plan targets the growth edges it surfaces.
- IF delegation_band = At-Risk THEN make a delegation action the top priority and set a delegation metric (e.g., reduce % decisions through founder); link `delegation-readiness-audit`.
- IF the founder cannot name key people's motivators THEN set "% of key people whose motivator I can name" as the performance/commitment metric and add an action to run/complete `motivation-mapper` "ask them" conversations.
- IF a growth edge is a stress/backup behavior (Dictatorial/Avoiding/Accommodating/Attacking) THEN add a specific trigger-management action (recognize the trigger, install a pause) rather than a vague "be calmer."
- IF the founder's stage is scaling THEN weight delegation and communication edges highest; IF early/survival stage THEN weight decisiveness and focus.
- IF `development_appetite = light` THEN cap the plan at 1–2 actions on the single highest-leverage edge; do not overload.
- IF a candidate action is a hard-skill course/coach the founder wants THEN fold it in as a named action with a completion metric.
- IF a metric has no baseline THEN the first step is to measure the baseline before setting a target.
- IF a growth edge implies a mental-health issue THEN refer to a professional; do not put clinical work in the plan.

## Procedure
1. Load `leader` (strengths, growth edges, delegation band, motive gaps, prior plan), `company` (stage), `goals`, `team`, `metrics`.
2. If no leadership profile exists, route to `leadership-style-assessment` first.
3. Rank growth edges by leverage for the current stage.
4. Confirm/collect the founder's personal goals and `development_appetite`.
5. Draft named development actions for the top edges (folding in the founder's candidate actions), each with owner, cadence, and a progress definition; cap the count to the appetite.
6. Instantiate exactly three trackable growth metrics — one per category (performance/commitment, delegation, founder-development) — each with baseline (or a baseline-measurement step) and target and horizon.
7. Sequence the plan; note dependencies (e.g., run `motivation-mapper` to populate the commitment metric).
8. Assemble output; write the development plan + the three metrics to `leader` and `metrics` (L0, internal self-data). Set review cadence.

## Output
```yaml
output:
  strengths_to_build_on: [str]
  priority_growth_edges: [str]      # leverage-ranked for current stage
  development_actions:
    - growth_edge: str
      action: str
      owner: str                    # the founder
      cadence: str                  # e.g., weekly, monthly
      progress_definition: str      # what improvement looks like
  growth_metrics:                   # exactly three, one per category
    - name: str
      category: enum(performance_commitment, delegation, founder_development)
      baseline: number              # or null with a "measure first" step
      target: number
      horizon: str
  review_cadence: str
  recommended_next_skills: [str]
```

## Recommendations
Actions are prioritized by leverage for the current company stage — the growth edge that most limits the founder's ability to grow the organization comes first — and the plan is deliberately sized to the founder's stated appetite so it gets executed rather than admired. Exactly three metrics are set (never more, per the model), one in each category, each with a baseline and horizon so progress is unambiguous. The plan builds on strengths, not only fixes weaknesses. It is the founder's own plan; this skill tracks and reminds but takes no action on anyone.

## Execution Opportunities
- Write the leadership development plan + three growth metrics to `leader` and `metrics` — reversible, LOW, internal self-data.
- Create internal reminders for review cadence and action check-ins — reversible, LOW.
- Draft a founder-facing one-page development plan — reversible, LOW.
- Propose (not run) `leadership-style-assessment`, `delegation-readiness-audit`, `motivation-mapper`.
This skill does not enroll the founder in anything, spend money, or act on any employee; external actions (hiring a coach, booking a course) are the founder's to execute.

## Human Approval Requirements
- L0 ceiling: all writes are internal self-development data; the founder owns and approves the plan.
- Any action that spends money (coach, course) or involves another person is the founder's to execute; this skill only names it as a plan item. Per `AUTONOMY_AND_APPROVAL_MODEL.md`, no external or employee-facing action is taken.

## Escalation Conditions
- **A growth edge that is really a mental-health matter (burnout, depression)** → refer to a qualified professional; do not put clinical work in the plan.
- **Leadership growth blocked by a co-founder or governance issue** → surface it; route to the appropriate strategy/People conversation.
- **A development need that is actually a fit problem (the founder doesn't want to lead a bigger org)** → surface honestly; this may reroute to strategy (e.g., hiring a CEO/COO, `exit-readiness`) rather than a growth plan.
- **The plan requires spend the business can't afford** → note the cost/reversibility and let the founder decide; do not commit funds.

## KPIs
- The three growth metrics themselves — movement of each toward target over the horizon (this skill's success is measured by the metrics it sets).
- % of development actions actually started and sustained at cadence.
- Downstream effectiveness signals: key-people retention/engagement, reduced founder hours on non-owner work, trust/feedback scores.
- Whether the plan is revisited on cadence rather than abandoned.

## Monitoring
After the plan: track the three metrics against baseline at the review cadence; watch whether actions are sustained (a coach hired but never met with is not progress). Re-rank growth edges as the company stage shifts. Update the plan when a new assessment surfaces a different top edge, or when a metric hits its target (retire it and set the next).

## Follow-Up
- Time-triggered: review at the set cadence (monthly for intensive plans, quarterly otherwise); full replan yearly.
- Event-triggered: after a new leadership assessment, a stage change (scaling, fundraise), a leadership incident, or when a growth metric hits target.

## Related Skills
Fed by `leadership-style-assessment` (growth edges, stress behavior), `delegation-readiness-audit` (delegation metric), and `motivation-mapper` (performance/commitment metric, motive alignment). Aligns with `mission-vision-builder` (personal goals ↔ company vision) and may reroute to `strategic-planning` or `exit-readiness-analysis` if the real issue is founder-role fit. Employee development routes to the People domain.

## Guardrails
- Advisory only (L0); the plan is the founder's, and no action is taken on any employee.
- Treat all plan and self-assessment data as `restricted`.
- Set exactly three metrics, each with a real baseline (or a baseline-first step) — never fabricate a baseline or target.
- Size the plan to the founder's appetite; do not over-prescribe.
- Refer mental-health matters to professionals; do not put clinical work in a development plan.
- Do not commit spend or enroll the founder in anything — name it, let the founder execute.

## Example
**Founder input:** "I did the style assessment (I'm a Driver, stress = Dictatorial), the delegation audit put me At-Risk, and I couldn't name why 3 of my 5 key people work here. I want to scale to 30 people in two years and stop being the bottleneck. Moderate appetite; I'm open to a coach." Company stage: scaling. Personal goal: build a company that runs without me in the room.
**Reasoning:** Growth edges ranked for scaling stage: (1) delegation (At-Risk, directly caps scaling — top leverage), (2) stress behavior Dictatorial (will worsen as pressure rises), (3) knowing key-people motivators (commitment/retention as headcount grows). Appetite moderate → ~3 actions. Metrics, one per category: performance_commitment = "% of key people whose motivator I can name" (baseline 40% → target 100% in 3 mo); delegation = "% of decisions made without me" (baseline unknown → measure first, then target); founder_development = "monthly coaching sessions" (baseline 0 → target 1/mo sustained).
**Output (abridged):** strengths_to_build_on: [decisiveness, drive, results focus]. priority_growth_edges: [delegation, Dictatorial-under-stress, knowing team motivators]. development_actions: [{growth_edge: delegation, action: "hand off one reversible weekly decision to the ops manager and don't touch it", cadence: weekly, progress_definition: "decisions made without me rising month over month"}, {growth_edge: Dictatorial stress, action: "name the trigger and install a 24-hour pause before high-pressure directives", cadence: as-triggered, progress_definition: "fewer order-giving episodes reported in feedback"}, {growth_edge: team motivators, action: "complete motivation-mapper 'ask them' conversations with the 3 unknown key people", cadence: within 30 days, progress_definition: "motivator known for all 5"}]. growth_metrics: the three above. review_cadence: monthly. recommended_next_skills: [motivation-mapper, delegation-readiness-audit].
**Executed vs. approval:** Wrote the development plan and three metrics to `leader`/`metrics`, set monthly review reminders, drafted the one-page plan. Hiring the coach and holding the conversations are the founder's to execute; nothing was spent or sent.

## Provenance
SOURCE. Derives from the leadership domain's Leadership Growth Plan diagnostic (D7) — strengths/weaknesses → development steps → three trackable growth metrics — and the metric categories (employee performance/commitment, delegation, founder-development) plus the effectiveness signals from the compassionate-leadership model. De-branded and described generically without citing any source book, author, program, or coaching vendor. See `internal/PROVENANCE_MAP.md`.
