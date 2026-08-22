---
name: social-value-designer
domain: strategy
version: 0.1.0
autonomy_ceiling: L0
provenance: SOURCE
reads: [company, founders, customers, offerings, finance, market, goals, strategy]
writes: [strategy, decisions]
related_skills: [opportunity-feasibility-analysis, strategic-planning, growth-lever-selector, resource-gap-analysis]
owned_by_agents: [strategy-agent]
---

# Skill: Social Value Designer

## Purpose
Help a mission-minded founder build social value that also strengthens the economics — "doing well by doing good." Given the business model and community context, it recommends a social-value model (employment, cross-subsidization, or donation) and lays out the concrete profitability rationale so social impact and financial sustainability reinforce each other rather than compete.

## When to Use
- The founder wants to build social impact into the business: "how can we give back / hire from our community / serve people who can't afford us — without going broke?"
- When mission/values call for a formal social-value model rather than ad-hoc charity.
- During opportunity or strategic planning for a mission-driven business, to design the impact model alongside the economics.
- When the founder wants to attract mission-aligned customers or qualify for hiring/training subsidies.

## When NOT to Use
- The business needs core viability first (cash critical) → stabilize via `business-health-diagnostic` before adding a social model.
- The founder wants pure philanthropy unconnected to the business → this skill designs *integrated* social+economic value, not a donation plan; note the distinction.
- Legal structuring of a nonprofit / B-corp / benefit entity → attorney (this skill designs the model, not the legal entity).
- Tax treatment of donations/subsidies → accountant/tax professional.

## Required Context
Reads `company` (model, mission/values), `founders` (motivation, community ties), `customers` (segments, including underserved ones), `offerings` (what could be shared/subsidized), `finance` (margins, capacity to fund a model), `market` (community context, subsidy landscape), `goals`. Needs the community/social context the founder wants to serve and the business's margin headroom to sustain a model.

## Inputs
```yaml
input:
  business_model: str                 # how the business makes money today
  mission_values: [str]
  community_context: str              # the community/cause and the need
  target_beneficiaries: str           # who the social value is meant to help
  offering: str                       # the product/service that could carry social value
  economics:
    gross_margin_pct: number
    price: number
    unit_cost: number
    capacity_slack: str               # idle capacity that could serve a second segment
  founder_motivation: str             # why this matters to the founder
  constraints: [str]                  # budget for impact, legal form limits, etc.
```

## Missing Information Protocol
1. Pull margins and capacity from `finance`/`operations`; ask the founder for community context, beneficiaries, and motivation (these are theirs to define).
2. If margin headroom is unknown, flag it — a social model must be affordable; do not assume the business can fund one.
3. Never claim a specific subsidy/grant exists for this business without a source — describe the *category* of support and mark verifying it as a research task.
4. Do not assume the founder's intended legal form (nonprofit, B-corp, for-profit) — the model design is form-agnostic; legal form is an attorney question.

## Diagnostic Questions
- What social value does the founder want to create, and for whom?
- Which social-value model best fits the business model and community need?
- How does the model also improve the economics (subsidy, loyalty/new customers, cost savings)?
- Can the current margin/capacity sustain the model, and at what scale?
- What is the profitability rationale — the specific mechanism by which doing good pays back?
- What would need to be true (subsidy eligibility, customer demand for the mission) for the model to work?

## Analysis Framework
Match the business to one (or a blend) of the three socially responsible business-model archetypes, then articulate the profitability rationale via the three ways social responsibility improves economics:
- **Employment Model** — provide training/jobs to disadvantaged community members. Fits labor-intensive businesses with training capacity.
- **Cross-Subsidization Model** — same product to two segments; one pays full price, the other discounted/free (buy-one-give-one, pro bono, sliding scale, affordable-access tier). Fits businesses with margin headroom and idle capacity.
- **Donation Model** — commit a set portion of revenue/profit to an external social-service organization (e.g., 1% of sales, 5% of every purchase). Fits businesses wanting simple, visible impact without operational change.

**Three profitability mechanisms (the "doing well by doing good" rationale):**
1. **Subsidies** — state/federal subsidies for hiring/training disadvantaged employees (Employment Model).
2. **Customer attraction/loyalty** — community activities and visible mission attract new customers and deepen loyalty (all models, esp. Cross-Subsidization/Donation).
3. **Cost savings/sustainability** — production/sourcing practices that save money and are environmentally sustainable.

The recommended model must pair an archetype with at least one credible profitability mechanism, sized against the business's actual margin and capacity.

## Calculations
- **Cross-subsidization affordability:** if the full-price segment yields margin `M` per unit and the subsidized segment costs `C` to serve, then a sustainable give ratio `r` satisfies `r ≤ M / C` (each full-price sale can fund up to `M/C` subsidized units before eroding profit). Use to size a buy-one-give-one or sliding-scale ratio.
- **Donation-model impact vs. margin:** committing `d%` of sales reduces net margin by `d% × price` per unit; check `gross_margin_pct − d%` remains sustainable. Present the trade-off explicitly (impact given up = the margin points committed).
- **Employment-model net cost:** `net_cost = training_and_wage_cost − applicable_subsidies`; if subsidies materially offset cost, the model can be near-neutral or positive — but subsidy amounts must be verified (research task), never assumed.
- **Capacity-slack utilization:** cross-subsidization is most efficient when it uses idle capacity (marginal cost ≈ variable cost only) — quantify slack before recommending scale.
- No source numeric benchmarks (the 1% / 5% / buy-one-give-one figures in the source are illustrative examples, not required rates); the affordability formulas are SYNTH tools over the source archetypes.

## Decision Rules
- **IF** the business is labor-intensive with training capacity AND the community need is jobs/skills **THEN** recommend the Employment Model (verify hiring/training subsidy category).
- **IF** the business has margin headroom + idle capacity AND the need is access to the product/service **THEN** recommend the Cross-Subsidization Model, sized by `r ≤ M/C`.
- **IF** the founder wants simple, visible impact without operational change **THEN** recommend the Donation Model, sized so `gross_margin_pct − d%` stays sustainable.
- **IF** no profitability mechanism credibly applies **THEN** the model is charity, not integrated social value — say so plainly and let the founder decide whether to fund it anyway.
- **IF** margin headroom is insufficient to sustain any model **THEN** recommend deferring until viability improves (route to `business-health-diagnostic`); do not design an unaffordable model.
- **IF** a subsidy/grant is central to the rationale **THEN** mark verifying eligibility as a blocking research task — never present it as certain.
- **IF** the founder's motivation and the model diverge (e.g., wants employment impact but model recommends donation) **THEN** surface the trade-off and prefer the founder's intent where affordable.
- **NEVER** advise on legal entity form or tax treatment — route to attorney/accountant.

## Procedure
1. Capture the community context, beneficiaries, founder motivation, and the offering.
2. Assess margin headroom and capacity slack (the affordability envelope).
3. Match to the best-fit archetype (or a blend) given fit and affordability.
4. Identify the applicable profitability mechanism(s) and size the model with the calculations.
5. Flag any subsidy/grant assumption as a research task; describe the support *category*, not a specific unverified program.
6. State the profitability rationale explicitly — the mechanism by which doing good pays back.
7. Note the trade-off (margin given up, operational change) honestly.
8. Route legal-form and tax questions to professionals.
9. Write the recommended model + rationale to `strategy`; propose feasibility/planning follow-on.

## Output
```yaml
output:
  recommended_model: enum(employment, cross_subsidization, donation, blend)
  model_design: str                   # how it works in this specific business
  target_beneficiaries: str
  profitability_rationale:
    mechanisms: [enum(subsidy, customer_attraction_loyalty, cost_savings_sustainability)]
    explanation: str                  # the specific payback logic for THIS business
    sizing:
      cross_subsidy_ratio: str        # r ≤ M/C, if applicable
      donation_rate_and_margin_impact: str  # d% and resulting margin, if applicable
      employment_net_cost_note: str   # cost minus (to-be-verified) subsidies, if applicable
  affordability: enum(sustainable, marginal, unaffordable_now)
  tradeoffs: [str]                    # margin points given up, operational change required
  research_tasks: [ {question: str, source_category: str, blocking: bool} ]  # e.g., verify subsidy eligibility
  is_integrated_value: bool           # true = pays back; false = charity, flagged as such
  professional_referrals: [str]       # attorney (entity form), accountant (tax) if relevant
  recommended_next_skills: [str]
```

## Recommendations
The recommendation always pairs a social-value archetype with a concrete profitability mechanism sized against real margin and capacity — social impact and economics designed together, not bolted on. Where the payback logic doesn't hold, the skill says so honestly (it's charity, decide accordingly) rather than dressing up a cost as a strategy. Any subsidy that carries the rationale is flagged as a to-verify research task, never assumed.

## Execution Opportunities
- Write the recommended model + profitability rationale to `strategy` and a decision record — reversible, LOW.
- Create research tasks to verify subsidy/grant eligibility (support category → specific program) — reversible, LOW.
- Draft a mission/impact narrative for the founder (internal draft; publishing is out of scope) — reversible, LOW.
- Propose `opportunity-feasibility-analysis` if the model is a new offering — reversible, LOW.
Autonomy ceiling L0 — analysis and internal drafts only. This skill never commits donations, hires, changes pricing, publishes claims, or forms a legal entity.

## Human Approval Requirements
- Committing a donation rate, launching a subsidized tier, hiring under an employment model, or making public impact claims all require founder approval (and touch financial/employment/brand domains) — this skill only designs and recommends.
- Forming a nonprofit/B-corp/benefit entity or claiming tax benefits requires the founder plus attorney/accountant.

## Escalation Conditions
- **Legal entity form (nonprofit, B-corp, benefit corporation)** → attorney.
- **Tax treatment of donations/subsidies/impact claims** → accountant/tax professional.
- **Employment-model hiring of protected/disadvantaged groups** → HR/attorney (compliance with hiring and subsidy rules).
- **Public impact/environmental claims** → founder + brand/legal (avoid greenwashing/false-claim risk).
- **Model is unaffordable now** → founder + `business-health-diagnostic` (fix viability first).

## KPIs
- Impact delivered (beneficiaries served, jobs created, units subsidized, funds donated) vs. plan.
- Economic payback: subsidy captured, new/retained customers attributable to the mission, cost savings realized.
- Sustainability: margin maintained within the affordability envelope after the model is live.
- Integration integrity: model remains net-positive or neutral (not silently drifting into pure cost).

## Monitoring
Track both impact and payback after launch; watch that the give ratio / donation rate stays within the affordability envelope as volume changes. Verify subsidy assumptions actually materialized. Re-check affordability if margins compress. Watch for mission-washing risk (claims outrunning reality).

## Follow-Up
- Re-run if the business model, margins, or community context changes.
- Feed a new subsidized offering into `opportunity-feasibility-analysis` and the model into `strategic-planning`.

## Related Skills
Pairs with `opportunity-feasibility-analysis` (if the social model is a new offering), `strategic-planning` (embedding it as an objective), `growth-lever-selector` (mission as a differentiator/customer-attraction lever), and `resource-gap-analysis` (capacity to run an employment model).

## Guardrails
- Always pair impact with a credible profitability mechanism — or label it honestly as charity.
- Never present a subsidy/grant as certain; mark verification as a blocking research task and describe the support category, not a specific unverified program.
- Never design an unaffordable model — respect the margin/capacity envelope.
- Never advise on legal entity form or tax treatment — route to professionals.
- Never make or publish impact/environmental claims from this skill; drafting internal narrative is the limit, and claims must be truthful and verifiable.

## Example
**Founder input:** "We run a small commercial cleaning company. I want to hire and train people coming out of long-term unemployment in our neighborhood. Margins are ~40%, and we have steady demand but struggle to staff up. Motivation: this is personal to me."
**Reasoning:** Labor-intensive + training capacity + community need = jobs → **Employment Model** is the strong fit (and it directly solves the founder's staffing constraint). Profitability mechanisms: (1) subsidy — hiring/training-disadvantaged-workers subsidies likely apply (mark as blocking research task — verify the specific programs; describe the category: government workforce/hiring-assistance support); (2) cost savings — a reliable, trained, loyal workforce reduces turnover/recruiting cost, which is the founder's current pain point; (3) customer attraction — a visible community-hiring mission can win mission-aligned commercial clients. Affordability: sustainable (40% margin; training cost partly offset by subsidies + reduced turnover). Trade-off: upfront training time before new hires are billable.
**Output (abridged):** recommended_model = employment; model_design = "structured train-to-hire pipeline from local long-term-unemployed residents, paired with the existing crew as mentors"; mechanisms = [subsidy, cost_savings_sustainability, customer_attraction_loyalty]; explanation ties the model to the staffing bottleneck; affordability = sustainable; research_tasks = [{verify workforce/hiring subsidy eligibility, source_category: government workforce-assistance office, blocking: true}]; is_integrated_value = true; professional_referrals = [accountant (subsidy/tax), HR/attorney (compliant hiring)].
**Executed vs. approval:** Wrote the model + rationale to `strategy`, created the subsidy-verification research task, drafted an internal mission narrative (all L0/analysis). Hiring, subsidy claims, and any public mission claims are held for founder approval with HR/accountant involvement.

## Provenance
SOURCE. Implements the source's Socially Responsible Business Models (Employment, Cross-Subsidization, Donation) and the three "Doing Well by Doing Good" profitability mechanisms (hiring/training subsidies; community-driven customer attraction/loyalty; cost-saving sustainable practices). Affordability sizing formulas are SYNTH tools; the illustrative 1%/5%/buy-one-give-one figures from the source are treated as examples, not required rates. See `internal/PROVENANCE_MAP.md`.
