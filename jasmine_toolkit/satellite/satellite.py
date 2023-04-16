from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.time import Time, TimeDelta
from jasmine_toolkit.satellite.attitude.attitude import Attitude
from jasmine_toolkit.satellite.orbit.orbit import Orbit
from jasmine_toolkit.operation.pointing_freedom import EnumPointingFreedom


class Satellite:
    def __init__(self, mode: EnumPointingFreedom, initial_time: Time):
        self.__orbit = Orbit(initial_time)
        self.__attitude = Attitude(mode)
        self.__target = SkyCoord(l=0.0 * u.deg, b=0.0 * u.deg,
                                 frame="galactic")

    def get_position_angle(self, pointing: SkyCoord, time: Time):
        return self.__attitude.get_position_angle(pointing, time)

    def next_observable_time(self, time: Time, dt: TimeDelta) -> Time:
        return self.__orbit.next_observable_time(time, dt)

    def observation_count(self, t: Time, dt: TimeDelta, max_obs: int):
        n: int = 0
        while self.__orbit.is_observable(t, self.__target) and n < max_obs:
            t = t + dt
            n = n + 1
        return n
