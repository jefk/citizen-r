import os
import itertools
import numpy

import dat_file_reader

class Hunter(object):
    def __init__(self, raw_data, event_name='UNK'):
        self.event_name = event_name
        self.raw_data = raw_data
        self.acceleration_threshhold = 1
        self.__nights = None

    def interesting_events(self):
        return []
        # return [
        #     self._nights()[night_index]
        #     for night_index in range(3, len(self._nights()))
        #     if self._light_curve_acceleration(night_index) > self.acceleration_threshhold]

    def print_summary_table(self):
        for i, night in enumerate(self._nights()):
            stuffs = [
                self.event_name,
                i,
                self._is_interesting(i),
                night['count'],
                night['start'],
                night['end'],
                '{0:.2f}'.format(night['normalized_magnitude']),
                ]
            print('\t'.join(str(stuff) for stuff in stuffs))

    def _is_interesting(self, night_index):
        this_night_mag = self._nights()[night_index]['normalized_magnitude']
        last_night_mag = self._nights()[night_index-1]['normalized_magnitude']
        slope = this_night_mag - last_night_mag
        # TODO put threshholds in config file
        return (
            self._nights()[night_index]['count'] > 4 and
            this_night_mag < -3 and
            last_night_mag < -1 and
            slope < -1
            )

    # TODO: use a separate class for chunking
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
            # TODO: put error limit config file
            if observation['error'] > 0.5:
                continue
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
    data_dir = '../data/shanensemail/'
    for f in os.listdir(data_dir):
        raw_data = dat_file_reader.DatFileReader(data_dir + f).observations()
        h = Hunter(raw_data=raw_data, event_name=f)
        h.print_summary_table()
