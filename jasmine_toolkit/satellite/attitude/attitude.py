import datetime
import math

import astropy
import astropy.units as u
from astropy.coordinates import get_sun, SkyCoord
from astropy.time import Time

from jasmine_toolkit.satellite.orbit.orbit import Orbit
from jasmine_toolkit.utils.parameters import Parameters


class Attitude:
    def __init__(self, orbit: Orbit):
        self.orbit = orbit
        self.parameters = Parameters.get_instance()
        self.galactic_center = SkyCoord(0.0 * u.deg, 0.0 * u.deg, frame='galactic')

    def get_position_angle(self, ra: float, dec: float, time: Time) -> float:
        sun = get_sun(time)
        xsun = math.cos(sun.dec.to('rad').value) * math.cos(sun.ra.to('rad').value)
        ysun = math.cos(sun.dec.to('rad').value) * math.sin(sun.ra.to('rad').value)
        zsun = math.sin(sun.dec.to('rad').value)
        print("ra:" + str(sun.ra) + "," + str(sun.dec))
        print("xyz:"+str(xsun) + "," + str(ysun) + "," + str(zsun))
        print(self.galactic_center.icrs)
        return sun.dec


if __name__ == '__main__':
    tz = astropy.time.TimezoneInfo(9 * u.hour)  # 時間帯を決める。
    toki = datetime.datetime(2019, 5, 16, 17, 0, 0, tzinfo=tz)
    toki = Time(toki)
    taiyou = get_sun(toki)
    print(taiyou)
    attitude = Attitude(Orbit())
    print(attitude.get_position_angle(0., 0., toki))

    print(attitude.galactic_center.icrs)
