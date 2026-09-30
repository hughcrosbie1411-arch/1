# Deployment

## Current state

The local build requires no paid service. Vercel team discovery returned no teams, the exposed deployment operation returned tool-not-found, and CLI was absent at initial inspection. A deployed website is not claimed. GitHub inspection identified the existing public repository `hughcrosbie1411-arch/1`; creation of a new repository was not available. See the final delivery status for any subsequent publication outcome.

## Reproducible run

Install Node 20.9+ and Python 3.11+. Run `npm ci`, `npm run build`, and `npm start`. For research checks run `cd research && python -m unittest -v`. GitHub Actions repeats the Python checks and web build. Never add source credentials to browser bundles; future source tokens must be server-only environment variables without a public prefix.

## Future preview checklist

Connect the chosen GitHub repository to an accessible Vercel account/project. Configure Next.js build and verify snapshot redistribution rights before serving data publicly. Deploy a preview, inspect all routes, errors, diagnostics and keyboard/mobile behaviour, then promote only a verified build. Keep the last verified deployment for rollback. Provision PostgreSQL separately only when authorised; apply and test `migrations/001_event_ledger.sql` against a disposable instance first. No database, cron, observability or live ingestion is configured in the initial app.
