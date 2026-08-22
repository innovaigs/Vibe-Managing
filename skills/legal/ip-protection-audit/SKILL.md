---
name: ip-protection-audit
domain: legal
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [company, team, operations, offerings, risks, integrations]
writes: [decisions, risks]
related_skills: [legal-escalation-router, employment-compliance-scan, contract-review-triage, business-continuity-plan, risk-diagnostic]
owned_by_agents: [legal-liaison-agent, operations-agent]
---

# Skill: IP & Trade-Secret Protection Audit

> **THIS IS GUIDANCE, NOT LEGAL ADVICE.** Trade-secret and IP protection depends on jurisdiction and on agreements that must be drafted and enforced by an attorney. This skill finds gaps in NDAs, IP-assignment, and access controls and proposes remediation to prepare a conversation with counsel. It does NOT draft or enforce agreements, does NOT file registrations, and does NOT make legal determinations of ownership or infringement. Suspected IP theft or infringement is an urgent attorney trigger — speed matters legally.

## Purpose
Protect what makes the business valuable — customer lists, pricing strategy, internal procedures, proprietary methods, code, and creative work — by finding the holes in the protection program: people or vendors with access but no NDA, contractors who may own what they created because there's no IP-assignment, and sensitive materials open to more people than need them. IP protection is a layered program, not a single document; this skill audits the layers and hands the fixes to counsel.

## When to Use
- The business has proprietary information worth protecting (customer/pricing data, methods, code, designs, brand) and the founder asks "is our IP protected?", "do our contractors sign anything?", "who can see our customer list?"
- Before or during onboarding of employees, contractors, or vendors who will access sensitive info.
- When engaging contractors/agencies to create work product (code, designs, content) — IP-assignment must be in place *before* the work.
- After a departure (employee/contractor leaves) — verify post-employment obligations and access revocation.
- When `risk-diagnostic` or `business-continuity-plan` flags a knowledge/access single-point-of-failure.
- Proactively, periodically, as the team and vendor set grow.

## When NOT to Use
- **Suspected trade-secret theft or infringement (yours or a claim against you) is happening** → STOP and route to an attorney immediately via `legal-escalation-router`; speed matters legally. Do not "audit," escalate.
- The founder wants to **file** a trademark/copyright/patent → that is an attorney/agent action; frame and escalate.
- The gap is really about employment-law compliance/classification → `employment-compliance-scan`.
- The issue is a specific contract's IP clause under review → `contract-review-triage` (then escalate).

## Required Context
- `company`: what proprietary assets exist, entity, jurisdictions.
- `offerings`: products/services and their underlying IP (code, methods, content, brand).
- `team`: who has access to what; employees vs. contractors; recent/upcoming departures.
- `operations`: vendors with access (dependency_risk), tools/systems holding sensitive data, SOPs, access controls.
- `integrations`: connected systems and their read/write scopes (where sensitive data flows).
- `risks`: existing IP/access entries.

## Inputs
```yaml
input:
  proprietary_assets:
    - asset: str                   # e.g. "customer list", "pricing model", "source code", "brand/logo"
      type: enum(trade_secret, copyright, trademark, patentable, confidential_data)
      criticality: enum(low, medium, high)
  access_map:
    - who: str                     # role/person/vendor
      relationship: enum(employee, contractor, vendor, partner)
      assets_accessed: [str]
      has_nda: bool
      has_ip_assignment: bool
      access_level: enum(need_to_know, broad, full)
  agreements_in_place:
    ndas_all_with_access: bool
    ip_assignment_employees: bool
    ip_assignment_contractors: bool
    handbook_data_policies: bool
    post_employment_obligations: bool
  events:
    recent_departure: bool
    engaging_contractor_for_work_product: bool
    suspected_theft_or_infringement: bool   # if true -> escalate immediately
  registrations_considered:
    trademark: bool
    copyright: bool
    patent: bool
```

## Missing Information Protocol
- **If `suspected_theft_or_infringement` is true, escalate immediately** and stop the audit.
- **Pull the access map from memory** (team, operations, integrations) — who touches what — before asking.
- **Ask ONE batch** for what data can't reveal: which agreements are actually signed, access levels, and upcoming departures/engagements.
- **Never assume** an NDA or IP-assignment exists because a relationship is old or trusted, and **never assume the business owns contractor-created work** — the default rule is that without a written assignment, a contractor may own what they create. Unverified agreements = gaps, not "probably fine."

## Diagnostic Questions
- What proprietary information is worth protecting (customer lists, pricing strategy, procedures, code, designs, brand), and how critical is each?
- Who has access to each — employees, contractors, vendors — and does each have a signed **NDA**?
- Does every employee **and contractor** agreement include an **IP-assignment** clause? (Without it, a contractor may own what they create.)
- Is access to sensitive materials restricted to **need-to-know**, or can too many people see everything?
- Do handbook/policies cover data access/handling and **post-employment** obligations?
- Is there a **rapid investigate-and-enforce** process for suspected violations?
- When someone leaves, is access revoked and are post-employment obligations reaffirmed?
- Are relevant **registrations** (trademark/copyright/patent) considered where they'd help?

## Analysis Framework
Audit the **layered trade-secret protection program** (SOURCE — holistic approach), then the registration layer (CLAUDE baseline):
1. **Agreement layer — NDAs.** Every employee, contractor, AND vendor with access should have a signed NDA that defines what's protected and for how long. Gap = anyone with access and no NDA.
2. **Ownership layer — IP-assignment.** Every employee and contractor agreement should assign IP/work product to the business. **Default rule:** without assignment, a contractor may own what they create → high-priority gap when engaging contractors for work product.
3. **Access-control layer — need-to-know.** Sensitive materials (customer lists, pricing, procedures, code) restricted to those who need them; audit for over-broad access, shared logins, and integration scopes that expose data.
4. **Policy layer — handbook.** Data access/handling and post-employment obligations documented and applied.
5. **Enforcement layer.** A defined process to investigate and act on suspected violations quickly — proactive protection strengthens legal standing under trade-secret law.
6. **Departure hygiene.** On exit: revoke access, reaffirm post-employment/confidentiality obligations, retrieve materials.
7. **Registration layer (CLAUDE).** Consider trademark (brand/name/logo), copyright (creative works), patent (inventions) where they add protection — all require attorney/agent involvement.

Then map each gap to a remediation and a risk-register warning metric (e.g. `access_holders_without_nda`, `contractors_without_ip_assignment`).

## Calculations
- **NDA coverage** = access-holders with a signed NDA / total access-holders. Target 100%.
- **IP-assignment coverage** = employees+contractors with assignment / total. Target 100% (contractor gap is highest-risk).
- **Access-breadth ratio** = holders with broad/full access / total holders → flag over-provisioning.
- **Need-to-know violations** = count of holders whose access exceeds their role.
- **Departure-hygiene rate** = departures with access revoked + obligations reaffirmed / total departures.
- **Gap-exposure score** = asset criticality (1–3) × gap severity (1–3) → prioritization.
No ownership or infringement determination is calculated — those are legal conclusions for counsel.

## Decision Rules
- IF anyone with access to sensitive info lacks a signed **NDA** THEN flag a high-priority gap → remediation + attorney. (SOURCE)
- IF any **employee or contractor** agreement lacks an **IP-assignment** clause THEN flag a gap; for contractors creating work product this is high-priority (default: they may own it). (SOURCE)
- IF engaging a contractor for work product AND no IP-assignment is signed **before** work starts THEN block/flag urgently — assignment after the fact is harder. (SOURCE)
- IF sensitive materials have broad/full access beyond need-to-know THEN flag over-provisioning and recommend restriction. (SOURCE)
- IF handbook/policies don't cover data handling + post-employment obligations THEN flag a policy gap (route to `employment-compliance-scan`/HR). (SOURCE)
- IF there is no investigate-and-enforce process THEN recommend establishing one (proactive protection strengthens legal standing). (SOURCE)
- IF a departure occurred without access revocation / obligation reaffirmation THEN flag departure-hygiene gap and remediate immediately. (SYNTHESIZED)
- IF `suspected_theft_or_infringement` THEN STOP and escalate to an attorney immediately — speed matters legally. (SOURCE trigger #9)
- IF a registration would materially help THEN note it and route filing to an attorney/agent. (CLAUDE + SOURCE trigger #12)
- **Default:** the agent never drafts or enforces the agreements — it identifies gaps and routes drafting/enforcement to counsel. (SOURCE)

## Procedure
1. **Check `suspected_theft_or_infringement`** — if true, escalate immediately and stop.
2. **Inventory proprietary assets** and their criticality (from `offerings`/memory).
3. **Build the access map** — who (employee/contractor/vendor) accesses what, and which agreements they have (from `team`/`operations`/`integrations` + one question batch).
4. **Audit each layer** (NDA, IP-assignment, access control, policy, enforcement, departure hygiene, registrations).
5. **Compute coverage metrics** and score gap exposure (criticality × severity).
6. **Assemble the gap list** ranked by exposure, each with a concrete remediation and whether it needs counsel.
7. **Route agreement/registration/enforcement items** to `legal-escalation-router`; policy items to `employment-compliance-scan`/HR.
8. **Add gaps to `risks`** with warning metrics; **log** the audit in `decisions`.

## Output
```yaml
output:
  disclaimer: "Guidance only — not legal advice. Agreements and registrations must be drafted/filed by an attorney; suspected theft/infringement is an urgent attorney matter."
  asset_inventory:
    - asset: str
      type: enum(trade_secret, copyright, trademark, patentable, confidential_data)
      criticality: enum(low, medium, high)
  coverage:
    nda_coverage_pct: number
    ip_assignment_coverage_pct: number
    access_breadth_ratio: number
    departure_hygiene_rate: number
  gaps:
    - gap: str
      layer: enum(nda, ip_assignment, access_control, policy, enforcement, departure, registration)
      exposure_score: number       # criticality * severity
      remediation: str
      needs_counsel: bool
  registration_notes: [str]        # trademark/copyright/patent to discuss with attorney
  escalations: [str]               # routed items + framed questions
  risk_register_entries: [ {risk, warning_metric} ]
  urgent: bool                     # true if suspected theft/infringement -> escalated
  decision_record_id: str
```

## Recommendations
Gaps are ranked by **exposure (asset criticality × gap severity)**, with the highest priority on: any high-criticality asset accessible without an NDA, and any contractor creating work product without an IP-assignment (because the business may not own its own product). The skill favors the fastest protective moves first — restrict access to need-to-know and get assignments/NDAs signed *before* new work — since those are cheap and prevent the worst outcomes. Every agreement and registration is recommended *to* an attorney; the agent proposes the remediation and drafts nothing binding.

## Execution Opportunities
- **Produce the audit and gap list** — analysis, L0/L1.
- **Draft NDA/IP-assignment templates and a data-handling policy outline** *for attorney review* — reversible drafts, never adopted without counsel.
- **Recommend and (where the founder approves) tighten access controls / integration scopes to need-to-know** — access changes to internal systems are reversible/recoverable but should be confirmed to avoid breaking workflows.
- **Create remediation tasks** (collect signatures, revoke departed access, restrict a shared folder) — reversible, LOW.
- **Add IP/access gaps to `risks`** with warning metrics — reversible, LOW.
- **Never:** finalize/enforce an agreement, file a registration, or make an ownership/infringement determination.

## Human Approval Requirements
Per `AUTONOMY_AND_APPROVAL_MODEL.md`, hold for human decision:
- Adopting/finalizing any NDA, IP-assignment, or policy (attorney + founder).
- Filing any registration (attorney/agent).
- Enforcement action against a person/vendor (attorney + founder).
- Access-control changes that could disrupt operations or a specific person's work (founder confirmation; coordinate with the person's manager).
The skill prepares drafts, findings, and task lists; counsel and the founder decide and execute.

## Escalation Conditions
> Per source escalation triggers, route to an attorney (do not auto-execute):
- **Immediately:** suspected trade-secret theft or IP infringement — yours or a claim against you (#9); speed matters legally.
- **Attorney (required):** drafting/enforcing NDAs, IP-assignment, and restrictive covenants (#3); IP registration filings (#12); any ownership/infringement question.
- **HR / `employment-compliance-scan`:** handbook data/post-employment policies and their consistent application.
- **IT / security specialist:** access-control implementation, integration scopes, and monitoring.
Escalation message includes: the asset at risk, the specific gap, exposure score, and the framed questions for counsel.

## KPIs
- NDA coverage and IP-assignment coverage across all access-holders (target 100%, contractors especially).
- Access-breadth ratio and need-to-know violations trending down.
- Departure-hygiene rate (access revoked + obligations reaffirmed) at 100%.
- % of contractor engagements with IP-assignment signed **before** work starts.
- # of open IP/access gaps by exposure, trending down.
- Zero instances of the agent drafting/enforcing agreements or determining ownership.

## Monitoring
Watch for new access-holders (a new contractor/vendor/integration) appearing without a matching NDA/IP-assignment, over-broad access creeping in (shared logins, wide integration scopes), and departures without access revocation. Each is a warning metric in `risks`. Renewal of contractor engagements triggers a re-check that assignments are current. Any signal of exfiltration or a competitor using your methods → immediate escalation.

## Follow-Up
- **Event-triggered:** before engaging any contractor for work product, on any departure, when a new vendor/integration gets access, and immediately on any suspected theft/infringement (escalate).
- **Periodic:** re-audit as the team and vendor set grow (quarterly for IP-heavy businesses).
- Retire a gap only when the signed agreement / restricted access is verified — record in `decisions`.

## Related Skills
- `legal-escalation-router` — routes agreement drafting, enforcement, registrations, and theft/infringement to counsel.
- `employment-compliance-scan` — for handbook data policies and worker agreements at hire.
- `contract-review-triage` — for IP clauses in specific contracts.
- `business-continuity-plan` — knowledge/access single-points-of-failure (documenting a capability must respect need-to-know).
- `risk-diagnostic` — receives IP/access gaps as scored risks.

## Guardrails
- **Guidance, not legal advice.** Every output carries the disclaimer; nothing may read as a legal opinion on ownership or infringement.
- **Never drafts a binding agreement, files a registration, or enforces** — those are attorney actions; the agent produces drafts *for review* only.
- **Suspected theft/infringement halts the audit and escalates immediately** — speed matters legally.
- **Never assumes an agreement exists or that the business owns contractor work** — unverified = gap; contractor work without assignment defaults to the contractor.
- **Access changes are confirmed before execution** to avoid breaking legitimate workflows, and always follow need-to-know.
- **Privacy:** the asset inventory and access map are highly sensitive (customer lists, pricing, code); store restricted, apply need-to-know to the audit itself, and never place in external URLs, payloads, or shared tools.

## Example
**Founder input:** "We're hiring a freelance dev agency to build our new app, and I realized I'm not sure any of our contractors sign anything. Are we covered?"

**Skill reasoning:**
- `suspected_theft_or_infringement` = false → audit proceeds.
- Asset inventory: source code (high, patentable/copyright), customer list (high, trade secret), pricing model (high, trade secret), brand/logo (medium, trademark).
- Access map: 3 current contractors + the new agency access code and customer data; **none have IP-assignment**, 1 has an NDA. → NDA coverage 25%, IP-assignment coverage 0% for contractors.
- Highest exposure: the agency will **create the app's source code with no IP-assignment** → default rule means the *agency* may own the app → critical gap, must sign assignment **before** work starts.
- Access control: customer list in a shared drive open to all contractors → over-provisioned; restrict to need-to-know.
- Registration: brand/logo worth a trademark discussion; app code copyright.

**Output (abridged):**
| Gap | Layer | Exposure | Remediation | Counsel? |
|---|---|---|---|---|
| Agency, no IP-assignment | ip_assignment | 9 | Sign assignment **before** work | Yes (attorney drafts) |
| Contractors, no NDA | nda | 9 | NDAs for all with access | Yes |
| Customer list open to all | access_control | 6 | Restrict to need-to-know | Founder confirms |
| No trademark on brand | registration | 4 | Discuss filing | Yes (attorney/agent) |

**Executed vs. escalation:** the skill produced the audit, drafted NDA + IP-assignment templates and a data-handling policy outline *for attorney review*, created tasks to restrict the shared drive (pending founder confirmation) and collect signatures, and added `contractors_without_ip_assignment` + `access_holders_without_nda` to `risks` (reversible, L1). It **drafted nothing binding and filed nothing**, and routed the agency IP-assignment (before work starts), the NDAs, and the trademark question to an attorney via `legal-escalation-router`.

## Provenance
**SOURCE.** Derives from the Legal & Negotiation domain: the holistic trade-secret protection approach (NDAs with employees/contractors/vendors; handbook data/post-employment policies; need-to-know access restriction; rapid investigate-and-enforce), the IP-protection checklist, the default rule that without IP-assignment a contractor may own what they create, and the escalation triggers for restrictive-covenant/agreement drafting, suspected theft/infringement, and registration filings. The registration layer (trademark/copyright/patent) is CLAUDE baseline, flagged as attorney/agent work. All source program branding removed. Guidance-only, never legal advice.
