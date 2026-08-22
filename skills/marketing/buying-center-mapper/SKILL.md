---
name: buying-center-mapper
domain: marketing
version: 0.1.0
autonomy_ceiling: L0
provenance: SOURCE
reads: [customers.personas, customers.accounts, offerings, market]
writes: [customers.personas, decisions]
related_skills: [customer-persona-builder, buyers-journey-mapper, marketing-funnel-planner, customer-value-proposition-builder]
owned_by_agents: [marketing-agent, sales-agent]
---

# Skill: Buying Center Mapper

## Purpose
Identify every person (or entity) who influences or decides a purchase, and the role each plays — so marketing and sales aim messages at the actual decision-maker and clear the gatekeeper, instead of only charming the end user who can't say yes. Founder outcome: a filled role map for a purchase, revealing who to convince, who to reach, and who can block. [SOURCE]

## When to Use
- A sale involves more than one person: "Why did this deal stall?", "Who actually approves this?", "We keep pitching the user but nothing closes."
- Any B2B or B2G purchase, and household B2C purchases where one person uses and another pays.
- Deals that exceed an organization's approval threshold and route to procurement.
- Before designing a B2B/B2G buyer's journey or funnel — the roles determine who each stage's message targets.

## When NOT to Use
- Building a segment archetype (typical buyer of a whole segment) → use `customer-persona-builder`.
- Simple single-decider B2C impulse purchases where the buyer, user, and decider are the same person → mapping adds no value.
- Mapping the *stages* of the purchase over time → `buyers-journey-mapper`.
- Choosing which segment to serve → `market-segmentation`.

## Required Context
- The specific purchase/deal context (what's being bought, by what kind of organization or household).
- `offerings` — price and complexity (drives how many roles get involved and whether procurement gates it).
- `customers.personas` and `customers.accounts` — known people at the account, if tracked.
- Org type (business, government, household) and any known approval thresholds. [SOURCE]

## Inputs
```yaml
input:
  purchase_context:
    offering: string             # what is being bought
    price: number                # deal size (drives approval gating)
    org_type: enum(business, government, household)
    org_size: string             # headcount / department, if known
    complexity: enum(low, medium, high)
  known_people:                  # optional; anyone already identified at the account
    - name_or_placeholder: string
      title: string
      apparent_role: string
  approval_threshold: number     # spend level above which a formal approver/procurement is required, if known
```

## Missing Information Protocol
1. If specific people are unknown, map roles by **title/function archetype** (e.g. "department head = likely decision-maker") rather than inventing names.
2. If the approval threshold is unknown for a business/government buyer, assume a formal approver exists above the user for any non-trivial spend and flag `procurement_gate: assumed`. [SOURCE decision rule]
3. If org_type is unclear, ask the founder ONE question: business, government, or household — and roughly how big.
4. Never assume a single person holds final authority in a B2B/B2G deal without evidence; default to a multi-role map.

## Diagnostic Questions
- Who **initiates** — who first recognizes the problem/need this offering solves? [SOURCE]
- Who is the **user** — who actually uses the product/service day to day? [SOURCE]
- Who is the **decision-maker** — who holds final yes/no authority? [SOURCE]
- Who **influences** — who has a say, and how much weight? [SOURCE]
- Who is the **buyer** — who places the purchase order / handles procurement? [SOURCE]
- Who is the **gatekeeper** — who controls whether you even get the chance to sell (access control)? [SOURCE]
- Who makes the final decision to buy *from us specifically*? [SOURCE]

## Analysis Framework
Map the six **Buying Center roles** (Bonoma 1982, applied): [SOURCE]

| Role | Definition | What they need from marketing |
|---|---|---|
| **Initiator** | Recognizes a problem/need solvable by acquiring the offering | Trigger content that names the problem |
| **User** | The actual user of the product/service | Proof it works and makes their job/life better |
| **Decision-Maker** | Final yes/no authority | ROI, risk reduction, business case |
| **Influencer** | Has a say (varying weight) | Reasons to advocate internally |
| **Buyer** | Places the purchase order / procurement | Ease of purchase, terms, compliance |
| **Gatekeeper** | Controls access to the sale (assistant, IT, procurement policy, front desk) | A reason to let you through |

Key principles: one person can hold **multiple** roles; a single sale may involve **several** people or entities; the larger/more regulated the buyer, the more roles are distinct and the more procurement/gatekeeping matters. [SOURCE]

## Calculations
None. This is a role-mapping/classification task, not a scored one. [SOURCE]

## Decision Rules
- IF org_type is business or government THEN map all six roles explicitly and identify the gatekeeper (assistant/IT/procurement) and the procurement approver — do not assume the user can buy. [SOURCE]
- IF the purchase exceeds the organization's approval threshold THEN a procurement/decision-maker role gates it → market the business case to that approver, not only the user. [SOURCE]
- IF org_type is household THEN check whether the user and the payer/decider differ (e.g. child uses, parent decides and pays) and map both. [SOURCE]
- IF one person holds several roles (common in small orgs) THEN record the overlap and tailor a single message that satisfies each hat they wear. [SOURCE]
- IF a gatekeeper exists THEN define an explicit "get past the gatekeeper" tactic before any pitch reaches the decision-maker. [SOURCE]
- IF the decision-maker is unknown THEN do not proceed to a B2B funnel; first identify who signs off. [SOURCE]

## Procedure
1. Confirm the purchase context: offering, deal size, org type/size, complexity.
2. For each of the six roles, name the person or the title/function archetype most likely to hold it.
3. Note overlaps (one person, multiple roles) and gaps (unknown roles → who to discover).
4. Apply the approval-threshold rule: does this deal route through procurement/a formal approver?
5. For each role, state what that role needs to hear and who on the seller side should reach them.
6. Identify the single "buy-from-us" decision-maker and the gatekeeper tactic.
7. Attach the role map to the relevant account/persona; hand to `buyers-journey-mapper` / `marketing-funnel-planner` so each stage targets the right role.

## Output
```yaml
output:
  buying_center:
    purchase: string
    org_type: enum(business, government, household)
    roles:
      initiator: {who: string, evidence: enum(known, archetype, unknown), needs: string, reach_via: string}
      user: {who, evidence, needs, reach_via}
      decision_maker: {who, evidence, needs, reach_via}
      influencer: [{who, evidence, weight: enum(high, medium, low), needs, reach_via}]
      buyer: {who, evidence, needs, reach_via}
      gatekeeper: {who, evidence, needs, get_past_tactic: string}
    overlaps: [string]                 # people holding multiple roles
    procurement_gate: {applies: bool, threshold: number|null, approver: string}
    primary_target: string             # who to convince first
    gaps_to_discover: [string]         # roles still unidentified
  provenance: {source: agent_analysis, as_of: date, confidence: 0.0-1.0}
```

## Recommendations
Name the single most important person to convince first (usually the decision-maker, or the influencer with the most weight if the DM is unreachable), and the gatekeeper tactic that unlocks access. Prioritize discovery tasks for any `unknown` role that could block the deal. Recommend distinct messages per role rather than one generic pitch. As an L0 skill, all outputs are recommendations for the founder/sales team to act on. [SOURCE]

## Execution Opportunities
- Attach the role map to the account/persona in memory (reversible, LOW).
- Create discovery tasks to identify unknown roles (reversible, LOW).
- Draft role-specific talking points for the sales team (reversible, LOW).
- Log a decision record of who was identified as the decision-maker (reversible, LOW).

## Human Approval Requirements
- This is an L0 (observe/recommend) skill: it never executes an external action. All outputs are analysis and drafts for the founder/sales team.
- No ad spend, publishing, or email blasts are triggered here; any outreach to the identified people is executed by sales/outreach skills under their own approval rules (external outreach requires approval).

## Escalation Conditions
- The decision-maker cannot be identified and the deal is stalled → escalate to founder/sales for direct discovery. [§7]
- A government/regulated buyer imposes procurement rules the company may not meet → flag to Legal Liaison.
- One customer/account would create concentration risk → flag to Risk Agent.

## KPIs
- Role-fill completeness: % of six roles identified (vs. archetype/unknown).
- Deal velocity: reduction in stalls once the decision-maker is targeted directly.
- Access rate: gatekeeper-passing success after applying the tactic.
- Win rate on multi-stakeholder deals where the map was used.

## Monitoring
Track whether deals mapped with a clear decision-maker close faster than un-mapped ones. If deals still stall after mapping, the influencer weights or gatekeeper tactic likely need revision.

## Follow-Up
Re-map when the account's org changes (new decision-maker, reorg), when a deal stalls, or for each new complex/B2B opportunity. Update as `unknown` roles are discovered.

## Related Skills
Feeds `buyers-journey-mapper` and `marketing-funnel-planner` (each stage targets a role) and `customer-value-proposition-builder` (the DM's value drivers). Complements `customer-persona-builder` (segment archetype vs. deal-level roles).

## Guardrails
- Map roles by function/archetype when people are unknown; do not fabricate named individuals.
- Respect privacy: named contacts are `customers`-sensitive data; do not export outside the system without approval.
- Do not assume authority — a wrong decision-maker assumption wastes a sales cycle; mark evidence level honestly.
- As L0, never initiate outreach; hand qualified targets to the outreach/sales layer.

## Example
**Founder input:** "We sell a $12,000/yr scheduling software to dental clinics. The office manager loves it and keeps asking for it, but nothing closes."

**Skill reasoning:**
- org_type = business (small clinic), price $12k/yr → above a typical discretionary threshold → procurement/owner sign-off likely.
- Initiator = office manager (known). User = front-desk staff + office manager. Decision-Maker = the dentist/practice owner (archetype — controls spend). Influencer = office manager (high weight, internal champion). Buyer = office manager or bookkeeper places the PO. Gatekeeper = the office manager also screens vendor calls to the dentist → she is both champion AND gatekeeper.
- procurement_gate: applies (owner sign-off), approver = practice owner.
- primary_target = practice owner (business case: staff time saved, no-show reduction, ROI), reached *through* the office-manager champion.

**Output:** role map with the office manager as champion+gatekeeper and the practice owner as the real decision-maker; recommended tactic = arm the office manager with a one-page ROI business case to bring to the owner, plus offer a short owner-facing demo.

**Executed vs. approval:** Skill produced the map, drafted the owner-facing ROI one-pager, and created a discovery task to confirm the owner's name (all LOW, L0 — recommendations only). Actually sending anything to the clinic is left to the sales/outreach layer under its approval rules.

## Provenance
SOURCE. Derives from the Buying Center model (six roles: initiator, user, decision-maker, influencer, buyer, gatekeeper; attributed to Bonoma 1982) and the approval-threshold decision rule for procurement-gated purchases. See `internal/PROVENANCE_MAP.md`.
