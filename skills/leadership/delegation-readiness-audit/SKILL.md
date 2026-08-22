---
name: delegation-readiness-audit
domain: leadership
version: 0.1.0
autonomy_ceiling: L0
provenance: SOURCE
reads: [leader, team, company, decisions, operations]
writes: [leader, metrics]
related_skills: [leadership-style-assessment, motivation-mapper, leadership-growth-planner]
owned_by_agents: [leadership-agent, orchestrator]
---

# Skill: Delegation Readiness Audit

## Purpose
Tell the founder, honestly, whether their own beliefs about people and work will let them delegate — or whether those beliefs are the bottleneck capping the company's growth. A founder who believes "if it's going to be right, I have to do it myself" cannot scale no matter how good the hire; this skill surfaces those control-oriented beliefs, scores where the founder sits on the control↔trust spectrum, and prescribes the coaching to move them toward healthy delegation.

## When to Use
- The founder is a bottleneck: working *in* the business not *on* it, every decision routes through them, they can't take a day off.
- The founder is about to make (or just made) a first management hire and needs to actually hand over authority.
- The founder complains that delegation "doesn't work here," that they always have to redo work, or that no one can be trusted with it.
- Growth has plateaued and the constraint looks like the founder's span rather than the market.
- As a follow-on when `leadership-style-assessment` flags Driver/Analytical control tendencies.

## When NOT to Use
- The founder wants to decide *which specific tasks or decisions* to delegate to *which specific person* — that is operating-model / People-domain work; this skill audits beliefs, not the delegation plan itself (hand off after).
- The problem is a genuine skills gap in the team, not the founder's beliefs → `resource-gap-analysis` (strategy) / People domain.
- The founder wants their leadership style classified → `leadership-style-assessment`.
- A specific employee's performance is the issue → People domain + founder; this skill never assesses an individual employee.

## Required Context
Reads Business Memory: `leader` (style profile from `leadership-style-assessment`, prior belief ratings, stated strengths/weaknesses), `team` (headcount, whether any managers exist, span of control), `company` (stage, growth state), `decisions` (how many recent decisions ran through the founder — behavioral evidence of centralization), `operations` (founder hours on non-owner work). Facts carry `source`, `confidence`, `as_of`. Belief self-reports are `restricted` founder data. Behavioral evidence (decision centralization, founder hours) is weighted alongside stated beliefs because founders often over-state their comfort with delegating.

## Inputs
```yaml
input:
  belief_ratings:                  # founder rates agreement 1-5 (1=strongly disagree, 5=strongly agree)
    must_do_it_myself: int         # "If it's going to be done right, I have to do it myself"
    work_harder_longer: int        # "If I just work longer and harder, I'll succeed"
    people_need_telling: int       # "People need to be told exactly what to do"
    people_slack_unchecked: int    # "People don't work hard unless you check up on them"
    people_want_challenge: int     # "People want to be challenged in their work"      (trust-oriented)
    people_need_autonomy: int      # "People need some autonomy to do their job well"  (trust-oriented)
  free_text_beliefs: [str]         # optional additional beliefs in the founder's words
  behavioral_signals:              # optional, from memory/integrations
    pct_decisions_through_founder: number   # 0-100
    founder_hours_on_nonowner_work: number  # hours/week
    has_managers: bool
    prior_delegation_attempts: [str]        # what was tried, what happened
  founder_style: enum(Driver, Expressive, Amiable, Analytical, unknown)  # from leadership-style-assessment
```

## Missing Information Protocol
1. If `belief_ratings` are missing, present the six belief statements to the founder as ONE concise batch and capture 1–5 ratings; do not infer a delegation score from style alone (style predicts tendency, not the actual belief).
2. If behavioral signals are available in memory/integrations, use them to corroborate or challenge the self-report before asking anything.
3. If self-report and behavior diverge (e.g., high trust ratings but 90% of decisions route through the founder), do not silently pick one — surface the gap as a finding.
4. Never assume the founder is a "delegation risk" purely from a Driver/Analytical style; the belief data decides.
5. Never fabricate behavioral percentages; mark them `unknown` and score on beliefs alone with a confidence flag.

## Diagnostic Questions
Answered internally:
- What does the founder believe to be true about human nature and how people should be led?
- Do those beliefs sit on the control end (people must be told and checked; only I can do it right) or the trust end (people want challenge and autonomy)?
- Does the founder's behavior match their stated beliefs, or is there a say/do gap?
- Is the founder physically capable of growing the org while holding these beliefs?
- Which single belief, if shifted, would unlock the most delegation?
- Has the founder tried to delegate before, and what belief got reinforced (or violated) when it went wrong?

## Analysis Framework
Beliefs are one of the four inner drivers that shape leadership (Identity → Motives → Values → Beliefs); beliefs about human nature directly determine delegation and control behavior. This audit maps the founder's beliefs onto a single control↔trust spectrum and cross-checks it against behavior.

**Control-oriented beliefs** (predict LOW delegation):
- "If it's going to be done right, I have to do it myself."
- "If I work longer and harder, I'll succeed."
- "People need to be told exactly what to do."
- "People don't work hard unless you check up on them."

**Trust-oriented beliefs** (predict HEALTHY delegation):
- "People want to be challenged in their work."
- "People need some autonomy to do their job well."

The four control statements pull the score toward Control; the two trust statements pull it toward Trust. Behavioral signals (decision centralization, founder hours, presence of managers) validate the belief score. The output is a readiness band plus targeted coaching aimed at the specific belief(s) holding delegation back.

## Calculations
Ratings are 1–5 (agreement).
- **control_load** = `must_do_it_myself + work_harder_longer + people_need_telling + people_slack_unchecked` → range 4–20 (higher = more control-oriented).
- **trust_load** = `people_want_challenge + people_need_autonomy` → range 2–10 (higher = more trust-oriented). Scale to 4–20 for comparability: `trust_scaled = trust_load × 2`.
- **delegation_readiness_score** = `trust_scaled − control_load` → range −16 to +16 (higher = more ready).
- **Readiness bands:**
  - `>= +6` → **Ready** (beliefs support delegation).
  - `−5 to +5` → **Mixed** (situational delegator; specific beliefs get in the way).
  - `<= −6` → **At-Risk** (control beliefs dominate → delegation bottleneck).
- **Say/do gap flag** = true if `delegation_readiness_score >= 0` (says ready) AND `pct_decisions_through_founder > 70` (behaves centralized), or the inverse.
- **Binding belief** = the single highest-rated control statement (the one to coach first).
- No financial calculations apply.

## Decision Rules
- IF `control_load >= 16` (mostly 4–5s on control statements) THEN band = **At-Risk**; founder is a delegation bottleneck → recommend authority-delegation coaching as the leadership priority.
- IF control-oriented beliefs dominate (delegation_readiness_score <= −6) THEN founder is a delegation risk → prescribe belief-reframing coaching targeting the binding belief; recommend `leadership-growth-planner`.
- IF `must_do_it_myself >= 4` THEN name it as the classic scaling cap; coaching = start with low-stakes, reversible tasks to build disconfirming evidence that others can do it right.
- IF `people_slack_unchecked >= 4` OR `people_need_telling >= 4` THEN coaching = shift from checking output to setting clear outcomes + autonomy; pair with `motivation-mapper` to see what actually drives the team.
- IF band = **Ready** but `pct_decisions_through_founder > 70` THEN surface the say/do gap: the beliefs are fine, the *habit* is the bottleneck → coaching = install a decision-delegation routine, not belief work.
- IF founder_style = Driver AND band = At-Risk THEN link to the Driver blind spot (delegate authority, don't squelch initiative); connect to the Dictatorial stress behavior.
- IF founder_style = Analytical AND `must_do_it_myself >= 4` THEN link to the "only the right way is acceptable" driver; coaching = define "good enough," set standards others can meet.
- IF `prior_delegation_attempts` failed THEN diagnose whether the failure reinforced a control belief and reframe (a single bad hand-off is evidence about the setup, not proof people can't be trusted).
- IF the founder wants to move to *which task to whom* THEN hand off to People/operating-model work — this skill's job ends at belief readiness + coaching.

## Procedure
1. Load `leader`, `team`, `company`, `decisions`, `operations`; note freshness and pull `founder_style`.
2. Collect `belief_ratings` (present the six statements as one batch if missing).
3. Compute control_load, trust_scaled, delegation_readiness_score, and readiness band.
4. Pull behavioral signals; compute the say/do gap flag.
5. Identify the binding belief (highest control rating).
6. Apply decision rules to generate targeted coaching for the binding belief and any secondary control beliefs.
7. Cross-link to the founder's style and stress behavior for a coherent picture.
8. If the diagnosis points to a development plan, recommend `leadership-growth-planner`; if to team-motivation causes, recommend `motivation-mapper`.
9. Assemble output; write the readiness score + coaching note to `leader` and a delegation metric to `metrics` (L0, internal self-data).

## Output
```yaml
output:
  delegation_readiness_score: number     # -16 to +16
  readiness_band: enum(Ready, Mixed, At-Risk)
  control_load: number                   # 4-20
  trust_load: number                     # 2-10
  binding_belief: str                    # the belief most blocking delegation
  say_do_gap: bool
  say_do_gap_note: str                   # if beliefs and behavior diverge
  confidence: enum(high, medium, low)    # lower if no behavioral corroboration
  coaching_actions: [ {belief: str, reframe: str, first_step: str} ]
  style_linkage: str                     # tie to founder's style + stress behavior
  recommended_next_skills: [str]
```

## Recommendations
Coaching is prioritized by which single belief is most blocking delegation (the binding belief) and how reversible the first step is — always start delegation practice on low-stakes, reversible work so a stumble produces learning, not a control-belief reinforcement. Each coaching item pairs the belief to reframe with a concrete first step. Recommendations are advisory to the founder; this skill does not delegate anything on the founder's behalf or reassign any employee's work.

## Execution Opportunities
- Write the delegation-readiness score + coaching note to `leader` — reversible, LOW, internal self-data.
- Write a `delegation_readiness` metric to `metrics` for tracking over time — reversible, LOW.
- Draft a founder-facing coaching one-pager (binding belief, reframe, first low-stakes hand-off to try) — reversible, LOW.
- Propose (not run) `leadership-growth-planner` and `motivation-mapper`.
No task is actually delegated, reassigned, or communicated to any employee by this skill.

## Human Approval Requirements
- No external or irreversible action; all writes are internal self-assessment data at L0.
- Any actual delegation of work/authority to a person is the founder's decision and is executed through the operating model / People domain, not here. Per `AUTONOMY_AND_APPROVAL_MODEL.md`, ceiling is L0.

## Escalation Conditions
- **Beliefs so control-oriented that the founder cannot grow the org** (At-Risk with high control_load) → flag as a strategic growth constraint and route to `leadership-growth-planner`; note for strategy that leadership span is a binding constraint.
- **Say/do gap driven by a trust breach with a specific person** → route to People + founder; do not assess the individual here.
- **Prior delegation failures tied to hiring/role-design problems** → route to People / `resource-gap-analysis`.
- **Founder distress about being unable to let go (overwork, burnout)** → recommend a qualified professional; do not counsel clinically.

## KPIs
- Movement in delegation_readiness_score across successive audits.
- Reduction in `pct_decisions_through_founder` and `founder_hours_on_nonowner_work` after coaching.
- Whether the founder completed the prescribed first low-stakes hand-off.
- Adoption of recommended next-skills.

## Monitoring
After the audit: watch whether the founder actually runs the first delegation experiment and how it lands; a success is disconfirming evidence to reinforce, a stumble needs reframing before it hardens a control belief. Track decision centralization and founder hours as leading indicators. Re-verify beliefs after any delegation attempt — beliefs move with evidence.

## Follow-Up
- Time-triggered: re-audit quarterly while the founder is actively working on delegation, else every 6–12 months.
- Event-triggered: before/after a first management hire, when growth plateaus on founder span, or when `leadership-style-assessment` flags control tendencies.

## Related Skills
Fed by `leadership-style-assessment` (style/control tendencies, stress behavior). Feeds `leadership-growth-planner` (coaching → development plan + metrics) and pairs with `motivation-mapper` (what drives the team, so the founder trusts outcomes over checking). Hands the actual delegation plan to the People domain / operating-model work.

## Guardrails
- Advisory only (L0); never delegate, reassign, or communicate work to any employee.
- Treat belief ratings as `restricted` founder data.
- Weigh behavior against self-report; never let a flattering self-report override clear centralization evidence — but surface the gap, don't accuse.
- The control↔trust score is a coaching lens, not a verdict on the founder's character; frame it as changeable.
- Do not turn belief data into a justification for any personnel action.
- On signs of overwork/burnout, refer to a professional rather than counseling.

## Example
**Founder input:** "Everyone tells me to delegate but honestly, if I want it done right I do it myself. I'm working 70 hours and I just hired an ops manager I don't really trust yet." Belief ratings: must_do_it_myself 5, work_harder_longer 4, people_need_telling 4, people_slack_unchecked 3, people_want_challenge 3, people_need_autonomy 3. Behavior: pct_decisions_through_founder 88, founder_hours_on_nonowner_work 45, has_managers true (new). Style: Driver.
**Reasoning:** control_load = 5+4+4+3 = 16; trust_load = 3+3 = 6 → trust_scaled 12; delegation_readiness_score = 12 − 16 = **−4** → band **Mixed**, but control_load 16 is high and behavior is highly centralized (88%). Binding belief = "I have to do it myself" (rated 5). Say/do gap = false (both say and do lean control — consistent). Confidence high (behavior corroborates). Style linkage: classic Driver bottleneck; under stress this becomes Dictatorial, which will drive the new ops manager away before trust can form.
**Output (abridged):** readiness_band Mixed (trending At-Risk); binding_belief "must do it myself"; coaching_actions: [{belief: "must do it myself", reframe: "Others can meet the standard if you define what 'right' means; your job is the standard, not the doing", first_step: "Hand the ops manager one reversible, low-stakes weekly task with a written definition of done, and do not touch it for two weeks"}, {belief: "people need telling", reframe: "Set the outcome, not the steps", first_step: "For that task, specify the result and the deadline only"}]. recommended_next_skills: [leadership-growth-planner, motivation-mapper].
**Executed vs. approval:** Wrote readiness score + coaching note to `leader`, `delegation_readiness` metric to `metrics`, drafted the founder coaching one-pager. Nothing delegated or communicated to the ops manager — the founder runs the experiment; role design routes to People.

## Provenance
SOURCE. Derives from the leadership domain's inner-drivers model (Identity → Motives → Values → Beliefs), the Belief-Audit (D3) control↔trust belief taxonomy, and the delegation-readiness decision rule ("IF control-oriented beliefs dominate THEN delegation risk → recommend authority-delegation work"). De-branded and described generically without citing any source book, author, or program. See `internal/PROVENANCE_MAP.md`.
