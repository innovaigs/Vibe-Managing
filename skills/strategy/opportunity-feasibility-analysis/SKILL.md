---
name: opportunity-feasibility-analysis
domain: strategy
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [company, founders, customers, offerings, finance, market, goals, strategy]
writes: [strategy, decisions, goals]
related_skills: [idea-expansion, growth-lever-selector, competitive-intelligence-analysis, resource-gap-analysis, risk-diagnostic, strategic-planning]
owned_by_agents: [strategy-agent]
---

# Skill: Opportunity Feasibility Analysis

## Purpose
Turn a raw business idea into either a validated, evidence-backed growth opportunity or an honest "not yet / not this." The skill screens an idea against the characteristics of a real opportunity, writes a crisp opportunity statement, stress-tests it across six feasibility dimensions, and returns a go / refine / kill decision plus the exact research gaps to close before committing money or time.

## When to Use
- The founder proposes a new idea: "Should we pursue X?", "I'm thinking about adding a new service / market / product line."
- An idea has emerged from `idea-expansion` and needs to be pressure-tested before resourcing.
- A growth lever from `growth-lever-selector` needs validation before it becomes a plan.
- Before allocating capital, hiring, or committing to any new offering or market.

## When NOT to Use
- The founder wants to generate options, not test one — use `idea-expansion` first.
- The idea is already validated and the founder wants a plan — use `strategic-planning` / `initiative-prioritization`.
- The question is which of several growth avenues to explore — use `growth-lever-selector`.
- Deep competitor benchmarking is the whole task — use `competitive-intelligence-analysis` (this skill calls it for the Competition dimension).

## Required Context
Reads `company` (current model, competitive advantage, stage), `founders` (goals, capacity, risk appetite), `customers` (current segments), `offerings` (current products/margins), `finance` (available capital, margins), `market` (segment sizes, trends), `goals`. Also needs the founder's raw idea and any customer-conversation evidence. Each fact's `confidence`/`as_of` governs how much weight it carries; unvalidated market assumptions must be flagged, not treated as fact.

## Inputs
```yaml
input:
  idea_description: str              # the raw idea in the founder's words
  target_customer_hypothesis: str    # who it's for
  competitive_advantage_claim: str   # the advantage this is meant to leverage
  founder_goals: [str]               # personal + business goals to fit against
  available_capital: number          # capital the founder could commit
  evidence:
    customer_conversations: int      # how many target customers actually spoken to
    customer_learnings: [str]        # what those conversations revealed
    market_data: object              # segment size, growth, trends if known
    competitor_data: [object]        # known competitors offering same/similar
  current_business:
    competitive_advantages: [str]
    gross_margin_pct: number
    current_segments: [str]
```

## Missing Information Protocol
1. Pull market/competitor/financial data from integrations and memory before asking.
2. For any feasibility question that cannot be answered, DO NOT guess — log it as a data gap with a named source and where to obtain it (this is the core operating rule of the framework).
3. Ask the founder ONE batched set only for facts only they hold (their goals, capital they'd commit, customers they've actually spoken to).
4. Never assume market size, growth rate, or competitor capability. An unvalidated number becomes a research task, not an input to the verdict.

## Diagnostic Questions
**Five-characteristics screen (gate):**
1. Does it solve a real customer pain/need?
2. Does it offer a new product/service OR reach a new market?
3. Does it leverage an existing competitive advantage?
4. Can it be profitable?
5. Does it fit the founder's personal life and goals ("Fits me")?

**Opportunity-statement inputs (the five questions):** the customer pain discovered; the new market/customer or new product/service; the current competitive advantage and how this leverages it; why it will be profitable; how it fits the founder's life and goals.

**Six-dimension feasibility interrogation:**
- **The Opportunity:** exact pain; exact offering; impact on the current business; risks (financial, operational, team, personal).
- **Potential Customers:** who/what segment; how they differ from current customers; how many spoken to directly and what was learned.
- **Market:** segment size; growth past 1/3/5 yrs; expected growth next 6 mo and 1/2/3/5 yrs; favorable/unfavorable trends (economic, demographic, technological, government) and the response; where the first 5, next 25, next 100 customers come from; adjacent reachable segments.
- **Competition:** who offers same/similar; what you provide they cannot; ease of your entry; ease of others' entry (barriers).
- **Financial:** capital to launch; price the segment will pay; product cost structure; resources needed (materials, supplies, equipment, location).
- **You (founder fit):** why you want this; benefit and cost to you/family/employees/partners/investors; mental/physical/emotional readiness.

## Analysis Framework
The Idea-to-Growth-Plan pipeline, gated:
1. **Idea** — capture the raw notion.
2. **Five-Characteristics Screen** — pass/fail each; a fail routes back to ideation or flags elevated risk (see Decision Rules).
3. **Opportunity Statement** — assemble the five answers into one or two EEC-compliant sentences (efficient, effective, compelling).
4. **Six-Dimension Feasibility Assessment** — interrogate each dimension; answer from data where possible, else log a data gap.
5. **Three-Growth-Factors check (3 Ms)** — confirm Management, Market, and Money are each adequate for the intended growth.
6. **Verdict** — go / refine / kill, with a risk list and a prioritized research task list.

## Calculations
- **Gross margin on the new offering** = `(price − COGS) / price × 100`. Compare to the founder's target and to current business margin. (The source's worked example targeted ~50% gross margin plus an offsetting cost reduction — illustrative, not a benchmark.)
- **Capital-to-launch vs. available capital**: `available_capital − capital_required`. If negative, financing becomes a gating data gap and a 3M "Money" flag.
- **Revenue-lift targeting** = express the opportunity as a target % revenue lift or a target capture of an addressable market (e.g., "capture X% of a segment of size S → S × X% revenue"). Illustrative targeting pattern, not a benchmark.
- **Market-timeline growth capture**: quantify segment size and growth across the fixed horizon set — past 1/3/5 yrs and next 6 mo, 1/2/3/5 yrs.
- **Customer-acquisition ladder**: plan explicitly for the first 5 → next 25 → next 100 customers; if the source of the first 5 is unknown, that is a Critical data gap.
- **Evidence sufficiency (heuristic, SYNTH):** direct customer conversations — 0 = unvalidated (kill or refine); 1–4 = weak signal; 5–14 = emerging validation; ≥15 = credible demand signal.

## Decision Rules
- **IF** it does not solve a customer pain/need **THEN** it is not a valid opportunity → return to `idea-expansion`.
- **IF** it neither offers a new product/service NOR reaches a new market **THEN** it is not a growth opportunity → kill or reframe.
- **IF** it does not leverage an existing competitive advantage **THEN** flag elevated execution risk (entering from weakness) — refine, don't auto-kill.
- **IF** there is no credible path to profitability **THEN** do not advance to full feasibility → kill or refine the economics first.
- **IF** it does not fit the founder's life/goals **THEN** flag founder-fit risk regardless of market attractiveness → surface to founder before proceeding.
- **IF** the five opportunity questions cannot be clearly answered **THEN** classify as "just an idea," not a tangible opportunity → refine.
- **IF** any feasibility question is unanswerable **THEN** log a data gap with a named source and assign it as a research task before committing resources.
- **IF** any of Management, Market, or Money is inadequate **THEN** the growth is at risk → address the weak factor first (verdict = refine).
- **IF** direct customer conversations = 0 **THEN** verdict cannot be "go" — minimum is refine with a "talk to ≥5 target customers" task.
- **IF** all five characteristics pass AND no Critical data gaps remain AND 3 Ms adequate **THEN** verdict = go.

## Procedure
1. Capture the raw idea, target customer, advantage claim, and founder goals.
2. Run the five-characteristics screen; record pass/fail and route per Decision Rules.
3. Assemble the opportunity statement from the five questions; check it against EEC.
4. Interrogate all six feasibility dimensions; answer from data or log a data gap (source + how to obtain) for each unanswered item.
5. Run the calculations (margin, capital gap, revenue-lift target, acquisition ladder, evidence sufficiency).
6. Run the 3M adequacy check.
7. Compile the risk list (financial, operational, team, personal).
8. Rank the data gaps by how blocking they are to a commitment decision.
9. Issue the verdict (go / refine / kill) with rationale, opportunity statement, risk list, and prioritized research tasks.
10. Write the opportunity + verdict to `strategy` and a decision record to `decisions`; propose research tasks (do not commit resources).

## Output
```yaml
output:
  opportunity_statement: str          # 1-2 EEC sentences: offering + segment + pain + advantage + profit mechanism
  five_characteristics:
    solves_pain: {pass: bool, note: str}
    new_product_or_market: {pass: bool, note: str}
    leverages_advantage: {pass: bool, note: str}
    can_be_profitable: {pass: bool, note: str}
    fits_founder: {pass: bool, note: str}
  feasibility:
    opportunity: {findings: str, risks: [str]}
    customers: {findings: str, conversations_held: int, gaps: [str]}
    market: {size: str, growth_trend: str, favorable_trends: [str], unfavorable_trends: [str], acquisition_ladder: str, gaps: [str]}
    competition: {who: [str], our_edge: str, our_entry_ease: str, others_entry_barriers: str, gaps: [str]}
    financial: {capital_required: number, capital_gap: number, target_price: number, target_margin_pct: number, gaps: [str]}
    founder_fit: {motivation: str, costs: [str], readiness: str, gaps: [str]}
  three_M_check: {management: enum(adequate, weak, unknown), market: enum(adequate, weak, unknown), money: enum(adequate, weak, unknown)}
  risk_list: [ {risk: str, type: enum(financial, operational, team, personal), note: str} ]
  data_gaps: [ {question: str, dimension: str, source_to_close: str, blocking: bool} ]
  verdict: enum(go, refine, kill)
  verdict_rationale: str
  recommended_next_skills: [str]
```

## Recommendations
The verdict is formed by the gate logic, not by vote-counting: any Critical data gap or failed hard characteristic caps the verdict at "refine" (or "kill" for pain/profitability failures). Research tasks are prioritized by how blocking they are to a resource commitment — the founder gets a short, ordered list of exactly what to learn next and where. Recommendations weigh impact (revenue-lift target), cost (capital gap), risk (the risk list), and reversibility (how committed the founder becomes by starting).

## Execution Opportunities
- Write the validated opportunity + verdict to `strategy` and a decision record to `decisions` — reversible, LOW.
- Create internal research tasks for each data gap (with named sources) — reversible, LOW.
- Draft the opportunity statement and a one-page founder brief — reversible, LOW.
- Trigger `competitive-intelligence-analysis` and `resource-gap-analysis` as follow-on analyses — reversible, LOW.
This skill never commits capital, signs anything, or launches an offering — those are downstream, approval-gated.

## Human Approval Requirements
- The verdict is a recommendation; committing capital, hiring, launching the offering, or entering the market all require founder approval and are out of scope for this skill.
- Any research task that itself costs money (e.g., paid market study) is flagged for founder approval.
- Per `AUTONOMY_AND_APPROVAL_MODEL.md`, no irreversible/financial action is auto-executed.

## Escalation Conditions
- **Capital required exceeds available capital / implies new financing** → founder (+ recommend accountant).
- **Opportunity depends on a legal/regulatory/IP question** (licensing, patent, compliance) → attorney.
- **Founder-fit fails but market is attractive** → founder (values/life-goals call, not a data call).
- **Pervasive low-confidence market inputs** → surface uncertainty; do not issue a confident "go."

## KPIs
- Decision quality: % of "go" opportunities that hit their revenue-lift/margin target within the planned horizon.
- Kill efficiency: bad ideas killed or refined before capital was committed.
- Data-gap closure rate: % of logged research tasks completed before commitment.
- Statement quality: opportunity statements that pass EEC on first review.

## Monitoring
Track whether logged data gaps get closed and whether the opportunity's assumptions (segment size, price, conversion) hold once tested. Re-run feasibility if a Critical assumption is invalidated. Watch the acquisition ladder — failure to land the first 5 customers is an early kill signal.

## Follow-Up
- Re-run when a Critical data gap is closed (to upgrade refine → go/kill).
- Re-run before final capital commitment.
- Feed a "go" verdict into `strategic-planning` and `resource-gap-analysis`.

## Related Skills
Upstream: `idea-expansion`, `growth-lever-selector`. Calls: `competitive-intelligence-analysis`, `resource-gap-analysis`, `risk-diagnostic`. Downstream: `strategic-planning`, `initiative-prioritization`.

## Guardrails
- Never present an unvalidated market assumption as fact — log it as a data gap.
- Never issue "go" when direct customer conversations = 0 or a hard characteristic (pain, profitability) fails.
- Do not advise on regulated matters (legal/IP/tax) — route to specialists.
- Keep the opportunity statement honest: it must state a real profitability mechanism, not aspiration.
- Founder-fit is a first-class gate — an attractive market that violates the founder's life goals is a flagged risk, not a silent "go."

## Example
**Founder input:** "A refill/subscription line for our existing cleaning-products customers — sell concentrated refills so they stop buying disposable bottles."
**Screen:** solves pain (recurring cost + waste) ✓; new product for existing market ✓; leverages advantage (existing loyal customer base + brand) ✓; profitable? plausibly ✓; fits founder (wants recurring revenue) ✓ — all five pass.
**Opportunity statement:** "Offer concentrated refills to our existing loyal cleaning-products customers who dislike repurchasing disposable bottles, leveraging our brand and direct customer relationships; we target a 50% gross margin while cutting per-unit packaging cost."
**Feasibility:** Customers — 6 existing customers interviewed, 5 want it (emerging validation). Market — segment size unknown → data gap (source: current CRM base + category data). Competition — two national brands offer refills but not to this niche; our edge = existing relationship; entry barrier for others = our customer loyalty. Financial — capital required $18k for filling equipment; available $40k → capital OK; target price set; margin modeled at 50%. Founder fit — strong. 3M: Management adequate, Market unknown (gap), Money adequate.
**Verdict:** refine → go pending one Critical gap (quantify segment size / addressable refill demand). Research tasks: (1) size the refill-willing base from CRM (blocking); (2) confirm unit COGS with supplier; (3) talk to 10 more customers to firm up the demand signal.
**Executed vs. approval:** Wrote opportunity + "refine" verdict to `strategy`, created three research tasks, drafted founder brief (all L1). No capital committed — equipment purchase held for approval pending gap closure.

## Provenance
SOURCE. Directly implements the Idea-to-Growth-Plan pipeline, the Five Characteristics of a Good Opportunity, the Opportunity Statement framework, the six-dimension Feasibility Assessment for Growth, the Three Growth Factors (3 Ms), the EEC standard, and the "log every unanswerable question as a sourced data gap" operating rule from the foundation/strategy domain. See `internal/PROVENANCE_MAP.md`.
