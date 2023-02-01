from jasmine_toolkit.operation.pointing_plan import PointingPlan
from jasmine_toolkit.operation.pointing_plan_factory import PointingPlanFactory, EnumPointingMode
from jasmine_toolkit.satellite.satellite import Satellite
from jasmine_toolkit.utils.parameters import Parameters


class Mapping:
    """
    client class for generate mapping strategy.
    """
    def __init__(self):
        satellite = Satellite()
        enum = EnumPointingMode.FOUR_FOV_IN_ORBIT
        pointing_plan_factory = PointingPlanFactory(enum)
        pointing_plan: PointingPlan = pointing_plan_factory.create
        self.data = pointing_plan.get_array()
        self.calc_statistics()

    def calc_statistics(self):
        # TODO  This is the program for calculate statistics of observation
        pass


if __name__ == '__main__':
    # mapping = Mapping()
    Parameters.get_instance().average_quantum_efficiency()
