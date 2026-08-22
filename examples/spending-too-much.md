# Worked Example — "I'm spending too much money and I don't know where."

A full trace through the Orchestrator's 16-step loop. Numbers are illustrative.

**Founder:** "I'm spending too much money and I don't know where."

## 1–2. Classify + context
- Intent: `diagnose`, domain `finance` (secondary `operations`), urgency `high`.
- Load: `finance.income_statement` (12 mo), `finance.cash_flow`, `operations.vendors`, `team` cost totals, `metrics` history.

## 3–5. Inspect + gaps
- Present: P&L by month, vendor list, payroll totals. Missing: category tags on 18% of transactions (confidence 0.6).
- Resolve: pull category data from the finance integration; 4% still uncategorized → flagged, not guessed.

## 6–8. Diagnose (skills: `financial-statement-analysis` common-size, `variance-diagnosis`)
- Common-size the cost base; compare each line to trailing 6-mo average and to revenue.
- Hypotheses tested:
  - H1 "Payroll grew faster than revenue" — **supported**: payroll 38%→46% of revenue over 6 mo.
  - H2 "Software/tools sprawl" — **supported**: 22 SaaS tools, +$3,100/mo YoY, 5 overlapping.
  - H3 "COGS creep" — rejected: gross margin stable.

## 9. Plan
| Initiative | Expected saving | Owner | Risk |
|---|---|---|---|
| Consolidate 5 overlapping tools | ~$1,900/mo | Operations agent | reversible |
| Review 3 low-utilization vendor contracts | ~$2,400/mo | CFO agent | approval (vendor comms) |
| Payroll-to-revenue plan (freeze backfill, tie to pipeline) | structural | People + CFO | approval (people) |

## 10–13. Actions (risk-tiered)
- **Auto (L2, reversible):** built a spend dashboard, tagged the remaining transactions for founder confirmation, drafted a tool-consolidation list with cancellation steps.
- **Approval:** cancel/downgrade specific subscriptions; contact vendors to renegotiate; any payroll/headcount change (→ People + founder).

## 14. Monitor
Registered: monthly opex %, software cost/mo, payroll-to-revenue, vendor spend. Alert if opex % rises again.

## 15. Report
> **What I found:** Spend rose mainly from (1) payroll outgrowing revenue (38%→46%) and (2) tool sprawl (22 tools, 5 overlapping). COGS is fine.
> **What I did:** Built your spend dashboard and a consolidation plan that frees ~$1,900/mo (reversible). Tagged the untagged transactions for your quick confirm.
> **What I need from you:** Approve cancelling 5 overlapping tools; approve me contacting 3 vendors to renegotiate (~$2,400/mo more); let's talk about the payroll-to-revenue trend — I've prepared options.
> **What I'll watch:** opex %, software spend, payroll-to-revenue — I'll flag any reversal.

## 16. Remember
Decision record written with expected savings (~$4,300/mo) and a 60-day check to compare actual vs. expected.
