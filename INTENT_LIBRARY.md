# INTENT_LIBRARY

**Deliverable 7 — Founder intents mapped to capabilities.**

Vibe Managing meets founders in natural language. This library catalogs the intents the system recognizes and maps each to its execution path:

```
Intent → Diagnostic → Skills → Agent(s) → Tools → Plan → Actions → Approval → Monitoring
```

The Orchestrator (`MASTER_ORCHESTRATOR.md`) classifies any phrasing into one of these intents (type + domain + urgency), then follows the mapping. The phrasings below are representative, not exhaustive — the classifier generalizes.

**Reading the mapping columns:** *Skills* → which capabilities run · *Agent* → who owns it · *Workflow* → the end-to-end orchestration (see `WORKFLOW_REGISTRY.md`) · *Approval* → what needs the founder.

---

## A. Growth & Revenue

**Phrasings:** "Grow revenue." · "We need more customers." · "Sales have slowed down." · "Find out why growth stopped." · "Help me enter a new market." · "How do we grow 20% this quarter?" · "Our best month vs. worst — why?" · "Which product should we push?" · "We're too dependent on one customer."

| Intent | Diagnostic | Skills | Agent | Workflow | Approval |
|---|---|---|---|---|---|
| grow revenue | find binding constraint | growth-pathway-classifier, variance-diagnosis, then funnel/sales/pricing | Growth | `grow-revenue` | spend, pricing, public content |
| sales slowed | conversion vs demand vs churn | variance-diagnosis, sales-process-design, website-conversion-audit | Growth+Sales | `grow-revenue` | outbound, pricing |
| enter new market | feasibility + economics | opportunity-feasibility-analysis, resource-gap-analysis, financial-forecast-builder | Strategy | `evaluate-opportunity` | market-entry commitment |
| reduce customer concentration | concentration risk | risk-diagnostic, market-segmentation, sales-process-design | Risk+Growth | `grow-revenue` | — |
| improve retention | churn drivers | variance-diagnosis, process-optimization | Growth | `improve-retention` | service/product changes |

## B. Financial & Cash

**Phrasings:** "We're running out of cash." · "Why are we profitable but don't have money?" · "Can I afford to hire?" · "Where are we wasting money?" · "Build next year's budget." · "Are our margins healthy?" · "Model what happens if sales drop 20%." · "Can we take on a loan?" · "What are we worth?" · "Prepare us to raise money."

| Intent | Diagnostic | Skills | Agent | Workflow | Approval |
|---|---|---|---|---|---|
| running out of cash | runway + cash bridge | cash-runway-monitor, cash-flow-diagnostic, working-capital-optimizer | CFO | `fix-cash` | money moves, term changes, financing |
| profitable but broke | NI→OCF bridge | cash-flow-diagnostic, working-capital-optimizer | CFO | `fix-cash` | collections comms |
| where's the money going | cost structure | financial-statement-analysis (common-size), variance-diagnosis | CFO | `reduce-spend` | cost cuts, vendor changes |
| build a budget | goals→budget | budget-builder, financial-forecast-builder | CFO | — | budget approval |
| margins healthy? | ratio panel | financial-ratio-analysis | CFO | — | — |
| what-if / stress test | scenarios | scenario-and-sensitivity-analysis | CFO | — | — |
| can we take on debt? | debt capacity | debt-service-and-covenant-analysis, bankability-assessment | CFO | `raise-capital` | taking on debt |
| what are we worth? | valuation | business-valuation, value-driver-analysis | CFO | `prepare-to-exit` | — |
| prepare to raise | fundability | bankability-assessment, financing-options-analysis, financial-forecast-builder | CFO | `raise-capital` | submitting applications |

## C. People & Organization

**Phrasings:** "I need to hire." · "The team isn't performing." · "I am doing too much myself." · "Who should I delegate this to?" · "What roles will we need next year?" · "How do I structure the team?" · "Write a job description for X." · "How do I interview for this role?" · "Onboard our new hire." · "Is our culture healthy?"

| Intent | Diagnostic | Skills | Agent | Workflow | Approval |
|---|---|---|---|---|---|
| should we hire? | capacity + economics | founder-capacity-diagnostic, hiring-plan-builder, financial-forecast-builder | People+CFO | `should-we-hire` | **hire, offers, comp (always)** |
| doing too much | founder-bottleneck | founder-capacity-diagnostic, delegation-planner | People | `delegate-and-offload` | — |
| who to delegate to | authority match | delegation-planner | People | `delegate-and-offload` | — |
| roles needed next year | workforce plan | hiring-plan-builder, organizational-design | People | `should-we-hire` | headcount budget |
| structure the team | org design | organizational-design | People | — | reorg decisions |
| write a JD | role spec | job-description-builder | People | — | — |
| how to interview | interview design | interview-guide-and-scorecard | People | — | — |
| onboard new hire | onboarding | onboarding-builder | People | — | — |
| team not performing | performance framing | organizational-design, delegation-planner | People | — | **any employee action → HR/attorney** |
| culture check | culture signals | culture-diagnostic | People | — | — |

## D. Operations

**Phrasings:** "Customer delivery is too slow." · "We're making too many mistakes." · "Document how this process works." · "Automate this process." · "Why can't we scale?" · "What tools do we need?" · "Map our fulfillment process." · "Where's the bottleneck?"

| Intent | Diagnostic | Skills | Agent | Workflow | Approval |
|---|---|---|---|---|---|
| delivery too slow | bottleneck | bottleneck-analysis, operational-audit | Operations | `scale-operations` | — |
| too many mistakes | quality/process | process-optimization, sop-writer | Operations | `scale-operations` | — |
| document a process | mapping+SOP | process-mapping, sop-writer | Operations | — | — |
| automate a process | automation fit | automation-triage, technology-evaluation | Operations | `scale-operations` | tool purchase |
| can't scale | constraints | operational-audit, bottleneck-analysis, process-optimization | Operations | `scale-operations` | — |
| what tools do we need | tech eval | technology-evaluation | Operations | — | tool purchase |

## E. Strategy & Decisions

**Phrasings:** "Should we launch this?" · "Should we enter this market?" · "Is this opportunity worth pursuing?" · "What should the company focus on next?" · "What is our biggest bottleneck?" · "Should we pursue this partnership?" · "Are we ready to sell the business?" · "What's our competitive edge?"

| Intent | Diagnostic | Skills | Agent | Workflow | Approval |
|---|---|---|---|---|---|
| should we launch/pursue X | feasibility | opportunity-feasibility-analysis, resource-gap-analysis, financial-forecast-builder, risk-diagnostic | Strategy | `evaluate-opportunity` | the commitment |
| what to focus on | priorities | business-health-diagnostic, strategic-planning, initiative-prioritization | Strategy | — | resource shifts |
| biggest bottleneck | whole-business scan | business-health-diagnostic | Analyst+Strategy | — | — |
| competitive edge | differentiation | competitive-intelligence-analysis, competitive-advantage-assessment | Strategy | — | — |
| ready to sell? | exit readiness | exit-readiness-analysis, business-valuation, value-driver-analysis | Strategy+CFO | `prepare-to-exit` | sale decisions |

## F. Marketing & Sales

**Phrasings:** "Who is our customer?" · "Sharpen our value proposition." · "Where should we market?" · "Why don't website visitors convert?" · "Plan our content." · "Build a marketing plan." · "Our selling is ad hoc — fix it." · "Will we hit the number?" · "Prepare me for this negotiation." · "Draft a proposal for this client."

| Intent | Diagnostic | Skills | Agent | Workflow | Approval |
|---|---|---|---|---|---|
| who is our customer | targeting | market-segmentation, customer-persona-builder | Marketing | — | — |
| sharpen value prop | positioning | customer-value-proposition-builder, competitive-advantage-assessment | Marketing | — | — |
| where to market | channel fit | channel-selection, marketing-funnel-planner | Marketing | — | ad spend |
| visitors don't convert | conversion | website-conversion-audit | Marketing | — | site changes |
| plan content | calendar | social-content-planner, keyword-and-search-map | Marketing | — | publishing |
| build marketing plan | GTM plan | marketing-strategy-builder + persona/CVP/funnel/channels | Marketing | — | spend, publishing |
| fix ad-hoc selling | process | sales-process-design, buyers-journey-mapper | Sales | — | — |
| will we hit the number | pipeline | pipeline-and-forecast-review | Sales | — | — |
| prep negotiation | prep plan | negotiation-preparation | Sales | `prepare-negotiation` | — |
| draft a proposal | proposal | proposal-builder | Sales | — | **send (always)** |

## G. Risk, Legal & Continuity

**Phrasings:** "What could go wrong?" · "Are we too exposed to one supplier?" · "Review this contract." · "Do we need an NDA?" · "Are we compliant now that we're hiring?" · "Is this person a contractor or employee?" · "We just lost our biggest client — what now?"

| Intent | Diagnostic | Skills | Agent | Workflow | Approval |
|---|---|---|---|---|---|
| what could go wrong | risk scan | risk-diagnostic | Risk | — | mitigations |
| supplier/customer exposure | concentration | risk-diagnostic, business-continuity-plan | Risk | — | — |
| review a contract | triage | contract-review-triage | Legal Liaison | — | **attorney review (always)** |
| employment compliance | law scan | employment-compliance-scan | Legal Liaison | — | **attorney** |
| contractor vs employee | classification | employment-compliance-scan | Legal Liaison | — | **attorney** |
| protect our IP | IP audit | ip-protection-audit | Legal Liaison | — | attorney for agreements |
| lost biggest client | crisis | crisis-response-planning, cash-runway-monitor | Risk+CFO | `manage-crisis` | recovery actions |

## H. Leadership (advisory)

**Phrasings:** "What's my leadership style?" · "How do I work with this person?" · "Am I ready to delegate?" · "Help me write our mission/vision." · "How do I grow as a leader?" · "What motivates my key people?"

| Intent | Skills | Agent | Approval |
|---|---|---|---|
| leadership style | leadership-style-assessment | Leadership Coach | — |
| work with a person | leadership-style-assessment (flex) | Leadership Coach | — |
| ready to delegate | delegation-readiness-audit | Leadership Coach | — |
| mission/vision | mission-vision-builder | Leadership Coach | — |
| grow as a leader | leadership-growth-planner | Leadership Coach | — |
| motivate key people | motivation-mapper | Leadership Coach | — |

## I. Meta / Cadence

**Phrasings:** "What should I focus on today?" · "What changed this week?" · "How are we doing?" · "Give me the monthly review." · "Are we executing the strategy?" · "What needs my approval?" · "What did you do while I was away?"

| Intent | Skills | Agent | Notes |
|---|---|---|---|
| focus today | business-health-diagnostic → daily brief | Analyst | ranked attention list |
| what changed this week | weekly cadence assembly | Analyst | scorecard + decisions |
| how are we doing | business-health-diagnostic | Analyst | health snapshot |
| monthly review | monthly-business-review, variance-diagnosis | CFO+Growth+Analyst | learning loop |
| executing strategy? | quarterly review | Strategy | initiative progress |
| what needs approval | approval queue | Orchestrator | ranked w/ recommendations |
| what did you do | audit log (reversible actions) | Orchestrator | transparency |

---

## Classification & routing rules

- **Ambiguous intent** → ask ONE clarifying question, then route.
- **Multi-domain intent** (e.g. "can we afford to grow and hire?") → fan out to multiple agents; CFO reconciles against cash before any commitment.
- **Every intent that implies an action** is risk-tiered; irreversible/financial/legal/employment actions are always held for approval.
- **Every intent that implies a metric** attaches monitoring so results are tracked and learned from.
- **Unknown intent** → the Orchestrator runs `business-health-diagnostic` to ground the conversation and proposes the most relevant workflow.

## Coverage

This library spans **9 intent categories** and **~90 distinct founder phrasings** mapped to skills, agents, workflows, approvals, and monitoring. It is designed to be extended: new phrasings attach to existing intents; genuinely new intents add a row and, if needed, a workflow.
