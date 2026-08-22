---
name: employment-compliance-scan
domain: legal
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [company, team, operations, finance, risks]
writes: [decisions, risks]
related_skills: [legal-escalation-router, contract-review-triage, ip-protection-audit, entity-structure-advisor, risk-diagnostic]
owned_by_agents: [legal-liaison-agent, people-agent]
---

# Skill: Employment Compliance Scan

> **THIS IS GUIDANCE, NOT LEGAL ADVICE.** Employment law is jurisdiction-specific, headcount-triggered, and changes constantly; the thresholds, statutes, and dollar amounts below are illustrative and MUST be re-verified for the business's actual state/county and the current year. This skill flags which laws likely apply, where the gaps are, and what to bring to an attorney or HR professional. It NEVER makes or executes a hiring, firing, classification, or discipline decision — every such action is an attorney/HR trigger.

## Purpose
As a business hires and grows, more employment laws attach — often silently at headcount thresholds — and misclassifying a worker or missing a policy creates real financial and legal exposure (the burden of proof for classification is on the employer). This skill maps which employment laws likely apply now, surfaces compliance gaps, checks worker classification, and routes every actual employment decision to an attorney/HR professional.

## When to Use
- The founder is hiring (especially the **first** W-2 employee), or bringing on a contractor.
- Headcount is growing and may be crossing a threshold (a new law can attach with the 15th, 20th, or 50th employee).
- The founder is hiring or has workers **remotely / across state lines**.
- The founder asks "what do I need to have in place before I hire?", "is this person a contractor or an employee?", "do I need a handbook?", "which employment laws apply to me?"
- A `risk-diagnostic` flag surfaces an employment/compliance gap.
- Before onboarding through a PEO/EOR or staffing arrangement (joint-employer risk).

## When NOT to Use
- There is an **active allegation or event** — harassment, discrimination, retaliation, a whistleblower complaint, an accommodation request, or a termination in progress → STOP and route immediately via `legal-escalation-router` to an attorney/HR; do not "scan," act.
- The founder wants the agent to **hire, fire, classify, or discipline** a specific person → never; those are attorney/HR + founder decisions.
- The question is purely about a contract's terms (not employment law) → `contract-review-triage`.
- The question is about IP/trade-secret protection of what employees can access → `ip-protection-audit`.

## Required Context
- `company`: entity_type, jurisdictions, locations, formation state.
- `team`: current headcount, roles, worker types (W-2 vs. contractor), key-person roles, turnover.
- `operations`: how work is directed/controlled (for classification), where workers physically work.
- `finance`: annual sales (some laws trigger on revenue, e.g. wage/hour), payroll.
- `risks`: existing employment/compliance entries.

## Inputs
```yaml
input:
  workforce:
    employee_headcount: int
    contractor_count: int
    states_of_operation: [str]       # where the business AND its workers are located
    remote_workers: [ {role, state, via_peo_or_eor: bool} ]
  workers_to_classify:               # optional, for classification check
    - role: str
      controls_manner_means_product: bool   # does the company control how/when/where + final product?
      serves_other_clients: bool
      sets_own_price_buys_own_tools: bool
      economically_dependent_on_us: bool
      is_former_employee_same_work: bool     # moving an employee into "contractor" = red flag
  policies_in_place:
    handbook: bool
    anti_harassment_policy_and_training: bool
    overtime_tracking: bool
    ip_assignment_agreements: bool
    ndas: bool
  event_flag: enum(none, allegation, accommodation_request, termination, whistleblower)  # if not none -> escalate
```

## Missing Information Protocol
- **Pull headcount, states, and worker types from memory** before asking.
- **If `event_flag` is anything but `none`, stop the scan and escalate immediately** — do not gather more; route to attorney/HR.
- **Ask ONE batch** for classification facts (control, other clients, pricing/tools, economic dependence) and which policies exist.
- **Never assume** a worker is a contractor (default toward employee when control exists), never assume a threshold doesn't apply, and never treat illustrative thresholds as current law. Unverified thresholds are flagged "re-verify for your state/year."

## Diagnostic Questions
- How many employees do you have right now, and in which states do you and your workers operate? (drives which laws apply)
- Is each worker correctly classified — **who controls the manner, means, and final product** of the work?
- Do you have signed agreements (employment, IC, NDA, IP-assignment) with everyone who has access to sensitive info?
- Do any workers live/work in a different state than the business? Any PEO/EOR arrangement?
- Do you have a handbook, and is it applied **consistently**?
- Are you about to hire, fire, or reclassify anyone? (if yes → attorney/HR)
- Is minimum wage (state may exceed federal) and overtime tracked; are exempt/non-exempt designations correct?

## Analysis Framework
**1. Applicable-law mapping by headcount (illustrative — re-verify).** As headcount grows, more laws attach:

| Law (illustrative) | Triggers at | Governs |
|---|---|---|
| Federal anti-discrimination (race/gender/national origin/religion) | 15+ employees | Discrimination & retaliation |
| Disability discrimination + accommodation | 15+ employees | Disability; interactive process |
| Age discrimination (40+) | 20+ employees | Age discrimination |
| Family/medical leave | 50+ within a ~75-mile radius | Protected leave |
| Wage & hour (minimum wage, overtime, classification) | 1+ employee / ~$500k annual sales | Pay; can carry personal liability |
| State civil-rights acts | often 15+ | State protected categories |
| State whistleblower acts | e.g. 10+ | Anti-retaliation |
| Workers'-comp retaliation / state minimum wage | often 1+ | Retaliation; state wage floor |
| County/city human-rights ordinances | as low as 5+ | Local protected categories |

Key principle: **re-run this scan at each hiring milestone** — new obligations attach as you grow.

**2. Worker-classification diagnostic (Right-to-Control + Economic-Realities).** More "company-control / dependence" answers → likely an **employee** (misclassification risk). Burden of proof is on the employer. A classic independent contractor runs their own business, serves the public, sets their own price, buys their own tools, controls their hours, and isn't directed by the hiring company. Moving an existing employee into a "contractor" role doing the same work is a high-risk red flag.

**3. Policy/obligation gap check.** Anti-harassment policy + training; reasonable-accommodation interactive process; wage/hour tracking (min wage, overtime, exempt/non-exempt); handbook (optional but must be applied consistently — avoid rigid progressive-discipline/raise/bonus/promotion policies that create enforceable expectations); recordkeeping (signed agreements, hour logs, compliance records).

**4. Remote/multistate check.** A remote worker is governed by the employment laws where they **live**, not where the business is based → local registration, tax withholding, benefits, and enforceable NDA/IP agreements under local law; with a PEO/EOR, confirm in writing who is the employer (day-to-day control can make you the actual/joint employer).

## Calculations
- **Headcount-threshold check:** for each law, does current headcount / annual sales meet the trigger? Output the set of applicable laws (illustrative, re-verify).
- **Distance test for leave laws:** employees within the radius that triggers family/medical leave.
- **Classification lean (qualitative score):** count of "company-control / economic-dependence" answers vs. "independent-business" answers → lean employee vs. contractor + misclassification-risk flag (any red flag → attorney review).
- **Misclassification exposure (qualitative, not quantified here):** back tax penalties (higher if willful), wage/hour liability, benefits/ERISA, NLRA, anti-discrimination coverage, tort liability — sized as high/medium, quantification deferred to professionals.
- **Compliance gap count:** required-but-missing policies/records → prioritized remediation list.
No penalty dollar amounts are computed — those are legal/accounting determinations.

## Decision Rules
- IF a worker's manner/means/final product is controlled by the company THEN treat as an **employee** (or escalate) — do not default to "contractor" for cost reasons. (SOURCE)
- IF moving an existing employee into a "contractor" role doing the same work THEN flag as a high-risk red flag → attorney review. (SOURCE)
- IF headcount (or annual sales) crosses a threshold in the mapping THEN new obligations attach: trigger a compliance review + attorney check. (SOURCE)
- IF a worker lives/works in a different state THEN apply **that** jurisdiction's employment law (registration, withholding, benefits, enforceable NDA/IP); confirm employer status if PEO/EOR. (SOURCE)
- IF `event_flag` is allegation/accommodation/termination/whistleblower THEN STOP and route to attorney/HR immediately — this is not a scan situation. (SOURCE triggers #5, #6, #8)
- IF hiring the first W-2 employee THEN run the full applicable-law + policy + recordkeeping checklist. (SOURCE)
- IF anti-harassment policy/training is missing at/above the discrimination threshold THEN flag a high-priority gap. (SOURCE)
- IF a required agreement (employment, IC, NDA, IP-assignment) is missing for someone with access THEN flag + route to `ip-protection-audit`. (SOURCE)
- IF the founder wants to hire/fire/classify/discipline a specific person THEN escalate to attorney/HR + founder — never execute. (SOURCE)
- **Default:** any hiring/firing decision, employment agreement, or classification/reclassification requires an attorney (trigger #4).

## Procedure
1. **Check `event_flag` first** — if not `none`, escalate immediately and stop.
2. **Pull workforce data** (headcount, states, worker types) from memory.
3. **Map applicable laws** by headcount/sales/geography (mark all illustrative → re-verify).
4. **Run the classification diagnostic** for any workers in question; produce a lean + red-flag list.
5. **Check policy/obligation gaps** (harassment, accommodation, wage/hour, handbook, recordkeeping).
6. **Run the remote/multistate check**; flag local-law and employer-status issues.
7. **Assemble the compliance report**: applicable-law map, gaps ranked by exposure, classification findings, and escalation items with framed questions for attorney/HR.
8. **Route triggers** via `legal-escalation-router`; add material gaps to `risks`.
9. **Log** the scan in `decisions`; set a re-scan trigger at the next hiring milestone.

## Output
```yaml
output:
  disclaimer: "Guidance only — not legal advice. Thresholds are illustrative; re-verify for your state/county and the current year with an attorney/HR professional. No employment decision is made or executed here."
  applicable_laws:
    - law: str
      trigger: str
      applies_now: bool
      basis: str                   # headcount / sales / geography
      note: "illustrative — re-verify"
  classification_findings:
    - role: str
      lean: enum(employee, contractor, unclear)
      misclassification_risk: enum(low, medium, high)
      red_flags: [str]
      protective_actions_if_contractor: [str]   # relinquish control, require invoices, written IC agreement, due diligence
  compliance_gaps:
    - gap: str
      severity: enum(high, medium, low)
      remediation: str
      needs_professional: bool
  remote_multistate_flags: [str]
  escalations: [str]               # items routed to attorney/HR + framed questions
  risk_register_entries: [ {risk, warning_metric} ]
  next_rescan_trigger: str         # e.g. "at 15th employee" / "before hiring in a new state"
  decision_record_id: str
```

## Recommendations
Gaps are prioritized by **exposure and reversibility**: misclassification of an existing worker (high exposure, employer bears the burden of proof) and missing anti-harassment policy/training at threshold outrank a nice-to-have handbook. For each gap the skill proposes the concrete remediation (adopt a written IC agreement and relinquish control; implement harassment training; set up overtime tracking; register in the worker's state) and marks whether it needs a professional. Every classification and hiring/firing decision is recommended *to* an attorney/HR, never decided by the agent. When in doubt on classification, the skill leans employee and escalates.

## Execution Opportunities
- **Produce the compliance report and gap list** — analysis, L0/L1.
- **Draft policy templates** (anti-harassment, confidentiality, at-will confirmation) *for attorney review* — reversible drafts, never adopted without counsel.
- **Create remediation tasks** (set up overtime tracking, gather signed agreements, register in a state) — reversible, LOW.
- **Add compliance gaps to `risks`** with warning metrics (e.g. `states_without_registration`, `workers_without_signed_agreement`) — reversible, LOW.
- **Record the scan** in `decisions` — reversible, LOW.
- **Never:** hire, fire, classify/reclassify, discipline, adopt a policy, or send an employment communication.

## Human Approval Requirements
Per `AUTONOMY_AND_APPROVAL_MODEL.md`, always human (founder + attorney/HR):
- Any hiring, firing, disciplinary action, or comp change (touching a specific employee's status) — never auto.
- Classifying or reclassifying a worker.
- Adopting a handbook or any employment policy.
- Any employment agreement, IC agreement, or restrictive covenant (route terms to counsel).
- Filing employment/tax registrations.
The skill prepares drafts and findings; professionals and the founder decide and execute.

## Escalation Conditions
> Per source escalation triggers, route to an attorney and/or HR professional (do not auto-execute):
- **Immediately (stop the scan):** any allegation/sign of discrimination, harassment, retaliation, or whistleblower complaint (#5); any accommodation request requiring the interactive process (#6); any termination (#8).
- **Attorney (required):** hiring/firing, employment agreements, worker classification/reclassification (#4); restrictive covenants (#3); crossing a headcount threshold (#7); hiring/operating across state lines / PEO-EOR liability (#10); any government audit (IRS/DOL/state) (#11).
- **HR professional:** policy design, handbook adoption, interactive-process handling, performance/discipline procedures.
- **CPA:** payroll tax, withholding, and multistate tax registration.
Escalation message includes: workforce snapshot, the trigger, the gap/finding, exposure size (qualitative), and the specific questions for the professional.

## KPIs
- % of workers with correct, documented classification.
- % of workers with signed agreements (employment/IC/NDA/IP-assignment).
- % of applicable required policies in place and consistently applied.
- Re-scan run at every hiring milestone / new-state hire (compliance cadence adherence).
- # of open compliance gaps by severity, trending down.
- Zero instances of the agent making/executing a hiring, firing, or classification decision.

## Monitoring
Watch headcount and geography as leading indicators: approaching a threshold (14 → 15 employees, first hire in a new state) should auto-prompt a re-scan *before* the obligation attaches. Track the compliance-gap register and any government-audit or complaint signals. Renewals of contractor engagements are re-checked for classification drift (a contractor gradually becoming economically dependent).

## Follow-Up
- **Event-triggered:** before every hire, before hiring in a new state, before onboarding a contractor, and immediately on any allegation/accommodation/termination (escalate, don't scan).
- **Milestone-triggered:** at each headcount threshold (5/10/15/20/50).
- **Periodic:** annual re-verification of thresholds and policies against current law (with counsel).

## Related Skills
- `legal-escalation-router` — routes every employment trigger and framed question to counsel/HR.
- `contract-review-triage` — for employment/IC agreement terms.
- `ip-protection-audit` — for NDA/IP-assignment coverage of workers with access.
- `entity-structure-advisor` — hiring the first employee also intersects entity/tax setup.
- `risk-diagnostic` — receives compliance gaps as scored risks.

## Guardrails
- **Guidance, not legal advice; thresholds illustrative and must be re-verified** for the state/county and year.
- **Never makes or executes a hiring, firing, classification, discipline, or comp decision** — all are attorney/HR + founder actions.
- **Any active allegation/accommodation/termination halts the scan and escalates immediately** — the agent does not analyze its way through a live employment event.
- **Classification defaults toward employee when control exists** — never toward contractor for cost reasons.
- **Policy drafts are for attorney review**, never adopted by the agent; avoid recommending rigid progressive-discipline/raise/bonus policies that create enforceable expectations.
- **Privacy:** worker identities, classification status, complaints, and health/accommodation info are highly sensitive (restricted); never place in external URLs, payloads, or shared tools, and never compile across sources beyond the task.

## Example
**Founder input:** "We're at 14 employees, about to hire our 15th, plus a designer in another state I want to pay as a 1099 contractor. Anything I need to worry about?"

**Skill reasoning:**
- `event_flag` = none → scan proceeds.
- Threshold: hiring the 15th employee likely triggers federal anti-discrimination + disability-accommodation obligations (illustrative — re-verify) → anti-harassment policy + training and an interactive-process procedure become high-priority gaps.
- Classification of the designer: founder says the company controls the manner/means and the designer works only for this business and uses company tools → lean **employee**, misclassification risk **high**; wanting 1099 "for cost" is exactly the trap; burden of proof is on the employer.
- Remote/multistate: designer in another state → that state's employment law, registration, withholding, benefits, and enforceable NDA/IP under local law.
- Policy gaps: no handbook, no harassment training, overtime tracking unclear.

**Output (abridged):**
- Applicable now (illustrative, re-verify): anti-discrimination + accommodation at 15; wage/hour already; possibly a local ordinance.
- Classification: designer leans employee — do not classify as 1099 without attorney review; if truly a contractor, relinquish control, require invoices, sign a written IC agreement.
- Gaps: adopt anti-harassment policy + training; set up an interactive-process; confirm overtime tracking; register/withhold in the designer's state.
- Escalations: 15th-employee threshold, the classification decision, and the multistate hire → attorney/HR (framed questions attached).

**Executed vs. escalation:** the skill produced the report, drafted a harassment-policy template *for attorney review*, created remediation tasks, and added `workers_without_signed_agreement` and `states_without_registration` to `risks` (reversible, L1). It **made no hiring or classification decision** and routed the classification, the threshold obligations, and the multistate hire to an attorney/HR via `legal-escalation-router`.

## Provenance
**SOURCE.** Derives from the Legal & Negotiation domain: the employment-law headcount-threshold table, the Right-to-Control and Economic-Realities classification tests and diagnostic, the prohibitions/obligations (harassment, retaliation, accommodation), the remote/multistate rules (local law governs; PEO/EOR joint-employer), the employee-handbook trade-offs, and the compliance/risk checklist — all wrapped in the source's hard escalation triggers. Thresholds/statutes are illustrative and flagged for re-verification. All source program branding removed. Guidance-only, never legal advice.
