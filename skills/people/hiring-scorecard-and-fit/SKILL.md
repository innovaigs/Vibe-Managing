---
name: hiring-scorecard-and-fit
domain: people
version: 0.1.0
autonomy_ceiling: L1
provenance: SOURCE
reads: [team.org.open_roles, company, team.culture, founders]
writes: [decisions]
related_skills: [interview-guide-and-scorecard, job-description-builder, onboarding-builder, culture-diagnostic]
owned_by_agents: [people-agent]
---

# Skill: Hiring Scorecard and Fit

## Purpose
Evaluate an interviewed candidate against the role's competencies and the company's values, converting behavioral evidence into an A–D scorecard and an overall recommendation — while actively blocking affinity bias so "fit" means alignment to mission/goals/values, not personal similarity to the interviewer.

## When to Use
- After interviews, to score a candidate and produce a defensible recommendation.
- Founder asks: "Was this candidate any good?", "Score them", "Is this person a good fit?", "Compare these two candidates."
- Calibrating multiple interviewers' scorecards into one decision.

## When NOT to Use
- To build the blank scorecard or questions → `interview-guide-and-scorecard`.
- To make or send the offer/rejection → those are employment actions requiring founder approval (and legal for rejections in sensitive cases); this skill only recommends.
- To assess overall company culture health → `culture-diagnostic`.

## Required Context
- The completed scorecard(s) with behavioral evidence per competency (from interviewers).
- The JD's `critical_tasks`, `competencies`, and `values_sought`.
- `company.mission`, `company.vision`, `company.values` — the standard "fit" is measured against.
- Must-pass criteria flagged on the scorecard template.

## Inputs
```yaml
input:
  candidate_ref: str                 # anonymized handle; PII referenced, not stored inline
  role_ref: str
  scorecards:                        # one per interviewer/round
    - interviewer: str
      round: int
      rows:
        - criterion: str
          competency: str
          evidence_notes: str        # what the candidate actually said/did (behavioral)
          score: enum(A, B, C, D)
          must_pass: bool
      overall_rating: enum(Highly Recommend, Acceptable, Acceptable with Reservations, Unacceptable)
      comments: str
  values_sought: [str]
  company_mission: str
  company_goals: [str]
  fit_signals:                       # for the affinity-bias check
    - signal: str                    # anything the interviewer cited as "fit"
      basis: str                     # why it was called fit
```

## Missing Information Protocol
1. Require behavioral evidence for every score; a score with no evidence note is treated as unsupported and downgraded to "insufficient evidence," not counted as strong.
2. Pull competencies/values/mission from the JD and `company` before asking.
3. If scorecards are incomplete (missing must-pass rows), ask the interviewer(s) for the missing evidence — do not infer.
4. **Never assume** competence or fit from resume/pedigree, shared background, or interviewer "gut feel." Never fabricate evidence.

## Diagnostic Questions
- Is each competency score backed by concrete past-behavior evidence, or by impression/pedigree? (Downgrade unsupported scores.)
- Does the candidate clear every must-pass competency?
- On the three selection tiers (F2): visible qualifications, intangibles (coachability, values, learner orientation), and alignment (vision/goals/values) — where is the candidate strong vs. weak?
- Is any "fit" judgment resting on shared background, interests, or comfort? → strip it out as affinity bias (R8).
- Re-score fit strictly against: mission enthusiasm, working approach, decision/risk alignment, and complementary perspective (F3).
- Do interviewers disagree, and does the disagreement trace to evidence or to bias?
- Did any answer reveal a values conflict (integrity question) or an unaddressed competency gap to probe in a later round?

## Analysis Framework
Applies the three-tier selection model (F2), the correct-vs-wrong fit definition and affinity-bias trap (F3), the wrong-hire/fit-risk diagnostic (DG4), and the A–D scoring convention.

1. **Evidence audit** — for each scored row, confirm behavioral evidence exists; downgrade unsupported scores.
2. **Competency scoring** — consolidate A–D per competency across interviewers; note dispersion.
3. **Must-pass gate** — any must-pass competency below the threshold (e.g. below B, per role config) fails the candidate regardless of other strengths.
4. **Three-tier readout** — summarize visible qualifications, intangibles, and company alignment separately (so a strong-on-paper/weak-on-values candidate is visible).
5. **Affinity-bias filter (mandatory)** — for every stated "fit" signal, test its basis: if it rests on shared background/interests/comfort, discard it and record the bias flag. Re-derive fit only from the four correct-fit dimensions (F3).
6. **Calibration** — reconcile interviewer disagreements against evidence; do not average away a legitimate red flag.
7. **Overall recommendation** — Highly Recommend / Acceptable / Acceptable with Reservations / Unacceptable, with the reasons and the specific items to probe if advancing.

## Calculations
- **Per-competency consolidated score:** modal/most-evidenced A–D across interviewers; if split, report the range and the evidence for each.
- **Must-pass gate:** IF any must_pass competency < B THEN overall = Unacceptable (hard gate; overrides other scores).
- **Overall rating:** qualitative synthesis, not a numeric average — anchored to the A–D distribution and the three-tier readout. Guidance: mostly A/B with all must-pass ≥ B → Highly Recommend/Acceptable; notable gap with mitigation path → Acceptable with Reservations; must-pass fail or values conflict → Unacceptable.
- **Affinity-bias adjustment:** each discarded similarity-based "fit" signal is logged; the fit sub-score is recomputed from only the four F3 dimensions.

## Decision Rules
- IF a score has no behavioral evidence THEN treat it as insufficient evidence (not strong); request evidence or discount it.
- IF any must-pass competency is below threshold THEN recommend Unacceptable regardless of other strengths.
- IF a "fit" rationale rests on shared background/interests/comfort/pedigree THEN flag affinity bias and exclude it from the fit score; re-score fit against mission enthusiasm, working approach, decision/risk alignment, and complementary perspective (R8, F3).
- IF the integrity/values question revealed a values conflict THEN cap the recommendation at Acceptable with Reservations and require founder attention (values are gating).
- IF interviewers disagree materially THEN surface both evidence sets to the founder rather than averaging.
- IF the candidate is strong on paper but weak on intangibles/alignment THEN say so explicitly (F2) — do not let credentials mask a fit/values gap.
- IF the pool is homogeneous or the "fit" language is consistently similarity-based THEN flag a systemic affinity-bias risk to `culture-diagnostic` (R8, DG4).
- IF advancing THEN list the specific competency gaps to probe in the next round.

## Procedure
1. Load completed scorecards, JD competencies/values, and company mission/goals.
2. Run the evidence audit; downgrade unsupported scores.
3. Consolidate A–D per competency; note dispersion.
4. Apply the must-pass gate.
5. Produce the three-tier readout (visible / intangibles / alignment).
6. Run the affinity-bias filter on every "fit" signal; recompute fit from the four F3 dimensions; log bias flags.
7. Calibrate interviewer disagreements against evidence.
8. Form the overall recommendation with reasons and probe-list.
9. Write a `decisions` record (candidate referenced by handle, `restricted` sensitivity); prepare the recommendation package for founder.
10. Do NOT issue any offer/rejection — hand the decision to the founder.

## Output
```yaml
output:
  candidate_ref: str
  role_ref: str
  competency_scores:
    - competency: str
      consolidated_score: enum(A, B, C, D, insufficient_evidence)
      evidence_summary: str
      must_pass: bool
      passed_gate: bool
  three_tier_readout:
    visible_qualifications: str
    intangibles: str                 # coachability, values, learner orientation
    company_alignment: str           # vision/goals/values
  fit_assessment:
    fit_score_basis: [str]           # ONLY F3 dimensions: mission enthusiasm, working approach, decision/risk alignment, complementary perspective
    affinity_bias_flags: [str]       # similarity-based signals discarded
    complementary_perspective: str   # what this person adds that the team lacks
  values_conflicts: [str]
  overall_recommendation: enum(Highly Recommend, Acceptable, Acceptable with Reservations, Unacceptable)
  rationale: str
  probe_next_round: [str]
  systemic_flags: [str]              # e.g. homogeneous pool / affinity-bias pattern → culture-diagnostic
  decision_owner: "founder"          # this skill never decides
```

## Recommendations
Lead with evidence, not impression. State the three tiers separately so a pedigreed-but-misaligned candidate cannot slide through on credentials. Treat every discarded similarity-based "fit" as a win against homogeneity. Recommend, never decide — the hire/no-hire and the offer belong to the founder.

## Execution Opportunities
- Consolidate scorecards and produce the assessment (reversible, LOW) — L1 prepare.
- Write a `restricted` `decisions` record with the recommendation (reversible, LOW).
- Assemble the founder recommendation package / approval request (reversible, LOW).
- NOT executed: offers, rejections, or any candidate-facing communication.

## Human Approval Requirements
- **The hire/no-hire decision, and any offer or rejection, ALWAYS require founder approval.** This skill recommends only (L1); it never notifies a candidate or commits to employment. (AUTONOMY_AND_APPROVAL_MODEL §4.)
- Any rejection where a protected-class or discrimination concern could arise must be reviewed by founder + HR/legal before it is sent.
- Compensation/offer terms are out of scope here and require founder approval (+ comp/legal).

## Escalation Conditions
- A values conflict, discrimination concern, or protected-class issue in the evidence → HR professional / attorney; founder informed.
- Consistent similarity-based "fit" language or a homogeneous pipeline → flag to `culture-diagnostic` + founder (systemic bias).
- Interviewer disagreement rooted in bias rather than evidence → founder; do not average it away.
- Low-confidence or missing evidence on a must-pass competency → request another round; do not recommend on thin evidence.

## KPIs
- Quality-of-hire: 90/180-day performance and retention of candidates advanced with this skill.
- Affinity-bias catch rate: similarity-based "fit" signals flagged and excluded.
- Pipeline/hire diversity trend (are complementary-perspective hires increasing?).
- Decision reversal rate (offers regretted) — should fall as evidence discipline improves.

## Monitoring
Track hired candidates' actual performance vs. their scorecard to calibrate which competencies and evidence patterns actually predict success. Watch for recurring affinity-bias flags across roles → systemic culture signal.

## Follow-Up
Runs per candidate during selection. Re-run after each round with new evidence. On a hire, hand critical-task gaps to `onboarding-builder` as ramp focus areas. Feed systemic bias flags to `culture-diagnostic`.

## Related Skills
`interview-guide-and-scorecard` (produces the instrument this applies), `job-description-builder` (defines competencies/values), `onboarding-builder` (uses probe-list/gaps for ramp), `culture-diagnostic` (receives systemic bias flags).

## Guardrails
- Evidence-based only: no score without behavioral evidence; no fit judgment without an F3 basis.
- Affinity bias is actively blocked — similarity/comfort/pedigree is never a fit reason (R8, F3, DG4).
- Values conflicts and must-pass failures are gating.
- Never decide, offer, or reject — recommend to the founder; protected-class/rejection concerns go to HR/legal.
- Individual candidate data is `restricted`; reference by handle, never expose PII or comp externally.

## Example
**Input:** Two scorecards for candidate "C-208," Operations Coordinator. Interviewer 1: Highly Recommend, comment "great fit — we both went to the same school and love hiking." Interviewer 2: Acceptable with Reservations, evidence that the candidate resolved a supplier crisis (A on exception-resolution) but gave a vague answer on reliability (must-pass) with no concrete example.

**Reasoning:** Evidence audit — exception-resolution = A (strong evidence); reliability = insufficient evidence (no example) and it is must-pass. Affinity-bias filter — Interviewer 1's "same school / love hiking" is pure similarity → discarded and flagged; nothing about mission enthusiasm or complementary perspective was actually cited, so the fit score cannot rest on it. Must-pass gate — reliability unproven → cannot recommend a hire yet.

**Output:** Competency scores with reliability = insufficient_evidence (must_pass, gate not passed); fit_assessment with affinity_bias_flags: ["same school", "shared hobby"] and a note that no valid F3 fit evidence was captured; overall_recommendation: Acceptable with Reservations; probe_next_round: ["reliability — get a concrete past example", "mission alignment — actually assess it"]; decision_owner: founder.

**Executed vs. approval:** Produced the assessment and the founder package (L1). No offer/rejection issued — held for founder; the affinity-bias pattern was flagged for `culture-diagnostic`.

## Provenance
SOURCE — derived from the visible/intangible/fit selection model (F2), the correct-vs-wrong cultural-fit definition and affinity-bias trap (F3), the wrong-hire/fit-risk diagnostic (DG4), the affinity-bias rejection rule (R8), and the A–D scoring + Highly Recommend/Acceptable/… rating scale in `05-people-org.md`.
