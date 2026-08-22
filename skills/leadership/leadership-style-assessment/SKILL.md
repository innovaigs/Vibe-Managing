---
name: leadership-style-assessment
domain: leadership
version: 0.1.0
autonomy_ceiling: L0
provenance: SOURCE
reads: [leader, team, company, decisions]
writes: [leader, metrics]
related_skills: [delegation-readiness-audit, motivation-mapper, leadership-growth-planner, mission-vision-builder]
owned_by_agents: [leadership-agent, orchestrator]
---

# Skill: Leadership Style Assessment

## Purpose
Give the founder an honest, structured read on their default leadership style, how that style degrades under stress, and exactly how to flex it to a specific person or situation. Self-awareness is the lever: a founder who knows their default and their backup behavior can consciously adapt instead of pushing a failing approach harder — which is the difference between getting people to follow because they *want to* versus because they are *made to*.

## When to Use
- The founder asks a self-awareness question: "What kind of leader am I?", "Why do people bristle when I do X?", "Am I a control freak?", "Why can't I get through to this person?"
- The founder is struggling to reach or manage a specific person and wants to know how to adapt their approach.
- Before a hard conversation, a negotiation, a first management hire, or a period of high stress (fundraise, crisis, big deadline) where the founder's backup behavior is likely to surface.
- As the entry-point diagnostic for the leadership domain, feeding `delegation-readiness-audit`, `motivation-mapper`, and `leadership-growth-planner`.
- Onboarding a founder to the operating system, to establish a baseline leadership profile.

## When NOT to Use
- The founder wants to act *on* a specific employee — a performance conversation, a role change, comp, a PIP, hiring/firing. This skill is advisory only; route people actions to the People domain and the founder.
- The question is about delegation beliefs specifically → `delegation-readiness-audit`.
- The question is about what motivates the founder or a key employee → `motivation-mapper`.
- The founder wants a development plan and growth metrics → `leadership-growth-planner`.
- The request is clinical (mental-health, burnout as a medical matter) → do not diagnose; suggest a qualified professional.

## Required Context
Reads Business Memory: `leader` (any prior style assessment, self-described strengths/weaknesses, observed decision patterns, stress episodes), `team` (styles/behaviors of key people if already profiled — from `motivation-mapper`), `company` (stage, crisis state, current pressure level), `decisions` (recent decision patterns that reveal assertiveness/responsiveness in action). Each fact carries `source`, `confidence`, `as_of`; a self-report from six months ago under calm conditions should not be treated as the current stress profile. This skill handles the founder's own psychometric data as `restricted` — it is never exposed to employees or third parties.

## Inputs
```yaml
input:
  mode: enum(full_assessment, quick_classify, flex_advice)   # full = run both batteries; quick = classify from known behaviors; flex = advise on adapting to a target
  assertiveness_battery: [int]     # 6 items, each 1-4 (1=Less-assertive pole, 4=More-assertive pole); required for full_assessment
  responsiveness_battery: [int]    # 6 items, each 1-4 (1=Less-responsive pole, 4=More-responsive pole); required for full_assessment
  stress_rerun:                    # optional second pass "answer as you behave under pressure"
    assertiveness_battery: [int]
    responsiveness_battery: [int]
  observed_behaviors: [str]        # for quick_classify: free-text descriptions of how the founder acts
  target:                          # for flex_advice: the person/context to adapt to
    person_style: enum(Driver, Expressive, Amiable, Analytical, unknown)
    observed_behaviors: [str]      # used to infer style if person_style unknown
    context: str                   # e.g. "delivering hard feedback", "pitching a big customer"
  current_pressure: enum(low, moderate, high)   # is the founder under stress right now?
```

## Missing Information Protocol
1. Prefer to infer axis scores from `decisions` and `observed_behaviors` already in memory before asking the founder to sit a questionnaire.
2. If `mode: full_assessment` but a battery is incomplete, do not fabricate item scores — run `quick_classify` from observed behaviors instead and label the result `provisional`.
3. For `flex_advice` where the target's style is `unknown` and no behaviors are given, ask the founder ONE concise batch: "How does this person tend to behave — fast or measured, task-first or people-first?" — then classify the target on the same two axes.
4. Never assume a stress profile from a calm-state assessment; if no `stress_rerun` and no observed stress episode exists, mark `stress_style` as `inferred_from_default` (the predicted backup behavior) and say so.
5. Never present a provisional or inferred classification as a definitive verdict.

## Diagnostic Questions
Answered internally (drawn from the leadership self-awareness set):
- **Assertiveness read:** Does the founder speak fast/emphatically and initiate, or speak tentatively and wait? Do they tell or ask? Take risks and decide fast, or stay cautious? Set the pace or go along with others'?
- **Responsiveness read:** Do they show feelings openly or hide them? People-focused or task-focused in conversation? Warm/flexible or formal/disciplined? Story/opinion-oriented or fact-oriented? Animated or reserved? Seek closeness or keep distance?
- **Dominance strength:** How far is each score from the 2.5 midline? Is this a strong default or a blended, easily-flexed style?
- **Stress behavior:** How does the founder change under pressure — which of the four backup behaviors appears (Avoiding, Dictatorial, Accommodating, Attacking)?
- **Flex history:** What has the founder done when their default style isn't working? How do they know when to adjust?
- **Target read (flex mode):** How does the person I need to reach behave on the two axes, and what does their style need from me?

## Analysis Framework
The two-dimension behavioral model. A leader's default style sits on two independent axes; their intersection places the leader in one of four quadrants. Every leader is a mix of all four and defaults to one — effectiveness comes from flexing, not from perfecting the default.

- **Axis A — Assertiveness:** how much the person tries to influence/direct others. `Less ↔ More`.
- **Axis B — Responsiveness:** how much the person openly shows emotion and orients to people/relationships vs. task. `Less ↔ More`.

**Quadrant key:**

| Assertiveness | Responsiveness | Style |
|---|---|---|
| Less | Less | **Analytical** |
| More | Less | **Driver** |
| Less | More | **Amiable** |
| More | More | **Expressive** |

**Style profiles (strengths / watch-outs):**
- **Driver** (More/Less): results-driven, decisive, fast, risk-taking. Watch: impatient, poor listener, oversteps authority, can turn autocratic and squelch initiative.
- **Expressive** (More/More): high-energy, visionary, motivating, loves interaction. Watch: weak planning, acts before thinking, oversells and under-instructs, quick-tempered.
- **Amiable** (Less/More): loyal team-builder, dependable, patient, relationship-first. Watch: indecisive to avoid conflict, acquiesces while resentful, takes criticism personally.
- **Analytical** (Less/Less): precise, systematic, quality-driven, process-oriented. Watch: over-analyzes into paralysis, drowns in detail, critical, emotionally detached.

**Backup (stress) behaviors** — each default degrades predictably under stress:

| Default | Under stress |
|---|---|
| Analytical | **Avoiding** (withdraws, disengages) |
| Driver | **Dictatorial** (autocratic, controlling) |
| Amiable | **Accommodating** (gives in, acquiesces) |
| Expressive | **Attacking** (verbally aggressive, quick-tempered) |

## Calculations
- **assertiveness_score** = `mean(assertiveness_battery)` → range 1.0–4.0.
- **responsiveness_score** = `mean(responsiveness_battery)` → range 1.0–4.0.
- **Midline threshold = 2.5** on each axis.
  - `assertiveness_level = "More" if assertiveness_score >= 2.5 else "Less"`
  - `responsiveness_level = "More" if responsiveness_score >= 2.5 else "Less"`
- **primary_style** = quadrant lookup on the two levels (table above).
- **Dominance strength** = `|score − 2.5|` on each axis. **Blended flag** = true if `|assertiveness_score − 2.5| < 0.4` OR `|responsiveness_score − 2.5| < 0.4` → the leader is near a midline and flexes easily; no single style strongly dominates.
- **Stress profile:** if `stress_rerun` supplied, recompute both scores under pressure. A shift of a full quadrant (either level flips), or the appearance of the backup behavior, identifies the `stress_style`. If no rerun, `stress_style = backup_of(primary_style)` and mark `inferred_from_default`.
- No financial calculations apply.

## Decision Rules
**Classification**
- IF `assertiveness_score >= 2.5` AND `responsiveness_score < 2.5` THEN primary_style = **Driver**.
- IF `assertiveness_score >= 2.5` AND `responsiveness_score >= 2.5` THEN primary_style = **Expressive**.
- IF `assertiveness_score < 2.5` AND `responsiveness_score >= 2.5` THEN primary_style = **Amiable**.
- IF `assertiveness_score < 2.5` AND `responsiveness_score < 2.5` THEN primary_style = **Analytical**.
- IF either axis is within 0.4 of 2.5 THEN set `blended = true` and note the two closest styles.

**Self-correction (managing the founder's own blind spots)**
- IF founder is a **Driver** THEN deliberately slow down, listen, delegate authority, check that initiative isn't being squelched.
- IF founder is an **Expressive** THEN add planning/goal-setting discipline, instruct fully (don't oversell), pause before acting.
- IF founder is an **Amiable** THEN state opinions directly, make the hard decision, address conflict instead of acquiescing.
- IF founder is an **Analytical** THEN set a decision deadline to beat paralysis, cap detail-gathering, add warmth and human connection.

**Flexing to another person (flex_advice)**
- IF target is a **Driver** THEN be brief, lead with results and options, respect their time, don't ramble, let them decide.
- IF target is an **Expressive** THEN allow time to socialize, show enthusiasm, focus on big-picture/vision, recognize them publicly, don't bury them in detail.
- IF target is an **Amiable** THEN slow down, build trust and rapport first, show genuine personal interest, avoid pressure/conflict, give reassurance and support.
- IF target is an **Analytical** THEN provide data and detail, be precise and logical, give thinking time, don't push a fast decision, follow proper process.
- IF the default style is not producing the needed result from a person or situation THEN consciously flex to another style rather than pushing the default harder.

**Stress detection**
- IF founder shows **Avoiding** THEN they are a stressed Analytical → reduce load, re-engage with structured next steps.
- IF founder shows **Dictatorial** THEN they are a stressed Driver → restore delegation, invite input.
- IF founder shows **Accommodating** THEN they are a stressed Amiable → help them voice their position; protect from being steamrolled.
- IF founder shows **Attacking** THEN they are a stressed Expressive → de-escalate, give space before decisions.
- IF `current_pressure = high` THEN proactively warn the founder of their predicted backup behavior before it surfaces.

**Routing**
- IF the founder's blind spots implicate delegation/control THEN recommend `delegation-readiness-audit`.
- IF the flex target is a specific employee needing a management change THEN advise on communication style only and route the action to People + founder.

## Procedure
1. Determine `mode`. Load `leader`, `team`, `decisions` from memory and note freshness.
2. **Full assessment:** validate both batteries (6 items each, values 1–4); compute axis scores, level per axis, primary_style, dominance strength, blended flag.
3. **Quick classify:** infer axis levels from `observed_behaviors` / `decisions`; label result `provisional`.
4. Attach the style profile (strengths + watch-outs) for the primary style.
5. Determine stress_style: from `stress_rerun` if present, from an observed stress episode if in memory, else infer from default and mark `inferred_from_default`.
6. If `current_pressure = high`, foreground the backup-behavior warning and de-escalation guidance.
7. **Flex mode:** classify the target on the two axes (from `person_style` or inferred behaviors), then emit the concrete flex adjustments and "what to avoid" for that pairing plus the given context.
8. Apply self-correction rules for the founder's own style.
9. Assemble output; write/refresh the founder's leadership profile to `leader` and a baseline metric to `metrics` (L0 — internal, self-data only).
10. Route to related skills where the diagnosis points beyond style.

## Output
```yaml
output:
  primary_style: enum(Driver, Expressive, Amiable, Analytical)
  assertiveness_score: number       # 1.0-4.0
  responsiveness_score: number      # 1.0-4.0
  blended: bool                     # near-midline, flexes easily
  nearest_alternate_style: str      # relevant when blended
  confidence: enum(high, medium, low)   # lower for provisional/inferred
  strengths: [str]                  # from style profile
  growth_edges: [str]               # watch-outs
  self_correction_actions: [str]    # the founder's own blind-spot fixes
  stress_style: enum(Avoiding, Dictatorial, Accommodating, Attacking)
  stress_style_basis: enum(measured, observed, inferred_from_default)
  stress_early_warning: str         # what the founder will do under pressure + how to catch it
  flex_advice:                      # present in flex mode
    target_style: enum(Driver, Expressive, Amiable, Analytical, unknown)
    context: str
    do: [str]
    avoid: [str]
  recommended_next_skills: [str]
```

## Recommendations
Recommendations are formed by pairing the founder's default style with either their own blind spots (self-correction) or a target person's style (flex). They are prioritized by immediacy: an active high-pressure situation surfaces the stress warning first; a stuck relationship surfaces the flex advice first; otherwise the highest-leverage growth edge leads. Every recommendation is a behavioral adjustment the founder makes themselves — this skill never directs an action taken on another person.

## Execution Opportunities
- Write/refresh the founder's leadership profile in `leader` — reversible, LOW risk, internal self-data.
- Write a baseline `leadership_style` metric to `metrics` — reversible, LOW.
- Draft a personal "flex cheat-sheet" for a named upcoming interaction (founder-facing note) — reversible, LOW.
- Propose (not run) `delegation-readiness-audit`, `motivation-mapper`, or `leadership-growth-planner`.
All outputs are advisory notes to the founder; nothing is sent to or executed on any employee.

## Human Approval Requirements
- No external or irreversible action. All writes are internal self-assessment data at L0.
- Any adjustment involving a specific employee (a conversation, a role/behavior change) is advice to the founder only; the founder decides and acts, with People-domain support. Per `AUTONOMY_AND_APPROVAL_MODEL.md`, this skill's ceiling is L0 — analysis and internal notes only.

## Escalation Conditions
- **Signs of burnout, depression, or a mental-health crisis in the self-report** → do not diagnose; gently recommend a qualified professional and notify no one else.
- **A style/stress issue that is really a specific-employee conflict** → route to People domain + founder; do not advise on the individual beyond communication style.
- **Persistent Dictatorial/Attacking backup behavior harming the team** → flag as an organizational risk and recommend `leadership-growth-planner` plus, if it touches employment conduct, the People domain.
- **Low-confidence/provisional classification the founder wants to act on heavily** → recommend completing the full assessment first.

## KPIs
- Founder-reported accuracy of the classification ("this describes me").
- Whether flex advice, when applied, improved the target interaction (founder self-report or People-domain follow-up).
- Reduction in observed backup-behavior episodes over time.
- Adoption: % of recommended next-skills the founder runs.

## Monitoring
After the assessment: watch for recurrence of the predicted stress_style during known high-pressure periods and re-surface the early warning. Track whether growth edges narrow across successive assessments. Re-verify the profile on fresh evidence rather than treating a one-time result as permanent — style expression can shift with company stage and load.

## Follow-Up
- Time-triggered: re-baseline every 6–12 months, and after a major role or company-stage change.
- Event-triggered: before a high-stress period (fundraise, crisis, first senior hire), before a hard conversation, or after a leadership incident where a backup behavior clearly surfaced.

## Related Skills
Entry point for the leadership domain. Feeds `delegation-readiness-audit` (control↔trust beliefs), `motivation-mapper` (the founder's own motivators + key-people style profiles that this skill flexes toward), `leadership-growth-planner` (growth edges → development plan), and `mission-vision-builder` (leader identity informs vision). Hands specific-employee actions to the People domain.

## Guardrails
- Advisory only (L0). Never act on or communicate with a specific employee; route to People + founder.
- Treat all founder psychometric data as `restricted`; never expose it to employees or third parties.
- Never present a provisional/inferred result as definitive; always attach a confidence flag and its basis.
- The style model is a behavioral lens, not a clinical or personality diagnosis; do not pathologize, label, or use it to exclude anyone.
- Do not use style classification to justify a hiring, firing, or pay decision — that is prohibited misuse.
- On any sign of a mental-health issue, stop and refer to a professional.

## Example
**Founder input:** "I keep losing my best engineer's attention in our 1:1s. I'm a fast, get-to-the-point person and she goes quiet. Full assessment please, and help me reach her." Assertiveness battery [4,4,4,3,4,4] → 3.83; Responsiveness [2,1,2,2,1,2] → 1.67. Target described as: careful, wants the data, uncomfortable being rushed, asks lots of "why" questions.
**Reasoning:** assertiveness 3.83 (More), responsiveness 1.67 (Less) → primary_style = **Driver**; not blended (both scores far from 2.5), confidence high. Strengths: decisive, fast, results-driven. Growth edges: impatient, poor listener, can squelch initiative. Stress_style (inferred_from_default) = **Dictatorial**. Target behaviors (measured, cautious, data-seeking, process-oriented, low emotional display) → target_style = **Analytical**. Driver→Analytical flex: the founder's default (brief, fast, decide-now) is exactly what shuts an Analytical down.
**Output (abridged):** primary_style Driver; self_correction: slow down, listen, don't push a fast decision. flex_advice for context "1:1 with the engineer": do = [send the agenda and data ahead of time, give her thinking space, ask then wait in silence, follow a predictable process, be precise]; avoid = [rushing to a decision, skipping the "why", emotional pressure, ambushing her with new topics]. stress_early_warning: "Under deadline pressure you'll go Dictatorial — watch for issuing orders instead of asking; that will lose her fastest." recommended_next_skills: [motivation-mapper, delegation-readiness-audit].
**Executed vs. approval:** Wrote the leadership profile to `leader` and a baseline metric to `metrics`; drafted the founder-facing flex cheat-sheet. No message or action directed at the engineer — the founder adapts their own approach; anything structural routes to People.

## Provenance
SOURCE. Derives from the leadership domain's Two-Dimension Behavioral / Leadership Style Model (assertiveness × responsiveness, 2.5 midline, four-quadrant lookup), the Style-Shift-Under-Stress backup-behavior model, and the style-flex + self-correction + stress-detection decision rules. De-branded: the underlying instrument is described generically without citing any source book, author, or program. See `internal/PROVENANCE_MAP.md`.
