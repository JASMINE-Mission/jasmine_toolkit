import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time, TimeDelta

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
        self.__time_per_a_fov = (p.orbital_period * 0.5 + p.maneuver_time) \
            / enum.value
        self.__num_exposure_per_field = int(
            (self.__time_per_a_fov - p.maneuver_time) /
            (p.exposure_time + p.read_time))

    def create(self, satellite: Satellite):
        """
        Create PointingPlan object, set observation entries, and return it.
        Returns: PointingPlan object

        """
        self.__satellite = satellite
        pointing_plan: PointingPlan = PointingPlan()
        t = self.__start
        while t < self.__end:
            pointing = pointing_plan.find_next_pointing()
            t = self._generate_observation_time(t)
            pa = self._get_position_angle(pointing, t)
            pointing_plan.make_observation(t, pa, self.__num_exposure_per_field)
            t = t + TimeDelta(self.__time_per_a_fov * u.second)
            print(t)
        return pointing_plan

    def _generate_observation_time(self, t: Time) -> Time:
        dt = TimeDelta(13.5 * u.second)
        t = self.__satellite.next_observable_time(t, dt)
        print(t)
        return t

    def _get_position_angle(self, pointing: SkyCoord, time: Time):
        return self.__satellite.get_position_angle(pointing, time)
