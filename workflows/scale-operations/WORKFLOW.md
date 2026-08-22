---
name: scale-operations
lead_agent: operations-agent
collaborators: [people-agent, cfo-agent]
triggers: ["can't scale", "delivery too slow", "too many mistakes", "document this process", "automate this"]
---

# Workflow: scale-operations

Make delivery reliable, efficient, and able to grow.

## 1. Understand
Retrieve: the process(es) in question; volume/demand trend; cycle times; defect/rework rate; capacity & utilization; tools; who owns what; customer SLAs.

## 2. Diagnose
`operational-audit` (surface constraints) → `bottleneck-analysis` (find the throughput ceiling & strain point) → `process-mapping` where the process is undocumented.
```
IF a single step caps throughput      → bottleneck   → relieve/redesign that step
IF defects/rework high                → quality      → process-optimization
IF capacity maxed                     → capacity     → hiring-plan-builder / automation-triage
IF process undocumented/tribal        → knowledge    → sop-writer
```

## 3. Plan
Prioritized fixes with expected impact (cycle time↓, throughput↑, defects↓) and effort/cost. `process-optimization` for redesign; `automation-triage` to route each step (automate/document/delegate/outsource/keep-manual); `technology-evaluation` if tooling is the lever.

## 4. Execute (risk-tiered)
- Auto (L1–L2): process maps, SOP drafts, internal task assignments, dashboards.
- Approval: tool purchases, vendor commitments, process changes affecting customers.

## 5. Monitor
Cycle time, throughput, on-time delivery, defect/rework rate, capacity utilization.

## 6. Adapt
Compare post-change metrics to expected; iterate on the next constraint (the bottleneck moves once relieved).

## Guardrails
Tool spend and customer-affecting changes require founder approval. Automation of steps requiring judgment/relationship is flagged, not auto-adopted.
