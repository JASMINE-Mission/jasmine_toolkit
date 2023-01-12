from jasmine_toolkit.operation.pointing_plan import PointingPlan
from jasmine_toolkit.operation.pointing_plan_factory import PointingPlanFactory
from jasmine_toolkit.satellite.satellite import Satellite


class Mapping:
    """
    client class for generate mapping strategy.
    """
    def __init__(self):
        satellite = Satellite()
        pointing_plan_factory = PointingPlanFactory()
        pointing_plan = pointing_plan_factory.create()


if __name__ == '__main__':
    mapping = Mapping()
