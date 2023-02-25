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


class EnumPointingFreedom(Enum):
    POINTING_FIXED = 0
    POINTING_RANDOM = 1

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

    @property
    def create(self):
        """
        Create PointingPlan object, set observation entries, and return it.
        Returns: PointingPlan object

        """
        # TODO Fix parameters needed within the function.
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
        detector_gap = self.parameters.detector_separation_x \
                       - self.parameters.detector_format_x * self.parameters.pixel_size
        gap_on_the_sky = detector_gap / self.parameters.effective_focal_length
        print(gap_on_the_sky)

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


if __name__ == "__main__":
    a = PointingPlanFactory(EnumPointingMode.FOUR_FOV_IN_ORBIT)
    a.generate_grid()
