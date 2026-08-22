---
name: onboarding-builder
domain: people
version: 0.1.0
autonomy_ceiling: L2
provenance: SOURCE
reads: [team.people, team.org, company, team.culture, goals]
writes: [team.people, team.org, decisions]
related_skills: [job-description-builder, hiring-scorecard-and-fit, delegation-planner, culture-diagnostic, hr-process-coverage-audit]
owned_by_agents: [people-agent]
---

# Skill: Onboarding Builder

## Purpose
Produce a complete, tracked onboarding sequence for a specific start date: pre-start provisioning, a Day-1 plan, a first-week orientation agenda, and a full checklist driven to completion and sign-off within 3 days — plus the culture-integration layer that makes the invisible parts of the company visible to a new hire. Turns "someone starts Monday" into a runnable plan that gets them productive and connected fast.

## When to Use
- A hire is accepted and has a start date (output of `hiring-scorecard-and-fit` → founder offer → acceptance).
- Founder asks: "Set up onboarding for our new hire", "What do we need ready for day 1?", "Build a first-week plan."
- Standardizing onboarding so it isn't reinvented per hire.

## When NOT to Use
- To evaluate or select the candidate → `hiring-scorecard-and-fit`.
- To set the person's ongoing responsibilities/authority after ramp → `delegation-planner`.
- To build the standing HR onboarding *policy/process* (vs. one instance) → `hr-process-coverage-audit` / `organizational-design`.
- Any offer, comp, or employment-terms decision → founder + HR/legal.

## Required Context
- The hire's role and JD `critical_tasks` (for role-specific onboarding and 30/60/90 focus).
- `team.org` — reporting line, team members, assigned buddy candidate.
- `company.mission`/`values` and `team.culture` — for the culture-integration layer (make invisible culture visible).
- Start date, hiring manager, and the new-hire impact plan (whose work shifts; from `organizational-design`/DG1) if a hire triggers system change.

## Inputs
```yaml
input:
  new_hire:
    handle: str                      # PII referenced, not stored inline
    role: str
    employment_type: enum(FTE, PT, contractor)
    start_date: date                 # required
    work_location: str               # onsite / hybrid / remote
  hiring_manager: str                # required
  team_members: [str]                # for intros + 1:1s
  buddy: str                         # assigned peer; skill proposes one if empty
  jd_ref: str                        # for critical tasks / ramp goals
  critical_tasks: [str]
  equipment_needs: [str]             # role-specific tools
  system_impact_plan_ref: str        # from organizational-design/DG1, optional
```

## Missing Information Protocol
1. Pull role, critical tasks, team, and reporting line from memory/JD before asking.
2. If no buddy is named, propose one (a peer on the team with spare capacity) for founder confirmation.
3. If start date or hiring manager is missing, ask for those two items only — everything else is derivable.
4. **Never assume** benefits/comp details (those come from HR and require approval) and never send external welcome communications without approval.
5. For remote/hybrid, adapt physical items (keys, facility tour) to their virtual equivalents rather than assuming an office.

## Diagnostic Questions
- Is the workstation, accounts, and access provisioned before day 1? (Nothing worse than day-1 dead time.)
- Who is the buddy coordinating onboarding activities?
- Is the existing team prepped for the change (whose work shifts, how the new person is introduced)? (DG1)
- Does day 1 cover paperwork, welcome, intros, tour, and department mission/values?
- Does week 1 cover company/HR intro, benefits, safety, key admin policies, and department overviews?
- Is the culture-integration layer present — vision/mission review at company and role level, invisible-culture made visible, 1:1s with each teammate?
- Is the full checklist tracked to 3-day completion with employee + manager sign-off?
- What are the 30/60/90-day ramp goals tied to the role's critical tasks?

## Analysis Framework
Applies the onboarding procedure (P1–P5) and the full onboarding checklist (P4), with the new-hire system-impact diagnostic (DG1) and the cultural-iceberg integration layer.

1. **Pre-start preparation (P1):** workstation + equipment/supplies; provision accounts (login, email, keys/access card, ID badge — or remote equivalents); assign the buddy; prepare paperwork packet; prep the existing team (DG1).
2. **First day (P2):** HR meets the hire to complete paperwork (W-4/state tax, I-9, employee handbook), issue keys/ID, review benefits; hiring manager welcomes with co-worker intros + facility tour, buddy handoff, lunch, and department mission/values/policy overview.
3. **First-week orientation (P3, one full day in week 1):** company & HR intro (mission, functions, culture, org chart, handbook review, benefits enrollment); safety/emergency review; key admin policies (anti-harassment, pay periods, travel, security, systems/logins); department overviews with Q&A. Orientation time is paid — code timecards accordingly.
4. **Full checklist (P4):** the grouped check-off list (intro to company; new-employee paperwork; benefits & compensation; administrative procedures; key policy review; introductions & tours; acknowledgment) — completed within 3 days, signed by employee + manager, original to HR.
5. **Culture & integration layer (P5):** orientation + team introduction; a team session reviewing vision/mission/goals at company and individual-role level; make invisible culture visible; schedule 1:1s with each team member.
6. **Ramp goals:** derive 30/60/90-day goals from the JD critical tasks; hand to `delegation-planner` for authority levels as competence is demonstrated.

## Calculations
- **Checklist completion rate** = items_completed ÷ total_items (target 100% within 3 days of start).
- **Days-to-complete** = sign-off_date − start_date (target ≤ 3).
- **Provisioning readiness** = items_ready_before_start ÷ items_required_before_start (target 100% by day 0).
- **Time-to-productivity** (tracked post-onboarding) = date reaching independent performance on core critical tasks − start_date.
- No scoring; onboarding is a tracked checklist, not a rated instrument.

## Decision Rules
- IF work_location is remote/hybrid THEN replace physical items (keys, in-person tour) with virtual equivalents (access provisioning, virtual tour/intro calls) — do not skip them.
- IF no buddy is assigned THEN propose one and hold onboarding start until confirmed (the buddy coordinates the activities).
- IF the hire triggers system change (someone's work shifts) THEN require the DG1 team-prep step completed before start.
- IF paperwork includes I-9/tax/benefits THEN route those to HR — the agent tracks completion but does not collect or store the sensitive data itself.
- IF the checklist is not signed off within 3 days THEN escalate to the hiring manager (R12).
- IF any welcome/announcement is external-facing THEN hold for approval before sending.
- IF benefits/comp specifics are needed THEN source from HR (approval required); never invent them.

## Procedure
1. Confirm start date, role, hiring manager, team, and buddy (propose if empty).
2. Build the pre-start provisioning list (P1) with an owner and due date per item (all due by day 0); adapt for remote.
3. Trigger the DG1 team-prep step if the hire shifts existing work.
4. Draft the Day-1 plan (P2): paperwork (routed to HR), welcome, intros, tour, department mission/values.
5. Draft the first-week orientation agenda (P3) as a scheduled one-day session plus the week's touchpoints.
6. Instantiate the full P4 checklist grouped by category, each item a tracked task with owner + due date, targeting 3-day completion + sign-off.
7. Add the culture-integration layer (P5): vision/mission session, invisible-culture-made-visible, and 1:1s scheduled with each teammate.
8. Derive 30/60/90-day ramp goals from the JD critical tasks; hand to `delegation-planner`.
9. Create the tracked tasks/reminders; write the onboarding record to `team.people`/`decisions`; present the plan for founder/manager confirmation.

## Output
```yaml
output:
  new_hire_handle: str
  role: str
  start_date: date
  buddy: str
  pre_start_provisioning:
    - item: str                      # workstation, login, email, access, ID, equipment (or remote equivalent)
      owner: str
      due: date                      # by day 0
      status: enum(pending, ready)
  team_prep:                         # DG1
    whose_work_shifts: [str]
    introduction_plan: str
    done_before_start: bool
  day_1_plan:
    hr_session: [str]                # paperwork (routed to HR), keys/ID, benefits review
    manager_welcome: [str]           # intros, tour, buddy handoff, lunch, dept mission/values
  first_week_agenda:
    company_hr: [str]
    safety: [str]
    key_policies: [str]
    department_overviews: [str]
    paid_time_note: "orientation/paperwork counts as paid hours"
  full_checklist:                    # P4, grouped
    intro_to_company: [ {item, owner, due, status} ]
    paperwork: [ {item, owner, due, status} ]     # routed to HR
    benefits_comp: [ {item, owner, due, status} ] # sourced from HR
    admin_procedures: [ {item, owner, due, status} ]
    key_policy_review: [ {item, owner, due, status} ]
    introductions_tours: [ {item, owner, due, status} ]
    acknowledgment: { employee_signed: bool, manager_signed: bool, date: date }
  culture_integration:              # P5
    vision_mission_session: str
    invisible_culture_made_visible: [str]
    one_on_ones: [ {with: str, scheduled: date} ]
  ramp_goals:
    day_30: [str]
    day_60: [str]
    day_90: [str]
  completion_tracking:
    target_days_to_complete: 3
    completion_rate: number
    escalated: bool
  next_skills: [delegation-planner]
```

## Recommendations
Front-load provisioning so day 1 has zero dead time. Assign a buddy — onboarding runs through them. Make the invisible culture explicit (how decisions get made, what "good" looks like); new hires fail on unspoken norms more than on tasks. Drive the checklist to signed completion in 3 days and set concrete 30/60/90 ramp goals tied to real critical tasks, then hand growth to `delegation-planner`.

## Execution Opportunities
- Create the tracked provisioning + checklist tasks and calendar the Day-1/Week-1 sessions and 1:1s (reversible, LOW) — auto at L2 if granted.
- Draft internal team-prep communication (reversible, LOW) — internal; L2.
- Provision *internal, reversible, non-security-critical* accounts/access where integrations allow and policy permits (recoverable, LOW-MEDIUM) — otherwise stage as tasks for IT/HR.
- Write the onboarding record to memory (reversible, LOW).
- NOT executed: external welcome announcements, collecting/storing I-9/tax/PII, benefits enrollment, or any security-setting change.

## Human Approval Requirements
- **Any external-facing welcome/announcement requires founder approval** before sending.
- **Paperwork (I-9, tax, benefits enrollment) and any compensation detail are handled by HR** — the agent tracks completion but must not collect, store, or decide these; HR/founder own them.
- **Granting access to sensitive systems, financial tools, or security settings requires founder/IT approval** (respects the always-approve list on config/security changes).
- The hire itself and its terms were approved upstream; this skill executes onboarding only, not employment decisions.

## Escalation Conditions
- Checklist not signed off within 3 days of start → hiring manager (R12).
- Provisioning not ready by day 0 → hiring manager/IT before start.
- Any employment-eligibility (I-9) or classification question → HR professional / attorney.
- Accommodation requests or protected-class considerations during onboarding → HR/legal.
- The hire triggers unaddressed system change → `organizational-design` + founder.

## KPIs
- Onboarding completion rate and days-to-complete (target 100% ≤ 3 days).
- Provisioning readiness by day 0 (target 100%).
- Time-to-productivity on core critical tasks.
- New-hire 30/60/90-day retention and ramp-goal attainment (quality-of-hire).
- New-hire experience/engagement pulse in first 30 days.

## Monitoring
Track checklist completion and sign-off, whether 1:1s actually happen, ramp-goal progress at 30/60/90, and early engagement signals. A stalled checklist or missed 1:1s predicts poor ramp — intervene. Feed engagement signals to `culture-diagnostic`.

## Follow-Up
Runs per hire on a start date. Trigger 30/60/90-day check-ins; at each, reassess ramp and hand growing responsibilities to `delegation-planner`. Feed recurring gaps into `hr-process-coverage-audit` to formalize the standing onboarding process.

## Related Skills
`hiring-scorecard-and-fit` (upstream selection), `job-description-builder` (critical tasks → ramp goals), `delegation-planner` (post-ramp responsibilities + authority), `culture-diagnostic` (culture layer + engagement signals), `hr-process-coverage-audit` (formalize onboarding as a process).

## Guardrails
- Never collect, store, or decide sensitive employment paperwork (I-9/tax/benefits/comp) — track completion; HR owns the data. Individual data is `restricted`.
- No external welcome communication without founder approval.
- Adapt, never skip, provisioning/tour/intro steps for remote/hybrid hires.
- Enforce 3-day checklist completion + dual sign-off (R12); escalate if missed.
- Access to sensitive/financial/security systems requires founder/IT approval.
- Employment-eligibility, accommodation, or protected-class matters go to HR/legal.

## Example
**Input:** New hire (handle "H-14"), Operations Coordinator, remote, start date next Monday, hiring manager = founder, team = [Priya, Sam], no buddy named. JD critical tasks: order processing, supplier coordination, exception resolution, weekly reporting.

**Reasoning:** Remote → keys/facility tour become access provisioning + a virtual tour and intro calls. Proposed buddy = Priya (spare capacity, same function). Team prep (DG1): Priya hands off order-processing basics; introduce H-14 as owning fulfillment so the founder exits the workflow. Paperwork routed to HR (agent tracks only). Culture layer: vision/mission session + a "how we decide / what good looks like" doc to make invisible culture visible + 1:1s with Priya and Sam. Ramp goals from critical tasks: 30 = process orders independently; 60 = own supplier coordination; 90 = handle exceptions + weekly reporting at Level C (hand to `delegation-planner`).

**Output (abridged):** provisioning list (laptop, SSO login, email, tool access, shipped equipment) all due by day 0; buddy Priya; day-1 + first-week agendas (virtual-adapted); full P4 checklist as tracked tasks targeting 3-day sign-off; culture_integration with 1:1s scheduled; ramp_goals 30/60/90; next_skills: [delegation-planner].

**Executed vs. approval:** Created the tracked tasks, calendared sessions/1:1s, drafted the internal team-prep note, and staged internal account provisioning (L2). HR paperwork/benefits routed to HR; any external welcome and sensitive-system access **held for approval**.

## Provenance
SOURCE — derived from the onboarding procedure P1–P5 (pre-start prep, first day, first-week orientation, culture & integration) and the full onboarding checklist P4, the new-hire system-impact diagnostic (DG1), the onboarding-completeness rule (R12), and the cultural-iceberg "make invisible culture visible" concept in `05-people-org.md`.
