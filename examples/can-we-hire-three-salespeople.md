# Worked Example — "Can we hire three salespeople?"

A decision-quality trace. Workflow: `should-we-hire`. Numbers illustrative.

**Founder:** "Can we hire three salespeople?"

## Understand
Loaded: cash $180k; monthly net burn $22k → runway 8.2 mo; MRR $95k growing 4%/mo; gross margin 68%; current pipeline $420k weighted; avg salesperson fully-loaded cost $8k/mo; ramp-to-productivity ~4 mo; current 2 reps at 95% capacity.

## Diagnose
- `founder-capacity-diagnostic`: sales is capacity-constrained (reps maxed, inbound leads unworked) — real need, not a process gap.
- Pipeline check: enough unworked demand to justify **added** capacity? Yes for ~2 reps; the 3rd outruns current lead flow.

## Plan (`hiring-plan-builder` + `financial-forecast-builder`)
Hiring economics per rep: cost $8k/mo; productive at month 4; target quota contribution $20k/mo new revenue × 68% margin.
- **3 reps at once:** added cost $24k/mo immediately; runway drops 8.2 → **4.9 mo** before ramp → below the 6-mo guardrail. ❌
- **2 reps now + 1 when lead flow supports:** runway 8.2 → **6.1 mo**, recovers as ramp lands; lead flow supports 2. ✅
- Decision rule fired: `IF runway after hires < 6 mo THEN stage the hires`.

## Recommendation
> Hire **2 now, not 3.** Three at once drops runway to ~4.9 months before they ramp — below safe. Two keeps you at ~6.1 and matches the leads you actually have. Add the third when weighted pipeline sustains >$600k or MRR clears $110k. I've modeled all three cases.

## Actions (risk-tiered)
- **Auto (L1–L2):** drafted the job description, interview guide + scorecard, 90-day onboarding/ramp plan, and the 3-scenario financial model.
- **Approval (always):** the hire decision, offers, and compensation — **held for founder + HR/legal**. Nothing executed.

## Monitor
Post-hire: ramp vs. plan, capacity relief, runway vs. forecast, pipeline coverage for the deferred 3rd hire.

## Remember
Decision record: chose 2-now/1-deferred; expected runway floor 6.1 mo; trigger for hire #3 logged; 60-day review scheduled to compare ramp actual vs. expected.
