import datetime
import math

from jasmine_toolkit.utils.parameters import Parameters


class Orbit:
    """
    A class that represents the orbit of a satellite.This class is specialized for SSO (Sun Synchronous Orbit), but
    should have subclasses that can represent different trajectories. It assumes that the necessary orbital information
    can be obtained from parameters.py.
    """
    def __init__(self, initial_time: datetime):
        """

        @param initial_time: Time at which the satellite first passes the phase 0 position.
        """
        self.__parameters: Parameters = Parameters.get_instance()
        self.__inclination = self.__parameters.inclination  # in radian
        self.__ltan = self.__parameters.ltan  # in hour
        self.__orbital_period = self.__parameters.orbital_period  # in second
        self.__initial_time = initial_time
        self.__orbital_radius = self.__parameters.EQUATORIAL_EARTH_RADIUS + self.__parameters.orbital_altitude

    def satellite_position(self, time: datetime):
        dt = (time - self.__initial_time).total_seconds()
        phase = math.modf(dt / self.__orbital_period)[0]
        pass

    def next_observable_time(self, time: datetime) -> datetime:
        pass


if __name__ == '__main__':
    orbit = Orbit(datetime.datetime.fromisoformat('2028-10-01T00:00:00'))
    orbit.satellite_position(datetime.datetime.fromisoformat('2029-05-01T00:00:00'))
    print("Hello")
