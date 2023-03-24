import math

import numpy as np
from astropy.time import Time
from numpy import ndarray

from jasmine_toolkit.operation.pointing_freedom import EnumPointingFreedom
from jasmine_toolkit.operation.pointing_mode import EnumPointingMode
from jasmine_toolkit.operation.pointing_plan import PointingPlan
from jasmine_toolkit.operation.pointing_plan_factory import PointingPlanFactory
from jasmine_toolkit.satellite.satellite import Satellite


class Mapping:
    """
    client class for generate mapping strategy.
    """

    def __init__(self, freedom: EnumPointingFreedom, mode: EnumPointingMode,
                 initial_time: Time):
        satellite = Satellite(freedom, initial_time)
        pointing_plan_factory = PointingPlanFactory(mode, initial_time)
        pointing_plan: PointingPlan = pointing_plan_factory.create(satellite)
        self.__data = pointing_plan.get_array()
        self.calc_statistics()

    def calc_statistics(self):
        # TODO  This is the program for calculate statistics of "data".
        pass

    @staticmethod
    def included_p(polygon: ndarray, target: ndarray):
        target = np.append(target, 0)
        z = np.zeros((len(polygon), 1))
        polygon = np.append(polygon, z, axis=1)
        win = 0
        for i in range(len(polygon)):
            j = i + 1
            if j > len(polygon) - 1:
                j = 0
            a0 = polygon[i] - target
            a1 = polygon[j] - target
            outer = np.cross(a0, a1) / (
                        np.linalg.norm(a0, ord=2) * np.linalg.norm(a1, ord=2))
            win = win + math.asin(outer[2])
        if 0.1 > win > -0.1:
            return False
        else:
            return True


if __name__ == '__main__':
    mapping = Mapping(EnumPointingFreedom.POINTING_FIXED,
                      EnumPointingMode.FOUR_FOV_IN_ORBIT,
                      Time('2028-01-01T00:00:00', scale="tcb"))
