# intents/ — Natural-language intent routing

Founders speak in plain language. The Orchestrator classifies any phrasing into an intent, then routes it to skills, agents, and a workflow. The full catalog with phrasings and mappings is [INTENT_LIBRARY.md](../INTENT_LIBRARY.md); `intents.yaml` here is the machine-readable routing table.

Routing shape: `intent → diagnostic → skills → agent(s) → workflow → approval → monitoring`.

Rules: ambiguous → one clarifying question; multi-domain → fan out + CFO reconciles against cash; any action → risk-tiered (irreversible/financial/legal/employment always need approval); any metric → attach monitoring; unknown → run `business-health-diagnostic` and propose the best-fit workflow.
