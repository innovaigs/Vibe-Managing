---
name: technology-evaluation
domain: operations
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [operations, offerings, finance, integrations, team, strategy, metrics]
writes: [operations, decisions, metrics]
related_skills: [automation-triage, process-optimization, bottleneck-analysis, operational-audit, sop-writer]
owned_by_agents: [operations-agent]
---

# Skill: Technology Evaluation

## Purpose
Turn the business's burning operational needs into a ranked list of technology adoptions — each tied to the problem it solves and the value it creates — and run a due-diligence checklist so the founder adopts the right technology at the right price point, and doesn't buy a tool that's wrong-fit, redundant, or won't integrate.

## When to Use
- "What tools/software do we need?", "should we buy X?", "is this tool worth it?", "how do we compare these options?"
- After `automation-triage` routes an "automate" or "outsource" disposition here for the specific tool/provider decision.
- When a burning operational need surfaces (a bottleneck, a manual data-entry pain, a measurement gap) and technology is a candidate solution.
- Before any tooling purchase or renewal — to justify it against the need and vet fit/price/integration.

## When NOT to Use
- You haven't decided *whether* to automate/outsource the step yet → `automation-triage` first (this skill assumes tech is the chosen path).
- The step is waste to remove, not to buy a tool for → `process-optimization`.
- The need is a whole-business scan → `operational-audit`.
- You need to actually purchase/sign → that's a founder-approval action, not this skill (this skill prepares the recommendation and due diligence; it never buys).

## Required Context
- `operations.tools` and `integrations` — what's already owned and connected (avoid redundant buys; prefer integration/consolidation).
- `operations.processes` — the process/step the technology serves and its metrics.
- `offerings` — whether the tool touches the core competency (higher scrutiny).
- `finance` — budget, cash position, and the cost the tool would offset (for ROI).
- `strategy.growth_plan` — so the tool fits where the business is going, not just today.
- `team.org` — who will adopt/administer it (ease-of-adoption factor).

## Inputs
```yaml
input:
  burning_needs:                        # the problems, in priority order
    - need: string                      # the problem/pain (NOT a product)
      process_affected: string
      current_cost_or_pain: string      # time lost, errors, missed revenue, etc.
      annual_manual_cost: number|null
  budget: number|null                   # available for tooling
  existing_systems: list[string]        # current tools/integrations (function-level)
  candidate_categories: list[string]    # optional: tool categories to consider (by function)
  constraints: list[string]             # data-sensitivity, compliance, must-integrate-with, team size
  growth_horizon: string                # so fit is judged against future volume
```

## Missing Information Protocol
1. Start from the burning need, never the tool. If the input names a product but not the problem, ask "what problem is this solving and what does it cost you today?" — the whole method anchors on the need.
2. Pull existing systems from `operations.tools`/`integrations` to avoid recommending something already owned or a redundant category.
3. If the cost-of-pain (annual manual cost, error cost, revenue impact) is unknown, estimate it and mark ROI directional; a tool can't be justified without sizing the need.
4. Never recommend a specific named vendor as "the answer" without the due-diligence checklist completed; evaluate by function and fit, and present options with trade-offs.
5. Never assume integration works — flag integration as a verification item, not a given.
6. Analysis and shortlisting are always allowed; the purchase itself is a founder-approval action and is never executed here.

## Diagnostic Questions
- What is the burning need/problem, and what does it cost today (time, errors, missed revenue, capacity ceiling)?
- What technology *category* (by function) could solve it, and what value would it create?
- Do we already own something that does this (or nearly)? Can we consolidate instead of buy?
- Is this the *right* technology for *this specific* business, at the *right price point*? (fit and price both)
- Will it integrate with existing systems, or create a new data silo?
- How hard is it for the team to adopt (learning curve, admin overhead)?
- Is it reliable, secure, and appropriate for our data sensitivity/compliance needs?
- Does it remove a real bottleneck / solve a real need, or just add a tool?
- What is the ROI and payback, and does it fit the budget and cash position?
- Does it fit where the business is going (growth horizon), not only today?

## Analysis Framework
The problem-first evaluation method: **Burning Need → Technology Solution → Value Created**, then due diligence, then rank.
1. **Anchor on the need.** For each burning need, state the problem and quantify the current cost/pain.
2. **Map to a solution category** (by function, not brand): what class of technology addresses it, and articulate the value created.
3. **Check for consolidation.** Can an existing system or integration solve it? Redundancy is a cost, not a feature.
4. **Score fit & price.** Right-fit for *this* business's size/stage/workflow, at a price point the business can sustain. A powerful tool at the wrong price/complexity is a wrong fit.
5. **Run the due-diligence checklist** (below) on each viable option.
6. **Compute ROI/payback** against the quantified need.
7. **Rank** adoptions by value/fit/price and select the top 1–2; defer the rest.
8. **Produce the adoption recommendation** with the due-diligence findings, an implementation/adoption note, and success metrics — held for founder approval to purchase.

**Due-diligence checklist (per option):**
- Fit to the specific problem and to this business's size/stage/workflow.
- Total cost of ownership vs. value created (subscription + setup + training + admin).
- Integration with existing systems (or does it create a silo?).
- Ease of staff adoption / learning curve / admin overhead.
- Reliability, security, and data-sensitivity/compliance appropriateness.
- Vendor viability (support, longevity), contract/lock-in terms, exit/data-portability.
- Whether it removes a real bottleneck/need or just adds a tool.
- Scalability to the growth horizon.

## Calculations
- **Automation/tech ROI** = (annual cost/value gained − annual tool cost) ÷ annual tool cost. Adopt-worthy when positive with reasonable payback.
- **Total cost of ownership (TCO)** = subscription/license + setup/implementation + training + ongoing admin (annualized).
- **Payback period** = (setup + first-year cost) ÷ annual value gained (savings + revenue enabled + risk avoided).
- **Annual value gained** = manual cost saved + throughput/revenue enabled (e.g. relieving a bottleneck) + error/rework cost avoided.
- **Fit score** (qualitative, 1–5 across: problem fit, price fit, integration, adoption ease, reliability/security, scalability) — used to rank options after ROI screen.
- **Consolidation saving** = cost of tools replaced/avoided by choosing an integrated option.
- Decision read: prefer the highest fit score among options with positive ROI within budget; a high ROI with a low fit/integration score is a red flag (hidden adoption cost).

## Decision Rules
- IF no burning need is defined for a proposed tool THEN do not evaluate/adopt — anchor on a real problem first.
- IF an existing system (or a modest integration) can solve the need THEN recommend consolidation over a new purchase.
- IF a technology promises efficiency BUT is wrong-fit or wrong-price for this specific business THEN do not adopt; require due diligence and a better-fit option.
- IF ROI is negative or payback is unreasonably long THEN do not adopt now; keep manual or re-visit at higher volume.
- IF the tool won't integrate and would create a data silo THEN downgrade it; prefer an option that integrates.
- IF the tool touches sensitive/regulated data THEN require security/compliance verification before recommending; adoption is founder-approval + compliance.
- IF the need is really a bottleneck THEN confirm with `bottleneck-analysis` that the tool relieves the actual constraint (not a non-constraint step).
- IF two options are close on ROI THEN choose the higher fit score (integration + adoption ease usually decide).
- IF adoption success depends on staff behavior change THEN pair the recommendation with an SOP/training plan (`sop-writer`) — a tool without adoption creates no value.
- IF the purchase is material relative to cash position THEN route ROI/cash-impact to finance before founder decision.

## Procedure
1. Collect the burning needs and quantify each one's current cost/pain.
2. Pull existing systems; screen for consolidation opportunities.
3. Map each remaining need to a solution category and articulate the value created.
4. Identify viable options (by function); run the due-diligence checklist on each.
5. Compute TCO, ROI, and payback; score fit.
6. Rank adoptions; select top 1–2; defer the rest with rationale.
7. Draft the adoption recommendation(s) with due-diligence findings, an adoption/implementation note, success metrics, and the approval request. Pair with `sop-writer`/training where adoption depends on it.
8. Write the evaluation to `decisions`/`operations` as a proposal; create a draft approval request. Never purchase.

## Output
```yaml
output:
  evaluations:
    - need: string
      process_affected: string
      value_created: string
      solution_category: string          # by function, not a brand
      consolidation_option: string|null   # existing system that could solve it instead
      options:
        - option_label: string           # function/fit description, not an endorsement
          tco_annual: number|null
          roi: number|null
          payback_months: number|null
          fit_score: number|null         # 1-5 composite
          due_diligence:
            problem_fit: string
            integration: string
            adoption_ease: string
            reliability_security: string
            scalability: string
            lock_in_exit: string
          red_flags: list[string]
      recommendation: enum(adopt, consolidate, defer, do_not_adopt)
      recommended_option: string|null
      requires_approval: boolean          # true for any purchase/commitment
      pair_with: list[string]             # e.g. sop-writer for adoption/training
  ranked_adoptions: list[string]          # top picks across all needs, in priority order
  deferred: list[object]                  # {need, why_deferred}
  due_diligence_checklist_status: string  # complete/partial
  approval_request:                       # per AUTONOMY_AND_APPROVAL_MODEL §8, for any buy
    what: string
    why: string
    cost_or_exposure: string
    expected_outcome: string
    alternatives: list[string]
    recommendation: string
    rollback: string
    reversibility: enum(reversible, recoverable, irreversible)
  open_questions: list[string]
```

## Recommendations
Rank adoptions by **value created × fit, gated by positive ROI and budget, discounted by adoption risk.** Prefer consolidation over new spend; prefer integrating tools over silos; cap the immediate ask at the top 1–2 adoptions so the team can actually absorb them. Every recommendation ties back to its burning need and states the value created, includes the completed due-diligence findings, and is packaged as a founder approval request (nothing is bought by the skill). Where success depends on behavior change, bundle the SOP/training plan into the recommendation.

## Execution Opportunities
- Write the evaluation and ranked adoptions to `decisions`/`operations` as proposals (L1).
- Draft the founder approval request(s) for any purchase (L1 draft).
- Draft an adoption/implementation task list and pair with `sop-writer` for training (L1).
- Draft a post-adoption success-metric set for the dashboard (L1 draft).
- No purchasing, no vendor commitment, no contract acceptance, no trial sign-up that commits money or data — all held for the founder.

## Human Approval Requirements
- Purchasing any tool, starting a paid trial/subscription, or committing to any vendor → founder approval (purchasing tools & vendor commitments per AUTONOMY_AND_APPROVAL_MODEL §4).
- Accepting terms/contracts or granting a tool access/permissions (OAuth/integration scopes) → founder approval.
- Adopting anything that processes sensitive/regulated data → founder approval + compliance/security review.
- Entering payment or account credentials is prohibited for the agent — the founder performs the purchase themselves.

## Escalation Conditions
- Material spend relative to cash position → founder + accountant/finance for cash-impact review.
- Contract terms, lock-in, liability, or data-ownership questions → attorney.
- Data-sensitivity/compliance/security concerns with a tool → legal/compliance/security.
- ROI depends on unverified estimates and the spend is large → surface uncertainty; recommend a bounded pilot before full commitment.
- The tool touches the core competency in a way that could create dependency/lock-in → founder (strategic decision).

## KPIs
- Adoption success: tool actually used by the team (active usage), not shelfware.
- Realized ROI vs. projected; payback met.
- Need resolved: the burning need's cost/pain measurably reduced (time saved, errors down, bottleneck relieved).
- Integration health: data flows without new silos/manual re-entry.
- Consolidation: net tool count / spend not ballooning; redundancy avoided.

## Monitoring
After adoption (post-approval), watch: active usage/adoption rate, realized savings vs. projection, the target process metric the tool was meant to move (cycle time, defect rate, throughput), and integration reliability. Flag shelfware early (paid-for, unused) and renewals for re-justification against the original need.

## Follow-Up
- Re-evaluate at renewal (does it still beat alternatives / still solve the need?).
- Re-run when a new burning need appears, at a growth step-change (a deferred tool may now clear ROI), or when `automation-triage` routes a new automate/outsource disposition here.
- Feed adoption outcomes back to `decisions` (expected vs. actual) for the learning layer.

## Related Skills
- `automation-triage` — decides whether tech is the right path before this skill picks the tool.
- `bottleneck-analysis` — confirms a tool relieves the real constraint.
- `process-optimization` — ensure you're not buying a tool for waste that should be removed.
- `sop-writer` — writes the adoption/training procedure so the tool actually gets used.
- `operational-audit` — surfaces the burning needs this skill evaluates.

## Guardrails
- Execution ceiling L1; the skill never purchases, subscribes, signs, grants access, or enters credentials — those are founder actions.
- Start from the burning need, not the tool; reject tool-first proposals with no defined problem.
- Right technology at the right price for THIS business only — complete due diligence before any recommendation to buy.
- Prefer consolidation/integration over new spend; flag silo-creating tools.
- Never present a single named vendor as "the answer" without options and trade-offs; evaluate by function and fit.
- Require security/compliance review for tools touching sensitive/regulated data; such data leaves the business only with approval.
- Label estimate-based ROI as directional; recommend a bounded pilot when large spend rests on estimates.

## Example
**Founder input:** burning_needs = [(1) "we re-key every order from email into our shipping tool by hand — ~8 hrs/week, and it causes wrong-address errors", process = fulfillment, annual_manual_cost ≈ $12k; (2) "no visibility into which jobs are late until a client complains", process = delivery, cost = churn risk]. existing_systems = [email, a shipping tool, spreadsheet-based tracking]. budget modest. growth_horizon = "2 years, ~2x volume".

**Skill reasoning:**
- Need 1 → solution category: order-to-shipping integration/automation. Value created: eliminates ~8 hrs/week re-keying + removes address errors. Consolidation check: the existing shipping tool may offer a native order-import integration — check that before buying a new tool (consolidation preferred). Options: (a) native integration/add-on to the current shipping tool — high fit, integrates, low adoption cost; (b) a standalone iPaaS/connector — more flexible, higher TCO, another system to admin. TCO/ROI: option (a) ROI strongly positive (≈$12k saved vs. modest add-on cost, payback < 3 months), fit_score high. red_flags for (b): new silo, admin overhead.
- Need 2 → solution category: job/project status tracking with due-date visibility. Value: catch late jobs before the client does (churn avoidance). Consolidation: could be the same job-tracking system that also feeds fulfillment. Recommendation: adopt a job-tracking tool that integrates with fulfillment; defer if budget forces a choice — Need 1 has the clearer, quantified ROI.
- Ranking: adopt Need-1 integration first (quick, high ROI, consolidates on existing tool); adopt/or pilot job-tracking for Need 2 next. Both paired with `sop-writer` for adoption. Because success = staff actually using them, bundle training.

**Output (excerpt):** ranked_adoptions = ["order-to-shipping integration (via existing shipping tool)", "integrated job-status tracking"]; Need-1 recommendation = `consolidate` (use current tool's integration) with `requires_approval: true`; approval_request drafted (what/why/cost/rollback = cancel subscription, reversibility = recoverable); open_questions = ["confirm the current shipping tool's order-import integration and its price tier"].

**Executed vs. approval:** Wrote the evaluation and drafted the approval request + adoption/training tasks (auto, L1). Nothing was purchased, no trial started, no terms accepted — the buy decision and any credential entry were left to the founder.

## Provenance
SOURCE — derived from the operations knowledge base: the "Exploring Technology" method (Burning Need/Problem → Technology Solution → Value Created), the core principle that only the *right* technology at the *right price point* is effective for a *specific* business, the "do due diligence before any technology decision" rule, and the technology-evaluation checklist (fit, TCO vs. value, integration, adoption ease, reliability, whether it removes a real bottleneck). ROI/TCO/payback formulas are SYNTHESIZED industry standards, flagged as such. De-branded per repository rules (tools referenced by function, not product).
