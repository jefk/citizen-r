import dat_file_reader

class Hunter(object):
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.__nights = None

    def interesting_events(self):
        for night_index in irange(2, len(self._nights())):
            acceleration = self.magnitude_acceleration(night_index)
            if acceleration > self.acceleration_threshhold:
                print self.summary(night_index)

    def _nights(self):
        if not self.__nights:
            self._set_nights()
        return self.__nights

    def _set_nights(self):
        self.__nights = []
        night = { 'observations': [] }
        last_observation = { 'day': 0 }

        for observation in self.raw_data:
            # TODO: put this in a config file
            if observation['day'] - last_observation['day'] > 6.0/24:
                self.__nights.append(night)
                night = { 'observations': [] }

            night['observations'].append(observation)
            last_observation = observation

if __name__ == '__main__':
    raw_data = dat_file_reader.DatFileReader('data/KB160053.dat').observations()
    h = Hunter(raw_data=raw_data)
    h.interesting_events()
