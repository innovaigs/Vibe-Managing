# MANIFEST — Vibe Managing

The complete map of the Vibe Managing Business Intelligence system: an AI-native business operating system that turns **founder intent → business execution**. This manifest indexes every part and every deliverable.

## What this is
A library of **skills** (discrete AI capabilities), composed by **agents** (specialized workers), orchestrated by **workflows**, governed by a **control plane**, and grounded in **business memory** + a **business digital twin** — all vendor-neutral and installable into AI coding/agent runtimes.

The business intelligence was extracted from real small-business management practice and rewritten as operational intelligence for AI execution. It carries no source-program branding (see `internal/PROVENANCE_MAP.md`).

## Deliverables index

| # | Deliverable | Location |
|---|---|---|
| 1 | Source inventory | [SOURCE_AUDIT.md](SOURCE_AUDIT.md) |
| 2 | Extracted business knowledge | [KNOWLEDGE_MAP.md](KNOWLEDGE_MAP.md) |
| 3 | System architecture | [VIBE_MANAGING_ARCHITECTURE.md](VIBE_MANAGING_ARCHITECTURE.md) |
| 4 | Skill registry | [SKILL_REGISTRY.md](SKILL_REGISTRY.md) |
| 5 | Agent registry | [AGENT_REGISTRY.md](AGENT_REGISTRY.md) |
| 6 | Workflow registry | [WORKFLOW_REGISTRY.md](WORKFLOW_REGISTRY.md) |
| 7 | Intent library | [INTENT_LIBRARY.md](INTENT_LIBRARY.md) |
| 8 | Business memory schema | [BUSINESS_MEMORY_SCHEMA.md](BUSINESS_MEMORY_SCHEMA.md) |
| 9 | Business digital twin | [BUSINESS_DIGITAL_TWIN.md](BUSINESS_DIGITAL_TWIN.md) |
| 10 | Autonomy & approval model | [AUTONOMY_AND_APPROVAL_MODEL.md](AUTONOMY_AND_APPROVAL_MODEL.md) |
| 11 | Integration architecture | [INTEGRATION_ARCHITECTURE.md](INTEGRATION_ARCHITECTURE.md) |
| 12 | Business health engine | [BUSINESS_HEALTH_ENGINE.md](BUSINESS_HEALTH_ENGINE.md) |
| 13 | Operating cadence | [OPERATING_CADENCE.md](OPERATING_CADENCE.md) |
| 14 | Skill folders | [skills/](skills/) |
| 15 | Agent folders | [agents/](agents/) |
| 16 | Evaluation suite | [evaluations/](evaluations/) |
| 17 | Master orchestrator | [MASTER_ORCHESTRATOR.md](MASTER_ORCHESTRATOR.md) |
| 18 | Human-judgment boundary | [policies/HUMAN_JUDGMENT_BOUNDARY.md](policies/HUMAN_JUDGMENT_BOUNDARY.md) |
| 19 | Provenance map (internal) | [internal/PROVENANCE_MAP.md](internal/PROVENANCE_MAP.md) |

## Repository layout
```
vibe-managing/
├── README.md · MANIFEST.md · VIBE_MANAGING_ARCHITECTURE.md
├── SOURCE_AUDIT.md · KNOWLEDGE_MAP.md
├── SKILL_REGISTRY.md · AGENT_REGISTRY.md · WORKFLOW_REGISTRY.md · INTENT_LIBRARY.md
├── BUSINESS_MEMORY_SCHEMA.md · BUSINESS_DIGITAL_TWIN.md · MASTER_ORCHESTRATOR.md
├── AUTONOMY_AND_APPROVAL_MODEL.md · INTEGRATION_ARCHITECTURE.md
├── BUSINESS_HEALTH_ENGINE.md · OPERATING_CADENCE.md
├── core/          # orchestrator, memory, twin, permissions, approvals, monitoring, learning, cadence
├── skills/        # 10 domains + template; each skill = a full SKILL.md
├── agents/        # 11 specialized agents (agent.yaml + AGENT.md)
├── workflows/     # end-to-end orchestrations
├── intents/       # intent library assets
├── schemas/       # JSON Schemas: skill, agent, memory, twin, decision, integration, health
├── integrations/  # connector category specs
├── plugins/       # packaging for coding agents + manifest.json
├── prompts/       # reusable system prompts
├── policies/      # guardrails + human-judgment boundary
├── evaluations/   # scenario test suite
├── examples/      # worked end-to-end traces
└── internal/      # provenance map (not user-facing)
```

## How to use it (for a coding agent)
1. Read this MANIFEST and `VIBE_MANAGING_ARCHITECTURE.md`.
2. Load skills from `skills/` (validate with `schemas/skill.schema.json`).
3. Load agents from `agents/` and the control plane from `core/permissions/` + `policies/`.
4. Bind `integrations/` categories to the company's real tools.
5. Drive it through `MASTER_ORCHESTRATOR.md`: founder intent → understanding → diagnosis → planning → execution → monitoring → learning.
6. Test against `evaluations/`.

## Machine-readable index
`plugins/manifest.json` enumerates all skills, agents, schemas, and required integration scopes.
