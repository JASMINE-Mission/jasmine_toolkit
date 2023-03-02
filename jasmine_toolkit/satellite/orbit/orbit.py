import math
import warnings

import astropy.coordinates
from astropy.time import Time
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
        self.__initial_orbit_vector_lon = astropy.coordinates.get_sun(initial_time).ra.to('deg').value + (self.__ltan
                                                                                                          - 6.0) * 15.0
        self.__orbital_radius = self.__parameters.EQUATORIAL_EARTH_RADIUS + self.__parameters.orbital_altitude

    def satellite_position(self, time: Time) -> float:
        dt = time - self.__initial_time
        phase = math.modf(dt.sec / self.__orbital_period)[0]
        orbit_vector_lon = self.__initial_orbit_vector_lon + math.modf(dt.to('year').value)[0] * 360
        if orbit_vector_lon >= 360:
            orbit_vector_lon = orbit_vector_lon - 360.0
        orbit_vector_lat = (90 * u.deg - self.__inclination * u.rad)
        print(str(orbit_vector_lon * u.deg) + "," + str((orbit_vector_lat.to('deg'))) + "," +
              str((phase * 360) * u.deg))
        return 0.0

    def next_observable_time(self, time: Time) -> Time:
        pass

    def observable_p(self, time: Time) -> bool:
        pass


if __name__ == '__main__':
    warnings.simplefilter('ignore', category=erfa.core.ErfaWarning)
    # times = ['2028-03-01T00:00:00', '2028-04-01T00:00:00', '2028-05-01T00:00:00', '2028-06-01T00:00:00',
    #          '2028-07-01T00:00:00', '2028-08-01T00:00:00', '2028-09-01T00:00:00', '2028-10-01T00:00:00',
    #          '2028-11-01T00:00:00', '2028-12-01T00:00:00', '2029-01-01T00:00:00', '2029-02-01T00:00:00',
    #          '2029-03-01T00:00:00', '2029-04-01T00:00:00', '2029-05-01T00:00:00', '2029-06-01T00:00:00']
    times = ['2028-03-01T00:00:00', '2028-03-01T00:10:00', '2028-03-01T00:20:00', '2028-03-01T00:30:00',
             '2028-03-01T00:40:00', '2028-03-01T00:50:00', '2028-03-01T01:00:00', '2028-03-01T01:10:00',
             '2028-03-01T01:20:00', '2028-03-01T01:30:00', '2028-03-01T01:40:00', '2028-03-01T01:50:00']
    t = Time(times, format='isot', scale='utc')
    orbit = Orbit(t[0])
    for i in range(0, len(times)):

        orbit.satellite_position(t[i])
    print("Hello")
