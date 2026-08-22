---
name: exit-readiness-analysis
domain: strategy
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [company, founders, finance, customers, offerings, team, operations, metrics, goals, strategy, risks]
writes: [strategy, goals, decisions]
related_skills: [strategic-planning, business-health-diagnostic, resource-gap-analysis, risk-diagnostic, growth-lever-selector]
owned_by_agents: [strategy-agent]
---

# Skill: Exit Readiness Analysis

## Purpose
Capture the founder's intended exit path, honestly score how ready the business is for it, and enforce that major decisions stay aligned with that intent. Answers "where do I want to go, how will I get there, and what will it look like when I arrive?" — and keeps day-to-day strategy from quietly working against the founder's end goal.

## When to Use
- The founder asks "am I ready to sell?", "how do I get this business ready to hand off?", "what's my exit worth?"
- When setting or revisiting long-term direction (exit intent should anchor `strategic-planning`).
- Before a major, hard-to-reverse decision, to check it against the exit path.
- Periodically, to track readiness improvement over time.

## When NOT to Use
- The founder needs the current whole-company health picture → `business-health-diagnostic`.
- The task is a formal business valuation for a transaction → escalate to an accountant/valuation professional (this skill estimates readiness, not a defensible sale price).
- Legal deal structuring/negotiation → attorney.
- The founder wants growth options, not exit → `growth-lever-selector`.

## Required Context
Reads `founders` (exit intent, timeline, financial needs), `company` (structure, owner-dependence), `finance` (revenue, margin, cash, financials quality), `customers` (concentration, retention), `offerings`, `team`/`operations` (does the business run without the founder?), `metrics`, `risks`, `strategy`, `goals`. Requires the founder's exit intent and timeline; without them, the skill first elicits them.

## Inputs
```yaml
input:
  exit_intent: enum(strategic_buyer, financial_buyer, family_or_heirs, employees_or_partners, ipo, close_or_liquidate, keep_indefinitely, undecided)
  exit_horizon: str                   # e.g., "3-5 years", "10+ years", "unclear"
  founder_financial_need: str         # what the founder needs the exit to deliver
  business_snapshot:
    revenue_trend: enum(rising, flat, declining)
    gross_margin_pct: number
    profitability: enum(profitable, breakeven, unprofitable)
    customer_concentration_pct: number   # top-customer share of revenue
    retention_rate_pct: number
    owner_dependence: enum(low, medium, high)   # can it run without the founder?
    financials_quality: enum(clean_audited, clean, informal, poor)
    documented_processes: enum(extensive, partial, minimal)
    recurring_revenue_pct: number
    key_person_risks: [str]
    transferable_assets: [str]          # IP, contracts, brand, systems
  major_decision_under_review: str      # optional: a decision to check for alignment
```

## Missing Information Protocol
1. If `exit_intent` or `exit_horizon` is undecided/unknown, the skill's first job is to elicit them via the exit-clarity questions — do not score readiness against an assumed exit.
2. Pull the business snapshot from memory/integrations; ask the founder only for intent, timeline, and financial need.
3. Never produce a sale-price figure — readiness is scored qualitatively; any dollar valuation is escalated to an accountant/valuation professional.
4. Never assume the founder wants to sell — "keep indefinitely" and "undecided" are valid intents that change the analysis.

## Diagnostic Questions
**Exit clarity (elicit first if unset):** Where do you want to go? How will you get there? What will it look like when you arrive? What does the exit need to give you (financially, personally)?
**Readiness interrogation:** Can the business run without you (owner-dependence)? Are revenues stable/growing and margins healthy? How concentrated are customers? Are financials clean enough for a buyer's diligence? Are processes documented and transferable? What key-person risks would scare a buyer/successor? What are the transferable assets (IP, contracts, brand)?
**Alignment:** Does the current strategy/major decision move the business toward or away from the chosen exit?

## Analysis Framework
Three stages: (1) **Capture** the exit path from the standard option set; (2) **Score readiness** against the value drivers that matter for *that* exit; (3) **Enforce alignment** of major decisions to the exit.
- **Exit option set:** sell to a strategic buyer; sell to a financial buyer; sell/pass to family or heirs; sell to employees/partners; go public (IPO); close/liquidate; keep indefinitely ("die with it"); undecided.
- **Value drivers (readiness dimensions):** revenue stability/growth · profitability & margin · customer diversification (low concentration) · retention/recurring revenue · owner-independence (does it run without the founder) · clean transferable financials · documented processes · transferable assets (IP/contracts/brand) · low key-person risk.
- **Exit-specific weighting:** each exit weights drivers differently (see Decision Rules) — e.g., a financial buyer prizes clean financials + owner-independence + recurring revenue; family succession prizes documented processes + owner-independence; liquidation cares mainly about asset value; "keep indefinitely" reframes the analysis toward durability and continuity rather than sale-readiness.

## Calculations
- **Readiness score (SYNTH, 0–100):** weighted average of the value-driver sub-scores (each 0–1), using the exit-specific weight profile. Bands: **Ready** ≥75, **Nearly Ready** 60–74, **Needs Work** 40–59, **Not Ready** <40.
- **Owner-dependence penalty:** high owner-dependence caps the readiness score at "Needs Work" for any sale/succession exit (a business that can't run without the founder is hard to transfer).
- **Concentration penalty:** `customer_concentration_pct > 30%` reduces the diversification sub-score sharply; `>40%` is a red flag buyers discount for.
- **Horizon check:** compare `exit_horizon` to the estimated time to close the top readiness gaps; if gaps take longer than the horizon, flag a timeline mismatch.
- **NOT computed:** a dollar sale price/valuation multiple — explicitly out of scope; escalate to a professional.
- Value drivers and the exit option set are source-derived; the scoring/weights and bands are SYNTH defaults.

## Decision Rules
- **IF** exit_intent is undecided/unknown **THEN** run exit-clarity elicitation first; do not score against an assumed exit.
- **IF** exit = strategic_buyer **THEN** weight strategic fit, growth, transferable assets/IP, and market position highest.
- **IF** exit = financial_buyer **THEN** weight clean financials, profitability, recurring revenue, and owner-independence highest.
- **IF** exit = family_or_heirs OR employees_or_partners **THEN** weight documented processes, owner-independence, and successor capability highest; involve successor readiness.
- **IF** exit = ipo **THEN** weight scale, growth, audited financials, and governance highest → also escalate to professionals (this is beyond small-business self-service).
- **IF** exit = close_or_liquidate **THEN** weight asset recoverability and obligation wind-down; readiness is about orderly closure, not sale value.
- **IF** exit = keep_indefinitely **THEN** reframe: score durability, continuity, and owner-well-being rather than transfer-readiness.
- **IF** owner_dependence = high **THEN** cap sale/succession readiness at "Needs Work" and make owner-independence the #1 gap.
- **IF** customer_concentration > 40% **THEN** flag as a buyer red flag → `growth-lever-selector` to diversify.
- **IF** financials_quality is informal/poor for a sale exit **THEN** top gap = clean up financials → escalate to accountant.
- **IF** a `major_decision_under_review` moves the business away from the exit **THEN** flag the misalignment to the founder (e.g., deepening owner-dependence when planning to sell).
- **IF** exit_horizon < time-to-close top gaps **THEN** flag a timeline mismatch (either extend horizon or accept a lower-readiness exit).

## Procedure
1. Capture (or elicit) exit intent, horizon, and financial need.
2. Select the exit-specific value-driver weight profile.
3. Score each value driver from the business snapshot; apply owner-dependence and concentration penalties.
4. Compute the weighted readiness score and band.
5. Identify and rank the readiness gaps; estimate time to close each; run the horizon check.
6. If a major decision is under review, run the alignment check against the exit.
7. Recommend the gap-closing sequence and the professionals to involve.
8. Write the exit path + readiness + alignment result to `strategy`/`goals` and a decision record.

## Output
```yaml
output:
  exit_intent: str
  exit_horizon: str
  readiness_score: number             # 0-100
  readiness_band: enum(Ready, Nearly Ready, Needs Work, Not Ready)
  value_driver_scores: {<driver>: number}    # 0-1 each
  penalties_applied: [str]            # owner-dependence cap, concentration, etc.
  readiness_gaps:
    - gap: str
      severity: enum(red_flag, major, minor)
      time_to_close_estimate: str
      action: str
      escalate_to: enum(founder, accountant, attorney, none)
  horizon_mismatch: bool
  alignment_check: {decision: str, verdict: enum(aligned, misaligned, n/a), note: str}
  recommended_next_skills: [str]
  professional_referrals: [str]       # accountant/attorney/valuation professional as needed
```

## Recommendations
Readiness is scored against the value drivers that matter for the *chosen* exit, not a generic checklist — so a family-succession founder isn't told to chase buyer-style growth, and a sell-in-5-years founder is told plainly that a business which can't run without them isn't sellable yet. Gaps are ranked red-flag-first with time-to-close estimates, and the analysis explicitly enforces that major decisions and the strategic plan keep moving toward the exit rather than away from it.

## Execution Opportunities
- Write/store the exit path and readiness snapshot to `strategy`/`goals` and a decision record — reversible, LOW.
- Create internal gap-closing tasks (e.g., "document fulfillment process," "reduce top-customer share") — reversible, LOW.
- Run alignment checks on major decisions and flag misalignments — reversible, LOW.
- Draft a founder exit-readiness brief and referral list — reversible, LOW.
This skill never executes a sale, signs a letter of intent, engages a broker, or commits to a transaction — all irreversible/legal/financial and approval-gated.

## Human Approval Requirements
- Any actual exit action — engaging a broker/banker, signing an LOI or sale agreement, initiating succession transfer, liquidating — requires founder approval and the appropriate professional (attorney/accountant); out of scope for this skill.
- Sharing confidential financials with any external party (buyer, advisor) requires founder approval.
- Per `AUTONOMY_AND_APPROVAL_MODEL.md`, contracts and financial/legal commitments always route to a human.

## Escalation Conditions
- **Any real transaction step (LOI, broker, sale, succession transfer)** → founder + attorney + accountant.
- **A dollar valuation is requested** → accountant/valuation professional (not produced here).
- **Tax implications of an exit** → accountant/tax professional.
- **IPO intent** → founder + professionals (beyond small-business self-service scope).
- **Major decision misaligned with exit** → founder (strategic call).
- **Exit intent conflicts with the founder's financial need** (e.g., readiness/horizon can't meet the need) → surface honestly to the founder.

## KPIs
- Readiness trajectory: readiness score improvement over time toward the target band.
- Gap closure: % of red-flag/major gaps closed before the exit horizon.
- Alignment: % of major decisions checked and kept aligned with the exit.
- Owner-independence: reduction in owner-dependence rating over time.

## Monitoring
Re-score readiness periodically and after each gap closes. Watch for decisions that increase owner-dependence or concentration (they erode readiness). Track the horizon vs. remaining gap time. Re-elicit exit intent if the founder's life goals shift.

## Follow-Up
- Time-triggered: annually, or more often as the horizon nears.
- Event-triggered: before any major decision (alignment check), after a big change in the business, or when the founder signals an intent change.
- Anchors `strategic-planning` (exit intent shapes objectives) and feeds `growth-lever-selector`/`resource-gap-analysis` for gap closure.

## Guardrails
- Never produce a sale price or valuation multiple — escalate to a professional.
- Never assume the founder wants to sell; honor "keep indefinitely" and "undecided."
- Never execute or commit to any exit action — recommend and prepare only.
- Handle financials/exit intent as confidential; never share externally without founder approval.
- Enforce alignment gently — surface misalignments to the founder as their decision, not a veto.

## Example
**Founder input:** "I'd like to sell to a strategic buyer in about 4 years and net enough to retire. The business is profitable, ~$1.1M revenue, growing slowly, gross margin healthy, but honestly it falls apart when I take two weeks off. Top customer is ~35% of revenue. Financials are done by me in spreadsheets. Processes are mostly in my head."
**Reasoning:** Exit = strategic_buyer, horizon 4 yrs. Weight profile: strategic fit/growth/transferable assets/market position + owner-independence. Owner-dependence = high → readiness capped at "Needs Work." Concentration 35% → diversification penalty (approaching red-flag). Financials informal → major gap for buyer diligence. Processes minimal → transferability gap. Readiness score ≈ 46 → **Needs Work**.
**Gaps (ranked):** (1) owner-independence — hire/train a manager, document operations [major, ~12–18 mo, founder + `resource-gap-analysis`]; (2) clean up financials — move to proper bookkeeping/accountant [major, ~3–6 mo, escalate to accountant]; (3) reduce top-customer concentration below 30% [major, ~12 mo, `growth-lever-selector`]; (4) document processes [minor→major, ongoing]. horizon_mismatch: false (4 yrs > ~18 mo top-gap time). alignment_check: n/a (no decision under review). professional_referrals: accountant (financials/tax), later attorney (deal).
**Executed vs. approval:** Stored the exit path + "Needs Work (46)" readiness snapshot, created gap-closing tasks, drafted the founder brief and referral list (all L1). No transaction step taken; when the founder is ready to engage a buyer/broker, that routes to founder + attorney + accountant.

## Provenance
SOURCE. Implements the source's Exit Strategy capture (the standard exit option set), the exit-clarity questions ("where do you want to go / how will you get there / what will it look like"), and the Growth-Plan requirement to include an exit strategy and align decisions to it — extended with a value-driver readiness score (SYNTH weights/bands). Dollar valuation is deliberately out of scope and escalated. See `internal/PROVENANCE_MAP.md`.
