# Validation record — 30 September 2026

Eight Python tests passed locally. They test point-in-time rejection, label maturity purging, simultaneous event grouping, market-adjusted CAR arithmetic, sample-size abstention, exclusive forecast creation, future-outcome isolation and baseline abstention.

The baseline runner was exercised on two source-verified SEC earnings filing dates using captured NKE/SPY daily prices. It returned `insufficient_sample`, zero eligible held-out predictions and no performance metrics. This is an abstention check, not proof of predictive validity. Synthetic values in unit tests test software mechanics only.

PostgreSQL is not installed/provisioned in this execution environment. The SQL migration has not been runtime validated. Vercel team discovery returned zero teams and the deployment operation returned `McpServerError: Tool deploy_to_vercel not found`; CLI is absent. No preview or production URL exists.

See final GitHub PR for web test/build verification. Continuous ingestion, fitted specialist models, audited consensus vintages and live model learning remain unimplemented. No paid infrastructure or automatic trading was enabled.
