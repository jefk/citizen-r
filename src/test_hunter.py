import unittest
import mock

import hunter

class DatFileReaderTestCase(unittest.TestCase):
    def setUp(self):
        observations = [
            {'day': 1.0, 'magnitude': 12.0},
            {'day': 1.1, 'magnitude': 12.0},
            {'day': 10.0, 'magnitude': 42.0},]
        self.hunter = hunter.Hunter(raw_data=observations)

    def test_nights_count(self):
        self.assertEqual(len(self.hunter._nights()), 2)

    def test_night_normalization(self):
        normalized_magnitude = self.hunter._nights()[-1]['normalized_magnitude']
        self.assertAlmostEqual(normalized_magnitude, 1.41421356237)

    def test_interesting_events(self):
        self.assertEqual(len(self.hunter.interesting_events()), 0)
