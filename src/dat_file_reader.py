class DatFileReader:
    def __init__(self, path):
        self.path = path

    def observations(self):
        return [
            self._line_data(line)
            for line in open(self.path)
            if self._valid_line(line)
            ]

    def _line_data(self, line):
        spline = line.strip().split()
        return {
            'day': float(spline[2]),
            'magnitude': float(spline[0]),
            }

    def _valid_line(self, line):
        spline = line.strip().split()
        return spline and spline[0] != '#'
