---
name: proposal-builder
domain: sales
version: 0.1.0
autonomy_ceiling: L1
provenance: SYNTH
reads: [company, deals, pipeline, offerings, pricing, cvp, competitive_advantage, personas, customers, brand, metrics]
writes: [proposals, deals, decisions, tasks]
related_skills: [sales-process-design, negotiation-preparation, pipeline-and-forecast-review, craft-cvp, assess-competitive-advantage, build-customer-persona, contract-review-triage]
owned_by_agents: [orchestrator, sales-agent]
---

# Skill: Proposal Builder

## Purpose
Draft a customer-facing proposal (or quote) for a specific deal that is anchored on the Customer Value Proposition and the founder's pricing — leading with the buyer's problem and the value/point-of-difference, not just a price line. It turns a qualified opportunity into a persuasive, structured document that advances the deal to Proposal/Negotiation — and it is ALWAYS held for founder approval before anything is sent or any price is committed.

## When to Use
- A qualified deal reaches the Proposal/Quote stage of the pipeline (handoff from `sales-process-design`).
- The founder says: "Draft a proposal for [customer]," "Write me a quote," "They asked for a written offer," "Put together a proposal for this deal," "Turn this conversation into a proposal."
- After discovery, when Need/Budget/Authority/Timing are confirmed and it's time to put value + price in writing.
- To respond to an RFP (formal proposal variant) in a B2B/B2G sale.

## When NOT to Use
- The deal isn't qualified yet (no confirmed need/decision-maker) → stay in Discovery; a proposal to an unqualified buyer wastes effort. Route back to `sales-process-design` qualification.
- The founder needs to prepare for back-and-forth on price/terms AFTER the proposal → `negotiation-preparation`.
- The CVP or pricing doesn't exist yet → run `craft-cvp` and set pricing (finance `break-even-and-pricing-analysis`) first; a proposal without a value proposition or a defensible price is just a number.
- The document is a binding CONTRACT (not a commercial proposal) → route to `contract-review-triage` / an attorney; this skill drafts a commercial proposal, not legal terms.
- A generic marketing asset (not a deal-specific offer) is wanted → use the marketing content skills.

## Required Context
Reads Business Memory: `deals`/`pipeline` (the specific opportunity: buyer, confirmed needs from discovery, scope discussed, expected value, timing), `offerings` (deliverables, options, cost-to-serve), `pricing` (list price, packages, discount policy, margin floor), `cvp` (the value proposition and point-of-difference — the spine of the proposal), `competitive_advantage` (why they should choose the founder over alternatives — from `assess-competitive-advantage`), `personas`/`customers` (buying-center roles: who reads it, who decides, what each cares about), `brand` (voice/tone if defined), `metrics` (past proposal win rates by format). Each fact carries `source`, `confidence`, `as_of`; do not state a price, scope, or claim not grounded in memory or founder input.

The proposal is the seller-side artifact for the buyer's Evaluation→Purchase transition (funnel Desire→Action): its job is to make the value obvious, differentiate against alternatives, remove friction, and give a clear next action.

## Inputs
```yaml
input:
  deal:
    id: str
    buyer_org: str                    # generalized to "the counterparty" in shared/example artifacts
    buying_center: [ {role: enum(initiator,user,decision_maker,influencer,buyer,gatekeeper), who: str} ]
    confirmed_needs: [str]            # from discovery — the buyer's own words where possible
    pains: [str]
    success_criteria: [str]           # what the buyer wants to be true after buying
    timing: str                       # decision/implementation timeline
    budget_signal: str                # confirmed range or constraint, if known
  offering:
    name: str
    deliverables: [str]
    options: [ {tier: str, inclusions: [str], price: number, margin_pct: number} ]  # good/better/best if used
    exclusions: [str]                 # what's explicitly not included (scope hygiene)
  pricing:
    list_price: number
    proposed_price: number            # founder-set or policy-derived
    discount_applied_pct: number
    margin_floor_pct: number          # guardrail — proposal must not breach without founder ok
    payment_terms: str
    validity_period: str              # e.g. "valid 30 days"
  value:
    cvp_statement: str                # from craft-cvp
    point_of_difference: str
    quantified_value: [str]           # ROI / time saved / cost reduced, if defensible
    proof: [str]                      # testimonials, results, credentials (must be real)
  format:
    type: enum(proposal, quote, rfp_response)
    length: enum(one_pager, standard, detailed)
    delivery_channel: enum(email, pdf, doc_link)   # generalized to function
    brand_voice: str                  # or "default"
```

## Missing Information Protocol
1. Pull CVP, competitive advantage, offering, and pricing from memory before asking anything.
2. If `confirmed_needs`/`success_criteria` are empty, the deal likely isn't discovered enough for a strong proposal — flag it and ask the founder for the discovery notes (one batch) rather than inventing buyer needs.
3. If `proposed_price` or `margin_floor_pct` is missing, ask the founder — NEVER set or infer a price; pricing is a founder decision and a hard guardrail.
4. Do NOT fabricate proof (testimonials, results, logos, credentials); if none are supplied, omit the proof section rather than invent it.
5. Batch at most one concise question set for the highest-leverage gaps (price, margin floor, confirmed needs, decision-maker).
6. Never assume scope, price, discount, or claims of results — all three carry commitment and credibility risk.

## Diagnostic Questions
Answered internally to draft well:
- Who actually reads and decides on this proposal (decision-maker vs. user vs. gatekeeper), and what does each most care about?
- What is the buyer's problem in THEIR words, and how do I open with it (problem-first, not company-first)?
- What is the point-of-difference vs. the specific alternatives this buyer is considering?
- Can the value be quantified defensibly (ROI, time, cost), or only stated qualitatively? (Never fake precision.)
- Is the scope crisp — deliverables, exclusions, assumptions — to prevent scope creep and later disputes?
- Is the price presented in the context of value (anchored to outcomes), and does it respect the margin floor?
- Is there a single, frictionless next action (sign, book kickoff, reply to accept)?
- Are there real proof points, or should that section be omitted?
- Does the price/terms language keep room for the coming negotiation, or does it over-commit?

## Analysis Framework
A value-first proposal structure (seller-side of Evaluation→Purchase):

1. **Open with the buyer's problem & goal** — restate confirmed needs/pains and success criteria in their words. (Buyer-centric, not "about us.")
2. **Proposed solution** — how the offering meets each confirmed need; map deliverables → needs one-to-one.
3. **Value & differentiation** — the CVP and point-of-difference; quantified value where defensible; what they LOSE by choosing an alternative (competitive advantage framing).
4. **Scope** — deliverables, explicit exclusions, assumptions, timeline/milestones. (Scope hygiene prevents disputes and protects margin.)
5. **Investment (pricing)** — price presented in value context; good/better/best options if used (anchor high, give choice, avoid single-price fixation); payment terms; validity period.
6. **Proof** — real testimonials, results, credentials (omit if none).
7. **Clear next step** — one frictionless action + who to contact + what happens after acceptance.

**Pricing presentation principles (from negotiation prep, applied to the written offer):** present options rather than one price; anchor on value/outcomes before the number; keep language that respects the upcoming negotiation (don't pre-concede in writing); never present a price below the margin floor without explicit founder approval.

## Calculations
- **Margin check** = `(proposed_price − cost_to_serve) ÷ proposed_price × 100` vs. `margin_floor_pct`. If below floor → HOLD and flag; do not draft a sub-floor price without founder approval. [SYNTH]
- **Effective discount** = `(list_price − proposed_price) ÷ list_price × 100`; surface it explicitly so the founder sees what's being given away. [CLAUDE-DERIVED]
- **Option spread (good/better/best)** = ensure each tier's price ≥ its own margin floor and tiers are spaced to anchor (e.g., best ~1.5–2× good) — anchoring high lifts the chosen middle. [CLAUDE-DERIVED]
- **Quantified value ratio** = `stated_customer_value ÷ proposed_price` (value-to-price); include ONLY if the value figure is defensible from real data. [SYNTH]
- **Deal value → forecast** = proposed_price × stage probability, handed to `pipeline-and-forecast-review` once sent. [cross-skill]
- No universal price thresholds — the margin floor and list price are the binding, founder-set guardrails.

## Decision Rules
- **IF** the deal is not qualified (no confirmed need or decision-maker) **THEN** do not draft a full proposal; return to qualification.
- **IF** `proposed_price` implies margin below the floor **THEN** HOLD; do not produce the priced proposal until the founder approves the exception.
- **IF** no real proof points exist **THEN** omit the proof section; never fabricate testimonials or results.
- **IF** the buyer is B2B/B2G with a formal process **THEN** use the RFP-response format and address stated evaluation criteria point-by-point; ensure the decision-maker AND gatekeeper's concerns are covered.
- **IF** a decision-maker and a user have different priorities **THEN** address both (value for the user, ROI/risk for the decision-maker).
- **IF** value can be quantified defensibly **THEN** lead the pricing with it; **IF NOT** THEN keep value qualitative — do not invent numbers.
- **IF** scope is fuzzy **THEN** add explicit exclusions and assumptions before pricing, to protect margin and prevent disputes.
- **IF** the document would create a binding legal commitment **THEN** route the terms to `contract-review-triage` / attorney; keep this artifact a commercial proposal.
- **IF** a discount is applied **THEN** state it explicitly to the founder and, ideally, tie it to a reciprocal ask (setting up `negotiation-preparation`).
- **IF** the proposal is ready **THEN** it is PREPARED at L1 and shown to the founder — sending and price commitment are always founder-approved.

## Procedure
1. Load the deal, CVP, competitive advantage, offering, pricing, personas, and brand from memory.
2. Confirm qualification (need, decision-maker, budget/timing); if missing, flag and request discovery notes.
3. Confirm `proposed_price` and `margin_floor_pct` with the founder if absent; run the margin check.
4. Identify the buying-center audience and tailor emphasis (user value vs. decision-maker ROI/risk).
5. Draft each section value-first: problem/goal → solution → value & differentiation → scope (with exclusions/assumptions) → investment (options, value-anchored) → proof (real only) → next step.
6. Apply brand voice; keep it concise and buyer-centric; ensure one frictionless call to action.
7. Run guardrail checks: margin floor respected, no fabricated proof, scope explicit, no unintended binding legal language, discount surfaced.
8. Produce the draft plus an internal cover note to the founder: price, effective discount, margin, what's assumed, and what to verify.
9. Write the draft to `proposals` and a decision record to `decisions` at L1; create a task "review & send proposal (founder approval required)."
10. Do NOT send. On founder approval, sending/commitment happens under founder authority; then hand the deal value to `pipeline-and-forecast-review` and prepare `negotiation-preparation` for the expected pushback.

## Output
```yaml
output:
  deal_id: str
  format: enum(proposal, quote, rfp_response)
  audience:
    primary_reader: str               # decision-maker
    secondary_readers: [str]
  draft:
    problem_and_goal: str
    proposed_solution: str
    needs_to_deliverables_map: [ {need: str, deliverable: str} ]
    value_and_differentiation: str
    point_of_difference: str
    scope:
      deliverables: [str]
      exclusions: [str]
      assumptions: [str]
      timeline: [ {milestone: str, date_or_offset: str} ]
    investment:
      options: [ {tier: str, inclusions: [str], price: number, margin_pct: number} ]
      recommended_option: str
      payment_terms: str
      validity_period: str
    proof: [str]                      # real only; empty if none
    next_step: str                    # single frictionless CTA
  pricing_summary:                    # internal cover note to founder
    proposed_price: number
    list_price: number
    effective_discount_pct: number
    margin_pct: number
    margin_floor_pct: number
    margin_floor_respected: bool
    quantified_value_ratio: number    # or null
  approval:
    status: enum(prepared_for_review)
    what_needs_founder_signoff: [str] # price, discount, scope, send
    items_to_verify: [str]            # anything low-confidence or assumed
  handoffs:
    to_forecast: bool                 # feed pipeline-and-forecast-review on send
    to_negotiation_prep: bool         # anticipate pushback
    to_legal: bool                    # if binding terms involved
  confidence: enum(high, medium, low)
```

## Recommendations
The draft leads with the buyer's problem and the value/point-of-difference, presents price in the context of outcomes, and offers tiered options rather than a single number to anchor the buyer and set up the negotiation. Recommendations to the founder prioritize: (1) verify price respects the margin floor; (2) confirm every claim/proof is real; (3) tighten scope (exclusions/assumptions) before sending. The skill flags what to verify and what needs sign-off. It drafts and prepares only — it never sends or commits.

## Execution Opportunities
- Write the proposal DRAFT to `proposals` and a decision record to `decisions` — reversible, LOW (prepared at L1 ceiling).
- Create an internal task "review & send proposal (founder approval)" — reversible, LOW.
- Draft the cover email / delivery message for the founder to review — reversible, LOW (drafting only).
- On founder approval, hand deal value to `pipeline-and-forecast-review` and spin up `negotiation-preparation` — reversible, LOW.
This skill NEVER sends the proposal, commits the price/terms, or signs anything.

## Human Approval Requirements
- Sending the proposal/quote to the customer is an EXTERNAL customer communication → ALWAYS founder-approved before sending (per `AUTONOMY_AND_APPROVAL_MODEL.md`).
- Committing the price, discount, or terms → ALWAYS founder-approved; the agent proposes, the founder commits.
- Any margin-floor exception (sub-floor price) → explicit founder approval, never auto-applied.
- If the document carries binding legal terms → founder approval AND attorney/`contract-review-triage` review before it becomes a commitment; the agent never signs.
- Publishing/reusing any customer name or logo as proof → founder approval (avoid using a real counterparty's identity without consent).

## Escalation Conditions
- **Price would breach the margin floor** → founder (approve exception or reprice); recommend accountant if it affects viability.
- **Buyer not truly qualified** → route back to `sales-process-design` qualification; do not proceed on a weak deal.
- **Binding legal/contract terms requested** → `contract-review-triage` / attorney before commitment.
- **No defensible proof but strong claims requested** → founder; do not fabricate — soften claims or supply real proof.
- **Low-confidence discovery inputs** (invented needs risk) → founder for the discovery notes before drafting.

## KPIs
- Proposal win rate (accepted ÷ sent) and by format/tier.
- Time-to-proposal (qualified → draft ready).
- Discount discipline: average effective discount and % of proposals at/above margin floor.
- Option uptake: share of deals taking the middle/best tier (anchoring effectiveness).
- Scope-dispute rate post-sale (proxy for scope hygiene).

## Monitoring
After a proposal is approved and sent (by the founder): track acceptance, time-to-decision, which tier was chosen, any discount given during negotiation vs. the drafted price, and post-sale scope disputes. Feed outcomes to `pipeline-and-forecast-review` and back into proposal win-rate metrics. Watch for repeated discounting below floor (a pricing or qualification problem upstream).

## Follow-Up
- Event-triggered: a qualified deal reaching Proposal stage; an RFP arriving; a buyer requesting a revised proposal after negotiation.
- Time-triggered: refresh proof points and standard pricing language periodically; review win-rate by format each quarter.

## Related Skills
Fed by `craft-cvp`, `assess-competitive-advantage`, `build-customer-persona` (value, differentiation, audience), `sales-process-design` (Proposal stage + qualification), and finance pricing skills (price/margin floor). Hands off to `negotiation-preparation` (anticipated pushback), `pipeline-and-forecast-review` (deal value on send), and `contract-review-triage` (if binding terms).

## Guardrails
- Never send the proposal or commit price/terms — always prepared for founder approval.
- Never price below the margin floor without explicit founder approval; always surface the effective discount and resulting margin.
- Never fabricate proof, results, ROI figures, or customer references; omit rather than invent, and don't use a real counterparty's name/logo without consent.
- Keep scope explicit (deliverables + exclusions + assumptions) to protect margin and prevent disputes.
- Keep the artifact a commercial proposal; route binding legal terms to counsel and never present legal advice.
- Generalize the counterparty and figures in shared/example artifacts unless the founder consents to naming.
- Present value before price; do not pre-concede in the written offer (preserve negotiation room).

## Example
**Founder input:** "Draft a proposal for a mid-size B2B customer for our $30k/year onboarding service. Discovery confirmed their pain is slow ramp of new hires; decision-maker is the VP of Ops, the user is the enablement lead. Our list is $30k, margin floor 60%, I'll offer good/better/best. We have two real case studies."
**Reasoning:** Qualified (need, decision-maker, timing confirmed) → proceed. Margin check: at $30k with 65% margin, floor respected. Audience: lead with ramp-time value for the enablement lead (user) AND ROI/risk-reduction for the VP of Ops (decision-maker). Quantified value defensible from case studies (e.g., "cut ramp time from 90 to 45 days") → lead pricing with it. Structure value-first; offer good ($24k, essentials) / better ($30k, recommended) / best ($45k, + QBRs & priority support) to anchor and steer to the middle. Two real case studies → include proof. One CTA: book a kickoff. Preserve negotiation room (don't pre-discount in writing).
**Output (abridged):** Problem/goal (slow new-hire ramp), solution mapped to needs, value & differentiation (ramp 90→45 days, point-of-difference vs. incumbent), scope with explicit exclusions/assumptions, investment as good/better/best (recommend "better" $30k, 65% margin, floor respected), 2 real case studies, next step = book kickoff, valid 30 days. Cover note: effective discount 0%, margin 65% (floor 60% ✓), value-to-price ratio flagged as defensible. Approval: prepared_for_review; needs founder sign-off on price + send. Handoffs: negotiation-prep (expect discount push), forecast on send.
**Executed vs. approval:** Wrote the draft + cover note to `proposals` at L1 and created a "review & send" task. Nothing sent; price not committed. On approval, deal value goes to `pipeline-and-forecast-review` and `negotiation-preparation` is prepared for the anticipated discount request.

## Provenance
SYNTH. Builds ON the SOURCE-DERIVED Customer Value Proposition (the four-part formula and CVP gauge), the buyer's-journey / marketing-funnel Evaluation→Purchase (Desire→Action) stage, the competitive-advantage / point-of-difference model, the buying-center roles, and the conversion principles (remove friction, clear action) from the Marketing & Customer domain — assembled into a deal-specific proposal artifact not present as a single tool in the source. Pricing-presentation and option-anchoring principles derive from the Legal & Negotiation domain (good/better/best packages, don't fixate on price). Margin-check, effective-discount, and option-spread math are CLAUDE-DERIVED. The always-approve-before-send/commit gate derives from `AUTONOMY_AND_APPROVAL_MODEL.md`. See `internal/PROVENANCE_MAP.md`.
