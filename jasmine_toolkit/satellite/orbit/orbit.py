from jasmine_toolkit.utils.parameters import Parameters


class Orbit:
    def __init__(self):
        self.__parameters: Parameters = Parameters.get_instance()
        self.__inclination = self.parameters.inclination
        self.__ltan = self.parameters.ltan


if __name__ == '__main__':
    orbit = Orbit()
    print("Hello")