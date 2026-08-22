# WORKFLOW_REGISTRY

**Deliverable 6 — Every end-to-end workflow.**

A **Workflow** orchestrates skills and agents to take a major founder intent all the way from words to coordinated action: `Understand → Diagnose → Plan → Execute → Monitor → Adapt`. Workflows are what make Vibe Managing respond to "grow revenue 20%" with a coordinated plan and executed actions instead of advice.

Each workflow has a spec at `workflows/<workflow-name>/WORKFLOW.md` and follows the six-phase shape below. This registry indexes them and details the flagship ones.

**Six-phase shape (every workflow):**
1. **Understand** — retrieve the relevant memory/twin state.
2. **Diagnose** — run diagnostic skills; form & validate hypotheses.
3. **Plan** — produce prioritized initiatives with expected impact, owners, timeline, budget, KPIs.
4. **Execute** — run authorized actions via agents/tools; risk-tier the rest.
5. **Monitor** — register leading indicators + thresholds.
6. **Adapt** — compare expected vs. actual; change the plan; run the next experiment.

---

## Workflow index

| Workflow | Trigger intent | Lead agent | Key skills |
|---|---|---|---|
| `grow-revenue` | "grow revenue / more customers / sales slowed" | Growth | growth-pathway-classifier, variance-diagnosis, marketing-funnel-planner, sales-process-design, pricing |
| `fix-cash` | "running out of cash / profitable but broke" | CFO | cash-flow-diagnostic, working-capital-optimizer, cash-runway-monitor, scenario |
| `should-we-hire` | "can I afford to hire / need to hire" | People + CFO | founder-capacity-diagnostic, hiring-plan-builder, financial-forecast-builder |
| `evaluate-opportunity` | "should we launch / enter this market" | Strategy | opportunity-feasibility-analysis, resource-gap-analysis, financial-forecast-builder, risk-diagnostic |
| `scale-operations` | "can't scale / delivery too slow / too many errors" | Operations | operational-audit, bottleneck-analysis, process-optimization, automation-triage |
| `build-growth-plan` | "build our growth plan" | Growth + Strategy | growth-plan-builder + most foundation/finance/GTM skills |
| `raise-capital` | "we need funding / prepare to raise" | CFO | bankability-assessment, financing-options-analysis, financial-forecast-builder, business-valuation |
| `reduce-spend` | "spending too much / where's the money going" | CFO | financial-statement-analysis (common-size), variance-diagnosis, vendor review |
| `improve-retention` | "churn is rising" | Growth | variance-diagnosis, customer analysis, process-optimization |
| `delegate-and-offload` | "I'm doing too much" | People | founder-capacity-diagnostic, delegation-planner, hiring-plan-builder |
| `prepare-to-exit` | "am I ready to sell" | Strategy + CFO | exit-readiness-analysis, business-valuation, value-driver-analysis |
| `manage-crisis` | acute disruption | Risk | crisis-response-planning, cash-runway-monitor, business-continuity-plan |
| `weekly-review` / `monthly-review` | cadence | Business Analyst | health-diagnostic, monthly-business-review, variance-diagnosis |
| `prepare-negotiation` | "I have a negotiation coming up" | Sales | negotiation-preparation |

---

## Flagship workflow: `grow-revenue`

**Intent examples:** "We need to grow revenue 20% this quarter." · "Sales have slowed down." · "Find out why growth stopped."

### 1. Understand
Retrieve: current & historical revenue, revenue by offering/segment, pipeline, pricing, gross margin, churn, acquisition channels & CAC, capacity/delivery limits, cash runway (constraint on spend).

### 2. Diagnose — find the binding constraint
Run `growth-pathway-classifier` + `variance-diagnosis`, then isolate which constraint is binding:
```
IF traffic/leads down          → demand-generation constraint  → channel-selection, marketing-funnel-planner
IF leads ok but conversion down→ conversion constraint         → website-conversion-audit, sales-process-design
IF conversion ok but churn up  → retention constraint          → improve-retention workflow
IF price/mix eroding margin    → pricing constraint            → break-even-and-pricing-analysis
IF demand ok but can't deliver → capacity constraint           → scale-operations workflow
IF one customer dominates      → concentration risk            → risk-diagnostic (guard growth quality)
```
Validate each hypothesis against the data before acting.

### 3. Plan
Produce a growth hypothesis and 2–4 prioritized initiatives (via `initiative-prioritization`), each with expected revenue impact, owner, timeline, budget, and KPIs. Check total spend against runway with the CFO agent.

### 4. Execute (risk-tiered)
- **Auto (L2, reversible):** build target lists, draft campaigns/content, create CRM tasks, assemble the tracking dashboard, schedule internal-review experiments.
- **Approval:** ad budget, price changes, public content, outbound to customers.

### 5. Monitor
Register leading indicators (traffic, leads, reply rate, conversion, pipeline coverage) and lagging (revenue, CAC, margin, churn) with the Health Engine; set review cadence.

### 6. Adapt
On the weekly/monthly review, run `variance-diagnosis`: if an initiative underperforms its expected impact, diagnose why → adjust or kill → launch the next experiment. Write lessons to the Decision store.

---

## Flagship workflow: `fix-cash`

**Intent examples:** "We're running out of cash." · "Why are we profitable but have no money?"

### 1. Understand
Retrieve: cash balance & accounts, monthly burn, income statement + balance sheet (≥2 periods), A/R & aging, A/P & terms, inventory, debt schedule & covenants, upcoming large outflows.

### 2. Diagnose
Run `cash-runway-monitor` (how long) and `cash-flow-diagnostic` (why): build the net-income→operating-cash bridge and rank drivers.
```
IF net income negative                 → profitability problem → reduce-spend / pricing / grow-revenue
IF DSO rising (A/R up)                  → collections problem   → working-capital-optimizer (collections)
IF DIO rising (inventory up)           → inventory problem     → working-capital-optimizer (inventory)
IF DPO too low (paying too fast)       → payables timing       → renegotiate terms
IF capex/debt principal spike          → financing problem     → debt-service-and-covenant-analysis
IF one-off timing                       → timing               → short-term bridge plan
```

### 3. Plan
Produce a cash-recovery plan: prioritized levers (collections push, inventory reduction, payables timing, cost cuts, pricing, financing) with expected cash freed and timeline; run `scenario-and-sensitivity-analysis` for base/downside. Target: restore runway above threshold.

### 4. Execute (risk-tiered)
- **Auto (L2):** draft collection reminders (for approval to send), flag slow-pay accounts, build the cash dashboard, model scenarios.
- **Approval (always):** sending customer communications, changing payment terms, drawing on credit, cutting costs that affect people/vendors, any financing.
- **Escalate:** accountant/CPA for tax/accounting; founder for all money moves.

### 5. Monitor
Daily cash watch; weekly A/R aging + burn; covenant headroom.

### 6. Adapt
Compare freed-cash actual vs. expected; if collections lag, escalate the lever mix; re-forecast.

---

## Flagship workflow: `should-we-hire`

**Intent examples:** "Can we hire three salespeople?" · "What roles will we need next year?"

### 1. Understand
Retrieve: workload & capacity by function, founder-load index, revenue & pipeline, gross margin, cash & runway, current comp structure, sales productivity (if sales roles).

### 2. Diagnose
Run `founder-capacity-diagnostic` (is the bottleneck the founder? delegable?) and confirm the need is real vs. a process/automation fix (`automation-triage`). For revenue roles, check pipeline supports added capacity.

### 3. Plan
Run `hiring-plan-builder`: define roles, timing, fully-loaded cost, and expected contribution; run `financial-forecast-builder` to test the hire against runway and break-even (hiring economics: months-to-productivity, payback).
```
IF runway after hires < threshold                → do not hire now; stage or bridge first
IF role is revenue-generating & pipeline supports → phase hires to pipeline ramp
IF need is episodic/uncertain                     → contractor/fractional before FTE
IF founder time freed > cost of hire              → strong hire case
```

### 4. Execute (risk-tiered)
- **Auto (L1–L2):** draft job descriptions, interview guides & scorecards, onboarding plans, hiring-plan document.
- **Approval (always):** the hire decision itself, offers, compensation — with HR/legal escalation.

### 5. Monitor
Post-hire: ramp-to-productivity, capacity relief, runway impact vs. plan.

### 6. Adapt
If a hire underdelivers vs. expected contribution by the review point, diagnose (role fit, ramp, pipeline) and adjust the plan.

---

## Flagship workflow: `evaluate-opportunity`

**Intent examples:** "Should we launch this?" · "Is this opportunity worth pursuing?"

1. **Understand:** capture the opportunity; retrieve capabilities, resources, cash, current focus.
2. **Diagnose:** `opportunity-feasibility-analysis` across customer, demand, competition, economics, resources/capability, risk; `resource-gap-analysis`; `assess-growth-opportunity` economics (incremental P&L, investment, break-even, ROI, payback).
3. **Plan:** go / refine / kill with conditions; if go, a phased validation plan with milestones.
4. **Execute:** draft validation experiments & research tasks (auto); commitments (approval).
5. **Monitor:** validation milestones + spend vs. budget.
6. **Adapt:** proceed/pivot/kill at each milestone gate.

---

## Remaining workflows (same six-phase shape)

- **`scale-operations`** — audit → find bottleneck → optimize/automate/document/hire → monitor throughput → adapt.
- **`build-growth-plan`** — assemble foundation + finance + GTM + ops + people outputs into the growth plan; set the review cadence.
- **`raise-capital`** — bankability assessment → gaps → forecast + valuation → financing-option choice → prepare package (approval to submit).
- **`reduce-spend`** — common-size + trend the cost base → rank cuts by impact/risk → vendor review → execute approved cuts → monitor.
- **`improve-retention`** — diagnose churn drivers → fix product/onboarding/service process → monitor cohort retention.
- **`delegate-and-offload`** — founder-capacity-diagnostic → delegation-planner (authority levels) → hire/automate as needed.
- **`prepare-to-exit`** — exit-readiness-analysis → valuation → value-driver actions → readiness plan.
- **`manage-crisis`** — stabilize cash → crisis-response-planning → continuity → staged recovery.
- **`weekly-review` / `monthly-review`** — assemble cadence briefing → variance-diagnosis → reprioritize (see `OPERATING_CADENCE.md`).
- **`prepare-negotiation`** — negotiation-preparation → plan → (human conducts negotiation) → record outcome.

Each is specified in `workflows/<name>/WORKFLOW.md`. All obey the autonomy/approval model: no irreversible action executes without founder approval, and every workflow ends by writing a decision record and scheduling its learning review.
