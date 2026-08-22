# Worked Example — "What should I focus on today?"

The founder experience: one question, a ranked answer, prepared actions. Assembled by the Business Analyst agent from the health snapshot + approval queue. Numbers illustrative.

**Founder:** "What should I focus on today?"

## System (Vibe Managing)
> **Three things need your attention:**
>
> 1. 🟠 **Cash runway fell from 7.2 → 5.8 months.** Cause: receivables aged — three invoices totaling $46k are >45 days past due (DSO rose 41→52). *I've drafted polite payment reminders for each — approve to send.*
> 2. 🟠 **Sales conversion dropped 18% this month** (22% → 18%). It isolates to the proposal stage, not lead volume. *I've queued a proposal-stage review and flagged 4 stalled deals for your call.*
> 3. 🟡 **Support response time crossed your SLA** (4h target, now 6.2h). Ticket volume +30% with the same staffing. *I've drafted a triage-rule change and a case for one part-time hire — for your review.*
>
> **Prepared and awaiting approval:** send 3 collection reminders · adjust support triage rules.
> **I handled automatically (reversible):** rebuilt your cash + pipeline dashboards, tagged new transactions, created follow-up tasks for the 4 stalled deals.
> **Approve the reminders and triage change?**

## Under the hood
- `business-health-diagnostic` produced the health snapshot; the worst 🟠/🟠/🟡 items ranked by impact.
- Item 1: `cash-runway-monitor` + `working-capital-optimizer` found DSO as the driver → `cash-flow-diagnostic` confirmed it's collections, not losses.
- Item 2: `variance-diagnosis` isolated the funnel stage; `sales-process-design` review queued.
- Item 3: capacity vs. volume flagged; `hiring-plan-builder` prepared the (approval-gated) staffing case.
- Every prepared action is risk-tiered; sends and hires are held for approval. Reversible dashboard/task work was auto-done and is logged.
