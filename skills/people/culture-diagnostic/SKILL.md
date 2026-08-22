---
name: culture-diagnostic
domain: people
version: 0.1.0
autonomy_ceiling: L1
provenance: SYNTH
reads: [team.culture, company, team.people, founders, metrics, goals]
writes: [team.culture, decisions]
related_skills: [organizational-design, hiring-scorecard-and-fit, onboarding-builder, hr-process-coverage-audit, delegation-planner]
owned_by_agents: [people-agent]
---

# Skill: Culture Diagnostic

## Purpose
Assess the gap between the company's *stated* values and its *lived* behavior, read engagement signals, and recommend concrete alignment actions — so culture is managed deliberately (the medium every people-process runs inside) instead of drifting. Surfaces where "what we say" and "what we reward/do" diverge, and where affinity-bias homogeneity is creeping in.

## When to Use
- Founder asks: "Is our culture healthy?", "Do we live our values?", "Why does morale feel off?", "Is engagement dropping?"
- Rising turnover, weak commitment signals, or friction after growth/reorg.
- Periodic culture review; after `hiring-scorecard-and-fit` flags systemic affinity bias; alongside `organizational-design`.

## When NOT to Use
- To score a candidate's fit → `hiring-scorecard-and-fit`.
- To make invisible culture visible to one new hire → `onboarding-builder` (P5).
- To audit formal HR procedures → `hr-process-coverage-audit`.
- Any specific-employee performance, discipline, or status decision → founder + HR/legal.

## Required Context
- `company.mission`/`vision`/`values` — the stated values.
- `team.culture.stated_values`, `observed_signals`, `engagement_indicators`.
- `metrics` — turnover, employee commitment, team learning (Org Audit Part I outcomes).
- `team.people` — composition/diversity signals (for homogeneity/affinity-bias read).
- Observed behaviors: what actually gets rewarded, tolerated, and celebrated (Org Audit Part III inputs).

## Inputs
```yaml
input:
  stated_values: [str]               # from company.values, required
  mission: str
  observed_behaviors:                # Org Audit Part III: what actually happens
    - behavior: str
      frequency: enum(rare, occasional, common)
      rewarded_or_tolerated: enum(rewarded, tolerated, punished, ignored)
  engagement_signals:
    turnover_rate: number|null
    commitment_rating: enum(highly_satisfied, satisfied, dissatisfied)|null
    team_learning: enum(highly_satisfied, satisfied, dissatisfied)|null
    qualitative_signals: [str]       # e.g. "people stopped raising ideas", "silos"
  symbols_rituals_stories: [str]     # what the org celebrates/tells (Part III)
  team_composition_signals: [str]    # homogeneity / affinity-bias indicators
  recent_changes: [str]              # growth, reorg, new hires
```

## Missing Information Protocol
1. Pull stated values, engagement metrics, and composition from memory before asking.
2. If observed-behavior data is thin, ask the founder **one batched question**: "For each stated value, name one recent behavior that shows we live it — and one that contradicts it. What do we actually reward vs. just say?"
3. Prefer behavioral evidence over opinion; a value with no observable behavior is treated as aspirational-only, not lived.
4. **Never assume** culture health from the founder's self-report alone; triangulate with turnover, commitment, and behavior signals. Flag low-confidence findings.

## Diagnostic Questions
- For each stated value: what observable behavior demonstrates it, and what behavior contradicts it? (Stated vs. lived.)
- What does the org actually *reward, tolerate, punish, or ignore*? (Behavior follows consequences, not slogans.)
- What are the shared beliefs/assumptions, common practices, and symbols/rituals/stories? (Org Audit Part III — the invisible culture.)
- What do engagement signals say (turnover, commitment, learning, qualitative)? Is enthusiasm for the mission real or performative?
- Is fit being defined as personal similarity (affinity bias → homogeneity), or as mission enthusiasm + working approach + decision/risk alignment + complementary perspective? (F3)
- Did a recent change (growth/reorg) shift the culture, and in which direction?
- Where does the founder's own behavior model or contradict the stated values? (Culture flows from the top.)

## Analysis Framework
Applies the correct-vs-wrong cultural-fit model (F3), the cultural-iceberg (visible vs. invisible culture), the Organizational Audit Part III (shared values, beliefs/assumptions, practices, symbols/rituals/stories), and Part I engagement outcomes — assembled into a stated-vs-lived gap analysis.

1. **Values-in-action mapping:** for each stated value, gather the behaviors that demonstrate vs. contradict it, and what is rewarded vs. tolerated. Classify each value as *lived*, *aspirational*, or *violated*.
2. **Iceberg read:** separate visible culture (perks, dress, office) from invisible culture (trust, decision norms, unspoken expectations, biases); name the invisible norms that actually drive behavior.
3. **Engagement synthesis:** combine turnover, commitment, learning, and qualitative signals into an engagement read; link weak signals to specific values gaps or changes.
4. **Homogeneity / affinity-bias scan:** check composition and "fit" language for similarity-based selection; a homogeneous, similarity-selected team is a culture risk (groupthink), not a strength (F3).
5. **Founder-behavior check:** identify where leadership behavior reinforces or undermines the stated values (the strongest culture signal).
6. **Alignment actions:** for each gap, recommend a concrete action — change what gets rewarded, make an invisible norm explicit, adjust a ritual/symbol, fix a process (route to `hr-process-coverage-audit`), or fix selection (route to `hiring-scorecard-and-fit`/`job-description-builder`).

## Calculations
- **Stated-vs-lived gap score** per value: lived = 0, aspirational = 1, violated = 2; sum across values → higher = larger culture gap.
- **Engagement index** (qualitative-to-ordinal): combine turnover trend, commitment rating, and learning rating into low/moderate/healthy; any "dissatisfied" outcome flags a hotspot.
- **Homogeneity flag:** raised when composition signals + similarity-based "fit" language co-occur.
- **Reward-alignment ratio** = values-consistent behaviors rewarded ÷ total rewarded behaviors (low = the org rewards things that contradict its values).
- No single composite culture "score" is asserted with high confidence; findings are ranged and evidence-linked (SYNTH — culture is inferred, not measured precisely).

## Decision Rules
- IF a stated value has no demonstrating behavior THEN mark it aspirational-only and recommend either living it (change rewards) or dropping the pretense.
- IF a stated value is actively contradicted by rewarded/tolerated behavior THEN mark it violated and prioritize an alignment action (this erodes trust fastest).
- IF the org rewards behaviors that contradict its values THEN recommend changing what gets rewarded/recognized (behavior follows consequences).
- IF composition + "fit" language show similarity-based selection THEN flag affinity-bias homogeneity and route to `hiring-scorecard-and-fit`/`job-description-builder` (screen fit against goals/values, not similarity — R8, F3).
- IF founder behavior contradicts a stated value THEN surface it directly to the founder (culture flows from the top) — highest-leverage fix.
- IF engagement signals are weak AND tied to a values gap THEN prioritize that gap.
- IF any signal implicates a *specific employee's* conduct/performance THEN do NOT diagnose it here — route to founder + HR/legal.
- IF signals suggest harassment, discrimination, or a hostile-environment issue THEN escalate immediately to HR/legal; do not treat it as a "culture tweak."

## Procedure
1. Load stated values, engagement metrics, composition, and observed behaviors.
2. Map each value to demonstrating vs. contradicting behavior and to what's rewarded/tolerated; classify lived/aspirational/violated.
3. Read the iceberg: name the invisible norms driving behavior.
4. Synthesize engagement signals and link weak ones to gaps/changes.
5. Run the homogeneity/affinity-bias scan.
6. Check founder behavior vs. stated values.
7. Derive prioritized alignment actions; route selection/process/structure fixes to the right skills.
8. Write findings to `team.culture` and a `decisions` record; present to the founder.

## Output
```yaml
output:
  summary: str
  values_in_action:
    - stated_value: str
      status: enum(lived, aspirational, violated)
      demonstrating_behaviors: [str]
      contradicting_behaviors: [str]
      what_is_rewarded: str
  invisible_culture:
    named_norms: [str]               # decision norms, trust, unspoken expectations
    symbols_rituals_stories: [str]
  engagement_read:
    index: enum(low, moderate, healthy)
    hotspots: [str]                  # dissatisfied outcomes / qualitative red flags
    turnover_note: str
  affinity_bias_flag:
    raised: bool
    evidence: [str]
    route_to: [str]                  # hiring-scorecard-and-fit / job-description-builder
  founder_behavior_notes: [str]      # where leadership reinforces/undermines values
  alignment_actions:
    - gap: str
      action: str
      type: enum(change_rewards, make_norm_explicit, adjust_ritual, fix_process, fix_selection, founder_modeling)
      priority_rank: int
      route_to_skill: str
  confidence: number                 # 0-1; culture inferences are ranged
  escalations: [str]                 # HR/legal items (harassment/discrimination/specific-person)
```

## Recommendations
Prioritize violated values over merely aspirational ones — an actively contradicted value destroys trust faster than an unmet one. The highest-leverage fixes are changing what the org *rewards* and changing what the *founder models*, not writing new value statements. Treat similarity-based "fit" as a risk to correct, not a culture to protect. Never dress up a harassment/discrimination signal as a culture initiative — escalate it.

## Execution Opportunities
- Produce the culture diagnosis and alignment-action plan (reversible, LOW) — L1 prepare.
- Draft internal culture communications / norm-articulation docs for founder review (reversible, LOW).
- Create internal tasks for alignment actions and route fixes to other skills (reversible, LOW).
- Write findings to `team.culture` and a `decisions` record (reversible, LOW).
- NOT executed: any specific-person action, any external culture messaging, any policy change (route to HR/legal).

## Human Approval Requirements
- **Any action touching a specific employee's conduct, performance, or status ALWAYS requires founder approval AND HR/legal review** — never handled as a culture tweak.
- Standing policy changes (code of conduct, anti-harassment, recognition/reward systems that affect comp) require founder + HR/legal.
- External-facing culture/employer-brand messaging requires founder approval.

## Escalation Conditions
- Any signal of harassment, discrimination, retaliation, or hostile environment → HR professional / attorney immediately; do not proceed as culture work.
- Protected-class patterns in composition/treatment → HR/legal.
- A specific person is implicated → founder + HR (out of this skill's scope).
- Engagement collapse / spiking turnover with cash/continuity risk → founder + risk agent.

## KPIs
- Stated-vs-lived gap score trending down (fewer violated/aspirational values).
- Engagement index and commitment rating improving; turnover trending down.
- Reward-alignment ratio rising (org rewards what it says it values).
- Affinity-bias flags falling; pipeline/hire diversity and complementary-perspective hires rising.
- Alignment-action completion rate.

## Monitoring
Re-measure engagement and turnover after alignment actions; watch whether changed rewards actually shift behavior and whether newly-explicit norms hold. Track recurring affinity-bias flags from `hiring-scorecard-and-fit`. Watch for any escalation-worthy signal continuously.

## Follow-Up
Run on a periodic culture-review cadence, after growth/reorg, when engagement/turnover signals degrade, or when `hiring-scorecard-and-fit` reports systemic affinity bias. Feed structural/process fixes to `organizational-design` and `hr-process-coverage-audit`; feed selection fixes to the hiring skills.

## Related Skills
`organizational-design` (culture as the system's medium; structural causes), `hiring-scorecard-and-fit` and `job-description-builder` (fix affinity-bias in selection), `onboarding-builder` (make invisible culture visible to new hires), `hr-process-coverage-audit` (process/policy fixes).

## Guardrails
- Behavior over slogans: a value is "lived" only with observable demonstrating behavior; culture is inferred, so findings are ranged with explicit confidence (SYNTH).
- Affinity-bias homogeneity is a risk to correct, never a culture to defend (F3, R8).
- Never diagnose or act on a specific employee — founder + HR/legal.
- Harassment/discrimination/hostile-environment signals escalate immediately to HR/legal — never treated as a culture tweak.
- Individual and composition data is `restricted`/confidential; do not expose externally.

## Example
**Input:** Stated values [transparency, ownership, growth]. Observed: leadership makes major decisions in closed rooms then announces them (contradicts transparency); the person who quietly fixes things gets praised while the person who raises problems is seen as negative (contradicts ownership/transparency). Turnover up; commitment rated dissatisfied; qualitative signal "people stopped bringing up ideas." Team increasingly hired from the founder's alma mater network.

**Reasoning:** Transparency = violated (closed decisions, punished problem-raising). Ownership = aspirational (praised only when quiet, not when surfacing issues). Growth = lived (learning invested in). Reward-alignment low: the org rewards silence over surfacing problems. Homogeneity flag raised (alma-mater network hiring → affinity bias). Founder behavior (closed decisions) is the root of the transparency gap — highest-leverage fix. No specific-person conduct issue rising to HR/legal, but "people stopped raising ideas" is a trust erosion to fix, not ignore.

**Output (abridged):** values_in_action (transparency=violated, ownership=aspirational, growth=lived); invisible_culture norms ["decisions happen behind closed doors", "raising problems is risky"]; engagement_read index=low, hotspots=[commitment dissatisfied, ideas suppressed]; affinity_bias_flag raised (alma-mater hiring) → route to hiring-scorecard-and-fit/job-description-builder; founder_behavior_notes ["closed decision-making undermines stated transparency"]; alignment_actions ranked: [1) founder opens decision rationale (founder_modeling), 2) recognize problem-surfacing publicly (change_rewards), 3) widen sourcing beyond the network (fix_selection)]; confidence 0.7.

**Executed vs. approval:** Produced the diagnosis, ranked actions, and routed the selection fixes (L1). The founder-behavior change, any recognition/reward-system change, and any policy update were **held for founder approval**; no specific-person or external messaging action taken.

## Provenance
SYNTH — assembled from the correct-vs-wrong cultural-fit model and affinity-bias trap (F3), the cultural-iceberg (visible/invisible culture), the Organizational Audit Part III (shared values, beliefs, practices, symbols/rituals/stories) and Part I engagement outcomes (W5), and the affinity-bias rule (R8) in `05-people-org.md`, generalized with standard stated-vs-lived / reward-alignment culture-diagnosis practice to make it executable. Culture inferences are explicitly ranged (low-confidence by nature).
