from jasmine_toolkit.operation.pointing_plan import PointingPlan
from enum import Enum
from jasmine_toolkit.utils.parameters import Parameters


class EnumPointingMode(Enum):
    FOUR_FOV_IN_ORBIT = 4
    SIX_FOV_IN_ORBIT = 6
    EIGHT_FOV_IN_ORBIT = 8

    @classmethod
    def get_names(cls):
        return [i.name for i in cls]

    @classmethod
    def get_values(cls):
        return [i.value for i in cls]


class PointingPlanFactory:
    def __init__(self, enum: EnumPointingMode):
        self.mode = enum
        self.parameters = Parameters.get_instance()
        self.grid = None
        self.observation_time = None

    def create(self):
        # TODO create PointingPlan object and return it.
        pointing_plan = PointingPlan()
        self.generate_grid()
        self.generate_observation_time()
        self.make_observation()
        return pointing_plan

    def generate_grid(self):
        # TODO
        #   calculate number of grids from size of observation area and grid separation
        #   grid separation is defined from gap between detectors.
        #   generate array with initial value = 0
        #   unit may be raDian (or degree) in celestial coordinate
        pass

    def generate_observation_time(self):
        # TODO
        #   generate time sequence by using mode and orbit information
        #   array component is [time, number_of_observation]
        pass

    def make_observation(self):
        # TODO
        #   define observation grid from the previous observation by using some algorithm.
        #   apply strategy pattern or etc. for flexibility of choice of algorithms.
        #   request position angle from attitude object.
        #   add number_of_observation observations (ra, dec, position_angle, time) to pointing_plan.
        pass
