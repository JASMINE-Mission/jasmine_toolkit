import math
import string
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
        pass

    @staticmethod
    def make_pointing_plan(freedom: EnumPointingFreedom, mode: EnumPointingMode,
                           initial_time: Time, duration: TimeDelta):
        satellite = Satellite(freedom, initial_time)
        ppf = PointingPlanFactory(mode, initial_time, duration)
        pointing_plan: PointingPlan = ppf.create(satellite)
        return pointing_plan

    @staticmethod
    def calc_statistics(tc: Time, mapping_result: list):
        # TODO  This is the program for calculate statistics of "data".
        """

        Args:
            tc:
            mapping_result:

        Returns:

        variables:
         matrix_a is matrix denoted by A defined in Heinrich Eichhorn and Warren
             G. Clay, Mon. Not. R. astr. Soc. (1974) 166, 425-432

        """
        gal: SkyCoord = SkyCoord(l=0.0 * u.rad, b=0.0 * u.rad,
                                 frame='galactic')
        lg = gal.barycentricmeanecliptic.lon.rad
        bg = gal.barycentricmeanecliptic.lat.rad
        statistical_result = []
        for i, j in product(range(len(mapping_result)),
                            range(len(mapping_result[0]))):
            matrix_a = np.ndarray((len(mapping_result[i][j]) * 2, 5))
            for k in range(len(mapping_result[i][j])):
                t = mapping_result[i][j][k][0]
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
            inv_parameter_dispersion = np.dot(matrix_a.T, matrix_a)
            if not np.linalg.det(inv_parameter_dispersion) == 0:
                dispersion = np.linalg.inv(inv_parameter_dispersion)
                statistical_result.append([int(i), int(j), dispersion[4][4],
                                          mapping_result[i][j][k][1]])
        return statistical_result


if __name__ == '__main__':
    m = Mapping()
    initial_time_0 = Time('2028-03-01T00:00:00', scale="tcb")
    duration_0 = TimeDelta(3 * u.yr)
    pointing_plan = m.make_pointing_plan(EnumPointingFreedom.POINTING_FIXED,
                                         EnumPointingMode.FOUR_FOV_IN_ORBIT,
                                         initial_time_0, duration_0)
    pointing_plan.save_plan('plan.csv')
    pointing_plan.save_grid('grid.csv')
    data = pointing_plan.get_grid()
    tc = initial_time_0 + duration_0 * 0.5
    ans = m.calc_statistics(tc, data)
    ans_nd = np.array(ans)
    np.savetxt("ans.csv", ans_nd, delimiter=',')
