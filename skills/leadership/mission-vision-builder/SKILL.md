---
name: mission-vision-builder
domain: leadership
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [company, leader, market, offerings, customers, goals]
writes: [company, strategy, leader]
related_skills: [motivation-mapper, leadership-style-assessment, strategic-planning, leadership-growth-planner]
owned_by_agents: [leadership-agent, orchestrator]
---

# Skill: Mission & Vision Builder

## Purpose
Draft and refine a crisp mission (what the company does now, for whom, and its distinctive value) and an inspiring 5-year vision (what the company will become, in both business and culture) — validated against a concrete quality checklist. A clear mission and vision are the founder's alignment tool: they tell the team, customers, and future talent where the company is going and why, and they anchor every downstream strategy and growth decision.

## When to Use
- The founder has no written mission/vision, or has ones that are vague, generic, or stale.
- The company is entering planning, fundraising, hiring at scale, or a rebrand and needs a north star everyone can repeat.
- The founder wants to attract talent and needs a vision that speaks to future employees, not just customers.
- After `motivation-mapper` clarifies the founder's real motives, so the vision reflects what actually drives them.
- Before `strategic-planning`, to give strategy something to bridge toward.

## When NOT to Use
- The founder needs the *plan* to reach the vision (strategy, objectives, tactics, metrics) → `strategic-planning`. This skill produces the destination, not the route.
- The founder wants brand voice / tagline / marketing copy → marketing domain.
- The founder wants to understand their own motives first → `motivation-mapper` (run it before this if motives are unclear).
- The statement needs legal/regulatory review (claims, trademarks) → legal domain.

## Required Context
Reads Business Memory: `company` (what it does, stage, size, model, any existing mission/vision), `leader` (founder motives and values from `motivation-mapper` — a vision must sustain the founder), `market` (the broad, diverse audience the company serves; competitive landscape for distinctiveness), `offerings` (the distinctive value delivered), `customers` (who is served now), `goals` (the founder's 5-year targets — size, geography, markets). Facts carry `source`, `confidence`, `as_of`. This skill produces founder-facing draft language; it does not publish anything externally.

## Inputs
```yaml
input:
  mode: enum(mission, vision, both)
  mission_inputs:
    what_we_do: str                # the activity/product/service
    for_whom: str                  # the customer / market served
    distinctive_value: str         # how it distinguishes from competitors / connects to a broad market
  vision_inputs:
    future_business: str           # 5-yr picture: size, revenue, geography, markets, recognition
    future_culture: str            # the culture, how it inspires/rewards employees
    talent_distinction: str        # how the company will stand out to talented employees
  existing_statement: str          # current mission/vision to refine, if any
  founder_motives: [str]           # from motivation-mapper, so the vision reflects real drivers
  iteration: int                   # 1 = first draft, 2+ = refinement pass
```

## Missing Information Protocol
1. For a **mission**, the two essentials are (a) what the business does + for whom, and (b) its distinctive value. If either is missing, ask the founder ONE concise batch; do not invent a value proposition.
2. For a **vision**, the essentials are the 5-year business picture AND the future culture (both are required — a vision that covers only one fails the checklist). Ask for the missing half.
3. Pull the founder's real motives from `motivation-mapper` before drafting a vision; a vision built on a motive the founder doesn't feel will not sustain them.
4. Never fabricate metrics, market claims, or a distinctiveness the company hasn't demonstrated — draft with the founder's own material and mark any placeholder for the founder to confirm.
5. Always produce a draft and invite refinement rather than presenting a first pass as final.

## Diagnostic Questions
Answered internally:
- **Mission (NOW/DO):** What does the company do now, and for whom? How is it distinguished from competitors while connecting with a broad, diverse market?
- **Vision (FUTURE/BECOME):** What should the company become in the next ~5 years — size, locations, markets, employees? What will the culture be? How will the company be distinguished in the market for *talented employees*?
- **Sustaining fit:** Does this vision reflect what actually drives the founder (from their motives)?
- **Quality:** Does the vision pass all six checks? Is the mission descriptive and tight?

## Analysis Framework
The Mission → Vision → Growth model:
- **Mission = NOW / DO** (descriptive): what the company does, for whom, and the distinctive value delivered. Tight, 1–2 sentences.
- **Vision = FUTURE / BECOME** (inspirational): what the company will be in ~5 years, covering both business and culture.
- The bridge from mission to vision is the **Growth Plan / Actions**, decomposed `Strategy → Objectives → Tactics → Metrics` — owned by `strategic-planning`, not this skill.

Both statements are built iteratively: Draft 1 → feedback → Draft 2 (shorter, more inspirational for the vision). The vision is validated against a six-point checklist; the mission against a descriptive/tightness standard.

**Mission structure (exemplar, structure only):** "[Type of company] specializing in [what] for [whom] in [where]. Through [distinctive strengths], we provide [the superior alternative / distinctive value]."

## Calculations
No numeric formulas. Two validation rubrics:

**Vision six-point checklist (all must pass):**
1. **Future-oriented** — set ~5 years out.
2. **Covers both business AND culture** — not one without the other.
3. **Effective** — clearly conveys the intended direction.
4. **Efficient** — tight, ~2–4 sentences.
5. **Compelling** — vivid, memorable language.
6. **Appealing to a broad, diverse audience** — including future talent.

**Mission standard:** descriptive (not aspirational), states what + for whom + distinctive value, 1–2 sentences, plain and repeatable.

## Decision Rules
- IF `mode` includes mission AND `distinctive_value` is missing THEN ask; do not draft a mission without a differentiator.
- IF `mode` includes vision AND either `future_business` OR `future_culture` is missing THEN ask for the missing half (both are required to pass check #2).
- IF the vision draft covers business but not culture (or vice versa) THEN it FAILS check #2 → revise before presenting.
- IF the vision exceeds ~4 sentences or reads as a paragraph THEN it FAILS check #4 (efficient) → shorten in the next iteration.
- IF the vision is generic/interchangeable-with-any-company THEN it FAILS check #5 (compelling) → add vivid, specific language.
- IF the vision speaks only to customers and ignores employees/talent THEN it FAILS check #6 → add the talent-distinction dimension.
- IF the vision conflicts with the founder's real motives (from `motivation-mapper`) THEN flag it — a vision the founder doesn't believe won't sustain the company; recommend resolving motives first.
- IF `iteration = 1` THEN present Draft 1 + explicit checklist pass/fail + specific improvement asks; do not treat it as final.
- IF the founder wants the plan to reach the vision THEN hand off to `strategic-planning`.

## Procedure
1. Determine `mode` and `iteration`. Load `company`, `leader` (motives), `market`, `offerings`, `customers`, `goals`.
2. **Mission:** assemble what + for whom + distinctive value into a 1–2 sentence descriptive statement using the structure; check it is descriptive, tight, and repeatable.
3. **Vision:** assemble the 5-year business picture + future culture + talent distinction into a 2–4 sentence inspirational statement.
4. Run the vision against all six checks; record pass/fail per check with a reason.
5. Check the vision against the founder's motives for sustaining fit.
6. If any check fails, revise (shorten, sharpen, add the missing dimension) and re-check; on iteration 1 present the draft with the checklist and specific improvement requests rather than forcing a pass.
7. Assemble output: draft statement(s), checklist results, and the specific next-iteration asks.
8. At L1, write the agreed statement to `company` and `strategy` and note the vision in `leader` — prepared and shown to the founder; nothing is published externally.
9. Recommend `strategic-planning` to build the bridge from mission to vision.

## Output
```yaml
output:
  mission_statement: str            # 1-2 sentences, descriptive
  mission_meets_standard: bool
  mission_notes: str
  vision_statement: str             # 2-4 sentences, inspirational
  vision_checklist:
    future_oriented: bool
    covers_business_and_culture: bool
    effective: bool
    efficient: bool
    compelling: bool
    appealing_broad_audience: bool
  vision_passes_all: bool
  sustaining_fit_with_founder_motives: enum(aligned, partial, conflict)
  iteration: int
  next_iteration_asks: [str]        # specific changes to make if not yet passing
  recommended_next_skills: [str]
```

## Recommendations
Drafts are refined iteratively: the first pass is explicitly a draft, presented with its checklist result and the specific improvements needed (shorten, add culture, make it vivid, speak to talent). Priority in refinement is any failed checklist item, then sustaining-fit with the founder's motives, then polish. The recommendation is always to iterate to a passing vision before locking it and handing strategy the destination. Statements are the founder's to approve and own.

## Execution Opportunities
- Draft/refine mission and vision statements (founder-facing) — reversible, LOW.
- Write the agreed mission/vision to `company` and `strategy` — reversible, LOW; prepared for founder approval at L1.
- Note the vision in `leader` for alignment with the founder's development plan — reversible, LOW.
- Propose (not run) `strategic-planning`, `motivation-mapper`.
This skill does not publish the statement externally (website, deck, press) — external publication is a separate, founder-approved marketing/legal step.

## Human Approval Requirements
- L1: internal writes are prepared and shown to the founder; the founder approves the final wording.
- External publication of the mission/vision (website, investor materials, marketing) requires founder approval and routes through marketing (and legal if it makes claims). Per `AUTONOMY_AND_APPROVAL_MODEL.md`, this skill drafts and stores; it does not publish.

## Escalation Conditions
- **The vision cannot pass the checklist because the underlying strategy is unclear** → route to `strategic-planning` (the destination depends on a viable route).
- **Founder motives conflict with the vision** → recommend `motivation-mapper` before locking.
- **The statement makes market or performance claims that could mislead** → route to legal/marketing before any external use.
- **Founders disagree (co-founders) on the vision** → surface the disagreement; do not paper over it with vague language.

## KPIs
- Vision passes all six checks.
- Mission and vision are short enough that the team can repeat them from memory.
- Founder confidence that the vision reflects what truly drives them (sustaining fit = aligned).
- Downstream: `strategic-planning` can decompose the vision into Strategy → Objectives → Tactics → Metrics without ambiguity.

## Monitoring
After adoption: watch whether the statements actually get used (in hiring, planning, comms) — an unused vision is a failed one. Re-verify sustaining fit if the founder's motives shift. Revisit the vision as the ~5-year horizon approaches or the company materially changes stage.

## Follow-Up
- Time-triggered: revisit the vision annually and fully refresh as the 5-year horizon nears.
- Event-triggered: major pivot, new market, fundraise, rebrand, scale-hiring push, or a shift in founder motives.

## Related Skills
Fed by `motivation-mapper` (founder motives → a sustaining vision) and `leadership-style-assessment` (leader identity). Feeds `strategic-planning` (builds the Growth Plan bridge from mission to vision) and `leadership-growth-planner` (personal goals align to the company vision). External use routes to marketing/legal.

## Guardrails
- Never fabricate metrics, market claims, or a distinctiveness the company hasn't shown; mark placeholders for founder confirmation.
- Do not publish externally — draft and store only; external use is a separate founder-approved step (marketing/legal).
- A vision must cover both business and culture and speak to talent — never ship a customer-only vision as complete.
- Keep the mission descriptive and the vision efficient; resist bloat.
- Do not let a polished statement paper over an unresolved strategy gap or co-founder disagreement.

## Example
**Founder input (iteration 1, both):** "We do independent repair for high-end European cars in the city; people come to us instead of the dealer because we're faster, more personal, and just as expert. In 5 years I want three locations, be the name people think of for exotic-car care in the region, and I want it to be the shop the best technicians want to work at — where they're trusted, keep learning, and share in the wins." Founder motives (from motivation-mapper): doing the very best work; building something recognized.
**Reasoning:** Mission has what (independent high-end European car repair), for whom (owners of those cars in the city), distinctive value (faster, personal, dealer-level expertise → superior alternative to the dealer). Vision has business (3 locations, regional recognition) but the culture/talent half is present too (trusted technicians, learning, shared wins). Run checklist: future-oriented ✓ (5 yr); business+culture ✓; effective ✓; efficient — draft is a bit long → tighten; compelling — "the name people think of" is decent, sharpen; broad/talent appeal ✓ (speaks to technicians). Sustaining fit: aligned (best work + recognition match the founder's motives).
**Output (abridged):** mission_statement: "An independent specialist in high-line European and exotic car service in [city]. Through faster, more personal, dealer-level workmanship, we give owners a superior alternative to the dealership." vision_statement (Draft 2, tightened): "By [year+5], we are the name the region trusts for exotic-car care — three thriving locations known for flawless work — and the shop the best technicians choose, because here they are trusted, always learning, and share in what we build." vision_checklist all true; vision_passes_all true; sustaining_fit aligned; next_iteration_asks: ["confirm the third-location target and the year"]. recommended_next_skills: [strategic-planning].
**Executed vs. approval:** Presented Draft 1 with the checklist, then Draft 2 after tightening; on founder sign-off, wrote mission/vision to `company` and `strategy` and noted the vision in `leader`. Nothing published externally — that routes to marketing/legal when the founder is ready.

## Provenance
SOURCE. Derives from the leadership domain's Mission → Vision → Growth model (Mission = NOW/DO, Vision = FUTURE/BECOME, bridged by Strategy → Objectives → Tactics → Metrics), the Mission Statement Builder (D5) and Vision Statement Builder (D6) with its six-point validation checklist and iterative Draft 1 → Draft 2 method. De-branded: the exemplar is structural only and no source book, author, program, or planning tool is cited. See `internal/PROVENANCE_MAP.md`.
