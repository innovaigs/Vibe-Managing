# core/ — Vibe Managing runtime

The engine that turns founder intent into governed business execution. Each component has a detailed specification at the repo root; this folder holds the runtime configs and integration points.

| Component | Folder | Spec | Config |
|---|---|---|---|
| Orchestrator | `orchestrator/` | `MASTER_ORCHESTRATOR.md` | — |
| Business Memory | `business-memory/` | `BUSINESS_MEMORY_SCHEMA.md` | `schemas/business-memory.schema.json` |
| Digital Twin | `digital-twin/` | `BUSINESS_DIGITAL_TWIN.md` | `schemas/digital-twin.schema.json` |
| Permissions | `permissions/` | `AUTONOMY_AND_APPROVAL_MODEL.md` | `permissions/permissions.config.yaml` |
| Approvals | `approvals/` | `AUTONOMY_AND_APPROVAL_MODEL.md` | — |
| Monitoring | `monitoring/` | `BUSINESS_HEALTH_ENGINE.md` | `monitoring/thresholds.config.yaml` |
| Learning | `learning/` | `MASTER_ORCHESTRATOR.md` §closing loop + `BUSINESS_MEMORY_SCHEMA.md` §decisions | — |
| Cadence | `cadence/` | `OPERATING_CADENCE.md` | `cadence/cadence.config.yaml` |

## Flow
```
intent → orchestrator → (memory + twin) → skills/agents → permissions/approvals → execution → monitoring → learning → memory
```

The runtime is deliberately storage- and vendor-neutral: components are specifications + configs that any agent runtime (Claude Code, Codex, Cursor, …) can implement against. See `plugins/` for packaging.
