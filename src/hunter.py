import itertools
import numpy

import dat_file_reader

class Hunter(object):
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.acceleration_threshhold = 1
        self.__nights = None

    def interesting_events(self):
        return []
        # return [
        #     self._nights()[night_index]
        #     for night_index in range(3, len(self._nights()))
        #     if self._light_curve_acceleration(night_index) > self.acceleration_threshhold]

    def summarize(self):
        for i, night in enumerate(self._nights()):
            magnitudes = [round(mag,1) for mag in night['normalized_magnitudes']]
            stuffs = [i,
                night['count'],
                night['start'],
                night['end'],
                night['normalized_magnitude']]
            print('\t'.join(str(stuff) for stuff in stuffs + magnitudes))

    def _nights(self):
        if not self.__nights:
            self._set_nights()
        return self.__nights

    def _set_nights(self):
        self.__nights = []
        self._set_stats()
        night = { 'observations': [] }
        last_observation = None

        for observation in self.raw_data:
            # TODO: put chunk gap in a config file
            if last_observation and observation['day'] - last_observation['day'] > 9.0/24:
                self.__nights.append(self._normalize(night))
                night = { 'observations': [] }

            night['observations'].append(observation)
            last_observation = observation

        self.__nights.append(self._normalize(night))

    def _normalize(self, night):
        observations = night['observations']
        night['count'] = len(observations)
        night['start'] = round(observations[0]['day'], 1)
        night['end'] = round(observations[-1]['day'], 1)
        night['normalized_magnitudes'] = [
            (o['magnitude'] - self._magnitude_mean) / self._magnitude_standard_deviation
            for o in observations ]
        night['normalized_magnitude'] = numpy.mean(night['normalized_magnitudes'])
        return night

    def _set_stats(self):
        all_magnitudes = [ o['magnitude'] for o in self.raw_data ]
        self._magnitude_mean = numpy.mean(all_magnitudes)
        self._magnitude_standard_deviation = numpy.std(all_magnitudes)


if __name__ == '__main__':
    raw_data = dat_file_reader.DatFileReader('../data/shanensemail/KB160053.dat').observations()
    h = Hunter(raw_data=raw_data)
    h.summarize()
