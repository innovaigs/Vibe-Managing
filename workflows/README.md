# workflows/ — End-to-end orchestrations

A workflow takes a major founder intent all the way from words to coordinated action through six phases: **Understand → Diagnose → Plan → Execute → Monitor → Adapt**. Workflows compose skills and agents; the Orchestrator selects and runs them.

Full catalog and flagship detail: [WORKFLOW_REGISTRY.md](../WORKFLOW_REGISTRY.md).

| Workflow | Folder | Intent |
|---|---|---|
| Grow revenue | `grow-revenue/` | "grow revenue / more customers / sales slowed" |
| Fix cash | `fix-cash/` | "running out of cash / profitable but broke" |
| Should we hire | `should-we-hire/` | "can I afford to hire / what roles next year" |
| Evaluate opportunity | `evaluate-opportunity/` | "should we launch / enter this market" |
| Scale operations | `scale-operations/` | "can't scale / delivery too slow" |
| Reduce spend | `reduce-spend/` | "where's the money going" |
| Raise capital | `raise-capital/` | "we need funding" |
| Manage crisis | `manage-crisis/` | acute disruption |
| Monthly review | `monthly-review/` | period close (the learning loop) |
| Prepare negotiation | `prepare-negotiation/` | upcoming negotiation |

Every workflow obeys the autonomy/approval model: no irreversible action executes without founder approval, and every run ends by writing a decision record and scheduling its learning review. Each `WORKFLOW.md` is a self-contained spec; the registry holds the complete phase-by-phase detail for the flagships.
