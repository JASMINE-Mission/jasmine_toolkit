from jasmine_toolkit.satellite.attitude import Attitude
from jasmine_toolkit.satellite.orbit.orbit import Orbit
from jasmine_toolkit.operation.pointing_freedom import EnumPointingFreedom


class Satellite:
    def __init__(self, mode: EnumPointingFreedom):
        self.orbit = Orbit()
        self.attitude = Attitude(mode)
