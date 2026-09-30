# Backtesting

A manual event study is descriptive, not a strategy backtest. The captured NKE/SPY universe contains neither verified historical earnings-event labels nor timestamped consensus; this release therefore makes no out-of-sample alpha claim.

The Python core provides chronological walk-forward primitives that exclude outcomes unavailable at each training cutoff and keep same-time events together. Embargo length must reflect the maximum label window and cross-event dependence. Use nested chronological tuning and reserve a final untouched holdout. Record every experiment, including failed models and repeated tests.

Before strategy evaluation: acquire delisted securities and corporate actions; resolve exact release/session timing with an exchange calendar; define executable entry prices; model spreads, slippage, fees, gaps and liquidity; avoid overlapping position double-counting. After-close events enter at the next executable session, not an already known closing price. Daily close-to-close exploratory returns do not represent an achievable announcement trade.

Report sample counts, MAE/RMSE, calibration/Brier/log loss, rank correlation, tails and costs where applicable. Bootstrap by dependent event/issuer blocks. Untested calendar assumptions, timestamp-unknown consensus and future revisions are exclusion flags. Keep live forecasts entirely separate from simulated historical forecasts.
