"""Validate a Longbridge candles export and write a reproducible local snapshot.

Usage: python ingestion/import_longbridge.py NKE.US exported-candles.json
The website cannot reuse ChatGPT connector credentials. This is an explicit
bridge for authorized connector exports; no trading or account tools are used.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path

def normalize(symbol, raw):
    if symbol not in {'NKE.US', 'SPY.US'}:
        raise ValueError('This first app supports NKE.US and SPY.US only')
    if not isinstance(raw, list) or not raw:
        raise ValueError('Expected nonempty candle array')
    seen = set()
    for row in raw:
        stamp = datetime.fromisoformat(row['timestamp'].replace('Z', '+00:00'))
        if stamp.tzinfo is None or row['timestamp'] in seen:
            raise ValueError('Unique timezone-aware candle timestamps required')
        seen.add(row['timestamp'])
        prices = [float(row[k]) for k in ('open', 'high', 'low', 'close')]
        if any(not math.isfinite(v) or v <= 0 for v in prices):
            raise ValueError('Invalid OHLC')
        o,h,l,c = prices
        if l > min(o,c) or h < max(o,c) or l > h:
            raise ValueError('Inconsistent OHLC')
        if not math.isfinite(float(row['volume'])) or float(row['volume']) < 0:
            raise ValueError('Invalid volume')
    return {'source':'Longbridge', 'symbol':symbol,
            'ingested_at':datetime.now(timezone.utc).isoformat(),
            'adjustment':'forward', 'snapshot_sha256':hashlib.sha256(json.dumps(raw,sort_keys=True).encode()).hexdigest(),
            'candles':sorted(raw,key=lambda r:r['timestamp'])}

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('symbol',choices=['NKE.US','SPY.US'])
    parser.add_argument('export',type=Path)
    args=parser.parse_args()
    result=normalize(args.symbol,json.loads(args.export.read_text()))
    dest=Path(__file__).resolve().parents[1]/'data'/f'{args.symbol}.json'
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(result))
    print(f'Imported {len(result["candles"])} candles for {args.symbol}')
