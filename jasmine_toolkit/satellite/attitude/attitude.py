import datetime

import astropy
import astropy.units as u
from astropy.coordinates import get_sun

from jasmine_toolkit.satellite.orbit.orbit import Orbit
from jasmine_toolkit.utils.parameters import Parameters


class Attitude:
    def __init__(self, orbit: Orbit):
        self.orbit = orbit
        self.parameters = Parameters.get_instance()

    def get_position_angle(self):
        return 1.0


if __name__ == '__main__':
    tz = astropy.time.TimezoneInfo(9 * u.hour)  # 時間帯を決める。
    toki = datetime.datetime(2019, 5, 16, 17, 0, 0, tzinfo=tz)
    toki = astropy.time.Time(toki)
    taiyou = get_sun(toki)
    print(taiyou)