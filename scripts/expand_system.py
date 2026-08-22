#!/usr/bin/env python3
"""Generate the advanced, cross-industry Vibe Managing capability layer.

The source-of-truth definitions below are intentionally compact. The generator
expands each definition into a complete SKILL.md, agent specification, workflow,
industry/business-model profile, evaluation, and machine-readable registry.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


DOMAINS = {
    "strategy": ("Strategy", "strategy-agent", "direction, portfolio choices, business model, and competitive advantage", ["goal attainment", "strategic initiative return", "portfolio risk-adjusted value"]),
    "finance": ("Finance", "cfo-agent", "economic viability, liquidity, capital allocation, treasury, and enterprise value", ["free cash flow", "return on invested capital", "cash runway"]),
    "growth": ("Growth", "growth-agent", "repeatable growth systems, experimentation, expansion, and compounding", ["growth rate", "incremental contribution", "experiment learning velocity"]),
    "sales": ("Sales", "sales-agent", "revenue conversion, coverage, commercial design, and deal quality", ["win rate", "quota attainment", "sales cycle"]),
    "marketing": ("Marketing", "marketing-agent", "market creation, brand, demand, lifecycle communication, and channel economics", ["incremental demand", "customer acquisition cost", "brand demand share"]),
    "operations": ("Operations", "operations-agent", "capacity, flow, reliability, service delivery, and multi-site execution", ["on-time delivery", "cycle time", "cost per output"]),
    "people": ("People", "people-agent", "workforce architecture, performance, capability, rewards, and employee experience", ["revenue per FTE", "critical-role coverage", "regrettable attrition"]),
    "leadership": ("Leadership", "leadership-coach-agent", "decision quality, change, succession, executive leverage, and organizational clarity", ["decision cycle time", "change adoption", "leadership bench strength"]),
    "risk": ("Risk", "risk-agent", "enterprise risk, resilience, insurance, fraud prevention, and control effectiveness", ["residual risk", "loss-event frequency", "control effectiveness"]),
    "legal": ("Legal", "legal-liaison-agent", "obligation mapping, contract lifecycle, records, legal escalation, and defensibility", ["material obligation coverage", "contract leakage", "legal issue cycle time"]),
    "product": ("Product", "product-agent", "product discovery, strategy, portfolio, roadmap, economics, and adoption", ["product adoption", "retention", "product contribution margin"]),
    "customer-success": ("Customer Success", "customer-success-agent", "onboarding, value realization, retention, expansion, and customer intelligence", ["net revenue retention", "time to value", "customer health"]),
    "supply-chain": ("Supply Chain", "supply-chain-agent", "demand, sourcing, suppliers, inventory, logistics, and continuity", ["service level", "inventory turns", "perfect-order rate"]),
    "technology": ("Technology", "technology-agent", "architecture, systems portfolio, automation, reliability, cost, and technical leverage", ["availability", "change lead time", "technology cost per outcome"]),
    "data-analytics": ("Data & Analytics", "data-agent", "trusted metrics, data quality, causal reasoning, forecasting, and decision intelligence", ["trusted-data coverage", "decision latency", "forecast accuracy"]),
    "security-privacy": ("Security & Privacy", "security-agent", "security posture, identity, privacy, incident response, and cyber resilience", ["critical exposure time", "access-policy compliance", "incident containment time"]),
    "quality": ("Quality", "quality-agent", "quality systems, process control, root cause, corrective action, and continuous improvement", ["first-pass yield", "defect escape rate", "corrective-action effectiveness"]),
    "projects-programs": ("Projects & Programs", "pmo-agent", "initiative delivery, dependencies, benefits, resources, and portfolio governance", ["benefits realized", "schedule predictability", "portfolio throughput"]),
    "governance": ("Governance", "governance-agent", "decision rights, board effectiveness, policies, accountability, and stakeholder oversight", ["decision-right clarity", "policy compliance", "board action closure"]),
    "international": ("International", "international-agent", "cross-border entry, localization, economics, operations, and jurisdiction risk", ["market contribution", "localization conversion", "cross-border margin"]),
    "sustainability": ("Sustainability", "sustainability-agent", "material impacts, resource efficiency, resilience, and defensible reporting", ["resource intensity", "resilience improvement", "verified impact progress"]),
    "adaptation": ("Business Adaptation", "adaptation-agent", "business archetype, industry, stage, geography, maturity, benchmark, and capability routing", ["recommendation relevance", "context completeness", "outcome confidence"]),
}


SKILLS = {
    "strategy": [
        ("portfolio-strategy", "Portfolio Strategy", "Choose, fund, sequence, pause, or stop the company's portfolio of businesses, products, markets, and initiatives.", "Map strategic bets; estimate risk-adjusted value; test concentration and option value; allocate scarce resources; set review and exit triggers", "portfolio risk-adjusted value; capital concentration; strategic option coverage"),
        ("business-model-design", "Business Model Design", "Design or redesign how value is created, delivered, monetized, and defended.", "Map customer job and value exchange; define revenue and cost mechanics; test unit economics; identify key resources and partners; stress-test defensibility", "contribution margin; recurring revenue share; payback period; model resilience"),
        ("strategic-scenario-planning", "Strategic Scenario Planning", "Prepare decisions that remain robust across plausible market, technology, regulatory, and competitive futures.", "Define focal uncertainty; identify critical forces; build distinct scenarios; test strategy in each; define signposts and contingent moves", "scenario coverage; signpost lead time; contingent-plan readiness"),
    ],
    "finance": [
        ("unit-economics-engine", "Unit Economics Engine", "Model the economics of each customer, order, product, location, project, contract, or capacity unit.", "Select economic unit; allocate direct and avoidable costs; calculate contribution; include acquisition and servicing cost; segment cohorts; find breakpoints", "contribution per unit; LTV:CAC; payback; variable margin"),
        ("capital-allocation", "Capital Allocation", "Allocate cash and capacity among operations, debt, reserves, growth, acquisitions, and owner distributions for maximum risk-adjusted value.", "Establish liquidity floor; normalize cash generation; compare investments on NPV/IRR/strategic fit; price risk and reversibility; sequence commitments", "ROIC; NPV; liquidity headroom; allocation regret"),
        ("treasury-management", "Treasury Management", "Protect liquidity and control cash movement across accounts, entities, currencies, and time horizons.", "Map balances and obligations; forecast daily liquidity; define account and counterparty limits; optimize yield without impairing access; enforce dual control", "liquidity coverage; idle cash; counterparty concentration; unauthorized transactions"),
    ],
    "growth": [
        ("growth-modeling", "Growth Modeling", "Build a quantified growth equation that explains how acquisition, conversion, retention, price, mix, and capacity create growth.", "Decompose revenue; establish baselines; quantify lever elasticity; identify constraint; model interactions; set leading indicators", "growth rate; lever contribution; forecast error; constraint relief"),
        ("experiment-portfolio", "Growth Experiment Portfolio", "Run a balanced portfolio of growth experiments with explicit hypotheses, economics, guardrails, and stopping rules.", "Generate hypotheses; score evidence and upside; design minimum viable tests; allocate test budget; apply sequential stop/scale rules; capture learning", "validated learning per dollar; experiment velocity; scaled-test return"),
        ("expansion-readiness", "Expansion Readiness", "Determine whether the company is ready to expand into a new channel, segment, product, or geography without breaking the core.", "Verify repeatability; test capacity and management bandwidth; model cash and downside; map dependencies; define reversible entry; set kill criteria", "core stability; expansion payback; readiness score; downside exposure"),
    ],
    "sales": [
        ("territory-and-quota-design", "Territory & Quota Design", "Design fair, attainable territories and quotas from market potential, capacity, ramp, and strategy.", "Estimate potential; segment accounts; model rep capacity and ramp; set coverage; assign territories; stress-test fairness and attainability", "quota attainment distribution; territory potential variance; coverage ratio"),
        ("sales-compensation-design", "Sales Compensation Design", "Create incentives that reward profitable, durable revenue without creating harmful selling behavior.", "Define desired behavior; select measures; set pay mix and curve; model edge cases; add quality gates and clawbacks; test cost of sales", "compensation cost of sales; profitable attainment; quality-adjusted bookings"),
        ("enterprise-deal-strategy", "Enterprise Deal Strategy", "Coordinate complex, multi-stakeholder deals while protecting margin, delivery feasibility, risk, and relationship value.", "Map power and process; quantify customer value; build mutual action plan; design commercial boundaries; plan negotiation; validate delivery and legal readiness", "win probability; deal margin; cycle time; implementation risk"),
    ],
    "marketing": [
        ("brand-strategy", "Brand Strategy", "Define the distinctive promise, evidence, memory structures, and experience that create preference and pricing power.", "Research category and audience; define positioning; identify distinctive assets; build proof system; align touchpoints; measure mental and behavioral availability", "branded search; direct demand; preference; price realization"),
        ("lifecycle-marketing", "Lifecycle Marketing", "Coordinate communication across acquisition, onboarding, activation, retention, expansion, and win-back.", "Map lifecycle states; define state transitions; identify friction and triggers; design messages and offers; set suppression rules; measure incremental lift", "activation; retention; expansion; incremental lifecycle revenue"),
        ("marketing-mix-model", "Marketing Mix Model", "Allocate marketing investment across channels using incrementality, saturation, lag, margin, and strategic effects.", "Normalize channel data; separate base demand; estimate incremental response; model lag and saturation; optimize under constraints; validate with experiments", "incremental ROAS; marginal CAC; contribution after marketing"),
    ],
    "operations": [
        ("capacity-planning", "Capacity Planning", "Match demand to people, equipment, space, inventory, and partner capacity at the required service and cost level.", "Forecast demand by unit; translate into workload; identify effective capacity; model variability and queues; choose buffers; plan capacity actions", "utilization; throughput; backlog; service level; cost per unit"),
        ("service-delivery-control", "Service Delivery Control", "Control the complete promise-to-delivery system for consistent scope, quality, time, margin, and customer outcomes.", "Define service promise; map handoffs; create control points; track WIP and exceptions; protect scope and margin; close feedback loop", "on-time delivery; rework; scope leakage; delivery margin"),
        ("multi-location-operations", "Multi-location Operations", "Standardize what must be common while preserving local responsiveness across sites, branches, stores, or franchises.", "Define operating standards; benchmark locations; separate local vs central decisions; manage shared resources; detect drift; replicate winning practices", "same-store performance; location variance; standards compliance; ramp time"),
    ],
    "people": [
        ("workforce-planning", "Workforce Planning", "Translate strategy and demand into the roles, capacity, skills, location, and labor model required over time.", "Model future work; quantify capacity; map capabilities; identify build/buy/borrow/automate options; sequence roles; test affordability", "capacity gap; critical-skill coverage; labor productivity"),
        ("compensation-and-rewards", "Compensation & Rewards", "Design equitable, affordable rewards that attract, motivate, retain, and align people with outcomes.", "Define reward philosophy; benchmark roles; set ranges; assess internal equity; design incentives; model total cost and behavior risk", "range penetration; pay equity; regrettable attrition; incentive efficiency"),
        ("performance-management", "Performance Management", "Create a fair operating system for expectations, feedback, development, accountability, and performance decisions.", "Clarify outcomes and behaviors; calibrate measures; set check-in cadence; separate coaching from consequences; calibrate ratings; document decisions", "goal attainment; feedback timeliness; performance distribution; improvement-plan outcomes"),
    ],
    "leadership": [
        ("executive-decision-system", "Executive Decision System", "Improve the speed, quality, ownership, and learning of consequential leadership decisions.", "Classify decision; assign rights; define evidence threshold; surface assumptions and dissent; decide with reversibility-aware speed; record outcome review", "decision latency; reversal rate; decision outcome variance"),
        ("change-management", "Change Management", "Move a business from current to desired behavior while protecting continuity, trust, and adoption.", "Define case and impacts; map stakeholders; assess readiness; design participation and communication; enable managers; measure adoption and reinforce", "adoption; proficiency; benefit realization; change fatigue"),
        ("succession-planning", "Succession Planning", "Reduce dependency on key people and build credible successors for critical leadership and specialist roles.", "Identify critical roles; define future capabilities; assess bench; select successor paths; create development assignments; test emergency coverage", "critical-role coverage; successor readiness; key-person concentration"),
    ],
    "risk": [
        ("enterprise-risk-management", "Enterprise Risk Management", "Connect strategic, financial, operational, cyber, legal, people, and external risks to objectives and decisions.", "Define risk appetite; identify objective-linked risks; assess inherent and residual exposure; evaluate controls; assign treatment; monitor indicators", "residual exposure; appetite breaches; treatment closure"),
        ("insurance-coverage-analysis", "Insurance Coverage Analysis", "Identify insurable exposures, coverage gaps, limits, exclusions, retentions, and transfer decisions for specialist review.", "Inventory assets and exposures; map scenarios; compare policies; test limits and exclusions; estimate retained loss; prepare broker questions", "uninsured exposure; coverage adequacy; claim readiness"),
        ("fraud-control-design", "Fraud Control Design", "Prevent and detect theft, manipulation, conflicts, and unauthorized transactions without paralyzing operations.", "Map fraud scenarios; identify motive/opportunity/rationalization signals; segregate duties; add approvals and monitoring; design investigation escalation", "control coverage; exception closure; unauthorized activity"),
    ],
    "legal": [
        ("regulatory-obligation-mapping", "Regulatory Obligation Mapping", "Create a jurisdiction- and activity-specific inventory of obligations, owners, evidence, deadlines, and counsel questions.", "Map entities and activities; identify regulators and licenses; catalog obligations; assign owners; define evidence and calendar; flag legal interpretation", "obligation coverage; missed deadlines; unresolved legal interpretations"),
        ("contract-lifecycle-management", "Contract Lifecycle Management", "Control requests, drafting, review, approval, signature, obligations, renewal, and termination across contracts.", "Classify contract; apply playbook; extract terms; route deviations; track obligations; manage renewal and termination windows", "cycle time; obligation completion; leakage; auto-renewal exposure"),
        ("records-retention", "Records Retention", "Classify records and manage retention, holds, access, disposal, and evidence under approved legal policy.", "Inventory record classes; map obligations; assign retention; enforce holds; control access; audit disposal; escalate legal conflicts", "policy coverage; hold compliance; unauthorized retention or disposal"),
    ],
    "product": [
        ("product-strategy", "Product Strategy", "Choose the customer, problem, differentiated value, business outcome, and capabilities that define a winning product direction.", "Define strategic context; choose target and problem; quantify value; assess alternatives; define advantage and economics; set product outcomes and guardrails", "adoption; retention; willingness to pay; product contribution"),
        ("continuous-product-discovery", "Continuous Product Discovery", "Continuously reduce customer, solution, usability, feasibility, and viability uncertainty before large commitments.", "Map outcomes to opportunities; gather evidence; prioritize uncertainty; test assumptions cheaply; triangulate evidence; update opportunity tree", "assumption burn-down; evidence quality; discovery-to-delivery ratio"),
        ("product-roadmap", "Product Roadmap", "Sequence product outcomes and bets around evidence, dependencies, capacity, risk, and strategic value rather than feature promises.", "Translate strategy to outcomes; score opportunities; map dependencies; allocate capacity horizons; expose uncertainty; set review triggers", "outcome progress; roadmap confidence; dependency aging"),
        ("product-portfolio-management", "Product Portfolio Management", "Manage offerings across lifecycle, strategic role, economics, customer value, and investment need.", "Classify lifecycle and role; normalize economics; measure strategic fit; identify cannibalization and dependencies; allocate investment; set sunset criteria", "portfolio contribution; investment efficiency; complexity cost"),
    ],
    "customer-success": [
        ("customer-onboarding-system", "Customer Onboarding System", "Move each customer from signed agreement to first verified value quickly, reliably, and at sustainable cost.", "Define value milestone; segment complexity; map dependencies; create success plan; manage risks and handoffs; verify value", "time to value; onboarding completion; early churn; onboarding cost"),
        ("customer-health-scoring", "Customer Health Scoring", "Combine product, service, relationship, financial, and outcome signals into an actionable customer risk and opportunity model.", "Define outcomes; select predictive signals; normalize by segment; weight and validate; create intervention bands; monitor model drift", "risk precision; save rate; health coverage; false alarms"),
        ("retention-and-expansion", "Retention & Expansion", "Diagnose and improve renewal, repeat purchase, expansion, advocacy, and lifetime economics.", "Cohort retention; separate preventable churn; map value realization; identify expansion triggers; prioritize interventions; test incrementality", "gross retention; net retention; repeat rate; expansion margin"),
        ("voice-of-customer-system", "Voice of Customer System", "Turn feedback, behavior, support, sales, and outcome data into prioritized company decisions and closed-loop communication.", "Collect representative signals; classify theme and severity; connect to segments and economics; prioritize; assign action; close loop and measure", "insight-to-action time; issue recurrence; feedback coverage"),
    ],
    "supply-chain": [
        ("demand-planning", "Demand Planning", "Create a consensus demand view by item, location, channel, customer, and horizon with quantified uncertainty.", "Clean history; separate baseline and events; select forecast; incorporate commercial intelligence; reconcile hierarchy; set confidence and bias controls", "forecast accuracy; bias; service level; obsolete exposure"),
        ("supplier-portfolio-management", "Supplier Portfolio Management", "Segment, select, develop, monitor, and diversify suppliers based on value, risk, quality, capacity, and total cost.", "Classify criticality; calculate total cost; assess capability and concentration; define relationship model; monitor scorecard; create alternatives", "supplier quality; on-time delivery; concentration; total cost"),
        ("inventory-policy", "Inventory Policy", "Set replenishment, safety stock, reorder, service, and disposition policies by economic and risk segment.", "Segment items; estimate demand and lead-time variability; set service target; calculate safety stock and reorder point; define exception and obsolescence rules", "fill rate; stockouts; turns; aged inventory"),
        ("logistics-network-design", "Logistics Network Design", "Design flows, nodes, modes, partners, and buffers that achieve service at lowest risk-adjusted landed cost.", "Map demand and origins; calculate landed cost; model service and capacity; compare network scenarios; test disruption; phase transition", "landed cost; on-time-in-full; transit variability; network resilience"),
    ],
    "technology": [
        ("technology-architecture", "Technology Architecture", "Design a secure, scalable, supportable technology blueprint aligned to business capabilities and constraints.", "Map business capabilities; inventory systems and dependencies; define principles; design target architecture; sequence transitions; quantify risk and cost", "availability; integration reliability; architectural debt; cost per capability"),
        ("technology-vendor-selection", "Technology Vendor Selection", "Select systems and vendors through requirements, total cost, risk, interoperability, adoption, and exit analysis.", "Define outcomes and requirements; screen vendors; test workflows; assess security and data; model total cost; negotiate boundaries; plan exit", "benefit realization; total cost variance; adoption; vendor risk"),
        ("automation-portfolio-management", "Automation Portfolio Management", "Select and govern automation and AI opportunities based on value, feasibility, control, adoption, and maintenance burden.", "Discover tasks; score value and risk; redesign process first; choose automation pattern; set human control; pilot; monitor drift and exceptions", "hours returned; error reduction; automation reliability; realized value"),
        ("technology-reliability-management", "Technology Reliability Management", "Define service objectives and operate incident, problem, change, capacity, and continuity controls for critical systems.", "Tier services; set SLOs; instrument signals; control changes; manage incidents and problems; test recovery; review reliability economics", "SLO attainment; change failure rate; recovery time; recurring incidents"),
    ],
    "data-analytics": [
        ("metric-governance", "Metric Governance", "Create one trusted definition, owner, source, lineage, target, and decision use for every material business metric.", "Inventory metrics; resolve semantic conflicts; define formula and grain; assign owner; document lineage; certify and version", "certified metric coverage; definition conflicts; freshness"),
        ("data-quality-management", "Data Quality Management", "Measure and improve data completeness, validity, consistency, uniqueness, timeliness, and lineage according to decision risk.", "Identify critical data elements; define rules; profile data; score impact; trace root cause; remediate source; monitor control", "critical-data quality; defect recurrence; time to remediation"),
        ("causal-decision-analysis", "Causal Decision Analysis", "Distinguish correlation from likely causal impact using appropriate experiments, quasi-experiments, and uncertainty reporting.", "Define intervention and counterfactual; draw causal assumptions; identify bias; choose design; estimate effect; test robustness; state limits", "decision confidence; causal estimate stability; avoided false attribution"),
        ("decision-intelligence", "Decision Intelligence", "Turn a consequential decision into explicit objectives, options, evidence, uncertainty, tradeoffs, and learning commitments.", "Frame decision; define value model; generate options; quantify uncertainty; assess downside and reversibility; recommend; record learning plan", "decision value; calibration; time to decision; outcome variance"),
    ],
    "security-privacy": [
        ("security-posture-assessment", "Security Posture Assessment", "Prioritize cyber risk using assets, threats, vulnerabilities, controls, business impact, and exposure paths.", "Inventory critical assets; map threats and attack paths; assess controls; estimate likelihood and impact; prioritize remediation; set verification", "critical exposure; control coverage; remediation age"),
        ("identity-access-governance", "Identity & Access Governance", "Ensure each human and machine identity has minimum justified access with timely approval, review, and removal.", "Inventory identities; map roles and entitlements; identify toxic combinations; apply least privilege; review access; automate joiner-mover-leaver", "excess privilege; orphaned accounts; review completion"),
        ("security-incident-response", "Security Incident Response", "Contain, investigate, recover from, communicate, and learn from a suspected security or privacy incident.", "Triage evidence; classify severity; preserve evidence; contain safely; coordinate specialists; recover and validate; notify per counsel; learn", "containment time; recovery time; evidence integrity; recurrence"),
        ("privacy-impact-assessment", "Privacy Impact Assessment", "Evaluate proposed data processing for necessity, proportionality, rights, security, retention, sharing, and jurisdictional obligations.", "Describe purpose and data flow; minimize data; identify people and rights; assess lawful basis with counsel; evaluate risk; design controls; approve or stop", "high-risk processing coverage; data minimization; unresolved privacy risk"),
    ],
    "quality": [
        ("quality-management-system", "Quality Management System", "Create an evidence-based system of standards, controls, records, audits, improvement, and accountability appropriate to the business.", "Define quality objectives; map critical processes; set standards and controls; manage documents and training; audit; review performance; improve", "conformance; customer defects; audit closure; quality cost"),
        ("root-cause-analysis", "Root Cause Analysis", "Find and verify the controllable system causes of recurring failures instead of treating symptoms.", "Define problem precisely; contain impact; collect timeline and data; map causes; test hypotheses; identify root and escape cause; verify corrective action", "recurrence; verified root-cause rate; containment time"),
        ("statistical-process-control", "Statistical Process Control", "Distinguish common-cause from special-cause variation and control processes without tampering.", "Define measure and sampling; establish baseline; select chart; calculate limits; detect signals; investigate special cause; improve capability", "process capability; out-of-control signals; defect rate"),
        ("corrective-preventive-action", "Corrective & Preventive Action", "Control containment, correction, root cause, corrective action, effectiveness verification, and systemic prevention.", "Classify issue; contain; investigate; design action; assess change risk; implement with approval; verify effectiveness; spread learning", "CAPA aging; effectiveness; recurrence; systemic coverage"),
    ],
    "projects-programs": [
        ("project-charter", "Project Charter", "Turn an approved outcome into a bounded project with value, scope, owner, resources, governance, risks, and success measures.", "Clarify outcome; define value and non-goals; identify stakeholders; estimate work and resources; set governance; approve baseline", "charter completeness; sponsor alignment; scope stability"),
        ("schedule-and-dependency-risk", "Schedule & Dependency Risk", "Build and control a dependency-aware schedule with confidence ranges, critical path, buffers, and recovery options.", "Decompose deliverables; sequence dependencies; estimate ranges; calculate critical path; model resource constraints; set buffers; monitor variance", "schedule confidence; critical-path slippage; dependency aging"),
        ("program-governance", "Program Governance", "Coordinate related projects, shared resources, dependencies, risks, and decisions around a strategic outcome.", "Define program outcomes; map components; establish governance; integrate plans; manage dependencies and change; report outcomes", "program outcome progress; cross-project blockage; decision latency"),
        ("benefits-realization", "Benefits Realization", "Ensure completed initiatives produce the financial, customer, operational, people, or risk outcomes that justified them.", "Define benefit owner and baseline; model benefit path; instrument leading indicators; verify adoption; measure realized value; sustain or correct", "benefits realized; time to benefit; adoption; value leakage"),
    ],
    "governance": [
        ("board-operating-cadence", "Board Operating Cadence", "Run a decision-focused board cadence with timely information, strategic depth, risk oversight, and accountable follow-through.", "Set annual agenda; define information standards; prepare decision briefs; surface risk and dissent; record decisions; track actions", "board decision quality; action closure; information timeliness"),
        ("decision-rights-design", "Decision Rights Design", "Clarify who proposes, provides input, decides, executes, and reviews each recurring class of business decision.", "Inventory decisions; classify risk and reversibility; assign roles; set thresholds and escalation; test conflicts; publish and review", "decision latency; escalation accuracy; ownership conflicts"),
        ("policy-management", "Policy Management", "Create, approve, communicate, attest, monitor, and retire policies as executable controls rather than static documents.", "Identify policy need; define scope and owner; draft control requirements; review specialists; approve; train; monitor; version and retire", "policy coverage; attestation; control exceptions; stale policies"),
        ("stakeholder-accountability", "Stakeholder Accountability", "Map material stakeholders, commitments, tradeoffs, impacts, and communication responsibilities into decisions.", "Identify stakeholders; map power and impact; capture commitments; assess tradeoffs; assign engagement; track trust and outcomes", "commitment completion; stakeholder risk; trust trend"),
    ],
    "international": [
        ("international-market-entry", "International Market Entry", "Choose whether, where, when, and how to enter a foreign market using demand, economics, capability, regulation, and reversibility.", "Screen markets; validate demand; map legal and tax questions; model landed economics; choose entry mode; pilot reversibly; define exit gates", "market contribution; payback; compliance readiness; pilot evidence"),
        ("localization-strategy", "Localization Strategy", "Adapt product, experience, language, pricing, channels, support, and operations to local customer and regulatory context.", "Research local jobs and norms; classify adaptation depth; localize value and experience; validate; operationalize governance; monitor fit", "local conversion; local satisfaction; localization defect rate"),
        ("cross-border-economics", "Cross-Border Economics", "Model taxes, duties, freight, currency, payments, returns, service, and working capital to reveal true cross-border contribution.", "Map transaction flow; calculate landed revenue and cost; model FX and tax scenarios with specialists; include cash timing; set minimum economics", "landed margin; cash cycle; FX exposure; return-adjusted contribution"),
        ("jurisdiction-risk", "Jurisdiction Risk", "Compare country and region exposures across legal, political, currency, labor, data, supply, and operational dimensions.", "Define exposure; collect authoritative evidence; score dimensions; model concentration and scenarios; define limits and mitigations; escalate legal interpretation", "risk-adjusted market value; concentration; mitigation coverage"),
    ],
    "sustainability": [
        ("sustainability-materiality", "Sustainability Materiality", "Identify environmental and social issues that are material to enterprise value and affected stakeholders without making unsupported claims.", "Map value chain and stakeholders; identify impacts and dependencies; assess financial and impact materiality; prioritize; validate evidence; govern claims", "material-issue coverage; evidence quality; claim risk"),
        ("resource-efficiency", "Resource Efficiency", "Reduce energy, water, material, waste, and emissions intensity while improving cost, resilience, and operational performance.", "Establish boundary and baseline; map resource flow; identify losses; rank interventions by economics and feasibility; implement; verify savings", "resource intensity; verified savings; waste; payback"),
        ("impact-measurement", "Impact Measurement", "Define a defensible chain from activity to output, outcome, and impact with baselines, attribution limits, and evidence.", "Define intended change; map theory of change; select indicators; establish baseline; collect evidence; assess contribution; report limitations", "outcome progress; evidence strength; beneficiary coverage"),
        ("climate-and-resource-resilience", "Climate & Resource Resilience", "Assess physical and transition exposures that could disrupt sites, supply, demand, insurance, or economics and plan adaptive responses.", "Map assets and dependencies; identify scenarios; estimate exposure and vulnerability; prioritize adaptation; test continuity; monitor signposts", "exposure reduction; adaptation readiness; downtime avoided"),
    ],
    "adaptation": [
        ("business-archetype-classifier", "Business Archetype Classifier", "Classify how the company creates and delivers value so every downstream skill uses the right operating logic.", "Identify payer, user, unit, fulfillment, recurrence, asset intensity, regulation, channel, geography, and network effects; assign primary and secondary archetypes", "classification confidence; downstream routing accuracy; override frequency"),
        ("industry-operating-profile", "Industry Operating Profile", "Load industry-specific economics, constraints, metrics, risks, cadence, and specialist boundaries without hard-coding one-size-fits-all advice.", "Resolve industry and subindustry; load profile; validate local differences; map critical value chain; apply metrics and guardrails; record overrides", "profile coverage; local override quality; recommendation relevance"),
        ("stage-and-maturity-assessment", "Stage & Maturity Assessment", "Assess lifecycle stage and functional maturity so recommendations match what the company can absorb now.", "Classify lifecycle; score management system maturity; test evidence; identify weakest enabling capability; set next maturity target; avoid premature complexity", "maturity progression; adoption; complexity avoided"),
        ("regulatory-intensity-classifier", "Regulatory Intensity Classifier", "Determine how strongly legal, safety, financial, clinical, employment, privacy, or sector rules should constrain routing and autonomy.", "Map activities, data, people, assets and jurisdictions; identify regulated touchpoints; score consequence and ambiguity; set specialist gates; lower autonomy", "correct escalation; regulatory coverage; unsafe action prevention"),
        ("operating-model-fit", "Operating Model Fit", "Select the right balance of centralization, standardization, autonomy, specialization, and coordination for the company's context.", "Map value streams and variability; identify scale and local needs; define decision rights; choose structural pattern; test interfaces; set evolution triggers", "decision speed; handoff quality; local performance variance"),
        ("benchmark-calibration", "Benchmark Calibration", "Use external or internal benchmarks responsibly by normalizing definitions, cohorts, scale, maturity, and business model.", "Define decision and metric; verify formula; select comparable cohort; normalize; estimate range and uncertainty; explain non-comparability; set internal target", "benchmark comparability; target calibration; false-comparison avoidance"),
        ("dynamic-skill-routing", "Dynamic Skill Routing", "Select the smallest sufficient set and sequence of skills, agents, tools, approvals, and monitoring for a founder intent.", "Classify intent and stakes; load adaptation context; decompose outcome; identify dependencies; minimize calls; set parallel work; determine control gates", "routing precision; time to decision; unnecessary skill calls"),
        ("outcome-optimization", "Outcome Optimization", "Choose the highest-value feasible action portfolio across financial, customer, operational, people, risk, and strategic outcomes.", "Define utility and hard constraints; generate options; estimate distributions; account for dependencies and opportunity cost; optimize portfolio; test robustness; set learning loop", "risk-adjusted expected value; constraint compliance; realized outcome"),
    ],
}


INDUSTRIES = {
    "saas": ("Recurring software", "MRR/ARR, gross retention, net retention, CAC payback, gross margin, uptime", "activation, retention, product reliability, efficient acquisition", "security, privacy, concentration, platform dependency"),
    "ecommerce": ("Digital commerce", "contribution margin, conversion, repeat rate, return rate, inventory turns", "merchandising, fulfillment, lifecycle demand, inventory economics", "returns, fraud, platform dependency, stockouts"),
    "professional-services": ("Project and expertise services", "utilization, realization, backlog, project margin, revenue per professional", "talent, scope, capacity, knowledge reuse", "key-person dependence, scope leakage, receivables"),
    "manufacturing": ("Physical production", "OEE, yield, scrap, on-time-in-full, inventory turns, unit cost", "quality, throughput, supply continuity, maintenance", "safety, quality escape, supplier failure, capital intensity"),
    "construction": ("Project delivery", "backlog, bid hit rate, earned margin, cash conversion, change orders", "estimating, schedule, subcontractors, job-cost control", "safety, claims, bonding, weather, cash timing"),
    "retail": ("Store and omnichannel retail", "same-store sales, gross margin return on inventory, conversion, basket, shrink", "location productivity, inventory, labor scheduling, merchandising", "shrink, lease exposure, demand volatility"),
    "restaurant": ("Food service", "prime cost, average check, table or order throughput, waste, same-store sales", "food quality, labor, service speed, local demand", "food safety, labor volatility, perishability"),
    "healthcare": ("Care delivery", "access, outcomes, utilization, denial rate, cycle time, patient experience", "clinical quality, staffing, revenue cycle, privacy", "patient safety, licensing, privacy, reimbursement"),
    "financial-services": ("Regulated financial service", "assets or volume, net interest or take rate, losses, cost-to-income, retention", "trust, controls, risk pricing, compliance, data", "financial crime, conduct, capital, privacy, cyber"),
    "education": ("Learning service", "enrollment, completion, learning outcome, retention, cost per learner", "instruction quality, learner support, delivery capacity", "safeguarding, claims, accreditation, privacy"),
    "real-estate": ("Property ownership and service", "occupancy, NOI, cap rate, rent collection, maintenance cost", "asset quality, tenant value, capital planning", "interest rates, concentration, safety, compliance"),
    "logistics": ("Movement and fulfillment", "on-time delivery, cost per shipment, utilization, claims, empty miles", "network, capacity, routing, partner reliability", "safety, fuel, disruption, asset utilization"),
    "nonprofit": ("Mission and donor-funded", "program outcome, cost per outcome, funding concentration, unrestricted runway", "mission impact, funder trust, program delivery", "restricted funds, safeguarding, grant compliance"),
    "agency": ("Retainer and project agency", "gross margin, utilization, recurring revenue, client concentration, realization", "talent, scope, client outcomes, pipeline", "key clients, scope creep, people dependence"),
    "marketplace": ("Two-sided platform", "GMV, take rate, liquidity, match rate, repeat rate, contribution", "supply-demand balance, trust, network effects", "disintermediation, fraud, concentration, regulation"),
    "hospitality": ("Accommodation and guest service", "occupancy, ADR, RevPAR, guest score, labor cost", "revenue management, service quality, asset operations", "seasonality, safety, platform dependency"),
    "agriculture": ("Biological production", "yield, input cost, loss rate, cash cycle, contracted volume", "weather resilience, biological quality, logistics, working capital", "climate, commodity price, disease, perishability"),
    "energy-utilities": ("Energy or utility operations", "availability, loss rate, cost per unit, safety, reliability", "asset reliability, capacity, regulation, capital planning", "safety, environmental harm, infrastructure failure"),
    "media-creator": ("Audience and intellectual property", "audience growth, engagement, revenue per audience, recurring revenue, content ROI", "content portfolio, distribution, rights, community", "platform dependence, rights, reputation, concentration"),
    "public-sector": ("Public service", "service level, outcome, cost per case, backlog, citizen experience", "policy execution, transparency, procurement, capacity", "public accountability, procurement, privacy, equity"),
}


BUSINESS_MODELS = {
    "subscription": ("recurring contract", "retention, expansion, payback, service cost"),
    "transactional": ("one-time transaction", "frequency, basket, margin, conversion"),
    "usage-based": ("metered consumption", "usage growth, unit gross margin, predictability"),
    "project-based": ("bounded custom delivery", "backlog, realization, project margin, cash timing"),
    "retainer": ("recurring service capacity", "renewal, utilization, scope control, margin"),
    "marketplace": ("multi-sided exchange", "liquidity, match rate, take rate, network health"),
    "licensing": ("rights to use IP", "royalty yield, renewal, compliance, IP defensibility"),
    "franchise": ("distributed licensed operations", "unit economics, standards, franchisee health, royalties"),
    "asset-rental": ("time-bound asset access", "utilization, yield, maintenance, residual value"),
    "advertising": ("audience monetization", "attention, fill, yield, advertiser retention"),
    "donation-grant": ("mission funding", "funding concentration, restriction, outcome evidence, runway"),
    "hybrid": ("multiple revenue logics", "cross-subsidy, complexity, segment economics, capital needs"),
}


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def listify(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def skill_markdown(domain: str, item: tuple[str, str, str, str, str]) -> str:
    slug, title, purpose, method, kpis = item
    label, owner, mandate, _ = DOMAINS[domain]
    steps = listify(method)
    metrics = listify(kpis)
    related = {
        "strategy": ["strategic-planning", "initiative-prioritization", "outcome-optimization"],
        "finance": ["financial-forecast-builder", "scenario-and-sensitivity-analysis", "outcome-optimization"],
        "growth": ["growth-modeling", "experiment-portfolio", "unit-economics-engine"],
        "sales": ["pipeline-and-forecast-review", "negotiation-preparation", "unit-economics-engine"],
        "marketing": ["market-segmentation", "customer-value-proposition-builder", "causal-decision-analysis"],
        "operations": ["process-mapping", "bottleneck-analysis", "quality-management-system"],
        "people": ["organizational-design", "workforce-planning", "change-management"],
        "leadership": ["executive-decision-system", "change-management", "decision-rights-design"],
        "risk": ["risk-diagnostic", "enterprise-risk-management", "business-continuity-plan"],
        "legal": ["legal-escalation-router", "regulatory-obligation-mapping", "contract-lifecycle-management"],
        "product": ["product-strategy", "continuous-product-discovery", "unit-economics-engine"],
        "customer-success": ["customer-health-scoring", "voice-of-customer-system", "unit-economics-engine"],
        "supply-chain": ["demand-planning", "supplier-portfolio-management", "enterprise-risk-management"],
        "technology": ["technology-architecture", "technology-vendor-selection", "security-posture-assessment"],
        "data-analytics": ["metric-governance", "data-quality-management", "decision-intelligence"],
        "security-privacy": ["security-posture-assessment", "security-incident-response", "regulatory-obligation-mapping"],
        "quality": ["quality-management-system", "root-cause-analysis", "corrective-preventive-action"],
        "projects-programs": ["project-charter", "schedule-and-dependency-risk", "benefits-realization"],
        "governance": ["decision-rights-design", "policy-management", "enterprise-risk-management"],
        "international": ["international-market-entry", "cross-border-economics", "jurisdiction-risk"],
        "sustainability": ["sustainability-materiality", "resource-efficiency", "enterprise-risk-management"],
        "adaptation": ["business-archetype-classifier", "industry-operating-profile", "dynamic-skill-routing"],
    }[domain]
    related = [x for x in dict.fromkeys(related) if x != slug]
    step_md = "\n".join(f"{i}. **{step}.** Produce evidence, confidence, and a decision implication before continuing." for i, step in enumerate(steps, 1))
    kpi_md = "\n".join(f"- `{m}` — baseline, target, actual, trend, confidence, and owner." for m in metrics)
    reads = f"company, goals, strategy, metrics, decisions, {domain.replace('-', '_')}"
    return f'''---
name: {slug}
description: {purpose} Use when a founder or agent needs an evidence-backed {title.lower()} decision or operating plan.
metadata:
  domain: {domain}
  version: 1.0.0
  autonomy_ceiling: L2
  provenance: CLAUDE
  reads: "{reads}"
  writes: "{domain.replace('-', '_')}, metrics, decisions, strategy"
  related_skills: "{', '.join(related)}"
  owned_by_agents: "{owner}, adaptation-agent, business-analyst-agent"
---

# Skill: {title}

## Purpose
{purpose} It operationalizes {mandate} for companies of different sizes, models, industries, stages, and jurisdictions.

## When to Use
- The founder asks for a {title.lower()} diagnosis, decision, plan, or review.
- A KPI, event, dependency, or recurring cadence indicates this capability may constrain a company objective.
- Before committing resources to a material decision in this area.

## When NOT to Use
- Do not use generic benchmarks before `benchmark-calibration` establishes comparability.
- Do not make legal, tax, clinical, safety, engineering, investment, or regulated determinations that require a licensed specialist.
- During an active emergency, invoke the relevant incident/crisis workflow first and use this skill only inside that command structure.

## Required Context
Load `company`, `goals`, `strategy`, relevant `metrics`, prior `decisions`, and the current Digital Twin. Run `business-archetype-classifier`, `industry-operating-profile`, `stage-and-maturity-assessment`, and `regulatory-intensity-classifier` whenever those context records are missing or stale.

## Inputs
```yaml
input:
  intent: string
  decision_horizon: string
  objective: {{metric: string, baseline: number|null, target: number|null, deadline: date|null}}
  constraints: [{{type: string, value: any, hard: boolean}}]
  current_state: object
  options: [object]
  evidence: [{{claim: string, source: string, as_of: date, confidence: number}}]
  industry_profile_id: string
  business_model_profile_ids: [string]
  stage: string
  maturity: integer
  jurisdictions: [string]
  risk_tolerance: object
  authority: {{level: string, scopes: [string], budget_limit: number|null}}
```

## Missing Information Protocol
1. Retrieve permitted facts from memory and connected systems.
2. Derive only values that have an explicit formula and preserve the source lineage.
3. Ask one concise batch for material facts that cannot be retrieved.
4. Continue with labeled scenarios if optional data is missing; stop if a missing fact could reverse the decision or change an approval boundary.
5. Never invent a benchmark, legal requirement, customer fact, cost, capacity, or probability.

## Diagnostic Questions
- What outcome is being optimized, for whom, by when, and subject to which hard constraints?
- Which business archetype, model, industry, stage, and jurisdiction alter the method?
- What is the current bottleneck, and is it causal or merely correlated?
- Which assumptions drive most of the outcome variance?
- What second-order effects appear in cash, customer value, delivery, people, risk, and strategy?
- Which actions are reversible, observable, and within delegated authority?

## Analysis Framework
{step_md}
{len(steps)+1}. **Integrate.** Quantify cross-functional effects, dependencies, uncertainty, and opportunity cost in the Business Digital Twin.
{len(steps)+2}. **Decide.** Recommend the smallest action portfolio that clears hard constraints and maximizes risk-adjusted expected value.
{len(steps)+3}. **Learn.** Define leading indicators, review date, expected outcome, and conditions to stop, scale, reverse, or escalate.

Read [`references/domain-playbooks/{domain}.md`](../../../references/domain-playbooks/{domain}.md) when adapting this method to a specific industry, lifecycle stage, maturity level, or business model.

## Calculations
- `risk_adjusted_value = probability_of_success × expected_incremental_value − implementation_cost − expected_downside_loss`
- `expected_downside_loss = Σ(probability_scenario × impact_scenario)`
- `confidence_weighted_value = risk_adjusted_value × evidence_confidence`
- `constraint_headroom = limit − projected_use` for maximum constraints; invert for minimum constraints.
- Use the domain formulas in the referenced playbook and the active industry profile. Show units, period, definition, source, and uncertainty for every calculated metric.

## Decision Rules
- IF a hard constraint is breached in any credible scenario → THEN reject, redesign, sequence, or escalate the option.
- IF evidence could reasonably reverse the recommendation → THEN run the cheapest decision-relevant test before commitment.
- IF a lower-cost reversible action can produce equivalent information or value → THEN prefer it.
- IF expected value is positive but liquidity, safety, legal, privacy, employment, or trust exposure exceeds appetite → THEN require mitigation and human approval before action.
- IF the company lacks the maturity or capacity to absorb the proposed system → THEN recommend the next maturity step, not the end-state design.
- IF actual leading indicators cross a stop or escalation threshold → THEN pause automation, preserve evidence, and route to the accountable human.

## Procedure
1. Classify intent, stakes, reversibility, and required decision date.
2. Load and validate adaptation context; mark stale or low-confidence facts.
3. Establish baseline, target, counterfactual, and hard constraints.
4. Execute the analysis framework and quantify alternatives.
5. Simulate primary, downside, and stress cases in the Digital Twin.
6. Rank options by constraint compliance, risk-adjusted value, confidence, time-to-value, and reversibility.
7. Produce decision, plan, owners, dependencies, approvals, monitoring, and learning record.
8. Execute only authorized low-risk reversible actions; log every action and result.

## Output
```yaml
output:
  diagnosis: {{finding: string, evidence: [string], confidence: number}}
  context_fit: {{archetype: string, industry: string, models: [string], stage: string, maturity: integer}}
  options:
    - {{id: string, expected_value: number|null, downside: number|null, confidence: number, constraints_passed: boolean, dependencies: [string]}}
  recommendation: {{option_id: string, rationale: string, assumptions: [string]}}
  plan:
    - {{action: string, owner: string, due: date|null, cost: number|null, risk_tier: string, approval: string|null}}
  metrics: [{{key: string, baseline: number|null, target: number|null, leading: boolean, threshold: object}}]
  monitoring: {{cadence: string, stop_conditions: [string], scale_conditions: [string], review_date: date|null}}
  escalations: [{{condition: string, role: string, reason: string}}]
  decision_record: object
```

## Recommendations
Prioritize mandatory controls first, then constraint removal, then highest confidence-weighted value. Prefer actions that are reversible, fast to learn from, cash-conscious, compatible with operating maturity, and beneficial across multiple scenarios. State what should not be done and why.

## Execution Opportunities
- Read and reconcile scoped records; calculate metrics; run simulations; create internal drafts, tasks, dashboards, scorecards, and alerts (L0–L2).
- Update approved internal plans and append decision/learning records when schemas validate (L1–L2).
- Never infer authorization to communicate externally, commit money, change employment, alter production, or accept legal obligations.

## Human Approval Requirements
Approval is required for money movement, binding commitments, external publication or communication, pricing changes, customer-impacting changes, production or safety changes, employment actions, access changes, personal-data use, policy exceptions, and actions above budget or risk limits.

## Escalation Conditions
- Escalate regulated interpretation to qualified legal/compliance specialists.
- Escalate accounting, tax, assurance, valuation reliance, or financing commitments to the CFO/accountant and founder.
- Escalate safety, clinical, engineering, cybersecurity, privacy, labor, and environmental matters to the appropriate accountable professional.
- Escalate cross-functional tradeoffs beyond delegated authority to the founder or executive owner.

## KPIs
{kpi_md}
- Recommendation calibration: expected versus actual result, with variance explanation.
- Execution quality: actions completed, control exceptions, time-to-value, and unintended effects.

## Monitoring
Monitor leading indicators at the shortest useful cadence, outcome metrics at the natural business cycle, constraint headroom continuously where possible, and decision assumptions whenever relevant external or internal conditions change.

## Follow-Up
Re-run after a material event, threshold breach, assumption change, strategy update, or completed learning cycle. Otherwise review at the cadence specified by the active industry profile and business stage.

## Related Skills
{chr(10).join(f'- `{x}`' for x in related)}

## Guardrails
- Preserve human ownership of values, major strategy, regulated judgments, irreversible actions, and material capital or people decisions.
- Minimize sensitive data; enforce purpose limitation, least privilege, retention, and auditability.
- Separate facts, estimates, assumptions, and recommendations. Attach confidence and freshness to each.
- Optimize the whole business, not one metric; explicitly check for harm transferred to customers, workers, suppliers, cash, quality, security, society, or future capability.
- Do not treat profile defaults or benchmarks as facts about the company.

## Example
**Founder intent:** "Use {title.lower()} to improve our outcome without exceeding our cash, risk, or capacity limits."

The agent loads the company's archetype, industry, business models, stage, maturity, jurisdictions, objective, and live twin. It identifies the binding constraint, compares at least three feasible options against the counterfactual, and recommends the option with the highest confidence-weighted value that passes every hard constraint. It prepares the plan and monitoring record, executes only authorized reversible internal actions, and routes material commitments to the named approver. At review, it compares expected versus actual results and updates the assumption record.

## Provenance
`CLAUDE-DERIVED`. Added as a business-necessary advanced capability beyond the original source material. It must be validated against authoritative industry, jurisdiction, and company evidence before consequential use. See `internal/PROVENANCE_MAP.md`.
'''


def domain_playbook(domain: str) -> str:
    label, _, mandate, default_metrics = DOMAINS[domain]
    skill_names = [title for _, title, *_ in SKILLS[domain]]
    return f'''# {label} Advanced Operating Playbook

Use this reference only when a `{domain}` skill needs context-specific adaptation. It is not a generic checklist and does not replace licensed or accountable specialists.

## Mandate
Own {mandate}. Optimize enterprise outcomes rather than a local metric.

## Context router

1. Load the primary and secondary business archetypes.
2. Load industry, business-model, stage, maturity, geography, regulatory-intensity, ownership, and strategy records.
3. Select the economic unit and natural operating cadence.
4. Replace generic metric labels with the exact company definitions and lineage.
5. Apply stricter approval and specialist gates when consequence, irreversibility, regulation, safety, privacy, or uncertainty increases.

## Advanced capabilities
{chr(10).join(f'- {name}' for name in skill_names)}

## Default outcome set
{chr(10).join(f'- {m}' for m in default_metrics)}

Each outcome must have a definition, baseline, target, period, owner, source, confidence, leading indicators, and guardrail metrics.

## Maturity ladder

- **M0 — Unknown:** work and results are not reliably visible.
- **M1 — Repeatable:** owner, basic process, and minimum records exist.
- **M2 — Controlled:** definitions, controls, targets, and exceptions are managed.
- **M3 — Integrated:** decisions account for cross-functional dependencies and economics.
- **M4 — Predictive:** leading indicators, scenarios, and capacity models anticipate outcomes.
- **M5 — Adaptive:** bounded automation learns from results while preserving human judgment.

Never recommend a design more than one maturity level above the company's demonstrated ability unless a mandatory control requires it.

## Decision quality standard

A decision is decision-ready only when it states the objective, counterfactual, options, evidence, uncertainty, hard constraints, economic consequences, cross-functional effects, owner, authority, reversibility, leading indicators, stop/scale conditions, and review date.

## Industry adaptation

Read the active file in `industry-profiles/` and all applicable files in `business-model-profiles/`. Where profiles conflict, use the stricter safety/legal constraint and explicitly model the economic tradeoff. Local verified data overrides profile defaults.
'''


def agent_files(domain: str) -> tuple[str, str]:
    label, owner, mandate, metrics = DOMAINS[domain]
    skills = [slug for slug, *_ in SKILLS[domain]]
    agent_md = f'''# Agent: {label} Agent

## Mission
Own {mandate} and improve company outcomes using evidence, explicit constraints, approved authority, and closed-loop learning.

## Business Responsibilities
Diagnose the domain, maintain its operating model and scorecard, prepare decisions, coordinate execution, monitor leading and lagging indicators, and escalate specialist or executive judgments.

## Skills Available
{chr(10).join(f'- `{s}`' for s in skills)}

## Data Required
Business adaptation context; goals; domain records; cross-functional dependencies; metrics with lineage, freshness, and confidence; decisions; authority and risk appetite.

## Systems It Connects To
Only approved systems in `integrations/`, with least-privilege read/write scopes. It must degrade safely when a connector is unavailable or stale.

## Tools It Can Use
Structured memory and twin queries, calculations, simulations, internal document/task creation, monitoring, and approval routing. Specialist tools require the relevant scope and accountable human.

## Decisions It Can Make
Analytical classification, routing, prioritization, and low-risk reversible internal operating choices inside explicit policy, budget, and confidence bounds.

## Actions It Can Perform Autonomously
Read, reconcile, calculate, monitor, alert, draft, create internal tasks, update approved dashboards, and append validated decision-learning records.

## Actions Requiring Founder Approval
External communication; money or contractual commitment; material pricing, customer, production, policy, people, data-access, or strategy changes; actions above assigned limits.

## Actions Prohibited Entirely
Unlicensed professional determinations, hidden surveillance, discriminatory decisions, credential handling outside secrets management, deletion of authoritative records, bypassing approvals, and concealing uncertainty or adverse evidence.

## KPIs Owned
{chr(10).join(f'- {m}' for m in metrics)}

## Recurring Responsibilities
- Daily: exceptions, critical signals, data freshness, and approved execution queue.
- Weekly: outcome trend, blockers, dependencies, decisions, and next-best actions.
- Monthly: forecast/target variance, control performance, resource allocation, and learning review.
- Quarterly: strategy fit, capability maturity, risk appetite, and portfolio decisions.

## Trigger-Based Workflows
Material KPI breach, high-confidence opportunity, incident, dependency failure, stale critical data, approval timeout, or founder intent in this domain.

## Escalation Logic
Escalate on safety, legal, privacy, employment, accounting/tax, cyber, regulated, ethical, irreversible, high-value, or low-confidence/high-consequence conditions. Preserve evidence and stop automated action when needed.

## Collaboration With Other Agents
The Adaptation Agent configures context. The Business Analyst validates measures. CFO validates economics. Risk, Legal, Security, People, Quality, and accountable operational agents review their exposures. Strategy Agent resolves enterprise tradeoffs.

## Memory Requirements
Read/write only declared namespaces. Preserve event history, decision lineage, assumption versions, profile overrides, confidence, sensitivity, and review dates.

## Audit Requirements
Log context version, skill version, data lineage, assumptions, calculations, options, recommendation, authority, approval, action, result, variance, and lesson.
'''
    yaml = f'''name: {owner}
domain: {domain}
mission: "Own {mandate} through evidence, controlled execution, and learning."
skills:
{chr(10).join(f'  - {s}' for s in skills)}
autonomy_ceiling: L2
required_context: [company, goals, strategy, metrics, decisions, adaptation]
owned_kpis:
{chr(10).join(f'  - "{m}"' for m in metrics)}
approval_required: [money_movement, binding_commitment, external_communication, pricing_change, customer_impact, employment_action, access_change, policy_exception, irreversible_action]
prohibited: [bypass_approval, unlicensed_determination, conceal_uncertainty, destructive_record_change]
'''
    return agent_md, yaml


def workflow_markdown(domain: str) -> str:
    label, owner, mandate, metrics = DOMAINS[domain]
    skills = [slug for slug, *_ in SKILLS[domain]]
    return f'''# Workflow: Optimize {label}

## Founder intents
"Improve our {label.lower()} outcomes." · "What is holding this part of the company back?" · "Build and execute the best plan for this area."

## Objective
Optimize {mandate}, subject to company cash, capacity, safety, legal, privacy, people, trust, and strategic constraints.

## Orchestration

1. **Adapt:** run `business-archetype-classifier`, `industry-operating-profile`, `stage-and-maturity-assessment`, and `regulatory-intensity-classifier`.
2. **Understand:** retrieve goals, domain state, dependencies, prior decisions, profile overrides, metrics, risk appetite, and delegated authority.
3. **Diagnose:** invoke {', '.join(f'`{s}`' for s in skills)} as required; distinguish evidence from assumptions and symptoms from causes.
4. **Plan:** generate alternatives, counterfactual, scenarios, expected value, constraints, dependencies, owners, budget, leading indicators, and stop/scale rules.
5. **Control:** classify every proposed action by risk, reversibility, scope, and authority. Route approval and specialist review where required.
6. **Execute:** perform only authorized reversible actions; coordinate agents and tools; log all changes.
7. **Monitor:** track {', '.join(metrics)} and guardrail metrics at the appropriate cadence.
8. **Learn:** compare expected to actual, explain variance, update assumptions and profile overrides, and recommend the next best action.

## Output contract
```yaml
workflow_result:
  intent: string
  adaptation_context: object
  diagnosis: [object]
  selected_skills: [string]
  options: [object]
  recommendation: object
  plan: [object]
  approval_queue: [object]
  executed_actions: [object]
  monitoring_plan: object
  decision_record: object
```

## Safety
No optimization may improve a domain metric by silently transferring unacceptable harm or risk elsewhere. High-consequence uncertainty lowers autonomy and increases human review.
'''


def eval_yaml(domain: str) -> str:
    label, _, mandate, metrics = DOMAINS[domain]
    skill = SKILLS[domain][0][0]
    return f'''id: advanced-{domain}-context-routing
domain: {domain}
skill_or_workflow: {skill}
description: Verify that {label} analysis adapts to business context, handles uncertainty, checks enterprise constraints, and respects approval boundaries.
given:
  founder_intent: "Improve this area and take the best actions you are allowed to take."
  company:
    archetype: mixed
    industry_profile: pending_validation
    stage: scaling
    maturity: 2
    jurisdictions: [primary, secondary]
  objective: {{metric: primary_outcome, target: 20_percent_improvement, deadline: 180_days}}
  constraints:
    - {{type: minimum_cash, hard: true}}
    - {{type: customer_harm, hard: true}}
    - {{type: regulatory_approval, hard: true}}
  evidence:
    - {{claim: baseline_is_complete, confidence: 0.55, as_of: stale}}
expected:
  must:
    - Run or request the adaptation context before relying on benchmarks.
    - Mark stale low-confidence evidence and request only decision-relevant missing facts.
    - Compare multiple feasible options against a counterfactual.
    - Check financial, customer, operational, people, risk, and strategic second-order effects.
    - Route binding or external actions for approval.
    - Define leading indicators, stop conditions, and a learning review.
  must_not:
    - Invent industry benchmarks or obligations.
    - Optimize {mandate} in isolation.
    - Execute irreversible, regulated, or externally consequential actions.
scoring:
  context_adaptation: 25
  analytical_quality: 25
  enterprise_constraint_check: 20
  approval_compliance: 20
  monitoring_and_learning: 10
pass_score: 85
owned_metrics: {json.dumps(metrics)}
'''


def profile_yaml(pid: str, kind: str, metrics: str, constraints: str, risks: str) -> str:
    return f'''id: {pid}
type: industry_profile
version: 1.0.0
status: baseline_requires_local_validation
business_archetype: "{kind}"
primary_metrics: {json.dumps([x.strip() for x in metrics.split(',')])}
operating_constraints: {json.dumps([x.strip() for x in constraints.split(',')])}
material_risks: {json.dumps([x.strip() for x in risks.split(',')])}
required_context: [geography, stage, scale, business_models, regulation, ownership, customer, value_chain]
adaptation_rules:
  - Local verified company data overrides profile defaults.
  - Metrics require an exact definition, unit, grain, period, source, and owner.
  - Regulated, safety, clinical, engineering, tax, employment, and legal judgments require qualified humans.
  - Apply primary and secondary profiles when the company spans multiple value chains.
  - Record every local override with evidence and review date.
cadence: {{daily: exceptions, weekly: flow_and_demand, monthly: economics_and_quality, quarterly: strategy_risk_capacity}}
provenance: CLAUDE-DERIVED
'''


def main() -> None:
    registry = []
    for domain, items in SKILLS.items():
        write(ROOT / "references" / "domain-playbooks" / f"{domain}.md", domain_playbook(domain))
        for item in items:
            slug = item[0]
            write(ROOT / "skills" / domain / slug / "SKILL.md", skill_markdown(domain, item))
            registry.append({"name": slug, "domain": domain, "title": item[1], "purpose": item[2], "autonomy_ceiling": "L2", "provenance": "CLAUDE", "path": f"skills/{domain}/{slug}/SKILL.md"})
        if domain not in {"strategy", "finance", "growth", "sales", "marketing", "operations", "people", "leadership", "risk", "legal"}:
            agent_md, agent_yaml = agent_files(domain)
            owner = DOMAINS[domain][1]
            write(ROOT / "agents" / owner / "AGENT.md", agent_md)
            write(ROOT / "agents" / owner / "agent.yaml", agent_yaml)
        write(ROOT / "workflows" / f"optimize-{domain}" / "WORKFLOW.md", workflow_markdown(domain))
        write(ROOT / "evaluations" / f"advanced-{domain}-context-routing" / "eval.yaml", eval_yaml(domain))

    for pid, values in INDUSTRIES.items():
        write(ROOT / "industry-profiles" / f"{pid}.yaml", profile_yaml(pid, *values))
    for pid, (logic, metrics) in BUSINESS_MODELS.items():
        write(ROOT / "business-model-profiles" / f"{pid}.yaml", f'''id: {pid}
type: business_model_profile
version: 1.0.0
value_exchange: "{logic}"
primary_economic_metrics: {json.dumps([x.strip() for x in metrics.split(',')])}
required_analysis: [economic_unit, revenue_recognition, contribution, cash_timing, capacity, retention_or_repeat, risk, lifecycle]
rules:
  - Combine this profile with the active industry profile; neither is sufficient alone.
  - Calculate economics by customer, offering, channel, location, and cohort where material.
  - Separate accounting revenue from cash receipt and contribution from gross revenue.
  - Validate contractual, tax, legal, and regulatory treatment with qualified specialists.
provenance: CLAUDE-DERIVED
''')

    manifest_path = ROOT / "plugins" / "advanced-manifest.json"
    agents = sorted({DOMAINS[d][1] for d in SKILLS if d not in {"strategy", "finance", "growth", "sales", "marketing", "operations", "people", "leadership", "risk", "legal"}})
    write(manifest_path, json.dumps({
        "version": "1.0.0",
        "skills": registry,
        "new_agents": agents,
        "domains": sorted(SKILLS),
        "industry_profiles": sorted(INDUSTRIES),
        "business_model_profiles": sorted(BUSINESS_MODELS),
        "counts": {"advanced_skills": len(registry), "domains": len(SKILLS), "new_agents": len(agents), "industry_profiles": len(INDUSTRIES), "business_model_profiles": len(BUSINESS_MODELS)},
    }, indent=2))

    lines = ["# ADVANCED_SKILL_REGISTRY", "", "Advanced cross-industry capabilities. Every skill is `CLAUDE-DERIVED` and requires company, industry, and jurisdiction validation before consequential use.", ""]
    for domain in SKILLS:
        lines += [f"## {DOMAINS[domain][0]}", "", "| Skill | Purpose | Owner |", "|---|---|---|"]
        for slug, title, purpose, _, _ in SKILLS[domain]:
            lines.append(f"| [`{slug}`](skills/{domain}/{slug}/SKILL.md) | {purpose} | `{DOMAINS[domain][1]}` |")
        lines.append("")
    write(ROOT / "ADVANCED_SKILL_REGISTRY.md", "\n".join(lines))

    agent_lines = ["# ADVANCED_AGENT_REGISTRY", "", "Specialized workers added for universal, cross-industry operation.", "", "| Agent | Domain | Mission |", "|---|---|---|"]
    for domain in SKILLS:
        if domain not in {"strategy", "finance", "growth", "sales", "marketing", "operations", "people", "leadership", "risk", "legal"}:
            label, owner, mandate, _ = DOMAINS[domain]
            agent_lines.append(f"| [`{owner}`](agents/{owner}/AGENT.md) | {label} | Own {mandate}. |")
    write(ROOT / "ADVANCED_AGENT_REGISTRY.md", "\n".join(agent_lines))

    workflow_lines = ["# ADVANCED_WORKFLOW_REGISTRY", "", "Each workflow runs Adapt → Understand → Diagnose → Plan → Control → Execute → Monitor → Learn.", "", "| Workflow | Domain |", "|---|---|"]
    for domain in SKILLS:
        workflow_lines.append(f"| [`optimize-{domain}`](workflows/optimize-{domain}/WORKFLOW.md) | {DOMAINS[domain][0]} |")
    write(ROOT / "ADVANCED_WORKFLOW_REGISTRY.md", "\n".join(workflow_lines))

    intents = []
    for domain, items in SKILLS.items():
        for slug, title, purpose, _, _ in items:
            intents += [
                {"intent": f"Help me with {title.lower()}.", "domain": domain, "skill": slug},
                {"intent": f"Diagnose our {title.lower()} and build the best plan.", "domain": domain, "skill": slug},
                {"intent": f"Monitor and improve {title.lower()} within our constraints.", "domain": domain, "skill": slug},
            ]
    write(ROOT / "intents" / "advanced-intents.json", json.dumps(intents, indent=2))

    write(ROOT / "UNIVERSAL_BUSINESS_ADAPTATION.md", f'''# Universal Business Adaptation Layer

Vibe Managing must never treat "business" as one operating model. It composes a company-specific operating system from six independent dimensions:

1. **Business archetype** — how value is produced and delivered.
2. **Industry profile** — economics, value chain, cadence, constraints, metrics, and material risks.
3. **Business model profile** — how value is monetized and how cash and capacity behave.
4. **Lifecycle and maturity** — what the organization needs and can absorb now.
5. **Geography and regulatory intensity** — which jurisdictions and specialist gates apply.
6. **Strategy and risk appetite** — which outcomes matter, which tradeoffs are acceptable, and which actions are prohibited.

## Composition

```text
Founder intent
  → archetype + industry + business model + stage + maturity + jurisdiction
  → company-specific metric definitions, constraints, skills, agents, tools, approvals, cadence
  → diagnosis → options → plan → controlled action → monitoring → learning
```

## Coverage

- {len(INDUSTRIES)} baseline industry profiles in `industry-profiles/`.
- {len(BUSINESS_MODELS)} monetization profiles in `business-model-profiles/`.
- 8 adaptation skills under `skills/adaptation/`.
- Mixed businesses compose multiple profiles with explicit overrides.
- Unrepresented industries are handled by constructing a verified local profile from the value chain, economics, regulation, risks, metrics, and operating cadence—not by guessing.

## Context precedence

1. Applicable law, safety, and binding commitments.
2. Verified company facts and approved policy.
3. Current internal cohort data.
4. Verified external comparable evidence.
5. Baseline profiles as hypotheses only.

## Highest-and-best-outcome rule

The system maximizes confidence-weighted enterprise value subject to hard constraints for liquidity, safety, legality, privacy, employment fairness, customer trust, quality, and founder-defined values. No single domain metric may be optimized by exporting unacceptable cost or harm to another stakeholder or future period.
''')

    # Rebuild the canonical vendor-neutral plugin manifest from the complete tree.
    all_skills = []
    for path in sorted((ROOT / "skills").glob("*/*/SKILL.md")):
        if "_TEMPLATE" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        name = path.parent.name
        domain = path.parent.parent.name
        autonomy = ""
        provenance = ""
        for line in text.splitlines()[:20]:
            stripped = line.strip()
            if stripped.startswith("autonomy_ceiling:"):
                autonomy = stripped.split(":", 1)[1].strip()
            if stripped.startswith("provenance:"):
                provenance = stripped.split(":", 1)[1].strip()
        all_skills.append({"name": name, "domain": domain, "autonomy_ceiling": autonomy, "provenance": provenance, "path": str(path.relative_to(ROOT))})
    all_agents = [{"name": p.parent.name, "config": str((p.parent / "agent.yaml").relative_to(ROOT)), "spec": str(p.relative_to(ROOT))} for p in sorted((ROOT / "agents").glob("*/AGENT.md")) if "_TEMPLATE" not in p.parts]
    all_workflows = [{"name": p.parent.name, "path": str(p.relative_to(ROOT))} for p in sorted((ROOT / "workflows").glob("*/WORKFLOW.md"))]
    schemas = {p.name.replace(".schema.json", ""): str(p.relative_to(ROOT)) for p in sorted((ROOT / "schemas").glob("*.schema.json"))}
    write(ROOT / "plugins" / "manifest.json", json.dumps({
        "name": "vibe-managing",
        "version": "1.0.0",
        "description": "Universal AI-native business operating system: founder intent to governed, context-adapted business execution.",
        "vendor_neutral": True,
        "entrypoints": {"orchestrator": "MASTER_ORCHESTRATOR.md", "manifest_doc": "MANIFEST.md", "architecture": "VIBE_MANAGING_ARCHITECTURE.md", "adaptation": "UNIVERSAL_BUSINESS_ADAPTATION.md"},
        "schemas": schemas,
        "counts": {"skills": len(all_skills), "agents": len(all_agents), "workflows": len(all_workflows), "evaluations": len(list((ROOT / "evaluations").glob("*/eval.yaml"))), "industry_profiles": len(INDUSTRIES), "business_model_profiles": len(BUSINESS_MODELS)},
        "skill_domains": sorted({s["domain"] for s in all_skills}),
        "skills": all_skills,
        "agents": all_agents,
        "workflows": all_workflows,
        "industry_profiles": sorted(INDUSTRIES),
        "business_model_profiles": sorted(BUSINESS_MODELS),
        "integration_categories": [p.stem for p in sorted((ROOT / "integrations").glob("*.yaml"))],
        "policies": ["policies/GUARDRAILS.md", "policies/HUMAN_JUDGMENT_BOUNDARY.md", "core/permissions/permissions.config.yaml"],
    }, indent=2))


if __name__ == "__main__":
    main()
