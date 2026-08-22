# AUTONOMY_AND_APPROVAL_MODEL

**Deliverable 10 — Permissions, risk, approvals, escalation.**

Vibe Managing never lets an agent do whatever it wants. Every action an agent proposes is classified by **risk** and **reversibility**, matched against the agent's **granted autonomy level** for that action-type, and then either auto-executed, executed-with-notice, or held for **human approval**. Everything is logged and, where possible, reversible.

This is the control plane. It is enforced by `core/permissions/` (what an agent *may* attempt) and `core/approvals/` (routing + audit of what requires a human).

---

## 1. Autonomy levels

| Level | Name | The agent may… | Human role |
|---|---|---|---|
| **L0** | Observe | read, analyze, diagnose, recommend | Human does everything executable |
| **L1** | Prepare | create drafts, plans, proposed actions, staged changes | Human approves every execution |
| **L2** | Limited autonomy | execute reversible, low-risk, pre-approved action-types | Human notified; can undo |
| **L3** | Supervised autonomy | execute larger workflows within budget/policy/role/risk limits | Human sets limits; reviews exceptions |
| **L4** | High autonomy | execute mature, proven workflows end-to-end | Human audits; strong observability + rollback required |

**Autonomy is per action-type, not per agent.** A Growth Agent may hold L3 for "schedule social post" while holding only L1 for "launch paid campaign with budget." Levels are granted in `core/permissions/permissions.config.yaml` and raised only after an action-type meets reliability criteria (see §6).

## 2. Risk classification of every action

Each action is scored on two axes; the higher axis wins.

**Reversibility**
- `reversible` — trivially undone (draft, internal note, task creation).
- `recoverable` — undoable with effort/cost (send internal message, reschedule).
- `irreversible` — cannot be undone (money sent, email to customer, data deleted, contract signed, employee notified).

**Impact / magnitude**
- `low` — no external party, no money, no commitment.
- `medium` — external-facing or small money within a set threshold.
- `high` — money above threshold, legal/regulatory, employment, or brand-critical.

```
risk_tier = f(reversibility, impact)

              impact:  low        medium       high
reversible            LOW         LOW          MEDIUM
recoverable           LOW         MEDIUM       HIGH
irreversible          MEDIUM      HIGH         CRITICAL
```

## 3. The decision matrix (risk × autonomy)

```
IF risk_tier == LOW        AND level >= L2  → auto-execute, log
IF risk_tier == MEDIUM     AND level >= L3  → auto-execute within limits, notify, log
IF risk_tier == HIGH                        → require approval (never auto), log
IF risk_tier == CRITICAL                    → require approval + explicit confirmation + audit, log
ELSE (level too low for tier)               → prepare only (L1 draft) and request approval
```

No configuration can auto-execute a `CRITICAL` action. High/critical always route to a human.

## 4. Actions that ALWAYS require human approval

Regardless of autonomy level (mirrors the platform safety rules and the source's own "get a professional" guidance):

- Moving money: payments, transfers, payroll runs, refunds above threshold, investments.
- Signing or agreeing to contracts, terms, or legal commitments.
- Hiring, firing, disciplinary action, compensation changes, or anything touching a specific employee's status.
- Filing taxes or regulatory submissions.
- Sending external communications that commit the company (offers, legal notices, price changes to customers).
- Changing standing configuration: bank connections, auto-pay rules, access permissions, data-retention/deletion policies.
- Deleting or overwriting business records.
- Any action the relevant skill's **Human Approval Requirements** section names.

## 5. Actions AI can own (at L2–L3, reversible/low-risk)

Analysis, monitoring, drafting, research, calculations, scenario modeling, creating internal tasks, preparing plans and documents, assembling reports and briefings, anomaly detection, and low-risk reversible execution (e.g. drafting a reply for approval, updating an internal dashboard, scheduling an internal reminder).

## 6. Earning higher autonomy

An action-type is eligible for promotion (e.g. L1→L2) only when all hold:

```
IF   executions_observed        >= N_min (per policy, e.g. 20)
AND  human_override_rate        <  5%
AND  error_or_reversal_rate     <  2%
AND  rollback_mechanism         exists and is tested
AND  monitoring_coverage        == full for this action-type
THEN action-type is eligible for promotion (founder confirms the promotion)
```

Promotion is always confirmed by the founder. Demotion is automatic: any incident (reversal, complaint, threshold breach caused by an auto-action) drops the action-type one level and flags it for review.

## 7. Escalation ladder

When an agent hits its limits, it escalates rather than guesses:

| Trigger | Escalate to |
|---|---|
| Action risk exceeds granted autonomy | Founder (approval) |
| Financial decision above threshold / cash risk | Founder + (recommend) accountant |
| Tax, entity, or regulatory question | Accountant / tax professional |
| Contract terms, IP, liability, disputes, termination | Attorney |
| Employee-specific / protected-class / performance action | HR professional / attorney |
| Strategic or irreversible bet | Founder (+ executive/advisor) |
| Data conflict or low confidence in inputs | Founder (surface uncertainty, do not act) |
| Ethical judgment / values call | Founder |

Escalation messages must include: the situation, what the agent knows, its confidence, the specific decision needed, and the recommended option with rationale.

## 8. Approval request format

Every approval request presented to the founder contains:

```yaml
approval_request:
  what: "One-line description of the action"
  why: "The diagnosis / reason this action is proposed"
  risk_tier: LOW | MEDIUM | HIGH | CRITICAL
  reversibility: reversible | recoverable | irreversible
  cost_or_exposure: "$ amount or scope"
  expected_outcome: "What should happen if approved"
  alternatives: ["option B", "do nothing → consequence"]
  recommendation: "The agent's recommended choice + confidence %"
  rollback: "How this can be undone, or 'irreversible'"
  expires: "When this decision must be made by"
```

## 9. Audit & logging

Every action — proposed, approved, executed, or rejected — writes an immutable audit record:

```yaml
audit_entry:
  timestamp, agent, skill, action, inputs_ref, twin_state_ref
  risk_tier, autonomy_level_used, approval: {required, by, at} | auto
  result, reversible, rollback_ref
  linked_decision_record   # ties action to the decision that authorized it
```

Audit records link to decision records in Business Memory so the Learning layer can later compare expected vs. actual outcomes of each authorized action.

## 10. Relationship to skills

Every Skill declares its own `Human Approval Requirements`, `Escalation Conditions`, and `Guardrails`. This document is the *system-wide* policy those per-skill declarations must comply with; where a skill is stricter, the skill wins. Policy source lives in `policies/` and `core/permissions/`.
