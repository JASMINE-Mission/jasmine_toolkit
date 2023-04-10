import math
from itertools import product

import astropy.units as u
import numpy as np
from astropy.coordinates import get_sun, SkyCoord
from astropy.time import Time, TimeDelta

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
        pointing_plan.save_plan('plan.csv')
        pointing_plan.save_grid('grid.csv')
        self.__data = pointing_plan.get_grid()

    def calc_statistics(self, tc: Time):
        # TODO  This is the program for calculate statistics of "data".
        gal: SkyCoord = SkyCoord(l=0.0 * u.rad, b=0.0 * u.rad, frame='galactic')
        lg = gal.barycentricmeanecliptic.lon.rad
        bg = gal.barycentricmeanecliptic.lat.rad
        answer = []
        for i, j in product(range(len(self.__data)),
                            range(len(self.__data[0]))):
            matrix_a = np.ndarray((len(self.__data[i][j]) * 2, 5))
            for k in range(len(self.__data[i][j])):
                t = self.__data[i][j][k][0]
                t0 = (t - tc).to('yr').value
                sun: SkyCoord = get_sun(t)
                ls = sun.geocentricmeanecliptic.lon.rad
                matrix_a[2 * k][0] = 1
                matrix_a[2 * k][1] = 0
                matrix_a[2 * k][2] = t0
                matrix_a[2 * k][3] = 0
                matrix_a[2 * k][4] = math.sin(lg - ls)
                matrix_a[2 * k + 1][0] = 0
                matrix_a[2 * k + 1][1] = 1
                matrix_a[2 * k + 1][2] = 0
                matrix_a[2 * k + 1][3] = t0
                matrix_a[2 * k + 1][4] = math.cos(lg - ls) * math.sin(bg)
            dispersion = np.linalg.inv(np.dot(matrix_a.T, matrix_a))
            answer.append([i, j, dispersion[4][4]])
        return answer


if __name__ == '__main__':
    m = Mapping()
    initial_time = Time('2028-01-01T00:00:00', scale="tcb")
    duration = TimeDelta(0.02 * u.d)
    m.run(EnumPointingFreedom.POINTING_FIXED,
          EnumPointingMode.FOUR_FOV_IN_ORBIT, initial_time, duration)
    tc = initial_time + duration * 0.5
    m.calc_statistics(tc)
