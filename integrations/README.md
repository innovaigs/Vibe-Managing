# integrations/ — Connector category specs

Vibe Managing connects to a company's real tools through a uniform connector contract (`schemas/integration.schema.json`), so agents treat every provider the same way and the control plane governs every write. Full design in `INTEGRATION_ARCHITECTURE.md`.

## Categories
`finance` · `crm_sales` · `marketing` · `people` · `operations` · `comms` · `data` · `documents` · `product_customer` · `supply_chain` · `technology_security` · `quality_projects` · `governance_external`

Each `<category>.yaml` here declares, generically (provider-neutral): what agents may **read**, what they may **write**, which actions are **high-risk** (always approval), audit + rollback requirements, and which memory namespaces / twin objects the data maps to. Bind a category to a concrete provider (via MCP, REST, or OAuth) at install time — see `plugins/`.

## Universal rules
- Secrets by reference only (never plaintext in memory or the twin).
- Reads are cheap; every write is risk-tiered and passes through `core/permissions/` + `core/approvals/`.
- Everything is audited; every write declares its rollback.
- Least privilege: only the scopes an installed skill needs are requested.

## Files
- Thirteen provider-neutral category files are included. `finance.yaml` and `crm_sales.yaml` remain the detailed reference examples; advanced categories cover product/customer, supply chain, technology/security, quality/projects, and governance/external operations.
