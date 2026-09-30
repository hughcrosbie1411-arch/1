import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from quant import Observation, abnormal_returns, walk_forward, probability_bins, write_prediction

START = datetime(2025, 1, 1, tzinfo=timezone.utc)

class QuantTests(unittest.TestCase):
    def row(self, i, delay=1):
        t = START + timedelta(days=i)
        return Observation(str(i), t, t + timedelta(days=delay), .02, (('known', 1., t),))

    def test_market_adjusted_car(self):
        result = abnormal_returns([100, 110, 121], [100, 105, 110.25])
        self.assertAlmostEqual(result['car'], .1)
        with self.assertRaises(ValueError):
            abnormal_returns([100, 0], [100, 101])

    def test_future_feature_rejected(self):
        bad = Observation('x', START, START + timedelta(days=2), 1., (('late', 1., START + timedelta(seconds=1)),))
        with self.assertRaises(ValueError):
            walk_forward([bad])

    def test_unmatured_training_labels_purged(self):
        rows = [self.row(i, delay=4 if i == 1 else 1) for i in range(8)]
        folds = walk_forward(rows, min_train=1, test_size=1)
        for fold in folds:
            self.assertTrue(all(r.label_available_at < fold['cutoff'] for r in fold['train']))
            self.assertTrue(all(r.event_at >= fold['cutoff'] for r in fold['test']))
        fold = next(f for f in folds if f['test'][0].event_id == '4')
        self.assertNotIn('1', [r.event_id for r in fold['train']])

    def test_simultaneous_events_not_split(self):
        rows = [self.row(i) for i in range(6)]
        rows.append(Observation('same', rows[4].event_at, rows[4].label_available_at, .01, ()))
        folds = walk_forward(rows, min_train=1, test_size=1)
        test = next(f['test'] for f in folds if any(r.event_id == '4' for r in f['test']))
        self.assertEqual({r.event_id for r in test}, {'4', 'same'})

    def test_sample_gate_and_probability_one(self):
        table = probability_bins([(1., True)] * 30 + [(.1, False)], bins=5)
        self.assertEqual(table[0]['status'], 'insufficient_sample')
        self.assertIsNone(table[0]['empirical_probability'])
        self.assertEqual(table[-1]['empirical_probability'], 1.)
        self.assertLess(table[-1]['wilson_95'][0], 1.)

    def test_forecast_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            args = dict(prediction_id='p1', event_id='e1', predicted_at=START,
                        model_version='v1', data_snapshot_sha256='a'*64, probability=.6)
            path = write_prediction(Path(d), **args)
            original = path.read_bytes()
            with self.assertRaises(FileExistsError):
                write_prediction(Path(d), **{**args, 'probability': .9})
            self.assertEqual(path.read_bytes(), original)
            self.assertEqual(json.loads(original)['payload']['probability'], .6)

if __name__ == '__main__':
    unittest.main()
