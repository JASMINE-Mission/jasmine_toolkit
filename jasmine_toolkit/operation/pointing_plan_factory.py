import astropy.units as u
from astropy.time import Time, TimeDelta

from jasmine_toolkit.operation.fov_change_mode import EnumFovChangeMode
from jasmine_toolkit.operation.pointing_mode import EnumPointingMode
from jasmine_toolkit.operation.pointing_plan import PointingPlan
from jasmine_toolkit.satellite.satellite import Satellite
from jasmine_toolkit.utils.parameters import Parameters


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
        """
        self.__start: Time = start
        self.__end: Time = start + duration
        self.__satellite: Satellite = None
        p: Parameters = Parameters.get_instance()
        self.__mode = enum
        self.__time_per_a_fov = p.orbital_period * 0.5 / enum.value
        self.__observation_sequence = []
        self.__max_exposure_per_field = int(
            (self.__time_per_a_fov - p.maneuver_time) /
            (p.exposure_time + p.read_time))

    def create(self, satellite: Satellite):
        """
        Create PointingPlan object, set observation entries, and return it.
        Returns: PointingPlan object

        """
        self.__satellite = satellite
        pointing_plan: PointingPlan = PointingPlan()
        p: Parameters = Parameters.get_instance()
        dt = TimeDelta(13.5 * u.second)
        self._set_time_sequence(dt, p, satellite)
        self._set_pointing_and_pa(pointing_plan, satellite)
        return pointing_plan

    def _set_pointing_and_pa(self, pointing_plan, satellite):
        pointing = pointing_plan.find_next_pointing()
        for os in self.__observation_sequence:
            if os[2] == EnumFovChangeMode.NEW:
                pointing = pointing_plan.find_next_pointing()
            else:
                pointing = pointing_plan.pointing_by_small_maneuver(pointing,
                                                                    os[2])
            pa = satellite.get_position_angle(pointing, os[0])
            pointing_plan.make_observation(os[0], pa, os[1])

    def _set_time_sequence(self, dt, p, satellite):
        t = self.__start
        fov_count = 0
        strategy = [EnumFovChangeMode.NEW, EnumFovChangeMode.VERTICAL,
                    EnumFovChangeMode.NEW, EnumFovChangeMode.HORIZONTAL]

        while t < self.__end:
            fov_mod = fov_count % 4
            n = satellite.observation_count(t, dt,
                                            self.__max_exposure_per_field)
            td = dt * n
            if fov_mod % 2 == 0:
                td = td + TimeDelta(p.maneuver_time * u.second)
            else:
                td = td + TimeDelta(p.large_maneuver_time * u.second)
            fov_mode = strategy[fov_mod]

            if not n == 0:
                self.__observation_sequence.append([t + dt * n / 2,
                                                    n, fov_mode])
            fov_count = fov_count + 1
            t = t + td
            if not n == self.__max_exposure_per_field:
                fov_count = 0
                t = satellite.next_observable_time(t, dt)
