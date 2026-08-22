---
name: negotiation-preparation
domain: sales
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [company, deals, pipeline, offerings, customers, cvp, competitive_advantage, pricing, metrics, relationships]
writes: [negotiations, decisions, tasks]
related_skills: [proposal-builder, pipeline-and-forecast-review, sales-process-design, contract-review-triage, legal-escalation-router, craft-cvp, assess-competitive-advantage]
owned_by_agents: [orchestrator, sales-agent]
---

# Skill: Negotiation Preparation

## Purpose
Produce a complete, table-ready negotiation plan for a specific upcoming negotiation so the founder walks in prepared instead of improvising: ranked interests (both sides), a marked BATNA, target and limit per issue, an estimated ZOPA, good/better/best option packages, a sequenced (bilateral) concession plan, objective standards to cite, and an opening-and-hold-back communication script. Preparation is the single biggest lever on negotiation outcomes — this skill front-loads it.

## When to Use
- A specific negotiation is coming up: a customer deal on price/terms, a supplier/vendor contract, a partnership, a lease, a renewal.
- A deal in the pipeline reaches the Negotiation stage (handoff from `sales-process-design` / `proposal-builder`).
- The founder says: "I have a call to negotiate price," "They pushed back on my quote — how do I respond?", "Prep me for this negotiation," "What should I concede and what should I hold?", "They want a discount."
- Before ANY high-stakes give-and-take where the founder wants to defend value and avoid conceding blindly.

## When NOT to Use
- The founder needs to draft the initial proposal/quote (before any back-and-forth) → `proposal-builder`.
- The negotiation is about contract LEGAL terms (indemnification, liability, IP, restrictive covenants) rather than commercial terms → prepare the commercial plan here, but route the legal clauses to `contract-review-triage` / `legal-escalation-router`; this skill does not give legal advice.
- The founder wants to design the overall sales process → `sales-process-design`.
- An employment negotiation (compensation, hiring/firing terms) → route to the People/HR domain; the framework applies but employment carries its own escalation triggers.

## Required Context
Reads Business Memory: `company` (model, size), `deals`/`pipeline` (the specific deal: value, stage, history, expected close), `offerings` (what's being sold and its cost-to-serve), `pricing` (list price, floor, margin), `cvp` (the value proposition to anchor on instead of price), `competitive_advantage` (what the counterparty loses by choosing a competitor), `customers`/`relationships` (prior/present/future relationship state), `metrics` (past negotiation outcomes, concession ratios). Each fact carries `source`, `confidence`, `as_of`. What is NOT known — the counterparty's true interests, target, and limit — must be treated as HYPOTHESES, explicitly labeled, never as fact.

This skill is the direct runnable form of the source Negotiation Preparation Framework: it collects the 7 prep inputs per party, runs the 11-step preparation procedure, and outputs a filled prep sheet plus tiered packages, a concession plan, standards, and a script.

## Inputs
```yaml
input:
  negotiation_context:
    counterparty: str                 # generalized to "the counterparty" in shared artifacts
    counterparty_type: enum(customer, supplier, partner, landlord, other)
    relationship:
      current_state: str              # e.g. "almost non-existent" / "existing 2-yr supplier"
      desired_future_state: str       # e.g. "trusted long-term supplier"
      one_time_or_repeat: enum(one_time, repeat)
    mode_bias: enum(claiming, creating, unknown)   # distributive vs. integrative
  issues:                             # what must be agreed
    - name: str                       # e.g. price, delivery_time, scope, payment_terms, volume, exclusivity
      unit: str                       # $, days, %, etc.
  my_side:
    interests: [ {interest: str, importance_rank: int} ]   # the WHY, ranked
    per_issue:
      - issue: str
        target: number                # ideal outcome
        limit: number                 # walk-away / reservation value
        opening: number               # first-offer anchor (optional)
    alternatives: [str]               # what I do if no deal
    batna: str                        # my BEST alternative (mark which of the above)
    resources_to_offer: [ {resource: str, cost_to_me: enum(low,med,high), value_to_them: enum(low,med,high)} ]
    standards: [str]                  # objective criteria I can cite (benchmarks, market data)
    constraints: [str]                # e.g. margin floor, cash timing, capacity
  other_side_hypotheses:              # explicitly hypotheses, not facts
    likely_interests: [ {interest: str, importance_rank: int} ]
    estimated_per_issue: [ {issue: str, est_target: number, est_limit: number} ]
    estimated_batna: str
    known_pressures: [str]            # timing, budget cycle, incumbent switching cost
  first_offer:
    who_should_open: enum(me, them, unknown)
    rationale: str
```

## Missing Information Protocol
1. Pull the deal, pricing, CVP, and competitive advantage from memory before asking the founder anything.
2. The founder MUST supply their own interests, target, and limit per issue — these cannot be invented; if missing, ask (one batch).
3. The other side's interests/target/limit are hypothesized from context and market standards, ALWAYS labeled as hypotheses with a confidence level — never presented as known.
4. If the founder has not identified a BATNA, that is the first thing to establish (a negotiation without a known BATNA is dangerous) — help enumerate alternatives and mark the best.
5. Batch at most one concise question set for the highest-leverage unknowns: my limit per key issue, my BATNA, the relationship state, and any hard constraints (margin floor).
6. Never assume the founder's walk-away limit, margin floor, or willingness to give a specific concession — a wrong limit can lose money or a good deal.

## Diagnostic Questions
The source's negotiation diagnostic set, answered internally:
- What are MY interests (the "why") vs. my stated position (the "what I'm asking for")?
- What is my BATNA — and theirs? How strong is each?
- What is my target and my walk-away limit on EACH issue (not just price)?
- Is there a ZOPA (do our limits overlap)? If not, what interest, resource, or added issue could create one (a New ZOPA)?
- What can I offer that costs ME little but is worth a lot to THEM?
- What objective standards (industry averages, benchmarks, real numbers) justify my offer?
- Is this one-time/distributive (claim value) or relationship/repeat (create value)?
- What does the counterparty LOSE by choosing a competitor (my competitive advantage)?
- What should I reveal, and what must I hold back?

## Analysis Framework
Applies the source concepts and the 11-step preparation procedure.

**Core concepts (definitions used):**
- **Target** = ideal outcome. **Limit / reservation value** = worst outcome still acceptable (walk-away).
- **ZOPA** = overlap between the parties' limits — the value available to distribute. No overlap → no ZOPA on that issue alone.
- **BATNA** = best alternative to a negotiated agreement; leverage comes from a strong one.
- **Interests vs. positions** — negotiate on interests (the why), not positions (the stated demand).
- **Standards** = objective criteria that legitimize an offer.
- **Options / resources** = solutions meeting both interests; resources ideally cost little to me, worth a lot to them.

**Claiming vs. creating value:**
- **Claiming (distributive):** fixed pie — play close to the vest, don't get anchored, push for your share. Use for one-time deals.
- **Creating (integrative):** expand the pie — disclose interests, add issues/resources so both gain. Use when relationship/repeat business matters.
- Guiding maxim: get them to give you what YOU want because it's in THEIR interest.

## Calculations
Negotiation is qualitative but these quantify the plan:
- **ZOPA (per issue)** = overlap between `[my_limit, my_target]` and `[their_est_limit, their_est_target]`. If the ranges overlap, ZOPA = the overlap band; if not, **No ZOPA on this issue alone** → must create value / add issues. [SOURCE-DERIVED]
- **Value captured (post-deal)** = `outcome − my_limit` (how far above walk-away). Target is to land near MY target, well inside the ZOPA on my side. [SYNTH]
- **Concession ratio** = value I give ÷ value I get back; plan for ≤ 1 (never concede unilaterally). [SOURCE-DERIVED principle → SYNTH metric]
- **Resource leverage score** = rank resources by `value_to_them ÷ cost_to_me`; offer high-ratio items first. [SOURCE-DERIVED]
- **Package math (good/better/best)** = each package is a bundle of issue settlements whose total must stay ≥ my limit across issues (a concession on one issue offset by a gain on another). [SOURCE-DERIVED]
- **BATNA strength (qualitative → ordinal):** strong / moderate / weak; a strong BATNA raises how close to MY target I can hold. [SOURCE-DERIVED]
- No universal numeric thresholds exist in the source — all bands are relative to the founder's own target/limit and margin floor.

## Decision Rules
Directly from the source (SOURCE-DERIVED unless noted):
- **IF** I don't yet understand the other side's interests **THEN** do NOT discuss price — seek their "why" first.
- **IF** asked to concede **THEN** propose a BILATERAL concession (get something back); never concede unilaterally.
- **IF** my BATNA is strong **THEN** use it to WARN, not threaten.
- **IF** there is no ZOPA on price alone **THEN** add interests/resources/options to build a New ZOPA (price + needs met) BEFORE walking away.
- **IF** the negotiation is one-time / purely distributive **THEN** claim value (play close to the vest). **IF** relationship/repeat business matters **THEN** create value (disclose interests, expand the pie). [SYNTH]
- **IF** deciding whether to open **THEN** consider making the first offer to set the anchor — especially when I have good standards to justify it.
- **IF** the counterparty tries to anchor me **THEN** do not accept their anchor; re-anchor with my standards.
- **IF** presenting options **THEN** offer good/better/best packages (incl. longer-term-contract options) — do NOT fixate solely on price.
- **IF** I have a resource that costs me little but is worth a lot to them **THEN** lead with it to expand the pie cheaply.
- **IF** the deal involves binding legal/contract terms **THEN** prepare the commercial plan but route legal clauses to `contract-review-triage` / an attorney — do not negotiate legal terms as advice. [SYNTH — legal escalation]
- **IF** the founder's limit would breach the margin floor **THEN** flag it; the limit, not the target, protects the business.
- **IF** any Legal Escalation Trigger is present (signing/amending a binding contract, restrictive covenant, etc.) **THEN** stop before commitment and route to counsel. [legal domain]

## Procedure
The source 11-step preparation procedure, executed in order:
1. **Prioritize my interests** — rank them; identify the top 1–3 I must satisfy.
2. **Set my target and limit for each issue** (price AND non-price issues).
3. **Identify standards** that legitimize my offers (industry averages, benchmarks, real numbers/stats).
4. **Hypothesize the other party's interests, target, and limit** — labeled as hypotheses with confidence.
5. **Estimate the ZOPA** per issue — do the limits overlap? If not, plan to create value / add issues to open a New ZOPA.
6. **Improve my BATNA** before the table — enumerate alternatives, strengthen the best (more alternatives = more power).
7. **Generate options** that meet their interests while getting me mine; bundle interests into packages.
8. **Identify resources to offer** — prioritize low-cost-to-me / high-value-to-them (resource leverage score).
9. **Build a concession plan** — decide in advance what I can give, in what order, to get what I most need; plan BILATERAL concessions (counter a concession demand with a concession ask).
10. **Prepare good / better / best packages** (including longer-term-contract options); don't anchor solely on price.
11. **Plan the first-offer strategy and communication** — opening, what to reveal vs. hold, and push for synchronous delivery (in person / live where possible).
Then: assemble the filled prep sheet (both columns), write it to `negotiations`, log a decision record, and draft an internal briefing/script at L1. Nothing is sent to the counterparty and no term is committed — those are founder-approved.

## Output
```yaml
output:
  counterparty: str                   # generalized in shared artifacts
  mode: enum(claiming, creating, mixed)
  prep_sheet:
    my_side:
      interests_ranked: [ {interest: str, rank: int} ]
      per_issue: [ {issue: str, target: number, limit: number, opening: number} ]
      batna: {description: str, strength: enum(strong, moderate, weak)}
      standards: [str]
      resources: [ {resource: str, cost_to_me: enum(low,med,high), value_to_them: enum(low,med,high), leverage: enum(high,med,low)} ]
    other_side_hypotheses:
      likely_interests_ranked: [ {interest: str, rank: int, confidence: enum(high,med,low)} ]
      estimated_per_issue: [ {issue: str, est_target: number, est_limit: number, confidence: enum(high,med,low)} ]
      estimated_batna: {description: str, strength: enum(strong, moderate, weak)}
  zopa:
    - issue: str
      my_range: [number, number]      # [limit, target]
      their_est_range: [number, number]
      zopa_exists: bool
      zopa_band: [number, number]     # or null
      if_no_zopa_plan: str            # value-creation / added issue to open a New ZOPA
  packages:                           # good / better / best
    - tier: enum(good, better, best)
      issue_settlements: [ {issue: str, value: number} ]
      total_vs_limit: str             # confirmation it stays >= my limit across issues
      what_they_gain: str
      what_i_gain: str
  concession_plan:
    sequence:                         # ordered, bilateral
      - give: str
        ask_in_return: str
        trigger: str                  # when to deploy
        max_extent: number            # how far this concession may go
    never_concede: [str]              # red lines tied to limit / margin floor
  standards_to_cite: [str]
  first_offer:
    who_opens: enum(me, them)
    opening_move: str
    rationale: str
  communication_script:
    open: str                         # how to start (interests-first)
    reveal: [str]                     # what to disclose
    hold_back: [str]                  # what NOT to say
    competitor_loss_framing: str      # what they lose by choosing a competitor
    warn_not_threaten: str            # how to use BATNA
  legal_flags: [str]                  # any clause/term to route to counsel
  confidence: enum(high, medium, low) # driven by quality of counterparty hypotheses
```

## Recommendations
The plan is organized so the founder leads with interests (not price), opens (or not) deliberately with standards behind the anchor, and moves through good/better/best packages rather than discounting. Concessions are pre-sequenced and always bilateral, each tied to a trigger and a maximum extent so the founder never gives past their limit. Recommendations prioritize: (1) satisfy the top-ranked interest; (2) protect the limit/margin floor; (3) preserve the desired future relationship if repeat business matters. Everything is a preparation aid — the founder decides and executes at the table.

## Execution Opportunities
- Write the prep sheet and plan to `negotiations` and a decision record to `decisions` — reversible, LOW (prepared at L1 ceiling).
- Draft the internal briefing, packages, concession sequence, and script for the founder to rehearse — reversible, LOW.
- Draft (never send) an opening message / counter-offer for the founder to review and send themselves — the draft is LOW/reversible; SENDING or COMMITTING any term is external and gated.
- Create internal prep tasks (gather a benchmark, confirm the margin floor, strengthen the BATNA by lining up an alternative) — reversible, LOW.
This skill prepares; it never negotiates with, messages, or commits anything to the counterparty.

## Human Approval Requirements
- Sending any offer, counter-offer, or message to the counterparty is an EXTERNAL customer/vendor communication → ALWAYS founder-approved before sending (per `AUTONOMY_AND_APPROVAL_MODEL.md`).
- Committing to any price, discount, term, or concession → ALWAYS founder-approved; the agent proposes the plan, the founder commits.
- Signing or agreeing to any contract, or amending binding terms → ALWAYS founder-approved and routed through legal review; the agent never signs or agrees.
- Any concession that would breach the margin floor or a stated constraint is held and flagged, not executed.

## Escalation Conditions
- **Binding contract, restrictive covenant, or material legal amendment on the table** → route to `contract-review-triage` / attorney BEFORE any commitment (legal escalation trigger).
- **No ZOPA even after value-creation attempts** → surface to founder: walk to BATNA or restructure the deal; do not push past the limit.
- **Counterparty's interests/limit are pure guesswork** (low-confidence hypotheses) → tell the founder the plan rests on assumptions; recommend discovery before hard commitments.
- **Deal exceeds the founder's financial authority / cash implications** → founder (+ recommend accountant if cash-critical).
- **Employment-related negotiation** → route to People/HR domain and its escalation triggers.

## KPIs
Source-aligned and CLAUDE-derived candidates:
- % of negotiations reaching agreement.
- % of agreements where the outcome ≥ target (value captured within the ZOPA).
- Average outcome vs. limit (how much margin above walk-away was preserved).
- Concessions given vs. received ratio (≤ 1 is the goal — no unilateral giving).
- Prep-sheet completion rate before negotiations (leading indicator of good outcomes).

## Monitoring
After the negotiation: record actual outcome vs. target and limit per issue, which concessions were used and whether each got something in return, whether the relationship moved toward the desired future state, and whether counterparty-interest hypotheses proved accurate (to calibrate future prep). Feed outcomes into `metrics` so the concession ratio and win-vs-target KPIs trend over time.

## Follow-Up
- Event-triggered: whenever a deal enters the Negotiation stage, a counter-offer arrives, or terms materially change mid-negotiation (re-run to update the plan).
- Time-triggered: refresh standards/benchmarks periodically so anchors stay defensible; review concession-ratio trend each quarter.

## Related Skills
Fed by `proposal-builder` (the proposal being negotiated), `sales-process-design` (Negotiation stage), `craft-cvp` and `assess-competitive-advantage` (anchoring on value and competitor-loss framing). Routes to `contract-review-triage` / `legal-escalation-router` for legal terms, and feeds `pipeline-and-forecast-review` (outcome updates the forecast).

## Guardrails
- Never present the counterparty's interests, target, or limit as known fact — they are labeled hypotheses with confidence.
- Never let a planned concession cross the founder's limit or margin floor; the limit protects the business.
- Always plan concessions as bilateral; the plan must never suggest conceding unilaterally.
- Use a strong BATNA to warn, never to threaten; keep the desired future relationship intact where repeat business matters.
- This skill prepares only — it never sends a message, commits a term, or signs a contract; all such actions are founder-approved and, for legal terms, attorney-reviewed.
- Do not generate content that reads as legal advice; route legal clauses to counsel.
- Generalize the counterparty and any sensitive figures in shared artifacts unless the founder consents to naming.

## Example
**Founder input:** "A repeat-potential B2B customer got my $30k quote for a year of services and asked for a 20% discount. I want to keep the relationship. How do I prepare?"
**Reasoning (11-step, abridged):**
1. My interests ranked: (1) protect margin, (2) win a multi-year relationship, (3) predictable cash. 2. Issues + my target/limit: price target $30k, limit $25.5k (margin floor); term target 24 months; payment target 50% upfront, limit net-30. 3. Standards: published market rate for comparable services, my CVP's quantified ROI. 4. Their hypotheses (labeled low-med confidence): interest in budget fit and risk reduction; est. limit ~$27k; likely has an incumbent alternative (moderate BATNA). 5. ZOPA on price: my [25.5k,30k] vs. their est [—,27k] → overlap $25.5k–$27k exists → ZOPA present but tight; plan to widen with non-price value. 6. Improve my BATNA: line up two other pipeline deals so I can hold near target. 7–8. Options/resources: instead of a straight 20% cut ($6k), offer a resource that costs me little but is worth a lot to them — priority onboarding and a quarterly business review (low cost, high value). 9. Concession plan (bilateral): give a 7% discount ($27.9k) ONLY in exchange for a 24-month commitment and 50% upfront; give priority onboarding in exchange for a case-study/testimonial; never go below $25.5k. 10. Packages: good = $30k / 12-mo / net-30; better = $28.5k / 24-mo / 50% upfront + priority onboarding; best = $27.9k / 24-mo / 50% upfront + onboarding + QBR + testimonial. 11. First offer: don't discuss price until their interests are clear; re-anchor with the market standard and CVP ROI; use the other pipeline deals to WARN (capacity is filling), not threaten.
**Output (abridged):** mode = creating (repeat relationship). ZOPA $25.5k–$27k on price; New-ZOPA plan adds term + resources. Good/better/best packages as above. Concession sequence tied to term + upfront + testimonial, red line at $25.5k. Script: open on their budget/risk interests, reveal ROI standard, hold back the true floor, frame competitor-loss (onboarding quality + ROI), warn via capacity.
**Executed vs. approval:** Wrote the prep sheet, packages, concession plan, and script to `negotiations` at L1; drafted a counter-offer message for the founder to review. Nothing sent to the customer; no discount committed; any resulting contract routed to `contract-review-triage` before signature.

## Provenance
SOURCE. Directly implements the SOURCE-DERIVED Negotiation Preparation Framework from the Legal & Negotiation domain: the 7 prep inputs per party, the 11-step preparation procedure, target/limit/ZOPA/BATNA mechanics, claiming-vs-creating-value, ranked interests, good/better/best packages, sequenced bilateral concessions, objective standards, and the opening/hold-back communication script, plus the source's at-the-table tactics and top high-stakes strategies. The concession-ratio and value-captured metrics are SYNTH quantifications of source principles; legal-escalation routing derives from the same domain's escalation triggers. All example counterparties and figures are generalized. See `internal/PROVENANCE_MAP.md`.
