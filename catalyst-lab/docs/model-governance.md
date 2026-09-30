# Model governance

No champion is active. A model may enter the registry only with code/dataset versions, immutable artifact hash, feature list, parameters, training/validation/holdout windows and evaluation metrics. Each prediction records its model version and frozen feature snapshot; outcomes are separate append-only observations. Corrections use superseding records rather than rewriting history.

The SQL schema rejects features unavailable at cutoff, edits/deletions to snapshots, features, predictions, models and outcomes, and addition of features after a prediction. These database protections are a proposed contract, not a verified deployed service. Privileged database owners can bypass triggers; production requires least privilege, backups and externally anchored audit hashes.

Challengers require explicit approval and credible held-out predictive/calibration/economic improvement, adequate event counts and complexity/stability review. No automatic promotion based on a small sample. Drift monitoring should measure feature, forecast, calibration and outcome changes, with regime-appropriate baselines. Drift automation and retraining are not yet wired.

Live forecasts must be captured before outcomes; historical runs are labelled backtests. Recalibration creates a new version and never rewrites original predictions. Preserve rejected candidates and all promotion evidence.
