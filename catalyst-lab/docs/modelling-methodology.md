# Modelling methodology

Start with unconditional market-adjusted event-study baselines. Compare conditional averages and regularised regression before fitting flexible trees or boosting. Separate earnings, contracts, clinical/regulatory, IPO, UK announcement and macro processes. Pre-event forecasts and post-announcement reaction forecasts are different tasks and must have different cutoffs.

The research core implements returns, daily benchmark adjustment, timestamp eligibility, chronological evaluation, probability summaries and forecast recording. It does not fit a validated model. No expected return, probability or confidence score is displayed as a live model estimate without a supported dataset and held-out evidence.

Abnormal return for the baseline is stock simple return minus aligned benchmark simple return. Arithmetic CAR sums these daily abnormal returns; this differs from compounded buy-and-hold abnormal return. Any market-model beta must be estimated strictly before the event. SPY is only a broad US market baseline for NKE, not a proven optimal benchmark. No intraday horizons can be derived from daily bars.

Maintain original release vintages and timestamped consensus. Feature availability must precede prediction time. Separate fact, consensus, guidance, interpretation and assumption. Fit imputation, scaling, feature selection and hyperparameters inside training folds. Empirical frequency intervals are not forecast confidence intervals, and clustered observations need block/bootstrap treatment.
