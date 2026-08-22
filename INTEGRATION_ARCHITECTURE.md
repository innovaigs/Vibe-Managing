# INTEGRATION_ARCHITECTURE

**Deliverable 11 — Plugin / MCP / API architecture.**

Vibe Managing is vendor-neutral. Capabilities are expressed as Markdown + schemas that any agent runtime can load (Claude Code, Codex, Cursor, Windsurf, VS Code agents, and others). To *act on* a real business, agents connect to that business's tools through a uniform connector layer — MCP servers, native APIs, or plugins — behind a single internal contract.

Home: `integrations/` (category specs) and `plugins/` (runtime packaging).

---

## Connector contract

Every integration, whatever the provider, is described by one spec so agents treat them uniformly:

```yaml
integration:
  id: str
  category: enum(finance, crm_sales, marketing, people, operations, comms, data, documents)
  provider: str                     # e.g. a bookkeeping tool, a CRM, an ad platform
  transport: enum(mcp, rest_api, oauth_api, file, webhook)
  auth: {type, scopes_requested, credentials_ref}   # secrets by reference only
  reads:  [ {entity, fields, freshness} ]           # what agents may READ
  writes: [ {entity, fields, risk_tier, approval} ] # what agents may WRITE
  high_risk_actions: [ {action, risk_tier, approval, rollback} ]
  rate_limits, audit: required, rollback: {supported, method}
  maps_to_memory: [ memory_namespace ]              # where synced data lands
  maps_to_twin:   [ twin_object ]                   # which twin objects it updates
```

**Universal rules for every connector:**
- **Secrets by reference.** Credentials/tokens are never stored in memory or the twin in plaintext.
- **Reads are cheap; writes are governed.** Every write is risk-tiered and passes through the autonomy/approval control plane.
- **Everything is audited.** Every read-sync and every write produces an audit entry.
- **Rollback declared.** A connector must state whether each write is reversible and how.
- **Least privilege.** Only the scopes a granted skill needs are requested.

---

## Integration categories

For each category: what agents **READ**, what they may **WRITE**, **high-risk** actions, and **approval** posture.

### 1. Finance (bookkeeping, banking, payments, billing)
- **READ:** transactions, invoices, bills, balances, P&L, balance sheet, cash position, AR/AP aging, payroll totals.
- **WRITE (governed):** draft invoices, categorize transactions, create draft bills, tag expenses.
- **HIGH-RISK (always approval):** send money, pay a bill, run payroll, issue refunds above threshold, change bank/auto-pay connections.
- **Feeds:** `finance.*` memory; `CashAccount / RevenueStream / CostItem` twin objects. This is the primary source for the Business Health Engine's cash/liquidity indicators.

### 2. CRM / Sales
- **READ:** contacts, accounts, deals, stages, pipeline value, activities, win/loss.
- **WRITE (governed):** create/update contacts, log activities, create tasks, move internal deal stages, draft follow-ups.
- **HIGH-RISK (approval):** send external customer emails/quotes, commit pricing, delete records.
- **Feeds:** `customers`, `strategy` memory; `Pipeline / Deal / Customer` twin objects.

### 3. Marketing (ads, email, analytics, social)
- **READ:** spend, impressions, clicks, conversions, CAC, ROAS, traffic, list size, campaign performance.
- **WRITE (governed):** draft campaigns/content, schedule internal-review posts, build audiences.
- **HIGH-RISK (approval):** launch paid campaigns / commit ad budget, publish public content, send email blasts.
- **Feeds:** `market`, `metrics`; `Campaign / Channel` twin objects.

### 4. People (HRIS, payroll, recruiting, scheduling)
- **READ:** roster, roles, org structure, comp totals (restricted), time-off, open reqs, candidate pipeline.
- **WRITE (governed):** draft job descriptions, draft offers, schedule interviews, create onboarding tasks.
- **HIGH-RISK (always approval + HR/legal escalation):** hire, terminate, change compensation, disciplinary records.
- **Feeds:** `team` (restricted) memory; `Employee / Role` twin objects.

### 5. Operations (project mgmt, ticketing, help desk, ERP, inventory)
- **READ:** tasks, tickets, SLAs, cycle times, backlog, inventory levels, delivery status.
- **WRITE (governed):** create/assign tasks, update statuses, draft SOPs, flag bottlenecks.
- **HIGH-RISK (approval):** customer-facing ticket responses, purchase orders, inventory writeoffs.
- **Feeds:** `operations`; `Process / Tool / Vendor` twin objects. Primary source for capacity/bottleneck views.

### 6. Communications (email, chat)
- **READ:** relevant threads/metadata (scoped, privacy-tiered).
- **WRITE (governed):** draft replies, draft internal messages.
- **HIGH-RISK (approval):** send any external message, send on the founder's behalf.
- **Feeds:** context for many skills; never bulk-harvested — scoped to the task.

### 7. Data (spreadsheets, databases, warehouses, BI)
- **READ:** structured datasets, query results, existing reports.
- **WRITE (governed):** write computed metrics, create/update dashboards, append analysis tables.
- **HIGH-RISK (approval):** schema changes, deletes, overwrites of source tables.
- **Feeds:** `metrics`; cross-checks many twin views.

### 8. Documents (drive, office suite, notes/wiki)
- **READ:** business documents, contracts, plans, policies.
- **WRITE (governed):** create/update internal docs, draft plans and reports.
- **HIGH-RISK (approval):** share externally, delete, overwrite finalized documents.
- **Feeds:** `company`, `strategy`, `operations` context.

---

## Sync model

- **Pull-on-demand** for expensive/rare reads (a valuation multiple lookup).
- **Scheduled sync** for core operational data (daily finance/CRM/ops pulls feeding the cadence).
- **Webhook/event** where the provider supports it (a payment lands → immediate twin event).

All synced data carries provenance (`source`, `as_of`, `confidence`) into memory.

## Failure & trust handling

- A connector in `error` state marks its downstream memory/twin data **stale**; agents must flag staleness before acting.
- Conflicting values across connectors are surfaced for reconciliation, not silently merged.
- Rate-limit/backoff and partial-sync detection are required; a partial sync never masquerades as complete.

## Packaging for coding agents (`plugins/`)

The same capabilities are packaged so a coding/agent runtime can install them:

- **Skills** ship as self-contained folders (Markdown + schema) — loadable as tools/prompts.
- **Integration specs** map to MCP servers where available; otherwise to REST/OAuth adapters.
- A manifest (`plugins/manifest.json`) lists skills, agents, required integration categories, and required scopes so a runtime can present them and request only the permissions in play.
- Nothing is provider-locked: swapping (say) one CRM for another means swapping a connector spec, not rewriting skills.

See `plugins/` for the manifest and adapter notes, and `schemas/integration.schema.json` for the machine-readable connector contract.
