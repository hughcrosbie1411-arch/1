# Data sources and capability matrix

| Source/layer | Intended responsibility | Observed availability | Training eligibility |
|---|---|---|---|
| Longbridge | OHLCV and market response | 1,000 forward-adjusted daily bars each for NKE.US/SPY.US captured | Descriptive research; adjustment provenance and event alignment still require scrutiny |
| Longbridge consensus | Expectations | Historical publication/availability timestamps unavailable | Excluded from historical training |
| Public Equity Investing | Analyst workflow, structured feature interpretation and audit | Workflow guidance used; not an independent historical dataset | Every extracted feature needs cited provenance and point-in-time availability |
| SEC/issuer IR | Earnings, filings, IPOs | Source targets; continuous adapter not operational | Only after publication timestamp capture and QA |
| USAspending/SAM.gov; UK procurement | Contract obligations and awards | Source targets; adapters not operational | Distinguish ceiling from funded amount |
| ClinicalTrials.gov/FDA/EMA/MHRA | Clinical and regulatory events | Source targets; adapters not operational | Preserve exact document publication and results availability |
| LSE/RNS/UK issuer IR | Regulated UK announcements | Source targets; adapters not operational | Licensing and retrieval eligibility unresolved |
| BLS/BEA/ONS/central banks; vintage series | Economic releases | Source targets; adapters not operational | Original release vintage plus timestamped consensus required |
| GitHub | Code, CI and versions | One existing public repo found; new-repo capability unavailable | Never store credentials |
| Vercel | Preview/production frontend | Team discovery empty; deploy tool returned tool-not-found | Deployment not completed |

Store provider, document URL/identifier, publication time, ingestion time, content hash, licence status and immutable raw object reference. Public accessibility does not by itself permit republication. Captured adjusted prices are not guaranteed point-in-time corporate-action vintages. Do not invent unavailable fields. A source target in this table is not an implemented integration.
