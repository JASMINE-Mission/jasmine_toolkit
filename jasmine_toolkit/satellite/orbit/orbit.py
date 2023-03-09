import math
import warnings

import astropy.coordinates
from astropy.coordinates import SkyCoord
from astropy.time import Time, TimeDelta
import astropy.units as u
import erfa

from jasmine_toolkit.utils.parameters import Parameters


class Orbit:
    """
    A class that represents the orbit of a satellite.This class is specialized for SSO (Sun Synchronous Orbit), but
    should have subclasses that can represent different trajectories. It assumes that the necessary orbital information
    can be obtained from parameters.py.
    """

    def __init__(self, initial_time: Time):
        """

        @param initial_time: Time at which the satellite first passes the phase 0 position.
        """
        self.__parameters: Parameters = Parameters.get_instance()
        self.__inclination = self.__parameters.inclination  # in radian
        self.__ltan = self.__parameters.ltan  # in hour
        self.__orbital_period = self.__parameters.orbital_period  # in second
        self.__initial_time = initial_time
        self.__initial_orbit_vector_lon = astropy.coordinates.get_sun(initial_time).ra.to('rad').value \
                                          + (self.__ltan + 6.0) * math.pi / 12
        if self.__initial_orbit_vector_lon > 2.0 * math.pi:
            self.__initial_orbit_vector_lon = self.__initial_orbit_vector_lon - 2.0 * math.pi
        self.__orbital_radius = self.__parameters.EQUATORIAL_EARTH_RADIUS + self.__parameters.orbital_altitude
        self.__cos_angle_max = math.cos(math.pi / 2 - self.__parameters.earth_avoiding_angle
                                        + math.acos(self.__parameters.EQUATORIAL_EARTH_RADIUS / self.__orbital_radius))
        self.__galactic_center = SkyCoord(l=0.0 * u.deg, b=0.0 * u.deg, frame="galactic")

    def satellite_direction(self, time: Time) -> tuple:
        dt = time - self.__initial_time
        phase = math.modf(dt.sec / self.__orbital_period)[0]
        theta = phase * 2.0 * math.pi
        dt_angle = math.modf(dt.to('year').value)[0] * 2.0 * math.pi
        if dt_angle < 0.0:
            dt_angle = dt_angle + 2.0 * math.pi
        orbit_vector_lon = self.__initial_orbit_vector_lon + dt_angle
        if orbit_vector_lon >= 2.0 * math.pi:
            orbit_vector_lon = orbit_vector_lon - 2.0 * math.pi
        orbit_vector_lat = (90 * u.deg - self.__inclination * u.rad)
        delta = orbit_vector_lat.to('rad').value
        alpha = orbit_vector_lon
        # print("orbit: lon: " + str(orbit_vector_lon * 180 / math.pi) + ", lat: " + str(orbit_vector_lat))
        sin_satellite_dec = math.sin(theta) * math.cos(delta)
        satellite_dec = math.asin(sin_satellite_dec)
        ra_y = -math.sin(alpha) * math.sin(delta) * math.sin(theta) + math.cos(alpha) * math.cos(theta)
        ra_x = -math.sin(theta) * math.sin(delta) * math.cos(alpha) - math.sin(alpha) * math.cos(theta)
        satellite_ra = math.atan2(ra_x, ra_y)
        return satellite_ra, satellite_dec

    def next_observable_time(self, time: Time, dt: TimeDelta) -> Time:
        while not self.observable_p(time, self.__galactic_center):
            time = time + dt
        return time

    def observable_p(self, time: Time, pointing: SkyCoord) -> bool:
        sat_ra, sat_dec = self.satellite_direction(time)
        p_ra = pointing.icrs.ra.to('rad').value
        p_dec = pointing.icrs.dec.to('rad').value
        inner_product_of_p_and_sat = math.cos(sat_ra) * math.cos(p_ra) * math.cos(sat_dec) * math.cos(p_dec)\
                                     + math.cos(sat_dec) * math.cos(p_dec) * math.sin(sat_ra) * math.sin(p_ra)\
                                     + math.sin(sat_dec) * math.sin(p_dec)
        if inner_product_of_p_and_sat > self.__cos_angle_max:
            return True
        else:
            return False


if __name__ == '__main__':
    warnings.simplefilter('ignore', category=erfa.core.ErfaWarning)
    t0 = Time('2028-01-01T00:00:00')
    dt = TimeDelta(60.0 * u.second)
    t1 = Time('2028-01-01T00:20:00')
    orbit = Orbit(t0)
    print(orbit.next_observable_time(t0, dt))
    print(orbit.observable_p(t1, SkyCoord(l=0.0 * u.deg, b=0.0 * u.deg, frame='galactic')))
    print(orbit.next_observable_time(t1, dt))