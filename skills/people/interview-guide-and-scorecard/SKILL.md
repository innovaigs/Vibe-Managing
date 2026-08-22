---
name: interview-guide-and-scorecard
domain: people
version: 0.1.0
autonomy_ceiling: L2
provenance: SOURCE
reads: [team.org.open_roles, company, team.culture, founders]
writes: [team.org.open_roles, decisions]
related_skills: [job-description-builder, hiring-scorecard-and-fit, onboarding-builder]
owned_by_agents: [people-agent]
---

# Skill: Interview Guide and Scorecard

## Purpose
Produce a behavioral interview guide and a legality-filtered A–D scorecard directly from a job description, so every interviewer probes actual past behavior against the role's real competencies and scores candidates on the same rubric. Removes hypothetical questions, interviewer improvisation, and legal exposure.

## When to Use
- A JD exists (from `job-description-builder`) and interviews are about to be scheduled.
- Founder asks: "What should I ask candidates for this role?", "Build me an interview guide/scorecard."
- Standardizing interviews across multiple interviewers or rounds.

## When NOT to Use
- To create the JD itself → `job-description-builder` (run it first; this skill needs its critical tasks and values).
- To score an actual candidate after the interview → `hiring-scorecard-and-fit` (this skill produces the blank instrument; that one applies it).
- Any performance review of an existing employee → out of scope (performance domain).

## Required Context
- The JD's `critical_tasks` (each with its mapped competency) and `values_sought` — the backbone of the guide.
- `company.mission`/`values` — for the mission-alignment question.
- Jurisdiction (from `company.jurisdictions`) — for the legality filter on protected classes.

## Inputs
```yaml
input:
  job_description_ref: str           # from job-description-builder, required
  critical_tasks:                    # pulled from the JD if not passed
    - id: str
      task: str
      competency: str
  values_sought: [str]
  competency_areas: [str]            # e.g. Values, Technical, Results, Business Acumen, Interpersonal, Leadership
  interview_rounds: int              # optional; default 1
  interviewers: [str]                # optional; for guide distribution
  jurisdiction: str                  # for legality filter
```

## Missing Information Protocol
1. Pull critical tasks, competencies, and values directly from the JD before asking anything.
2. If no JD exists, **stop and run `job-description-builder` first** — do not invent competencies.
3. If competency areas are unspecified, default to the standard set (Values, Technical, Results, Business Acumen, Interpersonal, Leadership) plus one question per critical task.
4. **Never assume** it is acceptable to ask a non-job-related or protected-class question; when in doubt, drop and flag.

## Diagnostic Questions
- Does every critical task have at least one behavioral question probing past performance on it? (F5 ladder)
- Is each question mapped to a named competency? (No orphan questions.)
- Is any question hypothetical ("what would you do")? → convert to past-behavior ("tell me about a time you did"). ("Stay out of the woulds.")
- Does any question risk a discrimination claim or touch a protected class? → drop and route to legal (R7).
- Does the guide include a values/integrity probe and a mission-alignment probe? (F2 intangibles + F3 fit)
- Is the scorecard consistent A–D per question with a single overall rating scale?

## Analysis Framework
Applies the Interview Guide + Scorecard generator (W2), the behavioral-interviewing ladder (F5), the question bank, and the interviewing DON'Ts / legality rule (R7).

1. **Competency coverage matrix** — list every competency (from JD critical tasks + standard areas + values) down the left; ensure each has ≥1 question.
2. **Behavioral question selection** — for each competency, select a question from the bank (below) or construct one using the F5 ladder against a critical task. All questions ask for *past behavior*.
3. **Per-critical-task probe** — for each critical task, apply the ladder: "This role requires [X]. Have you done that? Describe how. Describe a success. Describe a challenge and how you solved it."
4. **Values & fit probes** — include an integrity/values question and a mission-alignment question (screen fit against goals/values, not similarity — see `hiring-scorecard-and-fit`).
5. **Legality filter** — remove any question that is not clearly job-related or touches a protected class; flag removed items.
6. **Scorecard construction** — grid: Criterion | Question | Behavior/Evidence notes | Score A–D; plus overall rating scale and comments field.

### Behavioral question bank (select and adapt; all past-behavior)
| Competency | Question |
|---|---|
| Values / integrity | "Tell me about a time you were on the wrong side of an issue — what did you do, or not do?" |
| Values / ethics | "Describe a decision where you had to choose between what was easy and what was right." |
| Technical skill + coachability | "What are your technical strengths, and where are you actively developing?" |
| Technical depth | "Walk me through a technical problem you solved that you were proud of." |
| Results ownership | "What have your accomplishments been? Were you solely responsible, or was it shared?" |
| Drive for results | "Describe a goal you set for yourself and how you tracked and hit it." |
| Business acumen | "What are three challenges facing this industry, and who are the main competitors?" |
| Interpersonal / self-awareness | "Identify three skills you bring to working with others, and your areas for development." |
| Leadership / execution | "Tell me about a team you managed and how you kept them on track to finish." |
| Leadership under conflict | "Describe a time you managed conflict or strongly opinionated people on a team." |
| Role-specific (per critical task) | "This role requires [task X]. Have you done that? Describe how, a success, and a challenge you solved." |
| Life-long learner | "Tell me about the last new skill you taught yourself and why." |
| Coachability | "Describe feedback that was hard to hear and what you did with it." |
| Motivation (job vs. career) | "What draws you to this role — is this a job for now or a career direction?" |
| Culture/values alignment | "What about our mission or purpose resonates with you, and why?" |
| Decision/risk style | "Describe how you make decisions and assess risk when the answer isn't obvious." |
| Initiative | "Tell me about a time you took initiative beyond what was asked." |
| Collaboration | "Describe a time you collaborated across teams or with a difficult stakeholder." |
| Relationship-building | "Tell me about a long-term relationship you built and sustained." |

## Calculations
Scoring is ordinal, not numeric:
- **Per-question score:** A / B / C / D (A strongest evidence of the competency → D weakest/absent). Convention from the source scorecard.
- **Overall rating scale:** Highly Recommend / Acceptable / Acceptable with Reservations / Unacceptable.
- No weighted average is imposed here; the applied scoring (weighting, must-pass competencies) is decided in `hiring-scorecard-and-fit`. This skill defines the rubric and the anchors.

## Decision Rules
- IF a question is hypothetical ("would you") THEN rewrite it as past-behavior ("tell me about a time you did"). (R6)
- IF a question is not clearly job-related OR touches a protected class (age, race, religion, national origin, sex/gender, pregnancy, disability, marital/family status, etc.) THEN drop it and add to `legal_flags` (R7).
- IF a critical task lacks a question THEN add one via the F5 ladder before finalizing (full coverage required).
- IF the founder wants to discuss future compensation or imply job security in the guide THEN exclude it (interviewing DON'Ts).
- IF multiple rounds THEN distribute competencies across rounds (e.g. values + role-specific early; leadership + business acumen later) and carry flagged "probe further" items forward.
- IF a competency is must-pass for the role THEN mark it as a gating criterion on the scorecard for the applying skill to honor.

## Procedure
1. Load the JD's critical tasks, competencies, and values (or stop and invoke `job-description-builder`).
2. Build the competency coverage matrix.
3. Select/adapt a behavioral question for each competency and each critical task (F5 ladder).
4. Add the integrity and mission-alignment probes.
5. Run the legality filter; drop and flag any non-compliant question.
6. Sequence questions (and split across rounds if applicable).
7. Construct the scorecard grid (Criterion | Question | Evidence | A–D) + overall rating scale + comments field; mark must-pass criteria.
8. Assemble the interviewer-ready guide (with reminders: stay behavioral, take evidence notes, DON'Ts).
9. Save to memory; write a `decisions` record; hand the scorecard forward to `hiring-scorecard-and-fit`.

## Output
```yaml
output:
  role_title: str
  interview_guide:
    - round: int
      questions:
        - id: str
          competency: str
          question: str              # behavioral, past-tense
          maps_to_critical_task: str # "" if general competency
          followups: [str]           # ladder probes: success, challenge, resolution
  scorecard_template:
    scale_note: "A strongest evidence … D weakest/absent"
    rows:
      - criterion: str
        question_id: str
        evidence_notes: ""           # filled during interview
        score: ""                    # A|B|C|D, filled during interview
        must_pass: bool
    overall_rating_options: [Highly Recommend, Acceptable, Acceptable with Reservations, Unacceptable]
    comments: ""                     # strengths, concerns, what to probe next round
  interviewer_reminders: [str]       # stay behavioral; take evidence; DON'Ts
  legal_flags: [str]                 # questions removed and why
  coverage_check:
    all_critical_tasks_covered: bool
    all_competencies_covered: bool
```

## Recommendations
Keep every question behavioral and mapped to a competency; a guide that can't tie a question to a task shouldn't include it. Front-load values and role-specific probes. Give interviewers the DON'Ts and the evidence-note habit — the scorecard is only as good as the behavioral evidence captured under it.

## Execution Opportunities
- Generate and store the interview guide + blank scorecard (reversible, LOW) — auto at L2 if granted.
- Distribute the guide to named interviewers internally (recoverable, LOW) — internal share; L2.
- Write a `decisions` record (reversible, LOW).
- NOT executed: making offers, promises, or any candidate-facing commitment.

## Human Approval Requirements
- **The legality filter's judgments must be reviewed by founder + HR/legal before the guide is used** whenever any `legal_flags` exist or the role is in a sensitive category — protected-class exposure always escalates.
- Any deviation the founder requests that reintroduces a non-job-related or comp/guarantee question requires explicit founder acknowledgment and is still routed to legal.
- Employment decisions that follow (offers, rejections) always require founder approval (handled downstream).

## Escalation Conditions
- Any question near protected-class territory, or uncertainty about local employment/interview law → HR professional / attorney (R7).
- Role involves regulated screening (background/credit/health checks) → legal/compliance before including.
- Founder insists on a non-compliant question → escalate; do not include it.

## KPIs
- 100% coverage: every critical task and competency has a behavioral question.
- Zero non-compliant questions reaching the interview.
- Inter-interviewer scoring consistency (variance on shared candidates).
- Downstream signal: quality-of-hire for roles interviewed with this guide vs. without.

## Monitoring
Track which questions actually discriminate strong from weak candidates and which are noise; retire low-signal questions. Watch for interviewers drifting into hypotheticals or off-script (bias/legal risk).

## Follow-Up
Re-run when the JD changes, when a round reveals a competency gap to probe deeper, or when interview law/jurisdiction changes. Always precedes `hiring-scorecard-and-fit`.

## Related Skills
`job-description-builder` (supplies critical tasks/values), `hiring-scorecard-and-fit` (applies the scorecard to real candidates, blocking affinity bias), `onboarding-builder` (uses the same competency map for ramp goals).

## Guardrails
- Behavioral only — never hypothetical ("stay out of the woulds," R6).
- Every question job-related and competency-mapped; drop and flag anything protected-class-adjacent (R7).
- Never include future-comp discussion or employment-guarantee language (interviewing DON'Ts).
- The scorecard defines evidence-based A–D scoring; it does not license similarity-based "gut feel" (affinity bias is blocked in the applying skill).
- Any legal flag halts external use until HR/legal clears it.

## Example
**Input:** JD for "Operations Coordinator" with 4 critical tasks (order processing, supplier coordination, exception resolution, weekly reporting) and values [reliability, ownership, collaboration].

**Reasoning:** Built one behavioral probe per critical task via the F5 ladder (e.g. "This role requires resolving delivery exceptions. Tell me about a time you did — a success, and a challenge you solved."). Added values/integrity ("wrong side of an issue"), mission-alignment, coachability, and collaboration probes. Founder had suggested "Do you have young kids who might affect your schedule?" — dropped as protected-class (family status) and added to legal_flags. Scorecard grid built with must-pass = reliability + exception-resolution.

**Output:** Single-round guide, 9 questions across the 4 tasks + 5 competencies, each with ladder follow-ups; blank A–D scorecard with two must-pass rows; interviewer reminders; legal_flags: ["removed family-status question — protected class"].

**Executed vs. approval:** Guide + scorecard stored and shared to the interviewers (L2). Because a legal flag existed, the guide was routed to founder + HR review before first use.

## Provenance
SOURCE — derived from the Interview Guide + Scorecard generator (W2), the behavioral-interviewing ladder and "stay out of the woulds" rule (F5, R6), the reconstructed question bank, the A–D scoring convention and Highly Recommend/Acceptable/… rating scale, and the interviewing DON'Ts + question-legality rule (R7) in `05-people-org.md`.
