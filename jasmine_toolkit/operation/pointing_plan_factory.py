from jasmine_toolkit.operation.pointing_plan import PointingPlan
from jasmine_toolkit.utils.parameters import Parameters
from jasmine_toolkit.satellite.satellite import Satellite
from jasmine_toolkit.operation.pointing_mode import EnumPointingMode


class PointingPlanFactory:
    def __init__(self, enum: EnumPointingMode):
        self.__mode = enum
        self.__parameters = Parameters.get_instance()
        self.__grid = None
        self.__observation_time = None
        self.__satellite = None

    @property
    def create(self, satellite: Satellite):
        """
        Create PointingPlan object, set observation entries, and return it.
        Returns: PointingPlan object

        """
        # TODO Fix parameters needed within the function.
        self.__satellite = satellite
        pointing_plan = PointingPlan()
        self.generate_grid()
        self.find_next_pointing()
        self.generate_observation_time()
        self.get_position_angle()
        self.make_observation()
        return pointing_plan

    def generate_grid(self):
        # TODO
        #   calculate number of grids from size of observation area and grid separation
        #   grid separation is defined from gap between detectors.
        #   generate array with initial value = 0
        #   unit may be raDian (or degree) in celestial coordinate
        detector_gap = self.__parameters.detector_separation_x \
                       - self.__parameters.detector_format_x * self.__parameters.pixel_size
        gap_on_the_sky = detector_gap / self.__parameters.effective_focal_length
        print(gap_on_the_sky)

    def find_next_pointing(self):
        # TODO
        #   Determine next pointing by using some algorithm.
        #   This function may be abstract and function body is better to be implemented in child class.
        pass

    def generate_observation_time(self):
        # TODO
        #   generate time sequence by using mode and orbit information
        #   array component is [time, number_of_observation]
        pass

    def get_position_angle(self):
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
