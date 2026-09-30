# Catalyst Lab

Event-driven equity research foundation for six catalyst classes. This is a functioning local research application with genuine captured market data and manual event-study controls. It is not a validated trading model.

## Run

Use Node 20.9+ and Python 3.11+. From `catalyst-lab/`, run `npm ci`, import authorized Longbridge snapshots using `ingestion/import_longbridge.py`, then `npm run dev`, then open http://localhost:3000. Run `npm run build` for a production build. Run `python -m unittest discover -s research -v` for mathematical and leakage checks.

## Current evidence

Longbridge returned 1,000 forward-adjusted daily observations each for NKE.US and SPY.US. These are captured snapshots, not a live feed. Historical consensus timing is unavailable, so current consensus must not be used as historical model inputs. No live predictions, fitted catalyst engines, performance claims or automatic trades are enabled. The app supports an exploratory benchmark-adjusted daily event study; it does not establish an earnings strategy's predictive validity.

The PostgreSQL migration is a production-oriented schema contract. No persistent database has been provisioned and the migration has not been exercised against a running PostgreSQL instance. GitHub inspection found one existing public repository (`hughcrosbie1411-arch/1`); repository creation is unavailable through the inspected tools. Vercel team discovery returned no teams, the deployment operation returned tool-not-found, and the CLI was absent at initial inspection. No preview or production URL is claimed. Development is committed on the `catalyst-lab` branch in the `catalyst-lab/` folder, preserving the existing project.

## Structure

`app/`: Next.js interface. `data/`: public SEC event seeds; authorized market snapshots are local and excluded from GitHub. `research/`: auditable numerical routines and tests. `migrations/`: append-only event/feature/prediction schema. `docs/`: source map, methodology and operational constraints. Root `.github/workflows/catalyst-lab.yml`: build and numerical CI.

No paid services or automated brokerage transactions are required by the local build. Verify market-data redistribution terms before public deployment.
