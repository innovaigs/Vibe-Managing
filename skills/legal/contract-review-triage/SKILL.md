---
name: contract-review-triage
domain: legal
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [company, finance, operations, customers, strategy, risks]
writes: [decisions, risks]
related_skills: [legal-escalation-router, entity-structure-advisor, ip-protection-audit, employment-compliance-scan, risk-diagnostic]
owned_by_agents: [legal-liaison-agent, operations-agent]
---

# Skill: Contract Review Triage

> **THIS IS GUIDANCE, NOT LEGAL ADVICE.** This skill runs a pre-signature checklist and flags high-risk clauses to prepare the founder to work with an attorney. It does NOT approve contracts, does NOT provide a legal opinion on enforceability, and does NOT authorize signing. Any contract that is binding, high-value, or contains a flagged clause must be reviewed by a qualified attorney before signing. The agent never signs or commits the company to a contract.

## Purpose
Before a founder signs anything, catch the missing terms and the dangerous clauses — so nothing binding goes unexamined and the founder knows exactly what to hand an attorney. The skill produces a pre-signature checklist result, a list of flagged high-risk clauses with plain-language explanations, and a clear "attorney review required / recommended" verdict.

## When to Use
- Any contract, lease, loan, MSA, SOW, NDA, vendor agreement, customer agreement, or terms document is about to be signed.
- The founder asks "can you look over this contract?", "is this vendor agreement okay to sign?", "what should I watch out for in this lease?"
- Before renewal of an existing agreement (auto-renew and price-escalation clauses hide here).
- As a gate in a procurement or sales workflow, before routing to signature.

## When NOT to Use
- The contract needs to be *drafted* from scratch → that is an attorney action; route via `legal-escalation-router`.
- It's an employment agreement or worker-classification document → run `employment-compliance-scan` (and escalate); classification/hiring is always an attorney trigger.
- The document is an operating/partnership/shareholder agreement or entity formation doc → `entity-structure-advisor` (informational) + attorney.
- The question is really about IP ownership across many agreements → `ip-protection-audit`.
- The founder wants the agent to *sign or accept* the contract → never; this skill prepares, the founder (with counsel) executes.

## Required Context
- `company`: correct legal entity name(s), entity_type, authorized signatories, jurisdictions.
- `finance`: contract value vs. materiality thresholds; payment/cash impact.
- `operations`: vendor relationship, dependency_risk, renewal_date (for renewals).
- `customers` / `strategy`: strategic importance of the counterparty.
- `risks`: whether this contract creates or concentrates a risk (e.g. sole-source, personal guarantee).

## Inputs
```yaml
input:
  contract:
    type: enum(vendor, customer, lease, loan, msa, sow, nda, partnership, terms, other)
    counterparty_name: str
    contract_value: number
    term_length: str
    text_or_summary: str           # full text preferred; a summary if that's all that's available
  our_side:
    legal_entity_name: str         # our correct legal name
    authorized_signatory: str
  context:
    is_renewal: bool
    strategic_importance: enum(low, medium, high)
    materiality_threshold: number  # above this, attorney review is required (config)
```

## Missing Information Protocol
- **Pull the correct legal entity name and authorized signatory from memory** — a mismatched party name is one of the most common and consequential defects.
- **If only a summary is available, say so** and cap the confidence — a triage on a summary cannot catch clause-level traps; recommend supplying full text or attorney review.
- **Ask ONE batch** for materiality threshold (if not set), whether it's a renewal, and strategic importance.
- **Never assume** a clause is absent because it wasn't mentioned, never infer enforceability, and never treat "looks standard" as safe. Unknown or missing clauses are flagged as gaps, not passed.

## Diagnostic Questions
Pre-signature checklist (SOURCE-derived):
- Correct legal entity names for **both** parties, and authorized signatories?
- Scope/deliverables specific and measurable?
- Price, payment schedule, and late-payment terms defined?
- Term, renewal, and **both** termination paths (for-cause and for-convenience)?
- IP ownership/assignment explicit — especially for work product and contractor deliverables?
- Confidentiality / NDA coverage present?
- Indemnification **and** limitation of liability present and balanced (not one-sided)?
- Governing law and dispute-resolution mechanism specified?
- Any auto-renew, exclusivity, non-compete, or personal-guarantee clause?

## Analysis Framework
1. **Completeness pass** — run the pre-signature checklist; mark each item present / missing / unclear. Missing essentials (party names, scope, payment, termination, IP, liability, governing law) are defects.
2. **High-risk clause scan** — flag clauses that carry outsized or asymmetric risk:
   - **Personal guarantee** — pierces the liability shield; founder's personal assets exposed. Always attorney review.
   - **Auto-renewal + price escalation** — silent lock-in and cost creep.
   - **Exclusivity / non-compete** — limits the business's freedom; enforceability is jurisdiction-specific.
   - **Uncapped or one-sided indemnification / no limitation of liability** — unbounded exposure.
   - **IP assignment away from us** (or silence on IP for work product) — you may not own what you paid for.
   - **Unilateral termination / termination-for-convenience only on their side** — they can walk, you can't.
   - **Automatic assignment / change-of-control** clauses, **most-favored-nation**, **liquidated damages/penalties**, **broad confidentiality binding us indefinitely**.
   - **Governing law / venue in a distant or unfavorable jurisdiction**.
3. **Balance check** — is each protective clause reciprocal, or does the counterparty hold all the leverage?
4. **Materiality + trigger check** — apply the escalation rules: value over threshold, or any flagged clause → attorney review required.
5. **Verdict** — "attorney review required" (binding + high-value or any red-flag clause) vs. "attorney review recommended" (lower-stakes but still counsel-advised) — never "safe to sign."

## Calculations
- **Materiality test:** contract_value ≥ materiality_threshold → attorney review required. (Threshold is a business config; default conservative.)
- **Total exposure estimate (qualitative):** contract_value + potential indemnity/penalty exposure + personal-guarantee amount — used to size risk, not to price legal advice.
- **Clause-risk tally:** count of high-risk clauses flagged; ≥1 → attorney review required.
- **Completeness score:** essentials present / total essentials — for triage prioritization only, never as a green light.
No enforceability or damages calculation is performed — those are legal determinations.

## Decision Rules
- IF the contract is binding AND (contract_value ≥ materiality_threshold OR any high-risk clause is flagged) THEN verdict = **attorney review required**; do not proceed to signature. (SOURCE)
- IF a **personal guarantee** is present THEN always require attorney review and explicitly warn the founder their personal assets are at stake. (SOURCE — personal-guarantee escalation)
- IF an **auto-renew** or **exclusivity/non-compete** clause is present THEN flag for attorney review (enforceability and lock-in are jurisdiction-specific). (SOURCE)
- IF **IP ownership/assignment** is missing or assigns work product away from us THEN flag as a defect and route to `ip-protection-audit` + attorney (default rule: without assignment, a contractor may own what they create). (SOURCE)
- IF **indemnification is uncapped or one-sided**, or **limitation of liability is absent** THEN flag as high-risk. (CLAUDE baseline)
- IF the correct **legal entity name or authorized signatory** is wrong/missing THEN flag as a defect before anything else. (CLAUDE baseline)
- IF only a **summary** (not full text) is available THEN cap confidence and recommend full-text attorney review. (SYNTHESIZED)
- IF the contract is an **employment or worker-classification** document THEN route to `employment-compliance-scan` + attorney. (SOURCE)
- IF the founder asks the agent to **sign/accept** THEN refuse and route the execution to the founder with counsel. (SOURCE — never auto-execute legal commitments)
- **Default:** ANY drafting, signing, or material amendment of a binding contract is an attorney trigger. (SOURCE escalation #1)

## Procedure
1. **Confirm both parties' correct legal names + authorized signatories** from memory and the document.
2. **Run the completeness checklist**; mark present/missing/unclear.
3. **Scan for high-risk clauses**; for each flag, write a plain-language explanation of *what it means for the business* and *why it's risky*.
4. **Check balance/reciprocity** of protective clauses.
5. **Apply materiality + trigger rules** to set the verdict.
6. **Assemble the triage report**: checklist results, flagged clauses (ranked by exposure), verdict, and a framed question list for the attorney (what to negotiate, what to clarify).
7. **Route to `legal-escalation-router`** with the framed questions when review is required.
8. **Log** the triage in `decisions` and, if the contract creates a risk, add it to `risks`. Never mark the contract "approved."

## Output
```yaml
output:
  disclaimer: "Guidance only — not legal advice and not approval to sign. An attorney must review before signing where flagged."
  party_check:
    our_legal_name_correct: bool
    counterparty_name_correct: bool
    authorized_signatory_confirmed: bool
  checklist:
    - item: str                    # e.g. "termination for convenience"
      status: enum(present, missing, unclear)
      note: str
  flagged_clauses:
    - clause: str
      risk: enum(high, medium)
      plain_language: str          # what it means for the business
      why_risky: str
      recommended_action: str      # e.g. "negotiate a cap", "strike", "attorney review"
  exposure_estimate: str           # qualitative
  verdict: enum(attorney_review_required, attorney_review_recommended)
  never: "safe_to_sign is never an output of this skill"
  questions_for_attorney: [str]
  routed_to_counsel: bool
  risk_register_entry: {risk, warning_metric}   # if applicable
  decision_record_id: str
```

## Recommendations
Flagged clauses are ranked by **exposure and reversibility of the commitment** — a personal guarantee or uncapped indemnity (severe, irreversible) tops the list; a distant venue clause (annoying, negotiable) sits lower. For each, the skill suggests a negotiation posture (cap it, make it reciprocal, add a for-convenience termination, strike it) framed as "raise with your attorney," never as a settled legal position. The overriding recommendation is always: get attorney review before signing wherever a trigger fires, and never sign under time pressure without it.

## Execution Opportunities
- **Produce the triage report and checklist** — analysis, L0/L1.
- **Draft the framed question list / redline requests** for the attorney and counterparty — reversible drafts (sending to the counterparty is a communication that needs approval).
- **Create a risk-register entry** if the contract concentrates or creates a risk — reversible, LOW.
- **Record the triage** in `decisions` — reversible, LOW.
- **Never:** sign, accept, e-sign, click-accept terms, or communicate acceptance to the counterparty.

## Human Approval Requirements
Per `AUTONOMY_AND_APPROVAL_MODEL.md`, always human (founder, with counsel):
- **Signing or agreeing** to any contract, terms, or legal commitment — CRITICAL, never auto.
- **Sending redlines or acceptance** to the counterparty — external communication, approval required.
- **Amending** a binding agreement.
The skill prepares; the founder and attorney decide and execute.

## Escalation Conditions
> Per source escalation triggers, route to a qualified attorney (and do not auto-execute):
- **Attorney (required):** drafting, signing, or materially amending any binding contract, lease, loan, or personal guarantee (trigger #1); any restrictive covenant — non-compete/non-solicit/NDA enforceability (trigger #3); IP assignment/infringement questions (trigger #9); anything the founder is unsure about with financial/liability exposure (trigger #13).
- **CFO / accountant:** loans, personal guarantees, and material financial commitments.
- **`employment-compliance-scan` + attorney:** if the document is employment/classification-related.
- **`ip-protection-audit` + attorney:** if IP ownership is missing or adverse.
Escalation message includes: contract type, counterparty, value, the flagged clauses with plain-language risk, and the specific questions for counsel.

## KPIs
- % of binding/high-value contracts triaged before signature (target 100%).
- % of triaged contracts with a flagged clause that reached an attorney before signing.
- # of defects caught pre-signature (wrong party name, missing termination/IP/liability).
- Contract cycle time (draft → triaged → signed) without sacrificing review.
- Zero instances of the agent signing or accepting a contract.

## Monitoring
Watch renewal and auto-renew dates so agreements are re-triaged before they silently roll over or escalate in price. Track flagged-but-signed contracts and their live obligations (exclusivity windows, personal guarantees, indemnity caps) in `risks` so the exposure stays visible. If a counterparty later disputes a contract, the triage record + attorney routing is the audit trail.

## Follow-Up
- **Event-triggered:** re-triage before every renewal, amendment, or when the counterparty proposes new terms.
- **Post-signature:** record the executed terms and any surviving obligations in memory; add material exposures to the risk register.

## Related Skills
- `legal-escalation-router` — routes flagged contracts and framed questions to counsel.
- `entity-structure-advisor` — for operating/shareholder agreements (informational) + attorney.
- `ip-protection-audit` — when IP ownership/assignment is missing or adverse.
- `employment-compliance-scan` — for employment/classification documents.
- `risk-diagnostic` — receives material contract exposures as risks.

## Guardrails
- **Guidance, not legal advice; never "safe to sign."** Every output carries the disclaimer.
- **Never signs, accepts, e-signs, or communicates acceptance** — signing is always the founder's action with counsel.
- **Never opines on enforceability or damages** — those are attorney determinations.
- **Missing/unclear clauses are flagged, not assumed benign.**
- **Summary-only reviews are explicitly caveated** and never substitute for full-text attorney review.
- **Personal guarantees always trigger an explicit personal-asset warning** and attorney review.
- **Privacy:** contract terms, counterparty identity, and pricing are commercially sensitive; store restricted, never place in external URLs, payloads, or shared tools.

## Example
**Founder input:** "This SaaS vendor sent a 2-year MSA, $36k total. Okay to sign? I'm in a hurry."

**Skill reasoning:**
- Party check: our legal name in the draft is the founder's personal name, not the LLC → defect (undermines the liability shield).
- Completeness: scope present; payment present; **termination = for-convenience for the vendor only**, none for us → defect; **auto-renew for successive 2-year terms with 90-day notice + 8% annual price escalation** → high-risk lock-in; **limitation of liability caps the vendor at one month's fees but indemnity from us is uncapped** → one-sided, high-risk; governing law in a distant state.
- Materiality: $36k vs. a $10k threshold → over threshold → attorney review required regardless.
- Verdict: **attorney review required.** Not "safe to sign," despite the time pressure.

**Output (abridged):**
- Defects: wrong signing entity (use the LLC); no termination right for us.
- Flagged: auto-renew + 8% escalation (negotiate a cap / opt-out notice); uncapped indemnity vs. their 1-month cap (make reciprocal / cap ours); distant venue.
- Questions for attorney: enforceability of the one-sided LoL; whether to strike auto-renew; entity name correction.

**Executed vs. escalation:** the skill produced the triage, drafted the redline-request list, and logged it (reversible, L1). It **did not sign** and routed the contract + questions to an attorney via `legal-escalation-router`, explicitly telling the founder not to sign under time pressure before review. It added the auto-renew + uncapped-indemnity exposure to `risks`.

## Provenance
**SOURCE.** Derives from the Legal & Negotiation domain: the Contract pre-signature checklist, the commercial-contract essentials, the IP-assignment default rule, and the hard escalation trigger that drafting/signing/amending any binding contract or personal guarantee requires an attorney. High-risk clause definitions (indemnity caps, one-sided LoL, change-of-control) are CLAUDE baseline layered on the source checklist. All source program branding and the example counterparty are generalized. Guidance-only, never legal advice.
