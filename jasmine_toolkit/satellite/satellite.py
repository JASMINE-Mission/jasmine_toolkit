from jasmine_toolkit.satellite.attitude import Attitude
from jasmine_toolkit.satellite.orbit.orbit import Orbit


class Satellite:
    def __init__(self):
        self.orbit = Orbit()
        self.attitude = Attitude(self.orbit)
