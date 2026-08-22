---
name: risk-diagnostic
domain: risk
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [risks, company, finance, operations, market, team, strategy, metrics]
writes: [risks, metrics]
related_skills: [crisis-response-planning, business-continuity-plan, initiative-prioritization, employment-compliance-scan, legal-escalation-router]
owned_by_agents: [risk-agent, business-analyst-agent]
---

# Skill: Risk Diagnostic (Scored Risk Register)

## Purpose
Turn a founder's scattered worries into a disciplined, scored risk register so the business knows which threats matter most, who owns each one, what will be done about it, and which early-warning number to watch. This is how a small business stops being blindsided: every material risk gets a likelihood × impact score, a mitigation plan, an accountable owner, and a dashboard warning signal that fires *before* the risk lands.

## When to Use
- The founder asks "what could go wrong?", "what are we exposed to?", or "what keeps me up at night?"
- On a periodic cadence (quarterly by default, monthly for a fragile or fast-changing business).
- Before any major bet: new product, new market, hiring wave, large contract, financing, expansion.
- After a near-miss, a competitor move, a regulatory change, or a new dependency (single big customer, single key employee, single supplier).
- When another skill flags a risk (e.g. cash-flow diagnostic finds thin runway; employment-compliance-scan finds a gap) and it needs to be logged, scored, and tracked.
- Founder phrasings: "Am I too dependent on that one client?", "We're growing fast — what breaks first?", "Rank my risks for me."

## When NOT to Use
- A risk is already *materializing right now* (fire, outage, lawsuit served, key customer just fired you) → use `crisis-response-planning`.
- The concern is specifically single-point-of-failure / concentration (one customer = most of revenue, one person holds all the knowledge) and the founder wants diversification actions → run this to score it, then hand to `business-continuity-plan`.
- The risk is a live legal/employment matter (harassment claim, misclassification, contract dispute) → score it here but immediately route via `legal-escalation-router`; do not attempt to resolve the legal question.
- The founder wants to prioritize *initiatives* (not risks) → use `initiative-prioritization`.

## Required Context
Before running, the agent should pull from Business Memory:
- `company`: stage, entity_type, jurisdictions, business_model, headcount, locations.
- `finance`: cash runway, revenue concentration, margin trend, debt/covenants (for financial risks).
- `operations`: key processes, vendors + `dependency_risk`, tools, capacity/constraint flags.
- `market`: competitors + `threat_level`, trends, `regulatory_context`.
- `team`: headcount, key-person roles, turnover.
- `strategy`: current priorities and growth initiatives (each initiative carries risk).
- `risks`: any existing register (to update rather than duplicate).
If memory is sparse, the skill can still run from a guided brainstorm, but it must label the register `confidence: low` until the context is verified.

## Inputs
```yaml
input:
  business_context:
    stage: enum(startup, established, scaling, mature)   # from company
    headcount: int                                       # drives which risks/laws attach
    jurisdictions: [str]
    revenue_concentration_pct: number        # % of revenue from largest customer (optional)
    cash_runway_months: number               # optional, from finance
  candidate_risks:                           # from founder brainstorm and/or memory scan
    - description: str                       # e.g. "Largest customer is 45% of revenue"
      category: enum(financial, operational, market, legal, people, concentration, continuity)
      likelihood_estimate: int               # 1-5, optional (agent will elicit/estimate)
      impact_estimate: int                   # 1-5, optional
  scope: enum(full_register, single_risk, refresh)   # full build, add one, or periodic re-score
  cadence: enum(monthly, quarterly)          # review frequency to set on the register
  risk_appetite: enum(averse, moderate, tolerant)    # optional founder stance
```

## Missing Information Protocol
- **Fetch first:** pull likelihood/impact drivers from memory and connected data (concentration % from finance, vendor dependency from operations, headcount from company) before asking the founder.
- **Compute where possible:** revenue concentration, runway, turnover rate can be computed, not guessed.
- **Ask ONE concise batch** only for what can't be fetched or computed — typically: the starter-checklist brainstorm, likelihood estimates for novel risks, and who should own each risk. Do not interrogate the founder risk-by-risk in separate turns.
- **Never assume:** never invent a likelihood or impact number, never assign an owner the founder hasn't confirmed, never mark a risk "mitigated" without evidence, and never downgrade a legal/safety risk to make the register look better.
- If a required input stays unknown, log the risk with `confidence: low` and add "quantify this risk" as its first mitigation step.

## Diagnostic Questions
Use the **starter risk checklist** to surface risks the founder hasn't named (SOURCE — Risk Audit Tool):
- Increased competition (local → national → global)?
- Rising labor costs (wages, benefits, payroll taxes)?
- Regulatory or legislative change affecting the business?
- Founder/family health, availability, or life-status change (key-person risk)?
- Growing too fast — demand exceeding capacity, quality slipping?
- Growing too slow — stagnation, hire/fire cycling?
- Change in customer payment behavior or in supplier payment demands (cash risk)?
- Technology or process advances making the offering stale?
- Owner losing interest / burnout?
- Concentration: one customer, one supplier, one employee, one channel, one system?
Then for each candidate risk: How likely is it (1–5)? If it happened, how bad (1–5)? What single number would rise or fall *before* it hits (the warning signal)? Who is accountable? By when must a plan be in place?

## Analysis Framework
This skill runs two source frameworks together:

**1. Risk vs. Uncertainty 2×2 (classification).** Plot each threat on Probability (Low/High) × Impact (Low/High):
- **High probability, Low impact** → manage with standard operating procedures + insurance.
- **High probability, High impact** → manage with insurance **and** a written contingency plan.
- **Low probability, Low impact** → non-event; minimal attention.
- **Low probability, High impact** → **potential crisis / blindside** — the dangerous quadrant. Cannot be handled by data/forecasts alone; requires insurance + contingency plan + an entrepreneurial-mindset response, and is the natural handoff to `crisis-response-planning`.
Core distinction: a **Risk** lives in the "known world" (manageable with data and forecasts); an **Uncertainty** lives in the "unknown world" (many variables, little data). Flag uncertainties so the founder knows they can't simply be forecast away.

**2. Risk Audit Tool (register).** For the top 4–5 risks, build a register with six columns: (1) Key Risk, (2) Risk Score, (3) Contingency/Mitigation Steps, (4) Person Accountable, (5) Deadline (for the plan + owner to be in place), (6) Warning-Signal Metric (added to the dashboard). Then review the whole register for **themes** (are most risks financial? people? concentration?) and **coverage gaps** (any risk with no owner or no metric).

The two frameworks connect: the 2×2 quadrant sets the *handling strategy*; the score sets the *priority order*; the warning-signal metric makes the risk *monitorable* on the Business Dashboard.

## Calculations
- **Likelihood scale:** integer **1–5** (1 = rare, 5 = almost certain).
- **Impact scale:** integer **1–5** (1 = negligible, 5 = business-threatening).
- **Risk Score = Likelihood × Impact** → range **1–25**. (This maps the source's 1–10 severity idea onto the memory schema's `likelihood(1-5) × impact(1-5) → score`.)
- **Priority bands (SYNTHESIZED defaults, configurable by `risk_appetite`):**
  - Score **1–4** → Low / non-event (monitor lightly).
  - Score **5–9** → Moderate (SOP + insurance; owner optional).
  - Score **10–14** → High (written contingency plan + named owner + deadline + warning metric required).
  - Score **15–25** → Critical (contingency plan + owner + deadline + warning metric **and** escalation to founder; if it sits in the Low-probability/High-impact quadrant, prepare a crisis plan).
- **2×2 mapping from 1–5 estimates:** Likelihood ≥3 = "High probability"; Impact ≥3 = "High impact".
- **Concentration risk trigger (SYNTHESIZED):** any single customer > **20–25%** of revenue, single supplier as sole source of a critical input, or a single person as sole holder of a critical capability = automatic concentration/continuity risk regardless of computed score.
- **Warning-signal threshold examples (SOURCE + growth-execution knowledge):** cash runway < 6 months; win rate on proposals < 40%; burn rate > 15% over plan; gross-margin compression > 3%; employee turnover > 20% annually; largest-customer share rising toward its limit. Each high/critical risk gets one such metric + threshold.

## Decision Rules
- IF a threat is **Low probability + High impact** THEN classify as potential crisis/blindside: require insurance + contingency plan, and prepare a handoff to `crisis-response-planning`. (SOURCE)
- IF a threat is **High probability + High impact** THEN require both insurance and a written contingency plan. (SOURCE)
- IF a threat is **High probability + Low impact** THEN manage via standard operating procedures / insurance. (SOURCE)
- IF a threat is **Low probability + Low impact** THEN classify as a non-event; do not over-invest. (SOURCE)
- IF a risk **Score ≥ 10** THEN it requires a written contingency plan, a named accountable owner, a deadline, and a dashboard warning metric. (SOURCE)
- IF a risk **Score ≥ 15** THEN also escalate to the founder for explicit acknowledgement. (SYNTHESIZED)
- IF any risk lacks an accountable owner OR a warning metric THEN flag the register as having a coverage gap — it is not complete. (SOURCE)
- IF a single customer/supplier/employee/channel exceeds the concentration trigger THEN log a concentration + continuity risk and recommend `business-continuity-plan`. (SYNTHESIZED)
- IF a risk is legal, employment, tax, or contractual in nature THEN score it but route the *response* through `legal-escalation-router` — do not draft the legal remedy here. (SOURCE — legal guardrail)
- IF the threat is an **uncertainty** (unknown world, little data) THEN mark it as such and note it cannot be managed by forecast alone; favor optionality/contingency over precise prediction. (SOURCE)
- IF a warning-signal metric crosses its threshold on the dashboard THEN activate that risk's contingency plan and notify its owner. (SOURCE)

## Procedure
1. **Gather context** from memory (`risks`, `finance`, `operations`, `market`, `team`, `company`, `strategy`). Note confidence.
2. **Surface risks** by running the starter checklist against the business plus scanning memory for structural risks (concentration, thin runway, key-person, vendor dependency, regulatory).
3. **Deduplicate & categorize** each risk into one of: financial, operational, market, legal, people, concentration, continuity.
4. **Estimate likelihood (1–5) and impact (1–5)** for each, using data where available and eliciting the rest in one batch. Compute Risk Score = L × I.
5. **Classify** each on the 2×2 and tag Risk vs. Uncertainty.
6. **Rank** by score; keep the top 4–5 as the active register (park the rest in a watchlist).
7. **For each active risk** write: contingency/mitigation steps, accountable owner, deadline for the plan to exist, and one warning-signal metric + threshold.
8. **Review for themes and gaps:** cluster by category; flag any high/critical risk missing an owner or metric; flag concentration patterns.
9. **Wire warning metrics to the dashboard** (via `metrics`) as leading alert signals.
10. **Assemble the register**, mark confidence, list recommended next skills, and route any legal/financial actions for approval.
11. **Set the review cadence** and the next follow-up date.

## Output
```yaml
output:
  register:
    - id: str
      description: str
      category: enum(financial, operational, market, legal, people, concentration, continuity)
      likelihood: int            # 1-5
      impact: int                # 1-5
      score: int                 # likelihood * impact, 1-25
      priority: enum(low, moderate, high, critical)
      quadrant: enum(hi_prob_hi_impact, hi_prob_lo_impact, lo_prob_hi_impact, lo_prob_lo_impact)
      risk_type: enum(risk, uncertainty)
      handling_strategy: str     # SOP+insurance | insurance+contingency | crisis-prep | non-event
      mitigation_steps: [str]
      owner_id: str              # accountable person (founder-confirmed)
      plan_deadline: date        # when mitigation plan + owner must be in place
      warning_metric:
        key: str                 # dashboard metric, e.g. "largest_customer_share_pct"
        threshold: str           # e.g. ">25%" or "<6 months"
        current_value: number
      confidence: enum(low, medium, high)
  watchlist: [ {description, category, score} ]   # scored but below top 4-5
  themes: [str]                  # e.g. "3 of 5 top risks are cash-related"
  coverage_gaps: [str]           # risks missing owner/metric
  recommended_next_skills: [str] # e.g. business-continuity-plan, legal-escalation-router
  approvals_required: [str]      # any actions needing founder/attorney/CPA sign-off
  review_cadence: enum(monthly, quarterly)
  next_review_date: date
```

## Recommendations
Recommendations are prioritized by **Risk Score first, then reversibility and cost of mitigation**. For each active risk the skill proposes the cheapest mitigation that materially lowers likelihood or impact (prefer reversible, low-cost actions first: a process change or a contract clause before an insurance purchase before a structural change). It explicitly separates *mitigations the agent can prepare* (draft an SOP, set up a dashboard metric, create a task) from *mitigations requiring a spend or a legal/HR decision* (buy insurance, sign a contract, restructure), which are surfaced as approval items. Ties are broken toward risks in the Low-probability/High-impact "blindside" quadrant, because those are the ones that kill businesses that never saw them coming.

## Execution Opportunities
- **Create the risk register in memory** (`risks`) — reversible, LOW risk → may auto-execute at L1 as a draft for founder confirmation.
- **Add warning-signal metrics to the dashboard** (`metrics`) — reversible, LOW → prepare/auto at L1.
- **Create mitigation tasks** with owners and deadlines (internal task system) — reversible, LOW → prepare at L1.
- **Draft contingency-plan documents / SOPs** — reversible, LOW → draft for approval.
- **Schedule the next review** (internal reminder) — reversible, LOW.
- Purchasing insurance, signing contracts, restructuring, or any spend → **never executed by this skill**; surfaced as approval items only.

## Human Approval Requirements
Per `AUTONOMY_AND_APPROVAL_MODEL.md`, hold for founder approval before execution:
- Any mitigation that spends money (insurance premiums, tooling, hires) — HIGH if above threshold.
- Any mitigation that is a legal, contractual, tax, or employment action — always route to the relevant professional first.
- Assigning a *named person* as accountable owner (the founder confirms ownership; the agent proposes).
- Marking a risk as "accepted" / consciously not mitigated — the founder must own that decision, and it is recorded in `decisions`.
The register itself (analysis) needs no approval; the *actions* it recommends do.

## Escalation Conditions
- **Founder:** any Critical (score ≥ 15) risk; any risk the founder must consciously accept; any concentration risk above trigger.
- **Accountant / CPA:** financial risks touching tax, covenants, solvency, or cash beyond threshold.
- **Attorney (via `legal-escalation-router`):** any legal, contractual, IP, employment, or regulatory risk — this skill scores it, counsel handles the remedy.
- **HR / attorney:** people risks involving a specific employee, protected class, or performance action.
- **Insurance broker:** where insurance is the recommended handling.
- Escalation messages must include: the risk, its score and quadrant, what the agent knows, its confidence, the decision needed, and the recommended mitigation with rationale.

## KPIs
- % of top risks with a named owner, deadline, and warning metric (target 100%).
- % of warning metrics actually wired to the dashboard and monitored.
- Lead time: warning signal fires *before* the risk materializes (measured on any risk that lands).
- # of open critical risks trending down over successive reviews.
- Register freshness: days since last review vs. cadence.
- Reduction in "blindside" events (Low-prob/High-impact risks that materialized without a plan).

## Monitoring
After the register is built, the Business Analyst Agent watches every warning-signal metric against its threshold. Any breach triggers the linked contingency plan and notifies the owner. The skill also watches for *new* structural risks (a customer growing into concentration, runway shortening, a new regulation) and for stale mitigations (plan_deadline passed with no plan → execution-risk flag).

## Follow-Up
- **Time-triggered:** re-run at the set cadence (quarterly default; monthly if any critical risk is open or the business is fragile/scaling fast).
- **Event-triggered:** re-run before any major decision, after a near-miss, when headcount crosses an employment-law threshold, when a new dependency appears, or when a warning metric breaches.
- Each re-run re-scores existing risks, retires resolved ones (recording the outcome in `decisions`), and promotes watchlist items that have grown.

## Related Skills
- `crisis-response-planning` — when a Low-prob/High-impact risk becomes real, or to pre-build the plan for one.
- `business-continuity-plan` — for concentration / single-point-of-failure risks needing diversification.
- `initiative-prioritization` — to sequence mitigation initiatives against other work.
- `legal-escalation-router` / `employment-compliance-scan` — for legal and employment risks.
- `cash-flow-diagnostic`, `financial-ratio-analysis` — feed and receive financial risks.
- `executive-dashboard-builder` — hosts the warning-signal metrics.

## Guardrails
- **Analysis only auto-runs; actions do not.** No insurance, contract, spend, hire, or legal step is executed by this skill.
- **Never fabricate scores or owners.** Unknown likelihood/impact → `confidence: low` + "quantify this risk" as step one; never invent a number to complete the grid.
- **Legal/compliance/employment risks are scored, not solved here** — always routed to counsel/HR; nothing this skill writes may read as legal advice.
- **Do not downgrade safety, legal, or solvency risks** to improve the register's appearance.
- **Uncertainties are labeled as such** — the skill must not present an unforecastable uncertainty as a tidy managed risk.
- **Privacy:** owner assignments and any sensitive risk (litigation, health, insolvency) are stored in restricted memory; never place them in external URLs, payloads, or shared docs.
- **Reversibility bias:** prefer reversible, low-cost mitigations first; flag every irreversible action for approval.

## Example
**Founder input (scaling services firm, 12 employees, 2 states):** "We just landed a huge client and I'm hiring fast. What could go wrong?"

**Skill reasoning:**
- Memory scan + starter checklist surface candidate risks. Data pulled: largest customer now **45%** of revenue; cash runway **5 months**; one senior engineer holds all delivery knowledge; hiring across a second state; no employee handbook.
- Scoring (L × I):
  - Customer concentration (45%): L4 × I5 = **20 → Critical**; Low-prob? No — High/High quadrant; concentration trigger tripped.
  - Key-person dependency (sole delivery knowledge): L3 × I5 = **15 → Critical**; continuity risk.
  - Cash runway < 6 months: L4 × I4 = **16 → Critical**; financial.
  - Growing too fast / quality slips: L4 × I3 = **12 → High**; operational.
  - Multi-state employment compliance gap (no handbook, new jurisdiction): L4 × I3 = **12 → High**; legal → route to counsel.
- Themes: cash + concentration dominate; a clear continuity problem (customer AND person).
- Coverage: assign owners, set warning metrics.

**Output (abridged):**
| Risk | L×I | Score | Priority | Warning metric | Owner | Handling |
|---|---|---|---|---|---|---|
| Customer 45% of revenue | 4×5 | 20 | Critical | `largest_customer_share_pct` > 40% | Founder | Diversify → business-continuity-plan |
| Sole delivery knowledge | 3×5 | 15 | Critical | `bus_factor` = 1 | Ops lead | Document SOPs, cross-train |
| Runway < 6 mo | 4×4 | 16 | Critical | `cash_runway_months` < 6 | CFO agent | Contingency + financing (approval) |
| Growing too fast | 4×3 | 12 | High | `defect_rate` rising | Ops lead | Capacity plan + SOPs |
| Multi-state compliance gap | 4×3 | 12 | High | `states_without_handbook` | Founder | **Escalate to attorney** |

**Executed vs. approval:** the skill *auto-drafted* the register, wired the five warning metrics to the dashboard, and created cross-training + SOP tasks (all reversible, L1). It *held for approval*: any financing move (CFO + founder), and it *escalated* the multi-state employment gap to an attorney via `legal-escalation-router` rather than drafting a handbook itself. It recommended running `business-continuity-plan` next for the concentration + key-person pair. Next review set to monthly while three critical risks are open.

## Provenance
**SOURCE.** Derives from the Foundation & Strategy domain: Risk Audit Tool (risk register — score, mitigation, owner, deadline, warning metric), the Risk vs. Uncertainty 2×2 matrix, the starter-risk checklist, and the Risk-vs-Uncertainty distinction; warning-signal thresholds draw on the Growth Execution domain's risk warning-signals. The 1–5 × 1–5 scoring aligns the source's 1–10 severity idea to the `risks` namespace in `BUSINESS_MEMORY_SCHEMA.md`. Priority bands and concentration triggers are SYNTHESIZED defaults, configurable per business. All source program branding removed.
