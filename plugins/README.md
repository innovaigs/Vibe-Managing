# plugins/ — Packaging for coding agents

Vibe Managing is vendor-neutral. The same skills, agents, and workflows can be installed into any AI coding/agent runtime — Claude Code, OpenAI Codex, Cursor, Windsurf, VS Code agents, and others — because everything ships as Markdown + JSON Schema + YAML, not provider-specific code.

## What a runtime loads
- **Skills** (`skills/<domain>/<name>/SKILL.md`) — each is a self-contained capability with typed inputs/outputs (`schemas/skill.schema.json`). Load as tools or prompt modules.
- **Agents** (`agents/<name>/agent.yaml` + `AGENT.md`) — specialized workers that compose skills (`schemas/agent.schema.json`).
- **Workflows** (`workflows/<name>/WORKFLOW.md`) — end-to-end orchestrations.
- **Core** (`core/`) — orchestrator, memory, twin, permissions, approvals, monitoring, learning, cadence.
- **Policies** (`policies/`) — guardrails enforced across everything.

## Install patterns
| Runtime | How to load |
|---|---|
| Claude Code | Point the agent at this repo; skills become callable capabilities. `manifest.json` lists them + required integration scopes. |
| Codex / Cursor / Windsurf / VS Code agents | Load `SKILL.md` files as prompt/tool modules; use `schemas/*.json` to validate I/O. |
| Any MCP host | Map `integrations/` categories to MCP servers; skills call them through the connector contract (`schemas/integration.schema.json`). |

## Integration binding
Skills never hard-code a provider. A skill that needs financial data declares it reads the `finance` integration category; the runtime binds that to whatever connector is configured (a bookkeeping tool via MCP, a bank API, a spreadsheet). Swapping providers means swapping a connector, not touching skills.

## Permissions
`manifest.json` enumerates the integration categories and scopes each installed skill/agent needs, so a runtime requests **least-privilege** access and the founder approves only what's in play. The control plane (`core/permissions/`, `core/approvals/`) governs execution regardless of runtime.

See `manifest.json` for the machine-readable package index.
