import time

from astropy.coordinates import get_sun
from astropy.time import Time, TimeDelta
import astropy.units as u
from jasmine_toolkit.operation.pointing_freedom import EnumPointingFreedom
from jasmine_toolkit.operation.pointing_mode import EnumPointingMode
from jasmine_toolkit.operation.pointing_plan import PointingPlan
from jasmine_toolkit.operation.pointing_plan_factory import PointingPlanFactory
from jasmine_toolkit.satellite.satellite import Satellite


class Mapping:
    """
    client class for generate mapping strategy.
    """

    def __init__(self):
        self.__data = []

    def run(self, freedom: EnumPointingFreedom, mode: EnumPointingMode,
            initial_time: Time, duration: TimeDelta):
        satellite = Satellite(freedom, initial_time)
        ppf = PointingPlanFactory(mode, initial_time, duration)
        pointing_plan: PointingPlan = ppf.create(satellite)
        self.__data = pointing_plan.get_array()

    def calc_statistics(self, tc: Time):
        # TODO  This is the program for calculate statistics of "data".
        for i in range(len(self.__data)):
            for j in range(len(self.__data[0])):
                for k in range(len(self.__data[i][j])):
                    t = self.__data[i][j][k][0]
                    print(str((t - tc).to('yr').value) + "," + str(get_sun(t)))


if __name__ == '__main__':
    m = Mapping()
    # m.run(EnumPointingFreedom.POINTING_FIXED,
    #       EnumPointingMode.FOUR_FOV_IN_ORBIT,
    #       Time('2028-01-01T00:00:00', scale="tcb"),
    #       TimeDelta(0.02 * u.d))
    a = [[[]]]
    t = Time('2020-01-01T00:00:00')
    dt = TimeDelta(0.1 * u.yr)
    for i in range(30):
        a[0][0].append([t, 1])
        t = t + dt
    m._Mapping__data = a
    print(len(a[0][0]) - 1)
    duration = a[0][0][len(a[0][0]) - 1][0] - a[0][0][0][0]
    tc = a[0][0][0][0] + duration * 0.5
    m.calc_statistics(tc)
