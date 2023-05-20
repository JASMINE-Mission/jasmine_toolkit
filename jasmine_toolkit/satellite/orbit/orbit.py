import math

import astropy.coordinates
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time, TimeDelta
import numpy as np

from jasmine_toolkit.utils import parameter as p


class Orbit:
    """
    A class that represents the orbit of a satellite.This class is
    specialized for SSO (Sun Synchronous Orbit), but should have subclasses
    that can represent different trajectories. It assumes that the necessary
    orbital information can be obtained from parameters.py.
    """

    def __init__(self, initial_time: Time):
        """

        @param initial_time: Time at which the satellite first passes the
        phase 0 position.
        """
        self.__inclination = p.inclination  # in radian
        self.__ltan = p.ltan  # in hour
        self.__orbital_period = p.orbital_period  # in second
        self.__initial_time = initial_time
        self.__initial_orbit_vector_lon = astropy.coordinates.get_sun(
            initial_time).ra.to('rad') + (self.__ltan + 6.0 * u.h)  \
            * math.pi * u.rad / (12 * u.h)
        if self.__initial_orbit_vector_lon > 2.0 * math.pi * u.rad:
            self.__initial_orbit_vector_lon = self.__initial_orbit_vector_lon \
                                              - 2.0 * math.pi * u.rad
        self.__orbital_radius = p.EQUATORIAL_EARTH_RADIUS + p.orbital_altitude
        self.__cos_angle_max = math.cos(math.pi / 2 - p.earth_avoiding_angle +
                                        math.acos(p.EQUATORIAL_EARTH_RADIUS /
                                                  self.__orbital_radius))
        self.__target = SkyCoord(l=0.0 * u.deg, b=0.0 * u.deg, frame="galactic")

    def satellite_direction(self, time: Time) -> tuple:
        alpha = self._calc_alpha(time)
        delta = self._calc_delta()
        theta = self._calc_theta(time)
        satellite_dec = np.arcsin(np.sin(theta) * np.cos(delta))
        ra_y = -np.sin(alpha) * np.sin(delta) * np.sin(theta) + np.cos(
            alpha) * np.cos(theta)
        ra_x = -np.sin(theta) * np.sin(delta) * np.cos(alpha) - np.sin(
            alpha) * np.cos(theta)
        satellite_ra = math.atan2(ra_x, ra_y)
        return satellite_ra, satellite_dec

    def _calc_theta(self, time):
        dt = time - self.__initial_time
        phase = math.modf(dt.to('s') / self.__orbital_period)[0]
        theta = phase * 2.0 * math.pi * u.rad
        return theta

    def _calc_alpha(self, time):
        dt = time - self.__initial_time
        dt_angle = math.modf(dt.to('year').value)[0] * 2.0 * math.pi * u.rad
        if dt_angle < 0.0:
            dt_angle = dt_angle + 2.0 * math.pi * u.rad
        orbit_vector_lon = self.__initial_orbit_vector_lon + dt_angle
        if orbit_vector_lon >= 2.0 * math.pi * u.rad:
            orbit_vector_lon = orbit_vector_lon - 2.0 * math.pi * u.rad
        alpha = orbit_vector_lon
        return alpha

    def _calc_delta(self):
        orbit_vector_lat = (90 * u.deg - self.__inclination)
        delta = orbit_vector_lat.to('rad')
        return delta

    def next_observable_time(self, time: Time, dt: TimeDelta) -> Time:
        target_ra = self.__target.icrs.ra.to('rad').value
        target_dec = self.__target.icrs.dec.to('rad').value
        sun_ra = astropy.coordinates.get_sun(time).ra.to('rad').value
        sun_dec = astropy.coordinates.get_sun(time).dec.to('rad').value
        cos_theta = math.cos(sun_dec) * math.cos(target_dec) \
                    * math.cos(sun_ra - target_ra) \
                    + math.sin(sun_dec) * math.sin(target_dec)
        while cos_theta * cos_theta > 0.5:
            sun_ra = astropy.coordinates.get_sun(time).ra.to('rad').value
            sun_dec = astropy.coordinates.get_sun(time).dec.to('rad').value
            cos_theta = math.cos(sun_dec) * math.cos(target_dec) \
                * math.cos(sun_ra - target_ra) \
                + math.sin(sun_dec) * math.sin(target_dec)
            time = time + TimeDelta(1 * u.d)
        while not self.is_observable(time, self.__target):
            time = time + dt
        return time

    def is_observable(self, time: Time, pointing: SkyCoord) -> bool:
        # TODO
        #   The method will be moved to another class. Need class names.
        sat_ra, sat_dec = self.satellite_direction(time)
        p_ra = pointing.icrs.ra.to('rad').value
        p_dec = pointing.icrs.dec.to('rad').value
        inner_product_of_p_and_sat = np.cos(sat_ra) * np.cos(
            p_ra) * np.cos(sat_dec) * np.cos(p_dec) \
            + np.cos(sat_dec) * np.cos(
            p_dec) * np.sin(sat_ra) * np.sin(p_ra) \
            + np.sin(sat_dec) * np.sin(p_dec)
        if inner_product_of_p_and_sat > self.__cos_angle_max:
            return True
        else:
            return False
