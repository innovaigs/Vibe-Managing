---
name: job-description-builder
domain: people
version: 0.1.0
autonomy_ceiling: L2
provenance: SOURCE
reads: [team.org.open_roles, company, goals, team.culture, founders]
writes: [team.org.open_roles, decisions]
related_skills: [hiring-plan-builder, interview-guide-and-scorecard, hiring-scorecard-and-fit, onboarding-builder, organizational-design]
owned_by_agents: [people-agent]
---

# Skill: Job Description Builder

## Purpose
Turn an approved hiring need into a structured, defensible job description whose critical tasks, competencies, and values become the single source of truth for interviewing, scoring, and onboarding. A well-built JD is what makes downstream behavioral interviewing (one question per critical task) possible.

## When to Use
- A role has been approved (via `hiring-plan-builder` or founder decision) and needs to be specified before posting or interviewing.
- Founder asks: "Write a job description for a…", "What should this role own?", "Turn this need into a role."
- Re-scoping an existing role whose responsibilities have drifted.

## When NOT to Use
- To decide *whether* or *when* to hire, or affordability → `hiring-plan-builder`.
- To generate interview questions or the scorecard → `interview-guide-and-scorecard` (this JD feeds it).
- To restructure who owns what across the whole team → `organizational-design`.
- To describe a specific person's current job for a performance review → out of scope (performance domain).

## Required Context
- The approved role from `team.org.open_roles` (title, function, reason, reports_to).
- `company.mission`, `company.vision`, `company.values` — to embed purpose and target values in the JD (recruiting lens F4.1).
- `goals` — what the role must help achieve, to derive critical tasks.
- `team.org` structure — who it reports to and interfaces with.
- `team.culture.stated_values` — the values the role is screened against.

## Inputs
```yaml
input:
  role_title: str                    # required
  reports_to: str                    # role/person id, required
  function: str                      # e.g. sales, operations, finance
  business_context: str              # vision + why this role exists
  role_purpose_hint: str             # optional founder one-liner
  goals_the_role_serves: [str]
  critical_tasks_hint: [str]         # optional; skill will expand/refine
  work_arrangement:
    location: str                    # onsite / hybrid / remote
    employment_type: enum(FTE, PT, contractor)
    schedule: str
  known_constraints: [str]           # certifications/licenses legally required
  is_trainable_role: bool            # if unknown, skill infers (recruiting lens F4.2)
```

## Missing Information Protocol
1. Derive critical tasks from `goals_the_role_serves` + function norms before asking.
2. Pull mission/values from `company`; pull reporting line from `team.org`.
3. If purpose or critical tasks are still unclear, ask the founder **one batched question**: "What are the 3–5 things this person must own for the role to be a success, and who do they report to?"
4. **Never assume** a specific required credential/license (legal risk if it screens out protected groups without job justification), a compensation figure (do not include future comp per interviewing DON'Ts), or requirements not tied to a critical task.

## Diagnostic Questions
- What is the one-line purpose of this role — the outcome it exists to produce?
- What are the 3–7 critical tasks that, if done well, make this role successful?
- For each critical task, what competency (skill/behavior) does it demand? (This mapping drives the interview.)
- Which qualifications are truly *required* vs. merely *desired*? Is each required item actually necessary to perform a critical task, or an unexamined assumption? (Bias check, F4.3)
- Is this a role that can be trained for? If so, widen requirements to trainable candidates and under-tapped pools (F4.2, R10).
- Which company values must this person share, and how would each show up in behavior?
- Does any requirement risk excluding capable people without job justification (affinity/credential bias)?

## Analysis Framework
Applies the Job Description Builder worksheet (W1) plus the recruiting-strategy lenses (F4) and the visible/intangible/fit selection model (F2).

1. **Purpose statement** — one sentence: what the role produces and why it matters to the vision.
2. **Critical tasks & responsibilities** — 3–7 concrete, observable tasks the role owns (verbs + outcomes). These are the backbone; each becomes a behavioral interview probe.
3. **Competency mapping** — for each critical task, name the required competency (technical, results, business acumen, interpersonal, leadership, role-specific).
4. **Required vs. desired qualifications** — split into: technical skills, academic/credentials (only if job-justified), experience (only if not trainable), plus intangibles (coachability, learner orientation, values). Apply the bias check to every "required" line.
5. **Values sought** — 3–5 company values the role is screened for, each expressed as an observable behavior.
6. **Purpose & culture framing** — embed mission/purpose language so the posting attracts values-aligned candidates (F4.1).
7. **Legality pass** — remove anything not job-related or near protected-class territory; keep every requirement tied to a task.

## Calculations
None. (This is a specification skill; downstream scoring lives in `interview-guide-and-scorecard` and `hiring-scorecard-and-fit`.)

## Decision Rules
- IF a requirement is not tied to a named critical task THEN drop it or move it to "desired." (Prevents credential/affinity bias.)
- IF the role is trainable THEN express experience as "desired," widen the pool, and note under-tapped sourcing (R10, F4.2).
- IF a proposed requirement touches a protected class or is not clearly job-related THEN remove it and flag for legal review (R7).
- IF a critical task exists THEN it MUST have a mapped competency (so the interview can probe it) — no orphan tasks.
- IF the founder requests future compensation language or an employment-guarantee phrase THEN refuse to include it (interviewing DON'Ts) and note why.
- IF fewer than 3 or more than 7 critical tasks emerge THEN reconcile: split an overloaded role or consolidate a thin one, and flag to `organizational-design` if the role is mis-scoped.

## Procedure
1. Load the approved role, mission/values, goals, and reporting line.
2. Draft the one-line purpose statement.
3. Enumerate 3–7 critical tasks (verb + outcome); confirm each with the founder if ambiguous.
4. Map each critical task to its required competency.
5. Build required vs. desired qualifications; run the bias check on every "required" line; mark trainable roles.
6. Select 3–5 target values with observable behaviors.
7. Add purpose/culture framing for the posting.
8. Run the legality pass (R7); flag anything routed to legal.
9. Assemble the structured JD; write it to `team.org.open_roles` (as the role's spec) and a `decisions` record.
10. Hand the JD to `interview-guide-and-scorecard`.

## Output
```yaml
output:
  job_title: str
  reports_to: str
  function: str
  employment_type: enum(FTE, PT, contractor)
  location_arrangement: str
  purpose_statement: str             # one sentence
  critical_tasks:
    - id: str
      task: str                      # verb + outcome
      competency: str                # the competency it demands (feeds interview)
  qualifications:
    required:
      technical: [str]
      credentials: [str]             # only if job-justified
      experience: [str]              # trimmed/omitted if trainable
      intangibles: [str]             # coachability, learner orientation
    desired: [str]
  values_sought:
    - value: str
      observable_behavior: str
  posting_blurb: str                 # mission/purpose framing for candidates
  is_trainable_role: bool
  sourcing_notes: [str]              # widened pools if trainable (F4.2)
  legal_flags: [str]                 # anything routed to legal review
  source_of_truth_for: [interview-guide-and-scorecard, hiring-scorecard-and-fit, onboarding-builder]
```

## Recommendations
Keep critical tasks to 3–7, each observable and outcome-oriented. Bias every "required" qualification toward what a critical task actually demands; move the rest to "desired." Lead the posting with purpose to attract aligned candidates. Flag, don't guess, on any credential that could be a legal exposure.

## Execution Opportunities
- Write/refresh the role spec in `team.org.open_roles` (reversible, LOW) — auto at L2 if granted.
- Produce a posting-ready blurb draft (reversible, LOW).
- Write a `decisions` record (reversible, LOW).
- **Publishing the job posting externally is NOT executed here** — external publication is external-facing and requires founder approval.

## Human Approval Requirements
- **Publishing the JD externally (job boards, careers page, recruiter) requires founder approval** — external-facing content.
- Any legally-flagged requirement must be **approved by founder after HR/legal review** before it appears in a live posting.
- Including any compensation range in a live posting requires founder approval (and, where a jurisdiction mandates pay transparency, legal review).

## Escalation Conditions
- A requirement touches a protected class or is not clearly job-related → HR professional / attorney before publishing (R7).
- A required license/certification's legitimacy is uncertain → legal/compliance.
- The role appears mis-scoped or overlaps another person's job → `organizational-design` + founder.

## KPIs
- Downstream usability: every critical task maps cleanly to an interview question and an onboarding item.
- Applicant quality and pool diversity (did purpose framing + widened sourcing improve the pool?).
- Reduced mis-hire rate for roles specified with this skill (via 90/180-day quality-of-hire).
- Zero legally non-compliant requirements reaching a live posting.

## Monitoring
After posting (once approved), watch applicant volume/quality and whether any requirement is filtering out strong candidates unnecessarily (bias signal). Feed learnings back into the JD.

## Follow-Up
Re-run when the role's responsibilities drift, when the pool is weak (re-scope requirements/sourcing), or when the org is restructured. Always precedes `interview-guide-and-scorecard`.

## Related Skills
`hiring-plan-builder` (supplies the approved role), `interview-guide-and-scorecard` (consumes the JD), `hiring-scorecard-and-fit` (uses the values), `onboarding-builder` (uses critical tasks for role-specific onboarding), `organizational-design` (if the role is mis-scoped).

## Guardrails
- Every requirement must be job-related and tied to a critical task; no credential/affinity bias.
- Never include future compensation promises or employment-guarantee language (interviewing DON'Ts).
- Route protected-class-adjacent or non-job-related requirements to legal (R7); do not publish them.
- Do not publish externally without founder approval.
- Prefer trainable-role framing and widened pools where the role permits (R10).

## Example
**Input:** Approved role "Operations Coordinator," reports to Founder, function operations, exists to free the founder from fulfillment and keep on-time delivery ≥95%.

**Reasoning:** Purpose = "Own day-to-day order fulfillment so delivery is on time and the founder is out of the workflow." Critical tasks derived from the goal: (1) process/track orders end-to-end → competency: process discipline / results ownership; (2) coordinate with suppliers → business acumen / relationship-building; (3) resolve delivery exceptions → problem-solving; (4) report weekly on delivery metrics → communication. Role is trainable → experience moved to "desired," sourcing widened to under-tapped pools. Founder wanted "degree required" — bias check: no critical task requires a degree → moved to "desired," legal exposure avoided.

**Output (abridged):** Purpose statement + 4 critical tasks each with a mapped competency + required intangibles (coachability, reliability) + 3 values with observable behaviors + purpose-led posting blurb + sourcing notes + legal_flags: ["removed unjustified degree requirement"].

**Executed vs. approval:** Wrote the role spec and posting blurb draft to memory (L2). External posting held for founder approval.

## Provenance
SOURCE — derived from the Job Description Form worksheet (W1), the visible/intangible/fit selection model (F2), the recruiting-strategy lenses including purposeful-careers and bias-check (F4), the trainable-vs-experienced rule (R10), the question-legality rule (R7), and the interviewing DON'Ts in `05-people-org.md`.
