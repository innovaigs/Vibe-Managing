# PROVENANCE_MAP (internal)

**Deliverable 19 — provenance tracking.** Internal engineering artifact. Not user-facing. This maps every Vibe Managing capability back to where its knowledge originated, so source-grounded intelligence is never confused with model-added reasoning, and so no source-program branding leaks into shipped assets.

## Tags
- **SOURCE-DERIVED** — directly grounded in the studied source material (a framework, formula, worksheet, or decision logic that existed there, rewritten into original operational language).
- **SYNTHESIZED** — source concepts recombined or extended into a new operational capability.
- **CLAUDE-DERIVED** — added from model reasoning to fill a capability a running business needs that the source only implied or omitted. Clearly the smallest slice.

## De-branding rule (applied to ALL shipped assets)
None of the following ever appear in any file outside `internal/` and the git-ignored `10kgsb/` source folder: the source program's name or acronym, its sponsoring institution/college, instructor/panelist/participant names, cohort identifiers, or vendor tool brand names (a forecasting/planning tool, a valuation-multiples data provider, etc.). Vendor tools are generalized to their function. Example companies/counterparties from the source are anonymized.

## Domain → source unit → transformed capability

| Vibe Managing capability | Provenance | Originating source domain |
|---|---|---|
| strategy: opportunity-feasibility-analysis, idea-expansion, growth-pathway-classifier, growth-lever-selector, resource-gap-analysis, competitive-intelligence-analysis, exit-readiness-analysis, social-value-designer | SOURCE | Opportunity & growth-models unit |
| strategy: strategic-planning, initiative-prioritization, business-health-diagnostic | SYNTH | Assembled across units |
| risk: risk-diagnostic, crisis-response-planning | SOURCE | Risk/uncertainty & crisis material |
| risk: business-continuity-plan | SYNTH | Concentration/continuity implied by risk + growth |
| finance: financial-statement-analysis, financial-ratio-analysis, cash-flow-diagnostic, cash-runway-monitor, working-capital-optimizer, financial-forecast-builder, scenario-and-sensitivity-analysis, break-even-and-pricing-analysis, debt-service-and-covenant-analysis | SOURCE | Financial statements/ratios + forecasting/cash units |
| finance: budget-builder | SYNTH | Forecast + goals |
| finance: business-valuation, value-driver-analysis, financing-options-analysis, bankability-assessment | SOURCE (bankability numeric thresholds & 5 C's = CLAUDE) | Valuation & money unit |
| growth: growth-plan-builder, kpi-design, executive-dashboard-builder, monthly-business-review, variance-diagnosis, growth-pitch-generator | SOURCE | Growth plan + forecast-vs-actual review |
| marketing: market-segmentation, customer-persona-builder, buying-center-mapper, buyers-journey-mapper, customer-value-proposition-builder, marketing-funnel-planner, channel-selection, website-conversion-audit, keyword-and-search-map, social-content-planner, competitive-advantage-assessment, marketing-strategy-builder | SOURCE | Marketing & customer + digital-marketing units |
| marketing: marketing-metrics-tracker (CAC/LTV/ROAS pieces) | CLAUDE within SOURCE | Digital-marketing (funnel) + added metrics |
| sales: negotiation-preparation | SOURCE | Negotiation unit |
| sales: sales-process-design | CLAUDE | Gap-fill on buyer's journey/funnel |
| sales: pipeline-and-forecast-review, proposal-builder | SYNTH | Funnel + CVP + added forecasting mechanics |
| operations: operational-audit, process-mapping, bottleneck-analysis, sop-writer, process-optimization, automation-triage, technology-evaluation | SOURCE (ops formulas mostly SYNTH) | Operations unit |
| people: job-description-builder, interview-guide-and-scorecard, hiring-scorecard-and-fit, delegation-planner, founder-capacity-diagnostic, organizational-design, onboarding-builder, hr-process-coverage-audit | SOURCE | People & org unit |
| people: hiring-plan-builder, culture-diagnostic | SYNTH | Capacity + org + financials |
| leadership: leadership-style-assessment, delegation-readiness-audit, motivation-mapper, mission-vision-builder, leadership-growth-planner | SOURCE | Leadership unit (style model reconstructed from deck; assessment scoring reconstructed) |
| legal: contract-review-triage, employment-compliance-scan, ip-protection-audit, legal-escalation-router | SOURCE | Legal unit (employment-law heavy) |
| legal: entity-structure-advisor | CLAUDE | Baseline gap-fill; entity content thin in source |

## System architecture provenance
The six-layer architecture, orchestrator, digital twin, business memory schema, autonomy/approval model, integration architecture, health engine, cadence, plugin packaging, and evaluation suite are **CLAUDE-DERIVED system design** that operationalizes the SOURCE-DERIVED business intelligence. The business *knowledge* they carry (metrics, thresholds, frameworks, decision logic) is SOURCE/SYNTH as tagged above.

## Known reconstructions / caveats
- The leadership-style calculator's exact item wording was not recoverable from the source spreadsheet (extraction stub); its two-dimension four-quadrant scoring logic was reconstructed from the leadership deck. Tagged accordingly in the skill.
- Several forecasting spreadsheets did not extract cleanly; their driver→output structure was reconstructed from the forecasting exercise narratives and the statements/ratios material. Numbers in examples are illustrative, not from source.
- Bankability numeric thresholds (DSCR bands, equity %) and the 5 C's framing are CLAUDE-DERIVED industry-standard additions layered on the source's "being bankable" concept.

Per-block provenance tags live inside each domain knowledge extract and each `SKILL.md`'s Provenance section.
