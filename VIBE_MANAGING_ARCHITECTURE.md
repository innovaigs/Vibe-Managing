# VIBE_MANAGING_ARCHITECTURE

**Deliverable 3 — Complete system architecture.**

Vibe Managing is an AI-native business operating system. A founder expresses intent in natural language; the system understands the business, diagnoses the situation, plans, executes what it is authorized to execute, coordinates specialized agents and tools, asks for approval where required, monitors results, and learns.

```
Founder Intent  ─▶  Adaptation  ─▶  Understanding  ─▶  Diagnosis  ─▶  Planning  ─▶  Execution  ─▶  Monitoring  ─▶  Learning
      ▲                                                                                                │
      └────────────────────────────  next-best-action recommendations  ◀───────────────────────────┘
```

The intelligence that fills these layers is extracted from real small-business management practice and encoded as **Skills** (discrete capabilities), composed by **Agents** (specialized workers), orchestrated by **Workflows**, governed by a **Control Plane**, and grounded in **Business Memory** + a **Business Digital Twin**.

---

## The seven layers

### Layer 0 — Business Adaptation
The system first configures itself for the actual company: business archetype, industry and subindustry, business model(s), lifecycle stage, functional maturity, geography, regulatory intensity, ownership, strategy, and risk appetite. It composes multiple profiles for mixed businesses and records verified local overrides. Baseline profiles are never treated as company facts. See `UNIVERSAL_BUSINESS_ADAPTATION.md`.

### Layer 1 — Business Understanding
The system maintains a live, structured model of the company so agents reason about *this* business, not businesses in general.

- **Backed by:** `core/business-memory/` (persistent facts) + `core/digital-twin/` (live operational model).
- **Knows:** company, founder, business model, customers, products, revenue, costs, team, resources, goals, constraints, competitors, market, current performance.
- **Populated by:** integrations (Layer 4 tools reading external systems) + founder intake + agent analysis.

### Layer 2 — Diagnostics
The system determines what is working, what is wrong, and why.

- **Backed by:** the diagnostic Skills (e.g. Business Health Diagnostic, Cash Flow Diagnostic, Growth Constraint Diagnostic) and `core/monitoring/` (Business Health Engine).
- **Produces:** ranked findings with severity (`Healthy / Needs Attention / At Risk / Critical`), root-cause hypotheses, and evidence from the twin.

### Layer 3 — Planning
Diagnosis becomes strategy, priorities, objectives, plans, milestones, budgets, forecasts, and function-specific plans (hiring, GTM, operations).

- **Backed by:** planning Skills (Strategic Planning, Growth Plan Builder, Hiring Plan Builder, Budget Builder, GTM Plan Builder).
- **Produces:** a structured plan object with initiatives, expected impact, owners, timeline, budget, and KPIs — written to memory as a decision record.

### Layer 4 — Execution
The system uses tools and specialized agents to act: create, communicate, research, update systems, assign work, monitor projects, and automate operations.

- **Backed by:** `integrations/` (MCP/API connectors) + agents + the approval system.
- **Governed by:** the autonomy model — every action is risk-classified and either auto-executed, executed-with-notice, or held for approval.

### Layer 5 — Monitoring
Continuous watch over revenue, cash, margin, customers, pipeline, marketing, team, operations, delivery, risk, and strategic progress.

- **Backed by:** `core/monitoring/` (Business Health Engine) + `core/cadence/` (operating cadence).
- **Produces:** alerts, threshold breaches, anomalies, and cadence briefings (daily/weekly/monthly/quarterly).

### Layer 6 — Learning
The system compares expected vs. actual outcomes, diagnoses variance, updates assumptions, and improves future decisions.

- **Backed by:** `core/learning/` + the decision-record store in business memory.
- **Method:** the forecast-vs-actual review loop (extracted from real monthly-review practice) generalized to every plan and initiative.

---

## Component map

```
vibe-managing/
├── core/
│   ├── orchestrator/     Layer 0: intent → layers 1–6 (MASTER_ORCHESTRATOR)
│   ├── business-memory/  Layer 1: persistent company facts (schema + policies)
│   ├── digital-twin/     Layer 1: live operational model (objects, relations, events)
│   ├── permissions/      Control plane: roles, scopes, autonomy levels
│   ├── approvals/        Control plane: approval routing + audit
│   ├── monitoring/       Layer 5: Business Health Engine (indicators, thresholds)
│   ├── learning/         Layer 6: variance diagnosis + assumption updates
│   └── cadence/          Layer 5/6: daily/weekly/monthly/quarterly/annual loops
│
├── skills/               160 discrete AI capabilities across 22 domains
│   ├── strategy/ finance/ growth/ sales/ marketing/ operations/
│   ├── people/ leadership/ risk/ legal/ product/ customer-success/
│   ├── supply-chain/ technology/ data-analytics/ security-privacy/
│   └── quality/ projects-programs/ governance/ international/ sustainability/ adaptation/
│
├── agents/               Specialized workers that compose skills over time
├── workflows/            End-to-end orchestrations for major founder intents
├── intents/              Natural-language intent library → capability routing
├── schemas/              JSON schemas for memory, twin, skill I/O, decisions
├── integrations/         Integration categories: read/write/risk/approval/audit
├── plugins/              Packaging for coding agents (Claude Code, Codex, Cursor, …)
├── prompts/              Reusable system/role prompts for agents & skills
├── policies/             Guardrails: financial, legal, employment, privacy, ethics
├── evaluations/          Scenario tests for every core capability
├── examples/             Worked end-to-end examples
├── docs/                 Registries & specs (also mirrored as root deliverables)
└── internal/             Provenance map (source traceability; not user-facing)
```

## How a request flows (summary)

1. Founder states intent (natural language).
2. **Orchestrator** classifies intent and composes the company's adaptation context.
3. It loads required context from **memory + twin** and detects missing information.
3. Orchestrator invokes the relevant **diagnostic skills** and **agents**.
4. Agents form hypotheses and validate them against business data.
5. A **plan** is produced with risk-classified actions.
6. The **control plane** auto-executes low-risk reversible actions and routes the rest for **approval**.
7. **Monitoring** tracks leading indicators; the **learning** layer compares expected vs. actual and adapts.
8. Outcomes and lessons are written back to **memory**.

Detailed specs for each component live in their respective deliverables:
`MASTER_ORCHESTRATOR.md`, `BUSINESS_MEMORY_SCHEMA.md`, `BUSINESS_DIGITAL_TWIN.md`,
`AUTONOMY_AND_APPROVAL_MODEL.md`, `BUSINESS_HEALTH_ENGINE.md`, `OPERATING_CADENCE.md`,
`INTEGRATION_ARCHITECTURE.md`, `SKILL_REGISTRY.md`, `AGENT_REGISTRY.md`,
`WORKFLOW_REGISTRY.md`, `INTENT_LIBRARY.md`.

## Design principles

- **Adapt before advising.** Industry and business-model profiles configure decisions, but verified local evidence always wins.
- **Skills are the atom.** Everything an agent does resolves to a skill call with typed inputs and outputs. Skills are modular, self-contained, deterministic where possible, and independently testable.
- **Optimize the enterprise.** No function may improve its metric by exporting unacceptable cost or harm to cash, customers, workers, suppliers, quality, safety, security, society, or future capability.
- **The twin is the single source of truth** agents reason over — not raw dashboards.
- **Autonomy is earned, not assumed.** Actions default to the lowest autonomy that gets the job done; higher autonomy is unlocked per action-type as reliability is proven.
- **Human judgment is a first-class boundary,** not an afterthought — encoded in every skill's escalation and approval sections.
- **Vendor-neutral.** Capabilities are expressed as Markdown + schemas usable by any coding/agent runtime; integrations are pluggable.
