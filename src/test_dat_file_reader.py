import unittest
import mock

import dat_file_reader

class DatFileReaderTestCase(unittest.TestCase):
    def setUp(self):
        self.dat_file_reader = dat_file_reader.DatFileReader('notafile')

    def test_observations(self):
        expected = [{'day': 1.0, 'magnitude': 12.0},{'day': 10.0, 'magnitude': 42.0}]

        with mock.patch('__builtin__.open', self._mock_file(), create=True):
            observations = list(self.dat_file_reader.observations())

        self.assertEquals(observations, expected)

    def _mock_file(self):
        return_value = """
            # ignore this line
            12 11 1
            42 11 10""".split("\n")
        m = mock.mock_open()
        m.return_value = return_value
        return m
