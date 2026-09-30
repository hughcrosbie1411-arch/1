# Quantitative research core

Run `cd research && python -m unittest -v`.

`quant.py` provides auditable primitives, not a trained trading strategy:

- Aligned adjusted prices → daily benchmark-adjusted abnormal returns and arithmetic CAR. Estimate any beta strictly before the event. Session alignment and corporate action adjustment must happen upstream.
- `Observation.validate()` rejects features published after the forecast timestamp. Store actual publication/ingestion availability, not the economic period to which a fact refers. Revised macro series and restated fundamentals require point-in-time vintages.
- `walk_forward()` freezes each test block's training snapshot and excludes labels unavailable before its cutoff. Same-time events stay together. The embargo parameter widens the gap; choose it for the label horizon and dependencies. Fit preprocessing and tune parameters inside the training period using a nested chronological split.
- `probability_bins()` displays empirical hit rates and Wilson intervals only when the explicit sample threshold is met. Supply held-out forecasts only. Wilson intervals assume independent Bernoulli outcomes; correlated issuer/event clusters need a block bootstrap before production inference.
- `write_prediction()` writes a new forecast once and hashes its canonical payload. This prevents accidental overwrites locally; it is not tamper-proof. Production requires access-controlled append-only storage and externally anchored hashes. Attach eventual outcomes in separate records.

Before modelling, acquire licensed point-in-time prices, corporate actions, event timestamps, consensus vintages, exchange calendars, costs and delisted securities. Separate issuer families and repeated events where dependence affects validation. Compare against simple market-adjusted and unconditional baseline forecasts, reporting held-out calibration, Brier score, sample counts and net-of-cost returns. Record rejected models and multiple-testing choices. Do not promote a model because its in-sample fit looks good.

No observations, backtests, probability estimates or research results are fabricated by this module. It intentionally abstains when support is inadequate.
