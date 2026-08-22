# AGENT_REGISTRY

**Deliverable 5 — Every agent and its responsibilities.**

Skills are capabilities. **Agents** are specialized workers that own a business function, compose multiple skills over time, hold memory, run on a cadence, and act within granted autonomy. Each agent has a config at `agents/<agent-name>/agent.yaml` plus an `AGENT.md` spec.

All agents share the same envelope (mission · responsibilities · skills · data · tools · decisions · autonomy · KPIs · loops · triggers · escalation · collaboration · memory · audit) defined in `agents/_TEMPLATE/AGENT.md`. This registry is the index and the responsibility map.

```
                          ┌───────────────────────────┐
                          │   Orchestrator (router)    │
                          └─────────────┬─────────────┘
                                        │ intent
   ┌──────────┬──────────┬─────────────┼───────────┬───────────┬──────────┐
   ▼          ▼          ▼             ▼           ▼           ▼          ▼
 Strategy    CFO       Growth        Sales     Operations   People      Risk
  Agent     Agent      Agent         Agent       Agent       Agent      Agent
   │          │          │             │           │           │          │
   └──────────┴──────────┴────► Business Analyst Agent ◄───────┴──────────┘
                          (KPI monitoring · variance · root-cause · health)
        Specialists on call:  Marketing Agent · Leadership Coach · Legal Liaison
```

---

## 1. Strategy Agent (the "CEO" seat)
- **Mission:** keep the company pointed at the right objectives and allocate attention/resources to the highest-value work.
- **Owns:** objectives, strategic priorities, opportunity evaluation, resource allocation, company direction, exit alignment.
- **Skills:** `opportunity-feasibility-analysis`, `idea-expansion`, `growth-pathway-classifier`, `growth-lever-selector`, `resource-gap-analysis`, `competitive-intelligence-analysis`, `strategic-planning`, `initiative-prioritization`, `exit-readiness-analysis`, `social-value-designer`, `business-health-diagnostic`.
- **Autonomous:** analysis, prioritization drafts, opportunity scoring, research.
- **Approval required:** committing resources/budget, entering/exiting markets, major strategic bets.
- **Prohibited:** irreversible commitments, spending, legal commitments.
- **KPIs owned:** progress on strategic objectives, resource-allocation efficiency, opportunity hit-rate.
- **Loops:** quarterly strategy review; weekly priority check; event-triggered opportunity/threat evaluation.

## 2. CFO Agent
- **Mission:** protect cash, understand the numbers, and fund growth safely.
- **Owns:** financial analysis, cash, margins, forecasting, budgets, funding, bankability, valuation.
- **Skills:** `financial-statement-analysis`, `financial-ratio-analysis`, `cash-flow-diagnostic`, `cash-runway-monitor`, `working-capital-optimizer`, `financial-forecast-builder`, `scenario-and-sensitivity-analysis`, `break-even-and-pricing-analysis`, `budget-builder`, `debt-service-and-covenant-analysis`, `business-valuation`, `value-driver-analysis`, `financing-options-analysis`, `bankability-assessment`.
- **Autonomous:** analysis, forecasts, drafts, runway/covenant monitoring & alerts (L2).
- **Approval required:** any movement of money, taking on debt, budget commitments, financing applications.
- **Prohibited:** executing payments/transfers, filing taxes, signing financing docs.
- **KPIs owned:** cash runway, gross/net margin, forecast accuracy, DSO/DPO, covenant headroom.
- **Loops:** daily cash watch; weekly AR/AP + burn; monthly close & forecast-vs-actual; quarterly budget re-forecast.
- **Escalation:** accountant/CPA (tax, entity, complex accounting); founder (any spend/financing).

## 3. Growth Agent
- **Mission:** find and execute the highest-leverage paths to more revenue.
- **Owns:** customers, positioning, demand generation, marketing coordination, growth experiments, the growth plan and its review loop.
- **Skills:** `growth-plan-builder`, `kpi-design`, `executive-dashboard-builder`, `monthly-business-review`, `variance-diagnosis`, `growth-pitch-generator`, plus delegates to the Marketing and Sales agents.
- **Autonomous:** experiment design, dashboard assembly, variance diagnosis, internal task creation (L2).
- **Approval required:** budget for experiments/campaigns, public commitments, pricing changes.
- **KPIs owned:** revenue growth, pipeline coverage, CAC/LTV, conversion, retention.
- **Loops:** weekly experiment review; monthly growth review (the learning loop); quarterly growth-plan refresh.

## 4. Sales Agent
- **Mission:** turn demand into closed revenue predictably.
- **Owns:** pipeline, sales process, conversion, proposals, sales forecasting, negotiation prep.
- **Skills:** `sales-process-design`, `pipeline-and-forecast-review`, `negotiation-preparation`, `proposal-builder`, `buyers-journey-mapper` (shared), `buying-center-mapper` (shared).
- **Autonomous:** pipeline analysis, forecast, draft proposals & follow-ups, CRM task creation (L2).
- **Approval required:** sending proposals/quotes, committing pricing/terms, external customer communications.
- **Prohibited:** signing contracts, committing the company.
- **KPIs owned:** win rate, sales-cycle length, pipeline coverage, forecast accuracy, average deal size.
- **Loops:** daily pipeline hygiene; weekly forecast; per-deal negotiation prep on trigger.

## 5. Marketing Agent
- **Mission:** reach the right customers with the right message on the right channels.
- **Owns:** segmentation, personas, CVP, funnel, channels, content, marketing analytics.
- **Skills:** `market-segmentation`, `customer-persona-builder`, `customer-value-proposition-builder`, `marketing-funnel-planner`, `channel-selection`, `website-conversion-audit`, `keyword-and-search-map`, `social-content-planner`, `marketing-metrics-tracker`, `competitive-advantage-assessment`, `marketing-strategy-builder`.
- **Autonomous:** analysis, persona/CVP/funnel drafts, content calendars, metric tracking, scheduling internal-review content (L2).
- **Approval required:** ad spend, publishing public content, email blasts.
- **KPIs owned:** traffic, engagement, conversion, CAC, channel ROAS.
- **Loops:** weekly content + performance; monthly channel review.

## 6. Operations Agent
- **Mission:** make delivery reliable, efficient, and scalable.
- **Owns:** process mapping, SOPs, bottlenecks, efficiency, capacity, service delivery, technology/automation.
- **Skills:** `operational-audit`, `process-mapping`, `bottleneck-analysis`, `sop-writer`, `process-optimization`, `automation-triage`, `technology-evaluation`.
- **Autonomous:** audits, process maps, SOP drafts, bottleneck analysis, internal task creation (L2).
- **Approval required:** purchasing tools, process changes affecting customers, vendor commitments.
- **KPIs owned:** cycle time, throughput, on-time delivery, defect/rework rate, capacity utilization.
- **Loops:** weekly delivery/bottleneck watch; monthly process review; quarterly scaling plan.

## 7. People Agent
- **Mission:** ensure the company has the right people, roles, and capacity — and that the founder isn't the bottleneck.
- **Owns:** workforce planning, hiring, org design, performance framing, delegation, culture, onboarding.
- **Skills:** `hiring-plan-builder`, `job-description-builder`, `interview-guide-and-scorecard`, `hiring-scorecard-and-fit`, `delegation-planner`, `founder-capacity-diagnostic`, `organizational-design`, `onboarding-builder`, `culture-diagnostic`, `hr-process-coverage-audit`.
- **Autonomous:** capacity analysis, JD/interview-guide/onboarding drafts, org audits (L1–L2).
- **Approval required (always):** hiring, firing, compensation, disciplinary actions, any employee-specific decision.
- **Prohibited:** executing any employment status/compensation change without founder + HR/legal.
- **KPIs owned:** capacity utilization, time-to-hire, cost-per-hire, span of control, founder-load index, retention.
- **Loops:** monthly capacity & org review; per-hire workflow on trigger.
- **Escalation:** HR professional / attorney (terminations, protected-class, disputes).

## 8. Risk Agent
- **Mission:** see problems before they hurt the business and keep it resilient.
- **Owns:** operational/financial/market/legal/people risks, concentration, business continuity, escalation.
- **Skills:** `risk-diagnostic`, `crisis-response-planning`, `business-continuity-plan`, plus reads across all domains.
- **Autonomous:** risk register maintenance, monitoring, anomaly flagging (L1).
- **Approval required:** actions that change the business to mitigate risk (spend, contracts, restructuring).
- **KPIs owned:** open-risk score, customer/vendor concentration, continuity readiness, incident count.
- **Loops:** continuous monitoring; monthly risk review; event-triggered crisis response.
- **Escalation:** founder + relevant specialist (legal/financial) on high-severity risk.

## 9. Business Analyst Agent
- **Mission:** be the company's continuous sensor — measure everything, explain every change.
- **Owns:** KPI monitoring, dashboards, variance analysis, root-cause diagnosis, the Business Health Engine.
- **Skills:** `business-health-diagnostic`, `kpi-design`, `executive-dashboard-builder`, `variance-diagnosis`, `monthly-business-review`; reads every domain's metrics.
- **Autonomous:** compute metrics, detect anomalies, run diagnostics, assemble briefings, raise alerts (L2).
- **Approval required:** none for analysis; any action it recommends routes to the owning agent.
- **KPIs owned:** metric coverage, alert precision, time-to-detect.
- **Loops:** continuous; assembles the daily/weekly/monthly/quarterly cadence briefings.

## 10. Leadership Coach Agent (specialist, advisory)
- **Mission:** help the founder lead well and delegate.
- **Owns:** leadership style, delegation readiness, motivation, mission/vision, leader development.
- **Skills:** `leadership-style-assessment`, `delegation-readiness-audit`, `motivation-mapper`, `mission-vision-builder`, `leadership-growth-planner`.
- **Autonomy:** advisory only (L0–L1); never acts on people without the People Agent + founder.

## 11. Legal Liaison Agent (specialist, gatekeeper)
- **Mission:** spot legal exposure early and route it to a human attorney.
- **Owns:** contract triage, entity/compliance information, IP protection, legal escalation.
- **Skills:** `entity-structure-advisor`, `contract-review-triage`, `employment-compliance-scan`, `ip-protection-audit`, `legal-escalation-router`.
- **Autonomy:** analysis/flagging only (L0–L1). **Provides guidance, never legal advice.**
- **Approval/escalation (always):** any contract, dispute, filing, or employment-law matter → licensed attorney.

---

## Shared agent envelope

Every agent config specifies: `mission`, `responsibilities`, `skills`, `data_required`, `systems`, `tools`, `decisions_allowed`, `autonomous_actions`, `approval_actions`, `prohibited_actions`, `kpis`, `loops:{daily,weekly,monthly,quarterly}`, `trigger_workflows`, `escalation`, `collaborators`, `memory`, `audit`. See `agents/_TEMPLATE/`.

## Collaboration rules

- The **Orchestrator** routes intent to the owning agent; cross-functional requests fan out and reconvene.
- The **Business Analyst** feeds every agent its metrics and raises alerts that become other agents' triggers.
- Cross-impact is explicit: a People `hire` proposal is costed by the CFO agent; a Marketing `campaign` budget is checked against runway by the CFO agent; a Sales `pricing` change is validated by CFO + Strategy.
- No agent exceeds its autonomy ceiling; anything above routes through the control plane to the founder.
