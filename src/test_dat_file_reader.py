import unittest

class DatFileReaderTestCase(unittest.TestCase):
    def setUp(self):
        self.dat_file_reader = DatFileReader('test_file.dat')

    def test_observations(self):
        expected = [{'day': 1, 'magnitude': 12},{'day': 10, 'magnitude': 42}]
        observations = list(self.dat_file_reader.observations())
        self.assertEquals(observations, expected)
