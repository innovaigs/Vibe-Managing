---
name: delegation-planner
domain: people
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [team.people, team.org, founders, operations]
writes: [team.people, decisions]
related_skills: [founder-capacity-diagnostic, organizational-design, onboarding-builder, hiring-plan-builder]
owned_by_agents: [people-agent]
---

# Skill: Delegation Planner

## Purpose
Turn "I need someone else to own this" into a complete, executable delegation: the right authority level (A–D), the right instruction type (order/request/suggestion), and a delegation brief with responsibilities, definition-of-done, reporting cadence, and a feedback plan. Moves the founder off the critical path and develops the team by matching autonomy to proven competence and task risk.

## When to Use
- Founder asks: "Who should own this?", "How much rope do I give them?", "How do I hand this off?", "I'm doing too much of X."
- `founder-capacity-diagnostic` identified a task to offload to an existing person.
- Onboarding a person into a set of responsibilities, or promoting someone toward more autonomy.
- Recurring task currently bottlenecked on one person (often the founder).

## When NOT to Use
- If no one competent exists to receive the task → `hiring-plan-builder` (may need to hire) or accept it stays with the founder for now.
- To diagnose *whether* the founder is overloaded → `founder-capacity-diagnostic` first.
- To restructure roles/reporting lines across the org → `organizational-design`.
- Any change to a person's employment status, title, or compensation as part of "delegating" → founder + HR/legal, not this skill.

## Required Context
- `team.people` — the target person's role, `capabilities`, `responsibilities`, current `authority_level`, and demonstrated competence on this task type.
- The task itself: its risk/importance/novelty, and whether the *method* or only the *outcome* matters.
- `team.org` — reporting relationship and current span of control.
- Founder's development goal for the person (grow them vs. just get it done).

## Inputs
```yaml
input:
  task:
    name: str                        # required
    description: str
    importance: enum(low, medium, high)
    difficulty: enum(low, medium, high)
    novelty_to_person: enum(routine, somewhat_new, brand_new)
    method_criticality: enum(outcome_only, method_matters)  # safety/compliance/brand → method_matters
    is_recurring: bool
  target_person:
    person_id: str
    proven_competence_on_this_task_type: enum(none, emerging, competent, proven)
    current_authority_level: enum(A_none, B_minimal, C_medium, D_complete)
    is_new_or_new_supervisor: bool
  founder_intent:
    urgency: enum(immediate, normal, developmental)
    goal: enum(just_execute, develop_person, test_potential, buy_back_founder_time)
  reporting_preference:
    format: enum(verbal, written, either)
    detail: enum(detailed, general)
    frequency_hint: str              # optional
```

## Missing Information Protocol
1. Read the person's competence and current authority level from `team.people` before asking.
2. If competence on this specific task type is unknown, ask the founder **one question**: "Has [person] done this task type well before — never, a little, competently, or proven?" (Do not assume competence; it sets the authority level.)
3. Infer method_criticality from task type (safety/compliance/brand → method_matters) but confirm if ambiguous.
4. **Never assume** proven competence, and never grant a global authority level — authority is per task-type.

## Diagnostic Questions
- How risky/important/novel is this task, and how proven is this person on *this* task type? (The two variables that set the level.)
- Does the outcome matter more than the method, or is the method itself critical (safety/compliance/brand)? (Sets whether you specify ends or means — R4.)
- What is the founder's real intent: execute now, develop the person, test potential, or buy back time? (Shapes instruction type and level.)
- Is the person (or supervisor) new/inexperienced? (If so, don't rely on Suggestions — R13.)
- What reporting does the founder actually need — verbal/written, detailed/general, how often?
- Where can autonomy be raised next time as competence is demonstrated? (Ladder progression.)

## Analysis Framework
Applies the Delegation Setup (five elements), the Levels of Authority model (A–D), the Instruction Types model (F7), and the delegation rules (R1–R5, R13). Authority is a function of **(a) task risk/importance/novelty** and **(b) demonstrated competence + trust**.

1. **Set the five delegation elements** (before work starts): specific responsibilities; expected results (definition of done); expected reporting (what/when/how/detail); level of authority; observation + feedback plan.
2. **Select the authority level (A–D):**
   - **A – No authority:** nothing without sign-off; you hold all authority. Use for high-importance/high-difficulty/brand-new tasks or a new person; use as little as possible.
   - **B – Minimal authority:** greater latitude in action; person has a say in own goals/standards; you stay informed and can intervene.
   - **C – Medium authority:** person makes some decisions autonomously, sets own goals/plans/standards; regular status reports; consults you only on a particularly hard problem.
   - **D – Complete authority:** runs the whole assignment independently; you're removed even after completion; status report only. Target state for proven performers — buys back founder time.
3. **Select the instruction type (F7):** Orders (quick, no discussion, person already knows how — pairs with A); Requests (everyday, develops the team, invites initiative within control — pairs with B/C); Suggestions (developed/self-directed person, grows self-motivation — pairs with D). Do not use Suggestions with a new/inexperienced person or a new supervisor (R13).
4. **Means vs. ends (R4):** if outcome matters more, specify results and leave the how to the person; if method is critical, specify the how and focus feedback on adherence.
5. **Confirmation + feedback:** confirm understanding (ask the person to restate the assignment); plan early observation and feedback that is both instructive and motivating.
6. **Ladder plan:** note the competence signal that would justify moving the person up a level next time.

## Calculations
Authority-level selection matrix (risk × competence):

```
                      competence on THIS task type
risk/novelty      none        emerging      competent     proven
low               B           C             C/D           D
medium            A/B         B             C             C/D
high              A           A/B           B             C
brand-new task    A           A             B             B/C
```
- Instruction pairing: A→Orders; B→Requests; C→Requests; D→Suggestions (with R13 override: never Suggestions for new/inexperienced).
- Guiding default: "ends specified, means to discretion" unless `method_matters`.

## Decision Rules
- IF task is high-importance OR high-difficulty OR brand-new-to-person OR person is new THEN Level A + Orders/Directives; use A as little as possible. (R1)
- IF person is gaining experience but not yet proven THEN Level B (you stay informed, can intervene) or C (autonomous, regular status) + Requests. (R2)
- IF person has proven competence on this task type THEN Level D (complete authority, status-report only) + Suggestions — target state, buys back founder time. (R3)
- IF outcome matters more than method THEN specify results, leave the how to the person; IF method is critical (safety/compliance/brand) THEN specify the how and give activity/adherence feedback. (R4)
- IF the founder lacks discretionary time OR is a single point of failure on a task a competent person could own THEN delegate at the highest justified level rather than doing it. (R5)
- IF the person or supervisor is new/inexperienced THEN do not use Suggestions; use Orders/Requests until developed. (R13)
- IF no competent receiver exists THEN do not force a high level; either grant A with heavy support, or route to `hiring-plan-builder`.
- IF delegating would change the person's title/status/comp THEN that change goes to founder + HR/legal (not part of this brief).

## Procedure
1. Load the person's competence and current authority level; clarify the task's risk/novelty and method-criticality.
2. Determine authority level from the risk × competence matrix (R1–R3).
3. Select the matching instruction type (apply the R13 override).
4. Decide means vs. ends and the reporting plan (what/when/how/detail) (R4).
5. Write the delegation brief: responsibilities, expected results (definition of done), authority level (with what they decide vs. what you decide), reporting cadence/format, feedback + observation plan.
6. Add the confirmation step (person restates the assignment) and the manager follow-through checklist.
7. Note the ladder-progression signal for next time.
8. Stage the authority_level update on `team.people` (proposed) and write a `decisions` record; present the brief to the founder.

## Output
```yaml
output:
  task: str
  target_person: str
  authority_level: enum(A_none, B_minimal, C_medium, D_complete)
  authority_rationale: str           # the two variables that set it
  instruction_type: enum(order, request, suggestion)
  instruction_rationale: str
  delegation_brief:
    responsibilities: [str]
    expected_results: str            # definition of done
    decision_rights:
      person_decides: [str]
      founder_decides: [str]
    reporting:
      what: str
      cadence: str
      format: enum(verbal, written)
      detail: enum(detailed, general)
    means_vs_ends: enum(specify_results, specify_method)
    feedback_plan: str               # early observation + instructive & motivating feedback
    confirmation_step: str           # ask person to restate the assignment
  manager_followthrough_checklist: [str]  # show up to meetings, respond to reports, monitor post-feedback
  ladder_next_step:
    signal_to_raise_level: str
    next_level: enum(A_none, B_minimal, C_medium, D_complete)
  memory_update:
    person_id: str
    proposed_authority_level: enum(A_none, B_minimal, C_medium, D_complete)  # for this task type
```

## Recommendations
Default to the highest authority level the person's proven competence justifies — the point of delegation is to buy back founder time and develop people, and over-using Level A signals distrust. Specify ends, not means, unless the method is genuinely critical. Always include the confirmation step; most failed delegations fail at shared understanding, not capability.

## Execution Opportunities
- Produce the delegation brief and follow-through checklist (reversible, LOW) — L1 prepare.
- Stage the per-task authority_level update on `team.people` (reversible, LOW) — staged for approval.
- Create the reporting-cadence reminders/tasks (reversible, LOW).
- Write a `decisions` record (reversible, LOW).
- NOT executed: any title/status/comp change; any external communication.

## Human Approval Requirements
- **The founder approves the delegation and any authority-level change** before it takes effect (it changes who decides what). L1 prepare only.
- Any element that alters the person's **title, employment status, or compensation** ALWAYS requires founder approval AND HR/legal review — a delegation brief must not bundle such a change.
- Granting decision rights over money, contracts, or external commitments must respect the system-wide always-approve list (the person's authority cannot exceed what the control plane allows without founder sign-off).

## Escalation Conditions
- The task involves money movement, contracts, or legal/regulatory commitments → decision rights capped; founder (+ accountant/attorney) sets the limit.
- Delegation would touch a specific person's status/comp → founder + HR professional.
- No competent receiver exists and the task is critical → `hiring-plan-builder` + founder.
- Person repeatedly fails at the granted level → demote a level and re-plan feedback (do not escalate authority to compensate).

## KPIs
- Delegation depth: share of tasks at Level C/D vs. A/B (rising is good).
- Founder discretionary time reclaimed (the Level-D payoff).
- Task success rate post-delegation at the granted level; rework/intervention rate.
- Ladder progression: people moving up a level per task type over time.
- Span-of-control health for the delegating manager.

## Monitoring
After the brief is accepted: verify the manager shows up to the agreed reporting meetings, responds to reports, observes early, and gives the planned feedback. Watch task outcomes; if the person exceeds expectations (common with Requests), note the signal to raise the level; if they struggle, step the level down and add support.

## Follow-Up
Re-run when competence changes (raise/lower the level), when a new task type is delegated to the same person, when reporting reveals mismatch, or after `founder-capacity-diagnostic` surfaces new offload candidates. Goal over time: move most people to Level D on most routine tasks.

## Related Skills
`founder-capacity-diagnostic` (feeds tasks to delegate), `organizational-design` (roles/spans that delegation operationalizes), `onboarding-builder` (initial responsibilities + authority for a new hire), `hiring-plan-builder` (when no competent receiver exists).

## Guardrails
- Authority is per task-type and proportional to proven competence × task risk — never a blanket grant. (R1–R3)
- Under-use Level A; over-use signals distrust and starves the founder of time.
- Never use Suggestions with a new/inexperienced person or new supervisor. (R13)
- Specify ends over means unless method is safety/compliance/brand-critical. (R4)
- Decision rights cannot exceed the control plane's always-approve limits (money/contracts/legal) without founder sign-off.
- No title/status/comp change bundled into delegation — that path is founder + HR/legal.

## Example
**Founder input:** "I keep doing the weekly customer status reports myself. Maya has done them well the last two months when I was traveling. I just want them off my plate."

**Reasoning:** Task risk = low/medium, recurring; Maya's proven competence = proven on this task type; founder intent = buy_back_founder_time. Matrix (low/medium risk × proven) → Level D. Instruction type → Suggestions (Maya is experienced here; R13 does not block). Method not critical → specify results (the report standard), leave the how to Maya. Reporting = a status report only (Level D). Confirmation: ask Maya to restate the report standard and cadence.

**Output (abridged):** authority_level D_complete (rationale: proven competence, low/medium risk, founder wants time back); instruction_type suggestion; brief with responsibilities (own weekly status reports end-to-end), expected_results (report meets the existing standard, out by Friday EOD), decision_rights.person_decides (format, content emphasis, sourcing), founder_decides (nothing routine — status report only), reporting (a brief status note, weekly, written, general); feedback_plan (light-touch, review first two, then hands-off); ladder_next_step (already at D). memory_update: Maya → D_complete for "customer status reporting."

**Executed vs. approval:** Produced the brief and staged Maya's authority_level for this task type (L1). The authority change was **held for founder approval**; no status/comp change involved.

## Provenance
SOURCE — derived from the Delegation Setup five elements and Effective Delegation Checklist (W4), the Levels of Authority A–D model, the Instruction Types model (F7), and delegation rules R1–R5 and R13 in `05-people-org.md`.
