# integrations/ — Connector category specs

Vibe Managing connects to a company's real tools through a uniform connector contract (`schemas/integration.schema.json`), so agents treat every provider the same way and the control plane governs every write. Full design in `INTEGRATION_ARCHITECTURE.md`.

## Categories
`finance` · `crm_sales` · `marketing` · `people` · `operations` · `comms` · `data` · `documents`

Each `<category>.yaml` here declares, generically (provider-neutral): what agents may **read**, what they may **write**, which actions are **high-risk** (always approval), audit + rollback requirements, and which memory namespaces / twin objects the data maps to. Bind a category to a concrete provider (via MCP, REST, or OAuth) at install time — see `plugins/`.

## Universal rules
- Secrets by reference only (never plaintext in memory or the twin).
- Reads are cheap; every write is risk-tiered and passes through `core/permissions/` + `core/approvals/`.
- Everything is audited; every write declares its rollback.
- Least privilege: only the scopes an installed skill needs are requested.

## Files
- `finance.yaml`, `crm_sales.yaml`, `marketing.yaml`, `people.yaml`, `operations.yaml`, `comms.yaml`, `data.yaml`, `documents.yaml` — one per category. All eight are specified as YAML files here; `finance.yaml` and `crm_sales.yaml` are the most detailed reference examples. Full design rationale in `INTEGRATION_ARCHITECTURE.md`.
