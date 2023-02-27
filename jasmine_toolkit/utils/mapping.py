from jasmine_toolkit.operation.pointing_plan import PointingPlan
from jasmine_toolkit.operation.pointing_plan_factory import PointingPlanFactory
from jasmine_toolkit.satellite.satellite import Satellite
from jasmine_toolkit.utils.parameters import Parameters
from operation.pointing_freedom import EnumPointingFreedom
from operation.pointing_mode import EnumPointingMode


class Mapping:
    """
    client class for generate mapping strategy.
    """
    def __init__(self, freedom: EnumPointingFreedom, mode: EnumPointingMode):
        satellite = Satellite(freedom)
        pointing_plan_factory = PointingPlanFactory(mode)
        pointing_plan: PointingPlan = pointing_plan_factory.create(satellite)
        self.data = pointing_plan.get_array()
        self.calc_statistics()

    def calc_statistics(self):
        # TODO  This is the program for calculate statistics of "data".
        pass


if __name__ == '__main__':
    mapping_freedom = EnumPointingFreedom.POINTING_FIXED
    mapping_mode = EnumPointingMode.FOUR_FOV_IN_ORBIT
    mapping = Mapping(mapping_freedom, mapping_mode)
    print("Hello")
