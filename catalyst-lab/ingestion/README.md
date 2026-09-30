# Ingestion bridge

Longbridge was read successfully through the connected ChatGPT tool: 1,000 daily forward-adjusted candles each for NKE.US and SPY.US. Raw snapshots remain local and are excluded from this public repository. Use `import_longbridge.py` to validate connector JSON exports. Explicit forward adjustment is required when requesting exports; the importer cannot detect adjustment from the values alone.

ChatGPT connectors are not credentials for a deployed application. Continuous ingestion requires separately authorized server-side provider access and data-use rights. No background jobs or billable subscriptions have been enabled.

Public event seeds in `data/events.json` use SEC acceptance timestamps. They document filings, not the earliest announcement time. Current/historical-looking Longbridge consensus has no publication timestamps, so it is excluded from model training.

Primary source endpoints for subsequent adapters:

| Engine | Owner | Missing production requirement |
|---|---|---|
| Earnings / IPO | SEC submissions `https://data.sec.gov/submissions/CIK0000320187.json`, issuer IR | Contact User-Agent, pagination, archival documents, first-publication timestamp |
| Contracts | USAspending, SAM.gov, UK Find a Tender | Entity match, funded obligation versus ceiling, release timestamps |
| Clinical | ClinicalTrials.gov API v2, FDA | Historical record versions, earliest results release, ownership mapping |
| UK announcements | Issuer IR, LSE/RNS | Licensed archive, exact release timestamp, exchange calendars |
| Macro | BLS, BEA, ONS, central banks | Release vintages, historical consensus snapshots, market sensitivities |

Sources checked: https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data (maximum 10 requests/second); https://www.nlm.nih.gov/pubs/techbull/ma24/ma24_clinicaltrials_api.html (modernized API). Adapter discovery is not proof of operational ingestion.
