import dat_file_reader

class Hunter(object):
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.acceleration_threshhold = 1
        self.__nights = None

    def interesting_events(self):
        return [
            self._nights()[night_index]
            for night_index in range(3, len(self._nights()))
            if self._light_curve_acceleration(night_index) > self.acceleration_threshhold]

    def _light_curve_acceleration(self, night_index):
        last_last, last, this = nights[night_index-3:night_index]['normalized_magnitude']
        this_change = this - last
        last_change = last - last_last
        return this_change - last_change

    def _nights(self):
        if not self.__nights:
            self._set_nights()
        return self.__nights

    def _set_nights(self):
        self.__nights = []
        night = { 'observations': [], 'normalized_magnitude': 0 }
        last_observation = { 'day': 0 }

        for observation in self.raw_data:
            # TODO: put this in a config file
            if observation['day'] - last_observation['day'] > 9.0/24:
                self.__nights.append(night)
                night = { 'observations': [] }

            night['observations'].append(observation)
            last_observation = observation

if __name__ == '__main__':
    raw_data = dat_file_reader.DatFileReader('../data/shanensemail/KB160053.dat').observations()
    h = Hunter(raw_data=raw_data)
    h.interesting_events()
