import type { CSSProperties } from 'react';

const layers = [
  { n: '01', name: 'Adapt', copy: 'Industry, model, stage, maturity, geography, regulation.' },
  { n: '02', name: 'Understand', copy: 'A living memory and digital twin of the whole company.' },
  { n: '03', name: 'Diagnose', copy: 'Evidence-backed root causes, constraints, risks, and opportunities.' },
  { n: '04', name: 'Plan', copy: 'Options, scenarios, priorities, owners, budgets, and expected outcomes.' },
  { n: '05', name: 'Execute', copy: 'Agents and tools act inside explicit authority and approval limits.' },
  { n: '06', name: 'Learn', copy: 'Expected versus actual becomes the next better decision.' },
];

const domains = [
  'Strategy', 'Finance', 'Growth', 'Sales', 'Marketing', 'Operations',
  'People', 'Leadership', 'Risk', 'Legal', 'Product', 'Customer Success',
  'Supply Chain', 'Technology', 'Data & Analytics', 'Security & Privacy',
  'Quality', 'Projects & Programs', 'Governance', 'International',
  'Sustainability', 'Business Adaptation',
];

const context = [
  ['Archetype', 'How value is produced'], ['Industry', 'Economics & constraints'],
  ['Business model', 'How value becomes revenue'], ['Stage', 'What the company needs now'],
  ['Maturity', 'What it can absorb'], ['Jurisdiction', 'Which rules and gates apply'],
];

const agentGroups = [
  ['Direction', 'Strategy · Leadership · Governance · Adaptation'],
  ['Economics', 'Finance · Growth · Sales · Marketing'],
  ['Value', 'Product · Customer Success · Operations · Quality'],
  ['Infrastructure', 'Supply Chain · Technology · Data · Security'],
  ['Enterprise', 'People · Risk · Legal · Projects · International · Sustainability'],
];

const industries = ['SaaS', 'E-commerce', 'Professional Services', 'Manufacturing', 'Construction', 'Retail', 'Restaurant', 'Healthcare', 'Financial Services', 'Education', 'Real Estate', 'Logistics', 'Nonprofit', 'Agency', 'Marketplace', 'Hospitality', 'Agriculture', 'Energy & Utilities', 'Media & Creator', 'Public Sector'];

const controls = [
  ['L0', 'Observe', 'Read, calculate, diagnose, recommend.'],
  ['L1', 'Prepare', 'Draft plans, changes, and approval packages.'],
  ['L2', 'Limited', 'Run reversible, pre-authorized actions.'],
  ['L3', 'Supervised', 'Execute bounded workflows with live oversight.'],
  ['L4', 'High autonomy', 'Only proven, observable, reversible workflows.'],
];

export default function Home() {
  return (
    <main>
      <nav className="nav shell">
        <a className="brand" href="#top" aria-label="Vibe Managing home">
          <span className="brand-mark">VM</span>
          <span>Vibe Managing</span>
        </a>
        <div className="nav-links">
          <a href="#system">System</a>
          <a href="#domains">Domains</a>
          <a className="nav-cta" href="https://github.com/innovaigs/Vibe-Managing">Explore repository ↗</a>
        </div>
      </nav>

      <section id="top" className="hero shell">
        <div className="hero-copy">
          <p className="eyebrow"><span /> An operating system for the whole business</p>
          <h1>Founder intent.<br /><em>Business execution.</em></h1>
          <p className="lede">Tell Vibe Managing the outcome you want. It understands the company, finds the constraint, builds the plan, coordinates execution, asks when human judgment matters, and learns from the result.</p>
          <div className="hero-actions">
            <a className="button primary" href="#system">See how it works <span>↓</span></a>
            <a className="button quiet" href="https://github.com/innovaigs/Vibe-Managing">Read the operating system ↗</a>
          </div>
        </div>

        <div className="intent-card" aria-label="Example Vibe Managing conversation">
          <div className="intent-head"><span className="pulse" /> LIVE BUSINESS INTENT</div>
          <div className="founder-msg">“Can we hire three salespeople without putting cash at risk?”</div>
          <div className="system-thinking">
            <div className="thinking-title"><span className="mini-mark">VM</span><strong>Vibe Managing</strong><span className="checking">Analyzing</span></div>
            <div className="checks">
              <span>✓ Cash & runway</span><span>✓ Pipeline capacity</span><span>✓ Rep economics</span><span>✓ Hiring risk</span>
            </div>
            <div className="answer"><strong>Recommendation</strong><p>Hire one now. Stage two additional hires behind pipeline and cash milestones. Runway remains above the 6-month floor.</p></div>
            <div className="approval"><span>1 action needs approval</span><button>Review plan →</button></div>
          </div>
        </div>
      </section>

      <section className="proof shell" aria-label="System scale">
        <div><strong>160</strong><span>operational skills</span></div>
        <div><strong>23</strong><span>specialized agents</span></div>
        <div><strong>22</strong><span>business domains</span></div>
        <div><strong>32</strong><span>orchestrated workflows</span></div>
        <div><strong>20</strong><span>industry profiles</span></div>
      </section>

      <section id="system" className="system-section shell">
        <div className="section-intro">
          <p className="eyebrow"><span /> THE OPERATING LOOP</p>
          <h2>Complexity stays.<br /><em>The system absorbs it.</em></h2>
          <p>Every request moves through one governed loop—adapted to the actual company, connected to real data, and bounded by human approval.</p>
        </div>
        <div className="layer-grid">
          {layers.map((layer) => (
            <article className="layer" key={layer.n}>
              <span className="layer-num">{layer.n}</span>
              <div><h3>{layer.name}</h3><p>{layer.copy}</p></div>
            </article>
          ))}
        </div>
      </section>

      <section id="domains" className="domain-strip">
        <div className="shell">
          <p className="eyebrow light"><span /> ONE INTELLIGENCE LAYER, EVERY FUNCTION</p>
          <div className="domain-cloud">
            {domains.map((domain, index) => <span className={index > 9 ? 'new-domain' : ''} key={domain}>{domain}</span>)}
          </div>
        </div>
      </section>

      <section className="adapt-section shell">
        <div className="adapt-title">
          <p className="eyebrow"><span /> UNIVERSAL, NOT GENERIC</p>
          <h2>The system changes<br />for <em>your business.</em></h2>
          <p>A restaurant, SaaS company, manufacturer, clinic, construction firm, nonprofit, and marketplace do not share one management playbook. Vibe Managing composes one.</p>
        </div>
        <div className="adapt-map">
          <div className="intent-node">Founder<br /><strong>intent</strong></div>
          <div className="context-stack">
            {context.map(([title, copy]) => <div key={title}><strong>{title}</strong><span>{copy}</span></div>)}
          </div>
          <div className="router-node"><span>ADAPTATION ENGINE</span><strong>Right intelligence.<br />Right controls.<br />Right cadence.</strong></div>
          <div className="outcome-node">Coordinated<br /><strong>outcome</strong></div>
        </div>
      </section>

      <section className="agents-section">
        <div className="shell">
          <div className="section-head-row">
            <div><p className="eyebrow light"><span /> SPECIALIZED INTELLIGENCE</p><h2>23 agents.<br /><em>One company.</em></h2></div>
            <p>Each agent owns a function over time. The orchestrator assembles the smallest team needed for the founder’s outcome, then resolves cross-functional tradeoffs before anything happens.</p>
          </div>
          <div className="agent-network">
            <div className="orchestrator-core"><small>MASTER</small><strong>Vibe Managing<br />Orchestrator</strong><span>Intent → Outcome</span></div>
            <div className="agent-rings">
              {agentGroups.map(([title, list], i) => <article key={title} style={{'--i': i} as CSSProperties}><span>{String(i+1).padStart(2,'0')}</span><div><strong>{title}</strong><p>{list}</p></div></article>)}
            </div>
          </div>
        </div>
      </section>

      <section className="control-section shell">
        <div className="control-copy">
          <p className="eyebrow"><span /> HUMAN JUDGMENT, BUILT IN</p>
          <h2>Autonomy is<br /><em>earned.</em></h2>
          <p>The objective is not maximum autonomy. It is maximum useful autonomy with the appropriate level of control. Every action is classified by consequence, reversibility, authority, confidence, and risk.</p>
          <blockquote>Humans own values, major strategy, sensitive people decisions, legal commitments, regulated judgment, and irreversible capital allocation.</blockquote>
        </div>
        <div className="control-ladder">
          {controls.map(([level, name, copy], i) => <article key={level} className={`control-${i}`}><span>{level}</span><div><strong>{name}</strong><p>{copy}</p></div></article>)}
        </div>
      </section>

      <section className="industry-section">
        <div className="shell">
          <div className="industry-title"><p className="eyebrow"><span /> INDUSTRY-AWARE BY DESIGN</p><h2>One operating system.<br /><em>Many kinds of business.</em></h2></div>
          <div className="industry-grid">{industries.map((industry, i) => <div key={industry}><span>{String(i+1).padStart(2,'0')}</span><strong>{industry}</strong></div>)}</div>
          <p className="profile-note">Mixed or unlisted business? The system constructs a local profile from the value chain, economics, regulation, risks, metrics, and operating cadence—then asks a human to validate what matters.</p>
        </div>
      </section>

      <section className="closing shell">
        <p className="eyebrow"><span /> THE INTERFACE TO THE COMPANY</p>
        <h2>Say what you want.<br /><em>Let the system handle the machinery.</em></h2>
        <p>Vibe Managing translates entrepreneurial intent into coordinated business action—without pretending that expertise, accountability, or human judgment disappeared.</p>
        <a className="button primary" href="https://github.com/innovaigs/Vibe-Managing">Explore the complete system <span>↗</span></a>
      </section>

      <footer><div className="shell"><div className="brand"><span className="brand-mark">VM</span><span>Vibe Managing</span></div><p>Founder Intent → Business Execution</p><a href="#top">Back to top ↑</a></div></footer>
    </main>
  );
}
