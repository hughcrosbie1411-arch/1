# Architecture

The executable first release uses a Next.js App Router interface, captured data snapshots and an offline Python research core. It can be served locally without a database. The manual event-study interface computes research transformations, not forecasts.

The target pipeline is source adapters → immutable raw documents → canonical event ledger → point-in-time feature snapshots → versioned research/model experiments → immutable predictions → separately observed outcomes → challenger evaluation → explicit promotion. The SQL contract separates each stage. Security identity persists through ticker changes via `security_id`.

Only market snapshot capture and offline research/UI are operational. Scheduled primary-source ingestion, database writes, authentication, model training, automated outcomes, monitoring and deployment remain unimplemented. Heavy model jobs should run outside request handlers; Vercel would serve a read-only research frontend/API after deployment resources are available. No scheduler is configured to imply a working ingestion service.
