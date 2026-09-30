"""Empirical baseline evaluated with expanding point-in-time training sets.

Usage: python research/backtest.py observations.json
No observations are fabricated. Returns abstention when coverage is inadequate.
"""
from datetime import datetime
import json
from statistics import mean
import sys
from quant import Observation, walk_forward

def evaluate(rows, min_train=30, min_test=30):
    forecasts=[]
    for fold in walk_forward(rows,min_train=min_train,test_size=1):
        labels=[r.label for r in fold['train']]
        expected=mean(labels)
        probability=mean(float(v>0) for v in labels)
        for row in fold['test']:
            forecasts.append({'event_id':row.event_id,'predicted_at':row.event_at.isoformat(),
                              'expected_abnormal_return':expected,'probability_positive':probability,
                              'actual':row.label,'training_count':len(labels)})
    n=len(forecasts)
    if n<min_test:
        return {'status':'insufficient_sample','heldout_count':n,'required_heldout':min_test,
                'metrics':None,'forecasts':forecasts,'model':'unconditional_empirical_baseline'}
    return {'status':'research_only','heldout_count':n,'model':'unconditional_empirical_baseline',
            'metrics':{'mae':mean(abs(r['actual']-r['expected_abnormal_return']) for r in forecasts),
                       'brier_positive':mean((r['probability_positive']-float(r['actual']>0))**2 for r in forecasts)},
            'forecasts':forecasts,
            'limitations':['No execution costs or strategy simulation','No issuer-clustered uncertainty estimate',
                           'No challenger comparison or untouched holdout; no production promotion']}

if __name__=='__main__':
    raw=json.load(open(sys.argv[1]))
    parse=lambda s:datetime.fromisoformat(s.replace('Z','+00:00'))
    rows=[Observation(r['event_id'],parse(r['event_at']),parse(r['label_available_at']),r['label'],
                      tuple((f['name'],f['value'],parse(f['available_at'])) for f in r['features'])) for r in raw]
    print(json.dumps(evaluate(rows),indent=2))
