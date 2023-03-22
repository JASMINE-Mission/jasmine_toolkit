import warnings
import erfa
from astropy.coordinates import SkyCoord
from astropy.time import Time
from jasmine_toolkit.operation.pointing_plan import PointingPlan
from jasmine_toolkit.utils.parameters import Parameters
from jasmine_toolkit.satellite.satellite import Satellite
from jasmine_toolkit.operation.pointing_mode import EnumPointingMode


class PointingPlanFactory:
    def __init__(self, enum: EnumPointingMode):
        """

        Args:
            enum: Number of field of views within the half orbit.

        An attribute grid is list because the elements are Time object. It should not be nd array because ndarray can
        only have number.
        JASMINE mission uses time after 2027. In that case, erfaWarning ERFA function "dtf2d" yielded 1 of "dubious
        year (Note 6)" occurs. warnings.warn('ERFA function "{}" yielded {}'.format(func_name, wmsg), For avoiding
        this, warnings.simplefilter('ignore', category=erfa.core.ErfaWarning) is needed.
        """
        self.__mode: EnumPointingMode = enum
        self.__parameters: Parameters = Parameters.get_instance()
        self.__observation_time: Time = None
        self.__satellite: Satellite = None

    def create(self, satellite: Satellite):
        """
        Create PointingPlan object, set observation entries, and return it.
        Returns: PointingPlan object

        """
        # TODO
        #   Do not change class attributes, but use local variable
        #   variable grid is mutable. Use local variable rather than member attributes.
        self.__satellite = satellite
        pointing_plan = PointingPlan()
        grid = self._generate_grid()
        self._find_next_pointing(grid)
        self._generate_observation_time()
        # self.get_position_angle()
        self._make_observation()
        return pointing_plan

    def _generate_grid(self) -> list[list[list]]:
        detector_gap = self.__parameters.detector_separation_x \
                       - self.__parameters.detector_format_x * self.__parameters.pixel_size
        gap_on_the_sky = detector_gap / self.__parameters.effective_focal_length
        l_min = self.__parameters.minimum_l
        l_max = self.__parameters.maximum_l
        b_min = self.__parameters.minimum_b
        b_max = self.__parameters.maximum_b
        n_l = int((l_max - l_min) / gap_on_the_sky) + 1
        n_b = int((b_max - b_min) / gap_on_the_sky) + 1
        return [[[] for i in range(n_b)] for j in range(n_l)]
        # usage self.__grid[l][b].append(Time('2028-01-01T10:00:00'))

    @staticmethod
    def _find_next_pointing(grid: list):
        # TODO
        #   This function may be abstract and function body is better to be implemented in child class.
        #   It may depend on Satellite class. Calculation of "gain" is role of satellite?
        #   callable etc.
        l0 = -1
        b0 = -1
        min_count = 100000
        n_l = len(grid)
        n_b = len(grid[0])
        for l in range(n_l):
            for b in range(n_b):
                if len(grid[l][b]) < min_count:
                    min_count = len(grid[l][b])
                    l0 = l
                    b0 = b
        return l0, b0

    def _generate_observation_time(self):
        # TODO
        #   generate time sequence by using mode and orbit information
        #   array component is [time, number_of_observation]
        #   separate method.
        #   Do not implements calculation logic in factory class.
        pass

    def _get_position_angle(self, pointing: SkyCoord, time: Time):
        # TODO
        #   consider when position angle is needed and implementation in this class is appropriate or not.
        return self.__satellite.get_position_angle(pointing, time)

    def _make_observation(self):
        # TODO
        #   define observation grid from the previous observation by using some algorithm.
        #   apply strategy pattern or etc. for flexibility of choice of algorithms.
        #   request position angle from attitude object.
        #   add number_of_observation observations (ra, dec, position_angle, time) to pointing_plan.
        pass

    def test_function(self):
        # self.__grid[2][3].append(Time('2028-01-01T10:00:00'))
        # self.__grid[0][0].append(Time('2028-01-01T10:00:00'))
        # self.__grid[1][0].append(Time('2028-01-01T10:00:00'))
        pass


if __name__ == "__main__":
    warnings.simplefilter('ignore', category=erfa.core.ErfaWarning)
    a = PointingPlanFactory(EnumPointingMode.FOUR_FOV_IN_ORBIT)
    print(type(a._generate_grid()))
    # a.test_function()
    # a._find_next_pointing()