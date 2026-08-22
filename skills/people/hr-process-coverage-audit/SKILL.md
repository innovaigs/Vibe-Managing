---
name: hr-process-coverage-audit
domain: people
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [team.people, team.org, company, operations, policies]
writes: [decisions, team.org]
related_skills: [organizational-design, onboarding-builder, hiring-plan-builder, culture-diagnostic, delegation-planner]
owned_by_agents: [people-agent]
---

# Skill: HR Process Coverage Audit

## Purpose
Check which formal, documented HR procedures the business actually has versus the standard set it needs at its size and stage, and produce a prioritized gap list with escalation flags — so the company builds the people-processes that protect it (and its employees) before an incident forces the issue. Turns "we handle HR informally" into a concrete build list.

## When to Use
- Founder asks: "What HR processes do we need?", "Are we covered on HR?", "Do we have the right policies?", "What am I missing before we grow the team?"
- Growth (crossing headcount/legal thresholds), first non-founder hires, a reorg, or a near-miss incident.
- As a sub-step of `organizational-design` (process-maturity dimension) and before scaling the team.

## When NOT to Use
- To interpret which employment *laws* apply or check legal compliance specifically → route to the employment-compliance skill / attorney (this skill flags the need; it does not give legal advice).
- To handle a specific-employee matter (discipline, termination, complaint) → founder + HR/legal, immediately.
- To build one instance of onboarding → `onboarding-builder` (this skill decides whether a *standing onboarding process* exists).
- To assess lived culture → `culture-diagnostic`.

## Required Context
- Current process/policy inventory (what is documented and followed) — `policies` and founder input.
- `team.people` headcount, employment types, and `company.jurisdictions`/`stage` (size- and location-dependent obligations).
- Whether dedicated HR staff exists, or how HR is currently run.

## Inputs
```yaml
input:
  headcount: int                     # required
  employment_types: [enum(FTE, PT, contractor)]
  jurisdictions: [str]               # states/countries of employees
  has_dedicated_hr: bool
  how_hr_is_run: str                 # if no dedicated HR
  current_processes:                 # what is FORMALLY documented + followed
    - process: str
      documented: bool
      followed: bool
      owner: str
  recent_incidents: [str]            # near-misses / disputes that revealed gaps
  growth_plan: str                   # upcoming hiring that raises obligations
```

## Missing Information Protocol
1. Pull headcount, jurisdictions, and any known policies from memory before asking.
2. Ask the founder **one batched question** to inventory processes: "For each of these — recruiting, comp/benefits setting, performance evaluation, feedback, discipline, dismissal-for-cause, leave/attendance, anti-harassment/non-discrimination — do you have it *written down and actually followed*, yes or no?"
3. Distinguish "we do it informally" from "it is documented and followed" — informal = gap for audit purposes.
4. **Never assume** legal compliance from the existence of a process, and **never give legal advice**; flag legal-sensitive processes for HR/legal.

## Diagnostic Questions
(DG5 — HR-process maturity)
Does the business have formal, documented procedures for:
- Recruiting; setting salary/benefits; training; professional development; preparing the team for new hires?
- Performance evaluation (and how often); giving feedback; addressing unsatisfactory performance; dismissal for cause?
- Differentiated rewards for outstanding vs. acceptable performance; retaining top performers; handling resignations to competitors?
- Policies for sick/maternity/vacation leave, attendance, lateness, email usage?
- Non-discrimination, harassment, and workplace-violence policies?
- Is there dedicated HR staff — and if not, how is HR run?

Each "No" (or "informal only") is a process gap to build. Which gaps are legal-sensitive (discipline, termination, protected-class, leave) and must be built with HR/legal?

## Analysis Framework
Applies the HR-process maturity diagnostic (DG5), the HR lifecycle (F1), and the separation-gating rule (R11).

1. **Standard process set:** enumerate the expected HR procedures across the lifecycle (recruit → interview → hire → onboard → evaluate → delegate → develop → reward/retain → separate), plus standing policies.
2. **Coverage check:** for each, mark present (documented + followed) / informal-only / absent, and note the owner.
3. **Risk-tier each gap:** legal-sensitive (discipline, termination/dismissal-for-cause, non-discrimination, harassment, workplace violence, leave/FMLA, worker classification) vs. operational (recruiting, feedback, development, rewards, retention).
4. **Size/stage/jurisdiction trigger check:** flag processes that become *legally required* at the company's headcount or in its jurisdictions (the skill flags the trigger and routes to legal/compliance — it does not adjudicate the law).
5. **Prioritize:** by (risk exposure × likelihood-of-occurrence) and by what current growth will soon require; legal-sensitive gaps rank first.
6. **Build plan:** for each gap, name the process to build, its owner, whether it needs HR/legal, and route (onboarding → `onboarding-builder`; recruiting/selection → hiring skills; performance/reward → performance domain + founder; policies → HR/legal).

## Calculations
- **HR-process coverage %** = processes_present ÷ standard_process_set_size.
- **Legal-exposure gap count** = number of absent/informal legal-sensitive processes (weighted heaviest).
- **Gap priority** = risk_tier(1–4) × occurrence_likelihood(1–3), legal-sensitive gaps floored at high priority.
- **Trigger flags:** boolean per process for "becomes required at current/near-term headcount or jurisdiction" (routed to legal, not decided here).
- No pass/fail score; output is a ranked gap list, coverage %, and escalation flags.

## Decision Rules
- IF a process is done informally but not documented+followed THEN count it as a gap (informal processes fail under audit/dispute).
- IF a gap is legal-sensitive (discipline, termination/dismissal-for-cause, non-discrimination, harassment, workplace violence, leave/FMLA, worker classification) THEN flag it for HR professional / attorney and rank it high — it must be built with legal review (R11).
- IF a process becomes legally required at the company's headcount/jurisdiction THEN flag the trigger and route to legal/compliance; do NOT assert the legal conclusion in-skill.
- IF there is no dedicated HR AND headcount is growing past informal-management limits THEN recommend establishing an HR owner/function (build vs. outsource).
- IF a recent incident revealed a gap THEN prioritize that gap and flag any employee-specific fallout to founder + HR/legal.
- IF a gap maps to an existing Vibe Managing skill (onboarding/recruiting/selection) THEN route the build there rather than reinventing it.
- IF worker classification (contractor vs. employee) is unclear THEN flag misclassification risk to legal/compliance.

## Procedure
1. Load headcount, jurisdictions, HR ownership, and the current process inventory.
2. Enumerate the standard process set across the lifecycle + standing policies.
3. Mark coverage (present / informal / absent) and owner for each.
4. Risk-tier each gap (legal-sensitive vs. operational).
5. Run the size/stage/jurisdiction trigger check; flag legally-triggered gaps for legal.
6. Prioritize gaps (legal-sensitive first, then by risk × likelihood and growth need).
7. Build the gap-closure plan; route buildable processes to their skills and legal-sensitive ones to HR/legal.
8. Write findings to `decisions` (and process ownership to `team.org`); present the ranked gap list + escalations to the founder.

## Output
```yaml
output:
  summary: str
  coverage_pct: number
  hr_ownership:
    has_dedicated_hr: bool
    recommendation: str              # keep informal / assign owner / outsource / hire
  process_coverage:
    - process: str
      status: enum(present, informal_only, absent)
      owner: str
      risk_tier: enum(operational, legal_sensitive)
      legally_triggered: bool        # becomes required at size/jurisdiction (route to legal)
  gap_list:
    - gap: str
      risk_tier: enum(operational, legal_sensitive)
      priority_rank: int
      why_it_matters: str
      build_plan: str
      needs_hr_legal: bool
      route_to_skill: str            # onboarding-builder / hiring skills / performance / policies
  escalations: [str]                 # legal-sensitive + legally-triggered + incident items
  next_skills: [str]
```

## Recommendations
Build legal-sensitive processes first — discipline, termination, anti-harassment, non-discrimination, and leave are the gaps that create real liability, and they must be built with HR/legal, not improvised. Convert "informal" processes to documented+followed before headcount grows past the point where informality breaks. Route operational processes to the skills that already build them. Recommend a named HR owner (internal or outsourced) once the team outgrows founder-run HR.

## Execution Opportunities
- Produce the coverage audit + ranked gap list + build plan (reversible, LOW) — L1 prepare.
- Draft *operational, non-legal-sensitive* process documents (e.g. recruiting checklist, feedback cadence) for founder review (reversible, LOW).
- Create internal tasks to build/close gaps and route to the right skills (reversible, LOW).
- Write findings and process ownership to memory (reversible, LOW).
- NOT executed: publishing/adopting any policy, and NOT drafting legal-sensitive policies as authoritative — those are flagged for HR/legal.

## Human Approval Requirements
- **Adopting any HR policy or process requires founder approval**; legal-sensitive policies (discipline, termination, anti-harassment, non-discrimination, leave, classification) additionally require **HR professional / attorney review** before adoption (R11, AUTONOMY_AND_APPROVAL_MODEL §4).
- Establishing/outsourcing an HR function is a standing-configuration and spend decision → founder approval.
- This skill never resolves a specific-employee matter; any such matter is routed to founder + HR/legal.

## Escalation Conditions
- Any legal-sensitive gap, legally-triggered requirement, or worker-classification ambiguity → HR professional / attorney (R11).
- A recent incident with employee-specific or protected-class dimensions → HR/legal immediately; founder informed.
- Multi-jurisdiction employment (employees in several states/countries) → employment counsel.
- Termination/dismissal-for-cause process being invoked for a real case → attorney before acting (R11).

## KPIs
- HR-process coverage % rising toward target for the company's stage.
- Legal-exposure gap count trending to zero (with HR/legal sign-off on each).
- Time-to-close per gap; % of legal-sensitive gaps built with documented legal review.
- Reduction in HR incidents/disputes; existence of a named HR owner as the team scales.

## Monitoring
Re-audit as headcount and jurisdictions change (new thresholds trigger new required processes). Track whether "informal" processes actually get documented and followed, and whether adopted legal-sensitive policies were legal-reviewed. Watch for incidents that reveal untracked gaps.

## Follow-Up
Run at each growth threshold, before first non-founder hires, on entering a new jurisdiction, after any HR incident, and as the process-maturity input to `organizational-design`. Route each closed-gap build to its owning skill.

## Related Skills
`organizational-design` (consumes this as the process-maturity dimension), `onboarding-builder` (builds the onboarding process gap), `hiring-plan-builder`/`job-description-builder`/`interview-guide-and-scorecard` (recruiting/selection process gaps), `culture-diagnostic` (reward/recognition and non-discrimination interplay), `delegation-planner` (delegation/authority as a process).

## Guardrails
- Informal ≠ covered — a process counts only if documented and followed.
- Never give legal advice or assert a legal requirement; flag the trigger and route to HR/legal.
- Legal-sensitive processes (discipline, termination, protected-class, harassment, leave, classification) must be built with HR/legal and adopted only with founder + legal approval (R11).
- Never touch a specific-employee matter — route to founder + HR/legal.
- Do not publish/adopt any policy autonomously; prepare and route for approval.

## Example
**Input:** Headcount 8 (all FTE), employees in two states, no dedicated HR (founder runs it informally). Current processes: recruiting = informal; onboarding = absent; performance evaluation = absent; anti-harassment policy = absent; leave policy = informal; comp-setting = informal. Recent incident: an employee complained about inconsistent time-off approvals.

**Reasoning:** Coverage is low. Legal-sensitive gaps (anti-harassment/non-discrimination absent, leave informal, no documented performance/discipline process) rank first — at 8 employees across two states, several of these are approaching or past legal-requirement thresholds → flag legally_triggered and route to employment counsel (do not assert the law). Onboarding gap → route to `onboarding-builder`. Recruiting/selection gaps → route to hiring skills. The time-off incident revealed the leave-policy gap and is employee-specific in part → the policy build proceeds here; the specific complaint goes to founder + HR. Recommend assigning/outsourcing an HR owner given growth.

**Output (abridged):** coverage_pct ~0.2; hr_ownership recommendation "assign or outsource an HR owner"; gap_list ranked: [1) anti-harassment/non-discrimination policy (legal_sensitive, legally_triggered, needs_hr_legal), 2) leave/attendance policy (legal_sensitive, incident-driven), 3) performance-evaluation + discipline process (legal_sensitive), 4) onboarding process → onboarding-builder, 5) recruiting/selection → hiring skills, 6) comp-setting framework]; escalations: [anti-harassment + multi-state leave → employment counsel; time-off complaint → founder + HR].

**Executed vs. approval:** Produced the audit, ranked gap list, and drafted the operational process docs (recruiting checklist, onboarding hand-off); created build tasks (L1). All legal-sensitive policies and the HR-function decision were **flagged for HR/legal and held for founder approval**; the specific employee complaint was routed to founder + HR.

## Provenance
SOURCE — derived from the HR-process maturity diagnostic (DG5) and its full procedure list, the HR management lifecycle (F1), and the separation/termination legal-gating rule (R11) in `05-people-org.md`. Size/stage/jurisdiction trigger-flagging is handled as a routing signal to legal/compliance (no legal conclusions asserted in-skill).
