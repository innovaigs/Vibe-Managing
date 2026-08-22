# SKILL_REGISTRY

**Deliverable 4 — Every skill: purpose, trigger, inputs, outputs, dependencies.**

A **Skill** is a discrete capability an AI agent can perform repeatedly, with typed inputs and a defined output. Skills are the atom of Vibe Managing — every agent action resolves to a skill call. Each skill has its own folder under `skills/<domain>/<skill-name>/` containing a `SKILL.md` built to the standard structure (see `skills/_TEMPLATE/SKILL.md`).

The complete system now contains **160 skills across 22 domains**. This original registry documents the first 78 source-grounded capabilities; the 82 advanced cross-industry capabilities are indexed in [`ADVANCED_SKILL_REGISTRY.md`](ADVANCED_SKILL_REGISTRY.md).

**Provenance tags:** `SOURCE` = grounded in the source material · `SYNTH` = source concepts recombined/extended · `CLAUDE` = model-added to fill a business-necessary gap (see `internal/PROVENANCE_MAP.md`).

Legend for autonomy ceiling (max autonomy the skill's *actions* may reach; analysis is always allowed): **L0** observe · **L1** prepare · **L2** limited · **L3** supervised. No skill auto-executes irreversible actions.

---

## Cross-cutting

| Skill | Purpose | Trigger | Key inputs | Key output | Autonomy | Prov |
|---|---|---|---|---|---|---|
| `business-health-diagnostic` | Whole-company health scan across cash, revenue, margin, customers, ops, people, risk | "how's the business?", scheduled cadence, before any big decision | memory + twin snapshot | ranked findings with Healthy/Needs-Attention/At-Risk/Critical + recommended skills to run next | L1 | SYNTH |

---

## strategy/

| Skill | Purpose | Trigger | Key inputs | Key output | Autonomy | Prov |
|---|---|---|---|---|---|---|
| `opportunity-feasibility-analysis` | Screen & stress-test a business opportunity, produce a clear opportunity statement + go/refine/kill | "should we pursue X?", new idea | opportunity description, market/customer/competitor/financial data, founder goals | feasibility verdict across 6 dimensions, opportunity statement, risk & data-gap list | L1 | SOURCE |
| `idea-expansion` | Diverge then converge on ways to realize an opportunity | "how else could we do this?" | core opportunity | grounded/adjacent/blue-sky idea sets + top picks | L0 | SOURCE |
| `growth-pathway-classifier` | Classify a business's growth shape and stage-normal problems | "why has growth changed?" | historical + projected revenue series | pathway (rapid/incremental/episodic/plateau) + stage-normal vs. exceptional issues + lever | L0 | SOURCE |
| `growth-lever-selector` | Recommend growth avenues from a structured taxonomy | "how should we grow?" | business scope, aspirations, capability/resource assessment | ranked growth vectors with rationale | L1 | SOURCE |
| `resource-gap-analysis` | Inventory resources, classify gaps, prioritize, recommend actions | "what do we lack to do X?" | current assets, opportunity requirements | have/need/action grid by category + prioritized closures | L1 | SOURCE |
| `competitive-intelligence-analysis` | Benchmark competitors on customer-valued dimensions | "who are we up against?" | competitor names, market context, customer priorities | current-vs-aspirational grid + threat levels + research plan | L1 | SOURCE |
| `strategic-planning` | Set objectives, priorities, resource allocation, direction | "what should we focus on?" | goals, health diagnosis, constraints | prioritized objectives + allocation + measurable plan | L1 | SYNTH |
| `initiative-prioritization` | Rank initiatives by impact/effort/cost/risk/dependency | after diagnosis/planning | initiative list + scores | sequenced roadmap | L1 | SOURCE |
| `exit-readiness-analysis` | Capture exit intent, score readiness, enforce alignment | "am I ready to sell?", major decision | exit strategy, financials, value drivers | readiness score + gap list + decision-alignment checks | L1 | SOURCE |
| `social-value-designer` | Design combined social + economic value | mission-driven business | business model, community context | value model (employment/cross-subsidy/donation) + profitability rationale | L0 | SOURCE |

## risk/

| Skill | Purpose | Trigger | Key inputs | Key output | Autonomy | Prov |
|---|---|---|---|---|---|---|
| `risk-diagnostic` | Build & maintain a scored risk register (likelihood × impact), classify threats | "what could go wrong?", periodic | risk brainstorm (guided), business context | register with scores, mitigations, owners, warning-signal thresholds | L1 | SOURCE |
| `crisis-response-planning` | Analyze a crisis, protect the business, find the opportunity in it | acute disruption | crisis description, resources | impact assessment, action plan, resource gaps, lessons | L1 | SOURCE |
| `business-continuity-plan` | Reduce single-point-of-failure and concentration risk | concentration/continuity flag | dependencies (customers, staff, vendors, systems) | continuity plan + diversification actions | L1 | SYNTH |

## finance/

| Skill | Purpose | Trigger | Key inputs | Key output | Autonomy | Prov |
|---|---|---|---|---|---|---|
| `financial-statement-analysis` | Build/validate & interpret income statement, balance sheet, cash-flow statement | "how are our financials?" | statements or transaction log | reconciled statements, common-size, trend callouts | L1 | SOURCE |
| `financial-ratio-analysis` | Compute the full ratio set + DuPont, flag against benchmarks/covenants | "are our numbers healthy?" | IS + BS (+ SCF), optional benchmarks | labeled ratios + healthy/warning/critical + DuPont attribution | L1 | SOURCE |
| `cash-flow-diagnostic` | Explain "profitable but no cash" via a net-income→operating-cash bridge | "why is cash tight?" | IS + BS (two periods) | ranked cash drivers (ΔAR, ΔInv, ΔAP, capex, debt) + fixes | L1 | SOURCE |
| `cash-runway-monitor` | Track burn and time-to-out-of-cash | continuous / "how long do we have?" | cash balance, inflows, outflows | burn rate, runway months, out-of-cash date, alerts | L2 | SOURCE |
| `working-capital-optimizer` | Analyze cash conversion cycle, free trapped cash | "cash is stuck" | AR, inventory, AP, COGS, revenue, terms | DSO/DIO/DPO, cycle days, levers to shorten | L1 | SOURCE |
| `financial-forecast-builder` | Build a driver-based linked 3-statement forecast (monthly + multi-year) | planning, funding, "model this" | revenue drivers, cost structure, WC days, capex, debt, min-cash | IS/BS/CF forecast + funding-needed + covenant checks | L1 | SOURCE |
| `scenario-and-sensitivity-analysis` | Run base/upside/downside + single-variable sensitivities | "what if?" | base model + variables to flex | scenario matrix + breakpoints + most-fragile assumption | L1 | SOURCE |
| `break-even-and-pricing-analysis` | Contribution margin, break-even, price/cost sensitivity | pricing/viability question | price, variable cost, fixed costs | break-even units/revenue, margin of safety, price levers | L1 | SOURCE |
| `budget-builder` | Build an operating budget tied to goals and forecast | "build next year's budget" | goals, forecast, historicals | budget by line with owners + variance-tracking setup | L1 | SYNTH |
| `debt-service-and-covenant-analysis` | Test debt capacity and covenant headroom | financing decision | EBIT/EBITDA, interest, principal, covenants | TIE, DSCR, max supportable debt, breach alerts | L1 | SOURCE |
| `business-valuation` | Estimate business value via multiples (revenue/EBITDA/SDE) and other methods | "what's it worth?", exit/financing | financials, business type, market multiple data | valuation range by method + drivers of the number | L1 | SOURCE |
| `value-driver-analysis` | Identify levers that raise/lower business value | "how do I increase value?" | financials, ops, customer/risk profile | ranked value levers + actions | L1 | SOURCE |
| `financing-options-analysis` | Match a capital need to appropriate financing | "how should we fund X?" | need, amount, financials, risk posture | option comparison (cost/requirements/fit) + recommendation | L1 | SOURCE |
| `bankability-assessment` | Assess creditworthiness against lender criteria (the 5 C's) | before seeking a loan | financials, credit, collateral, plan | bankability score, gaps, actions to become fundable | L1 | SOURCE |

## growth/

| Skill | Purpose | Trigger | Key inputs | Key output | Autonomy | Prov |
|---|---|---|---|---|---|---|
| `growth-plan-builder` | Assemble the end-to-end growth plan from foundation + finance + GTM + ops outputs | "build our growth plan" | opportunity, feasibility, resources, financials, GTM, ops | populated growth-plan document + exec summary | L1 | SOURCE |
| `kpi-design` | Choose the right leading/lagging KPIs with formulas & thresholds | "what should we measure?" | business type, goals, processes | KPI set with definitions/formulas/thresholds/cadence | L1 | SOURCE |
| `executive-dashboard-builder` | Assemble a three-lens (founder/business/environment) dashboard | "give me a dashboard" | chosen metrics, data sources | dashboard spec with source/decision per metric | L1 | SOURCE |
| `monthly-business-review` | Run the forecast-vs-actual learning loop and adapt the plan | monthly / period close | period actuals + forecast + related metrics | classified variances, top movers, adaptation decisions, next steps | L1 | SOURCE |
| `variance-diagnosis` | Attribute a metric miss to line-item drivers, interpret vs. co-moving metrics | any target miss | actual, forecast, related metrics | root cause + recommended lever | L1 | SOURCE |
| `growth-pitch-generator` | Compress a growth plan into a 3-point pitch | fundraising/partner ask | full growth plan | what-it-is + 3 points + CSFs + 3 next steps | L1 | SOURCE |

## marketing/

| Skill | Purpose | Trigger | Key inputs | Key output | Autonomy | Prov |
|---|---|---|---|---|---|---|
| `market-segmentation` | Divide the market and pick target segments | "who should we target?" | offering, customer data, revenue mix | ranked segments scored on attractiveness/reachability | L1 | SOURCE |
| `customer-persona-builder` | Build persona cards per segment | "who is our customer?" | segment, deep-dive answers, user vs. decision-maker | persona cards + completeness check | L1 | SOURCE |
| `buying-center-mapper` | Identify who influences/decides a purchase | complex/B2B sale | deal context, org type | roles filled (initiator/user/decider/influencer/buyer/gatekeeper) | L0 | SOURCE |
| `buyers-journey-mapper` | Map the multi-stage purchase process + marketing job per stage | GTM design | persona, B2C/B2B/B2G | per-stage behavior + message + tool + action | L1 | SOURCE |
| `customer-value-proposition-builder` | Produce a scored CVP statement | positioning work | target+need, brand, benefits, point-of-difference | CVP statement + score + sharpening tweaks | L1 | SOURCE |
| `marketing-funnel-planner` | Define message/tool/action + persuasion lever per funnel stage | campaign design | persona, CVP, competitive advantage | funnel plan with influence levers | L1 | SOURCE |
| `channel-selection` | Recommend paid/owned/earned channels per goal & persona | "where do we market?" | goals, persona motivations | ranked channel plan | L1 | SOURCE |
| `website-conversion-audit` | Score a site on conversion fundamentals + fixes | "why don't visitors convert?" | page content, conversion goals | red/yellow/green scorecard + fix list | L1 | SOURCE |
| `keyword-and-search-map` | Build an intent-tagged keyword map + coverage gaps | SEO/content planning | business terms, persona, pages | keyword table + gaps | L1 | SOURCE |
| `social-content-planner` | Generate a content calendar honoring value/promo balance + analyze performance | "plan our posts" | content buckets, goals, past post metrics | calendar + reuse/drop guidance | L2 | SOURCE |
| `marketing-metrics-tracker` | Compute & monitor marketing KPIs (funnel, CAC, ROAS) | continuous | impressions, clicks, spend, conversions | KPI dashboard + alerts | L2 | SYNTH |
| `competitive-advantage-assessment` | Rate capabilities vs. competitors on what customers value | positioning/strategy | competitors, customer-valued variables | differentiation matrix + improvement actions | L1 | SOURCE |
| `marketing-strategy-builder` | Turn positioning + funnel into a dated action plan | "build our marketing plan" | all marketing outputs | action steps with owners/deadlines | L1 | SOURCE |

## sales/

| Skill | Purpose | Trigger | Key inputs | Key output | Autonomy | Prov |
|---|---|---|---|---|---|---|
| `sales-process-design` | Design a repeatable pipeline with stages, criteria, and conversion targets | "our selling is ad hoc" | offering, buyer's journey, current pipeline | staged sales process + exit criteria + KPIs | L1 | CLAUDE |
| `pipeline-and-forecast-review` | Diagnose pipeline coverage & conversion; forecast bookings | "will we hit the number?" | pipeline, stages, win rates, targets | coverage/conversion diagnosis + weighted forecast + gaps | L1 | SYNTH |
| `negotiation-preparation` | Build a full negotiation prep plan (interests, BATNA/ZOPA, concessions, tactics) | before a negotiation | parties, issues, interests/target/limit, known facts | prep plan, ZOPA/BATNA, option packages, concession sequence, script | L1 | SOURCE |
| `proposal-builder` | Draft a customer proposal aligned to CVP and pricing | "prepare a proposal" | opportunity, CVP, pricing, terms | proposal draft (for approval before send) | L1 | SYNTH |

## operations/

| Skill | Purpose | Trigger | Key inputs | Key output | Autonomy | Prov |
|---|---|---|---|---|---|---|
| `operational-audit` | Run a multi-dimension audit; surface top operational constraints | "why can't we scale?" | business description, offerings, sales trend, tools, org | prioritized constraints/gaps/automation candidates | L1 | SOURCE |
| `process-mapping` | Decompose a process into a linked map with details + diagnostics | "document how X works" | process name, required output, walkthrough | structured process map + improvement opportunities + metrics | L1 | SOURCE |
| `bottleneck-analysis` | Find the constraint capping throughput + its strain point | "delivery is too slow" | process map or step timings, demand trend | named bottleneck, capacity ceiling, relief action | L1 | SOURCE |
| `sop-writer` | Codify tribal knowledge into a documented, monitorable SOP | "write this down" | process walkthrough, standards | SOP with steps, standards, quality checkpoints | L2 | SOURCE |
| `process-optimization` | Tag value vs. waste per step; project process evolution for growth | "streamline this" / "too many steps" | process map, growth plan | value-added analysis + elimination/redesign + roadmap | L1 | SOURCE |
| `automation-triage` | Route each step to automate/document/delegate/outsource/keep-manual | "automate this" | process map, volume/judgment profile, budget | per-step disposition + tool fit | L1 | SOURCE |
| `technology-evaluation` | Turn burning needs into ranked technology adoptions | "what tools do we need?" | problem list, budget, existing systems | need→solution→value table + due-diligence checklist | L1 | SOURCE |

## people/

| Skill | Purpose | Trigger | Key inputs | Key output | Autonomy | Prov |
|---|---|---|---|---|---|---|
| `hiring-plan-builder` | Determine what roles are needed, affordable, and when | "should we hire?" / "what roles next year?" | workload, capacity, goals, financials | prioritized hiring plan with roles, timing, budgeted cost | L1 | SYNTH |
| `job-description-builder` | Turn a hiring need into a structured JD | after hiring decision | role, reports-to, context | JD with critical tasks + competencies + values | L2 | SOURCE |
| `interview-guide-and-scorecard` | Produce a behavioral interview guide + legality-filtered scorecard | before interviewing | JD, competencies | question-per-competency guide + A–D scorecard | L2 | SOURCE |
| `hiring-scorecard-and-fit` | Evaluate candidates on competencies + values, blocking affinity bias | during selection | candidate signals, mission/values | scored fit assessment | L1 | SOURCE |
| `delegation-planner` | Set authority level + instruction type + delegation brief for a task/person | "who should I delegate to?", founder overloaded | task risk/novelty, employee competence/trust | authority level (A–D) + instruction type + delegation brief | L1 | SOURCE |
| `founder-capacity-diagnostic` | Detect founder-as-bottleneck and what to offload | "I'm doing too much" | founder task list, decision flow, goals | tasks to delegate/hire/automate + target levels | L1 | SOURCE |
| `organizational-design` | Audit org-as-system and build a capacity roadmap | scaling/reorg | results, key people, HR processes, culture, vision | org audit + I-need/I-have/gaps/plan roadmap | L1 | SOURCE |
| `onboarding-builder` | Produce the onboarding sequence for a start date | new hire starting | role, manager, start date, team | provisioning list, day-1 plan, first-week agenda, checklist | L2 | SOURCE |
| `culture-diagnostic` | Assess stated vs. lived values and engagement signals | "is our culture healthy?" | values, observed signals, indicators | culture findings + alignment actions | L1 | SYNTH |
| `hr-process-coverage-audit` | Check which formal HR procedures exist vs. needed | growth/compliance | current process inventory | gap list + escalation flags | L1 | SOURCE |

## leadership/

| Skill | Purpose | Trigger | Key inputs | Key output | Autonomy | Prov |
|---|---|---|---|---|---|---|
| `leadership-style-assessment` | Classify style, detect stress/backup style, advise how to flex | onboarding, team friction | assertiveness + responsiveness ratings, target person/context | style profile + flex guidance + stress guidance | L0 | SOURCE |
| `delegation-readiness-audit` | Assess whether the founder's beliefs support delegation | founder overload | belief ratings | control↔trust score + coaching actions | L0 | SOURCE |
| `motivation-mapper` | Surface founder motives + key-people non-monetary motivators | retention, alignment | ranked motives, per-employee signals | motive profiles + tailored management approach | L1 | SOURCE |
| `mission-vision-builder` | Draft/refine mission + 5-year vision against a quality checklist | foundation/reset | what/for-whom, distinctive value, future picture | mission + vision statements | L1 | SOURCE |
| `leadership-growth-planner` | Build a personal leadership development plan | development | strengths/weaknesses, steps | action plan + 3 trackable growth metrics | L0 | SOURCE |

## legal/

> All legal skills are **guidance, not legal advice**, and carry hard escalation triggers to a licensed attorney.

| Skill | Purpose | Trigger | Key inputs | Key output | Autonomy | Prov |
|---|---|---|---|---|---|---|
| `entity-structure-advisor` | Compare entity structures for a situation (informational) | formation/restructure | ownership, liability, tax, growth intent | option comparison + "confirm with attorney/CPA" flag | L0 | CLAUDE |
| `contract-review-triage` | Pre-signature checklist + high-risk clause flags | any contract | contract/terms | checklist results + flagged clauses + attorney-review verdict | L1 | SOURCE |
| `employment-compliance-scan` | Which employment laws now apply + gaps + worker classification | hiring, growth, remote | headcount, states, policies, work arrangement | applicable-law map, gaps, misclassification flags, escalation | L1 | SOURCE |
| `ip-protection-audit` | Find gaps in NDA/IP-assignment/access controls | IP-sensitive work | who has access, existing agreements | gap list + remediation steps | L1 | SOURCE |
| `legal-escalation-router` | Decide if a question/action requires counsel and frame it | any legal question | the question/action | escalation verdict + framed question for counsel | L0 | SOURCE |

---

## Summary

- **10 skill domains** + 1 cross-cutting flagship.
- **78 skills** consolidated from ~113 raw candidates (overlaps merged, e.g. duplicate cash/working-capital/opportunity/forecast/dashboard skills across finance, strategy, and growth clusters).
- Provenance: majority **SOURCE**, with **SYNTH** where source concepts were recombined and **CLAUDE** where a running business needs a capability the source only implied (sales process, entity structure, budgeting, continuity).
- Each skill's full specification lives in `skills/<domain>/<skill-name>/SKILL.md`, built to `skills/_TEMPLATE/SKILL.md`.
- Agents (see `AGENT_REGISTRY.md`) compose these skills; workflows (see `WORKFLOW_REGISTRY.md`) orchestrate them end-to-end.
