import warnings
import erfa
from astropy.coordinates import SkyCoord
from astropy.time import Time, TimeDelta

from jasmine_toolkit.operation.pointing_freedom import EnumPointingFreedom
from jasmine_toolkit.operation.pointing_plan import PointingPlan
from jasmine_toolkit.utils.parameters import Parameters
from jasmine_toolkit.satellite.satellite import Satellite
from jasmine_toolkit.operation.pointing_mode import EnumPointingMode
import astropy.units as u


class PointingPlanFactory:
    def __init__(self, enum: EnumPointingMode, start: Time,
                 duration: TimeDelta = TimeDelta(3.0 * u.yr)):
        """

        Args:
            enum: Number of field of views within the half orbit.
            start: Time of start observation.
            duration: Mission duration, default value is 3 years.

        An attribute grid is list because the elements are Time object. It
        should not be nd array because ndarray can only have number.
        JASMINE mission uses time after 2027. In that case, erfaWarning ERFA
        function "dtf2d" yielded 1 of "dubious year (Note 6)" occurs.

        warnings.warn('ERFA function "{}" yielded {}'.format(func_name, wmsg),

        For avoiding this, the below is needed,

        warnings.simplefilter('ignore', category=erfa.core.ErfaWarning).
        """
        self.__mode: EnumPointingMode = enum
        self.__start: Time = start
        self.__end: Time = start + duration
        self.__observation_time: Time = None
        self.__satellite: Satellite = None
        self.__gap_on_the_sky = 0
        p: Parameters = Parameters.get_instance()
        self.__time_per_a_fov = (p.orbital_period * 0.5 + p.maneuver_time)\
                                / self.__mode.value
        self.__num_exposure_per_field = int(
            (self.__time_per_a_fov - p.maneuver_time) /
            (p.exposure_time + p.read_time))
        self.__l0 = 0
        self.__b0 = 0
        print(self.__time_per_a_fov)
        print(self.__num_exposure_per_field)

    def create(self, satellite: Satellite):
        """
        Create PointingPlan object, set observation entries, and return it.
        Returns: PointingPlan object

        """
        # TODO
        #   Do not change class attributes, but use local variable
        #   variable grid is mutable. Use local variable rather than member
        #   attributes.
        self.__satellite = satellite
        pointing_plan = PointingPlan()
        grid = self._generate_grid()
        t = self.__start
        while t < self.__end:
            pointing = self._find_next_pointing(grid)
            t = self._generate_observation_time(t)
            self._get_position_angle(pointing, t)
            grid = self._make_observation(t, pointing_plan, grid)
            t = t + TimeDelta(self.__time_per_a_fov * u.second)
            print(t)
        return pointing_plan

    def _generate_grid(self) -> list[list[list]]:
        """

        Returns: empty 3 dimensional list. The first and the second index
         denotes

        """
        p = Parameters.get_instance()
        detector_gap = p.detector_separation_x \
                       - p.detector_format_x * p.pixel_size
        self.__gap_on_the_sky = detector_gap / p.effective_focal_length
        l_min = p.minimum_l
        l_max = p.maximum_l
        b_min = p.minimum_b
        b_max = p.maximum_b
        n_l = int((l_max - l_min) / self.__gap_on_the_sky) + 1
        n_b = int((b_max - b_min) / self.__gap_on_the_sky) + 1
        return [[[] for i in range(n_b)] for j in range(n_l)]

    def _find_next_pointing(self, grid: list) -> SkyCoord:
        # TODO
        #   This function may be abstract and function body is better to be
        #   implemented in child class. It may depend on Satellite class.
        #   Calculation of "gain" is role of satellite? callable etc.
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
        p = Parameters.get_instance()
        self.__l0 = l0
        self.__b0 = b0
        coord_l = p.minimum_l + l0 * self.__gap_on_the_sky
        coord_b = p.minimum_b + b0 * self.__gap_on_the_sky
        return SkyCoord(l=coord_l * u.rad, b=coord_b * u.rad, frame='galactic')

    def _generate_observation_time(self, t: Time) -> Time:
        # TODO
        #   generate time sequence by using mode and orbit information
        #   array component is [time, number_of_observation]
        #   separate method.
        #   Do not implements calculation logic in factory class.
        dt = TimeDelta(13.5 * u.second)
        t = self.__satellite.next_observable_time(t, dt)
        print(t)
        return t

    def _get_position_angle(self, pointing: SkyCoord, time: Time):
        # TODO
        #   consider when position angle is needed and implementation in this
        #   class is appropriate or not.
        return self.__satellite.get_position_angle(pointing, time)

    def _make_observation(self, t: Time, pointing_plan: PointingPlan, grid: list) -> list:
        # TODO
        #
        n_l = len(grid)
        n_b = len(grid[0])
        for l in range(n_l):
            for b in range(n_b):
                pass
        grid[self.__l0][self.__b0].append([t, self.__num_exposure_per_field])
        return grid


if __name__ == "__main__":
    warnings.simplefilter('ignore', category=erfa.core.ErfaWarning)
    it = Time('2020-01-01T00:00:00')
    a: PointingPlanFactory \
        = PointingPlanFactory(EnumPointingMode.FOUR_FOV_IN_ORBIT, it)
    a.create(Satellite(EnumPointingFreedom.POINTING_FIXED, it))
    # a.test_function()
    # a._find_next_pointing(a._generate_grid())
