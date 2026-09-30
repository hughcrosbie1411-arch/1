"""Point-in-time catalyst research primitives. No trading or fitted-result claims."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
import json
from pathlib import Path
from statistics import mean
from typing import Iterable


@dataclass(frozen=True)
class Observation:
    event_id: str
    event_at: datetime
    label_available_at: datetime
    label: float
    features: tuple[tuple[str, float, datetime], ...]

    def validate(self) -> None:
        if self.event_at.tzinfo is None or self.label_available_at.tzinfo is None:
            raise ValueError('Timezone-aware timestamps required')
        if self.label_available_at <= self.event_at:
            raise ValueError('Label must become available after event')
        names = set()
        for name, value, available_at in self.features:
            if name in names:
                raise ValueError('Duplicate feature')
            names.add(name)
            if available_at.tzinfo is None or available_at > self.event_at:
                raise ValueError(f'Feature {name} was not known at prediction time')
            if not isinstance(value, (int, float)) or not __import__('math').isfinite(value):
                raise ValueError('Feature must be finite')
        if not __import__('math').isfinite(self.label):
            raise ValueError('Label must be finite')


def abnormal_returns(stock_prices: Iterable[float], benchmark_prices: Iterable[float], *, beta: float = 1.0) -> dict:
    """Daily simple-return abnormal returns and arithmetic CAR.

    Prices must be corporate-action-adjusted, aligned to the same trading sessions.
    Beta must be fixed using only pre-event observations; default is market-adjusted.
    CAR is the sum of daily abnormal returns, not compounded wealth.
    """
    import math
    stock, benchmark = list(stock_prices), list(benchmark_prices)
    if len(stock) != len(benchmark) or len(stock) < 2:
        raise ValueError('Need equally sized aligned price series with at least two points')
    if not math.isfinite(beta) or any(not math.isfinite(p) or p <= 0 for p in stock + benchmark):
        raise ValueError('Finite beta and positive finite prices required')
    daily = [(s1 / s0 - 1) - beta * (b1 / b0 - 1)
             for s0, s1, b0, b1 in zip(stock, stock[1:], benchmark, benchmark[1:])]
    return {'daily_abnormal_returns': daily, 'car': sum(daily), 'beta': beta}


def walk_forward(rows: Iterable[Observation], *, min_train: int = 30, test_size: int = 10, embargo_seconds: float = 0) -> list[dict]:
    """Expanding chronological splits; each test block uses a frozen train snapshot.

    Training labels must have matured strictly before block start minus embargo.
    Event timestamps shared across rows always stay in the same test block.
    Any preprocessing and hyperparameter tuning must be fitted on train only.
    """
    from datetime import timedelta
    if min_train < 1 or test_size < 1 or embargo_seconds < 0:
        raise ValueError('Invalid split configuration')
    data = sorted(rows, key=lambda r: (r.event_at, r.event_id))
    for row in data:
        row.validate()
    if len({r.event_id for r in data}) != len(data):
        raise ValueError('Duplicate event IDs')
    folds, cursor = [], 0
    while cursor < len(data):
        cutoff = data[cursor].event_at - timedelta(seconds=embargo_seconds)
        train = [r for r in data[:cursor] if r.label_available_at < cutoff]
        end = min(cursor + test_size, len(data))
        while end < len(data) and data[end].event_at == data[end - 1].event_at:
            end += 1
        if len(train) >= min_train:
            folds.append({'train': tuple(train), 'test': tuple(data[cursor:end]), 'cutoff': cutoff})
        cursor = end
    return folds


def probability_bins(predictions: Iterable[tuple[float, bool]], *, bins: int = 5, min_samples: int = 30) -> list[dict]:
    """Out-of-sample reliability table with Wilson 95% intervals and abstention.

    Inputs must be independent held-out forecasts paired with matured outcomes.
    Counts are observations, not a claim that correlated events are independent.
    """
    import math
    if bins < 1 or min_samples < 1:
        raise ValueError('Positive bins and min_samples required')
    grouped = [[] for _ in range(bins)]
    for probability, outcome in predictions:
        if not math.isfinite(probability) or not 0 <= probability <= 1 or not isinstance(outcome, bool):
            raise ValueError('Probability in [0, 1] and boolean outcome required')
        grouped[min(int(probability * bins), bins - 1)].append((probability, outcome))
    result = []
    for i, group in enumerate(grouped):
        n = len(group)
        record = {'lower': i / bins, 'upper': (i + 1) / bins, 'count': n,
                  'status': 'sufficient' if n >= min_samples else 'insufficient_sample',
                  'mean_prediction': mean(p for p, _ in group) if n else None,
                  'empirical_probability': None, 'wilson_95': None}
        if n >= min_samples:
            p = sum(y for _, y in group) / n
            z = 1.959963984540054
            denominator = 1 + z*z/n
            centre = (p + z*z/(2*n)) / denominator
            half = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / denominator
            record.update(empirical_probability=p, wilson_95=(centre-half, centre+half))
        result.append(record)
    return result


def write_prediction(directory: Path, *, prediction_id: str, event_id: str, predicted_at: datetime,
                     model_version: str, data_snapshot_sha256: str, probability: float) -> Path:
    """Append-only local audit record using exclusive creation and content hash.

    Filesystem protection is not tamper-proof storage: production needs restricted
    append-only object storage, retention policy and externally anchored hashes.
    Outcomes belong in separate records; never overwrite a forecast after an event.
    """
    import math
    if not prediction_id or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in prediction_id):
        raise ValueError('Invalid prediction ID')
    if predicted_at.tzinfo is None or not math.isfinite(probability) or not 0 <= probability <= 1:
        raise ValueError('Invalid timestamp or probability')
    if len(data_snapshot_sha256) != 64 or any(c not in '0123456789abcdef' for c in data_snapshot_sha256):
        raise ValueError('Expected SHA-256 snapshot identifier')
    payload = {'schema_version': 1, 'prediction_id': prediction_id, 'event_id': event_id,
               'predicted_at': predicted_at.isoformat(), 'model_version': model_version,
               'data_snapshot_sha256': data_snapshot_sha256, 'probability': probability}
    canonical = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    envelope = {'payload': payload, 'sha256': hashlib.sha256(canonical.encode()).hexdigest()}
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f'{prediction_id}.json'
    with path.open('x', encoding='utf-8') as file:
        json.dump(envelope, file, sort_keys=True, indent=2)
    return path
