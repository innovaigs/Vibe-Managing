---
name: legal-escalation-router
domain: legal
version: 0.1.0
autonomy_ceiling: L0
provenance: SOURCE
reads: [company, team, finance, operations, market, risks, decisions]
writes: [decisions, risks]
related_skills: [contract-review-triage, employment-compliance-scan, ip-protection-audit, entity-structure-advisor, crisis-response-planning, risk-diagnostic]
owned_by_agents: [legal-liaison-agent]
---

# Skill: Legal Escalation Router

> **THIS IS GUIDANCE, NOT LEGAL ADVICE.** This skill decides whether a question or proposed action requires a qualified attorney (or other professional) and frames the question for them. It NEVER answers the legal question itself, NEVER drafts a legal position, and NEVER authorizes a legal commitment. Its default is to escalate when in doubt.

## Purpose
Be the gatekeeper between the founder's everyday questions and a lawyer's desk. For any legal-ish question or proposed action, decide whether it must go to counsel (or a CPA/HR professional), and if so, package it so the professional meeting is fast and cheap: the situation, what's known, the specific decision needed, and the framed question. This is how Vibe Managing keeps agents from ever generating something that reads as legal advice or executing a legal commitment.

## When to Use
- Any time a founder asks a legal-flavored question ("can I...", "is it legal to...", "do I need a lawyer for...") or proposes an action with legal, tax, IP, employment, or contractual dimensions.
- As the mandatory hand-off point from the other legal skills (`contract-review-triage`, `employment-compliance-scan`, `ip-protection-audit`, `entity-structure-advisor`) once they hit a trigger.
- When any agent (risk, finance, people, sales, ops) surfaces something that might carry legal exposure and needs a yes/no on "does this need a lawyer?"
- Before executing anything that could be a binding commitment, filing, or protected-class-affecting action.

## When NOT to Use
- The matter is a full contract triage, compliance scan, IP audit, or entity comparison → run the specific skill first; it will route back here at the trigger. (This skill is the router, not the analyzer.)
- The matter is a live crisis with a legal dimension → `crisis-response-planning` stabilizes; this skill routes the legal substance.
- There is no legal/tax/IP/employment dimension at all → no escalation; return "no legal trigger" so the owning agent proceeds normally.

## Required Context
- `company`: entity, jurisdictions, stage — shapes which triggers apply.
- `team` / `finance` / `operations` / `market`: enough to describe the situation accurately to counsel (headcount, contract value, worker arrangement, IP at stake, regulatory context).
- `risks`: whether this connects to a scored risk.
- `decisions`: prior related decisions and any prior counsel guidance (so the founder doesn't re-pay for the same question).
- Any relevant professional contacts on file (attorney, CPA, HR) — to name the escalation target; if none, recommend engaging one.

## Inputs
```yaml
input:
  matter:
    question_or_action: str          # the founder's question or the proposed action
    proposed_by: enum(founder, agent) # who wants to act
    is_action: bool                  # true = about to DO something; false = a question
    reversibility: enum(reversible, recoverable, irreversible)
    financial_exposure: number       # $ at stake, if any
    time_pressure: enum(none, days, urgent)
  signals:                           # any that apply (drives trigger matching)
    contract_or_signing: bool
    entity_or_ownership: bool
    restrictive_covenant: bool       # non-compete/non-solicit/NDA
    hiring_firing_classification: bool
    discrimination_harassment_retaliation: bool
    accommodation_request: bool
    headcount_threshold_crossed: bool
    termination: bool
    ip_theft_or_infringement: bool
    multistate_or_remote: bool
    litigation_audit_subpoena_regulatory: bool
    ip_registration: bool
    tax_question: bool
    founder_uncertain_with_exposure: bool
  known_professionals: {attorney: bool, cpa: bool, hr: bool}
```

## Missing Information Protocol
- **Match triggers from the signals and memory first** — most escalation decisions can be made from the situation without more input.
- **Ask ONE batch** only to disambiguate whether a trigger truly applies (e.g. "is this binding?", "does the company control how the work is done?", "which state does the worker live in?").
- **Never assume no trigger applies** to avoid escalating — the default is to escalate when in doubt. If a signal is unclear, treat it as present.
- **Never answer the underlying legal question** to "save" an escalation, and never estimate legal outcomes.

## Diagnostic Questions
- Is this a *question* or an *action about to be taken*? If an action, is it reversible, and what's the financial/liability exposure?
- Does it touch any of: contracts/signing, entity/ownership, restrictive covenants, hiring/firing/classification, discrimination/harassment/retaliation, accommodation, a headcount threshold, termination, IP theft/infringement, multistate/remote work, litigation/audit/subpoena/regulatory, IP registration, or tax?
- Is the founder uncertain about something that carries financial, tax, or liability exposure?
- Is there time pressure that could push the founder to act without counsel? (If so, the escalation is more urgent, not less.)
- Is there an existing attorney/CPA/HR to route to, or must one be engaged?

## Analysis Framework
**Match against the Legal Escalation Trigger list (SOURCE — the matter must STOP and route to counsel when any is present):**
1. Drafting, signing, or materially amending any binding contract, lease, loan, or personal guarantee.
2. Choosing/changing entity structure, ownership %, or drafting operating/partnership/shareholder agreements.
3. Drafting or enforcing restrictive covenants (non-compete, non-solicit, NDA).
4. Any hiring/firing decision, employment agreement, or classifying/reclassifying a worker.
5. Any allegation or sign of discrimination, harassment, retaliation, or a whistleblower complaint.
6. Any accommodation request (religious or disability) requiring the interactive process.
7. Crossing an employment-law headcount threshold.
8. Termination of an employee.
9. Suspected trade-secret theft or IP infringement (yours or against you) — speed matters.
10. Hiring/operating across state lines or with remote workers.
11. Any litigation, demand letter, government audit (IRS/DOL/state), subpoena, or regulatory inquiry.
12. IP registration (trademark/copyright/patent) filings.
13. Anything the founder is uncertain about that carries financial, tax, or liability exposure.

**Then classify urgency and target:**
- **Urgency:** urgent (litigation/subpoena/audit, suspected IP theft, imminent irreversible signing, active allegation) vs. standard.
- **Target:** attorney (most triggers), CPA/tax professional (entity tax, tax questions), HR professional (policy/interactive-process/discipline, alongside attorney for protected-class or termination matters), or founder (the actual decision, always).
- **Verdict:** `escalate_required` (a trigger fired), `escalate_recommended` (no hard trigger but exposure/uncertainty warrants it), or `no_trigger` (proceed).

**Default rule:** when in doubt, frame the question and escalate — never generate content that reads as legal advice or a final legal position.

## Calculations
**None as legal determinations.** The only scoring is a **routing decision**: (triggers matched) → escalate_required; (no hard trigger but irreversible or financial_exposure above a business-set threshold or founder uncertain) → escalate_recommended; (else) → no_trigger. Urgency is set by the presence of an urgent trigger or imminent irreversible action. No legal risk, damages, or outcome is computed.

## Decision Rules
- IF any trigger #1–#13 is present THEN verdict = **escalate_required**; do not answer the legal question or execute the action. (SOURCE)
- IF the matter is **urgent** (litigation/subpoena/audit #11, suspected IP theft #9, active allegation #5, imminent irreversible signing #1) THEN escalate **immediately** and advise the founder not to act/respond before counsel. (SOURCE)
- IF the action is **irreversible** OR financial_exposure exceeds the business threshold OR the founder is uncertain with exposure (#13) THEN escalate (required or recommended). (SOURCE)
- IF the matter is tax/entity THEN route to a **CPA/tax professional** (and attorney for entity/agreements). (SOURCE)
- IF the matter is protected-class, termination, discipline, or interactive-process THEN route to **HR professional + attorney**. (SOURCE)
- IF no `known_professionals` exist for the needed type THEN recommend engaging one before proceeding — do not let the agent substitute. (SYNTHESIZED)
- IF time_pressure is pushing the founder to act without counsel THEN treat urgency as **higher**, not lower — never let a deadline justify skipping escalation. (SOURCE — never auto-execute legal commitments)
- IF **no** trigger and no material exposure THEN verdict = **no_trigger**; return control to the owning agent to proceed. (SYNTHESIZED)
- **Always:** the agent frames the question; it never provides the legal answer or a final legal position. (SOURCE default rule)

## Procedure
1. **Ingest the matter** and match signals against the 13 triggers (plus memory context).
2. **Set the verdict** (escalate_required / escalate_recommended / no_trigger) and **urgency**.
3. **Identify the target** professional(s) — attorney, CPA, HR, founder — and whether one exists on file.
4. **Frame the escalation package** (per `AUTONOMY_AND_APPROVAL_MODEL.md` escalation format): the situation, what the agent knows, its confidence, the specific decision needed, the recommended option/next step with rationale, exposure, reversibility, and any deadline.
5. **If urgent**, advise the founder explicitly not to sign/respond/act before counsel.
6. **Return control appropriately:** hold the action (do not execute) and hand the framed question to the founder to bring to their professional; if `no_trigger`, release back to the owning agent.
7. **Log** the routing decision in `decisions` (matter, triggers matched, target, verdict) and link to any related `risks` entry.

## Output
```yaml
output:
  disclaimer: "Routing guidance only — not legal advice. The named professional provides the legal answer; the agent does not."
  verdict: enum(escalate_required, escalate_recommended, no_trigger)
  urgency: enum(urgent, standard)
  triggers_matched: [str]          # which of the 13 fired
  route_to: [enum(attorney, cpa, hr, founder)]
  professional_on_file: bool       # if false, recommend engaging one
  framed_question:                 # the package to hand the professional
    situation: str
    what_we_know: str
    confidence: str
    specific_decision_needed: str
    exposure: str
    reversibility: enum(reversible, recoverable, irreversible)
    deadline: str
    recommended_next_step: str     # e.g. "do not sign before review"
  action_hold: bool                # true = the proposed action is held, not executed
  advice_to_founder: str           # e.g. "Do not respond to the subpoena before counsel."
  decision_record_id: str
```

## Recommendations
The recommendation is always a *routing* recommendation, never a legal one: which professional, how urgently, and what NOT to do before they weigh in. When a trigger fires, the skill recommends holding the action and provides the framed question so counsel can resolve it efficiently (minimizing legal cost). For `escalate_recommended` (no hard trigger but real exposure), it lays out the trade-off honestly so the founder can choose to consult or proceed at their own risk — while noting the agent's default is caution. It never recommends a way to "avoid" needing a lawyer when a trigger is present.

## Execution Opportunities
- **Produce the routing verdict and framed question** — analysis only, L0.
- **Draft the escalation package / email to the attorney or CPA** *for the founder to send* — reversible draft; the founder sends it (sending on the founder's behalf needs approval).
- **Hold the proposed action** and record the hold — reversible, LOW.
- **Log the routing decision** in `decisions` and link `risks` — reversible, LOW.
- **Never:** answer the legal question, draft a legal position, sign/commit anything, or send a legal communication without approval.

## Human Approval Requirements
Per `AUTONOMY_AND_APPROVAL_MODEL.md`:
- The agent **never executes the legal commitment** — signing, filing, responding to a legal demand, or any protected-class/employment action is always the founder's, made with the professional.
- **Sending** the framed question to a professional on the founder's behalf is an external communication → approval required (the founder normally sends it).
- The founder approves engaging (and paying) a professional.

## Escalation Conditions
This skill *is* the escalation mechanism; its "conditions" are the 13 triggers above. Targets:
- **Attorney:** triggers #1–#4, #7–#12, and most of #13.
- **CPA / tax professional:** entity tax and tax questions (part of #2, and tax portions of #13).
- **HR professional (with attorney):** #4 (classification/discipline), #5, #6, #8.
- **Founder:** the ultimate decision-maker in every case; also for ethical/values calls.
Every escalation carries the full framed package (situation, knowledge, confidence, decision needed, recommended step, exposure, deadline).

## KPIs
- % of legal-triggered matters correctly escalated (no missed triggers) — the critical safety KPI, target 100%.
- Zero instances of the agent answering a legal question or executing a legal commitment.
- Time-to-escalate for urgent matters (litigation/subpoena/theft) — minimized.
- Quality of framed questions (professional-reported: did they have what they needed?).
- Legal cost efficiency (well-framed questions → less billable back-and-forth).
- False-positive rate low enough not to bury the founder, but the skill errs toward over-escalation by design.

## Monitoring
Track escalated matters through to resolution (was counsel engaged? what did they decide?) and write the outcome back to `decisions` so repeated questions can cite prior guidance instead of re-escalating. Watch for patterns (many contract or classification escalations) that suggest a systemic fix (a standard template reviewed once by counsel, a retained attorney). Any matter left un-actioned past its deadline is surfaced as an execution risk.

## Follow-Up
- **Event-triggered:** runs whenever any of the 13 triggers appears in any agent's work.
- **After counsel responds:** record the professional's guidance in `decisions`; update the relevant skill's inputs (e.g. a reviewed contract template, a confirmed classification) so future matters resolve faster.
- **Periodic:** review the trigger list against current law with counsel (thresholds and rules change).

## Related Skills
- `contract-review-triage`, `employment-compliance-scan`, `ip-protection-audit`, `entity-structure-advisor` — all route their triggers *through* this skill.
- `crisis-response-planning` — hands the legal substance of a crisis here.
- `risk-diagnostic` — legal risks are scored there and routed here for the response.

## Guardrails
- **Guidance, not legal advice — and the router never answers the legal question.** Its only job is to decide *who* handles it and to frame it.
- **Default to escalation when in doubt** — an unclear signal is treated as a trigger, not waved through.
- **Never executes or authorizes a legal commitment** — signing, filing, responding to demands, and protected-class/employment actions are always human, with a professional.
- **Time pressure raises urgency, never lowers the bar** — a deadline is never a reason to skip counsel.
- **If no professional is on file, recommend engaging one** — the agent never fills the gap itself.
- **Nothing generated may read as a legal position or opinion.**
- **Privacy:** legal matters (litigation, allegations, subpoenas, IP theft) are highly sensitive (restricted); never place details in external URLs, payloads, or shared tools, and only share with the intended professional at the founder's direction.

## Example
**Founder input (urgent):** "We got a letter from a lawyer claiming our brand name infringes their trademark and demanding we stop using it in 10 days. Can you draft a response saying we disagree?"

**Skill reasoning:**
- Signals: `litigation_audit_subpoena_regulatory` = true (demand letter), `ip_theft_or_infringement` = true (infringement claim against us), `founder_uncertain_with_exposure` = true; is_action = true (about to respond), reversibility = a written response is effectively irreversible, time_pressure = urgent (10 days).
- Triggers matched: #11 (demand letter), #9 (IP infringement claim), #13 (uncertain + exposure).
- Verdict: **escalate_required**, urgency = **urgent**.
- Target: attorney (IP/litigation). Professional on file? Assume no → recommend engaging one immediately.
- The agent must **not** draft the disagreement response — a response can waive rights or create admissions; that is precisely a legal position.

**Output (abridged):**
- verdict: escalate_required; urgency: urgent; route_to: [attorney, founder]; professional_on_file: false → engage IP counsel now.
- framed_question: situation = "Received a trademark-infringement demand letter, 10-day deadline to stop using our brand name"; what_we_know = brand usage history, classes, first-use date if known; specific_decision_needed = "how to respond and whether to stop use"; exposure = brand/rebrand cost + potential litigation; reversibility = irreversible (a response can waive rights); deadline = 10 days; recommended_next_step = **"Do not respond or admit anything before counsel."**
- action_hold: true; advice_to_founder: "Do not send any response yourself; get IP counsel within 1–2 days given the deadline."

**Executed vs. escalation:** the skill **refused to draft the response**, produced the routing verdict and framed package, drafted an intake email *for the founder to send to an IP attorney*, held the action, and logged the decision. It answered no legal question and took no legal position.

## Provenance
**SOURCE.** Directly implements the Legal & Negotiation domain's Legal Escalation Triggers (the 13-item "when a human attorney is REQUIRED" list) and the default rule "when in doubt, frame the question and escalate — never generate content that reads as legal advice or a final legal position," plus the escalation-target ladder (attorney / CPA / HR / founder). The framed-question package mirrors the approval/escalation format in `AUTONOMY_AND_APPROVAL_MODEL.md`. Routing thresholds for `escalate_recommended` are SYNTHESIZED defaults. All source program branding removed. Guidance-only, never legal advice.
