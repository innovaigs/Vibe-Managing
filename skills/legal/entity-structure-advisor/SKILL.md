---
name: entity-structure-advisor
domain: legal
version: 0.1.0
autonomy_ceiling: L0
provenance: CLAUDE
reads: [company, founders, finance, team, strategy, market]
writes: [decisions]
related_skills: [legal-escalation-router, employment-compliance-scan, contract-review-triage, risk-diagnostic]
owned_by_agents: [legal-liaison-agent, strategy-agent]
---

# Skill: Entity Structure Advisor (Informational)

> **THIS IS GUIDANCE, NOT LEGAL OR TAX ADVICE.** Entity choice has tax, liability, and financing consequences that depend on the founder's exact state/jurisdiction, ownership, and goals, and the law changes. This skill produces an *informational comparison to prepare a conversation with a qualified attorney and CPA*. It never selects, forms, or changes an entity, and it must always tell the founder to confirm with an attorney and a CPA before acting.

## Purpose
Help a founder understand the trade-offs between common business entity structures — liability protection, tax treatment, formalities, and fit for raising capital — so they walk into a conversation with an attorney and CPA informed and with the right questions ready. The output is a neutral comparison and a framed question list, not a recommendation to file anything.

## When to Use
- The founder is forming a business and asks "what entity should I be — LLC, S-corp, C-corp, sole prop?"
- A restructure is on the table: adding a co-owner, taking on investment, hiring the first employee, expanding to another state, or profits/self-employment tax have grown.
- The founder asks informational questions like "what's the difference between an LLC and an S-corp?", "do I need to incorporate to get liability protection?", "what do investors expect?"
- As pre-work before an attorney/CPA meeting, to make that meeting efficient.

## When NOT to Use
- The founder wants a decision *made* or an entity *formed/changed* → that is always an attorney + CPA action; route via `legal-escalation-router`.
- The question is really about employment obligations that attach at hiring → `employment-compliance-scan`.
- The question is about a specific contract or agreement (operating agreement, shareholder agreement) → those must be drafted by an attorney; use `contract-review-triage` only to triage an existing draft, and escalate.
- The question involves specific tax filings, elections, or dollar-level tax optimization → that is a CPA action; frame and escalate.

## Required Context
- `company`: current entity_type, formation_date, jurisdictions, business_model, stage.
- `founders`: number of owners, ownership intent, US-person status (relevant to S-corp eligibility).
- `finance`: revenue level, profitability, whether the founder takes a salary/draw, self-employment tax exposure.
- `team`: whether/when a W-2 employee will be hired (triggers employment compliance regardless of entity).
- `strategy`: growth intent — bootstrapping vs. raising venture capital vs. issuing equity/options.
- `market`: whether operations/customers/workers span multiple states.

## Inputs
```yaml
input:
  situation:
    current_entity: enum(none, sole_prop, general_partnership, llc, s_corp, c_corp, other)
    home_state: str
    num_owners: int
    owners_us_persons: bool           # relevant to S-corp eligibility
  liability_exposure: enum(low, moderate, high)   # physical products, client premises, employees, contracts
  financials:
    profitable: bool
    founder_takes_salary: bool
    approx_annual_profit_band: str    # rough band only, never used as tax advice
  growth_intent: enum(lifestyle, steady_growth, raise_venture_capital, issue_equity)
  multistate: bool                    # operating/hiring/remote across state lines
  hiring_first_employee_soon: bool
```

## Missing Information Protocol
- **Pull from memory** current entity, owner count, growth intent, and multistate status before asking.
- **Ask ONE batch** for the few decision-shaping unknowns: number of owners, liability exposure, growth/financing intent, and whether hiring is imminent.
- **Never assume** the founder's tax situation, never estimate specific tax savings, never assert what is legal in their state, and never treat rough profit bands as a basis for a tax recommendation.
- If key facts are unknown, present the general comparison with the caveat that the recommendation-shaping factors are incomplete and must be confirmed with professionals.

## Diagnostic Questions
- How many owners are there, now and planned? (handshake partnerships are a trap — multi-owner needs a written agreement.)
- What's the liability exposure — physical products, client premises, employees, signed contracts?
- Are you profitable and paying yourself, and is self-employment tax a concern?
- Do you plan to raise venture capital or grant stock options?
- Will you operate, hire, or have remote workers across state lines?
- Are all owners US persons? (S-corp eligibility.)
- Are you hiring your first W-2 employee soon? (triggers employment compliance regardless of entity.)

## Analysis Framework
Compare the common structures on four dimensions — **liability shield, tax treatment, formalities/cost, and financing/ownership fit** — then map the founder's situation to which structures are *worth discussing with professionals* (never a single directive):

| Structure | Liability shield | Tax treatment | Formalities | Best fit |
|---|---|---|---|---|
| Sole proprietorship | None (personal assets exposed) | Pass-through, self-employment tax | Minimal | Solo, low-liability, testing an idea |
| General partnership | None (joint liability) | Pass-through | Low, but **needs a written partnership agreement** | 2+ owners, early, low-liability (rare without an agreement) |
| LLC | Yes | Pass-through, flexible | Light | Common default once there's real liability/revenue |
| S-corporation (a tax election) | Yes (as corp/LLC) | Pass-through with potential payroll-tax savings | Moderate; **ownership limits** (US persons, ≤100 shareholders, one class of stock) | Profitable owner-operators taking a salary |
| C-corporation | Yes | Entity-level tax; **double taxation** on distributed profit | Highest | Raising venture capital, multiple share classes, retaining earnings |

Then apply the triage heuristics (below) to shortlist 1–2 structures to raise with the attorney/CPA, always with the "confirm with a professional" flag.

## Calculations
**None as a basis for advice.** This skill does not compute tax savings, self-employment tax, or entity-level tax — those are CPA calculations that depend on jurisdiction, current-year rules, and the founder's full picture. Any illustrative arithmetic (e.g. the concept that an S-corp election can reduce self-employment tax on distributions) is described qualitatively and explicitly handed to a CPA to quantify. Never present a dollar figure as a tax outcome.

## Decision Rules
> Output every rule as "**consider** X — confirm with an attorney + CPA," never as a directive.
- IF solo, low liability, testing an idea THEN a sole proprietorship may suffice; revisit as revenue/liability grow. (CLAUDE)
- IF there is any meaningful liability exposure (physical products, client premises, employees, signed contracts) THEN consider an LLC or corporation for a liability shield. (CLAUDE)
- IF there are multiple owners THEN never operate on a handshake — consider an LLC/partnership/corporation **with a written operating/partnership/shareholder agreement** (ownership %, decision rights, buy-sell, exit). Route the agreement to an attorney. (CLAUDE + SOURCE escalation)
- IF profitable, paying yourself a salary, and self-employment tax is a concern THEN consider discussing an S-corp election with a CPA. (CLAUDE)
- IF planning to raise venture capital or grant stock options THEN consider a C-corporation (often formed in a VC-friendly state). (CLAUDE)
- IF hiring the first W-2 employee THEN trigger `employment-compliance-scan` regardless of entity type. (SOURCE)
- IF operating/hiring across state lines or with remote workers THEN consider foreign-qualification/registration and local-law compliance in those states. (SOURCE)
- IF the founder wants a decision made, an entity formed, or an agreement drafted THEN STOP and route to an attorney + CPA via `legal-escalation-router`. (SOURCE — always-escalate)

## Procedure
1. **Gather the situation** from memory + one question batch (owners, liability, financials, growth intent, multistate, imminent hiring).
2. **Present the four-dimension comparison table**, tailored to the founder's plain-language level.
3. **Apply the triage heuristics** to shortlist 1–2 structures worth discussing — framed as options, never a directive.
4. **Flag downstream triggers:** multi-owner → written agreement; hiring → employment compliance; multistate → foreign qualification.
5. **Assemble a framed question list** for the attorney and CPA (see Output) so the professional meeting is efficient.
6. **Attach the mandatory "confirm with attorney + CPA" disclaimer** to every output.
7. **Record the informational session** in `decisions` (as context/pre-work), noting that no entity action was taken.

## Output
```yaml
output:
  disclaimer: "Informational only — not legal or tax advice. Confirm any entity choice or change with a licensed attorney and a CPA before acting."
  comparison_table:
    - structure: str
      liability_shield: str
      tax_treatment: str
      formalities: str
      best_fit: str
      relevance_to_you: str
  shortlist_to_discuss:              # 1-2 options, framed as "consider + confirm"
    - structure: str
      why_it_may_fit: str
      what_to_confirm_with_professional: [str]
  downstream_triggers:
    written_agreement_needed: bool   # multi-owner
    employment_compliance_triggered: bool
    multistate_registration_flag: bool
  questions_for_attorney: [str]
  questions_for_cpa: [str]
  escalation: "Route entity formation/change and any agreement drafting to an attorney + CPA."
  decision_record_id: str
```

## Recommendations
This skill does not make a recommendation in the executable sense — it produces an *informed shortlist and a question set*. Options are ordered by how well they fit the stated situation on liability and financing, with tax deliberately deferred to the CPA. The framing is always comparative ("A gives you X but costs Y in formalities; B is what investors expect if you raise") plus the explicit instruction to confirm with professionals. It never tells the founder which to pick or implies the model can substitute for counsel.

## Execution Opportunities
- **Produce the comparison and question list** — analysis only, L0.
- **Record the informational session** in `decisions` as pre-work — reversible, LOW.
- **Draft the agenda/questions for the attorney/CPA meeting** — reversible draft.
- **Trigger `employment-compliance-scan`** if hiring is imminent — analysis handoff.
- **Nothing else.** No entity formation, no filing, no agreement drafting, no tax election — ever.

## Human Approval Requirements
By design this skill takes **no executable legal or financial action**, so there is nothing to auto-execute. The founder — with an attorney and CPA — makes and executes any entity decision. If the founder asks the agent to form or change an entity, the agent declines and routes to professionals.

## Escalation Conditions
> Per the source legal escalation triggers, the following **require** a human professional; this skill frames the question and hands off — it never resolves them:
- **Attorney (required):** choosing or changing entity structure; setting ownership %; drafting operating/partnership/shareholder agreements; any binding formation document. (SOURCE trigger #2)
- **CPA / tax professional (required):** tax elections (incl. S-corp), tax treatment, and any quantified tax comparison. (SOURCE trigger — tax/entity question)
- **Attorney:** multistate/foreign qualification and its liability/tax implications. (SOURCE trigger #10)
- **Founder:** the actual decision, always made with professionals.
Escalation message includes: the situation, the shortlisted options, the specific questions for each professional, and a clear statement that no action was taken by the agent.

## KPIs
- % of entity questions that reach an attorney/CPA before any action (target 100%).
- Founder-reported efficiency of the professional meeting (were the right questions asked?).
- Zero instances of the agent forming/changing an entity or presenting tax figures as advice.
- Downstream triggers (employment, multistate, agreements) correctly flagged.

## Monitoring
Watch for situation changes that should re-open the entity conversation: adding an owner, crossing into a new state, becoming profitable, taking a salary, or preparing to raise capital. When any occurs, prompt the founder to revisit with professionals — but never auto-act.

## Follow-Up
- **Event-triggered:** re-run informationally when ownership, profitability, financing intent, or geography changes.
- **After the professional meeting:** capture the professionals' actual decision in `decisions` (superseding the informational pre-work) so downstream skills use the real entity.

## Related Skills
- `legal-escalation-router` — routes the actual decision and any drafting to counsel.
- `employment-compliance-scan` — triggered when hiring the first employee.
- `contract-review-triage` — to triage (not draft) an operating/shareholder agreement.
- `risk-diagnostic` — liability exposure feeds the risk register.

## Guardrails
- **Guidance, not legal or tax advice** — every output carries the disclaimer; nothing may read as a legal opinion.
- **Never forms, changes, or files** an entity, election, or agreement.
- **Never presents dollar-level tax figures as advice** — tax quantification is a CPA action.
- **Never asserts what is legal in a specific jurisdiction/year** — flags it as "confirm for your state and the current year."
- **Multi-owner situations always route to a written agreement drafted by an attorney** — never "a handshake is fine."
- **Low-confidence inputs are surfaced, not smoothed over** — if the situation is unclear, say so and defer to professionals.
- **Privacy:** ownership, EIN, and financial details are restricted-sensitivity; never place in external URLs or payloads.

## Example
**Founder input:** "I've been a sole proprietor freelancing, but I'm bringing on a co-founder and we might raise money next year. Should I become an LLC or something?"

**Skill reasoning:**
- Situation: currently sole prop → but adding a 2nd owner (handshake risk), moderate liability (client contracts), growth intent = may raise venture capital, single state for now.
- Comparison table presented plainly.
- Triage: multi-owner → written agreement needed (attorney). Raising venture capital → investors typically expect a C-corporation, and converting later has cost — worth discussing *now* with an attorney/CPA. LLC is a common interim shield but may need conversion for VC.
- Shortlist to discuss (framed, not directive): (a) LLC with a written operating agreement if raising is uncertain; (b) C-corporation if raising is likely — confirm timing and state with professionals. Tax treatment deferred to CPA.

**Output (abridged):**
- Shortlist: "Consider an LLC (+ operating agreement) vs. a C-corp — the right call depends on how real the fundraise is and your tax picture. Confirm with an attorney + CPA before choosing."
- Questions for attorney: co-founder ownership %, vesting, buy-sell, decision rights; LLC-vs-C-corp for a planned raise; conversion cost/timing; which state.
- Questions for CPA: tax impact of each; how a raise changes the calculus; self-employment tax now.
- Downstream: `written_agreement_needed: true`; if they hire, run `employment-compliance-scan`.

**Executed vs. escalation:** the skill produced the comparison and question list and recorded it as pre-work (L0). It **took no entity action** and routed the actual decision, the operating/shareholder agreement, and the tax analysis to an attorney and CPA via `legal-escalation-router`.

## Provenance
**CLAUDE.** The source curriculum did not cover entity selection; this skill uses standard baseline legal/tax knowledge (entity types, liability, pass-through vs. double taxation, S-corp eligibility) explicitly flagged as CLAUDE-derived, wrapped in the source's own hard rule that entity/tax decisions and agreement drafting always go to an attorney and CPA (Legal & Negotiation domain escalation triggers). The entity-structure decision heuristics mirror the source's "IF <situation> THEN consider X, confirm with attorney + CPA" logic. All source program branding removed.
