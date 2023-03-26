from astropy.time import Time, TimeDelta
import astropy.units as u
from jasmine_toolkit.operation.pointing_freedom import EnumPointingFreedom
from jasmine_toolkit.operation.pointing_mode import EnumPointingMode
from jasmine_toolkit.operation.pointing_plan_factory import PointingPlanFactory
from jasmine_toolkit.satellite.satellite import Satellite


def test_create():
    start_time = Time('2028-01-01T00:00:00', scale="tcb")
    s = Satellite(EnumPointingFreedom.POINTING_FIXED, start_time)
    ppf = PointingPlanFactory(EnumPointingMode.FOUR_FOV_IN_ORBIT, start_time,
                              TimeDelta(0.02 * u.d))
    pp = ppf.create(s)
    array = pp.get_array()
    assert len(array) == 49
    assert len(array[0]) == 28
