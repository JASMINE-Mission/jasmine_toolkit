import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time, TimeDelta

from jasmine_toolkit.operation.pointing_freedom import EnumPointingFreedom
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
        t = self.__start
        observation_sequence = []
        fov_count = 0
        # if fov_count is even, observing after small maneuver
        #   fov_count = 0 means vertical, fov_count = 2 means horizontal
        #   shift of FOV
        # if fov_count is odd, observing after large maneuver
        while t < self.__end:
            n = satellite.observation_count(t, dt, self.__max_exposure_per_field)
            # print(str(n) + ", " + str(t) + ", " + str(fov_count))
            observation_sequence.append([t, n, fov_count])
            t = t + dt * n
            fov_count = fov_count + 1
            if fov_count == 4:
                fov_count = 0
            if fov_count == 1 or fov_count == 3:
                t = t + TimeDelta(p.large_maneuver_time * u.second)
            else:
                t = t + TimeDelta(p.maneuver_time * u.second)
            if not n == self.__max_exposure_per_field:
                fov_count = 0
                t = satellite.next_observable_time(t, dt)
        for os in observation_sequence:
            print(os[2])
#            if os[2] == 0:
            pass
        while t < self.__end:
            pointing: SkyCoord = pointing_plan.find_next_pointing()
            # t = self._find_next_observation_time(t)
            t = satellite.next_observable_time(t, dt)
            # pa = self._get_position_angle(pointing, t)
            pa = satellite.get_position_angle(pointing, t)
            # TODO should implement
            # n = self._number_of_exposure() max value is __num_exposure_per_field
            pointing_plan.make_observation(t, pa, self.__max_exposure_per_field) # last arg should be n
            t = t + TimeDelta(self.__time_per_a_fov * u.second)
            print(t)
        return pointing_plan


if __name__ == '__main__':
    start_time = Time('2028-01-01T00:00:00', scale="tcb")
    ppf = PointingPlanFactory(EnumPointingMode.FOUR_FOV_IN_ORBIT, start_time,
                              TimeDelta(0.2 * u.d))
    pp = ppf.create(Satellite(EnumPointingFreedom.POINTING_FIXED, start_time))
