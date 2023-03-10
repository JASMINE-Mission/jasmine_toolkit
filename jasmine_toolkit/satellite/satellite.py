from astropy.time import Time
from jasmine_toolkit.satellite.attitude.attitude import Attitude
from jasmine_toolkit.satellite.orbit.orbit import Orbit
from jasmine_toolkit.operation.pointing_freedom import EnumPointingFreedom


class Satellite:
    def __init__(self, mode: EnumPointingFreedom, initial_time: Time):
        self.__orbit = Orbit(initial_time)
        self.__attitude = Attitude(mode)
