from jasmine_toolkit.utils.parameters import Parameters


class Orbit:
    def __init__(self):
        self.parameters: Parameters = Parameters.get_instance()
        self.inclination = self.parameters.inclination
        self.ltan = self.parameters.lo


