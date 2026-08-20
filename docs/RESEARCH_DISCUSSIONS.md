# Research & Discussion Topics for AMF v1.1

**Generated**: August 20, 2026  
**Purpose**: Catalog advanced research areas requiring deeper investigation and team discussion  
**Status**: Open for comments and research collaboration

---

## 📚 Research Tracks

### Track 1: Policy & Regulatory Architecture

#### Discussion 1.1: Tiered Regulatory Framework Harmonization
**Theme**: How to model policy harmonization across different regulatory regimes

**Key Questions**:
- How do regulatory tiers interact across jurisdictions (e.g., SEC rules vs. FCA rules on same asset)?
- What is the "impedance mismatch" cost when markets operate under divergent regimes?
- Can we measure cross-jurisdictional policy arbitrage risk?
- Which policy layers are "harmonizable" and which are path-dependent?

**Research Areas**:
- Lamfalussy levels (EU financial services) vs. US regulatory structure
- Post-2008 Basel III compliance divergence across G20 nations
- Brexit impact on EU/UK market bifurcation
- GDPR vs. SEC data-sharing regimes (conflict case study)

**Deliverable**: `docs/research/policy_harmonization.md` with case studies

---

#### Discussion 1.2: Entrenchment Thresholds & Constitutional Economics
**Theme**: When does a policy become immovable? What makes a financial rule "constitutional"?

**Key Questions**:
- What percentage of binding coverage makes a layer "entrenched"?
- How long does a policy need to be in force before it becomes self-reinforcing?
- Are entrenchment thresholds the same across democracies, autocracies, mixed systems?
- Can we detect entrenchment empirically (via legislative failure rates)?

**Research Areas**:
- Brennan & Buchanan's constitutional economics
- Sabatier's Advocacy Coalition Framework (ACF) — which layers are ACF "deep core" vs "policy core"?
- Historical policy changes: How many failed attempts before success?
- Case: Can the US modify Securities Act of 1933 (93 years old, rarely rewritten)?

**Deliverable**: `docs/research/entrenchment_theory.md` + dataset of policy lifespans

---

#### Discussion 1.3: Regulatory Change Modes & Market Instability
**Theme**: Different change modes (displacement, layering, drift, conversion) create different cascades

**Key Questions**:
- Which change mode creates maximum market disruption?
- How do markets pre-adapt to anticipated displacement vs. gradual drift?
- Can we measure "regulatory uncertainty" as a market stress input to AMF?
- What is the lead time for market participants to adjust to each mode?

**Research Areas**:
- Streeck & Thelen (2005) institutional change modes applied to finance
- Dodd-Frank (2010) "layering" mode: how did markets adjust year by year?
- MiFID II (2018) "displacement" mode in Europe: compare to Dodd-Frank
- Hong Kong vs. Singapore regulatory convergence/divergence (real-time study)

**Deliverable**: `docs/research/change_modes_impact.md` + case study matrix

---

### Track 2: Global Market Mapping & Taxonomy

#### Discussion 2.1: Global Equity Market Classification
**Theme**: What are the atomic units of equity markets? How do we classify them?

**Key Questions**:
- Is a "national stock exchange" the right unit, or should we split by asset class (large-cap, small-cap, SPAC, etc.)?
- How do we handle off-exchange trading (dark pools, OTC), which is now ~40% of US equities?
- Should we model retail vs. institutional markets separately?
- How do we capture "shadow capital" (private equity, hedge funds) that influences public markets?

**Research Areas**:
- NYSE + Nasdaq + CBOE ecosystem vs. single "US equity market" model
- Emerging markets: Is a single exchange sufficient (e.g., Shanghai Composite)?
- Fragmentation in Europe: Euronext + LSE + Deutsche Börse + regional exchanges
- Cross-listing complexity: Alibaba on Nasdaq but controlled by Hang Seng

**Deliverable**: `docs/taxonomies/equity_market_classification.md` + global exchange dataset

---

#### Discussion 2.2: Liquidity Measurement Across Asset Classes
**Theme**: "Liquidity" has different meanings in equities, bonds, forex, commodities. Can we unify?

**Key Questions**:
- Bid-ask spread works for equities; does it work for bonds (where spreads vary wildly by issuer)?
- Forex trades $6T/day but mostly between banks — is retail liquidity separate?
- Commodity futures vs. physical commodity liquidity — which matters for markets?
- How do we measure "flash crash" risk as illiquidity metric?

**Research Areas**:
- Kyle's lambda (resilience), effective spread, realized spread — which best predicts crisis?
- Goodhart's Law: Does measuring liquidity change it?
- Central Bank interventions (QE, rate cuts) as liquidity provider vs. market structure
- Stress liquidity vs. normal-times liquidity (two different beasts)

**Deliverable**: `docs/research/liquidity_unified_framework.md` with metrics per asset class

---

#### Discussion 2.3: Regulatory Regime Mapping by Country
**Theme**: Create a global taxonomy of financial-services regulation

**Key Questions**:
- How do we represent regulatory "strictness" or "progressiveness" dimensionlessly?
- What is the regulatory distance between US/EU/Asia/LatAm?
- How do we encode policy uncertainty (are rules enforced consistently)?
- Which countries have "shadow regulatory regimes" (enforcement discretion)?

**Research Areas**:
- World Bank Regulatory Quality Index + IMF financial stability assessments
- Financial Action Task Force (FATF) AML/KYC regimes
- ESG vs. Traditional regulation split
- Sanctions & capital controls as regulatory layer

**Deliverable**: `docs/taxonomies/regulatory_regimes_by_jurisdiction.md` + heatmap

---

### Track 3: Shock Propagation & Contagion

#### Discussion 3.1: Contagion via Policy, Not Just Markets
**Theme**: Financial crises propagate through policy failure, not just illiquidity. How do we model it?

**Key Questions**:
- 2008 crisis: Did contagion spread via interbank lending, or via policy paralysis?
- COVID-19 (2020): Markets crashed, then policy intervened (QE), then recovered. How to model?
- Can policy contagion be faster/slower than market contagion?
- What policies trigger "circuit breakers" vs. amplify shocks?

**Research Areas**:
- 2008 Bear Stearns collapse → Lehman failure → AIG bailout chain
- 2010 Greek crisis → Eurozone contagion → sovereign-bank feedback loop
- 2020 COVID: Policy speed of response (Fed rate cuts, Treasury intervention) prevented 2008 repeat
- Brexit vote (2016): Market shock then policy uncertainty, no banking crisis

**Deliverable**: `docs/research/policy_contagion_models.md` with 3–5 case studies

---

#### Discussion 3.2: Feedback Loops: Markets ↔ Policy
**Theme**: Markets move policy (e.g., market crash forces rate cut) and policy moves markets

**Key Questions**:
- What is the time-lag from market shock to policy response?
- Do markets "anticipate" policy changes before they're announced?
- Can policy move at the speed of electronic markets (~milliseconds)?
- What is the delay between policy announcement and market impact?

**Research Areas**:
- Fed rate decision announcements: Market reaction within 100ms
- Circuit breaker halts: Do they give policymakers time, or damage confidence?
- Central Bank communication (forward guidance) as pre-emptive market adjustment
- Negative rates (ECB, BoJ): Market resistance via capital flight

**Deliverable**: `docs/research/market_policy_feedback.md` with time-series analysis

---

#### Discussion 3.3: Systemic Risk Indicators
**Theme**: What are leading indicators of financial system failure?

**Key Questions**:
- VIX (equity volatility) is well-known. What about credit spreads, forex volatility, commodity price variance?
- How do we aggregate them into a single "system health" score?
- Can we predict crisis 6–12 months ahead using policy + market metrics?
- Which indicators work in different crisis types (banking, currency, debt, liquidity)?

**Research Areas**:
- Minsky moments (excessive debt, fragility in financial structure)
- Kaleckian instability (profits/investment cycles)
- Behavioral risk (herd behavior, panic selling)
- Regulatory arbitrage (weaknesses exploited by market participants)

**Deliverable**: `docs/research/systemic_risk_indicators.md` with mathematical framework

---

### Track 4: Fraud & Market Abuse Detection

#### Discussion 4.1: Hindenburg Report — What Does It Tell Us About Market Structure?
**Theme**: Can regulatory structures have blind spots that enable fraud?

**Key Questions**:
- Hindenburg's targets (Nikola, Adani, etc.): Were they enabled by regulatory gaps or violations?
- What structural vulnerabilities in skeleton/circulatory/nervous systems enabled deception?
- Can AMF predict which markets/companies are "high-fraud-risk"?
- What policy changes would have prevented each case?

**Research Areas**:
- Nikola (2020): EV startup claims vs. reality — disclosure gap
- Wirecard (2020): Audit failure — who watched the watchers?
- Adani (2023): Related-party transactions + export credit masking
- Common thread: Regulatory arbitrage (gaps between accounting, auditing, enforcement)

**Deliverable**: `docs/case_studies/hindenburg_analysis.md` + fraud indicators framework

---

#### Discussion 4.2: Market Abuse Detection via Network Analysis
**Theme**: Fraudsters leave traces in transaction networks. Can we detect patterns?

**Key Questions**:
- What network signatures indicate pump-and-dump schemes?
- How do insider-trading rings structure trades to avoid detection?
- Can we model "manipulation cascades" (one actor influences many others)?
- Are there scale-free network properties that emerge in fraud vs. legitimate trading?

**Research Areas**:
- Social network analysis of trader relationships
- Transaction graph: Who trades with whom, in what order?
- Information asymmetry: Who knows what, when?
- Temporal patterns: Abnormal clustering of trades

**Deliverable**: `docs/research/fraud_detection_networks.md` + algorithmic framework

---

#### Discussion 4.3: Regulatory Capture & Policy Failure
**Theme**: When regulators are "captured" by the industry, policy becomes complicit in fraud

**Key Questions**:
- What are the markers of regulatory capture (e.g., revolving door, weak enforcement)?
- Which countries/regulators have higher capture risk?
- Can we measure capture quantitatively (enforcement rate vs. violations detected)?
- How does capture feedback into our policy models?

**Research Areas**:
- Stigler's Economic Theory of Regulation (industry captures regulator)
- Revolving door: SEC official → investment bank → SEC again
- Enforcement disparity: Large firms settled with fines; small firms prosecuted criminally
- Regulatory monoculture: One agency (SEC) overseeing 4000+ listed companies

**Deliverable**: `docs/research/regulatory_capture_theory.md` with metrics

---

### Track 5: Emerging Markets & Frontier Finance

#### Discussion 5.1: Frontier Market Stability & Policy Volatility
**Theme**: In emerging markets, policy itself is often the largest source of risk

**Key Questions**:
- How do we model "policy uncertainty" in markets without stable rule of law?
- Should the entrenchment model differ in autocracies vs. democracies?
- What is the "policy half-life" in unstable regimes (days? weeks?)?
- How do external shocks (IMF conditions, sanctions) reshape policy?

**Research Areas**:
- Turkey: Central bank independence eroded; policy became volatile
- Argentina: Currency regime changes every 5–10 years; peso devaluation cycles
- Venezuela: Hyperinflation as policy failure cascading through all markets
- China: Policy announcements move markets more than economic data

**Deliverable**: `docs/research/frontier_market_policy_risk.md` with case studies

---

#### Discussion 5.2: Informal Finance & Shadow Banking
**Theme**: In many economies, formal markets are dwarfed by informal finance

**Key Questions**:
- Can we model "parallel economies" (informal lending, money remittances, cryptocurrencies)?
- How do informal and formal markets interact/compete?
- What happens when informal capital "formalizes" (e.g., BNPL platforms, crypto exchanges)?
- How do regulators govern markets they can't see?

**Research Areas**:
- India: Informal lending (chit funds) exceeds bank lending in some regions
- Africa: Mobile money (M-Pesa) bypasses traditional banking
- China: P2P lending networks (some collapsed, others absorbed into formal system)
- Crypto: $3T market that exists outside regulatory perimeter

**Deliverable**: `docs/research/informal_finance_modeling.md` + market estimates

---

#### Discussion 5.3: Currency Risk & Capital Flight
**Theme**: Emerging market crises often feature currency collapses and capital flight

**Key Questions**:
- How do we model capital flight as a systemic event (not just individual decisions)?
- What role does policy uncertainty play in triggering runs?
- Can we predict currency crises 6–12 months ahead using AMF?
- How do capital controls work (and fail) to prevent capital flight?

**Research Areas**:
- Trilemma: Can't have free capital flows + fixed currency + independent policy
- Asian Financial Crisis (1997): Thailand → Korea → Russia contagion
- Argentine crisis (2001): Bank runs, currency collapse, policy shock
- Sri Lankan crisis (2022): Forex reserves → currency collapse → political instability

**Deliverable**: `docs/research/currency_crisis_models.md` with predictive framework

---

### Track 6: Technology & Market Evolution

#### Discussion 6.1: High-Frequency Trading & Regulatory Arbitrage
**Theme**: Technology enables new forms of market abuse. Can policy keep up?

**Key Questions**:
- HFT strategies: Order spoofing, layering, spoofing. Are they detectable via network analysis?
- Latency arbitrage: Exchanges competing to be "fastest". Social benefit?
- Regulation lag: By the time a rule is written, traders have adapted. How to close this gap?
- Should there be a "speed limit" for markets (e.g., min. 100ms between trades)?

**Research Areas**:
- Flash Crash (2010): What happened and why?
- IEX Exchange: Built to prevent HFT abuses; now 2% market share
- Citadel Securities as market maker: Benefit or predator?
- PFOF (payment for order flow): Rebates vs. best execution

**Deliverable**: `docs/research/hft_regulation_gap.md` with proposals

---

#### Discussion 6.2: Fintech Disruption & Regulatory Fragmentation
**Theme**: New technologies (APIs, crypto, AI) create new regulatory challenges

**Key Questions**:
- Where do fintech firms live in the regulatory tree (bank? broker? something new)?
- Crypto exchanges: Regulated as exchanges? Banks? Commodity venues?
- Buy-now-pay-later (BNPL): Credit regulated? Consumer finance regulated? Not regulated?
- AI/algorithmic advisors: Do existing advisor regulations apply?

**Research Areas**:
- Silvergate, FTX bankruptcies: Regulatory gaps in crypto banking
- Robinhood vs. traditional brokers: Commission-free trading enabled retail herd behavior (GME saga)
- Stablecoin reserves: Who audits them? Who's liable if they fail?
- Regulatory arbitrage: Fintech moves to low-regulation jurisdictions (Panama, Cayman Islands)

**Deliverable**: `docs/research/fintech_regulatory_fragmentation.md` with classification matrix

---

#### Discussion 6.3: AI/ML in Finance — New Risks & Opportunities
**Theme**: Machine learning optimizes trading and risk, but introduces new systemic risks

**Key Questions**:
- If all traders use the same ML model, do they converge to the same positions (crowding risk)?
- How do we stress-test an ML model if we don't understand how it decides?
- Can AI-driven trading amplify feedback loops (policy → markets → policy)?
- Do regulators need to audit ML models before deployment?

**Research Areas**:
- Model risk: JP Morgan's CCAR model vs. actual stress outcomes
- Crowding: Passive index investing (60%+ of US equity flows) creates monoculture
- Adversarial ML: Can traders fool market surveillance AI?
- Responsible AI: What does "fairness" mean in algorithmic trading?

**Deliverable**: `docs/research/ai_systemic_risk.md` with governance proposals

---

### Track 7: Geopolitical & Macro Policy

#### Discussion 7.1: Sanctions as a Financial Weapon
**Theme**: Sanctions reshape capital flows, asset classes, and market structure

**Key Questions**:
- How do sanctions on a major economy (Russia, Iran) propagate through global markets?
- Do markets pre-adapt to anticipated sanctions (capital flight, asset reallocation)?
- Secondary sanctions: How effective are they? Do they create "resistance markets"?
- What is the cost to global liquidity when major economies are cut off from SWIFT?

**Research Areas**:
- Russia-Ukraine war (2022): SWIFT expulsion, capital controls, asset freezes
- Iran sanctions: Oil market volatility, banking sector isolation
- China decoupling risk: What if US imposes sanctions similar to Russia?
- Alternative payment systems (CIPS, cryptocurrency, barter) as sanction workarounds

**Deliverable**: `docs/research/sanctions_market_impact.md` with case studies

---

#### Discussion 7.2: Central Bank Independence Under Political Pressure
**Theme**: When politicians constrain central bank autonomy, policy becomes volatile

**Key Questions**:
- What metrics indicate central bank independence/capture?
- How does loss of independence correlate with inflation, currency devaluation?
- Can we predict policy reversals when political pressure builds?
- What is the market impact of a central bank's independence being questioned?

**Research Areas**:
- Fed independence: Trump pressure vs. institutional autonomy (2017–2021)
- ECB: Political pressure from North (fiscal hawks) vs. South (stimulus advocates)
- Turkey: Erdogan firing central bank governors who resist rate cuts (2023)
- UK: Bank of England independence preserved even during 2022 pension fund crisis

**Deliverable**: `docs/research/central_bank_independence.md` with quantitative index

---

#### Discussion 7.3: Deglobalization & Market Fragmentation
**Theme**: Geopolitical tensions are driving markets to fragment (not integrate)

**Key Questions**:
- Are we seeing a "splinternet" in finance (US markets, China markets, EU markets)?
- How do sanctions + tariffs + capital controls reshape capital flows?
- What is the cost of market fragmentation (liquidity, efficiency, access)?
- Can markets remain globally integrated if geopolitical risk is very high?

**Research Areas**:
- Trade wars (2018–2020): Tariffs changed manufacturing networks
- Semiconductor shortages (2021–2023): Revealed supply chain fragility
- Nearshoring: Companies moving supply chains closer to home
- Financial decoupling: SWIFT alternatives, dual-use technologies, capital controls

**Deliverable**: `docs/research/deglobalization_market_impact.md` with structural analysis

---

### Track 8: Climate, ESG & Long-Term Risk

#### Discussion 8.1: Climate Risk as Systemic Financial Risk
**Theme**: Climate change will reprrice assets; regulatory response is fragmentary

**Key Questions**:
- How do we measure "transition risk" (stranded assets, carbon taxes)?
- How do we measure "physical risk" (extreme weather, sea-level rise)?
- Which market segments are most exposed (energy, insurance, real estate)?
- Can a "climate stress test" be built into AMF?

**Research Areas**:
- Stranded fossil fuel assets: $1–2T at risk if carbon pricing rises
- Insurance industry: Profitability erodes if catastrophe frequency increases
- Real estate: Coastal properties at risk; inland properties benefit
- Sovereign debt: Small island nations face existential climate risk

**Deliverable**: `docs/research/climate_financial_risk.md` with asset class analysis

---

#### Discussion 8.2: ESG Mandates & Unintended Consequences
**Theme**: ESG regulation aims to internalize externalities, but creates new risks

**Key Questions**:
- Does mandatory ESG screening reduce market efficiency?
- ESG "washing": How do companies green-wash ESG ratings?
- Liquidity consequences: If ESG removes capital from "bad" sectors, does that impair resilience?
- Regulatory arbitrage: Do ESG-disfavored companies relocate to weaker jurisdictions?

**Research Areas**:
- Divestment movements: Fossil fuel divestment success? Alternative energy investment?
- German coal phase-out: Reliance on Russia gas (ironic given 2022 sanctions)
- Emerging market distress: ESG reduces capital to LatAm/Africa
- Regulatory fragmentation: EU taxonomy vs. US ESG standards vs. ISSB

**Deliverable**: `docs/research/esg_unintended_consequences.md` with case studies

---

#### Discussion 8.3: Biodiversity Collapse & Financial System Risk
**Theme**: Biodiversity loss is the least-priced financial risk; when it reprices, shock will be large

**Key Questions**:
- Which industries depend on biodiversity (agriculture, pharma, fisheries)?
- How do we quantify the cost of pollinator decline, soil depletion, deforestation?
- Is there a "biodiversity bubble" (ecosystem services underpriced)?
- Can a financial crisis trigger from ecological collapse?

**Research Areas**:
- Davos 2023: "Biodiversity risk" added to systemic risk agenda
- Agricultural commodity markets: Monoculture as risk (crop failures)
- Pharma supply chains: Compound extraction from natural products (50%+ of drugs)
- Insurance pricing: Catastrophe models based on historical data, not climate-altered futures

**Deliverable**: `docs/research/biodiversity_financial_risk.md` with valuation framework

---

---

## 🗂️ Cross-Cutting Research Themes

### Theme A: Measurement & Metrics
- How do we quantify regulatory quality, policy entrenchment, systemic risk?
- Dimensionless metrics vs. calibrated estimates
- Observable vs. latent variables
- Validation against real crises

### Theme B: Temporal Dynamics
- Policy lag times (announcement → enforcement → market impact)
- Crisis time horizons (hours for flash crash, weeks for contagion, months for policy adaptation)
- Historical precedent vs. novel regimes

### Theme C: Institutional Heterogeneity
- Do models work the same in democracies vs. autocracies?
- Developed vs. emerging markets
- Centralized vs. decentralized financial structures

### Theme D: Network Effects
- How does interconnectedness amplify shocks?
- Hub-and-spoke vs. distributed resilience
- Cascading failures: When does one failure trigger many?

---

## 📌 How to Engage

**For each discussion:**
1. **Open a GitHub Discussion** (use the template below)
2. **Invite domain experts** to comment
3. **Link to related issues** (e.g., Discussion 1.1 → Issue #31, #32)
4. **Track progress** in this file

### Discussion Template

```markdown
# Discussion [#.#]: [Topic]

**Track**: [Track name]  
**Research Type**: [Theoretical / Empirical / Case Study / Framework]  
**Status**: Open for comments

## Problem Statement
[1–2 paragraphs on why this matters]

## Key Questions
- [ ] Question 1
- [ ] Question 2
- [ ] Question 3

## Research Areas
- Area 1: [Description]
- Area 2: [Description]

## Deliverable
`docs/research/[filename].md` or implementation PR

## Comments
[Threaded discussion below]
```

---

## 🚀 Next Steps

1. **This week**: Create GitHub Discussions for Tracks 1–3 (most foundational)
2. **Next week**: Create Discussions for Tracks 4–5 (fraud & emerging markets)
3. **Later**: Tracks 6–8 (tech, geopolitics, climate)
4. **Assign research leads** to each Track
5. **Monthly review**: Consolidate findings into `docs/research/` and integrate into code

---

**Created**: August 20, 2026  
**Maintained by**: Autonomous Agent + Research Community  
**Last Updated**: [To be updated as discussions progress]
