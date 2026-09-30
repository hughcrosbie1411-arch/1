import unittest
from datetime import datetime,timedelta,timezone
from backtest import evaluate
from quant import Observation

class BacktestTests(unittest.TestCase):
    def test_future_extreme_outcome_cannot_change_earlier_forecast(self):
        start=datetime(2020,1,1,tzinfo=timezone.utc)
        def make(last):
            return [Observation(str(i),start+timedelta(days=i*2),start+timedelta(days=i*2+1),last if i==9 else .01,()) for i in range(10)]
        a=evaluate(make(-1),min_train=3,min_test=3)
        b=evaluate(make(1),min_train=3,min_test=3)
        self.assertEqual([r['expected_abnormal_return'] for r in a['forecasts']], [r['expected_abnormal_return'] for r in b['forecasts']])
        self.assertAlmostEqual(a['forecasts'][-1]['expected_abnormal_return'],.01)
    def test_small_sample_returns_no_metrics(self):
        result=evaluate([])
        self.assertEqual(result['status'],'insufficient_sample')
        self.assertIsNone(result['metrics'])

if __name__=='__main__':unittest.main()
