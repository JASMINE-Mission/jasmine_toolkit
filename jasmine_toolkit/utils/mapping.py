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

    def __init__(self, freedom: EnumPointingFreedom, mode: EnumPointingMode,
                 initial_time: Time, duration: TimeDelta):
        satellite = Satellite(freedom, initial_time)
        ppf = PointingPlanFactory(mode, initial_time, duration)
        pointing_plan: PointingPlan = ppf.create(satellite)
        self.__data = pointing_plan.get_array()
        self.calc_statistics()

    def calc_statistics(self):
        # TODO  This is the program for calculate statistics of "data".
        pass
