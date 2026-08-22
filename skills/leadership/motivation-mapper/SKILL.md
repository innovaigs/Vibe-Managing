---
name: motivation-mapper
domain: leadership
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [leader, team, company, goals]
writes: [leader, team, metrics]
related_skills: [leadership-style-assessment, delegation-readiness-audit, mission-vision-builder, leadership-growth-planner]
owned_by_agents: [leadership-agent, orchestrator]
---

# Skill: Motivation Mapper

## Purpose
Surface what actually drives the founder to run this business, and — for each key person — what makes them work here beyond the paycheck, so the founder can lead each one the way that person is actually motivated. Money is table stakes; retention, discretionary effort, and loyalty come from the non-monetary motivators. A founder who cannot name why a key employee works for them (beyond pay) is flying blind on the thing that keeps that person.

## When to Use
- The founder is designing incentives, a vision, or roles and wants them aligned to what truly drives people.
- A key person seems disengaged, or the founder is worried about losing them, and wants to understand what would actually keep them.
- The founder can't articulate what motivates their own business decisions (mission/vision work stalls without this).
- Onboarding into the leadership domain, to build the founder's self-motive profile and a key-people motivation map.
- After `leadership-style-assessment`, to pair each key person's style with their motivators for tailored management.

## When NOT to Use
- The founder wants to take a concrete action *on* an employee — a raise, promotion, role change, retention offer, or a conversation. This skill maps motivators and recommends an approach; the action routes to the People domain + founder.
- The question is about the founder's leadership style, not motives → `leadership-style-assessment`.
- The question is about delegation beliefs → `delegation-readiness-audit`.
- Comp benchmarking or a specific pay decision → People/HR domain (comp is out of scope; this skill is deliberately about non-monetary drivers).

## Required Context
Reads Business Memory: `leader` (any prior motive ranking, values, identity notes), `team` (key people, their styles from `leadership-style-assessment`, tenure, role importance, any known motivators), `company` (stage, what it can offer — growth, flexibility, mission), `goals` (founder's personal and business goals, to check alignment). Facts carry `source`, `confidence`, `as_of`. Employee-level motivation data is `restricted`; it is used to help the founder lead, never exposed beyond the founder, and per-person profiles are only as good as their source — anything the founder is guessing about an employee must be flagged "ask them."

## Inputs
```yaml
input:
  scope: enum(founder_motives, key_people_map, both)
  founder_motive_ranking: [str]      # founder rank-orders the motive taxonomy (top to bottom)
  founder_free_text_motives: [str]   # additional motives in the founder's words
  founder_emotional_pull: str        # what the founder *feels* most pulled toward (for mind-vs-heart check)
  key_people:                        # for key_people_map
    - name: str
      style: enum(Driver, Expressive, Amiable, Analytical, unknown)  # from leadership-style-assessment
      why_important: str             # why this person matters to the business
      why_they_work_here: str        # non-monetary reason, or "unknown"
      source: enum(they_told_me, i_am_guessing)   # provenance of why_they_work_here
      engagement_signal: enum(high, steady, slipping, unknown)
```

## Missing Information Protocol
1. **Founder motives:** if no ranking, present the motive taxonomy and ask the founder to rank their top few; capture free-text additions.
2. **Key people — the core rule:** IF `why_they_work_here` is `unknown` OR `source: i_am_guessing` THEN do NOT invent a motivator. Output an explicit **"ask them"** action for the founder — the principle is clear: if you cannot state why an employee works for you beyond a paycheck, you ask them directly.
3. Never assume an employee's motivator from their style alone — style predicts *how* to communicate, not *what* drives them.
4. If a founder's stated ranking and emotional pull diverge, do not resolve it silently — flag the mind-vs-heart conflict.
5. Batch missing-info questions into one concise set.

## Diagnostic Questions
Answered internally:
- **Founder:** What motivates me to run my own business — what value am I trying to create, for myself and others? What do I value in people and in business? Does my stated ranking match my emotional pull (mind vs. heart)?
- **Per key person:** Who are my key people and why is each important to the business? What motivates each of them to work here aside from compensation? How does someone best motivate a person like this (given their style)? Is their engagement holding?
- **Alignment:** Do the vision, incentives, and roles reflect what actually drives the founder and the key people, or something the founder assumes drives them?

## Analysis Framework
Motives are one of the four inner drivers (Identity → Motives → Values → Beliefs). Two mapping routines:

**A. Founder motive ranking (D2).** The founder rank-orders motivators from this taxonomy (plus free-text):
`Making a good living | Making as much money as possible | Doing the very best work | Doing interesting work | Doing significant work | Being my own boss | Choosing who I work with | Having control over my work life | Continuing a legacy | Contributing to my community`
Output: top-3 motives → used to align vision, incentives, and role design with what actually drives the founder. Flag **mind-vs-heart conflicts** where the stated ranking diverges from the emotional pull (e.g., ranks "make as much money as possible" first but lights up talking about "doing significant work").

**B. Key-people motivation map (D4).** Per key person: name, style, why important, why they work here (beyond pay). Each profile feeds the style-flex approach — the motivator says *what* to offer, the style says *how* to deliver it. Where the "why they work here" is unknown or guessed, the profile carries an "ask them" flag instead of a fabricated motivator.

Effective use of these maps sits inside compassionate leadership: genuine concern for people combined with real understanding of their motivations and the discipline to deliver on agreed priorities — compassion alone is insufficient.

## Calculations
No numeric formulas. Structured mappings only:
- **Founder top motives** = first 3 entries of the ranking (+ any strong free-text motive).
- **Mind-vs-heart conflict** = flagged when the top stated motive is not the one the founder's `founder_emotional_pull` points to.
- **Per-person confidence** = `high` if `source: they_told_me`; `low` + "ask them" if `unknown`/`i_am_guessing`.
- **Motivator-to-approach mapping** combines motivator (what) with style rule (how) — see Decision Rules.

## Decision Rules
**Founder**
- IF top motive is *money/good living* THEN align incentives and vision to financial outcomes and personal security; check it isn't crowding out a heart-motive.
- IF top motive is *doing significant/best work* or *legacy/community* THEN foreground purpose in the vision and in how wins are framed; recommend `mission-vision-builder`.
- IF top motive is *being my own boss / control over work life* THEN note the tension with delegation and cross-link `delegation-readiness-audit`.
- IF stated ranking ≠ emotional pull THEN surface the mind-vs-heart conflict and recommend resolving it before locking a vision or incentive plan.

**Key people (motivator → approach), delivered through the person's style**
- IF motivator is *growth/challenge* THEN offer stretch work, ownership, a development path.
- IF motivator is *recognition/status* THEN offer visible credit and advancement (deliver publicly for Expressive, privately/precisely for Analytical).
- IF motivator is *autonomy/flexibility* THEN offer latitude and flexible arrangements; reduce checking-up.
- IF motivator is *mission/impact* THEN connect their work explicitly to the company's purpose and the people it helps.
- IF motivator is *stability/belonging* THEN offer security, a stable team, and personal connection (natural fit for Amiable).
- IF motivator is *mastery/quality* THEN offer the tools, time, and standards to do excellent work (natural fit for Analytical).

**Style overlay (how to deliver the above)**
- Driver → be brief, results-framed, give them decisions to own.
- Expressive → enthusiasm, big-picture, public recognition, don't drown in detail.
- Amiable → rapport first, reassurance, no pressure/conflict.
- Analytical → data, precision, thinking time, proper process.

**The unknown rule**
- IF `why_they_work_here` is unknown or guessed THEN the ONLY action is "ask them" — no fabricated motivator, no approach recommendation built on a guess.
- IF `engagement_signal = slipping` AND motivator known THEN recommend a founder conversation aligned to that motivator, routed through People + founder (this skill does not act on the employee).

## Procedure
1. Determine `scope`. Load `leader`, `team`, `company`, `goals`; pull styles from prior assessments.
2. **Founder motives:** capture/parse the ranking; extract top 3; run the mind-vs-heart check against emotional pull.
3. **Key people:** for each, record style, why-important, why-they-work-here + its source; set per-person confidence.
4. For each person with a known motivator, build the motivator→approach recommendation and overlay their style.
5. For each unknown/guessed motivator, emit an "ask them" action (a suggested question the founder can ask), not a recommendation.
6. Check alignment: do current vision/incentives/roles match the founder's real motives and the team's motivators? Note gaps.
7. Route: purpose motives → `mission-vision-builder`; control motive tension → `delegation-readiness-audit`.
8. Assemble output; write the founder motive profile to `leader`, per-person motivation profiles to `team` (restricted), and an alignment metric to `metrics`. At L1, these internal writes and any founder-facing conversation drafts are prepared and shown to the founder.

## Output
```yaml
output:
  founder_motives:
    top_motives: [str]             # ranked top 3
    mind_vs_heart_conflict: bool
    conflict_note: str
    alignment_recommendations: [str]   # vision/incentive/role alignment
  key_people_map:
    - name: str
      style: enum(Driver, Expressive, Amiable, Analytical, unknown)
      why_important: str
      motivator: str               # or "UNKNOWN — ask them"
      confidence: enum(high, low)
      recommended_approach: str    # motivator (what) + style (how); empty if unknown
      ask_them_question: str       # suggested question when motivator unknown
      engagement_flag: enum(high, steady, slipping, unknown)
  alignment_gaps: [str]            # where current incentives/vision/roles mismatch real motivators
  recommended_next_skills: [str]
```

## Recommendations
Founder-motive recommendations are prioritized to resolve any mind-vs-heart conflict first (a vision built on a stated motive the founder doesn't actually feel will not sustain them), then to align vision/incentives/roles. Key-people recommendations are prioritized by engagement risk × role importance: a slipping high-importance person with a known motivator gets the first, most specific approach; anyone with an unknown motivator gets an "ask them" action before any approach is designed. All people recommendations are advisory to the founder — the founder acts, with People-domain support.

## Execution Opportunities
- Write the founder motive profile to `leader` — reversible, LOW.
- Write per-person motivation profiles to `team` (restricted) — reversible, LOW-MEDIUM (sensitive people data).
- Write a motivation-alignment metric to `metrics` — reversible, LOW.
- Draft a founder-facing conversation guide ("ask them" questions, motivator-aligned talking points) — reversible, LOW; prepared for founder approval at L1.
- Propose (not run) `mission-vision-builder`, `delegation-readiness-audit`.
This skill never sends a message to, or takes an action on, any employee. Incentive/role/comp *changes* are proposed to the founder and executed via People.

## Human Approval Requirements
- L1 ceiling: internal writes and drafts are prepared and shown to the founder before being finalized; nothing is sent to an employee.
- Any change to incentives, roles, or comp, and any conversation with an employee, requires founder approval and routes to the People domain. Per `AUTONOMY_AND_APPROVAL_MODEL.md`, this skill does not act on individuals.
- Writing restricted per-person motivation data requires the founder to have consented to storing it.

## Escalation Conditions
- **A slipping key person who is critical to the business** → flag as a retention/key-person risk; route the retention action to People + founder (and note for `risk` if the dependency is severe).
- **Motivator conflict that implies a fairness/equity issue across the team** → route to People/HR.
- **Founder mind-vs-heart conflict that destabilizes the whole vision** → recommend pausing `mission-vision-builder` until resolved.
- **Comp or legal dimension to a motivation problem** → route to People/HR / legal; do not advise on pay or employment terms here.

## KPIs
- % of key people whose non-monetary motivator the founder can name (from source: they_told_me) — the core self-awareness KPI.
- Retention/engagement of key people after motivator-aligned approaches (via People-domain follow-up).
- Whether "ask them" actions were completed and converted unknowns into known motivators.
- Founder motive clarity: mind-vs-heart conflict resolved before vision lock.

## Monitoring
After the map: track whether the founder completed the "ask them" conversations and update profiles with what was learned. Watch engagement signals on key people and re-check that the approach in use matches the stated motivator. Refresh profiles when a person's role, life stage, or engagement changes — motivators are not static.

## Follow-Up
- Time-triggered: refresh the key-people map every 6 months; refresh founder motives yearly or when personal goals change.
- Event-triggered: before designing incentives or a vision, when a key person's engagement slips, after a new key hire, or when a role materially changes.

## Related Skills
Paired with `leadership-style-assessment` (styles that this map's approaches flex toward). Feeds `mission-vision-builder` (founder motives shape a vision that will actually sustain the founder and attract talent) and links to `delegation-readiness-audit` (control-motive tension) and `leadership-growth-planner`. Hands all employee actions to the People domain.

## Guardrails
- Never fabricate an employee's motivator; unknown → "ask them," always.
- Treat per-person motivation data as `restricted`; use it only to help the founder lead, never expose it to other employees or third parties.
- Advisory only for people actions (L1 internal drafts); the founder acts, People executes.
- Comp and legal matters are out of scope — route to People/HR/legal.
- Style is *how* to deliver, not *what* motivates — never substitute one for the other.
- Do not use motivation data to manipulate or to justify adverse treatment of anyone.

## Example
**Founder input:** "Help me not lose my lead designer, Maya, and figure out what actually drives me — I keep saying it's the money but I'm not sure. Rank: (1) doing significant work, (2) being my own boss, (3) making a good living. Emotional pull: I light up when we ship something that changes how customers work. Maya: Expressive, she's important because she owns our whole product look; she once told me she stays because she gets to shape the vision, not just execute. She's been quieter lately." 
**Reasoning:** Founder top motives = significant work, autonomy, good living. Stated #1 (significant work) matches the emotional pull → no mind-vs-heart conflict; earlier "it's the money" was a reflex, not the real driver — note it. "Being my own boss" (control motive) → flag delegation tension. Maya: motivator = *shaping the vision / impact* (source: she told me → confidence high); style Expressive → deliver with enthusiasm, big-picture, public recognition, involve her early in vision. engagement_signal slipping + high importance → retention flag.
**Output (abridged):** founder top_motives [significant work, being my own boss, good living]; mind_vs_heart_conflict false (with note that stated money-motive is not the real driver); alignment_recommendations: [frame the company vision around customer impact; connect wins to "significant work"; watch that the autonomy motive doesn't block delegation]. key_people_map: [{name: Maya, style: Expressive, motivator: "shaping the vision/impact", confidence: high, recommended_approach: "bring her into vision-setting early and visibly; give public credit for product direction; big-picture framing, not task lists", engagement_flag: slipping}]. alignment_gaps: ["Maya's motivator is vision-shaping but she's been kept in execution lately"]. recommended_next_skills: [mission-vision-builder, delegation-readiness-audit].
**Executed vs. approval:** Wrote founder motive profile to `leader` and Maya's profile to `team` (restricted); drafted a founder-facing conversation guide to re-involve Maya in vision-setting (shown for approval at L1). No message sent to Maya and no role change made — the founder acts, and any role/scope change routes to People.

## Provenance
SOURCE. Derives from the leadership domain's inner-drivers model (Identity → Motives → Values → Beliefs), the Motive Ranking diagnostic (D2) and its motive taxonomy + mind-vs-heart conflict flag, the Key-People Motivation Map (D4) with its "if unknown, ask them" rule, and the Compassionate Leadership model. De-branded and described generically without citing any source book, author, or program. See `internal/PROVENANCE_MAP.md`.
